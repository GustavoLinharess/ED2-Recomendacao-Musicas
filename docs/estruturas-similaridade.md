# Estruturas de Dados e Similaridade por Atributos

Esta seção documenta a implementação da tabela hash própria (estruturas de
indexação) e da segunda medida de similaridade (por atributos), conforme
exigido pelos critérios 3 e 5 do trabalho.

## 1. Hash Table própria

### Por que uma estrutura própria?

O projeto precisa responder, repetidamente e em grande volume, a três perguntas:

- Quais músicas um usuário ouviu?
- Quais usuários ouviram uma música?
- Quais são os atributos (vetor de características) de uma música?

Essas consultas são feitas **milhares de vezes** durante a construção da
projeção do grafo música-música e durante a geração de recomendações. Usar
uma lista comum para isso custaria **O(n)** por consulta (é necessário
percorrer todos os elementos até achar o procurado), o que tornaria a
construção da projeção **O(n²)** ou pior.

Para resolver isso, implementamos uma `HashTable` própria
(`src/structures/hash_table.py`), com tratamento de colisão por
**encadeamento (chaining)**: cada posição da tabela (bucket) guarda uma
lista ligada de pares chave-valor.

### Como funciona

1. Uma função hash (`hash(key) % capacidade`) calcula em qual bucket a
   chave deve ser guardada — operação O(1), independente do tamanho dos
   dados.
2. Se duas chaves caem no mesmo bucket (colisão), elas formam uma
   pequena lista ligada dentro daquele bucket.
3. A tabela mantém um **fator de carga máximo de 0.75** (no máximo 0.75
   item por bucket, em média). Quando esse limite é ultrapassado, a
   tabela dobra de tamanho automaticamente (`resize`) e todos os itens
   são reposicionados — isso mantém o número médio de itens por bucket
   baixo e constante.

### Análise de complexidade

| Operação | Complexidade média | Pior caso |
|---|---|---|
| Inserir | O(1) | O(n) |
| Buscar | O(1) | O(n) |
| Remover | O(1) | O(n) |

O pior caso (O(n)) só ocorreria se todas as chaves colidissem no mesmo
bucket, o que é estatisticamente improvável com uma boa função hash e é
mitigado pelo controle do fator de carga.

**Impacto no projeto:** ao usar a HashTable para os três índices abaixo,
a construção da projeção do grafo passa a custar **O(n)** no total
(proporcional ao número de interações), em vez de **O(n²)**, que seria o
custo se cada consulta fosse feita por busca linear em uma lista.

### Os três índices (`IndexadorMusicas`)

Implementados em `src/structures/indexador_musicas.py`, todos construídos
sobre a `HashTable` própria:

```python
usuario_para_musicas:  usuario_id -> set(musica_id)
musica_para_usuarios:  musica_id  -> set(usuario_id)
musica_para_atributos: musica_id  -> vetor_de_atributos
```

---

## 2. Similaridade por atributos (segunda medida)

### Objetivo

Enquanto a coocorrência mede comportamento (quem ouviu o quê em comum), a
similaridade por atributos mede **conteúdo**: duas músicas são parecidas
se têm gênero e características sonoras (energia, dançabilidade,
valência, BPM) parecidas — independente de quem as ouviu. Isso resolve o
problema do **cold-start**: músicas novas, sem nenhum histórico de
interação, ainda recebem uma recomendação baseada em conteúdo.

### Construção do vetor de características

Cada música é transformada em um vetor:
vetor = one-hot(gênero) + [energia, dancabilidade, valencia, tempo_bpm_normalizado]

- **Gênero** é codificado em one-hot (1 na posição do gênero da música, 0
  nas demais), já que é uma variável categórica.
- **Energia, dancabilidade e valência** já vêm normalizadas em [0, 1] no
  dataset original.
- **Tempo (BPM)** passa por normalização **min-max**, transformando seu
  intervalo original (ex.: 60 a 180) em [0, 1]. Isso é necessário porque,
  sem essa normalização, o BPM (escala muito maior que os demais
  atributos) dominaria o cálculo de similaridade.

### Cálculo da similaridade (cosseno)

