# Base de dados

A base é fictícia e foi pensada para ser **coerente**, e não apenas aleatória. São três
coleções com schema congelado (mudar o schema afeta o trabalho de todo o grupo). Os
arquivos ficam em `data/` no formato CSV.

## musicas.csv — 60 músicas

| campo | tipo | observação |
|---|---|---|
| `id` | int | único |
| `titulo` | string | exibição |
| `artista` | string | exibição (não é vértice) |
| `genero` | string | um de 8 gêneros |
| `ano` | int | 1958–2025 |
| `energia` | float | 0–1 |
| `dancabilidade` | float | 0–1 |
| `valencia` | float | 0–1 (humor: triste → feliz) |
| `tempo_bpm` | int | 60–200 (normalizar antes do cosseno) |

Gêneros usados: Sertanejo, MPB, Bossa Nova, Samba, Pagode, Funk, Forró e Rock Nacional.

## usuarios.csv — 25 usuários

| campo | tipo | observação |
|---|---|---|
| `id` | int | único |
| `nome` | string | exibição |
| `generos_preferidos` | lista | separada por `\|`, usada no cold-start |

## interacoes.csv — ~420 interações

| campo | tipo | observação |
|---|---|---|
| `usuario_id` | int | origem da aresta |
| `musica_id` | int | destino da aresta |
| `tipo` | string | avaliacao, interesse ou compartilhamento |
| `nota` | int | 0–10, só quando tipo = avaliacao |

A nota só existe quando o tipo é `avaliacao`. Para `interesse` e `compartilhamento` o peso
da aresta é derivado do tipo (sugestão: interesse = 0,6 e compartilhamento = 0,8, numa escala
onde nota 10 = 1,0). O peso não é armazenado, é calculado a partir de tipo + nota.

## Coerência garantida

- **Atributos batem com o gênero.** Cada gênero tem uma faixa plausível de energia,
  dançabilidade, valência e BPM. Bossa Nova fica calma e lenta; Funk fica agitado e rápido.
  Não existe balada com energia 0,9.
- **Gosto reflete nas interações.** Cerca de 80% das interações de cada usuário caem nos
  seus gêneros preferidos, e as notas dentro do gosto são mais altas.
- **Densidade suficiente.** Toda música tem pelo menos 3 interações (média ~7), para que a
  projeção música–música tenha coocorrência e não saia vazia.

## Validação

Os dados passam por checagens automáticas antes de serem salvos:

- ids sem duplicata em usuários e músicas;
- toda interação aponta para usuário e música existentes;
- nota dentro de 0–10;
- nenhuma música com menos de 3 interações.
