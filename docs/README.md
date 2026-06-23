# Visão geral

Sistema de recomendação de músicas desenvolvido para a disciplina de **Estruturas de
Dados II** (Engenharia de Software — UnB).

A ideia é recomendar músicas para um usuário combinando duas estratégias:

- **Colaborativa** — usuários com gostos parecidos recebem recomendações parecidas, a partir
  das interações registradas no grafo.
- **Por conteúdo** — músicas parecidas no "som" (energia, dançabilidade, valência, BPM) são
  aproximadas pelo cosseno entre seus atributos.

## O pipeline

```
CSVs → grafo bipartido → projeção música-música → filtragem → BFS/DFS → recomendação
```

Cada etapa é uma estrutura implementada à mão, documentada nas seções ao lado.

## Como navegar

| Seção | O que tem |
|---|---|
| [Definição do problema](problema.md) | o que estamos resolvendo e por quê |
| [Base de dados](base-de-dados.md) | o schema das três coleções e as regras de coerência |
| [Geração via LLM](geracao-llm.md) | como os dados fictícios foram gerados |
| [Modelagem do grafo](modelagem.md) | vértices, arestas, pesos e projeção por cosseno |
| [Estruturas e Similaridade](estruturas-similaridade.md) | hash table própria e similaridade por atributos |
| [Motor de recomendação](recomendacao.md) | como o ranking final é montado e o cold-start |
| [Análise dos resultados](analise-resultados.md) | clusters, MST, thresholds e padrões encontrados |
| [Equipe](equipe.md) | quem está no projeto |

## Stack

- **Python** com orientação a objetos
- **Grafos e estruturas** implementados manualmente (lista de adjacência, hash table, Union-Find, Kruskal)
- **pandas** e **Faker** apenas no apoio à geração dos dados
