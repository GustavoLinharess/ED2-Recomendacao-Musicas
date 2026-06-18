class Usuario:
    """Representa um usuário do sistema de recomendação."""

    def __init__(self, id: int, nome: str) -> None:
        self._id: int = id
        self._nome: str = nome

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

    def __str__(self) -> str:
        return f"Usuario(id={self._id}, nome='{self._nome}')"
