from core.training_mode import (
    TrainingMode
)

from core.trainers.ml_trainer import (
    MLTrainer
)

from core.trainers.dl_trainer import (
    DLTrainer
)

from core.trainers.hybrid_trainer import (
    HybridTrainer
)
class TrainerEngine:

    def entrenar(

        self,

        modo: TrainingMode,

        X,

        y

    ):

        print(
            "\n🚀 AI TRAINER ENGINE"
        )

        print(
            f"Modo seleccionado:"
            f" {modo.value}"
        )

        # -------------------------
        # MACHINE LEARNING
        # -------------------------

        if modo == TrainingMode.ML:

            trainer = MLTrainer()

            return trainer.entrenar(

                X,

                y,

                "models/modelo_ml.pkl"

            )

        # -------------------------
        # DEEP LEARNING
        # -------------------------

        if modo == TrainingMode.DL:

            trainer = DLTrainer()

            return trainer.entrenar(

                X,

                y,

                "models/modelo_dl.pth"

            )

        # -------------------------
        # HÍBRIDO
        # -------------------------

        if modo == TrainingMode.HYBRID:

            trainer = HybridTrainer()
        
        return trainer.entrenar(

            X,

            y,

            "models/modelo_hybrid_dl.pth",
            "models/modelo_hybrid_ml.pkl"
        )  