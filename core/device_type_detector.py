from dataclasses import dataclass
import platform


@dataclass
class DeviceTypeInfo:

    tipo: str

    fabricante: str

    modelo: str

    nombre_equipo: str

    tiene_bateria: bool

    bateria_porcentaje: float | None

    conectado_corriente: bool | None

    maquina_virtual: bool


class DeviceTypeDetector:

    def detectar(self):

        fabricante = "Desconocido"

        modelo = "Desconocido"

        nombre_equipo = platform.node()

        tiene_bateria = False

        bateria_porcentaje = None

        conectado_corriente = None

        maquina_virtual = False

        # =====================================
        # DETECTAR WINDOWS
        # =====================================

        if platform.system() == "Windows":

            try:

                import wmi

                conexion = wmi.WMI()

                sistemas = conexion.Win32_ComputerSystem()

                if sistemas:

                    sistema = sistemas[0]

                    fabricante = (
                        sistema.Manufacturer
                        or "Desconocido"
                    )

                    modelo = (
                        sistema.Model
                        or "Desconocido"
                    )

            except ImportError:

                pass

            except Exception:

                pass

        # =====================================
        # DETECTAR BATERÍA
        # =====================================

        try:

            import psutil

            bateria = psutil.sensors_battery()

            if bateria is not None:

                tiene_bateria = True

                bateria_porcentaje = (
                    float(bateria.percent)
                )

                conectado_corriente = (
                    bool(bateria.power_plugged)
                )

        except Exception:

            pass

        # =====================================
        # DETECTAR MÁQUINA VIRTUAL
        # =====================================

        texto_hardware = (

            f"{fabricante} "
            f"{modelo}"

        ).lower()

        indicadores_vm = [

            "virtualbox",

            "vmware",

            "virtual machine",

            "qemu",

            "kvm",

            "hyper-v",

            "microsoft corporation"

        ]

        for indicador in indicadores_vm:

            if indicador in texto_hardware:

                maquina_virtual = True

                break

        # =====================================
        # DETERMINAR TIPO
        # =====================================

        if maquina_virtual:

            tipo = "virtual"

        elif tiene_bateria:

            tipo = "laptop"

        else:

            tipo = "desktop"

        return DeviceTypeInfo(

            tipo=tipo,

            fabricante=fabricante,

            modelo=modelo,

            nombre_equipo=nombre_equipo,

            tiene_bateria=tiene_bateria,

            bateria_porcentaje=(
                bateria_porcentaje
            ),

            conectado_corriente=(
                conectado_corriente
            ),

            maquina_virtual=(
                maquina_virtual
            )

        )