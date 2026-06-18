import pandas as pd
from src.models.usuario import Usuario
from src.models.musica import Musica
from src.structures.grafo_bipartido import GrafoBipartido


def carregar_usuarios(caminho: str) -> list[Usuario]:
    df = pd.read_csv(caminho)
    usuarios = []
    for _, linha in df.iterrows():
        usuarios.append(Usuario(id=int(linha["id"]), nome=linha["nome"]))
    return usuarios


def carregar_musicas(caminho: str) -> list[Musica]:
    df = pd.read_csv(caminho)
    musicas = []
    for _, linha in df.iterrows():
        musicas.append(Musica(
            id=int(linha["id"]),
            titulo=linha["titulo"],
            artista=linha["artista"],
            genero=linha["genero"],
            descricao=linha["descricao"],
        ))
    return musicas


def construir_grafo(
    caminho_usuarios: str,
    caminho_musicas: str,
    caminho_avaliacoes: str,
) -> GrafoBipartido:
    usuarios = carregar_usuarios(caminho_usuarios)
    musicas  = carregar_musicas(caminho_musicas)
    avaliacoes = pd.read_csv(caminho_avaliacoes)

    grafo = GrafoBipartido()

    for u in usuarios:
        grafo.adicionar_usuario(u)

    for m in musicas:
        grafo.adicionar_musica(m)

    for _, linha in avaliacoes.iterrows():
        grafo.adicionar_avaliacao(
            int(linha["usuario_id"]),
            int(linha["musica_id"]),
            float(linha["nota"]),
        )

    return grafo
