# Definição do problema e geração da base

## Problema (critério 1)

O objetivo do projeto é recomendar músicas para usuários a partir de duas fontes
de informação: o histórico de interações de cada usuário (avaliações, interesse e
compartilhamento) e a similaridade entre as músicas com base em seus atributos
(gênero, energia, dançabilidade, valência, BPM e ano).

A recomendação é modelada sobre um grafo bipartido usuário–música, onde as arestas
representam interações. A partir dele derivamos a projeção música–música
(músicas conectadas quando avaliadas pelos mesmos usuários) e usamos os atributos
numéricos para medir proximidade entre faixas.

## Descrição dos dados (critério 2)

A base é fictícia e foi pensada para ser coerente, e não apenas aleatória. São três
coleções congeladas (qualquer mudança de schema afeta o restante do grupo):

### musicas.csv — 60 músicas
| campo | tipo | observação |
|---|---|---|
| id | int | único |
| titulo | string | exibição |
| artista | string | exibição (não é vértice) |
| genero | string | um de 8 gêneros |
| ano | int | 1958–2025 |
| energia | float | 0–1 |
| dancabilidade | float | 0–1 |
| valencia | float | 0–1 (humor: triste → feliz) |
| tempo_bpm | int | 60–200, normalizar antes do cosseno |

Gêneros usados: Sertanejo, MPB, Bossa Nova, Samba, Pagode, Funk, Forró e Rock Nacional.

### usuarios.csv — 25 usuários
| campo | tipo | observação |
|---|---|---|
| id | int | único |
| nome | string | exibição |
| generos_preferidos | lista | separada por `\|`, usada no cold-start |

### interacoes.csv — ~420 interações
| campo | tipo | observação |
|---|---|---|
| usuario_id | int | origem da aresta |
| musica_id | int | destino da aresta |
| tipo | string | avaliacao, interesse ou compartilhamento |
| nota | int | 0–10, só quando tipo = avaliacao |

A nota só existe quando o tipo é `avaliacao`. Para `interesse` e `compartilhamento`
o peso da aresta é derivado do tipo (sugestão: interesse = 0,6 e compartilhamento = 0,8
numa escala onde nota 10 = 1,0). O peso não é armazenado, é calculado a partir de tipo + nota.

### Coerência garantida
- **Atributos batem com o gênero.** Cada gênero tem uma faixa plausível de energia,
  dançabilidade, valência e BPM. Bossa Nova fica com energia/BPM baixos; Funk com
  energia, dançabilidade e BPM altos. Não existe balada com energia 0,9.
- **Gosto reflete nas interações.** Cerca de 80% das interações de cada usuário caem
  nos seus gêneros preferidos, e as notas dentro do gosto são mais altas.
- **Densidade suficiente.** Toda música tem pelo menos 3 interações (média ~7), para
  que a projeção música–música tenha coocorrência e não saia vazia.

### Validação
Os dados passam por checagens automáticas antes de serem salvos: ids sem duplicata,
toda interação aponta para usuário e música existentes, nota dentro de 0–10 e nenhuma
música com menos de 3 interações.

## Uso de LLM na geração (critério 6)

Os dados foram gerados com apoio de um LLM (Claude, modelo Opus 4.8).

O que foi feito com o LLM:
- definição do schema das três coleções e da convenção de pesos por tipo de interação;
- construção das faixas de atributos por gênero (os intervalos de energia, dançabilidade,
  valência, BPM e ano que mantêm cada gênero plausível);
- listas-semente de gêneros, artistas fictícios e fragmentos de títulos;
- a rotina que materializa as três coleções aplicando essas regras e a validação final.

O que foi ajustado à mão:
- revisão dos intervalos por gênero para evitar combinações estranhas;
- ajuste das quantidades (60 músicas, 25 usuários) e da concentração das interações
  para garantir coocorrência;
- conferência final dos CSVs gerados.

A semente aleatória é fixa, então a base é reproduzível.
