
from dataclasses import dataclass, field

import os
import platform

from torch import device


from core.device_type_detector import (
    DeviceTypeDetector
)


@dataclass
class HardwareProfile:

    # ============================
    # IDENTIDAD
    # ============================

    device_id: str

    nombre_equipo: str

    fabricante: str

    modelo_equipo: str

    tipo_dispositivo: str      # desktop, laptop, servidor

    sistema_operativo: str

    arquitectura: str

    # ============================
    # CPU
    # ============================

    cpu: str

    nucleos_fisicos: int

    nucleos_logicos: int

    frecuencia_cpu_mhz: float

    # ============================
    # MEMORIA
    # ============================

    ram_total_gb: float

    ram_disponible_gb: float

    ram_utilizada_gb: float

    # ============================
    # GPU
    # ============================

    gpu_disponible: bool

    gpu_nombre: str | None

    gpu_vram_gb: float

    cuda_disponible: bool

    cuda_version: str | None

    # ============================
    # ALMACENAMIENTO
    # ============================

    espacio_total_gb: float

    espacio_libre_gb: float

    disco_ssd: bool | None

    # ============================
    # ENERGÍA
    # ============================

    tiene_bateria: bool

    bateria_porcentaje: float | None

    conectado_corriente: bool | None

    # ============================
    # RED
    # ============================

    hostname: str

    direccion_mac: str

    direccion_ip: str | None

    # ============================
    # CAPACIDADES
    # ============================

    soporta_ml: bool

    soporta_dl: bool

    soporta_hibrido: bool

    # ============================
    # RECOMENDACIONES
    # ============================

    recomendaciones: list[str] = field(
        default_factory=list
    )


