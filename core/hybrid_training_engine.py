from dataclasses import dataclass

from typing import Any


@dataclass
class HybridTrainingResult:

    mejor_motor: str

    mejor_modelo: Any

    resultado_ml: Any

    resultado_dl: Any

    metricas: dict[str, float]

    estrategia: str

    aprobado: bool 

    tiempo_total: float = 0.0

    observaciones: list[str] | None = None


class HybridTrainingEngine:

   def __init__(

        self,

        ml_engine,

        dl_engine,

        evaluation_engine,

        policy_engine=None,

        model_registry=None,

        checkpoint_manager=None

    ):

        self.ml_engine = ml_engine

        self.dl_engine = dl_engine

        self.evaluation_engine = evaluation_engine

        self.policy_engine = policy_engine

        self.model_registry = model_registry

        self.checkpoint_manager = checkpoint_manager

    # =====================================
    # ENTRENAMIENTO HÍBRIDO
    # =====================================

    def entrenar(

        self,

        parametros_ml,

        parametros_dl

    ):

        resultado_ml = (

            self.pipeline.ejecutar_ml(

                **parametros_ml

            )

        )

        resultado_dl = (

            self.pipeline.ejecutar_dl(

                **parametros_dl

            )

        )

        accuracy_ml = (

            resultado_ml

            ["metricas"]

            .get(

                "accuracy",

                0.0

            )

        )

        accuracy_dl = (

            resultado_dl

            ["metricas"]

            .get(

                "accuracy",

                0.0

            )

        )

        if accuracy_dl >= accuracy_ml:

            mejor_motor = "PyTorch"

            mejor_modelo = (

                resultado_dl

                ["modelo"]

            )

            metricas = (

                resultado_dl

                ["metricas"]

            )

        else:

            mejor_motor = "Scikit-learn"

            mejor_modelo = (

                resultado_ml

                ["modelo"]

            )

            metricas = (

                resultado_ml

                ["metricas"]

            )

        return HybridTrainingResult(

            mejor_motor=mejor_motor,

            mejor_modelo=mejor_modelo,

            resultado_ml=resultado_ml,

            resultado_dl=resultado_dl,

            metricas=metricas

        )
