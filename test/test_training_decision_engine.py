from core.hardware_profiler import (
    HardwareProfiler
)

from core.resource_manager import (
    ResourceManager
)

from core.training_decision_engine import (
    TrainingDecisionEngine
)


def main():

    profiler = HardwareProfiler()

    hardware = profiler.analizar()

    resources = ResourceManager(

        hardware

    ).analizar()

    engine = TrainingDecisionEngine(

        hardware,

        resources

    )

    decision = engine.decidir(

        tipo_tarea="clasificacion",

        tamano_dataset=3000,

        precision_objetivo=0.90

    )

    print(
        "\n========== DECISIÓN =========="
    )

    print(
        f"Tipo: "
        f"{decision.tipo_entrenamiento}"
    )

    print(
        f"Estrategia: "
        f"{decision.estrategia}"
    )

    print(
        f"Framework: "
        f"{decision.framework}"
    )

    print(
        f"Dispositivo: "
        f"{decision.dispositivo}"
    )

    print(
        f"Confianza: "
        f"{decision.confianza}"
    )

    print(
        f"\nMotivo:\n"
        f"{decision.motivo}"
    )

    print(
        "\n===== RECOMENDACIONES ====="
    )

    for recomendacion in (

        decision.recomendaciones

    ):

        print(
            f"- {recomendacion}"
        )


if __name__ == "__main__":

    main()