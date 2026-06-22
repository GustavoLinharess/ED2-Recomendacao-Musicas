"""
GrafoProjecao: grafo não-direcionado ponderado resultante da projeção
bipartita sobre o conjunto de músicas.

Cada nó é um musica_id (int).
Cada aresta (u, v, peso) representa similaridade ou coocorrência entre músicas.

Formato de adjacência:
    _adj: dict[int, list[tuple[int, float]]]
         musica_id -> [(vizinho_id, peso), ...]

Complexidade de espaço: O(V + E)
"""

class GrafoProjecao:
    """Grafo não-direcionado ponderado para a projeção de músicas."""

    def __init__(self) -> None:
        # musica_id -> lista de (vizinho_id, peso)
        self._adj: dict[int, list[tuple[int, float]]] = {}
        self._num_arestas: int = 0

    # ------------------------------------------------------------------ #
    #  Construção                                                          #
    # ------------------------------------------------------------------ #

    def adicionar_no(self, musica_id: int) -> None:
        if musica_id not in self._adj:
            self._adj[musica_id] = []

    def adicionar_aresta(self, u: int, v: int, peso: float) -> None:
        """Adiciona aresta não-direcionada com peso. Ignora auto-laços."""
        if u == v:
            return
        self.adicionar_no(u)
        self.adicionar_no(v)
        self._adj[u].append((v, peso))
        self._adj[v].append((u, peso))
        self._num_arestas += 1

    @classmethod
    def de_lista_arestas(
        cls, arestas: list[tuple[int, int, float]]
    ) -> "GrafoProjecao":
        """Constrói o grafo a partir de uma lista (u, v, peso)."""
        g = cls()
        for u, v, peso in arestas:
            g.adicionar_aresta(u, v, peso)
        return g

    @classmethod
    def de_projecao(cls, projecao) -> "GrafoProjecao":
        """
        Adapta um ProjecaoMusicas (Card 2 – Pedro) para GrafoProjecao.

        Consome o contrato congelado:
            projecao.ids_musicas()       -> list[int]
            projecao.vizinhos(musica_id) -> list[tuple[int, float]]

        Cada aresta é inserida uma única vez (u < v) para evitar duplicata.
        """
        g = cls()
        for mid in projecao.ids_musicas():
            for viz, peso in projecao.vizinhos(mid):
                if mid < viz:           # garante inserção única por par
                    g.adicionar_aresta(mid, viz, peso)
        return g

    # ------------------------------------------------------------------ #
    #  Consultas                                                           #
    # ------------------------------------------------------------------ #

    def vizinhos(self, musica_id: int) -> list[tuple[int, float]]:
        """Retorna [(vizinho_id, peso), ...] para o nó dado."""
        return self._adj.get(musica_id, [])

    def nos(self) -> list[int]:
        return list(self._adj.keys())

    def arestas(self) -> list[tuple[int, int, float]]:
        """Retorna cada aresta uma única vez: (u, v, peso)."""
        vistas: set[tuple[int, int]] = set()
        resultado: list[tuple[int, int, float]] = []
        for u, vizs in self._adj.items():
            for v, peso in vizs:
                par = (min(u, v), max(u, v))
                if par not in vistas:
                    vistas.add(par)
                    resultado.append((u, v, peso))
        return resultado

    def grau(self, musica_id: int) -> int:
        return len(self._adj.get(musica_id, []))

    def peso_aresta(self, u: int, v: int) -> float | None:
        """Retorna o peso da aresta (u, v), ou None se não existir."""
        for viz, peso in self._adj.get(u, []):
            if viz == v:
                return peso
        return None

    # ------------------------------------------------------------------ #
    #  Métricas básicas                                                    #
    # ------------------------------------------------------------------ #

    def num_nos(self) -> int:
        return len(self._adj)

    def num_arestas(self) -> int:
        return self._num_arestas

    def densidade(self) -> float:
        n = self.num_nos()
        if n < 2:
            return 0.0
        return 2 * self._num_arestas / (n * (n - 1))

    def grau_medio(self) -> float:
        nos = self.nos()
        if not nos:
            return 0.0
        return sum(self.grau(n) for n in nos) / len(nos)

    def __len__(self) -> int:
        return self.num_nos()

    def __repr__(self) -> str:
        return (
            f"GrafoProjecao(nos={self.num_nos()}, "
            f"arestas={self.num_arestas()}, "
            f"densidade={self.densidade():.4f})"
        )