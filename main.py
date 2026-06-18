from src.models.usuario import Usuario
from src.models.musica import Musica
from src.structures.grafo_bipartido import GrafoBipartido


def main() -> None:
    # --- Usuários ---
    u1 = Usuario(id=1, nome="Alice")
    u2 = Usuario(id=2, nome="Bruno")
    u3 = Usuario(id=3, nome="Carla")

    print(u1)
    print(u2)
    print(u3)

    # --- Músicas ---
    m1 = Musica(id=1, titulo="Bohemian Rhapsody", artista="Queen", genero="Rock")
    m2 = Musica(id=2, titulo="Blinding Lights", artista="The Weeknd", genero="Pop")
    m3 = Musica(
        id=3,
        titulo="Lose Yourself",
        artista="Eminem",
        genero="Hip-Hop",
        descricao="Trilha sonora do filme 8 Mile.",
    )

    print(m1)
    print(m2)
    print(m3)

    # --- Grafo ---
    grafo = GrafoBipartido()

    grafo.adicionar_usuario(u1)
    grafo.adicionar_usuario(u2)
    grafo.adicionar_usuario(u3)

    grafo.adicionar_musica(m1)
    grafo.adicionar_musica(m2)
    grafo.adicionar_musica(m3)

    # Avaliações: (id_usuario, id_musica, nota de 0 a 5)
    grafo.adicionar_avaliacao(u1.id, m1.id, 5.0)
    grafo.adicionar_avaliacao(u1.id, m2.id, 3.5)
    grafo.adicionar_avaliacao(u2.id, m2.id, 4.0)
    grafo.adicionar_avaliacao(u2.id, m3.id, 4.5)
    grafo.adicionar_avaliacao(u3.id, m1.id, 2.0)

    grafo.exibir_grafo()


if __name__ == "__main__":
    main()
