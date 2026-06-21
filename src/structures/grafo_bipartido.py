from src.models.usuario import Usuario
from src.models.musica import Musica
from src.pesos import peso_interacao


class GrafoBipartido:
    """
    Grafo bipartido e ponderado usuário-música.

    Documentação explícita (critério 3):

      Vértices: dois conjuntos disjuntos.
        - U: usuários  (identificados por usuario_id)
        - M: músicas   (identificadas por musica_id)
        Os ids dos dois conjuntos podem se sobrepor (ambos começam em 1), por
        isso as consultas distinguem o lado pelo método/parâmetro.

      Arestas: existe aresta (u, m) quando há interação do usuário u com a
        música m. O grafo guarda a interação dos DOIS lados (lista de
        adjacência dupla), para recuperar tanto as músicas de um usuário
        quanto os usuários de uma música em O(grau).

      Peso: NÃO é armazenado — é derivado de (tipo, nota) por
        `src.pesos.peso_interacao`, numa escala onde nota 10 = 1,0
        (avaliacao = nota/10; interesse = 0,6; compartilhamento = 0,8).
        Optou-se por nota/10 (min-max) e não por (nota - média_do_usuário):
        centralizar pela média produz pesos negativos, que quebrariam a
        não-negatividade do cosseno usado na projeção e a leitura 0–1.

      Relações: cada item de adjacência é a tripla (id_vizinho, tipo, nota),
        preservando o tipo e a nota crus; o peso é calculado sob demanda.

    Encapsulamento: o estado (_usuarios, _musicas, _adj, _adj_musicas) é
    privado. Os outros módulos (projeção, recomendação, análise) devem usar
    APENAS os métodos públicos abaixo, sem tocar nos atributos `_`.

    Representação: listas de adjacência indexadas por id (dicionário = tabela
    hash dá acesso O(1) ao vértice e à sua lista).
    """

    def __init__(self) -> None:
        self._usuarios: dict[int, Usuario] = {}
        self._musicas: dict[int, Musica] = {}
        # usuario_id -> [(musica_id, tipo, nota)]
        self._adj: dict[int, list[tuple[int, str, float | None]]] = {}
        # musica_id -> [(usuario_id, tipo, nota)]
        self._adj_musicas: dict[int, list[tuple[int, str, float | None]]] = {}

    # ------------------------------------------------------------ construção
    def adicionar_usuario(self, usuario: Usuario) -> None:
        self._usuarios[usuario.id] = usuario
        self._adj.setdefault(usuario.id, [])

    def adicionar_musica(self, musica: Musica) -> None:
        self._musicas[musica.id] = musica
        self._adj_musicas.setdefault(musica.id, [])

    def adicionar_interacao(self, id_usuario: int, id_musica: int, tipo: str, nota: float | None) -> None:
        self._adj.setdefault(id_usuario, []).append((id_musica, tipo, nota))
        self._adj_musicas.setdefault(id_musica, []).append((id_usuario, tipo, nota))

    # ------------------------------------------------------- acesso a objetos
    def usuario(self, id_usuario: int) -> Usuario | None:
        return self._usuarios.get(id_usuario)

    def musica(self, id_musica: int) -> Musica | None:
        return self._musicas.get(id_musica)

    def usuarios(self) -> list[Usuario]:
        return list(self._usuarios.values())

    def musicas(self) -> list[Musica]:
        return list(self._musicas.values())

    def ids_usuarios(self) -> list[int]:
        return list(self._usuarios.keys())

    def ids_musicas(self) -> list[int]:
        return list(self._musicas.keys())

    def numero_usuarios(self) -> int:
        return len(self._usuarios)

    def numero_musicas(self) -> int:
        return len(self._musicas)

    def numero_interacoes(self) -> int:
        return sum(len(lista) for lista in self._adj.values())

    # ----------------------------------------------------------- vizinhanças
    def musicas_do_usuario(self, id_usuario: int) -> list[tuple[int, str, float | None]]:
        """Todas as músicas com que o usuário interagiu (com tipo e nota)."""
        return self._adj.get(id_usuario, [])

    def usuarios_da_musica(self, id_musica: int) -> list[tuple[int, str, float | None]]:
        """Todos os usuários que interagiram com a música (com tipo e nota)."""
        return self._adj_musicas.get(id_musica, [])

    def vizinhos(self, vertice: int, tipo_vertice: str = "usuario") -> list[tuple[int, str, float | None]]:
        """
        Vizinhança genérica pedida no card. Como os ids de U e M podem se
        sobrepor, `tipo_vertice` ("usuario" | "musica") diz de que lado o
        vértice está.
        """
        if tipo_vertice == "musica":
            return self.usuarios_da_musica(vertice)
        return self.musicas_do_usuario(vertice)

    def obter_vizinhos(self, id_usuario: int) -> list[tuple[int, str, float | None]]:
        """Alias de `musicas_do_usuario`, mantido por compatibilidade."""
        return self.musicas_do_usuario(id_usuario)

    def adjacencia_usuarios(self):
        """
        Itera a adjacência do lado dos usuários como pares
        (usuario_id, [(musica_id, tipo, nota), ...]). É o que a projeção
        consome — sem precisar acessar o estado interno do grafo.
        """
        return self._adj.items()

    # ----------------------------------------------------------------- pesos
    def peso(self, tipo: str, nota: float | None) -> float:
        """Peso da aresta derivado de (tipo, nota)."""
        return peso_interacao(tipo, nota)

    # --------------------------------------------------------------- utilidades
    def exibir_grafo(self) -> None:
        for id_usuario, vizinhos in self._adj.items():
            usuario = self._usuarios.get(id_usuario)
            rotulo = usuario.nome if usuario else id_usuario
            print(f"{rotulo} -> {vizinhos}")

    def __repr__(self) -> str:
        return (
            f"GrafoBipartido(usuarios={self.numero_usuarios()}, "
            f"musicas={self.numero_musicas()}, interacoes={self.numero_interacoes()})"
        )
