
from Bio import SeqIO
from pathlib import Path
import csv

# Obtener la ubicación principal del proyecto
BASE = Path(__file__).resolve().parent.parent

# Carpeta donde se encuentran los FASTA
CARPETA_DATOS = BASE / "datos"

# Archivos que vamos a procesar
archivos = [
    {
        "id_especie": 1,
        "nombre": "Maíz",
        "archivo": "especie1.fasta"
    },
    {
        "id_especie": 2,
        "nombre": "Cacao",
        "archivo": "especie2.fasta"
    }
]

# Archivo CSV de salida
ruta_csv = CARPETA_DATOS / "secuencias.csv"

# Crear el CSV
with open(
    ruta_csv,
    "w",
    newline="",
    encoding="utf-8"
) as archivo_csv:

    escritor = csv.writer(archivo_csv)

    # Encabezados del CSV
    escritor.writerow([
        "id_especie",
        "accession",
        "encabezado",
        "secuencia",
        "longitud"
    ])

    # Procesar cada archivo FASTA
    for especie in archivos:

        ruta_fasta = CARPETA_DATOS / especie["archivo"]

        if not ruta_fasta.exists():
            raise FileNotFoundError(
                f"No se encontró: {ruta_fasta}"
            )

        print("\nProcesando:", especie["nombre"])

        cantidad = 0

        # Leer las secuencias con Biopython
        for registro in SeqIO.parse(
            ruta_fasta,
            "fasta"
        ):

            secuencia = str(registro.seq).upper()

            if not secuencia:
                continue

            # Guardar los datos en el CSV
            escritor.writerow([
                especie["id_especie"],
                registro.id,
                registro.description,
                secuencia,
                len(secuencia)
            ])

            cantidad += 1

            # Mostrar información en pantalla
            print("-------------------------")
            print("Especie:", especie["nombre"])
            print("ID:", registro.id)
            print("Encabezado:", registro.description)
            print("Longitud:", len(secuencia))

        if cantidad == 0:
            raise ValueError(
                f"No se encontraron secuencias en "
                f"{especie['archivo']}"
            )

        print("Registros encontrados:", cantidad)

print("\nProceso terminado correctamente.")
print("CSV generado en:", ruta_csv)
