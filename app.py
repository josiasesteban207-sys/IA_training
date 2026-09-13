from research.researcher import AIResearcher


def main():

    print("=" * 50)
    print("          AI TRAINER v0.1")
    print("=" * 50)

    tema = input(
        "\n¿Sobre qué tema quieres investigar?: "
    )

    investigador = AIResearcher()

    resultados = investigador.investigar(
        tema
    )

    print("\nRESULTADOS:")

    for numero, resultado in enumerate(
        resultados,
        start=1
    ):

        print(
            f"{numero}. "
            f"{resultado.url}"
        )


if __name__ == "__main__":
    main()