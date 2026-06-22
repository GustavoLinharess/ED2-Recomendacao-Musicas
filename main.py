from src.carregar_dados import construir_grafo
from src.structures.indexador_musicas import IndexadorMusicas
from src.structures.projecao_musicas import ProjecaoMusicas
from src.structures.similaridade_atributos import (
    construir_vetores_todas_musicas,
    construir_matriz_similaridade,
)

from src.structures.grafo_projecao import GrafoProjecao
from src.structures.bfs_dfs import recomendar_para_usuario, extrair_sementes
from src.structures.agrupamento import componentes_conexas, kruskal_mst, relatorio_clusters
from src.structures.filtragem import analisar_thresholds, construir_grafo_filtrado


THRESHOLD = 0.5
USUARIO_DEMO = 4

def main() -> None:
    grafo = construir_grafo(
        caminho_usuarios="data/usuarios.csv",
        caminho_musicas="data/musicas.csv",
        caminho_interacoes="data/interacoes.csv",
    )

    # teste rápido: interações do usuário 4
    vizinhos = grafo.obter_vizinhos(4)
    print(f"interações do usuário 4: {vizinhos}")

    # ---- índices em HashTable própria  ----
    indexador = IndexadorMusicas()

    musicas = grafo.musicas()
    vetores = construir_vetores_todas_musicas(musicas, indexador=indexador)

    for usuario_id, interacoes in grafo.adjacencia_usuarios():
        for musica_id, _tipo, _nota in interacoes:
            indexador.registrar_interacao(usuario_id, musica_id)

    print(f"\nMúsicas do usuário 4 (via HashTable): {indexador.musicas_do_usuario(4)}")
    print(f"Usuários da música 1 (via HashTable): {indexador.usuarios_da_musica(1)}")
    print(f"Vetor de atributos da música 1: {indexador.atributos_da_musica(1)}")

    # ---- similaridade por atributos ----
    arestas_atributos = construir_matriz_similaridade(vetores, limiar=0.5)
    print(f"\nTotal de arestas por similaridade de atributos (limiar 0.5): {len(arestas_atributos)}")

    # ---- Card 1 (Pedro): recuperar os dois lados do grafo bipartido ----
    print("\n=== Grafo bipartido (Card 1) ===")
    print(f"Músicas do usuário 4: {grafo.musicas_do_usuario(4)}")
    print(f"Usuários da música 1: {grafo.usuarios_da_musica(1)}")

    # ---- Card 2 (Pedro): projeção música-música por coocorrência ----
    print("\n=== Projeção música-música (Card 2) ===")
    projecao = ProjecaoMusicas.de_grafo(grafo, min_usuarios_comuns=2)
    print(projecao)

    musica_alvo = 31
    titulo_alvo = grafo.musica(musica_alvo).titulo
    vizinhas = sorted(projecao.vizinhos(musica_alvo), key=lambda par: par[1], reverse=True)
    print(f"Vizinhas mais próximas de '{titulo_alvo}' (id={musica_alvo}, cosseno de coocorrência):")
    for musica_id, peso in vizinhas[:5]:
        titulo = grafo.musica(musica_id).titulo
        print(f"  {titulo} (id={musica_id}): peso={peso:.3f}")

  # ---- (Card 3 Esdras): filtragem e grafo de projeção ----
    print("\n=== Filtragem da projeção (Card 3) ===")
    grafo_bruto = GrafoProjecao.de_projecao(projecao)
    arestas_brutas = grafo_bruto.arestas()
    analisar_thresholds(arestas_brutas, thresholds=[0.0, 0.3, 0.5, 0.6, 0.7, 0.8])
    grafo_filtrado = construir_grafo_filtrado(arestas_brutas, threshold=THRESHOLD)
    print(f"Bruto: {grafo_bruto}")
    print(f"Filtrado (threshold={THRESHOLD}): {grafo_filtrado}")
 
    # ---- Card 4 (Esdras): BFS / DFS ----
    print(f"\n=== BFS / DFS — recomendações para usuário {USUARIO_DEMO} (Card 4) ===")
    nomes = {m.id: m.titulo for m in grafo.musicas()}
    interacoes_demo = grafo.obter_vizinhos(USUARIO_DEMO)
    sementes = extrair_sementes(interacoes_demo, top_k=5, nota_minima=3.0)
    musicas_ouvidas = {mid for mid, _, _ in interacoes_demo}
 
    if not sementes:
        print("  Usuário sem avaliações suficientes para semente.")
    else:
        for metodo in ("bfs", "dfs"):
            print(f"\n  [{metodo.upper()}]")
            recomendacoes = recomendar_para_usuario(
                grafo_filtrado,
                sementes=sementes,
                musicas_ja_ouvidas=musicas_ouvidas,
                profundidade=2,
                top_n=10,
                metodo=metodo,
            )
            for rank, (mid, score) in enumerate(recomendacoes, 1):
                print(f"    {rank:2d}. {nomes.get(mid, mid):<35} score={score:.4f}")
 
    # ---- (Card 4 Esdras): agrupamento ---- 

    print("\n=== Agrupamento (Card 4) ===")
    clusters = componentes_conexas(grafo_filtrado)
    relatorio_clusters(clusters, nomes=nomes, top_n_exibir=5)
 
    mst = kruskal_mst(grafo_filtrado)
    print(f"\nMST (Kruskal): {len(mst)} arestas | peso total={sum(p for _,_,p in mst):.4f}")
    for u, v, p in sorted(mst, key=lambda x: x[2], reverse=True)[:5]:
        print(f"  {nomes.get(u, u):<30} ↔ {nomes.get(v, v):<30} ({p:.4f})")



if __name__ == "__main__":
    main()