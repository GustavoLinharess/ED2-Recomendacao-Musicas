from src.carregar_dados import construir_grafo


def main() -> None:
    grafo = construir_grafo(
        caminho_usuarios="data/usuarios.csv",
        caminho_musicas="data/musicas.csv",
        caminho_interacoes="data/interacoes.csv",
    )

    # teste rápido: interações do usuário 4
    vizinhos = grafo.obter_vizinhos(4)
    print(f"interações do usuário 4: {vizinhos}")


if __name__ == "__main__":
    main()
