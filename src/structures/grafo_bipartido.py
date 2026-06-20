from src.models.usuario import Usuario
from src.models.musica import Musica


class GrafoBipartido:

    def __init__(self) -> None:
        self._usuarios: dict[int, Usuario] = {}
        self._musicas: dict[int, Musica] = {}
        # lista de adjacência: usuario_id -> [(musica_id, tipo, nota)]
        self._adj: dict[int, list[tuple[int, str, float | None]]] = {}

    def adicionar_usuario(self, usuario: Usuario) -> None:
        self._usuarios[usuario.id] = usuario
        if usuario.id not in self._adj:
            self._adj[usuario.id] = []

    def adicionar_musica(self, musica: Musica) -> None:
        self._musicas[musica.id] = musica

    def adicionar_interacao(self, id_usuario: int, id_musica: int, tipo: str, nota: float | None) -> None:
        if id_usuario not in self._adj:
            self._adj[id_usuario] = []
        self._adj[id_usuario].append((id_musica, tipo, nota))

    def obter_vizinhos(self, id_usuario: int) -> list[tuple[int, str, float | None]]:
        return self._adj.get(id_usuario, [])

    def exibir_grafo(self) -> None:
        for uid, vizinhos in self._adj.items():
            nome = self._usuarios[uid].nome if uid in self._usuarios else uid
            print(f"{nome} -> {vizinhos}")
