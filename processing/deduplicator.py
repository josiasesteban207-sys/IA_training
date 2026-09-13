import hashlib


class Deduplicator:

    def __init__(self):

        self.hashes = set()

    def es_duplicado(
        self,
        texto: str
    ) -> bool:

        hash_texto = hashlib.sha256(
            texto.encode(
                "utf-8"
            )
        ).hexdigest()

        if hash_texto in self.hashes:

            return True

        self.hashes.add(
            hash_texto
        )

        return False

    def filtrar(
        self,
        fragmentos: list[str]
    ) -> list[str]:

        resultados = []

        for fragmento in fragmentos:

            if not self.es_duplicado(
                fragmento
            ):

                resultados.append(
                    fragmento
                )

        return resultados