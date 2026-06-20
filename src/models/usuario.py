class Usuario:
    """Representa um usuário do sistema de recomendação."""

    def __init__(self, id: int, nome: str, generos_preferidos: list[str] | None = None) -> None:
        self._id = id
        self._nome = nome
        self._generos_preferidos = generos_preferidos or []

    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = valor

    @property
    def generos_preferidos(self) -> list[str]:
        return self._generos_preferidos

    def __str__(self) -> str:
        return f"Usuario(id={self._id}, nome='{self._nome}')"
