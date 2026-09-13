from dataclasses import dataclass


@dataclass
class TaskType:

    nombre: str

    descripcion: str

    tipo_evaluacion: str

    framework_recomendado: str


class TaskTypeRouter:

    TAREAS = {

        "clasificacion": TaskType(

            nombre="Clasificación",

            descripcion=(

                "Predice una clase o categoría."

            ),

            tipo_evaluacion="clasificacion",

            framework_recomendado=(

                "Scikit-learn / PyTorch"

            )

        ),

        "regresion": TaskType(

            nombre="Regresión",

            descripcion=(

                "Predice un valor numérico."

            ),

            tipo_evaluacion="regresion",

            framework_recomendado=(

                "Scikit-learn / PyTorch"

            )

        ),

        "deteccion": TaskType(

            nombre="Detección de objetos",

            descripcion=(

                "Detecta objetos dentro "
                "de imágenes o videos."

            ),

            tipo_evaluacion="deteccion",

            framework_recomendado=(

                "PyTorch"

            )

        ),

        "segmentacion": TaskType(

            nombre="Segmentación",

            descripcion=(

                "Clasifica cada píxel "
                "de una imagen."

            ),

            tipo_evaluacion="segmentacion",

            framework_recomendado=(

                "PyTorch"

            )

        ),

        "nlp": TaskType(

            nombre="Procesamiento de lenguaje",

            descripcion=(

                "Procesa y analiza "
                "lenguaje humano."

            ),

            tipo_evaluacion="nlp",

            framework_recomendado=(

                "PyTorch"

            )

        )

    }

    # =========================================
    # OBTENER TIPO DE TAREA
    # =========================================

    def obtener(

        self,

        tipo

    ):

        tipo = tipo.lower().strip()

        tarea = self.TAREAS.get(

            tipo

        )

        if tarea is None:

            raise ValueError(

                f"Tipo de tarea "
                f"no soportado: {tipo}"

            )

        return tarea

    # =========================================
    # LISTAR TAREAS
    # =========================================

    def listar(self):

        return list(

            self.TAREAS.values()

        )

    # =========================================
    # VALIDAR TAREA
    # =========================================

    def validar(

        self,

        tipo

    ):

        return (

            tipo.lower().strip()

            in

            self.TAREAS

        )