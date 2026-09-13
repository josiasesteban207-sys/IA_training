from core.device_manager import (
    DeviceInfo,
    DeviceManager,
    DeviceStatus
)


def main():

    manager = DeviceManager()

    # =====================================
    # DISPOSITIVO LOCAL
    # =====================================

    pc = DeviceInfo(

        id="local",

        nombre="PC Principal",

        sistema_operativo="Windows",

        cpu="Intel",

        ram_gb=31.69,

        gpu=None,

        vram_gb=0.0,

        cuda=False,

        estado=DeviceStatus.LOCAL,

        autorizado=True

    )

    manager.registrar(pc)

    # =====================================
    # OTROS DISPOSITIVOS
    # =====================================

    laptop1 = DeviceInfo(

        id="laptop_01",

        nombre="Laptop 1",

        sistema_operativo="Windows",

        cpu="Intel",

        ram_gb=8.0,

        gpu=None,

        vram_gb=0.0,

        cuda=False

    )

    laptop2 = DeviceInfo(

        id="laptop_02",

        nombre="Laptop 2",

        sistema_operativo="Windows",

        cpu="Intel",

        ram_gb=16.0,

        gpu=None,

        vram_gb=0.0,

        cuda=False

    )

    manager.registrar(laptop1)

    manager.registrar(laptop2)

    # =====================================
    # MOSTRAR
    # =====================================

    print(
        "\n========== DISPOSITIVOS =========="
    )

    for device in manager.listar():

        print(

            f"{device.nombre} | "

            f"{device.estado.value} | "

            f"Autorizado: "

            f"{device.autorizado}"

        )

    # =====================================
    # AUTORIZAR LAPTOP 1
    # =====================================

    manager.autorizar(

        "laptop_01"

    )

    print(
        "\n===== AUTORIZADOS ====="
    )

    for device in (

        manager.obtener_autorizados()

    ):

        print(

            f"- {device.nombre}"

        )

    # =====================================
    # INTENTAR ENTRENAMIENTO
    # =====================================

    manager.iniciar_entrenamiento(

        "laptop_01"

    )

    print(

        "\nLaptop 1 está entrenando."

    )


if __name__ == "__main__":

    main()