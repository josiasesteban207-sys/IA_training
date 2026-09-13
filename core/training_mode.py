from dataclasses import dataclass
from enum import Enum


class TrainingMode(Enum):

    AUTO = "auto"

    ML = "ml"

    DL = "dl"

    HYBRID = "hybrid"


@dataclass
class TrainingProfile:

    mode: TrainingMode

    nombre: str

    frameworks: list[str]

    nivel_recursos: str

    tiempo_estimado: str

    gpu_recomendada: bool

    descripcion: str