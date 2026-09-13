from dataclasses import dataclass


@dataclass
class ResourceStatus:

    cpu_uso: float

    ram_uso: float

    ram_disponible_gb: float

    gpu_disponible: bool

    gpu_uso: float

    vram_disponible_gb: float

    puede_ml: bool

    puede_dl: bool

    puede_hibrido: bool

    nivel_recursos: str

    recomendaciones: list[str]


class ResourceManager:

    def __init__(self, hardware_profile):

        self.hardware = hardware_profile

    # =====================================
    # ANALIZAR RECURSOS
    # =====================================

    def analizar(self):

        cpu_uso = 0.0

        ram_uso = 0.0

        gpu_uso = 0.0

        vram_disponible = (

            self.hardware.gpu_vram_gb

        )

        # =================================
        # PSUTIL
        # =================================

        try:

            import psutil

            cpu_uso = (

                psutil.cpu_percent(

                    interval=0.5

                )

            )

            ram = psutil.virtual_memory()

            ram_uso = ram.percent

        except ImportError:

            pass

        # =================================
        # CAPACIDADES
        # =================================

        puede_ml = True

        puede_dl = (

            self.hardware.gpu_disponible

            or

            self.hardware.ram_total_gb >= 16

        )

        puede_hibrido = (

            puede_dl

            and

            self.hardware.ram_total_gb >= 16

        )

        # =================================
        # NIVEL DE RECURSOS
        # =================================

        if (

            ram_uso >= 90

            or

            cpu_uso >= 90

        ):

            nivel = "critico"

        elif (

            ram_uso >= 75

            or

            cpu_uso >= 75

        ):

            nivel = "alto"

        elif (

            ram_uso >= 50

            or

            cpu_uso >= 50

        ):

            nivel = "moderado"

        else:

            nivel = "disponible"

        recomendaciones = []

        if nivel == "critico":

            recomendaciones.append(

                "Los recursos están muy ocupados. "
                "Se recomienda reducir la carga."

            )

        elif nivel == "alto":

            recomendaciones.append(

                "La utilización del sistema es alta."

            )

        else:

            recomendaciones.append(

                "Los recursos permiten ejecutar "
                "entrenamiento."

            )

        if not self.hardware.gpu_disponible:

            recomendaciones.append(

                "No hay GPU CUDA disponible. "
                "DL utilizará CPU."

            )

        return ResourceStatus(

            cpu_uso=cpu_uso,

            ram_uso=ram_uso,

            ram_disponible_gb=(

                self.hardware.ram_disponible_gb

            ),

            gpu_disponible=(

                self.hardware.gpu_disponible

            ),

            gpu_uso=gpu_uso,

            vram_disponible_gb=(

                vram_disponible

            ),

            puede_ml=puede_ml,

            puede_dl=puede_dl,

            puede_hibrido=puede_hibrido,

            nivel_recursos=nivel,

            recomendaciones=recomendaciones

        )