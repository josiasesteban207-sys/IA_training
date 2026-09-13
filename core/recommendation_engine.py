from dataclasses import dataclass


@dataclass
class ModelCandidate:

    nombre: str

    framework: str

    tipo: str

    puntuacion: float

    razones: list[str]

    advertencias: list[str]


class RecommendationEngine:

    def recomendar(

        self,

        tipo_datos,

        objetivo,

        tiene_gpu,

        cantidad_datos

    ):

        candidatos = []

        # =====================================
        # VISIÓN ARTIFICIAL
        # =====================================

        if tipo_datos == "image":

            # CNN

            puntuacion_cnn = 0.75

            razones_cnn = [

                "Adecuada para clasificación "
                "de imágenes.",

                "Arquitectura ampliamente utilizada."

            ]

            candidatos.append(

                ModelCandidate(

                    nombre="CNN",

                    framework="PyTorch",

                    tipo="Deep Learning",

                    puntuacion=(
                        puntuacion_cnn
                    ),

                    razones=razones_cnn,

                    advertencias=[]

                )

            )

            # YOLO

            if objetivo == "detection":

                puntuacion_yolo = 0.90

                razones_yolo = [

                    "Diseñado para detección "
                    "de objetos.",

                    "Adecuado para inferencia "
                    "en tiempo cercano al real."

                ]

                candidatos.append(

                    ModelCandidate(

                        nombre="YOLO",

                        framework="PyTorch",

                        tipo="Deep Learning",

                        puntuacion=(
                            puntuacion_yolo
                        ),

                        razones=razones_yolo,

                        advertencias=[]

                    )

                )

            # Vision Transformer

            if cantidad_datos >= 100000:

                puntuacion_vit = 0.85

                razones_vit = [

                    "Puede aprovechar datasets "
                    "grandes.",

                    "Arquitectura basada "
                    "en Transformers."

                ]

                candidatos.append(

                    ModelCandidate(

                        nombre=(
                            "Vision Transformer"
                        ),

                        framework="PyTorch",

                        tipo="Deep Learning",

                        puntuacion=(
                            puntuacion_vit
                        ),

                        razones=razones_vit,

                        advertencias=[]

                    )

                )

        # =====================================
        # DATOS TABULARES
        # =====================================

        elif tipo_datos == "tabular":

            candidatos.append(

                ModelCandidate(

                    nombre="Random Forest",

                    framework=(
                        "Scikit-learn"
                    ),

                    tipo="Machine Learning",

                    puntuacion=0.85,

                    razones=[

                        "Buen punto de partida "
                        "para datos tabulares.",

                        "Entrenamiento relativamente "
                        "sencillo."

                    ],

                    advertencias=[]

                )

            )

            candidatos.append(

                ModelCandidate(

                    nombre="Gradient Boosting",

                    framework=(
                        "Scikit-learn"
                    ),

                    tipo="Machine Learning",

                    puntuacion=0.85,

                    razones=[

                        "Adecuado para problemas "
                        "de clasificación y regresión."

                    ],

                    advertencias=[]

                )

            )

        # =====================================
        # SIN CANDIDATOS
        # =====================================

        if not candidatos:

            return {

                "estado": "sin_recomendacion",

                "candidatos": []

            }

        # =====================================
        # ORDENAR
        # =====================================

        candidatos.sort(

            key=lambda x: x.puntuacion,

            reverse=True

        )

        mejor = candidatos[0]

        return {

            "estado": "ok",

            "recomendado": mejor,

            "alternativas": candidatos[1:]

        }