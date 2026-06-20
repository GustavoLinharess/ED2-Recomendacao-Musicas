# Visão geral

Sistema de recomendação de músicas desenvolvido para a disciplina de **Estruturas de
Dados II** (Engenharia de Software — UnB).

A ideia é recomendar músicas para um usuário combinando duas estratégias:

- **Colaborativa** — usuários com gostos parecidos recebem recomendações parecidas,
  a partir das interações registradas no grafo.
- **Por conteúdo** — músicas parecidas no "som" (energia, dançabilidade, valência, BPM)
  são aproximadas pelo cosseno entre seus atributos.

## Como navegar

| Seção | O que tem |
|---|---|
| [Definição do problema](problema.md) | o que estamos resolvendo e por quê |
| [Base de dados](base-de-dados.md) | o schema das três coleções e as regras de coerência |
| [Geração via LLM](geracao-llm.md) | como os dados fictícios foram gerados |
| [Modelagem do grafo](modelagem.md) | vértices, arestas, pesos e projeção |
| [Próximas etapas](roadmap.md) | o que já foi feito e o que falta |
| [Equipe](equipe.md) | quem está no projeto |

## Stack

- **Python** com orientação a objetos
- **Grafos** implementados manualmente (lista de adjacência)
- **pandas** e **Faker** apenas no apoio à geração dos dados
