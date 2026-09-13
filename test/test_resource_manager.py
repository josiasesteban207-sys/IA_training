from core.hardware_profiler import (
    HardwareProfiler
)

from core.resource_manager import (
    ResourceManager
)


def main():

    profiler = HardwareProfiler()

    hardware = profiler.analizar()

    manager = ResourceManager(

        hardware

    )

    recursos = manager.analizar()

    print(
        "\n========== RECURSOS =========="
    )

    print(
        f"CPU: {recursos.cpu_uso}%"
    )

    print(
        f"RAM: {recursos.ram_uso}%"
    )

    print(
        f"RAM disponible: "
        f"{recursos.ram_disponible_gb} GB"
    )

    print(
        f"GPU disponible: "
        f"{recursos.gpu_disponible}"
    )

    print(
        f"VRAM disponible: "
        f"{recursos.vram_disponible_gb} GB"
    )

    print(
        f"Nivel: "
        f"{recursos.nivel_recursos}"
    )

    print(
        "\n===== CAPACIDADES ====="
    )

    print(
        f"ML: {recursos.puede_ml}"
    )

    print(
        f"DL: {recursos.puede_dl}"
    )

    print(
        f"Híbrido: {recursos.puede_hibrido}"
    )

    print(
        "\n===== RECOMENDACIONES ====="
    )

    for recomendacion in (

        recursos.recomendaciones

    ):

        print(
            f"- {recomendacion}"
        )


if __name__ == "__main__":

    main()