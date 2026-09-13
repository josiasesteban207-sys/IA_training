from core.hardware_profiler import (
    HardwareProfiler
)

from core.resource_manager import (
    ResourceManager
)

from core.training_decision_engine import (
    TrainingDecisionEngine
)

from core.training_planner import (
    TrainingPlanner
)


def main():

    # =====================================
    # HARDWARE
    # =====================================

    profiler = HardwareProfiler()

    hardware = profiler.analizar()

    # =====================================
    # RECURSOS
    # =====================================

    resources = ResourceManager(

        hardware

    ).analizar()

    # =====================================
    # DECISIÓN
    # =====================================

    decision_engine = (

        TrainingDecisionEngine(

            hardware,

            resources

        )

    )

    # =====================================
    # PLANIFICADOR
    # =====================================

    planner = TrainingPlanner(

        decision_engine

    )

    # =====================================
    # CREAR PLAN
    # =====================================

    plan = planner.crear_plan(

        tipo_tarea="clasificacion",

        modelo="RandomForest",

        tamano_dataset=3000,

        precision_objetivo=0.90

    )

    decision = plan.decision

    estrategia = plan.estrategia

    # =====================================
    # RESULTADO
    # =====================================

    print(
        "\n========== PLAN =========="
    )

    print(
        f"Tipo: "
        f"{decision.tipo_entrenamiento}"
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
        "\n===== ESTRATEGIA ====="
    )

    print(
        f"Modelo: "
        f"{estrategia.modelo}"
    )

    print(
        f"Batch: "
        f"{estrategia.batch_size}"
    )

    print(
        f"Epochs: "
        f"{estrategia.epochs}"
    )

    print(
        f"Learning rate: "
        f"{estrategia.learning_rate}"
    )

    print(
        f"Workers: "
        f"{estrategia.num_workers}"
    )

    print(
        f"Checkpoint: "
        f"{estrategia.guardar_checkpoint}"
    )

    print(
        f"Early stopping: "
        f"{estrategia.usar_early_stopping}"
    )

    print(
        f"Precision mixta: "
        f"{estrategia.precision_mixta}"
    )

    print(
        f"Optimización: "
        f"{estrategia.optimizar_hiperparametros}"
    )

    print(
        "\n===== RECOMENDACIONES ====="
    )

    for recomendacion in (

        decision.recomendaciones

        +

        estrategia.recomendaciones

    ):

        print(
            f"- {recomendacion}"
        )


if __name__ == "__main__":

    main()