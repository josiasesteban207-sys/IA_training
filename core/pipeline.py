from rules.policies import TrainingPolicy


class TrainingPipeline:

    def __init__(
        self,
        tipo_ia: str,
        tema: str,
        objetivo: str
    ):
        self.tipo_ia = tipo_ia
        self.tema = tema
        self.objetivo = objetivo

        self.policy = TrainingPolicy(
            tema=self.tema,

            fuentes_permitidas=[
                "Universidades",
                "Organizaciones oficiales",
                "Artículos científicos"
            ],

            fuentes_bloqueadas=[
                "Contenido sin autor",
                "Fuentes no verificadas"
            ],

            exigir_autor=True,
            exigir_fecha=False,
            exigir_referencias=True,

            permitir_contenido_no_verificado=False
        )

    def iniciar(self):

        print("\n" + "=" * 50)
        print("CONFIGURACIÓN DEL ENTRENAMIENTO")
        print("=" * 50)

        print(f"Tipo de IA: {self.tipo_ia}")
        print(f"Tema: {self.tema}")
        print(f"Objetivo: {self.objetivo}")

        self.policy.mostrar()

        print("\n[1/5] Analizando solicitud...")
        print("[2/5] Preparando búsqueda de información...")
        print("[3/5] Verificando fuentes...")
        print("[4/5] Preparando datos...")
        print("[5/5] Sistema listo para entrenar.")

        print("\nConfiguración creada correctamente.")