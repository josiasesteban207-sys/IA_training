from dataclasses import dataclass, field

from datetime import datetime

from pathlib import Path

from typing import Any


@dataclass
class ModelRecord:

    id: int

    nombre: str

    framework: str

    arquitectura: str

    dataset: str

    version: str

    metricas: dict[str, float] = field(

        default_factory=dict

    )

    estado: str = "registrado"

    ruta_modelo: str | None = None

    creado: str = field(

        default_factory=lambda:

        datetime.now().isoformat()

    )


class ModelRegistry:

    def __init__(

        self,

        directorio="models"

    ):

        self.directorio = Path(

            directorio

        )

        self.directorio.mkdir(

            parents=True,

            exist_ok=True

        )

        self.modelos = {}

        self.contador = 0

    # ==========================================
    # REGISTRAR MODELO
    # ==========================================

    def registrar(

        self,

        nombre,

        framework,

        arquitectura,

        dataset,

        version,

        metricas,

        ruta_modelo=None

    ):

        self.contador += 1

        modelo_id = self.contador

        registro = ModelRecord(

            id=modelo_id,

            nombre=nombre,

            framework=framework,

            arquitectura=arquitectura,

            dataset=dataset,

            version=version,

            metricas=metricas,

            ruta_modelo=ruta_modelo

        )

        self.modelos[

            modelo_id

        ] = registro

        return registro

    # ==========================================
    # OBTENER MODELO
    # ==========================================

    def obtener(

        self,

        modelo_id

    ):

        return self.modelos.get(

            modelo_id

        )

    # ==========================================
    # LISTAR MODELOS
    # ==========================================

    def listar(self):

        return list(

            self.modelos.values()

        )

    # ==========================================
    # CAMBIAR ESTADO
    # ==========================================

    def cambiar_estado(

        self,

        modelo_id,

        estado

    ):

        modelo = self.obtener(

            modelo_id

        )

        if modelo is None:

            raise ValueError(

                "Modelo no encontrado."

            )

        modelo.estado = estado

        return modelo