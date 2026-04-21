"""
Punto de entrada interactivo para operar sobre una matriz A cargada desde .txt.
"""

import numpy as np

from io_sistema import leer_matriz_cuadrada_desde_txt
from sustitucionRegresiva import sustitucion_regresiva
from factorizacionLR import gauss_lr_pivoteo
from eliminacionGaussiana import eliminacion_gaussiana_solo_matriz, mostrar_matriz
from gaussSeidel import gauss_seidel_homogeneo, mostrar_historial, mostrar_errores


def leer_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Ingresa un número (no dejes la línea vacía).")
            continue
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print("Eso no es un número válido.")


def leer_int_positivo(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Ingresa un número entero (no dejes la línea vacía).")
            continue
        try:
            n = int(raw)
        except ValueError:
            print("Eso no es un número entero válido.")
            continue
        if n < 1:
            print("El valor debe ser al menos 1.")
            continue
        return n


def leer_matriz_desde_archivo():
    ruta = input("Ruta del archivo .txt con la matriz cuadrada A: ").strip()
    A = leer_matriz_cuadrada_desde_txt(ruta)
    print("\nMatriz A cargada correctamente:")
    mostrar_matriz(A, "A")
    return A


def leer_matriz_desde_consola():
    n = leer_int_positivo("Orden de la matriz cuadrada A (n): ")
    filas = []
    print(f"Ingresa {n} filas, cada una con {n} valores separados por espacios.")
    for i in range(n):
        while True:
            raw = input(f"Fila {i + 1}: ").strip()
            if not raw:
                print("La fila no puede estar vacía.")
                continue
            partes = raw.split()
            if len(partes) != n:
                print(f"Debes ingresar exactamente {n} valores.")
                continue
            try:
                fila = [float(x.replace(",", ".")) for x in partes]
            except ValueError:
                print("La fila contiene valores no numéricos. Intenta de nuevo.")
                continue
            filas.append(fila)
            break

    A = np.array(filas, dtype=float)
    print("\nMatriz A cargada correctamente:")
    mostrar_matriz(A, "A")
    return A


def leer_matriz():
    print("\n¿Cómo deseas ingresar la matriz A?")
    print("1) Desde archivo .txt")
    print("2) Por consola")
    opcion = input("Seleccione una opción (1-2): ").strip()

    if opcion == "1":
        return leer_matriz_desde_archivo()
    if opcion == "2":
        return leer_matriz_desde_consola()
    raise ValueError("Opción de ingreso de matriz no válida.")


def imprimir_matriz(nombre, M):
    print(f"{nombre}:")
    for fila in M:
        print("  " + "  ".join(f"{v:8.4f}" for v in fila))
    print()


def opcion_1_sustitucion_regresiva(A):
    print("\n--- Sustitución regresiva sobre A ---")
    print("Se ejecuta directamente sobre A con C=0 (modo transformación).")
    print("Nota: si A no es triangular superior, el resultado puede no ser interpretable.\n")
    C = np.zeros(A.shape[0])
    x = sustitucion_regresiva(A, C)
    print("Resultado del vector x para A*x=0:")
    print("  " + "  ".join(f"{val:8.4f}" for val in x))
    print()


def opcion_2_eliminacion_gaussiana(A):
    print("\n--- Eliminación gaussiana (triangularización de A) ---")
    exito, U, mensaje = eliminacion_gaussiana_solo_matriz(A)
    if not exito:
        print("Estado: FRACASO")
        print(mensaje)
        return
    print("Estado: ÉXITO\n")
    mostrar_matriz(U, "Matriz triangular superior U")


def opcion_3_factorizacion_lr(A):
    print("\n--- Factorización LR ---")
    print("Descomponiendo A con pivoteo parcial...\n")
    b_dummy = np.zeros(A.shape[0])
    L, R, P, _b_perm = gauss_lr_pivoteo(A, b_dummy)
    imprimir_matriz("Matriz L (triangular inferior)", L)
    imprimir_matriz("Matriz R (triangular superior)", R)
    print("Vector de permutación P:", P)
    PA = A[P, :]
    error_factorizacion = np.linalg.norm(PA - (L @ R))
    print(f"Verificación ||P*A - L*R||: {error_factorizacion:.2e}")
    if np.isclose(error_factorizacion, 0.0, atol=1e-8):
        print("Estado verificación: OK (factorización consistente)")
    else:
        print("Estado verificación: ADVERTENCIA (revisar factorización)")
    print()


def opcion_4_gauss_seidel(A):
    print("\n--- Gauss-Seidel (sistema homogéneo A*x=0) ---")
    variables = [f"X{i + 1}" for i in range(A.shape[0])]
    print(f"Vector inicial X0 (una componente por variable, orden {variables}):")
    X0 = [leer_float(f"  {v}: ") for v in variables]
    epsilon = leer_float("Tolerancia (epsilon): ")
    N_max = leer_int_positivo("Máximo de iteraciones: ")
    print()
    x, iteraciones, historial, errores, convergio = gauss_seidel_homogeneo(
        A, X0, epsilon, N_max
    )
    if convergio:
        print(f"Convergió en {iteraciones} iteraciones.")
    else:
        print(f"No convergió en {N_max} iteraciones.")
    print("\nÚltima aproximación:")
    print("  " + "  ".join(f"{val:8.6f}" for val in x))
    mostrar_historial(historial)
    mostrar_errores(errores)


def main():
    print("=== MÉTODOS PARA MATRICES CUADRADAS ===")
    print("1) Sustitución regresiva (modo transformación)")
    print("2) Eliminación gaussiana (triangularización)")
    print("3) Factorización LR (con pivoteo parcial)")
    print("4) Gauss-Seidel para sistema homogéneo A*x=0")

    opcion = input("Seleccione un método (1-4): ").strip()

    try:
        A = leer_matriz()

        if opcion == "1":
            opcion_1_sustitucion_regresiva(A)
        elif opcion == "2":
            opcion_2_eliminacion_gaussiana(A)
        elif opcion == "3":
            opcion_3_factorizacion_lr(A)
        elif opcion == "4":
            opcion_4_gauss_seidel(A)
        else:
            print("Opción no válida.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
