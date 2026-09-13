from dataclasses import dataclass


@dataclass
class DeviceScore:

    device_id: str

    puntuacion: float

    motivo: str


class DeviceSelector:

    def __init__(self, device_manager):

        self.device_manager = device_manager

    # =====================================
    # SELECCIONAR MEJOR DISPOSITIVO
    # =====================================

    def seleccionar(

        self,

        tipo_entrenamiento="ml",

        memoria_requerida_gb=0.0,

        requiere_gpu=False

    ):

        dispositivos = (
            self.device_manager.obtener_autorizados()
        )

        candidatos = []

        for device in dispositivos:

            # ---------------------------------
            # NO USAR DISPOSITIVOS OCUPADOS
            # ---------------------------------

            if device.estado.value == "entrenando":

                continue

            # ---------------------------------
            # COMPROBAR GPU
            # ---------------------------------

            if requiere_gpu and not device.cuda:

                continue

            # ---------------------------------
            # COMPROBAR RAM
            # ---------------------------------

            if (
                memoria_requerida_gb > 0
                and device.ram_gb < memoria_requerida_gb
            ):

                continue

            # ---------------------------------
            # CALCULAR PUNTUACIÓN
            # ---------------------------------

            puntuacion = 0.0

            # RAM

            puntuacion += (
                min(device.ram_gb, 64)
                / 64
                * 30
            )

            # GPU

            if device.cuda:

                puntuacion += 30

            # VRAM

            puntuacion += (
                min(device.vram_gb, 24)
                / 24
                * 25
            )

            # CPU

            if device.ram_gb >= 16:

                puntuacion += 10

            else:

                puntuacion += 5

            # ---------------------------------
            # PREFERENCIA ML / DL
            # ---------------------------------

            if tipo_entrenamiento == "dl":

                if device.cuda:

                    puntuacion += 5

            elif tipo_entrenamiento == "ml":

                if not device.cuda:

                    puntuacion += 5

            candidatos.append(

                DeviceScore(

                    device_id=device.id,

                    puntuacion=round(
                        puntuacion,
                        2
                    ),

                    motivo=(
                        "Dispositivo seleccionado "
                        "por capacidad disponible."
                    )

                )

            )

        # =====================================
        # NINGÚN DISPOSITIVO
        # =====================================

        if not candidatos:

            raise RuntimeError(

                "No existe ningún dispositivo "
                "autorizado y disponible para "
                "este entrenamiento."

            )

        # =====================================
        # MEJOR DISPOSITIVO
        # =====================================

        candidatos.sort(

            key=lambda x: x.puntuacion,

            reverse=True

        )

        return candidatos[0]

    # =====================================
    # MOSTRAR CANDIDATOS
    # =====================================

    def evaluar_dispositivos(

        self,

        tipo_entrenamiento="ml",

        memoria_requerida_gb=0.0,

        requiere_gpu=False

    ):

        dispositivos = (
            self.device_manager.obtener_autorizados()
        )

        resultados = []

        for device in dispositivos:

            if device.estado.value == "entrenando":

                continue

            if requiere_gpu and not device.cuda:

                continue

            if (
                memoria_requerida_gb > 0
                and device.ram_gb < memoria_requerida_gb
            ):

                continue

            puntuacion = 0.0

            puntuacion += (
                min(device.ram_gb, 64)
                / 64
                * 30
            )

            if device.cuda:

                puntuacion += 30

            puntuacion += (
                min(device.vram_gb, 24)
                / 24
                * 25
            )

            if device.ram_gb >= 16:

                puntuacion += 10

            else:

                puntuacion += 5

            if tipo_entrenamiento == "dl":

                if device.cuda:

                    puntuacion += 5

            elif tipo_entrenamiento == "ml":

                if not device.cuda:

                    puntuacion += 5

            resultados.append(

                DeviceScore(

                    device_id=device.id,

                    puntuacion=round(
                        puntuacion,
                        2
                    ),

                    motivo=(
                        "Candidato disponible."
                    )

                )

            )

        resultados.sort(

            key=lambda x: x.puntuacion,

            reverse=True

        )

        return resultados