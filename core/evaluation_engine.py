from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvaluationResult:

    tarea: str

    metricas: dict[str, float] = field(
        default_factory=dict
    )

    matriz_confusion: Any | None = None

    aprobado: bool = False

    recomendaciones: list[str] = field(
        default_factory=list
    )


class EvaluationEngine:

    # ==================================================
    # CLASIFICACIÓN
    # ==================================================

    def evaluar_clasificacion(

        self,

        y_real,

        y_pred,

        objetivo_f1=0.90

    ):

        try:

            from sklearn.metrics import (

                accuracy_score,

                precision_score,

                recall_score,

                f1_score,

                confusion_matrix

            )

        except ImportError as error:

            raise RuntimeError(

                "Scikit-learn no está instalado."

            ) from error

        # ==================================================
        # CALCULAR MÉTRICAS
        # ==================================================

        accuracy = accuracy_score(

            y_real,

            y_pred

        )

        precision = precision_score(

            y_real,

            y_pred,

            average="weighted",

            zero_division=0

        )

        recall = recall_score(

            y_real,

            y_pred,

            average="weighted",

            zero_division=0

        )

        f1 = f1_score(

            y_real,

            y_pred,

            average="weighted",

            zero_division=0

        )

        matriz = confusion_matrix(

            y_real,

            y_pred

        )

        # ==================================================
        # GUARDAR MÉTRICAS
        # ==================================================

        metricas = {

            "accuracy": float(

                accuracy

            ),

            "precision": float(

                precision

            ),

            "recall": float(

                recall

            ),

            "f1": float(

                f1

            )

        }

        recomendaciones = []

        # ==================================================
        # EVALUAR F1
        # ==================================================

        if f1 >= objetivo_f1:

            aprobado = True

            recomendaciones.append(

                "El modelo alcanzó "
                "el objetivo de F1."

            )

        else:

            aprobado = False

            recomendaciones.append(

                "El modelo no alcanzó "
                "el objetivo de F1."

            )

            recomendaciones.append(

                "Se recomienda revisar "
                "los datos, el modelo "
                "o los hiperparámetros."

            )

        # ==================================================
        # ANALIZAR PRECISIÓN Y RECALL
        # ==================================================

        if precision < recall:

            recomendaciones.append(

                "La precisión es inferior "
                "al recall. Puede existir "
                "un problema de falsos positivos."

            )

        elif recall < precision:

            recomendaciones.append(

                "El recall es inferior "
                "a la precisión. Puede existir "
                "un problema de falsos negativos."

            )

        # ==================================================
        # RESULTADO
        # ==================================================

        return EvaluationResult(

            tarea="clasificacion",

            metricas=metricas,

            matriz_confusion=matriz,

            aprobado=aprobado,

            recomendaciones=recomendaciones

        )

    # ==================================================
    # REGRESIÓN
    # ==================================================

    def evaluar_regresion(

        self,

        y_real,

        y_pred,

        objetivo_r2=0.80

    ):

        try:

            from sklearn.metrics import (

                mean_absolute_error,

                mean_squared_error,

                r2_score

            )

        except ImportError as error:

            raise RuntimeError(

                "Scikit-learn no está instalado."

            ) from error

        # ==================================================
        # CALCULAR MÉTRICAS
        # ==================================================

        mae = mean_absolute_error(

            y_real,

            y_pred

        )

        mse = mean_squared_error(

            y_real,

            y_pred

        )

        rmse = mse ** 0.5

        r2 = r2_score(

            y_real,

            y_pred

        )

        # ==================================================
        # GUARDAR MÉTRICAS
        # ==================================================

        metricas = {

            "mae": float(

                mae

            ),

            "mse": float(

                mse

            ),

            "rmse": float(

                rmse

            ),

            "r2": float(

                r2

            )

        }

        recomendaciones = []

        # ==================================================
        # EVALUAR R²
        # ==================================================

        if r2 >= objetivo_r2:

            aprobado = True

            recomendaciones.append(

                "El modelo alcanzó "
                "el objetivo de R²."

            )

        else:

            aprobado = False

            recomendaciones.append(

                "El modelo no alcanzó "
                "el objetivo de R²."

            )

            recomendaciones.append(

                "Se recomienda revisar "
                "las variables, los datos "
                "o el modelo utilizado."

            )

        # ==================================================
        # RESULTADO
        # ==================================================

        return EvaluationResult(

            tarea="regresion",

            metricas=metricas,

            aprobado=aprobado,

            recomendaciones=recomendaciones

        )