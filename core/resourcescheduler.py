from resource_monitor import ResourceMonitor
from dataclasses import dataclass, field
from enum import Enum
class SchedulerLevel(Enum):

    BAJO = "bajo"

    MEDIO = "medio"

    ALTO = "alto"

    CRITICO = "critico"

class SchedulerAction(Enum):

    CONTINUAR = "continuar"

    PAUSAR = "pausar"

    REANUDAR = "reanudar"

    REDUCIR_BATCH = "reducir_batch"

    CAMBIAR_CPU = "cambiar_cpu"

    CAMBIAR_GPU = "cambiar_gpu"

    MIGRAR_DISPOSITIVO = "migrar_dispositivo"

    CREAR_CHECKPOINT = "crear_checkpoint"

    DETENER = "detener"


@dataclass
class SchedulerDecision:

    accion: SchedulerAction

    nivel: SchedulerLevel

    motivo: str

    recomendaciones: list[str] = field(
        default_factory=list
    )

    prioridad: int = 0

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
    nivel_recursos: SchedulerLevel
    recomendaciones: list[str] = field(
        default_factory=list
        )


    
class ResourceScheduler:
    
    def __init__(self, hardware_profile):
        self.resource_monitor = ResourceMonitor(hardware_profile)
        
    def obtener_recursos(self):
        cpu_percent = self.resource_monitor.obtener_cpu()
        ram_percent, ram_available_gb = self.resource_monitor.obtener_ram()
        gpu_available, gpu_percent, vram_used_gb, vram_total_gb = self.resource_monitor.obtener_gpu()

        return {
            "cpu_percent": cpu_percent,
            "ram_percent": ram_percent,
            "ram_available_gb": ram_available_gb,
            "gpu_available": gpu_available,
            "gpu_percent": gpu_percent,
            "vram_used_gb": vram_used_gb,
            "vram_total_gb": vram_total_gb
        }
    def decidir_nivel(self, resource_status: ResourceStatus) -> SchedulerLevel:

        if (
            resource_status.cpu_uso >= 95
            or
            resource_status.ram_uso >= 95
        ):
            return SchedulerLevel.CRITICO

        if resource_status.puede_hibrido:
                return SchedulerLevel.ALTO

        if resource_status.puede_ml:
                return SchedulerLevel.MEDIO

        return SchedulerLevel.BAJO

    def calculo(self):
        hardware = self.resource_monitor.hardware
        recursos = self.obtener_recursos()
        cpu_uso = recursos["cpu_percent"]
        ram_uso = recursos["ram_percent"]
        ram_disponible_gb = recursos["ram_available_gb"]
        gpu_disponible = hardware.gpu_disponible
        gpu_uso = recursos["gpu_percent"] if gpu_disponible else 0.0
        vram_disponible_gb = hardware.gpu_vram_gb - (recursos["vram_used_gb"] if recursos["vram_used_gb"] is not None else 0.0)
        
        puede_ml = (cpu_uso < 90 and ram_uso < 90)
        puede_dl = (gpu_disponible and vram_disponible_gb >= 2 and gpu_uso < 90)
        puede_hibrido = (puede_ml and puede_dl)
        
        nivel_recursos = self.decidir_nivel(ResourceStatus(
            cpu_uso=cpu_uso,
            ram_uso=ram_uso,
            ram_disponible_gb=ram_disponible_gb,
            gpu_disponible=gpu_disponible,
            gpu_uso=gpu_uso,
            vram_disponible_gb=vram_disponible_gb,
            puede_ml=puede_ml,
            puede_dl=puede_dl,
            puede_hibrido=puede_hibrido,
            nivel_recursos=SchedulerLevel.BAJO,  # Placeholder, will be updated
            recomendaciones=[]
        ))
        
        recomendaciones = []
        if cpu_uso > 80:
            recomendaciones.append("Reducir carga de CPU")
        if ram_uso > 80:
            recomendaciones.append("Liberar memoria RAM")
        if gpu_disponible and gpu_uso > 80:
            recomendaciones.append("Reducir carga de GPU")
        
        return ResourceStatus(
            cpu_uso=cpu_uso,
            ram_uso=ram_uso,
            ram_disponible_gb=ram_disponible_gb,
            gpu_disponible=gpu_disponible,
            gpu_uso=gpu_uso,
            vram_disponible_gb=vram_disponible_gb,
            puede_ml=puede_ml,
            puede_dl=puede_dl,
            puede_hibrido=puede_hibrido,
            nivel_recursos=nivel_recursos,
            recomendaciones=recomendaciones
        )
    def decidir_nivel(self, resource_status: ResourceStatus) -> SchedulerLevel:
        if resource_status.puede_hibrido:
            return SchedulerLevel.ALTO
        elif resource_status.puede_ml:
            return SchedulerLevel.MEDIO
        else:
            return SchedulerLevel.BAJO
    def decidir(self):
        resource_status = self.calculo()
        nivel = self.decidir_nivel(resource_status)
        recomendaciones = resource_status.recomendaciones

        if nivel == SchedulerLevel.CRITICO:
            recomendaciones.append(
                "El sistema está en un estado crítico. "
                "Se recomienda detener procesos intensivos."
            )
        elif nivel == SchedulerLevel.ALTO:
            recomendaciones.append(
                "La utilización del sistema es alta."
            )
        else:
            recomendaciones.append(
                "Los recursos permiten ejecutar "
                "entrenamiento."
            )

        if not self.resource_monitor.hardware.gpu_disponible:
            recomendaciones.append(
                "No hay GPU CUDA disponible. "
                "DL utilizará CPU."
            )

        return ResourceStatus(
            cpu_uso=resource_status.cpu_uso,
            ram_uso=resource_status.ram_uso,
            ram_disponible_gb=resource_status.ram_disponible_gb,
            gpu_disponible=resource_status.gpu_disponible,
            gpu_uso=resource_status.gpu_uso,
            vram_disponible_gb=resource_status.vram_disponible_gb,
            puede_ml=resource_status.puede_ml,
            puede_dl=resource_status.puede_dl,
            puede_hibrido=resource_status.puede_hibrido,
            nivel_recursos=nivel,
            recomendaciones=recomendaciones
        )
