"""
Similaridade por atributos (segunda medida) — critério de similaridade
baseado em conteúdo das músicas (gênero + energia/dancabilidade/valencia/bpm),
calculada via cosseno entre vetores.

"""

from src.models.musica import Musica


def raiz_quadrada(x: float, precisao: float = 1e-10) -> float:
    if x < 0:
        raise ValueError("Não existe raiz quadrada real de número negativo")
    if x == 0:
        return 0.0

    palpite = x / 2.0
    while True:
        novo_palpite = (palpite + x / palpite) / 2.0
        if abs(novo_palpite - palpite) < precisao:
            return novo_palpite
        palpite = novo_palpite


def normalizar_min_max(valores: dict[int, float]) -> dict[int, float]:
   
    vmin = min(valores.values())
    vmax = max(valores.values())
    if vmax == vmin:
        return {k: 0.0 for k in valores}
    return {k: (v - vmin) / (vmax - vmin) for k, v in valores.items()}


def construir_vetor_musica(
    musica: Musica,
    generos_possiveis: list[str],
    tempo_bpm_normalizado: dict[int, float],
) -> list[float]:
    """
    Vetor = one-hot(genero) + [energia, dancabilidade, valencia, tempo_bpm_norm]
    """
    one_hot = [1.0 if g == musica.genero else 0.0 for g in generos_possiveis]

    numericos = [
        musica.energia,
        musica.dancabilidade,
        musica.valencia,
        tempo_bpm_normalizado[musica.id],
    ]

    return one_hot + numericos


def construir_vetores_todas_musicas(
    musicas: list[Musica],
    indexador=None,
) -> dict[int, list[float]]:
    """
    musicas: lista de objetos Musica
    indexador: IndexadorMusicas opcional para popular musica_para_atributos

    Retorna {musica_id: vetor_atributos}
    """
    generos_possiveis = sorted({m.genero for m in musicas})

    bpm_bruto = {m.id: m.tempo_bpm for m in musicas}
    bpm_normalizado = normalizar_min_max(bpm_bruto)

    vetores: dict[int, list[float]] = {}
    for musica in musicas:
        vetor = construir_vetor_musica(musica, generos_possiveis, bpm_normalizado)
        vetores[musica.id] = vetor
        if indexador is not None:
            indexador.registrar_atributos(musica.id, vetor)

    return vetores


def similaridade_atributos(v1: list[float], v2: list[float]) -> float:
    """Similaridade do cosseno: cos(theta) = (v1.v2) / (||v1|| * ||v2||)"""
    if len(v1) != len(v2):
        raise ValueError("Vetores de tamanhos diferentes")

    produto_escalar = sum(a * b for a, b in zip(v1, v2))
    norma1 = raiz_quadrada(sum(a * a for a in v1))
    norma2 = raiz_quadrada(sum(b * b for b in v2))

    if norma1 == 0 or norma2 == 0:
        return 0.0

    return produto_escalar / (norma1 * norma2)


def construir_matriz_similaridade(
    vetores_por_musica: dict[int, list[float]],
    limiar: float = 0.0,
) -> list[tuple[int, int, float]]:
    """
    Retorna lista de arestas (m1_id, m2_id, peso=similaridade_atributos).
    'limiar' evita grafo completo denso demais.
    """
    ids = list(vetores_por_musica.keys())
    arestas = []
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            m1, m2 = ids[i], ids[j]
            sim = similaridade_atributos(vetores_por_musica[m1], vetores_por_musica[m2])
            if sim >= limiar:
                arestas.append((m1, m2, sim))
    return arestas