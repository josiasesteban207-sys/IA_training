import re


class TextCleaner:

    def limpiar(self, texto: str) -> str:

        if not texto:
            return ""

        # Eliminar espacios repetidos
        texto = re.sub(
            r"\s+",
            " ",
            texto
        )

        # Eliminar caracteres extraños
        texto = re.sub(
            r"[^\w\s.,;:!?¿¡()\-/%]",
            "",
            texto
        )

        # Eliminar espacios al inicio y final
        texto = texto.strip()

        return texto

    def dividir(
        self,
        texto: str,
        max_caracteres: int = 1000
    ) -> list[str]:

        texto = self.limpiar(texto)

        if not texto:
            return []

        fragmentos = []

        inicio = 0

        while inicio < len(texto):

            final = (
                inicio
                + max_caracteres
            )

            fragmento = texto[
                inicio:final
            ]

            fragmentos.append(
                fragmento.strip()
            )

            inicio = final

        return fragmentos