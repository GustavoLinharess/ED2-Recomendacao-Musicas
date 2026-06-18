from typing import Optional
from src.models.usuario import Usuario
from src.models.musica import Musica


class GrafoBipartido:
    """
    Grafo bipartido entre usuários e músicas.

    Um lado contém nós do tipo Usuario, o outro do tipo Musica.
    As arestas representam avaliações de um usuário para uma música.
    A lista de adjacência é indexada pelo id do usuário.
    """

    def __init__(self) -> None:
        # id_usuario -> Usuario
        self._usuarios: dict[int, Usuario] = {}
        # id_musica -> Musica
        self._musicas: dict[int, Musica] = {}
        # id_usuario -> lista de (id_musica, nota)
        self._avaliacoes: dict[int, list[tuple[int, float]]] = {}

    def adicionar_usuario(self, usuario: Usuario) -> None:
        """Adiciona um nó de usuário ao grafo."""
        pass

    def adicionar_musica(self, musica: Musica) -> None:
        """Adiciona um nó de música ao grafo."""
        pass

    def adicionar_avaliacao(
        self, id_usuario: int, id_musica: int, nota: float
    ) -> None:
        """Cria uma aresta entre um usuário e uma música com a nota dada."""
        pass

    def obter_vizinhos(self, id_usuario: int) -> list[tuple[int, float]]:
        """Retorna as músicas avaliadas pelo usuário como lista de (id_musica, nota)."""
        pass

    def exibir_grafo(self) -> None:
        """Imprime a lista de adjacência do grafo."""
        pass
