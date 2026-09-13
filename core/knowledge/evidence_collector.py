from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Evidence:

    titulo: str

    url: str

    tipo: str

    resumen: str

    relevancia: float

    fuente_validada: bool

    fecha: str = field(

        default_factory=lambda:
        datetime.now().isoformat()

    )


class EvidenceCollector:

    def __init__(self):

        self.evidencias = []

    def agregar(

        self,

        titulo,

        url,

        tipo,

        resumen,

        relevancia,

        fuente_validada

    ):

        evidencia = Evidence(

            titulo=titulo,

            url=url,

            tipo=tipo,

            resumen=resumen,

            relevancia=relevancia,

            fuente_validada=(
                fuente_validada
            )

        )

        self.evidencias.append(

            evidencia

        )

    def obtener_validas(self):

        return [

            evidencia

            for evidencia
            in self.evidencias

            if evidencia.fuente_validada

        ]

    def ordenar_por_relevancia(self):

        return sorted(

            self.evidencias,

            key=lambda evidencia:
                evidencia.relevancia,

            reverse=True

        )

    def mostrar(self):

        print(

            "\n📚 EVIDENCIAS RECOPILADAS"

        )

        print(

            "=" * 60

        )

        for evidencia in (

            self.ordenar_por_relevancia()

        ):

            print(

                f"\n📌 {evidencia.titulo}"

            )

            print(

                f"🌐 {evidencia.url}"

            )

            print(

                f"📂 Tipo: {evidencia.tipo}"

            )

            print(

                f"📊 Relevancia: "
                f"{evidencia.relevancia}"

            )

            print(

                f"🛡️ Validada: "
                f"{evidencia.fuente_validada}"

            )

            print(

                f"📝 {evidencia.resumen}"

            )