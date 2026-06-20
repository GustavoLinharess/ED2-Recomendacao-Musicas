import pandas as pd
from src.models.usuario import Usuario
from src.models.musica import Musica
from src.structures.grafo_bipartido import GrafoBipartido


def carregar_usuarios(caminho: str) -> list[Usuario]:
    df = pd.read_csv(caminho)
    usuarios = []
    for _, linha in df.iterrows():
        preferidos = str(linha["generos_preferidos"]).split("|")
        usuarios.append(Usuario(
            id=int(linha["id"]),
            nome=linha["nome"],
            generos_preferidos=preferidos,
        ))
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
            ano=int(linha["ano"]),
            energia=float(linha["energia"]),
            dancabilidade=float(linha["dancabilidade"]),
            valencia=float(linha["valencia"]),
            tempo_bpm=int(linha["tempo_bpm"]),
        ))
    return musicas


def construir_grafo(
    caminho_usuarios: str,
    caminho_musicas: str,
    caminho_interacoes: str,
) -> GrafoBipartido:
    usuarios = carregar_usuarios(caminho_usuarios)
    musicas = carregar_musicas(caminho_musicas)
    interacoes = pd.read_csv(caminho_interacoes)

    grafo = GrafoBipartido()

    for u in usuarios:
        grafo.adicionar_usuario(u)

    for m in musicas:
        grafo.adicionar_musica(m)

    for _, linha in interacoes.iterrows():
        # nota fica vazia quando o tipo não é avaliacao
        nota = float(linha["nota"]) if pd.notna(linha["nota"]) else None
        grafo.adicionar_interacao(
            int(linha["usuario_id"]),
            int(linha["musica_id"]),
            linha["tipo"],
            nota,
        )

    return grafo
