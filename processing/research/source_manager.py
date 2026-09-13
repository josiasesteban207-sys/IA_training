from database.db import Database


class KnowledgeManager:

    def __init__(self):

        self.db = Database()

    def registrar_fuente(
        self,
        source,
        resultado_validacion,
        tema
    ):

        if resultado_validacion.aprobada:

            estado = "APROBADA"

        else:

            estado = "RECHAZADA"

        guardada = self.db.guardar_fuente(

            titulo=source.titulo,

            url=source.url,

            autor=source.autor,

            fecha=source.fecha,

            tema=tema,

            puntuacion=(
                resultado_validacion.puntuacion
            ),

            nivel=(
                resultado_validacion.nivel
            ),

            estado=estado

        )

        if guardada:

            print(
                f"✅ Fuente registrada: "
                f"{source.titulo}"
            )

        return guardada

    def mostrar_fuentes(
        self,
        tema=None
    ):

        fuentes = self.db.obtener_fuentes(
            tema
        )

        print(
            "\n===== BASE DE CONOCIMIENTO ====="
        )

        if not fuentes:

            print(
                "No hay fuentes registradas."
            )

            return

        for fuente in fuentes:

            print(
                f"\nID: {fuente[0]}"
            )

            print(
                f"Título: {fuente[1]}"
            )

            print(
                f"URL: {fuente[2]}"
            )

            print(
                f"Tema: {fuente[5]}"
            )

            print(
                f"Puntuación: {fuente[6]}"
            )

            print(
                f"Nivel: {fuente[7]}"
            )

            print(
                f"Estado: {fuente[8]}"
            )