from dataclasses import dataclass


@dataclass
class TrainingDecision:

    tipo_entrenamiento: str

    estrategia: str

    framework: str

    dispositivo: str

    confianza: float

    motivo: str

    recomendaciones: list[str]


class TrainingDecisionEngine:

    def __init__(

        self,

        hardware,

        resources

    ):

        self.hardware = hardware

        self.resources = resources

    # =====================================
    # DECIDIR
    # =====================================

    def decidir(

        self,

        tipo_tarea,

        tamano_dataset,

        precision_objetivo=0.90,

        permitir_hibrido=True

    ):

        recomendaciones = []

        # =================================
        # DATASET PEQUEÑO
        # =================================

        if tamano_dataset < 5000:

            tipo = "ml"

            estrategia = (

                "machine_learning"

            )

            framework = (

                "scikit-learn"

            )

            dispositivo = "cpu"

            confianza = 0.90

            motivo = (

                "El dataset es pequeño. "
                "Machine Learning ofrece "
                "una relación adecuada entre "
                "velocidad y precisión."

            )

            recomendaciones.append(

                "Se recomienda ML para reducir "
                "tiempo de entrenamiento."

            )

        # =================================
        # DATASET GRANDE + GPU
        # =================================

        elif (

            tamano_dataset >= 50000

            and

            self.resources.gpu_disponible

            and

            self.hardware.cuda_disponible

        ):

            tipo = "dl"

            estrategia = (

                "deep_learning"

            )

            framework = "pytorch"

            dispositivo = "cuda"

            confianza = 0.95

            motivo = (

                "El dataset es grande y existe "
                "una GPU compatible con CUDA."

            )

            recomendaciones.append(

                "Se recomienda utilizar GPU "
                "para acelerar DL."

            )

        # =================================
        # HÍBRIDO
        # =================================

        elif (

            permitir_hibrido

            and

            precision_objetivo >= 0.95

            and

            self.resources.gpu_disponible

        ):

            tipo = "hibrido"

            estrategia = (

                "ml_dl_hibrido"

            )

            framework = (

                "scikit-learn+pytorch"

            )

            dispositivo = (

                "cuda"

            )

            confianza = 0.92

            motivo = (

                "El objetivo de precisión es alto "
                "y existe capacidad para combinar "
                "ML y DL."

            )

            recomendaciones.append(

                "Se recomienda comparar ML y DL "
                "para seleccionar el mejor modelo."

            )

        # =================================
        # CPU SIN GPU
        # =================================

        else:

            tipo = "ml"

            estrategia = (

                "machine_learning"

            )

            framework = (

                "scikit-learn"

            )

            dispositivo = "cpu"

            confianza = 0.85

            motivo = (

                "No existe una GPU compatible "
                "disponible. Se prioriza ML "
                "para reducir el costo computacional."

            )

            recomendaciones.append(

                "Se recomienda ML debido a "
                "la ausencia de GPU CUDA."

            )

        # =================================
        # RECURSOS LIMITADOS
        # =================================

        if (

            self.resources.nivel_recursos

            == "critico"

        ):

            recomendaciones.append(

                "Los recursos actuales son "
                "críticos. Se recomienda esperar "
                "antes de iniciar entrenamiento."

            )

        elif (

            self.resources.nivel_recursos

            == "alto"

        ):

            recomendaciones.append(

                "El sistema presenta alta carga. "
                "Se recomienda reducir el consumo "
                "antes de entrenar."

            )

        return TrainingDecision(

            tipo_entrenamiento=tipo,

            estrategia=estrategia,

            framework=framework,

            dispositivo=dispositivo,

            confianza=confianza,

            motivo=motivo,

            recomendaciones=recomendaciones

        )