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
quando foram avaliadas pelos mesmos usuários, e o peso da conexão é a quantidade de usuários
em comum. Essa projeção é a base da recomendação colaborativa.

## Similaridade por atributos

Cada música também é um vetor numérico:

```
musica = [energia, dancabilidade, valencia, tempo_bpm_normalizado]
```

A proximidade entre duas músicas é o **cosseno** entre esses vetores. O `tempo_bpm` precisa
ser normalizado para 0–1 antes, senão domina o cálculo por estar numa escala maior. Essa via
permite recomendar até músicas novas, que ainda não têm interações no grafo.
