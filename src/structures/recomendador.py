"""
Motor de recomendação.

Responsável por:
- recomendar para usuário existente:
    * pegar músicas semente (notas altas)
    * usar travessia BFS/DFS na projeção
    * combinar com similaridade de atributos
    * remover músicas já consumidas
    * retornar ranking

- cold-start:
    * usuário novo escolhe gêneros
    * recomendar músicas centrais desses gêneros
    * combinar com similaridade de atributos
"""

from src.structures.grafo_projecao import GrafoProjecao
from src.structures.bfs_dfs import bfs, dfs, extrair_sementes
from src.structures.similaridade_atributos import (
    similaridade_atributos,
    construir_vetores_todas_musicas,
)


# pesos da combinação das duas medidas
PESO_TRAVESSIA = 0.7
PESO_ATRIBUTOS = 0.3


def recomendar(
    usuario_id: int,
    grafo_bipartido,
    grafo_projecao: GrafoProjecao,
    vetores_atributos: dict[int, list[float]],
    metodo: str = "bfs",
    top_n: int = 10,
) -> list[tuple[int, float]]:
    """
    Recomendação para usuário existente.

    Retorna:
        [(musica_id, score), ...]
    """

    # -----------------------------
    # 1) pegar músicas já vistas
    # -----------------------------

    interacoes = grafo_bipartido.obter_vizinhos(usuario_id)

    if not interacoes:
        return []


    musicas_ja_ouvidas = {
        mid for mid, _, _ in interacoes
    }


    # -----------------------------
    # 2) criar sementes
    # -----------------------------

    sementes = extrair_sementes(
        interacoes,
        top_k=5,
        nota_minima=3.0
    )


    if not sementes:
        return []


    # -----------------------------
    # 3) rodar BFS/DFS na projeção
    # -----------------------------

    busca = bfs if metodo == "bfs" else dfs


    score_travessia = {}


    for musica, nota in sementes:

        candidatos = busca(
            grafo_projecao,
            musica,
            profundidade_max=2
        )


        for candidato, peso in candidatos.items():

            if candidato in musicas_ja_ouvidas:
                continue


            score_travessia[candidato] = (
                score_travessia.get(candidato, 0)
                + nota * peso
            )


    # -----------------------------
    # 4) adicionar similaridade de atributos
    # -----------------------------


    ranking = {}


    for candidato, score in score_travessia.items():

        melhor_sim = 0.0


        for semente, _nota in sementes:

            sim = similaridade_atributos(
                vetores_atributos[candidato],
                vetores_atributos[semente]
            )

            melhor_sim = max(
                melhor_sim,
                sim
            )


        score_final = (
            PESO_TRAVESSIA * score
            +
            PESO_ATRIBUTOS * melhor_sim
        )


        ranking[candidato] = score_final



    # -----------------------------
    # 5) ordenar top 10
    # -----------------------------


    resultado = sorted(
        ranking.items(),
        key=lambda x: x[1],
        reverse=True
    )


    return resultado[:top_n]





def recomendar_novo(
    generos: list[str],
    musicas,
    vetores_atributos: dict[int, list[float]],
    top_n: int = 10,
) -> list[tuple[int, float]]:
    """
    Cold-start.

    Usuário escolhe gêneros.
    Retorna músicas compatíveis.

    Estratégia:
    - filtra gênero
    - calcula centroide dos gêneros
    - mede similaridade
    """

    candidatas = [
        m for m in musicas
        if m.genero in generos
    ]


    if not candidatas:
        return []


    # -----------------------------
    # calcula centroide do gênero
    # -----------------------------


    tamanho = len(
        vetores_atributos[candidatas[0].id]
    )


    centroide = [
        0.0
        for _ in range(tamanho)
    ]


    for musica in candidatas:

        vetor = vetores_atributos[musica.id]


        for i, valor in enumerate(vetor):

            centroide[i] += valor



    for i in range(tamanho):

        centroide[i] /= len(candidatas)



    # -----------------------------
    # ranking pela proximidade
    # -----------------------------


    ranking = []


    for musica in candidatas:

        sim = similaridade_atributos(
            vetores_atributos[musica.id],
            centroide
        )


        ranking.append(
            (
                musica.id,
                sim
            )
        )


    ranking.sort(
        key=lambda x: x[1],
        reverse=True
    )


    return ranking[:top_n]