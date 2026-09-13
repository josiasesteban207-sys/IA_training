from core.hardware_profiler import (
    HardwareProfiler
)


def main():

    profiler = HardwareProfiler()

    hardware = profiler.analizar()

    print(
        "\n========== HARDWARE =========="
    )

    print(
        f"Sistema: "
        f"{hardware.sistema_operativo}"
    )

    print(
        f"Arquitectura: "
        f"{hardware.arquitectura}"
    )

    print(
        f"CPU: "
        f"{hardware.cpu}"
    )

    print(
        f"Núcleos físicos: "
        f"{hardware.nucleos_fisicos}"
    )

    print(
        f"Núcleos lógicos: "
        f"{hardware.nucleos_logicos}"
    )

    print(
        f"RAM total: "
        f"{hardware.ram_total_gb} GB"
    )

    print(
        f"RAM disponible: "
        f"{hardware.ram_disponible_gb} GB"
    )

    print(
        f"GPU: "
        f"{hardware.gpu_nombre}"
    )

    print(
        f"VRAM: "
        f"{hardware.gpu_vram_gb} GB"
    )

    print(
        f"CUDA: "
        f"{hardware.cuda_disponible}"
    )

    print(
        f"Versión CUDA: "
        f"{hardware.cuda_version}"
    )

    print(
        f"Dispositivo: "
        f"{hardware.dispositivo_principal}"
    )

    print(
        "\n===== RECOMENDACIONES ====="
    )

    for recomendacion in (
        hardware.recomendaciones
    ):

        print(
            f"- {recomendacion}"
        )


if __name__ == "__main__":

    main()