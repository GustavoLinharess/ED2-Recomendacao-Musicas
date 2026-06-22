"""
Algoritmos de agrupamento sobre o GrafoProjecao.

Implementações do zero (critério 4):
  1. Union-Find com compressão de caminho e union-by-rank
  2. Componentes conexas (via Union-Find)
  3. Maximum Spanning Tree por Kruskal (arestas mais pesadas primeiro,
     para preservar as relações mais fortes entre músicas)
"""

from src.structures.grafo_projecao import GrafoProjecao


# ------------------------------------------------------------------ #
#  Union-Find (Disjoint Set Union)                                    #
# ------------------------------------------------------------------ #

class UnionFind:
    """
    Union-Find com compressão de caminho e union-by-rank.
    Complexidade:
      - Quase O(1) amortizado por operação (α de Ackermann inversa).
      - O(n) espaço.
    """

    def __init__(self, nos: list[int]) -> None:
        self._pai: dict[int, int] = {n: n for n in nos}
        self._rank: dict[int, int] = {n: 0 for n in nos}
        self._tamanho: dict[int, int] = {n: 1 for n in nos}

    def encontrar(self, x: int) -> int:
        """Retorna a raiz do conjunto de x (com path compression)."""
        while self._pai[x] != x:
            # Path halving: aponta dois níveis acima
            self._pai[x] = self._pai[self._pai[x]]
            x = self._pai[x]
        return x

    def unir(self, x: int, y: int) -> bool:
        """
        Une os conjuntos de x e y.
        Retorna True se estavam em conjuntos distintos, False se já unidos.
        """
        rx, ry = self.encontrar(x), self.encontrar(y)
        if rx == ry:
            return False
        # Union-by-rank: árvore menor aponta para a maior
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._pai[ry] = rx
        self._tamanho[rx] += self._tamanho[ry]
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        return True

    def mesmo_conjunto(self, x: int, y: int) -> bool:
        return self.encontrar(x) == self.encontrar(y)

    def tamanho_conjunto(self, x: int) -> int:
        return self._tamanho[self.encontrar(x)]

    def grupos(self) -> dict[int, list[int]]:
        """Retorna {raiz: [lista de membros]} para cada componente."""
        resultado: dict[int, list[int]] = {}
        for n in self._pai:
            raiz = self.encontrar(n)
            if raiz not in resultado:
                resultado[raiz] = []
            resultado[raiz].append(n)
        return resultado


# ------------------------------------------------------------------ #
#  Componentes Conexas                                                #
# ------------------------------------------------------------------ #

def componentes_conexas(grafo: GrafoProjecao) -> list[list[int]]:
    """
    Identifica todos os componentes conexos do grafo.
    Retorna lista de clusters, cada um sendo uma lista de musica_id.
    Ordenado do maior para o menor cluster.
    Complexidade: O(V · α(V) + E) ≈ O(V + E)
    """
    nos = grafo.nos()
    if not nos:
        return []

    uf = UnionFind(nos)

    for u, v, _peso in grafo.arestas():
        uf.unir(u, v)

    clusters = list(uf.grupos().values())
    clusters.sort(key=len, reverse=True)
    return clusters


def mapear_cluster_por_musica(clusters: list[list[int]]) -> dict[int, int]:
    """
    Retorna {musica_id: cluster_index} para acesso O(1).
    cluster_index é o índice na lista retornada por componentes_conexas.
    """
    mapa: dict[int, int] = {}
    for idx, cluster in enumerate(clusters):
        for mid in cluster:
            mapa[mid] = idx
    return mapa


# ------------------------------------------------------------------ #
#  Kruskal – Maximum Spanning Tree                                   #
# ------------------------------------------------------------------ #

def kruskal_mst(grafo: GrafoProjecao) -> list[tuple[int, int, float]]:
    """
    Constrói a Maximum Spanning Tree (MST de peso máximo) via Kruskal.
    Usamos a versão *máxima* porque queremos preservar as arestas de
    maior similaridade, formando o "esqueleto forte" do grafo.
    Retorna lista de arestas (u, v, peso) que compõem a MST.
    Complexidade: O(E log E) pelo sort + O(E · α(V)) pelo Union-Find.
    """
    nos = grafo.nos()
    if not nos:
        return []

    # Ordena decrescente para Kruskal máximo
    arestas = sorted(grafo.arestas(), key=lambda x: x[2], reverse=True)
    uf = UnionFind(nos)
    mst: list[tuple[int, int, float]] = []

    limite = len(nos) - 1  # MST tem no máximo V-1 arestas

    for u, v, peso in arestas:
        if uf.unir(u, v):
            mst.append((u, v, peso))
            if len(mst) == limite:
                break  # MST completa

    return mst


def grafo_de_mst(mst: list[tuple[int, int, float]]) -> GrafoProjecao:
    """Constrói um GrafoProjecao apenas com as arestas da MST."""
    from src.structures.grafo_projecao import GrafoProjecao
    return GrafoProjecao.de_lista_arestas(mst)


# ------------------------------------------------------------------ #
#  Relatório de agrupamento                                           #
# ------------------------------------------------------------------ #

def relatorio_clusters(
    clusters: list[list[int]],
    nomes: dict[int, str] | None = None,
    top_n_exibir: int = 5,
) -> None:
    """
    Imprime um resumo dos clusters encontrados.
    """
    tamanhos = [len(c) for c in clusters]
    total_nos = sum(tamanhos)

    print("=" * 60)
    print("RELATÓRIO DE AGRUPAMENTO (COMPONENTES CONEXAS)")
    print("=" * 60)
    print(f"  Total de clusters : {len(clusters)}")
    print(f"  Total de nós      : {total_nos}")
    print(f"  Maior cluster     : {tamanhos[0]} nós")
    print(f"  Menor cluster     : {tamanhos[-1]} nós")
    media = sum(tamanhos) / len(tamanhos) if tamanhos else 0
    print(f"  Tamanho médio     : {media:.1f} nós")
    isolados = sum(1 for t in tamanhos if t == 1)
    print(f"  Nós isolados      : {isolados}")

    # Distribuição por faixas de tamanho
    faixas = {"1": 0, "2-5": 0, "6-20": 0, "21-100": 0, ">100": 0}
    for t in tamanhos:
        if t == 1:
            faixas["1"] += 1
        elif t <= 5:
            faixas["2-5"] += 1
        elif t <= 20:
            faixas["6-20"] += 1
        elif t <= 100:
            faixas["21-100"] += 1
        else:
            faixas[">100"] += 1
    print("\n  Distribuição de tamanhos:")
    for faixa, qtd in faixas.items():
        pct = 100 * qtd / len(clusters) if clusters else 0
        barra = "█" * int(pct / 2)
        print(f"    {faixa:>6} nós: {qtd:4d} clusters ({pct:5.1f}%) {barra}")

    # Detalhe dos maiores clusters
    print(f"\n  Top {min(top_n_exibir, len(clusters))} maiores clusters:")
    for i, cluster in enumerate(clusters[:top_n_exibir]):
        exemplos = cluster[:5]
        if nomes:
            exemplos_str = ", ".join(
                nomes.get(mid, str(mid)) for mid in exemplos
            )
        else:
            exemplos_str = ", ".join(str(mid) for mid in exemplos)
        sufixo = "..." if len(cluster) > 5 else ""
        print(f"    Cluster {i+1}: {len(cluster)} nós → [{exemplos_str}{sufixo}]")
    print("=" * 60)