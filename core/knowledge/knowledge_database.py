import sqlite3

from pathlib import Path


class KnowledgeDatabase:

    def __init__(

        self,

        database_path="data/ai_trainer.db"

    ):

        self.database_path = Path(

            database_path

        )

        self.database_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        self.connection = (

            sqlite3.connect(

                self.database_path

            )

        )

        self.crear_tablas()

    # =====================================
    # CREAR TABLAS
    # =====================================

    def crear_tablas(self):

        cursor = (

            self.connection.cursor()

        )

        # FUENTES

        cursor.execute("""

            CREATE TABLE IF NOT EXISTS sources (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                url TEXT UNIQUE NOT NULL,

                titulo TEXT NOT NULL,

                tipo TEXT,

                autoridad REAL,

                confiabilidad REAL,

                fecha TEXT

            )

        """)

        # EVIDENCIAS

        cursor.execute("""

            CREATE TABLE IF NOT EXISTS evidences (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                source_id INTEGER,

                titulo TEXT,

                resumen TEXT,

                relevancia REAL,

                fecha TEXT,

                FOREIGN KEY (

                    source_id

                )

                REFERENCES sources(id)

            )

        """)

        # INVESTIGACIONES

        cursor.execute("""

            CREATE TABLE IF NOT EXISTS research (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                objetivo TEXT NOT NULL,

                tipo_datos TEXT,

                dominio TEXT,

                fecha TEXT,

                estado TEXT

            )

        """)

        # RECOMENDACIONES

        cursor.execute("""

            CREATE TABLE IF NOT EXISTS recommendations (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                research_id INTEGER,

                modelo TEXT,

                framework TEXT,

                confianza REAL,

                motivo TEXT,

                fecha TEXT,

                FOREIGN KEY (

                    research_id

                )

                REFERENCES research(id)

            )

        """)

        self.connection.commit()

    # =====================================
    # AGREGAR FUENTE
    # =====================================

    def agregar_fuente(

        self,

        url,

        titulo,

        tipo,

        autoridad,

        confiabilidad,

        fecha

    ):

        cursor = (

            self.connection.cursor()

        )

        cursor.execute("""

            INSERT OR IGNORE INTO sources (

                url,

                titulo,

                tipo,

                autoridad,

                confiabilidad,

                fecha

            )

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            url,

            titulo,

            tipo,

            autoridad,

            confiabilidad,

            fecha

        ))

        self.connection.commit()

    # =====================================
    # OBTENER FUENTE
    # =====================================

    def obtener_fuente(

        self,

        url

    ):

        cursor = (

            self.connection.cursor()

        )

        cursor.execute("""

            SELECT *

            FROM sources

            WHERE url = ?

        """, (

            url,

        ))

        return cursor.fetchone()

    # =====================================
    # AGREGAR INVESTIGACIÓN
    # =====================================

    def agregar_investigacion(

        self,

        objetivo,

        tipo_datos,

        dominio,

        fecha,

        estado

    ):

        cursor = (

            self.connection.cursor()

        )

        cursor.execute("""

            INSERT INTO research (

                objetivo,

                tipo_datos,

                dominio,

                fecha,

                estado

            )

            VALUES (?, ?, ?, ?, ?)

        """, (

            objetivo,

            tipo_datos,

            dominio,

            fecha,

            estado

        ))

        self.connection.commit()

        return cursor.lastrowid

    # =====================================
    # AGREGAR RECOMENDACIÓN
    # =====================================

    def agregar_recomendacion(

        self,

        research_id,

        modelo,

        framework,

        confianza,

        motivo,

        fecha

    ):

        cursor = (

            self.connection.cursor()

        )

        cursor.execute("""

            INSERT INTO recommendations (

                research_id,

                modelo,

                framework,

                confianza,

                motivo,

                fecha

            )

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            research_id,

            modelo,

            framework,

            confianza,

            motivo,

            fecha

        ))

        self.connection.commit()

    # =====================================
    # CERRAR BASE
    # =====================================

    def cerrar(self):

        self.connection.close()