from dataclasses import dataclass
from enum import Enum


class TrainingMode(Enum):

    ML = "ml"

    DL = "dl"

    HYBRID = "hybrid"


@dataclass
class TrainingModeInfo:

    modo: TrainingMode

    nombre: str

    descripcion: str


class TrainingModeSelector:

    def __init__(self):

        self._modos = {

            "ml": TrainingModeInfo(

                modo=TrainingMode.ML,

                nombre="Machine Learning",

                descripcion="Entrenamiento con Scikit-learn"

            ),

            "dl": TrainingModeInfo(

                modo=TrainingMode.DL,

                nombre="Deep Learning",

                descripcion="Entrenamiento con PyTorch"

            ),

            "hybrid": TrainingModeInfo(

                modo=TrainingMode.HYBRID,

                nombre="Entrenamiento híbrido",

                descripcion="Combina ML y DL"

            )

        }

    def obtener(

        self,

        modo: str

    ) -> TrainingModeInfo:

        try:

            return self._modos[

                modo.lower()

            ]

        except KeyError as error:

            raise ValueError(

                f"Modo '{modo}' no soportado."

            ) from error

    def listar(self):

        return list(

            self._modos.values()

        )