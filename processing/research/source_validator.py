from dataclasses import dataclass
from urllib.parse import urlparse

from rules.policies import TrainingPolicy


@dataclass
class Source:
    titulo: str
    url: str
    autor: str | None = None
    fecha: str | None = None
    tiene_referencias: bool = False


@dataclass
class ValidationResult:
    aprobada: bool
    puntuacion: int
    nivel: str
    razones: list[str]


class SourceValidator:

    def __init__(self, policy: TrainingPolicy):

        self.policy = policy

    def validar(
        self,
        source: Source
    ) -> ValidationResult:

        puntuacion = 0
        razones = []

        dominio = urlparse(
            source.url
        ).netloc.lower()

        # -------------------------
        # 1. AUTOR
        # -------------------------

        if source.autor:

            puntuacion += 20

            razones.append(
                "La fuente tiene autor identificado."
            )

        elif self.policy.exigir_autor:

            razones.append(
                "La fuente no tiene autor."
            )

        # -------------------------
        # 2. FECHA
        # -------------------------

        if source.fecha:

            puntuacion += 15

            razones.append(
                "La fuente tiene fecha."
            )

        elif self.policy.exigir_fecha:

            razones.append(
                "La fuente no tiene fecha."
            )

        # -------------------------
        # 3. REFERENCIAS
        # -------------------------

        if source.tiene_referencias:

            puntuacion += 25

            razones.append(
                "La fuente contiene referencias."
            )

        elif self.policy.exigir_referencias:

            razones.append(
                "La fuente no contiene referencias."
            )

        # -------------------------
        # 4. DOMINIO CONFIABLE
        # -------------------------

        dominios_confiables = [

            ".edu",
            ".gov",
            ".org",

            "who.int",
            "fao.org",
            "apa.org"
        ]

        dominio_confiable = any(

            dominio.endswith(
                dominio_permitido
            )

            for dominio_permitido
            in dominios_confiables

        )

        if dominio_confiable:

            puntuacion += 30

            razones.append(
                "El dominio pertenece "
                "a una categoría confiable."
            )

        else:

            razones.append(
                "El dominio no está "
                "entre los dominios prioritarios."
            )

        # -------------------------
        # 5. DETERMINAR NIVEL
        # -------------------------

        if puntuacion >= 75:

            nivel = "ALTA"

        elif puntuacion >= 50:

            nivel = "MEDIA"

        else:

            nivel = "BAJA"

        # -------------------------
        # 6. DECISIÓN
        # -------------------------

        aprobada = (

            puntuacion >= 75

            and (

                self.policy.permitir_contenido_no_verificado

                or source.autor is not None

            )

        )

        return ValidationResult(

            aprobada=aprobada,

            puntuacion=puntuacion,

            nivel=nivel,

            razones=razones

        )