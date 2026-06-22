"""
BFS e DFS sobre o GrafoProjecao.

Critério 4: implementação própria, sem networkx nem similar.

Estratégia de pontuação
-----------------------
A partir de cada música-semente (avaliada pelo usuário), percorremos o
grafo de projeção até `profundidade_max`.  O peso acumulado ao longo do
caminho é calculado como produto dos pesos das arestas percorridas —
caminhos por arestas fortes valem mais do que caminhos longos por
arestas fracas.

A pontuação final de cada candidato é a soma das contribuições de todas
as sementes que o alcançaram, ponderadas pela nota que o usuário deu à
semente de origem.

Saída: dict[musica_id, pontuacao_acumulada]
"""

from collections import deque
from src.structures.grafo_projecao import GrafoProjecao


# ------------------------------------------------------------------ #
#  BFS                                                                #
# ------------------------------------------------------------------ #
"""
    Busca em largura a partir de `origem` até `profundidade_max`.
    
    dict[musica_id, pontuacao] – exclui a própria origem.
    Pontuação = produto dos pesos das arestas percorridas até o nó.
    Se um nó for alcançado por múltiplos caminhos, acumula a soma.  
"""

def bfs(
    grafo: GrafoProjecao,
    origem: int,
    profundidade_max: int = 2,
) -> dict[int, float]:
    
    if origem not in grafo._adj:
        return {}

    # visitados guarda o MELHOR peso acumulado já registrado para cada nó
    visitados: dict[int, float] = {origem: 1.0}
    fila: deque[tuple[int, int, float]] = deque()
    # (no_atual, profundidade_atual, peso_acumulado)
    fila.append((origem, 0, 1.0))
    candidatos: dict[int, float] = {}

    while fila:
        no_atual, prof_atual, peso_acum = fila.popleft()

        if prof_atual >= profundidade_max:
            continue

        for vizinho, peso_aresta in grafo.vizinhos(no_atual):
            novo_peso = peso_acum * peso_aresta

            # Explora mesmo se já visitado, mas apenas se encontramos
            # um caminho mais pesado (acumula contribuições)
            melhor_anterior = visitados.get(vizinho, 0.0)

            if vizinho != origem:
                candidatos[vizinho] = candidatos.get(vizinho, 0.0) + novo_peso

            # Só coloca na fila se ainda pode expandir e encontrou caminho novo
            if vizinho not in visitados or novo_peso > melhor_anterior:
                visitados[vizinho] = max(melhor_anterior, novo_peso)
                fila.append((vizinho, prof_atual + 1, novo_peso))

    return candidatos


# ------------------------------------------------------------------ #
#  DFS                                                                #
# ------------------------------------------------------------------ #

"""
    Busca em profundidade iterativa a partir de `origem` até `profundidade_max`.
    Retorna:
    dict[musica_id, pontuacao] – exclui a própria origem.
    Pontuação = produto dos pesos das arestas percorridas até o nó.
    Múltiplos caminhos para o mesmo nó são acumulados.
    """

def dfs(
    grafo: GrafoProjecao,
    origem: int,
    profundidade_max: int = 2,
) -> dict[int, float]:

    if origem not in grafo._adj:
        return {}

    visitados: dict[int, float] = {origem: 1.0}
    # pilha LIFO: (no_atual, profundidade_atual, peso_acumulado)
    pilha: list[tuple[int, int, float]] = [(origem, 0, 1.0)]
    candidatos: dict[int, float] = {}

    while pilha:
        no_atual, prof_atual, peso_acum = pilha.pop()

        if prof_atual >= profundidade_max:
            continue

        for vizinho, peso_aresta in grafo.vizinhos(no_atual):
            novo_peso = peso_acum * peso_aresta
            melhor_anterior = visitados.get(vizinho, 0.0)

            if vizinho != origem:
                candidatos[vizinho] = candidatos.get(vizinho, 0.0) + novo_peso

            if vizinho not in visitados or novo_peso > melhor_anterior:
                visitados[vizinho] = max(melhor_anterior, novo_peso)
                pilha.append((vizinho, prof_atual + 1, novo_peso))

    return candidatos


# ------------------------------------------------------------------ #
#  Recomendação a partir de sementes                                  #
# ------------------------------------------------------------------ #
"""
    Gera recomendações para um usuário a partir de suas músicas semente.
    Retorna:
    list[(musica_id, pontuacao)] – top_n recomendações em ordem decrescente
"""

def recomendar_para_usuario(
    grafo: GrafoProjecao,
    sementes: list[tuple[int, float]],
    musicas_ja_ouvidas: set[int] | None = None,
    profundidade: int = 2,
    top_n: int = 10,
    metodo: str = "bfs",
) -> list[tuple[int, float]]:
    
    if metodo not in ("bfs", "dfs"):
        raise ValueError(f"Método inválido: '{metodo}'. Use 'bfs' ou 'dfs'.")

    busca = bfs if metodo == "bfs" else dfs
    excluidos = musicas_ja_ouvidas or set()
    excluidos = excluidos | {mid for mid, _ in sementes}

    scores: dict[int, float] = {}

    for musica_id, nota in sementes:
        candidatos = busca(grafo, musica_id, profundidade)
        for cand_id, peso_caminho in candidatos.items():
            if cand_id not in excluidos:
                # Pondera pelo rating do usuário à semente
                scores[cand_id] = scores.get(cand_id, 0.0) + nota * peso_caminho

    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranking[:top_n]


# ------------------------------------------------------------------ #
#  Utilitário: extrair sementes de um usuário                         #
# ------------------------------------------------------------------ #

"""
    Extrai as músicas-semente de um usuário a partir de suas interações.
    Retorna:
    list[(musica_id, nota)] ordenada de forma decrescente por nota
"""

def extrair_sementes(
    interacoes_usuario: list[tuple[int, str, float | None]],
    top_k: int = 5,
    nota_minima: float = 3.0,
) -> list[tuple[int, float]]:
    
    avaliadas = [
        (mid, nota)
        for mid, _tipo, nota in interacoes_usuario
        if nota is not None and nota >= nota_minima
    ]
    avaliadas.sort(key=lambda x: x[1], reverse=True)
    return avaliadas[:top_k]