from research.web_search import WebSearcher


class AIResearcher:

    def __init__(self):

        self.searcher = WebSearcher()

    def investigar(self, tema: str):

        print("\n" + "=" * 50)
        print("AI TRAINER — INVESTIGACIÓN")
        print("=" * 50)

        consultas = [

            f"{tema} información oficial",

            f"{tema} universidad",

            f"{tema} investigación científica",

            f"{tema} organismo oficial"

        ]

        resultados_totales = []

        for consulta in consultas:

            resultados = self.searcher.buscar(
                consulta
            )

            resultados_totales.extend(
                resultados
            )

        print(
            f"\n📚 Resultados encontrados: "
            f"{len(resultados_totales)}"
        )

        return resultados_totales