from dataclasses import dataclass

from typing import Any


@dataclass
class MLTrainingResult:

    modelo: Any

    predicciones: Any

    metricas_entrenamiento: dict[str, float]

    estado: str = "completado"


class MLTrainingEngine:

    def __init__(self):

        self.modelo = None

    # =========================================
    # ENTRENAR MODELO
    # =========================================

    def entrenar(

        self,

        tipo_tarea,

        X_train,

        y_train,

        X_test,

        y_test,

        modelo=None

    ):

        try:

            from sklearn.ensemble import (

                RandomForestClassifier,

                RandomForestRegressor

            )

        except ImportError as error:

            raise RuntimeError(

                "Scikit-learn no está instalado."

            ) from error

        # =====================================
        # SELECCIONAR MODELO
        # =====================================

        if modelo is None:

            if tipo_tarea == (

                "clasificacion"

            ):

                modelo = (

                    RandomForestClassifier(

                        n_estimators=100,

                        random_state=42

                    )

                )

            elif tipo_tarea == (

                "regresion"

            ):

                modelo = (

                    RandomForestRegressor(

                        n_estimators=100,

                        random_state=42

                    )

                )

            else:

                raise ValueError(

                    "Tipo de tarea "
                    "no soportado."

                )

        # =====================================
        # ENTRENAR
        # =====================================

        modelo.fit(

            X_train,

            y_train

        )

        self.modelo = modelo

        # =====================================
        # PREDICCIÓN
        # =====================================

        predicciones = modelo.predict(

            X_test

        )

        # =====================================
        # RESULTADO
        # =====================================

        return MLTrainingResult(

            modelo=modelo,

            predicciones=predicciones,

            metricas_entrenamiento={},

            estado="completado"

        )