from dataclasses import dataclass


@dataclass
class ResearchQuery:

    consulta: str

    objetivo: str

    tipo_datos: str

    prioridad: str


class ResearchEngine:

    def generar_consultas(

        self,

        objetivo,

        tipo_datos,

        dominio=None

    ):

        consultas = []

        # Consulta principal

        consultas.append(

            ResearchQuery(

                consulta=(
                    f"{objetivo} "
                    f"{tipo_datos} "
                    f"machine learning "
                    f"deep learning"
                ),

                objetivo=objetivo,

                tipo_datos=tipo_datos,

                prioridad="alta"

            )

        )

        # Consulta sobre modelos

        consultas.append(

            ResearchQuery(

                consulta=(

                    f"{objetivo} "
                    f"best models "
                    f"benchmark"

                ),

                objetivo=objetivo,

                tipo_datos=tipo_datos,

                prioridad="alta"

            )

        )

        # Consulta científica

        consultas.append(

            ResearchQuery(

                consulta=(

                    f"{objetivo} "
                    f"{tipo_datos} "
                    f"research paper"

                ),

                objetivo=objetivo,

                tipo_datos=tipo_datos,

                prioridad="alta"

            )

        )

        # Consulta específica del dominio

        if dominio:

            consultas.append(

                ResearchQuery(

                    consulta=(

                        f"{objetivo} "
                        f"{dominio} "
                        f"artificial intelligence"

                    ),

                    objetivo=objetivo,

                    tipo_datos=tipo_datos,

                    prioridad="media"

                )

            )

        return consultas