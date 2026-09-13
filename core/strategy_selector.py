from core.training_mode import (
    TrainingMode,
    TrainingProfile
)


class StrategySelector:

    def seleccionar(
        self,
        modo: TrainingMode,
        tipo_ia: str,
        objetivo: str,
        cantidad_datos: int = 0
    ) -> TrainingProfile:

        if modo == TrainingMode.ML:

            return self._modo_ml()

        if modo == TrainingMode.DL:

            return self._modo_dl()

        if modo == TrainingMode.HYBRID:

            return self._modo_hibrido()

        return self._modo_auto(

            tipo_ia,

            objetivo,

            cantidad_datos

        )

    # --------------------------------
    # MACHINE LEARNING
    # --------------------------------

    def _modo_ml(self):

        return TrainingProfile(

            mode=TrainingMode.ML,

            nombre="Machine Learning",

            frameworks=[
                "Scikit-learn"
            ],

            nivel_recursos="Bajo",

            tiempo_estimado="Rápido",

            gpu_recomendada=False,

            descripcion=(
                "Entrenamiento eficiente para "
                "datos estructurados y problemas "
                "de clasificación o regresión."
            )

        )

    # --------------------------------
    # DEEP LEARNING
    # --------------------------------

    def _modo_dl(self):

        return TrainingProfile(

            mode=TrainingMode.DL,

            nombre="Deep Learning",

            frameworks=[
                "PyTorch"
            ],

            nivel_recursos="Medio / Alto",

            tiempo_estimado="Medio / Largo",

            gpu_recomendada=True,

            descripcion=(
                "Entrenamiento basado en redes "
                "neuronales profundas."
            )

        )

    # --------------------------------
    # HÍBRIDO
    # --------------------------------

    def _modo_hibrido(self):

        return TrainingProfile(

            mode=TrainingMode.HYBRID,

            nombre="Entrenamiento Híbrido",

            frameworks=[
                "Scikit-learn",
                "PyTorch"
            ],

            nivel_recursos="Alto",

            tiempo_estimado="Largo",

            gpu_recomendada=True,

            descripcion=(
                "Combina técnicas de Machine "
                "Learning y Deep Learning."
            )

        )

    # --------------------------------
    # AUTOMÁTICO
    # --------------------------------

    def _modo_auto(

        self,

        tipo_ia,

        objetivo,

        cantidad_datos

    ):

        tipo = tipo_ia.lower()

        objetivo = objetivo.lower()

        # Datos pequeños
        if cantidad_datos < 10000:

            if (
                "imagen" not in tipo
                and "visión" not in tipo
                and "vision" not in tipo
            ):

                return self._modo_ml()

        # Imágenes
        if (
            "imagen" in tipo
            or "visión" in tipo
            or "vision" in tipo
        ):

            return self._modo_dl()

        # Problemas complejos
        if (
            "complejo" in objetivo
            or "avanzado" in objetivo
        ):

            return self._modo_dl()

        return self._modo_ml()