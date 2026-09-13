from dataclasses import dataclass, field

from enum import Enum

import time

class ResourceLevel(Enum):

    LOW = "low"

    MODERATE = "moderate"

    HIGH = "high"

    CRITICAL = "critical"
@dataclass
class ResourceSnapshot:

    cpu_percent: float

    ram_percent: float

    ram_available_gb: float

    gpu_available: bool

    gpu_percent: float | None

    vram_used_gb: float | None

    vram_total_gb: float | None

    battery_percent: float | None

    charging: bool | None

    disk_free_gb: float

    estado_general: ResourceLevel

    recomendaciones: list[str] = field(
        default_factory=list
    )

    timestamp: float = field(
        default_factory=time.time
    )
    

class ResourceMonitor:

    def __init__(

        self,

        hardware_profile

    ):

        self.hardware = hardware_profile

        self.snapshots = []

    def obtener_cpu(self):
        try:

            import psutil

            cpu_percent = psutil.cpu_percent()

        except ImportError:

            cpu_percent = 0.0

        return cpu_percent
    def obtener_ram(self):
        try:

            import psutil

            ram = psutil.virtual_memory()

            ram_percent = ram.percent

            ram_available_gb = ram.available / (1024 ** 3)

        except ImportError:

            ram_percent = 0.0

            ram_available_gb = self.hardware.ram_gb

        return ram_percent, ram_available_gb
    def obtener_gpu(self):
        gpu_available = self.hardware.gpu_disponible

        gpu_percent = None

        vram_used_gb = None

        vram_total_gb = None

        if gpu_available:

            try:

                import torch

                if torch.cuda.is_available():

                    gpu_percent = None

                    vram_used_gb = (
                        torch.cuda.memory_allocated(0)
                        / (1024 ** 3)
                    )

                    vram_total_gb = (
                        torch.cuda.get_device_properties(0).total_memory
                        / (1024 ** 3)
                    )

            except ImportError:

                pass

        return gpu_available, gpu_percent, vram_used_gb, vram_total_gb
    def obtener_bateria(self):
        battery_percent = self.hardware.bateria_porcentaje

        charging = self.hardware.conectado_corriente

        return battery_percent, charging
    def obtener_disco(self):
        try:

            import psutil

            import os

            disk = psutil.disk_usage(os.path.abspath(os.sep))

            disk_free_gb = disk.free / (1024 ** 3)

        except ImportError:

            disk_free_gb = 0.0

        return disk_free_gb
    def evaluar_estado_general(self, cpu_percent, ram_percent, gpu_percent):
        if (
            cpu_percent > 90
            or ram_percent > 90
            or (gpu_percent is not None and gpu_percent > 90)
        ):

            return ResourceLevel.CRITICAL

        elif (
            cpu_percent > 75
            or ram_percent > 75
            or (gpu_percent is not None and gpu_percent > 75)
        ):

            return ResourceLevel.HIGH

        elif (
            cpu_percent > 50
            or ram_percent > 50
            or (gpu_percent is not None and gpu_percent > 50)
        ):

            return ResourceLevel.MODERATE

        else:

            return ResourceLevel.LOW
    def generar_recomendaciones(self, snapshot):

        recomendaciones = []

    # =====================================
    # ESTADO GENERAL
    # =====================================

        if snapshot.estado_general == ResourceLevel.CRITICAL:

            recomendaciones.append(
                "El sistema está en un estado crítico. Cierre aplicaciones innecesarias."
            )

        elif snapshot.estado_general == ResourceLevel.HIGH:

            recomendaciones.append(
                "El sistema está bajo alta carga."
            )

        elif snapshot.estado_general == ResourceLevel.MODERATE:

            recomendaciones.append(
                "El sistema tiene una carga moderada."
            )

        else:

            recomendaciones.append(
                "El sistema está funcionando normalmente."
            )

    # =====================================
    # CPU
    # =====================================

        if snapshot.cpu_percent >= 90:

            recomendaciones.append(
                "Uso de CPU muy alto."
            )

        elif snapshot.cpu_percent >= 70:

            recomendaciones.append(
                "La CPU está bastante ocupada."
            )

    # =====================================
    # RAM
    # =====================================

        if snapshot.ram_percent >= 90:

            recomendaciones.append(
                "La memoria RAM está casi llena."
            )

        elif snapshot.ram_percent >= 75:

            recomendaciones.append(
                "La memoria RAM comienza a ser limitada."
            )

    # =====================================
    # GPU
    # =====================================

        if not snapshot.gpu_available:

            recomendaciones.append(
                "No hay una GPU disponible. El entrenamiento utilizará CPU."
            )

        elif (
            snapshot.gpu_percent is not None
            and
            snapshot.gpu_percent >= 90
        ):

            recomendaciones.append(
                "La GPU está bajo una carga elevada."
            )

    # =====================================
    # BATERÍA
    # =====================================

        if (
            snapshot.battery_percent is not None
            and
            snapshot.charging is False
            and
            snapshot.battery_percent < 20
        ):

            recomendaciones.append(
                "La batería es baja. Se recomienda conectar el equipo."
            )

        # =====================================
        # DISCO
        # =====================================

        if snapshot.disk_free_gb < 10:

            recomendaciones.append(
                "Queda poco espacio libre en el disco."
            )

        return recomendaciones
    def Capturar(self):
        cpu_percent = self.obtener_cpu()

        ram_percent, ram_available_gb = self.obtener_ram()

        gpu_available, gpu_percent, vram_used_gb, vram_total_gb = self.obtener_gpu()

        battery_percent, charging = self.obtener_bateria()

        disk_free_gb = self.obtener_disco()

        estado_general = self.evaluar_estado_general(
            cpu_percent, ram_percent, gpu_percent
        )

        recomendaciones = self.generar_recomendaciones(snapshot)

        snapshot = ResourceSnapshot(
            cpu_percent=cpu_percent,
            ram_percent=ram_percent,
            ram_available_gb=ram_available_gb,
            gpu_available=gpu_available,
            gpu_percent=gpu_percent,
            vram_used_gb=vram_used_gb,
            vram_total_gb=vram_total_gb,
            battery_percent=battery_percent,
            charging=charging,
            disk_free_gb=disk_free_gb,
            estado_general=estado_general,
            recomendaciones=recomendaciones
        )

        self.snapshots.append(snapshot)

        return snapshot
    def ultimo_snapshot(self):
        if not self.snapshots:

            return None
        
        return self.snapshots[-1]

    

    def historial_snapshots(self):
        return self.snapshots
    
    def limpiar_historial(self):
        self.snapshots.clear()

    def imprimir_estado(self,snapshot):
        print("=========== RECURSO MONITOR =============")
        if snapshot.cpu_percent is not None:
            print(f"cpu.............{snapshot.cpu_percent:.1f}%")
        else:
            
            print("cpu.............N/A")
        print(f"ram.............{snapshot.ram_percent:.1f}%")
        print(f"ram disponible..{snapshot.ram_available_gb:.2f} GB")
        if snapshot.gpu_available:
            print(f"gpu.............{snapshot.gpu_percent}%")
        else:
            print("gpu.............N/A")
        if snapshot.gpu_available and snapshot.vram_used_gb is not None:
            print(f"vram usada......{snapshot.vram_used_gb:.2f} GB")
        else:
            print("vram usada......N/A")
        if snapshot.vram_total_gb is not None:
            print(f"vram total......{snapshot.vram_total_gb:.2f} GB")
        else:    
            print("vram total......N/A")
        if snapshot.battery_percent is not None:
            print(f"bateria.........{snapshot.battery_percent}%")
        else:
            print("bateria.........N/A")
        if snapshot.charging is not None:
            print(f"cargando........{snapshot.charging}")
        else:
            print("cargando........N/A")
        
        print(f"disco libre.....{snapshot.disk_free_gb:.2f} GB")
        print(f"estado general..{snapshot.estado_general.value}")
        print("recomendaciones:")
        for recomendacion in snapshot.recomendaciones:
            print(f"- {recomendacion}")
        