# Definição do problema

Queremos recomendar músicas para usuários a partir de duas fontes de informação:

1. o **histórico de interações** de cada usuário (avaliações, interesse e compartilhamento);
2. a **similaridade entre as músicas** com base em seus atributos (gênero, energia,
   dançabilidade, valência, BPM e ano).

A recomendação é modelada sobre um **grafo bipartido** usuário–música. A partir dele
derivamos a projeção música–música (músicas conectadas quando avaliadas pelos mesmos
usuários) e usamos os atributos numéricos para medir proximidade entre faixas.

## Por que grafo

O problema é naturalmente relacional: quem interagiu com o quê. Um grafo bipartido
representa isso de forma direta e permite caminhar entre usuários e músicas para
encontrar vizinhanças e padrões de coocorrência.

## O caso do usuário novo (cold-start)

Um usuário recém-criado quase não tem avaliações, então o método colaborativo "não sabe"
com quem ele se parece. A base trata isso de duas formas:

- **`generos_preferidos`** — dá um ponto de partida mesmo sem nenhum histórico.
- **tipos de interação mais leves** (`interesse`, `compartilhamento`) — criam arestas no
  grafo antes do usuário dar a primeira nota, ligando ele à rede mais cedo.

## Restrições do trabalho

- Os algoritmos principais de grafos são implementados **à mão**.
- Bibliotecas externas entram só como apoio (geração de dados).
- Código modular e orientado a objetos.
