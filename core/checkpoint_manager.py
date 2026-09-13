from dataclasses import dataclass

from pathlib import Path


@dataclass
class Checkpoint:

    epoch: int

    ruta: str

    metricas: dict[str, float]

    es_mejor: bool = False


class CheckpointManager:

    def __init__(

        self,

        directorio="models/checkpoints"

    ):

        self.directorio = Path(

            directorio

        )

        self.directorio.mkdir(

            parents=True,

            exist_ok=True

        )

        self.checkpoints = {}

        self.mejor_checkpoint = None

    # ==========================================
    # REGISTRAR CHECKPOINT
    # ==========================================

    def registrar(

        self,

        job_id,

        epoch,

        metricas,

        ruta

    ):

        checkpoint = Checkpoint(

            epoch=epoch,

            ruta=ruta,

            metricas=metricas

        )

        if job_id not in self.checkpoints:

            self.checkpoints[

                job_id

            ] = []

        self.checkpoints[

            job_id

        ].append(

            checkpoint

        )

        return checkpoint

    # ==========================================
    # ESTABLECER MEJOR CHECKPOINT
    # ==========================================

    def establecer_mejor(

        self,

        job_id,

        epoch

    ):

        checkpoints = self.checkpoints.get(

            job_id,

            []

        )

        for checkpoint in checkpoints:

            checkpoint.es_mejor = (

                checkpoint.epoch == epoch

            )

            if checkpoint.es_mejor:

                self.mejor_checkpoint = (

                    checkpoint

                )

        return self.mejor_checkpoint

    # ==========================================
    # OBTENER CHECKPOINTS
    # ==========================================

    def obtener(

        self,

        job_id

    ):

        return self.checkpoints.get(

            job_id,

            []

        )

    # ==========================================
    # OBTENER MEJOR
    # ==========================================

    def obtener_mejor(

        self,

        job_id

    ):

        checkpoints = self.obtener(

            job_id

        )

        for checkpoint in checkpoints:

            if checkpoint.es_mejor:

                return checkpoint

        return None