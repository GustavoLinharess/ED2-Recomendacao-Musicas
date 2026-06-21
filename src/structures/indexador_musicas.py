from src.structures.hash_table import HashTable


class IndexadorMusicas:
    """
    Três índices em O(1) médio, exigidos pelo critério 3:

        usuario_para_musicas:  usuario_id (int) -> set(musica_id)
        musica_para_usuarios:  musica_id (int)  -> set(usuario_id)
        musica_para_atributos: musica_id (int)  -> vetor_atributos (list[float])
    """

    def __init__(self) -> None:
        self.usuario_para_musicas = HashTable()
        self.musica_para_usuarios = HashTable()
        self.musica_para_atributos = HashTable()

    def registrar_interacao(self, usuario_id: int, musica_id: int) -> None:
        musicas = self.usuario_para_musicas.buscar(usuario_id)
        if musicas is None:
            musicas = set()
            self.usuario_para_musicas.inserir(usuario_id, musicas)
        musicas.add(musica_id)

        usuarios = self.musica_para_usuarios.buscar(musica_id)
        if usuarios is None:
            usuarios = set()
            self.musica_para_usuarios.inserir(musica_id, usuarios)
        usuarios.add(usuario_id)

    def registrar_atributos(self, musica_id: int, vetor_atributos: list[float]) -> None:
        self.musica_para_atributos.inserir(musica_id, vetor_atributos)

    def musicas_do_usuario(self, usuario_id: int) -> set:
        return self.usuario_para_musicas.buscar(usuario_id) or set()

    def usuarios_da_musica(self, musica_id: int) -> set:
        return self.musica_para_usuarios.buscar(musica_id) or set()

    def atributos_da_musica(self, musica_id: int):
        return self.musica_para_atributos.buscar(musica_id)