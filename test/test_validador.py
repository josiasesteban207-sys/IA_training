from database.db import Database

from research.source_validator import (
    Source,
    SourceValidator
)

from research.source_manager import (
    KnowledgeManager
)

from rules.policies import TrainingPolicy


def main():

    tema = "psicologia"

    policy = TrainingPolicy(

        tema=tema,

        exigir_autor=True,

        exigir_referencias=True

    )

    validator = SourceValidator(
        policy
    )

    fuente = Source(

        titulo=(
            "Investigación científica "
            "sobre psicología"
        ),

        url=(
            "https://example.edu/"
            "psicologia"
        ),

        autor="Dr. Juan Pérez",

        fecha="2026",

        tiene_referencias=True

    )

    resultado = validator.validar(
        fuente
    )

    print(
        f"\nPuntuación: "
        f"{resultado.puntuacion}"
    )

    manager = KnowledgeManager()

    manager.registrar_fuente(

        source=fuente,

        resultado_validacion=resultado,

        tema=tema

    )

    manager.mostrar_fuentes(
        tema
    )


if __name__ == "__main__":

    main()