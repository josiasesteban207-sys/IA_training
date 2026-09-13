from dataclasses import dataclass
from typing import Any


@dataclass
class TrainingRequest:

    modo: str

    parametros: dict[str, Any]


class TrainingOrchestrator:

    def __init__(

        self,

        pipeline

    ):

        self.pipeline = pipeline

    # =====================================
    # ENTRENAMIENTO GENERAL
    # =====================================

    def entrenar(

        self,

        request: TrainingRequest

    ):

        modo = (

            request.modo

            .lower()

        )

        if modo == "ml":

            return (

                self.pipeline.ejecutar_ml(

                    **request.parametros

                )

            )

        elif modo == "dl":

            return (

                self.pipeline.ejecutar_dl(

                    **request.parametros

                )

            )

        elif modo == "hybrid":

            return (

                self.pipeline.ejecutar_hibrido(

                    **request.parametros

                )

            )

        raise ValueError(

            f"Modo '{modo}' no soportado."

        )

    # =====================================
    # MODOS DISPONIBLES
    # =====================================

    def modos_disponibles(

        self

    ):

        return [

            "ml",

            "dl",

            "hybrid"

        ]