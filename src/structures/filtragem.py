"""
Filtragem do GrafoProjecao por threshold de peso e seleção top-N.

Objetivo
--------
  1. Podar arestas fracas (threshold), reduzindo ruído nas recomendações.
  2. Selecionar top-N arestas mais pesadas por nó (evita grafo completo denso).
  3. Testar múltiplos valores e registrar efeito em número de arestas e
     métricas de qualidade aparente.

Todas as funções recebem/retornam listas de arestas (u, v, peso) para
manter independência da estrutura GrafoProjecao e facilitar o encadeamento.
"""

from src.structures.grafo_projecao import GrafoProjecao


# ------------------------------------------------------------------ #
#  Filtros primários                                                  #
# ------------------------------------------------------------------ #

def filtrar_por_threshold(
    arestas: list[tuple[int, int, float]],
    threshold: float,
) -> list[tuple[int, int, float]]:
    """
    Remove arestas com peso < threshold

    Retorna lista filtrada, mantendo a ordem original.
    """
    return [(u, v, p) for u, v, p in arestas if p >= threshold]


def top_n_global(
    arestas: list[tuple[int, int, float]],
    n: int,
) -> list[tuple[int, int, float]]:
    """
    Mantém apenas as n arestas de maior peso no grafo inteiro.
    Útil para grafos muito densos.
    """
    return sorted(arestas, key=lambda x: x[2], reverse=True)[:n]


def top_n_por_no(
    arestas: list[tuple[int, int, float]],
    n: int,
) -> list[tuple[int, int, float]]:
    """
    Para cada nó, mantém apenas as n arestas de maior peso.
    Garante que todo nó tenha ao menos conectividade local relevante,
    mesmo que globalmente o grafo seja esparso.

    Retorna lista sem duplicatas (cada aresta aparece uma vez).
    """
    # Monta adjacência temporária
    adj: dict[int, list[tuple[int, float]]] = {}
    for u, v, p in arestas:
        adj.setdefault(u, []).append((v, p))
        adj.setdefault(v, []).append((u, p))

    # Para cada nó, seleciona top-n vizinhos
    arestas_mantidas: set[tuple[int, int]] = set()
    for no, vizs in adj.items():
        vizs_ord = sorted(vizs, key=lambda x: x[1], reverse=True)[:n]
        for viz, _ in vizs_ord:
            par = (min(no, viz), max(no, viz))
            arestas_mantidas.add(par)

    # Reconstrói lista a partir dos pares mantidos
    indice: dict[tuple[int, int], float] = {
        (min(u, v), max(u, v)): p for u, v, p in arestas
    }
    return [(u, v, indice[(u, v)]) for u, v in arestas_mantidas]


# ------------------------------------------------------------------ #
#  Filtragem combinada                                                #
# ------------------------------------------------------------------ #

def filtrar(
    arestas: list[tuple[int, int, float]],
    threshold: float = 0.0,
    top_n_global_val: int | None = None,
    top_n_por_no_val: int | None = None,
) -> list[tuple[int, int, float]]:
    """
    Pipeline de filtragem parametrizável.
    Aplica em ordem: threshold → top_n_por_no → top_n_global.
    Passe None em qualquer parâmetro para pular essa etapa.

    Retorna lista filtrada de (u, v, peso)
    """
    resultado = arestas

    if threshold > 0.0:
        resultado = filtrar_por_threshold(resultado, threshold)

    if top_n_por_no_val is not None:
        resultado = top_n_por_no(resultado, top_n_por_no_val)

    if top_n_global_val is not None:
        resultado = top_n_global(resultado, top_n_global_val)

    return resultado


# ------------------------------------------------------------------ #
#  Análise comparativa de thresholds                                  #
# ------------------------------------------------------------------ #

def analisar_thresholds(
    arestas_originais: list[tuple[int, int, float]],
    thresholds: list[float] | None = None,
) -> list[dict]:
    """
    Testa múltiplos valores de threshold e registra o efeito no grafo.

    Retorna lista de dicts com métricas por threshold – útil para logging ou análise
    """
    if thresholds is None:
        thresholds = [0.0, 0.3, 0.5, 0.6, 0.7, 0.8]

    total_orig = len(arestas_originais)
    pesos_orig = [p for _, _, p in arestas_originais]
    nos_orig = len(
        {n for u, v, _ in arestas_originais for n in (u, v)}
    )

    resultados: list[dict] = []

    print("=" * 72)
    print("ANÁLISE COMPARATIVA DE THRESHOLDS")
    print("=" * 72)
    print(f"  Grafo original: {nos_orig} nós, {total_orig} arestas")
    if pesos_orig:
        print(
            f"  Peso original  : min={min(pesos_orig):.4f}  "
            f"max={max(pesos_orig):.4f}  "
            f"média={sum(pesos_orig)/len(pesos_orig):.4f}"
        )
    print()
    print(
        f"  {'Threshold':>10} {'Arestas':>9} {'% mantidas':>11} "
        f"{'Nós ativos':>11} {'Peso médio':>11} {'Peso mín':>9}"
    )
    print("  " + "-" * 64)

    for t in thresholds:
        filtradas = filtrar_por_threshold(arestas_originais, t)
        n_arestas = len(filtradas)
        pct = 100 * n_arestas / total_orig if total_orig > 0 else 0.0
        pesos = [p for _, _, p in filtradas]
        media = sum(pesos) / len(pesos) if pesos else 0.0
        minimo = min(pesos) if pesos else 0.0
        nos_ativos = len({n for u, v, _ in filtradas for n in (u, v)})

        print(
            f"  {t:>10.2f} {n_arestas:>9d} {pct:>10.1f}% "
            f"{nos_ativos:>11d} {media:>11.4f} {minimo:>9.4f}"
        )

        resultados.append(
            {
                "threshold": t,
                "arestas": n_arestas,
                "pct_mantidas": pct,
                "nos_ativos": nos_ativos,
                "peso_medio": media,
                "peso_minimo": minimo,
            }
        )

    print("=" * 72)
    return resultados


# ------------------------------------------------------------------ #
#  Construção do grafo filtrado                                       #
# ------------------------------------------------------------------ #

def construir_grafo_filtrado(
    arestas: list[tuple[int, int, float]],
    threshold: float = 0.5,
    top_n_por_no_val: int | None = None,
    top_n_global_val: int | None = None,
) -> GrafoProjecao:
    """
    Atalho: filtra as arestas e já constrói o GrafoProjecao resultante.
    """
    arestas_filtradas = filtrar(
        arestas,
        threshold=threshold,
        top_n_por_no_val=top_n_por_no_val,
        top_n_global_val=top_n_global_val,
    )
    return GrafoProjecao.de_lista_arestas(arestas_filtradas)