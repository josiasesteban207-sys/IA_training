from core.device_type_detector import (
    DeviceTypeDetector
)


def main():

    detector = DeviceTypeDetector()

    info = detector.detectar()

    print(
        "\n========== TIPO DE DISPOSITIVO =========="
    )

    print(
        f"Tipo: {info.tipo}"
    )

    print(
        f"Fabricante: {info.fabricante}"
    )

    print(
        f"Modelo: {info.modelo}"
    )

    print(
        f"Nombre: {info.nombre_equipo}"
    )

    print(
        f"Tiene batería: "
        f"{info.tiene_bateria}"
    )

    print(
        f"Batería: "
        f"{info.bateria_porcentaje}"
    )

    print(
        f"Conectado a corriente: "
        f"{info.conectado_corriente}"
    )

    print(
        f"Máquina virtual: "
        f"{info.maquina_virtual}"
    )


if __name__ == "__main__":

    main()