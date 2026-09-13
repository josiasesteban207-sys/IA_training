from dataclasses import dataclass

from pathlib import Path

from collections import Counter

import hashlib


@dataclass
class DatasetProfile:

    ruta: str

    tipo: str

    total_archivos: int

    archivos_validos: int

    archivos_corruptos: int

    duplicados: int

    clases: dict

    extensiones: dict

    tamano_bytes: int

    tipo_dispositivo: str

    fabricante: str

    modelo_equipo: str

    tiene_bateria: bool

    bateria_porcentaje: float | None

    conectado_corriente: bool | None


class DatasetProfiler:

    EXTENSIONES_IMAGEN = {

        ".jpg",

        ".jpeg",

        ".png",

        ".bmp",

        ".webp"

    }

    def analizar(

        self,

        ruta

    ):

        ruta = Path(ruta)
        from core.device_type_detector import (
        DeviceTypeDetector
        )
        device_detector = DeviceTypeDetector()

        device_info = device_detector.detectar()
        if not ruta.exists():

            raise FileNotFoundError(

                f"Dataset no encontrado: "
                f"{ruta}"

            )

        archivos = [

            archivo

            for archivo in ruta.rglob("*")

            if archivo.is_file()

        ]

        extensiones = Counter()

        clases = Counter()

        hashes = set()

        duplicados = 0

        archivos_validos = 0

        archivos_corruptos = 0

        tamano_total = 0

        for archivo in archivos:

            extension = (

                archivo.suffix.lower()

            )

            extensiones[

                extension

            ] += 1

            try:

                tamano_total += (

                    archivo.stat().st_size

                )

                contenido = (

                    archivo.read_bytes()

                )

                hash_archivo = (

                    hashlib.sha256(

                        contenido

                    ).hexdigest()

                )

                if hash_archivo in hashes:

                    duplicados += 1

                else:

                    hashes.add(

                        hash_archivo

                    )

                archivos_validos += 1

                # =================================
                # DETECTAR CLASE
                # =================================

                if (

                    extension

                    in self.EXTENSIONES_IMAGEN

                ):

                    clase = (

                        archivo.parent.name

                    )

                    clases[

                        clase

                    ] += 1

            except Exception:

                archivos_corruptos += 1

        if (

            any(

                extension

                in self.EXTENSIONES_IMAGEN

                for extension

                in extensiones

            )

        ):

            tipo = "image"

        elif ".csv" in extensiones:

            tipo = "tabular"

        elif (

            ".json"

            in extensiones

        ):

            tipo = "json"

        else:

            tipo = "unknown"

        return DatasetProfile(

            ruta=str(ruta),

            tipo=tipo,

            total_archivos=len(

                archivos

            ),

            archivos_validos=(

                archivos_validos

            ),

            archivos_corruptos=(

                archivos_corruptos

            ),

            duplicados=(

                duplicados

            ),

            clases=dict(

                clases

            ),

            extensiones=dict(

                extensiones

            ),

            tamano_bytes=(

                tamano_total

            ),
            tipo_dispositivo=device_info.tipo,

            fabricante=device_info.fabricante,

            modelo_equipo=device_info.modelo,

            tiene_bateria=device_info.tiene_bateria,

            bateria_porcentaje=(
                device_info.bateria_porcentaje),

            conectado_corriente=(
                device_info.conectado_corriente
            )

        )