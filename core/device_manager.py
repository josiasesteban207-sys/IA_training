from dataclasses import dataclass
from enum import Enum
import platform
import uuid


class DeviceStatus(Enum):

    LOCAL = "local"

    DISPONIBLE = "disponible"

    AUTORIZADO = "autorizado"

    ENTRENANDO = "entrenando"

    DESCONECTADO = "desconectado"


@dataclass
class DeviceInfo:

    id: str

    nombre: str

    tipo: str

    sistema_operativo: str

    fabricante: str

    modelo_equipo: str

    cpu: str

    ram_gb: float

    gpu: str | None

    vram_gb: float

    cuda: bool

    tiene_bateria: bool

    bateria_porcentaje: float | None

    conectado_corriente: bool | None

    estado: DeviceStatus = (
        DeviceStatus.DISPONIBLE
    )

    autorizado: bool = False


class DeviceManager:

    def __init__(self):

        self.devices = {}

    # =====================================
    # REGISTRAR DISPOSITIVO
    # =====================================

    def registrar(

        self,

        device

    ):

        self.devices[device.id] = device

        return device

    # =====================================
    # OBTENER DISPOSITIVO
    # =====================================

    def obtener(

        self,

        device_id

    ):

        return self.devices.get(device_id)

    # =====================================
    # LISTAR DISPOSITIVOS
    # =====================================

    def listar(self):

        return list(
            self.devices.values()
        )

    # =====================================
    # REGISTRAR DISPOSITIVO LOCAL
    # =====================================

    def registrar_local(

        self,

        hardware

    ):

        device_id = (

            f"local-"
            f"{uuid.getnode()}"

        )

        device = DeviceInfo(

            id=device_id,

            nombre=(
                hardware.nombre_equipo
            ),

            tipo=(
                hardware.tipo_dispositivo
            ),

            sistema_operativo=(
                hardware.sistema_operativo
            ),

            fabricante=(
                hardware.fabricante
            ),

            modelo_equipo=(
                hardware.modelo_equipo
            ),

            cpu=(
                hardware.cpu
            ),

            ram_gb=(
                hardware.ram_total_gb
            ),

            # CORREGIDO
            gpu=(
                hardware.gpu_nombre
            ),

            vram_gb=(
                hardware.gpu_vram_gb
            ),

            cuda=(
                hardware.cuda_disponible
            ),

            tiene_bateria=(
                hardware.tiene_bateria
            ),

            bateria_porcentaje=(
                hardware.bateria_porcentaje
            ),

            conectado_corriente=(
                hardware.conectado_corriente
            ),

            estado=(
                DeviceStatus.LOCAL
            ),

            autorizado=True

        )

        return self.registrar(device)

    # =====================================
    # AUTORIZAR
    # =====================================

    def autorizar(

        self,

        device_id

    ):

        device = self.obtener(device_id)

        if device is None:

            raise ValueError(
                "Dispositivo no encontrado."
            )

        if device.estado == (
            DeviceStatus.LOCAL
        ):

            return device

        device.autorizado = True

        device.estado = (
            DeviceStatus.AUTORIZADO
        )

        return device

    # =====================================
    # REVOCAR AUTORIZACIÓN
    # =====================================

    def revocar(

        self,

        device_id

    ):

        device = self.obtener(device_id)

        if device is None:

            raise ValueError(
                "Dispositivo no encontrado."
            )

        if device.estado == (
            DeviceStatus.LOCAL
        ):

            raise PermissionError(
                "El dispositivo local "
                "no puede ser revocado."
            )

        if device.estado == (
            DeviceStatus.ENTRENANDO
        ):

            raise RuntimeError(
                "No se puede revocar un "
                "dispositivo que está entrenando."
            )

        device.autorizado = False

        device.estado = (
            DeviceStatus.DISPONIBLE
        )

        return device

    # =====================================
    # DISPOSITIVOS AUTORIZADOS
    # =====================================

    def obtener_autorizados(self):

        return [

            device

            for device in self.devices.values()

            if device.autorizado

        ]

    # =====================================
    # INICIAR ENTRENAMIENTO
    # =====================================

    def iniciar_entrenamiento(

        self,

        device_id

    ):

        device = self.obtener(device_id)

        if device is None:

            raise ValueError(
                "Dispositivo no encontrado."
            )

        if not device.autorizado:

            raise PermissionError(
                "El dispositivo no está "
                "autorizado para entrenamiento."
            )

        if device.estado == (
            DeviceStatus.ENTRENANDO
        ):

            raise RuntimeError(
                "El dispositivo ya está "
                "ejecutando un entrenamiento."
            )

        # =================================
        # PROTECCIÓN DE BATERÍA
        # =================================

        if device.tiene_bateria:

            if (

                device.bateria_porcentaje
                is not None

                and

                device.bateria_porcentaje < 20

                and

                device.conectado_corriente
                is not True

            ):

                raise RuntimeError(
                    "El dispositivo tiene "
                    "batería insuficiente para "
                    "iniciar entrenamiento."
                )

        device.estado = (
            DeviceStatus.ENTRENANDO
        )

        return device

    # =====================================
    # FINALIZAR ENTRENAMIENTO
    # =====================================

    def finalizar_entrenamiento(

        self,

        device_id

    ):

        device = self.obtener(device_id)

        if device is None:

            raise ValueError(
                "Dispositivo no encontrado."
            )

        if device.estado != (
            DeviceStatus.ENTRENANDO
        ):

            raise RuntimeError(
                "El dispositivo no está "
                "ejecutando un entrenamiento."
            )

        # El dispositivo local se
        # identifica mediante su ID.
        if device.id.startswith("local-"):

            device.estado = (
                DeviceStatus.LOCAL
            )

        else:

            device.estado = (
                DeviceStatus.AUTORIZADO
            )

        return device

    # =====================================
    # ELIMINAR DISPOSITIVO
    # =====================================

    def eliminar(

        self,

        device_id

    ):

        device = self.obtener(device_id)

        if device is None:

            return False

        if device.estado == (
            DeviceStatus.LOCAL
        ):

            raise PermissionError(
                "El dispositivo local "
                "no puede eliminarse."
            )

        if device.estado == (
            DeviceStatus.ENTRENANDO
        ):

            raise RuntimeError(
                "No se puede eliminar un "
                "dispositivo que está entrenando."
            )

        del self.devices[device_id]

        return True