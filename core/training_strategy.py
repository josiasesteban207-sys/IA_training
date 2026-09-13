from dataclasses import dataclass, field


@dataclass
class TrainingStrategy:

    tipo_entrenamiento: str

    framework: str

    modelo: str

    estrategia: str

    dispositivo: str

    batch_size: int

    epochs: int

    learning_rate: float

    precision_objetivo: float

    num_workers: int

    guardar_checkpoint: bool

    usar_early_stopping: bool

    precision_mixta: bool

    optimizar_hiperparametros: bool

    recomendaciones: list[str] = field(
        default_factory=list
    )


class TrainingStrategyPlanner:

    def crear_estrategia(

        self,

        tipo_entrenamiento,

        framework,

        modelo,

        dispositivo,

        gpu_vram,

        ram_disponible,

        nucleos_cpu,

        tamano_dataset,

        precision_objetivo=0.90

    ):

        recomendaciones = []

        # =====================================
        # CONFIGURACIÓN BASE
        # =====================================

        batch_size = 16

        epochs = 30

        learning_rate = 0.001

        num_workers = 1

        guardar_checkpoint = True

        usar_early_stopping = True

        precision_mixta = False

        optimizar_hiperparametros = False

        estrategia = "entrenamiento_estandar"

        # =====================================
        # CONFIGURAR SEGÚN DISPOSITIVO
        # =====================================

        if dispositivo == "cuda":

            precision_mixta = True

            recomendaciones.append(

                "Se habilita precisión mixta "
                "para aprovechar la GPU."

            )

        else:

            precision_mixta = False

            recomendaciones.append(

                "El entrenamiento se realizará "
                "utilizando CPU."

            )

        # =====================================
        # CONFIGURAR BATCH SEGÚN VRAM
        # =====================================

        if dispositivo == "cuda":

            if gpu_vram < 4:

                batch_size = 8

            elif gpu_vram < 8:

                batch_size = 16

            else:

                batch_size = 32

        else:

            batch_size = 8

        # =====================================
        # CPU
        # =====================================

        if nucleos_cpu >= 8:

            num_workers = 4

        elif nucleos_cpu >= 4:

            num_workers = 2

        else:

            num_workers = 1

        # =====================================
        # DATASET PEQUEÑO
        # =====================================

        if tamano_dataset < 5000:

            estrategia = (

                "dataset_pequeno"

            )

            epochs = 20

            recomendaciones.append(

                "Dataset pequeño: se prioriza "
                "un entrenamiento rápido."

            )

        # =====================================
        # DATASET MEDIO
        # =====================================

        elif tamano_dataset < 50000:

            estrategia = (

                "dataset_medio"

            )

            epochs = 30

            recomendaciones.append(

                "Dataset de tamaño medio."

            )

        # =====================================
        # DATASET GRANDE
        # =====================================

        else:

            estrategia = (

                "dataset_grande"

            )

            epochs = 50

            recomendaciones.append(

                "Dataset grande: se permite "
                "un entrenamiento más prolongado."

            )

        # =====================================
        # HÍBRIDO
        # =====================================

        if tipo_entrenamiento == "hibrido":

            estrategia = (

                "ml_dl_hibrido"

            )

            optimizar_hiperparametros = True

            recomendaciones.append(

                "Se utilizará una estrategia "
                "híbrida ML + DL."

            )

        # =====================================
        # PRECISIÓN ALTA
        # =====================================

        if precision_objetivo >= 0.95:

            epochs += 20

            optimizar_hiperparametros = True

            recomendaciones.append(

                "Objetivo de precisión alto: "
                "se habilita optimización adicional."

            )

        # =====================================
        # RAM BAJA
        # =====================================

        if ram_disponible < 4:

            batch_size = min(

                batch_size,

                4

            )

            num_workers = 1

            recomendaciones.append(

                "RAM limitada: se reduce "
                "la carga del entrenamiento."

            )

        elif ram_disponible < 8:

            batch_size = min(

                batch_size,

                8

            )

            recomendaciones.append(

                "RAM moderada: se limita "
                "el tamaño del batch."

            )

        # =====================================
        # RESULTADO
        # =====================================

        return TrainingStrategy(

            tipo_entrenamiento=(

                tipo_entrenamiento

            ),

            framework=framework,

            modelo=modelo,

            estrategia=estrategia,

            dispositivo=dispositivo,

            batch_size=batch_size,

            epochs=epochs,

            learning_rate=learning_rate,

            precision_objetivo=(

                precision_objetivo

            ),

            num_workers=num_workers,

            guardar_checkpoint=(

                guardar_checkpoint

            ),

            usar_early_stopping=(

                usar_early_stopping

            ),

            precision_mixta=(

                precision_mixta

            ),

            optimizar_hiperparametros=(

                optimizar_hiperparametros

            ),

            recomendaciones=(

                recomendaciones

            )

        )