from dataclasses import dataclass, field

from typing import Any


@dataclass
class EvaluationPolicy:

    nombre: str

    metricas_minimas: dict[str, float] = field(

        default_factory=dict

    )

    metricas_criticas: list[str] = field(

        default_factory=list

    )


@dataclass
class PolicyResult:

    estado: str

    metricas_cumplidas: dict[str, bool]

    recomendaciones: list[str] = field(

        default_factory=list

    )


class EvaluationPolicyEngine:

    def evaluar(

        self,

        resultado: Any,

        politica: EvaluationPolicy

    ):

        metricas = resultado.metricas

        metricas_cumplidas = {}

        recomendaciones = []

        # =========================================
        # EVALUAR CADA MÉTRICA
        # =========================================

        for nombre, minimo in (

            politica.metricas_minimas.items()

        ):

            valor = metricas.get(

                nombre

            )

            if valor is None:

                metricas_cumplidas[

                    nombre

                ] = False

                recomendaciones.append(

                    f"No se encontró "
                    f"la métrica '{nombre}'."

                )

                continue

            # =====================================
            # MÉTRICAS DONDE MAYOR ES MEJOR
            # =====================================

            if nombre in [

                "accuracy",

                "precision",

                "recall",

                "f1",

                "r2"

            ]:

                cumple = (

                    valor >= minimo

                )

            # =====================================
            # MÉTRICAS DONDE MENOR ES MEJOR
            # =====================================

            elif nombre in [

                "mae",

                "mse",

                "rmse"

            ]:

                cumple = (

                    valor <= minimo

                )

            else:

                cumple = (

                    valor >= minimo

                )

            metricas_cumplidas[

                nombre

            ] = cumple

        # =========================================
        # ANALIZAR MÉTRICAS CRÍTICAS
        # =========================================

        metricas_criticas_fallidas = []

        for metrica in (

            politica.metricas_criticas

        ):

            if not metricas_cumplidas.get(

                metrica,

                False

            ):

                metricas_criticas_fallidas.append(

                    metrica

                )

        # =========================================
        # DECISIÓN
        # =========================================

        if metricas_criticas_fallidas:

            estado = "rechazado"

            recomendaciones.append(

                "Una o más métricas críticas "
                "no alcanzaron el objetivo."

            )

            recomendaciones.append(

                "Métricas críticas fallidas: "

                + ", ".join(

                    metricas_criticas_fallidas

                )

            )

        elif all(

            metricas_cumplidas.values()

        ):

            estado = "aprobado"

            recomendaciones.append(

                "El modelo cumple "
                "con todos los objetivos."

            )

        else:

            estado = "mejorar"

            recomendaciones.append(

                "El modelo cumple algunos "
                "objetivos, pero necesita mejoras."

            )

        return PolicyResult(

            estado=estado,

            metricas_cumplidas=(

                metricas_cumplidas

            ),

            recomendaciones=recomendaciones

        )