A similaridade entre dois vetores é calculada pelo **cosseno do ângulo**
entre eles:
similaridade(v1, v2) = (v1 · v2) / (||v1|| × ||v2||)
Onde `v1 · v2` é o produto escalar e `||v||` é a norma (magnitude) do
vetor. O resultado varia de 0 (nenhuma similaridade) a 1 (vetores
idênticos), já que todos os componentes dos vetores são não-negativos.

A raiz quadrada usada no cálculo da norma foi implementada manualmente
(Método de Newton-Raphson), sem depender da biblioteca `math`.

### Saída

A função `construir_matriz_similaridade()` gera uma lista de arestas
`(musica_a, musica_b, peso)`, com `peso` sendo a similaridade do cosseno
entre as duas músicas. Essa lista funciona como um segundo grafo
música-música, complementar ao grafo de coocorrência.

---

## 3. Análise de Similaridades e Agrupamentos

Resultados obtidos ao rodar `python -m src.analise.analise_similaridades`
sobre os dados atuais do projeto (60 músicas, 25 usuários):

### Visão geral

- Total de pares possíveis de música-música: **1.770**
- Pares com coocorrência > 0 (pelo menos um usuário em comum): **1.488 (84,1%)**
- Similaridade de atributos — média: **0,5469**, mínima: **0,1649**, máxima: **0,9999**

### Distribuição dos pesos de similaridade de atributos

| Faixa | Pares | % |
|---|---|---|
| 0.0 – 0.5 | 852 | 48,1% |
| 0.5 – 0.7 | 690 | 39,0% |
| 0.7 – 0.85 | 3 | 0,2% |
| 0.85 – 0.95 | 7 | 0,4% |
| 0.95 – 1.0 | 218 | 12,3% |

Observa-se uma lacuna entre 0,7 e 0,85: como o gênero é codificado em
one-hot (componente binário forte no vetor), pares do **mesmo gênero**
tendem a ter similaridade muito alta (>0,95), enquanto pares de
**gêneros diferentes** ficam quase todos abaixo de 0,7. O gênero acaba
sendo o fator dominante na medida de similaridade por atributos.

### Concordância entre as duas medidas

A correlação de Pearson entre coocorrência e similaridade de atributos
(nos pares que coocorrem) é de **0,5517** — uma correlação moderada e
positiva: em geral, usuários tendem a ouvir junto músicas que também são
parecidas em conteúdo, mas a relação não é forte o suficiente pra dizer
que uma medida substitui a outra.

**Exemplo de concordância:** o grupo de músicas de Samba ("Coração em
Salvador", "Beijo do Norte", "Calor Perdido", "Estrada Feliz", "Chuva na
Chuva") aparece simultaneamente no topo da coocorrência (8–9 usuários em
comum) e da similaridade de atributos (0,98–0,999). Esses são os casos
"seguros" de recomendação, onde as duas medidas se reforçam.

**Exemplo de divergência:** a música "Sonho Perdido" (Bossa Nova)
coocorre com "Saudade do Norte" (Rock Nacional) em 3 usuários, mas tem a
menor similaridade de atributos do dataset (0,165). Isso indica usuários
com gosto eclético, que ouvem gêneros muito diferentes em conjunto — um
padrão que só a coocorrência identifica.

**Exemplo de cold-start:** o par "Coração do Sertão" (Rock Nacional) e
"Amor Escondido" (Funk) tem similaridade de atributos de 0,709, mas
**nenhuma** coocorrência registrada. É exatamente esse tipo de caso que a
similaridade por atributos resolve — recomendar com base em conteúdo
sonoro, mesmo sem qualquer histórico de interação em comum.

### Conclusão

As duas medidas são complementares:

- A **coocorrência** captura padrões reais de comportamento (incluindo
  combinações inesperadas de gêneros), mas não funciona para músicas
  novas ou pouco avaliadas.
- A **similaridade por atributos** cobre essa lacuna (cold-start), mas
  tende a favorecer fortemente músicas do mesmo gênero, devido ao peso do
  one-hot no vetor.

Uma estratégia de combinação sugerida para a recomendação final é:
peso_final = alpha × coocorrencia_normalizada + (1 - alpha) × similaridade_atributos

Com `alpha` alto quando há dados suficientes de coocorrência para a
música, e baixo (priorizando atributos) quando a música é nova ou tem
poucas interações registradas.