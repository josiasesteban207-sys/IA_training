from dataclasses import dataclass
from typing import Any


@dataclass
class TrainingAssignment:

    training_id: str

    model_id: str

    device_id: str

    estado: str = "asignado"


class TrainingCoordinator:

    def __init__(

        self,

        device_manager

    ):

        self.device_manager = (
            device_manager
        )

        self.assignments = {}

        self.active_models = {}

    # =====================================
    # ASIGNAR ENTRENAMIENTO
    # =====================================

    def asignar(

        self,

        training_id,

        model_id,

        device_id

    ):

        # -----------------------------
        # COMPROBAR DISPOSITIVO
        # -----------------------------

        device = self.device_manager.obtener(
            device_id
        )

        if device is None:

            raise ValueError(
                "Dispositivo no encontrado."
            )

        # -----------------------------
        # COMPROBAR AUTORIZACIÓN
        # -----------------------------

        if not device.autorizado:

            raise PermissionError(
                "El dispositivo no está "
                "autorizado para entrenar."
            )

        # -----------------------------
        # EVITAR MODELO DUPLICADO
        # -----------------------------

        if model_id in self.active_models:

            raise RuntimeError(

                "El modelo ya está siendo "
                "entrenado por otro dispositivo."

            )

        # -----------------------------
        # EVITAR DISPOSITIVO OCUPADO
        # -----------------------------

        for assignment in self.assignments.values():

            if (

                assignment.device_id
                == device_id

                and

                assignment.estado
                == "ejecutando"

            ):

                raise RuntimeError(

                    "El dispositivo ya está "
                    "ejecutando otro entrenamiento."

                )

        # -----------------------------
        # CREAR ASIGNACIÓN
        # -----------------------------

        assignment = TrainingAssignment(

            training_id=training_id,

            model_id=model_id,

            device_id=device_id

        )

        self.assignments[training_id] = (
            assignment
        )

        self.active_models[model_id] = (
            training_id
        )

        # -----------------------------
        # MARCAR DISPOSITIVO
        # -----------------------------

        self.device_manager.iniciar_entrenamiento(
            device_id
        )

        assignment.estado = "ejecutando"

        return assignment

    # =====================================
    # FINALIZAR
    # =====================================

    def finalizar(

        self,

        training_id

    ):

        assignment = self.assignments.get(
            training_id
        )

        if assignment is None:

            raise ValueError(
                "Entrenamiento no encontrado."
            )

        assignment.estado = "completado"

        self.active_models.pop(
            assignment.model_id,
            None
        )

        self.device_manager.finalizar_entrenamiento(
            assignment.device_id
        )

        return assignment

    # =====================================
    # CANCELAR
    # =====================================

    def cancelar(

        self,

        training_id

    ):

        assignment = self.assignments.get(
            training_id
        )

        if assignment is None:

            raise ValueError(
                "Entrenamiento no encontrado."
            )

        assignment.estado = "cancelado"

        self.active_models.pop(
            assignment.model_id,
            None
        )

        device = self.device_manager.obtener(
            assignment.device_id
        )

        if device is not None:

            self.device_manager.finalizar_entrenamiento(
                assignment.device_id
            )

        return assignment

    # =====================================
    # OBTENER ASIGNACIÓN
    # =====================================

    def obtener(

        self,

        training_id

    ):

        return self.assignments.get(
            training_id
        )

    # =====================================
    # ENTRENAMIENTOS ACTIVOS
    # =====================================

    def obtener_activos(self):

        return [

            assignment

            for assignment
            in self.assignments.values()

            if assignment.estado
            == "ejecutando"

        ]

    # =====================================
    # COMPROBAR MODELO
    # =====================================

    def modelo_entrenando(

        self,

        model_id

    ):

        return model_id in self.active_models