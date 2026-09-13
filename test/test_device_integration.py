from core.hardware_profiler import (
    HardwareProfiler
)

from core.device_manager import (
    DeviceManager
)


def main():

    # =====================================
    # HARDWARE
    # =====================================

    profiler = HardwareProfiler()

    hardware = profiler.analizar()

    # =====================================
    # DEVICE MANAGER
    # =====================================

    manager = DeviceManager()

    device = manager.registrar_local(

        hardware

    )

    # =====================================
    # RESULTADO
    # =====================================

    print(
        "\n========== DISPOSITIVO LOCAL =========="
    )

    print(
        f"ID: {device.id}"
    )

    print(
        f"Nombre: {device.nombre}"
    )

    print(
        f"Tipo: {device.tipo}"
    )

    print(
        f"Fabricante: {device.fabricante}"
    )

    print(
        f"Modelo: {device.modelo_equipo}"
    )

    print(
        f"Sistema: {device.sistema_operativo}"
    )

    print(
        f"RAM: {device.ram_gb} GB"
    )

    print(
        f"GPU: {device.gpu}"
    )

    print(
        f"CUDA: {device.cuda}"
    )

    print(
        f"Batería: "
        f"{device.bateria_porcentaje}"
    )

    print(
        f"Corriente: "
        f"{device.conectado_corriente}"
    )

    print(
        f"Estado: "
        f"{device.estado.value}"
    )

    print(
        f"Autorizado: "
        f"{device.autorizado}"
    )


if __name__ == "__main__":

    main()