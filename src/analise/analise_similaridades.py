"""
Análise de Similaridades e Agrupamentos (critério 5).
"""

from collections import defaultdict

from src.carregar_dados import construir_grafo
from src.structures.similaridade_atributos import (
    construir_vetores_todas_musicas,
    construir_matriz_similaridade,
    raiz_quadrada,
)


def calcular_coocorrencia(grafo) -> dict[tuple[int, int], int]:
    usuario_musicas = defaultdict(set)
    for usuario_id, interacoes in grafo._adj.items():
        for musica_id, _tipo, _nota in interacoes:
            usuario_musicas[usuario_id].add(musica_id)

    cooc = defaultdict(int)
    for musicas_do_usuario in usuario_musicas.values():
        musicas = list(musicas_do_usuario)
        for i in range(len(musicas)):
            for j in range(i + 1, len(musicas)):
                par = tuple(sorted((musicas[i], musicas[j])))
                cooc[par] += 1
    return cooc


def correlacao_pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    media_x, media_y = sum(xs) / n, sum(ys) / n
    cov = sum((xs[i] - media_x) * (ys[i] - media_y) for i in range(n))
    desvio_x = raiz_quadrada(sum((x - media_x) ** 2 for x in xs))
    desvio_y = raiz_quadrada(sum((y - media_y) ** 2 for y in ys))
    if desvio_x == 0 or desvio_y == 0:
        return 0.0
    return cov / (desvio_x * desvio_y)


def distribuicao_por_faixa(pesos: list[float]) -> dict[str, int]:
    """Conta quantos pesos caem em cada faixa de 0.0 a 1.0."""
    faixas = {"0.0-0.5": 0, "0.5-0.7": 0, "0.7-0.85": 0, "0.85-0.95": 0, "0.95-1.0": 0}
    for p in pesos:
        if p < 0.5:
            faixas["0.0-0.5"] += 1
        elif p < 0.7:
            faixas["0.5-0.7"] += 1
        elif p < 0.85:
            faixas["0.7-0.85"] += 1
        elif p < 0.95:
            faixas["0.85-0.95"] += 1
        else:
            faixas["0.95-1.0"] += 1
    return faixas


def gerar_analise(
    caminho_usuarios: str = "data/usuarios.csv",
    caminho_musicas: str = "data/musicas.csv",
    caminho_interacoes: str = "data/interacoes.csv",
    limiar_divergencia_cooc: int = 3,
    top_n: int = 5,
) -> None:
    grafo = construir_grafo(
        caminho_usuarios=caminho_usuarios,
        caminho_musicas=caminho_musicas,
        caminho_interacoes=caminho_interacoes,
    )

    musicas = list(grafo._musicas.values())
    nomes = {m.id: m.titulo for m in musicas}
    generos = {m.id: m.genero for m in musicas}

    vetores = construir_vetores_todas_musicas(musicas)
    arestas_atributos = construir_matriz_similaridade(vetores, limiar=0.0)
    sim_por_par = {(a, b): s for a, b, s in arestas_atributos}

    cooc = calcular_coocorrencia(grafo)

    total_pares = len(arestas_atributos)
    pesos_atributos = [s for _, _, s in arestas_atributos]

    print("=" * 60)
    print("ANÁLISE DE SIMILARIDADES E AGRUPAMENTOS")
    print("=" * 60)

    print(f"\nTotal de pares possíveis: {total_pares}")
    print(f"Pares com coocorrência > 0: {len(cooc)} ({100 * len(cooc) / total_pares:.1f}%)")
    print(
        f"Similaridade de atributos — média: {sum(pesos_atributos) / len(pesos_atributos):.4f}, "
        f"min: {min(pesos_atributos):.4f}, max: {max(pesos_atributos):.4f}"
    )

    print("\nDistribuição de pesos (similaridade de atributos):")
    for faixa, qtd in distribuicao_por_faixa(pesos_atributos).items():
        print(f"  {faixa}: {qtd} pares ({100 * qtd / total_pares:.1f}%)")

    # correlação entre as duas medidas (apenas nos pares que coocorrem)
    pares_comuns = list(cooc.keys())
    xs = [cooc[p] for p in pares_comuns]
    ys = [sim_por_par.get(p, 0.0) for p in pares_comuns]
    corr = correlacao_pearson(xs, ys)
    print(f"\nCorrelação de Pearson (coocorrência vs. similaridade de atributos): {corr:.4f}")

    def fmt(par, extra=""):
        a, b = par
        return f"  {extra}{nomes[a]} ({generos[a]}) <-> {nomes[b]} ({generos[b]})"

    print(f"\nTop {top_n} pares de CONCORDÂNCIA (maior coocorrência):")
    top_cooc = sorted(cooc.items(), key=lambda x: -x[1])[:top_n]
    for par, c in top_cooc:
        s = sim_por_par.get(par, 0.0)
        print(fmt(par, f"cooc={c}, sim={s:.3f}  "))

    print(
        f"\nTop {top_n} pares de DIVERGÊNCIA "
        f"(coocorrência >= {limiar_divergencia_cooc}, baixa similaridade):"
    )
    divergentes = [
        (par, cooc[par], sim_por_par.get(par, 0.0))
        for par in pares_comuns
        if cooc[par] >= limiar_divergencia_cooc
    ]
    divergentes.sort(key=lambda d: d[2])
    for par, c, s in divergentes[:top_n]:
        print(fmt(par, f"cooc={c}, sim={s:.3f}  "))

    print(f"\nTop {top_n} pares de COLD-START (sem coocorrência, alta similaridade):")
    sem_cooc = [(par, s) for par, s in sim_por_par.items() if par not in cooc]
    sem_cooc.sort(key=lambda x: -x[1])
    for par, s in sem_cooc[:top_n]:
        print(fmt(par, f"sim={s:.3f}  "))


if __name__ == "__main__":
    gerar_analise()