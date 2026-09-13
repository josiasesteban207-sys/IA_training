import sqlite3
from pathlib import Path


class Database:

    def __init__(self, db_path="data/ai_trainer.db"):

        self.db_path = db_path

        Path(db_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.crear_tablas()

    def conectar(self):

        return sqlite3.connect(
            self.db_path
        )

    def crear_tablas(self):

        with self.conectar() as conexion:

            cursor = conexion.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fuentes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    autor TEXT,
                    fecha TEXT,
                    tema TEXT NOT NULL,
                    puntuacion INTEGER,
                    nivel TEXT,
                    estado TEXT NOT NULL,
                    fecha_registro
                    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conexion.commit()

    def guardar_fuente(
        self,
        titulo,
        url,
        autor,
        fecha,
        tema,
        puntuacion,
        nivel,
        estado
    ):

        with self.conectar() as conexion:

            cursor = conexion.cursor()

            try:

                cursor.execute("""
                    INSERT INTO fuentes (
                        titulo,
                        url,
                        autor,
                        fecha,
                        tema,
                        puntuacion,
                        nivel,
                        estado
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    titulo,
                    url,
                    autor,
                    fecha,
                    tema,
                    puntuacion,
                    nivel,
                    estado
                ))

                conexion.commit()

                return True

            except sqlite3.IntegrityError:

                print(
                    "⚠️ La fuente ya existe."
                )

                return False

    def obtener_fuentes(
        self,
        tema=None
    ):

        with self.conectar() as conexion:

            cursor = conexion.cursor()

            if tema:

                cursor.execute("""
                    SELECT *
                    FROM fuentes
                    WHERE tema = ?
                """, (tema,))

            else:

                cursor.execute("""
                    SELECT *
                    FROM fuentes
                """)

            return cursor.fetchall()