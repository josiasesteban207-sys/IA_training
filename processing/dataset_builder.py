import json

from pathlib import Path

from processing.cleaner import (
    TextCleaner
)

from processing.deduplicator import (
    Deduplicator
)


class DatasetBuilder:

    def __init__(self):

        self.cleaner = TextCleaner()

        self.deduplicator = (
            Deduplicator()
        )

    def procesar(
        self,
        textos: list[str],
        tema: str
    ):

        fragmentos_totales = []

        for texto in textos:

            fragmentos = (
                self.cleaner.dividir(
                    texto
                )
            )

            fragmentos_totales.extend(
                fragmentos
            )

        # Eliminar duplicados

        fragmentos_unicos = (
            self.deduplicator.filtrar(
                fragmentos_totales
            )
        )

        dataset = []

        for fragmento in fragmentos_unicos:

            dataset.append({

                "tema": tema,

                "texto": fragmento

            })

        return dataset

    def guardar(
        self,
        dataset: list[dict],
        archivo: str
    ):

        Path(
            archivo
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            archivo,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(

                dataset,

                file,

                ensure_ascii=False,

                indent=4

            )

        print(
            f"\n💾 Dataset guardado en:"
            f" {archivo}"
        )