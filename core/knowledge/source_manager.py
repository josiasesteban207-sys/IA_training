from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class Source:

    url: str

    titulo: str

    tipo: str

    autoridad: float

    confiabilidad: float

    fecha_agregada: str = field(

        default_factory=lambda:
        datetime.now().isoformat()

    )


class SourceManager:

    def __init__(self):

        self.sources = []

    def agregar(

        self,

        url,

        titulo,

        tipo,

        autoridad,

        confiabilidad

    ):

        fuente = Source(

            url=url,

            titulo=titulo,

            tipo=tipo,

            autoridad=autoridad,

            confiabilidad=confiabilidad

        )

        self.sources.append(

            fuente

        )

        print(

            "\nFuente agregada:"

        )

        print(

            fuente.titulo

        )

    def listar(self):

        print(

            "\n📚 FUENTES REGISTRADAS"

        )

        print(

            "=" * 50

        )

        for fuente in self.sources:

            print(

                f"\n📌 {fuente.titulo}"

            )

            print(

                f"🌐 {fuente.url}"

            )

            print(

                f"📂 Tipo: {fuente.tipo}"

            )

            print(

                f"🎯 Autoridad: "
                f"{fuente.autoridad}"

            )

            print(

                f"🛡️ Confiabilidad: "
                f"{fuente.confiabilidad}"

            )

    def obtener_fuentes_validas(

        self,

        minimo=0.70

    ):

        return [

            fuente

            for fuente in self.sources

            if (

                fuente.confiabilidad
                >= minimo

            )

        ]