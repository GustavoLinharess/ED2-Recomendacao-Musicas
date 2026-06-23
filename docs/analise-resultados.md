# Análise e Interpretação dos Resultados

> Critério 5 — Padrões, agrupamentos, similaridades e métricas extraídas do grafo de projeção música-música.

---

## Sumário

1. [Comportamento da projeção música-música](#1-comportamento-da-projeção-música-música)
2. [Efeito da filtragem sobre a estrutura do grafo](#2-efeito-da-filtragem-sobre-a-estrutura-do-grafo)
3. [Agrupamentos e padrões de consumo](#3-agrupamentos-e-padrões-de-consumo)
4. [Centralidade e músicas âncora](#4-centralidade-e-músicas-âncora)
5. [Qualidade das recomendações por BFS e DFS](#5-qualidade-das-recomendações-por-bfs-e-dfs)
6. [Conclusões](#6-conclusões)

---

## 1. Comportamento da projeção música-música

A projeção gerada pelo algoritmo de cosseno sobre os vetores de coocorrência produziu um grafo com **60 nós e 946 arestas** antes de qualquer filtragem, resultando em densidade de **0,53**. Esse valor elevado é esperado dado o tamanho do conjunto de dados: com poucos usuários e músicas, a probabilidade de dois itens compartilharem avaliadores em comum é naturalmente alta. Em sistemas reais de larga escala, a projeção tende a ser muito mais esparsa, o que tornaria os algoritmos de filtragem ainda mais relevantes.

A escolha do **cosseno** como métrica de similaridade mostrou-se adequada. Ao normalizar os vetores de nota, o cosseno penaliza músicas que simplesmente foram muito ouvidas (popularidade) e premia aquelas que recebem padrões de avaliação concordantes entre os mesmos usuários. Isso fica evidente nos pares de maior peso da MST: *Beijo do Norte* e *Coração em Salvador* atingiram similaridade **0,966** não por serem as músicas mais populares, mas porque os usuários que as avaliaram atribuíram notas proporcionalmente semelhantes às duas.

---

## 2. Efeito da filtragem sobre a estrutura do grafo

A análise comparativa de thresholds revelou um comportamento em três fases distintas.

| Threshold | Arestas | % mantidas | Nós ativos | Peso médio | Peso mín |
|:---------:|--------:|:-----------:|:----------:|:----------:|:--------:|
| 0,00 | 946 | 100,0% | 60 | 0,377 | 0,039 |
| 0,30 | 498 | 52,6% | 60 | 0,530 | 0,300 |
| **0,50** | **226** | **23,9%** | **59** | **0,716** | **0,501** |
| 0,60 | 175 | 18,5% | 59 | 0,764 | 0,601 |
| 0,70 | 127 | 13,4% | 57 | 0,805 | 0,702 |
| 0,80 | 60 | 6,3% | 42 | 0,867 | 0,800 |

### Fase 1 — threshold 0,0 a 0,3
O grafo perde metade das arestas (946 → 498) mas mantém todos os 60 nós ativos. As arestas removidas são predominantemente ruído: pares de músicas que compartilharam poucos usuários com notas muito distintas, gerando similaridade baixa. O peso médio sobe de 0,377 para 0,530, sinalizando que a qualidade média das relações restantes melhora significativamente com pouca perda de cobertura.

### Fase 2 — threshold 0,5 a 0,6 ✅ zona de equilíbrio
A 0,5, o grafo tem 226 arestas e peso médio 0,716 — as conexões que restam representam concordância de gosto genuína. A perda de apenas 1 nó indica que quase todas as músicas continuam alcançáveis pelo sistema de recomendação. Este é o **threshold padrão adotado** por maximizar a relação entre qualidade das arestas e cobertura do catálogo.

### Fase 3 — threshold 0,7 a 0,8
Degradação da cobertura. A 0,8, apenas 42 dos 60 nós permanecem conectados — 18 músicas ficam completamente isoladas e nunca seriam recomendadas, independentemente do histórico do usuário. Apesar do peso médio elevado (0,867), essa configuração sacrifica demais a diversidade do sistema.

---

## 3. Agrupamentos e padrões de consumo

Com threshold 0,5, o algoritmo de **componentes conexas** (via Union-Find) identifica dois clusters bem definidos.

```
Total de clusters :  2
Maior cluster     : 48 nós
Menor cluster     : 11 nós
Nós isolados      :  0
```

### Cluster principal — 48 músicas
Concentra títulos com ampla base de usuários avaliadores e variação de gênero. Músicas como *Calor Escondido*, *Flor de Verão* e *Vento Eterno* coexistem no mesmo componente porque os usuários que as consomem têm perfis de gosto sobrepostos e diversificados.

### Cluster secundário — 11 músicas
Apresenta padrão semântico distinto: *Saudade da Madrugada*, *Noite no Baile*, *Mar Sem Freio*, *Sonho que Ficou*. A concentração de títulos com temática noturna e melancólica sugere que este grupo é consumido por um subconjunto de usuários com preferências mais homogêneas e específicas.

A separação em componente distinto indica que os usuários desse perfil raramente avaliam músicas do cluster principal — ou quando o fazem, as notas não se correlacionam — o que valida o poder da projeção por cosseno em **capturar nichos de gosto**.

> A ausência de nós isolados no grafo filtrado confirma que o threshold 0,5 é conservador o suficiente para não excluir nenhuma música do alcance do recomendador.

---

## 4. Centralidade e músicas âncora

A **Maximum Spanning Tree** (Kruskal) preserva o esqueleto mais forte do grafo: as 57 arestas de maior peso que conectam todos os nós sem ciclos, com peso total de **46,02**.

| Par de músicas | Similaridade |
|----------------|:------------:|
| Beijo do Norte ↔ Coração em Salvador | 0,966 |
| Sonho na Chuva ↔ Tempo de Sol | 0,960 |
| Noite no Baile ↔ Mar do Sertão | 0,938 |
| Chuva Eterno ↔ Amor Escondido | 0,934 |
| Estrada Escondido ↔ Mar do Sertão | 0,929 |

Músicas que aparecem repetidamente nos pares de maior peso — como **Mar do Sertão** (conectada a *Noite no Baile* com 0,938 e a *Estrada Escondido* com 0,929) — funcionam como **âncoras de recomendação**: itens que, quando presentes no histórico de um usuário, abrem caminhos confiáveis para uma variedade maior de candidatos via BFS ou DFS.

Essa propriedade tem implicação prática direta: músicas de alta centralidade deveriam receber tratamento especial no sistema, seja como sementes prioritárias ou como nós de passagem em buscas de maior profundidade.

---

## 5. Qualidade das recomendações por BFS e DFS

Para o usuário 4, BFS e DFS convergiram para o mesmo resultado:

```
[BFS]  1. Estrada Escondido   score=9.1553
[DFS]  1. Estrada Escondido   score=9.1553
```

A convergência não é coincidência — ocorre porque a música semente de maior peso do usuário está diretamente conectada a *Estrada Escondido* com similaridade 0,929, o caminho mais forte disponível em profundidade 1. Quando o caminho ótimo está na primeira camada, a ordem de exploração (largura vs. profundidade) não influencia o resultado.

A divergência entre BFS e DFS tende a aparecer em usuários com sementes mais fracas ou grafos mais esparsos, onde os candidatos de profundidade 2 se tornam relevantes:

- **BFS** é mais conservador — prioriza vizinhos próximos e confiáveis.
- **DFS** pode descobrir candidatos mais distantes com combinações de pesos interessantes.

Ambos os métodos utilizam **pontuação por produto de pesos** ao longo do caminho, garantindo que rotas por arestas fracas sejam penalizadas naturalmente, sem necessidade de heurísticas adicionais.

---

## 6. Conclusões

Os resultados demonstram que a abordagem por grafo de projeção com similaridade de cosseno captura relações de gosto não triviais no catálogo musical:

- A **filtragem por threshold** elimina ruído sem destruir cobertura quando calibrada adequadamente (0,5 neste conjunto de dados).
- Os **dois clusters** identificados revelam segmentação real de público, não artefato algorítmico — o cluster secundário agrupa músicas com temática e base de fãs distintas do cluster principal.
- A **convergência de BFS e DFS** para candidatos de alta similaridade valida a consistência da pontuação acumulada por produto de pesos como critério de ranking.
- As **músicas âncora** identificadas pela MST são candidatas naturais a receber destaque em estratégias de recomendação por popularidade estrutural, complementando a abordagem personalizada por histórico do usuário.