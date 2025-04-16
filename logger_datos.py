import os
import csv

def guardar_log(tipo, datos, columnas):
    """
    Guarda un log en formato CSV para un módulo específico del sistema.

    Parámetros:
    - tipo: str → Nombre del módulo (registro, diagnostico, recursos, etc.)
    - datos: dict → Diccionario con los datos a guardar
    - columnas: list → Lista con el orden de las columnas
    """

    nombre_archivo = f"log_{tipo}.csv"
    archivo_existe = os.path.isfile(nombre_archivo)

    with open(nombre_archivo, "a", newline="") as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)

        if not archivo_existe:
            writer.writeheader()
        writer.writerow({col: datos.get(col, "") for col in columnas})
