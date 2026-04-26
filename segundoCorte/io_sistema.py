import os
import numpy as np


def leer_matriz_cuadrada_desde_txt(ruta_archivo):
    """
    Lee una matriz cuadrada desde un archivo .txt.

    Formato esperado:
    - Una fila por línea
    - Valores separados por espacios o tabs
    - Se permiten líneas vacías y comentarios iniciados por '#'
    """
    if not ruta_archivo:
        raise ValueError("Debes indicar la ruta del archivo .txt.")

    if not os.path.exists(ruta_archivo):
        raise ValueError(f"No existe el archivo: {ruta_archivo}")

    if not os.path.isfile(ruta_archivo):
        raise ValueError(f"La ruta no corresponde a un archivo: {ruta_archivo}")

    filas = []
    with open(ruta_archivo, "r", encoding="utf-8") as f:
        for numero_linea, linea in enumerate(f, start=1):
            contenido = linea.strip()
            if not contenido or contenido.startswith("#"):
                continue

            partes = contenido.split()
            try:
                fila = [float(x.replace(",", ".")) for x in partes]
            except ValueError:
                raise ValueError(
                    f"La línea {numero_linea} contiene un valor no numérico: {contenido}"
                )
            filas.append(fila)

    if not filas:
        raise ValueError("El archivo no contiene datos de matriz.")

    n_columnas = len(filas[0])
    for i, fila in enumerate(filas, start=1):
        if len(fila) != n_columnas:
            raise ValueError(
                f"Formato inválido: la fila {i} tiene {len(fila)} columnas y "
                f"se esperaban {n_columnas}."
            )

    n_filas = len(filas)
    if n_filas != n_columnas:
        raise ValueError(
            f"La matriz debe ser cuadrada. Se recibió {n_filas}x{n_columnas}."
        )

    return np.array(filas, dtype=float)

