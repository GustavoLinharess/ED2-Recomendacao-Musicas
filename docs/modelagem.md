# Modelagem do grafo

O grafo é **bipartido e ponderado**.

## Vértices

- **Conjunto U** — usuários
- **Conjunto M** — músicas

## Arestas

Uma aresta liga um usuário a uma música quando existe interação entre eles:

```
usuario  →  musica
```

O **peso** da aresta vem do tipo da interação:

- `avaliacao` → a própria nota (0–10);
- `interesse` e `compartilhamento` → peso fixo derivado do tipo (não há nota).

O peso não é armazenado: é calculado a partir de `tipo + nota`.

## Representação

A estrutura usa **lista de adjacência**, indexada pelo id do usuário:

```
usuario_id  →  [(musica_id, tipo, nota), (musica_id, tipo, nota), ...]
```

Uma tabela hash (dicionário) dá acesso rápido a usuário e música por id.

## Projeção música–música

A partir do grafo bipartido derivamos um grafo só de músicas: duas músicas ficam conectadas
quando foram avaliadas por usuários em comum. Essa projeção é a base da recomendação
colaborativa.

O **peso** da aresta é a **similaridade de cosseno** entre os vetores de nota das duas
músicas (cada música é um vetor indexado por usuário, com o peso da interação como valor):

```
sim(a, b) = (a · b) / (||a|| × ||b||)
```

Escolhemos cosseno em vez da simples contagem de usuários em comum porque a contagem premia
músicas populares e ignora se as notas concordam; o cosseno mede concordância de gosto
normalizada, sem inflar por popularidade. O produto escalar só tem termos nos usuários em
comum; as normas usam todos os usuários de cada música.

**Filtragem mínima na origem:** não criamos aresta para coocorrência de um único usuário
(ruído). O threshold de verdade (podar arestas fracas) fica a cargo da etapa de filtragem.

**Formato congelado** (consumido pelas etapas seguintes — travessia e recomendação):

```
projecao.como_lista_adjacencia()  ->  { musica_id: [(musica_id_vizinha, peso), ...] }
projecao.vizinhos(musica_id)      ->  [(musica_id_vizinha, peso), ...]
```

## Similaridade por atributos

Cada música também é um vetor numérico:

```
musica = [energia, dancabilidade, valencia, tempo_bpm_normalizado]
```

A proximidade entre duas músicas é o **cosseno** entre esses vetores. O `tempo_bpm` precisa
ser normalizado para 0–1 antes, senão domina o cálculo por estar numa escala maior. Essa via
permite recomendar até músicas novas, que ainda não têm interações no grafo.
