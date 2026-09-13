from dataclasses import dataclass
from urllib.parse import quote
from urllib.request import Request, urlopen
from html.parser import HTMLParser


@dataclass
class SearchResult:
    titulo: str
    url: str
    descripcion: str = ""


class SimpleHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):

        if tag != "a":
            return

        for atributo, valor in attrs:

            if atributo == "href" and valor:
                self.links.append(valor)


class WebSearcher:

    def buscar(self, consulta: str) -> list[SearchResult]:

        print(f"\n🔎 Buscando información sobre: {consulta}")

        url = (
            "https://www.google.com/search?q="
            + quote(consulta)
        )

        request = Request(
            url,
            headers={
                "User-Agent": "AI-TRAINER/0.1"
            }
        )

        try:

            with urlopen(request, timeout=10) as response:

                html = response.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            parser = SimpleHTMLParser()
            parser.feed(html)

            resultados = []

            for link in parser.links:

                if link.startswith("http"):

                    resultados.append(
                        SearchResult(
                            titulo="Resultado encontrado",
                            url=link
                        )
                    )

            return resultados[:10]

        except Exception as error:

            print(
                f"⚠️ Error durante la búsqueda: {error}"
            )

            return []