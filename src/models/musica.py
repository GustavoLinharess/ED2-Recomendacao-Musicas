class Musica:
    """Representa uma música no sistema de recomendação."""

    def __init__(
        self,
        id: int,
        titulo: str,
        artista: str,
        genero: str,
        ano: int,
        energia: float,
        dancabilidade: float,
        valencia: float,
        tempo_bpm: int,
    ) -> None:
        self._id = id
        self._titulo = titulo
        self._artista = artista
        self._genero = genero
        self._ano = ano
        self._energia = energia
        self._dancabilidade = dancabilidade
        self._valencia = valencia
        self._tempo_bpm = tempo_bpm

    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def artista(self) -> str:
        return self._artista

    @property
    def genero(self) -> str:
        return self._genero

    @property
    def ano(self) -> int:
        return self._ano

    @property
    def energia(self) -> float:
        return self._energia

    @property
    def dancabilidade(self) -> float:
        return self._dancabilidade

    @property
    def valencia(self) -> float:
        return self._valencia

    @property
    def tempo_bpm(self) -> int:
        return self._tempo_bpm

    def __str__(self) -> str:
        return (
            f"Musica(id={self._id}, titulo='{self._titulo}', "
            f"artista='{self._artista}', genero='{self._genero}')"
        )
