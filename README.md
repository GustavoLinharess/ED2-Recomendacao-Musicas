# 🎵 Sistema de Recomendação de Músicas

Projeto da disciplina de **Estruturas de Dados II** — Engenharia de Software, Universidade de Brasília (UnB).

Sistema de recomendação de músicas construído sobre **grafos implementados à mão**, combinando
duas estratégias: recomendação **colaborativa** (quem ouve o quê em comum) e por **conteúdo**
(similaridade entre os atributos sonoros das músicas).

📖 **Documentação completa:** https://gustavolinharess.github.io/ED2-Recomendacao-Musicas/

---

## Como funciona

O sistema é um pipeline que parte dos dados brutos e termina em recomendações:

```
CSVs  →  grafo bipartido  →  projeção música-música  →  filtragem  →  travessia (BFS/DFS)  →  recomendação
        (usuário × música)    (coocorrência/cosseno)    (threshold)   + similaridade de atributos
```

1. **Grafo bipartido** usuário × música, com peso derivado do tipo de interação (avaliação, interesse, compartilhamento).
2. **Projeção música-música** por coocorrência, usando cosseno para medir concordância de gosto sem inflar por popularidade.
3. **Filtragem** por threshold para remover arestas fracas (ruído) sem perder cobertura do catálogo.
4. **Travessia BFS/DFS** a partir das músicas que o usuário mais gostou (sementes).
5. **Recomendação** combinando a travessia (70%) com a similaridade de atributos (30%), com tratamento de **cold-start** para usuários novos.

Estruturas de apoio: **HashTable própria** (acesso O(1) por id) e **similaridade por atributos** (vetor sonoro + cosseno).

---

## Estrutura do projeto

```
ED2-Recomendacao-Musicas/
├── data/                       # base fictícia (musicas, usuarios, interacoes)
├── docs/                       # site de documentação (docsify + GitHub Pages)
├── src/
│   ├── models/                 # Usuario, Musica
│   ├── carregar_dados.py       # leitura dos CSVs → grafo
│   ├── pesos.py                # convenção única de peso das arestas
│   ├── structures/
│   │   ├── grafo_bipartido.py      # grafo usuário × música
│   │   ├── projecao_musicas.py     # projeção por coocorrência (cosseno)
│   │   ├── grafo_projecao.py       # grafo de projeção + densidade
│   │   ├── filtragem.py            # poda por threshold
│   │   ├── bfs_dfs.py              # travessias
│   │   ├── agrupamento.py          # componentes conexas + Kruskal (MST)
│   │   ├── hash_table.py           # tabela hash própria (chaining)
│   │   ├── indexador_musicas.py    # índices usuário/música/atributos
│   │   ├── similaridade_atributos.py  # vetor sonoro + cosseno
│   │   └── recomendador.py         # motor de recomendação
│   └── analise/                # análise de similaridades e padrões
└── main.py                     # demonstração ponta a ponta
```

---

## Como executar

**Pré-requisito:** Python 3.10+ (e `pandas` + `faker` apenas para regenerar os dados).

```bash
git clone https://github.com/GustavoLinharess/ED2-Recomendacao-Musicas.git
cd ED2-Recomendacao-Musicas
python main.py
```

`main.py` roda o pipeline inteiro: carrega os dados, monta o grafo, gera a projeção, filtra,
recomenda para um usuário de exemplo e exibe os agrupamentos.

---

## Principais resultados

- Projeção com **60 músicas** e **946 arestas** (densidade 0,53); o threshold **0,5** é o ponto de
  equilíbrio (mantém 24% das arestas com peso médio 0,72, perdendo cobertura de só 1 música).
- O agrupamento identifica **2 clusters** reais de gosto, sem nenhuma música isolada.
- A **MST (Kruskal)** revela músicas "âncora" de alta centralidade, úteis como sementes de recomendação.
- BFS e DFS convergem nos caminhos de alta similaridade, validando a pontuação por produto de pesos.

Análise detalhada na [documentação](https://gustavolinharess.github.io/ED2-Recomendacao-Musicas/#/analise-resultados).

---

## Divisão por integrante

| Integrante | Parte no projeto |
|---|---|
| **Gustavo** | Base de dados, schema, geração via LLM, carregamento dos CSVs, estrutura inicial do grafo e documentação/site |
| **Pedro** | Grafo bipartido (consultas dos dois lados) e projeção música-música por coocorrência |
| **Miguel** | HashTable própria, indexador e similaridade por atributos |
| **Esdras** | Filtragem por threshold, grafo de projeção, BFS/DFS, agrupamento (Union-Find e Kruskal) e análise dos resultados |
| **João Vitor** | Motor de recomendação (travessia + atributos) e cold-start |

---

## Equipe

| Nome | Matrícula | GitHub |
|---|---|---|
| Esdras de Sousa Nogueira | 222006230 | [@Edzada](https://github.com/Edzada) |
| Gustavo Ribeiro Linhares | 222008691 | [@GustavoLinharess](https://github.com/GustavoLinharess) |
| João Vitor Sales Ibiapina | 222006857 | [@jv-ibiapina](https://github.com/jv-ibiapina) |
| Miguel Pires Gomes | 222007030 | [@miguelpiresgomes25](https://github.com/miguelpiresgomes25) |
| Pedro Henrique Faria da Mota | 222007086 | [@phfariaa](https://github.com/phfariaa) |

---

**Estruturas de Dados II** — Engenharia de Software — UnB
