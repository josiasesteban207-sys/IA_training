from processing.dataset_builder import (
    DatasetBuilder
)


def main():

    textos = [

        """
        La inteligencia artificial
        es una tecnología que permite
        desarrollar sistemas capaces
        de realizar tareas que normalmente
        requieren inteligencia humana.
        """,

        """
        La inteligencia artificial
        puede utilizarse en educación,
        medicina, agricultura y tecnología.
        """,

        """
        La inteligencia artificial
        es una tecnología que permite
        desarrollar sistemas capaces
        de realizar tareas que normalmente
        requieren inteligencia humana.
        """

    ]

    builder = DatasetBuilder()

    dataset = builder.procesar(

        textos=textos,

        tema="inteligencia artificial"

    )

    print(
        "\n===== DATASET ====="
    )

    for numero, dato in enumerate(
        dataset,
        start=1
    ):

        print(
            f"\n{numero}."
        )

        print(
            dato["texto"]
        )

    builder.guardar(

        dataset,

        "data/processed/"
        "dataset.json"

    )


if __name__ == "__main__":

    main()