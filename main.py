from src.carregar_dados import construir_grafo
from src.structures.indexador_musicas import IndexadorMusicas
from src.structures.projecao_musicas import ProjecaoMusicas
from src.structures.similaridade_atributos import (
    construir_vetores_todas_musicas,
    construir_matriz_similaridade,
)


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


if __name__ == "__main__":
    main()