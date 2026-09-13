from dataclasses import dataclass

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


@dataclass
class EvaluationResult:

    accuracy: float

    precision: float

    recall: float

    f1: float

    aprobado: bool

    motivo: str


class ModelEvaluator:

    def __init__(
        self,
        umbral=0.80
    ):

        self.umbral = umbral

    def evaluar(
        self,
        y_real,
        y_pred
    ):

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

        aprobado = (
            f1 >= self.umbral
        )

        if aprobado:

            motivo = (
                "El modelo supera "
                "el umbral establecido."
            )

        else:

            motivo = (
                "El modelo no alcanza "
                "el rendimiento mínimo."
            )

        return EvaluationResult(

            accuracy=accuracy,

            precision=precision,

            recall=recall,

            f1=f1,

            aprobado=aprobado,

            motivo=motivo

        )

    def mostrar(
        self,
        resultado
    ):

        print(
            "\n" + "=" * 50
        )

        print(
            "🧪 EVALUACIÓN DEL MODELO"
        )

        print(
            "=" * 50
        )

        print(
            f"Accuracy: "
            f"{resultado.accuracy * 100:.2f}%"
        )

        print(
            f"Precision: "
            f"{resultado.precision * 100:.2f}%"
        )

        print(
            f"Recall: "
            f"{resultado.recall * 100:.2f}%"
        )

        print(
            f"F1 Score: "
            f"{resultado.f1 * 100:.2f}%"
        )

        print(
            "\nResultado:"
        )

        if resultado.aprobado:

            print(
                "🟢 MODELO APROBADO"
            )

        else:

            print(
                "🔴 MODELO RECHAZADO"
            )

        print(
            f"\n📝 {resultado.motivo}"
        )