from dataclasses import dataclass, field


@dataclass
class TrainingPolicy:
    """
    Define las reglas que debe cumplir la información
    utilizada durante un entrenamiento.
    """

    tema: str

    fuentes_permitidas: list[str] = field(default_factory=list)
    fuentes_bloqueadas: list[str] = field(default_factory=list)

    exigir_autor: bool = True
    exigir_fecha: bool = False
    exigir_referencias: bool = False

    permitir_contenido_no_verificado: bool = False

    def mostrar(self):
        print("\n" + "=" * 50)
        print("NORMATIVA DEL ENTRENAMIENTO")
        print("=" * 50)

        print(f"Tema: {self.tema}")

        print("\nFuentes permitidas:")
        for fuente in self.fuentes_permitidas:
            print(f"  ✅ {fuente}")

        print("\nFuentes bloqueadas:")
        for fuente in self.fuentes_bloqueadas:
            print(f"  ❌ {fuente}")

        print(f"\nExigir autor: {self.exigir_autor}")
        print(f"Exigir fecha: {self.exigir_fecha}")
        print(f"Exigir referencias: {self.exigir_referencias}")

        print(
            "Permitir contenido no verificado: "
            f"{self.permitir_contenido_no_verificado}"
        )