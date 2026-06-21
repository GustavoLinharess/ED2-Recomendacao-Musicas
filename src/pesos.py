"""
Convenção única de peso das arestas usuário-música.

O peso da aresta não é armazenado no grafo: é derivado de `tipo + nota`,
conforme combinado no schema (ver docs/base-de-dados.md). Centralizar isso
aqui garante que o grafo bipartido, a projeção do Pedro e o motor de
recomendação do João usem exatamente a mesma escala.

Escala: nota 10 = 1,0.
    - avaliacao  -> nota / 10        (0,0 a 1,0)
    - interesse  -> 0,6              (sinal de gosto sem nota)
    - compartilhamento -> 0,8        (sinal mais forte que interesse)
"""

PESO_INTERESSE = 0.6
PESO_COMPARTILHAMENTO = 0.8
NOTA_MAXIMA = 10.0


def peso_interacao(tipo: str, nota: float | None) -> float:
    """Converte (tipo, nota) no peso normalizado da aresta, em [0, 1]."""
    if tipo == "avaliacao":
        if nota is None:
            return 0.0
        return nota / NOTA_MAXIMA
    if tipo == "interesse":
        return PESO_INTERESSE
    if tipo == "compartilhamento":
        return PESO_COMPARTILHAMENTO
    # tipo desconhecido: trata como sinal neutro fraco
    return 0.0