class HardwareProfiler:

    def __init__(self):

        self.profile = None

        self.device_detector = (
            DeviceTypeDetector()
        )

    # =====================================
    # ANALIZAR HARDWARE
    # =====================================

    def analizar(self):

        # =================================
        # SISTEMA OPERATIVO
        # =================================

        sistema_operativo = (
            platform.system()
        )

        arquitectura = (
            platform.machine()
        )

        nombre_equipo = (
            platform.node()
        )

        # =================================
        # TIPO DE DISPOSITIVO
        # =================================

        device_info = (
            self.device_detector.detectar()
        )

        tipo_dispositivo = (
            device_info.tipo
        )

        fabricante = (
            device_info.fabricante
        )

        modelo_equipo = (
            device_info.modelo
        )

        tiene_bateria = (
            device_info.tiene_bateria
        )

        bateria_porcentaje = (
            device_info.bateria_porcentaje
        )

        conectado_corriente = (
            device_info.conectado_corriente
        )

        # =================================
        # CPU
        # =================================

        cpu = (
            platform.processor()
            or "Desconocido"
        )

        nucleos_fisicos = (
            self._obtener_nucleos_fisicos()
        )

        nucleos_logicos = (
            os.cpu_count()
            or 1
        )

        # =================================
        # RAM
        # =================================

        ram_total_gb = 0.0

        ram_disponible_gb = 0.0

        try:

            import psutil

            ram = psutil.virtual_memory()

            ram_total_gb = round(

                ram.total
                / (1024 ** 3),

                2

            )

            ram_disponible_gb = round(

                ram.available
                / (1024 ** 3),

                2

            )

        except ImportError:

            pass
        
        # =================================
        # GPU / CUDA / PYTORCH
        # =================================

        gpu_disponible = False

        gpu_nombre = None

        gpu_vram_gb = 0.0

        cuda_disponible = False

        cuda_version = None

        pytorch_disponible = False

        try:

            import torch

            pytorch_disponible = True

            cuda_disponible = (
                torch.cuda.is_available()
            )

            cuda_version = (
                torch.version.cuda
            )

            if cuda_disponible:

                gpu_disponible = True

                gpu_nombre = (
                    torch.cuda
                    .get_device_name(0)
                )

                memoria = (torch.cuda.get_device_properties(0).total_memory)

                gpu_vram_gb = round(

                    memoria
                    / (1024 ** 3),

                    2

                )

        except ImportError:

            pass

        except Exception:

            pass

        # =================================
        # DISPOSITIVO PRINCIPAL
        # =================================

        if cuda_disponible:

            dispositivo_principal = "cuda"

        else:

            dispositivo_principal = "cpu"

        # =================================
        # RECOMENDACIONES
        # =================================

        recomendaciones = (
            self._generar_recomendaciones(

                ram_disponible_gb,

                gpu_disponible,

                gpu_vram_gb,

                cuda_disponible,

                nucleos_logicos,

                tipo_dispositivo,

                bateria_porcentaje,

                conectado_corriente

            )
        )

        # =================================
        # CREAR PERFIL
        # =================================

        self.profile = HardwareProfile(

            sistema_operativo=(
                sistema_operativo
            ),

            arquitectura=(
                arquitectura
            ),

            nombre_equipo=(
                nombre_equipo
            ),

            tipo_dispositivo=(
                tipo_dispositivo
            ),

            fabricante=(
                fabricante
            ),

            modelo_equipo=(
                modelo_equipo
            ),

            cpu=cpu,

            nucleos_fisicos=(
                nucleos_fisicos
            ),

            nucleos_logicos=(
                nucleos_logicos
            ),

            ram_total_gb=(
                ram_total_gb
            ),

            ram_disponible_gb=(
                ram_disponible_gb
            ),

            gpu_disponible=(
                gpu_disponible
            ),

            gpu_nombre=(
                gpu_nombre
            ),

            gpu_vram_gb=(
                gpu_vram_gb
            ),

            cuda_disponible=(
                cuda_disponible
            ),

            cuda_version=(
                cuda_version
            ),

            pytorch_disponible=(
                pytorch_disponible
            ),

            dispositivo_principal=(
                dispositivo_principal
            ),

            tiene_bateria=(
                tiene_bateria
            ),

            bateria_porcentaje=(
                bateria_porcentaje
            ),

            conectado_corriente=(
                conectado_corriente
            ),

            recomendaciones=(
                recomendaciones
            )

        )

        return self.profile

    # =====================================
    # CPU
    # =====================================

    def _obtener_nucleos_fisicos(self):

        try:

            import psutil

            return (

                psutil.cpu_count(
                    logical=False
                )

                or 1

            )

        except ImportError:

            return 1

    # =====================================
    # RECOMENDACIONES
    # =====================================

    def _generar_recomendaciones(

        self,

        ram_disponible,

        gpu_disponible,

        gpu_vram,

        cuda_disponible,

        nucleos,

        tipo_dispositivo,

        bateria_porcentaje,

        conectado_corriente

    ):

        recomendaciones = []

        # =================================
        # GPU
        # =================================

        if not gpu_disponible:

            recomendaciones.append(

                "No se detectó una GPU "
                "compatible. Se utilizará CPU."

            )

        elif gpu_vram < 4:

            recomendaciones.append(

                "VRAM limitada. "
                "Se recomienda utilizar "
                "batches pequeños."

            )

        elif gpu_vram < 8:

            recomendaciones.append(

                "GPU adecuada para "
                "entrenamiento moderado."

            )

        else:

            recomendaciones.append(

                "GPU adecuada para "
                "entrenamiento de mayor carga."

            )

        # =================================
        # RAM
        # =================================

        if ram_disponible < 4:

            recomendaciones.append(

                "RAM disponible baja. "
                "Evitar cargas de trabajo grandes."

            )

        elif ram_disponible < 8:

            recomendaciones.append(

                "RAM disponible moderada."

            )

        else:

            recomendaciones.append(

                "RAM disponible suficiente "
                "para cargas de trabajo mayores."

            )

        # =================================
        # CUDA
        # =================================

        if cuda_disponible:

            recomendaciones.append(

                "CUDA está disponible "
                "para aceleración GPU."

            )

        # =================================
        # CPU
        # =================================

        if nucleos >= 8:

            recomendaciones.append(

                "El procesador dispone de "
                "suficientes núcleos para "
                "procesamiento paralelo."

            )

        # =================================
        # TIPO DE DISPOSITIVO
        # =================================

        if tipo_dispositivo == "laptop":

            recomendaciones.append(

                "El dispositivo es una laptop. "
                "Se tendrá en cuenta el estado "
                "de batería durante el entrenamiento."

            )

        elif tipo_dispositivo == "desktop":

            recomendaciones.append(

                "El dispositivo es un PC de escritorio. "
                "Es adecuado para cargas sostenidas."

            )

        # =================================
        # BATERÍA
        # =================================

        if (

            tipo_dispositivo == "laptop"

            and

            bateria_porcentaje is not None

        ):

            if (

                bateria_porcentaje < 20

                and

                conectado_corriente is not True

            ):

                recomendaciones.append(

                    "Batería baja y el dispositivo "
                    "no está conectado a corriente. "
                    "Se recomienda evitar "
                    "entrenamientos pesados."

                )

            elif (

                conectado_corriente is True

            ):

                recomendaciones.append(

                    "La laptop está conectada "
                    "a corriente."

                )

        return recomendaciones

