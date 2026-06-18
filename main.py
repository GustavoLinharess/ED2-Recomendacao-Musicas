from src.carregar_dados import construir_grafo


def main() -> None:
    grafo = construir_grafo(
        caminho_usuarios="data/usuarios.csv",
        caminho_musicas="data/musicas.csv",
        caminho_avaliacoes="data/avaliacoes.csv",
    )

    # teste rápido: vizinhos do usuário 1
    vizinhos = grafo.obter_vizinhos(1)
    print(f"músicas avaliadas pelo usuário 1: {vizinhos}")


if __name__ == "__main__":
    main()
