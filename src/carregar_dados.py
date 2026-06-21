"""
Leitura dos CSVs e construção do grafo bipartido.

Sem bibliotecas externas (pandas etc.): o CSV é lido e parseado "na mão",
conforme a exigência do trabalho de implementar tudo do zero. Os dados não
têm vírgulas dentro dos campos (a lista de gêneros usa `|`), então um split
simples por vírgula é suficiente e seguro para esta base.
"""

from src.models.usuario import Usuario
from src.models.musica import Musica
from src.structures.grafo_bipartido import GrafoBipartido


def _ler_csv(caminho: str) -> list[dict[str, str]]:
    """Lê um CSV simples e devolve uma lista de dicionários {coluna: valor}."""
    with open(caminho, encoding="utf-8-sig") as arquivo:
        linhas = arquivo.read().splitlines()

    if not linhas:
        return []

    cabecalho = linhas[0].split(",")
    registros: list[dict[str, str]] = []
    for linha in linhas[1:]:
        if not linha.strip():
            continue
        valores = linha.split(",")
        # completa colunas faltantes (ex.: nota vazia no fim da linha)
        while len(valores) < len(cabecalho):
            valores.append("")
        registros.append(dict(zip(cabecalho, valores)))
    return registros


def carregar_usuarios(caminho: str) -> list[Usuario]:
    usuarios = []
    for linha in _ler_csv(caminho):
        preferidos = linha["generos_preferidos"].split("|")
        usuarios.append(Usuario(
            id=int(linha["id"]),
            nome=linha["nome"],
            generos_preferidos=preferidos,
        ))
    return usuarios


def carregar_musicas(caminho: str) -> list[Musica]:
    musicas = []
    for linha in _ler_csv(caminho):
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
    caminho_usuarios: str = "data/usuarios.csv",
    caminho_musicas: str = "data/musicas.csv",
    caminho_interacoes: str = "data/interacoes.csv",
) -> GrafoBipartido:
    usuarios = carregar_usuarios(caminho_usuarios)
    musicas = carregar_musicas(caminho_musicas)

    grafo = GrafoBipartido()

    for u in usuarios:
        grafo.adicionar_usuario(u)

    for m in musicas:
        grafo.adicionar_musica(m)

    for linha in _ler_csv(caminho_interacoes):
        nota_bruta = linha.get("nota", "").strip()
        # nota fica vazia quando o tipo não é avaliacao
        nota = float(nota_bruta) if nota_bruta else None
        grafo.adicionar_interacao(
            int(linha["usuario_id"]),
            int(linha["musica_id"]),
            linha["tipo"],
            nota,
        )

    return grafo
