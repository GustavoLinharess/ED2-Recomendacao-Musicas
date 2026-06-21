"""
Projeção música-música por coocorrência (Card 2 — Pedro).

A partir do grafo bipartido usuário-música derivamos um grafo só de músicas.
Duas músicas ficam conectadas quando foram avaliadas por usuários em comum.

CONTRATO CONGELADO (consumido por Ed e João) — não mudar o formato:

    projecao.como_lista_adjacencia()  ->  dict[int, list[tuple[int, float]]]
        musica_id -> [(musica_id_vizinha, peso), ...]

    projecao.vizinhos(musica_id)      ->  list[tuple[int, float]]

Escolha do peso — SIMILARIDADE DE COSSENO entre os vetores de nota:
    Cada música é um vetor indexado por usuário, cujo valor é o peso da
    interação daquele usuário (ver src/pesos.py). O peso da aresta é o cosseno
    entre os vetores de duas músicas:

        sim(a, b) = (a · b) / (||a|| * ||b||)

    Por que cosseno e não a simples contagem de usuários em comum?
    A contagem premia músicas populares (mais avaliações = mais coocorrências)
    e ignora se as notas concordam. O cosseno mede *concordância de gosto*
    normalizada: duas músicas que recebem notas parecidas dos mesmos usuários
    ficam próximas mesmo com poucas avaliações, e a popularidade pura não
    infla o peso. O produto escalar só tem termos não-nulos nos usuários em
    comum; as normas usam todos os usuários de cada música.

Filtragem mínima na origem (anti-ruído, NÃO é o threshold do Ed):
    não cria aresta para coocorrência de um único usuário. O threshold "de
    verdade" (podar arestas fracas) é responsabilidade do Ed.
"""

from src.pesos import peso_interacao
from src.structures.similaridade_atributos import raiz_quadrada


class ProjecaoMusicas:
    def __init__(self, min_usuarios_comuns: int = 2) -> None:
        self.min_usuarios_comuns = min_usuarios_comuns
        # peso canônico de cada par usuario->musica (máximo entre interações)
        self._peso_um: dict[int, dict[int, float]] = {}
        # transposta: musica -> {usuario: peso}
        self._musica_usuarios: dict[int, dict[int, float]] = {}
        # norma do vetor de cada música
        self._norma: dict[int, float] = {}
        # adjacência interna: musica -> {vizinha: peso}
        self._adj: dict[int, dict[int, float]] = {}

    # ------------------------------------------------------------------ build
    @classmethod
    def de_grafo(cls, grafo, min_usuarios_comuns: int = 2) -> "ProjecaoMusicas":
        """Fábrica: cria e já constrói a projeção a partir do grafo bipartido."""
        return cls(min_usuarios_comuns=min_usuarios_comuns).construir(grafo)

    def construir(self, grafo) -> "ProjecaoMusicas":
        """Constrói a projeção a partir do grafo bipartido do Pedro (Card 1)."""
        self._peso_um = {}
        for usuario_id, interacoes in grafo.adjacencia_usuarios():
            pesos_usuario: dict[int, float] = {}
            for musica_id, tipo, nota in interacoes:
                peso = peso_interacao(tipo, nota)
                # se o usuário interagiu mais de uma vez com a música,
                # fica o sinal mais forte
                if peso > pesos_usuario.get(musica_id, 0.0):
                    pesos_usuario[musica_id] = peso
            if pesos_usuario:
                self._peso_um[usuario_id] = pesos_usuario

        self._transpor_e_normalizar()
        self._calcular_arestas()
        return self

    def _transpor_e_normalizar(self) -> None:
        self._musica_usuarios = {}
        for usuario_id, pesos_usuario in self._peso_um.items():
            for musica_id, peso in pesos_usuario.items():
                self._musica_usuarios.setdefault(musica_id, {})[usuario_id] = peso

        self._norma = {}
        for musica_id, usuarios in self._musica_usuarios.items():
            soma_quadrados = sum(peso * peso for peso in usuarios.values())
            self._norma[musica_id] = raiz_quadrada(soma_quadrados)

    def _calcular_arestas(self) -> None:
        # produto escalar e contagem de usuários em comum por par de músicas.
        # Acumulado varrendo, para cada usuário, os pares das músicas que ele
        # avaliou -> custo O(soma grau(usuario)^2), bem abaixo de O(M^2).
        produto: dict[tuple[int, int], float] = {}
        comuns: dict[tuple[int, int], int] = {}

        for pesos_usuario in self._peso_um.values():
            itens = list(pesos_usuario.items())
            for i in range(len(itens)):
                mi, wi = itens[i]
                for j in range(i + 1, len(itens)):
                    mj, wj = itens[j]
                    par = (mi, mj) if mi < mj else (mj, mi)
                    produto[par] = produto.get(par, 0.0) + wi * wj
                    comuns[par] = comuns.get(par, 0) + 1

        self._adj = {}
        for par, qtd in comuns.items():
            if qtd < self.min_usuarios_comuns:
                continue
            a, b = par
            na, nb = self._norma[a], self._norma[b]
            if na == 0.0 or nb == 0.0:
                continue
            sim = produto[par] / (na * nb)
            if sim <= 0.0:
                continue
            self._definir_aresta(a, b, sim)

    def _definir_aresta(self, a: int, b: int, peso: float) -> None:
        self._adj.setdefault(a, {})[b] = peso
        self._adj.setdefault(b, {})[a] = peso

    # ------------------------------------------------------------- consultas
    def vizinhos(self, musica_id: int) -> list[tuple[int, float]]:
        return [(viz, peso) for viz, peso in self._adj.get(musica_id, {}).items()]

    def como_lista_adjacencia(self) -> dict[int, list[tuple[int, float]]]:
        """Formato congelado do contrato, consumido por Ed e João."""
        return {m: self.vizinhos(m) for m in self._adj}

    def grau(self, musica_id: int) -> int:
        return len(self._adj.get(musica_id, {}))

    def grau_ponderado(self, musica_id: int) -> float:
        return sum(self._adj.get(musica_id, {}).values())

    def ids_musicas(self) -> list[int]:
        """Ids das músicas que têm ao menos uma aresta na projeção (os nós)."""
        return list(self._adj.keys())

    def numero_musicas(self) -> int:
        return len(self._adj)

    def numero_arestas(self) -> int:
        return sum(len(v) for v in self._adj.values()) // 2

    def __repr__(self) -> str:
        return f"ProjecaoMusicas(musicas={len(self._adj)}, arestas={self.numero_arestas()})"
