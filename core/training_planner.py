from dataclasses import dataclass

from core.training_strategy import (
    TrainingStrategyPlanner
)


@dataclass
class TrainingPlan:

    decision: object

    estrategia: object


class TrainingPlanner:

    def __init__(

        self,

        decision_engine,

        strategy_planner=None

    ):

        self.decision_engine = (
            decision_engine
        )

        self.strategy_planner = (

            strategy_planner

            or

            TrainingStrategyPlanner()

        )

    def crear_plan(

        self,

        tipo_tarea,

        modelo,

        tamano_dataset,

        precision_objetivo=0.90,

        permitir_hibrido=True

    ):

        # =================================
        # DECISIÓN
        # =================================

        decision = (

            self.decision_engine.decidir(

                tipo_tarea=tipo_tarea,

                tamano_dataset=tamano_dataset,

                precision_objetivo=(
                    precision_objetivo
                ),

                permitir_hibrido=(
                    permitir_hibrido
                )

            )

        )

        # =================================
        # ESTRATEGIA
        # =================================

        estrategia = (

            self.strategy_planner.crear_estrategia(

                tipo_entrenamiento=(

                    decision.tipo_entrenamiento

                ),

                framework=(

                    decision.framework

                ),

                modelo=modelo,

                dispositivo=(

                    decision.dispositivo

                ),

                gpu_vram=(

                    self.decision_engine
                    .hardware
                    .gpu_vram_gb

                ),

                ram_disponible=(

                    self.decision_engine
                    .hardware
                    .ram_disponible_gb

                ),

                nucleos_cpu=(

                    self.decision_engine
                    .hardware
                    .nucleos_logicos

                ),

                tamano_dataset=(

                    tamano_dataset

                ),

                precision_objetivo=(

                    precision_objetivo

                )

            )

        )

        return TrainingPlan(

            decision=decision,

            estrategia=estrategia

        )