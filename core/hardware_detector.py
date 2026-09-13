import platform
import shutil

from dataclasses import dataclass

try:
    import psutil
except ImportError:
    psutil = None


@dataclass
class HardwareProfile:

    sistema: str

    procesador: str

    ram_gb: float

    gpu_disponible: bool

    gpu_nombre: str

    vram_gb: float

    cuda_disponible: bool

    pytorch_disponible: bool

    # =====================================
    # INFORMACIÓN DEL DISPOSITIVO
    # =====================================

    nombre_equipo: str

    tipo_dispositivo: str

    fabricante: str

    modelo_equipo: str

    tiene_bateria: bool

    bateria_porcentaje: float | None

    conectado_corriente: bool | None


class HardwareDetector:

    def detectar(self):

        # =====================================
        # SISTEMA OPERATIVO
        # =====================================

        sistema = platform.system()

        # =====================================
        # PROCESADOR
        # =====================================

        procesador = platform.processor()
        from core.device_type_detector import (
    DeviceTypeDetector
        )
        device_detector = DeviceTypeDetector()
        device_info = device_detector.detectar()
        if not procesador:

            procesador = (

                platform.machine()

            )

        # =====================================
        # RAM
        # =====================================

        if psutil:

            ram_gb = (

                psutil.virtual_memory().total

                / (1024 ** 3)

            )

        else:

            ram_gb = 0.0

        # =====================================
        # PYTORCH
        # =====================================

        pytorch_disponible = False

        gpu_disponible = False

        gpu_nombre = "No detectada"

        vram_gb = 0.0

        cuda_disponible = False

        try:

            import torch

            pytorch_disponible = True

            cuda_disponible = (

                torch.cuda.is_available()

            )

            if cuda_disponible:

                gpu_disponible = True

                gpu_nombre = (

                    torch.cuda.get_device_name(

                        0

                    )

                )

                vram_gb = (

                    torch.cuda.get_device_properties(

                        0

                    ).total_memory

                    / (1024 ** 3)

                )

        except ImportError:

            pass

        return HardwareProfile(

            sistema=sistema,

            procesador=procesador,

            ram_gb=round(

                ram_gb,

                2

            ),

            gpu_disponible=(

                gpu_disponible

            ),

            gpu_nombre=gpu_nombre,

            vram_gb=round(

                vram_gb,

                2

            ),

            cuda_disponible=(

                cuda_disponible

            ),

            pytorch_disponible=(

                pytorch_disponible

            )

            nombre_equipo=(
                device_info.nombre_equipo
            ),

            tipo_dispositivo=(
                device_info.tipo
            ),

            fabricante=(
                device_info.fabricante
            ),

            modelo_equipo=(
                device_info.modelo
            ),

            tiene_bateria=(
                device_info.tiene_bateria
            ),

            bateria_porcentaje=(
                device_info.bateria_porcentaje
            ),

            conectado_corriente=(
                device_info.conectado_corriente
            )

        )