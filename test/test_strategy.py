from core.strategy_selector import (
    StrategySelector
)


def main():

    selector = StrategySelector()

    casos = [

        (
            "Texto",
            "Responder preguntas sobre psicología"
        ),

        (
            "Imagen",
            "Detectar enfermedades en plantas"
        ),

        (
            "Datos",
            "Predecir producción agrícola"
        ),

        (
            "Imagen",
            "Clasificar fotografías de plantas"
        )

    ]

    for tipo, objetivo in casos:

        estrategia = selector.seleccionar(

            tipo_ia=tipo,

            objetivo=objetivo

        )

        print("\n" + "=" * 50)

        print(
            f"Tipo: {tipo}"
        )

        print(
            f"Objetivo: {objetivo}"
        )

        print(
            f"\n🧠 Estrategia: "
            f"{estrategia.nombre}"
        )

        print(
            f"📊 Datos: "
            f"{estrategia.tipo_datos}"
        )

        print(
            f"⚙️ Método: "
            f"{estrategia.metodo}"
        )

        print(
            f"🔧 Framework: "
            f"{estrategia.framework}"
        )

        print(
            f"📝 {estrategia.descripcion}"
        )


if __name__ == "__main__":

    main()