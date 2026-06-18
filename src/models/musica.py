class Musica:
    """Representa uma música no sistema de recomendação."""

    def __init__(
        self,
        id: int,
        titulo: str,
        artista: str,
        genero: str,
        descricao: str = "",
    ) -> None:
        self._id: int = id
        self._titulo: str = titulo
        self._artista: str = artista
        self._genero: str = genero
        self._descricao: str = descricao

    @property
    def id(self) -> int:
        return self._id

    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("Título não pode ser vazio.")
        self._titulo = valor

    @property
    def artista(self) -> str:
        return self._artista

    @artista.setter
    def artista(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("Artista não pode ser vazio.")
        self._artista = valor

    @property
    def genero(self) -> str:
        return self._genero

    @genero.setter
    def genero(self, valor: str) -> None:
        self._genero = valor

    @property
    def descricao(self) -> str:
        return self._descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        self._descricao = valor

    def __str__(self) -> str:
        return (
            f"Musica(id={self._id}, titulo='{self._titulo}', "
            f"artista='{self._artista}', genero='{self._genero}')"
        )
