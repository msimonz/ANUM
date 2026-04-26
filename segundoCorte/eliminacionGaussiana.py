"""
Eliminación gaussiana con sustitución hacia atrás.

Sigue el pseudocódigo del curso: eliminación hacia adelante con pivoteo por
fila (menor índice p ≥ i con elemento no nulo en la columna i), luego
sustitución regresiva sobre la matriz aumentada.
"""

import numpy as np

# Tolerancia para considerar un pivote numéricamente nulo
TOL = 1e-12

MSG_FRACASO = (
    "El sistema tiene infinitas soluciones o no tiene solución"
)


def matriz_aumentada(A, b):
    """Construye la matriz aumentada [A | b] de tamaño n × (n+1)."""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1, 1)
    return np.hstack([A, b])


def eliminacion_gaussiana(A, b):
    """
    Resuelve Ax = b por eliminación gaussiana y sustitución hacia atrás.

    Parámetros
    ----------
    A : array_like
        Matriz de coeficientes (n × n).
    b : array_like
        Términos independientes (n,).

    Retorna
    -------
    exito : bool
        True si se obtuvo una solución única.
    x : ndarray o None
        Vector solución de dimensión (n,) si exito; si no, None.
    mensaje : str o None
        Mensaje de fracaso si no exito; None si hubo éxito.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).ravel()

    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A debe ser una matriz cuadrada.")
    n = A.shape[0]
    if b.shape[0] != n:
        raise ValueError("Las dimensiones de A y b no coinciden.")

    # Copia de trabajo: matriz aumentada (n filas, n+1 columnas)
    Ab = matriz_aumentada(A, b).copy()

    # --- Fase 1: eliminación hacia adelante (pasos 1–6) ---
    for i in range(n - 1):
        # Paso 2: menor p >= i tal que a_p,i != 0
        p = None
        for row in range(i, n):
            if abs(Ab[row, i]) > TOL:
                p = row
                break
        if p is None:
            return False, None, MSG_FRACASO

        # Paso 3: intercambio de filas
        if p != i:
            Ab[[i, p], :] = Ab[[p, i], :]

        # Pasos 4–6: eliminar debajo del pivote
        piv = Ab[i, i]
        for j in range(i + 1, n):
            m_ji = Ab[j, i] / piv
            Ab[j, :] = Ab[j, :] - m_ji * Ab[i, :]

    # --- Fase 2: sustitución hacia atrás (pasos 7–10) ---
    # Paso 7
    if abs(Ab[n - 1, n - 1]) <= TOL:
        return False, None, MSG_FRACASO

    x = np.zeros(n)
    # Paso 8
    x[n - 1] = Ab[n - 1, n] / Ab[n - 1, n - 1]
    # Paso 9
    for i in range(n - 2, -1, -1):
        s = 0.0
        for j in range(i + 1, n):
            s += Ab[i, j] * x[j]
        if abs(Ab[i, i]) <= TOL:
            return False, None, MSG_FRACASO
        x[i] = (Ab[i, n] - s) / Ab[i, i]

    return True, x, None


def mostrar_matriz_aumentada(Ab):
    """Muestra la matriz aumentada [A | b]."""
    n = Ab.shape[0]
    print("Matriz aumentada [ A | b ]:")
    print()
    for i in range(n):
        coefs = "  ".join(f"{Ab[i, j]:8.4f}" for j in range(n))
        print(f"   [{coefs} | {Ab[i, n]:8.4f}]")
    print()


def eliminacion_gaussiana_solo_matriz(A):
    """
    Triangulariza una matriz cuadrada A con eliminación gaussiana.

    Retorna:
    -------
    exito : bool
    U : ndarray o None
    mensaje : str o None
    """
    U = np.array(A, dtype=float).copy()
    if U.ndim != 2 or U.shape[0] != U.shape[1]:
        raise ValueError("A debe ser una matriz cuadrada.")

    n = U.shape[0]
    for i in range(n - 1):
        p = None
        for row in range(i, n):
            if abs(U[row, i]) > TOL:
                p = row
                break

        if p is None:
            return False, None, MSG_FRACASO

        if p != i:
            U[[i, p], :] = U[[p, i], :]

        piv = U[i, i]
        for j in range(i + 1, n):
            m_ji = U[j, i] / piv
            U[j, :] = U[j, :] - m_ji * U[i, :]

    return True, U, None


def mostrar_matriz(matriz, nombre):
    """Muestra una matriz con formato uniforme."""
    print(f"{nombre}:")
    print()
    for fila in matriz:
        print("  " + "  ".join(f"{val:8.4f}" for val in fila))
    print()
