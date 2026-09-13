from dataclasses import dataclass
from enum import Enum


class DataType(Enum):

    TABULAR = "tabular"

    TEXT = "text"

    IMAGE = "image"

    AUDIO = "audio"

    VIDEO = "video"

    UNKNOWN = "unknown"


class RecommendedMode(Enum):

    ML = "ml"

    DL = "dl"

    HYBRID = "hybrid"


@dataclass
class ProjectConfig:

    objetivo: str

    tipo_datos: DataType

    cantidad_datos: int

    tiene_gpu: bool

    memoria_ram_gb: int

    tiempo_disponible_horas: float

    modo_preferido: str | None = None


@dataclass
class ProjectRecommendation:

    modo_recomendado: RecommendedMode

    confianza: float

    razones: list[str]

    advertencias: list[str]


class ProjectAnalyzer:

    def analizar(

        self,

        config: ProjectConfig

    ):

        razones = []

        advertencias = []

        # =================================
        # IMÁGENES
        # =================================

        if (

            config.tipo_datos
            == DataType.IMAGE

        ):

            if config.tiene_gpu:

                modo = (
                    RecommendedMode.DL
                )

                razones.append(

                    "Las imágenes suelen "
                    "beneficiarse de modelos "
                    "de Deep Learning."

                )

                razones.append(

                    "La GPU permite acelerar "
                    "el entrenamiento."

                )

                confianza = 0.90

            else:

                modo = (
                    RecommendedMode.DL
                )

                razones.append(

                    "Deep Learning sigue siendo "
                    "una opción adecuada para "
                    "visión artificial."

                )

                advertencias.append(

                    "Sin GPU, el entrenamiento "
                    "puede ser considerablemente "
                    "más lento."

                )

                confianza = 0.75

        # =================================
        # DATOS TABULARES
        # =================================

        elif (

            config.tipo_datos
            == DataType.TABULAR

        ):

            if (

                config.cantidad_datos
                < 10000

            ):

                modo = (
                    RecommendedMode.ML
                )

                razones.append(

                    "Para datasets tabulares "
                    "pequeños o medianos, "
                    "Machine Learning clásico "
                    "puede ser eficiente."

                )

                confianza = 0.85

            else:

                modo = (
                    RecommendedMode.ML
                )

                razones.append(

                    "Los modelos clásicos "
                    "siguen siendo una opción "
                    "competitiva para datos "
                    "tabulares."

                )

                confianza = 0.75

        # =================================
        # TEXTO
        # =================================

        elif (

            config.tipo_datos
            == DataType.TEXT

        ):

            modo = (
                RecommendedMode.DL
            )

            razones.append(

                "Los problemas modernos "
                "de procesamiento de lenguaje "
                "suelen utilizar Deep Learning."

            )

            advertencias.append(

                "El modelo concreto depende "
                "del idioma, volumen y objetivo."

            )

            confianza = 0.80

        # =================================
        # AUDIO / VIDEO
        # =================================

        elif (

            config.tipo_datos
            in [

                DataType.AUDIO,

                DataType.VIDEO

            ]

        ):

            modo = (
                RecommendedMode.DL
            )

            razones.append(

                "Audio y video suelen "
                "requerir modelos capaces "
                "de procesar datos complejos."

            )

            confianza = 0.80

        # =================================
        # DESCONOCIDO
        # =================================

        else:

            modo = (
                RecommendedMode.ML
            )

            razones.append(

                "No se pudo identificar "
                "el tipo de datos."

            )

            advertencias.append(

                "La recomendación es "
                "provisional."

            )

            confianza = 0.30

        # =================================
        # VALIDAR MODO MANUAL
        # =================================

        if config.modo_preferido:

            if (

                config.modo_preferido
                != modo.value

            ):

                advertencias.append(

                    "El modo seleccionado "
                    "manualmente no coincide "
                    "con la recomendación."

                )

        return ProjectRecommendation(

            modo_recomendado=modo,

            confianza=confianza,

            razones=razones,

            advertencias=advertencias

        )