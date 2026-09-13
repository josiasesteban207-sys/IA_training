from dataclasses import dataclass, field


@dataclass
class PreparationAction:

    nombre: str

    descripcion: str

    prioridad: str

    automatizable: bool


@dataclass
class PreparationPlan:

    acciones: list[PreparationAction] = field(

        default_factory=list

    )

    estado: str = "pendiente"


class DatasetPreparationEngine:

    def crear_plan(

        self,

        profile

    ):

        plan = PreparationPlan()

        # =====================================
        # DUPLICADOS
        # =====================================

        if profile.duplicados > 0:

            plan.acciones.append(

                PreparationAction(

                    nombre=(
                        "eliminar_duplicados"
                    ),

                    descripcion=(

                        "Eliminar archivos "
                        "duplicados detectados."

                    ),

                    prioridad="alta",

                    automatizable=True

                )

            )

        # =====================================
        # ARCHIVOS CORRUPTOS
        # =====================================

        if profile.archivos_corruptos > 0:

            plan.acciones.append(

                PreparationAction(

                    nombre=(

                        "aislar_corruptos"

                    ),

                    descripcion=(

                        "Separar archivos "
                        "corruptos del dataset."

                    ),

                    prioridad="alta",

                    automatizable=True

                )

            )

        # =====================================
        # DESBALANCE
        # =====================================

        if profile.clases:

            cantidades = (

                list(

                    profile.clases.values()

                )

            )

            minimo = min(

                cantidades

            )

            maximo = max(

                cantidades

            )

            if maximo > (

                minimo * 3

            ):

                plan.acciones.append(

                    PreparationAction(

                        nombre=(

                            "balancear_clases"

                        ),

                        descripcion=(

                            "Existe un desbalance "
                            "significativo entre clases."

                        ),

                        prioridad="media",

                        automatizable=False

                    )

                )

        # =====================================
        # DIVISIÓN
        # =====================================

        plan.acciones.append(

            PreparationAction(

                nombre=(

                    "dividir_dataset"

                ),

                descripcion=(

                    "Crear conjuntos "
                    "train, validation y test."

                ),

                prioridad="alta",

                automatizable=False

            )

        )

        # =====================================
        # NORMALIZACIÓN
        # =====================================

        if profile.tipo == "image":

            plan.acciones.append(

                PreparationAction(

                    nombre=(

                        "normalizar_imagenes"

                    ),

                    descripcion=(

                        "Preparar imágenes "
                        "para el modelo."

                    ),

                    prioridad="media",

                    automatizable=False

                )

            )

        # =====================================
        # ESTADO
        # =====================================

        if plan.acciones:

            plan.estado = (

                "pendiente_aprobacion"

            )

        else:

            plan.estado = (

                "sin_acciones"

            )

        return plan