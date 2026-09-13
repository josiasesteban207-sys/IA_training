from dataclasses import dataclass, field

from datetime import datetime

from enum import Enum

from typing import Any


class JobStatus(Enum):

    PENDIENTE = "pendiente"

    EJECUTANDO = "ejecutando"

    PAUSADO = "pausado"

    COMPLETADO = "completado"

    ERROR = "error"

    CANCELADO = "cancelado"


@dataclass
class TrainingJob:

    id: int

    tipo: str

    modelo: str

    framework: str

    dataset: str

    configuracion: dict[str, Any]

    estado: JobStatus = (

        JobStatus.PENDIENTE

    )

    progreso: float = 0.0

    epoch_actual: int = 0

    epoch_total: int = 0

    metricas: dict[str, float] = field(

        default_factory=dict

    )

    error: str | None = None

    creado: str = field(

        default_factory=lambda:

        datetime.now().isoformat()

    )


class TrainingJobManager:

    def __init__(self):

        self.jobs = {}

        self.contador = 0

    # =====================================
    # CREAR JOB
    # =====================================

    def crear_job(

        self,

        tipo,

        modelo,

        framework,

        dataset,

        configuracion

    ):

        self.contador += 1

        job = TrainingJob(

            id=self.contador,

            tipo=tipo,

            modelo=modelo,

            framework=framework,

            dataset=dataset,

            configuracion=configuracion,

            epoch_total=(

                configuracion.get(

                    "epochs",

                    1

                )

            )

        )

        self.jobs[job.id] = job

        return job

    # =====================================
    # INICIAR
    # =====================================

    def iniciar(

        self,

        job_id

    ):

        job = self.jobs.get(

            job_id

        )

        if not job:

            raise ValueError(

                "Job no encontrado"

            )

        if job.estado not in [

            JobStatus.PENDIENTE,

            JobStatus.PAUSADO

        ]:

            raise ValueError(

                "El job no puede iniciarse "
                "en su estado actual."

            )

        job.estado = (

            JobStatus.EJECUTANDO

        )

        return job

    # =====================================
    # ACTUALIZAR PROGRESO
    # =====================================

    def actualizar_progreso(

        self,

        job_id,

        epoch,

        metricas=None

    ):

        job = self.jobs.get(

            job_id

        )

        if not job:

            raise ValueError(

                "Job no encontrado"

            )

        job.epoch_actual = epoch

        if job.epoch_total > 0:

            job.progreso = (

                epoch

                /

                job.epoch_total

                * 100

            )

        if metricas:

            job.metricas.update(

                metricas

            )

        return job

    # =====================================
    # COMPLETAR
    # =====================================

    def completar(

        self,

        job_id

    ):

        job = self.jobs.get(

            job_id

        )

        if not job:

            raise ValueError(

                "Job no encontrado"

            )

        job.estado = (

            JobStatus.COMPLETADO

        )

        job.progreso = 100.0

        return job

    # =====================================
    # PAUSAR
    # =====================================

    def pausar(

        self,

        job_id

    ):

        job = self.jobs.get(

            job_id

        )

        if not job:

            raise ValueError(

                "Job no encontrado"

            )

        if job.estado != (

            JobStatus.EJECUTANDO

        ):

            raise ValueError(

                "El job no está ejecutándose."

            )

        job.estado = (

            JobStatus.PAUSADO

        )

        return job

    # =====================================
    # CANCELAR
    # =====================================

    def cancelar(

        self,

        job_id

    ):

        job = self.jobs.get(

            job_id

        )

        if not job:

            raise ValueError(

                "Job no encontrado"

            )

        job.estado = (

            JobStatus.CANCELADO

        )

        return job

    # =====================================
    # ERROR
    # =====================================

    def registrar_error(

        self,

        job_id,

        error

    ):

        job = self.jobs.get(

            job_id

        )

        if not job:

            raise ValueError(

                "Job no encontrado"

            )

        job.estado = (

            JobStatus.ERROR

        )

        job.error = str(

            error

        )

        return job

    # =====================================
    # OBTENER JOB
    # =====================================

    def obtener(

        self,

        job_id

    ):

        return self.jobs.get(

            job_id

        )