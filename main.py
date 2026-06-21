from src.carregar_dados import construir_grafo
from src.structures.indexador_musicas import IndexadorMusicas
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

    musicas = list(grafo._musicas.values())
    vetores = construir_vetores_todas_musicas(musicas, indexador=indexador)

    for usuario_id, interacoes in grafo._adj.items():
        for musica_id, _tipo, _nota in interacoes:
            indexador.registrar_interacao(usuario_id, musica_id)

    print(f"\nMúsicas do usuário 4 (via HashTable): {indexador.musicas_do_usuario(4)}")
    print(f"Usuários da música 1 (via HashTable): {indexador.usuarios_da_musica(1)}")
    print(f"Vetor de atributos da música 1: {indexador.atributos_da_musica(1)}")

    # ---- similaridade por atributos cat docs/sidebar.md----
    arestas_atributos = construir_matriz_similaridade(vetores, limiar=0.5)
    print(f"\nTotal de arestas por similaridade de atributos (limiar 0.5): {len(arestas_atributos)}")


if __name__ == "__main__":
    main()