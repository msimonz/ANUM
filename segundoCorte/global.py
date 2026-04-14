"""
Punto de entrada interactivo
"""

import re

from sustitucionRegresiva import (
    parsear_sistema as parsear_sistema_sr,
    sustitucion_regresiva,
    mostrar_matriz_sistema,
    mostrar_solucion as mostrar_solucion_sr,
    verificar_solucion as verificar_solucion_sr,
)
from factorizacionLR import (
    parsear_sistema,
    resolver_sistema_lr,
    mostrar_solucion,
    verificar_solucion,
)
from eliminacionGaussiana import (
    eliminacion_gaussiana,
    matriz_aumentada,
    mostrar_matriz_aumentada,
)
from gaussSeidel import gauss_seidel


def imprimir_ayuda_opcion_1():
    """Sustitución regresiva."""
    print("Ingresa: cantidad de ecuaciones y cada ecuación en una línea.")
    print("De eso se arma R (coeficientes) y C (términos independientes).")
    print("Sistema cuadrado y R triangular superior.")
    print()


def imprimir_ayuda_opcion_2():
    """Eliminación gaussiana."""
    print("Ingresa: cantidad de ecuaciones y cada ecuación en una línea.")
    print("De eso se arma A y b; el método usa la matriz aumentada [A | b]. Sistema cuadrado.")
    print()


def imprimir_ayuda_opcion_3():
    """Factorización LR."""
    print("Ingresa: cantidad de ecuaciones y cada ecuación en una línea (sistema Ax = b).")
    print("L, R y P los calcula el programa. Sistema cuadrado.")
    print()


def imprimir_ayuda_opcion_4_antes_ecuaciones():
    """Gauss-Seidel: antes de las ecuaciones."""
    print("Ingresa primero el sistema (mismas reglas: una ecuación por línea).")
    print("Luego: X0 (valor inicial por cada variable), epsilon (tolerancia) y N_max (tope de iteraciones).")
    print()


def imprimir_ayuda_opcion_4_parametros_iteracion(variables):
    """Gauss-Seidel: antes de X0, epsilon, N_max."""
    print(f"X0: un número por variable en orden {variables}. epsilon y N_max: números.")
    print()


def _linea_parece_ecuacion(linea: str) -> bool:
    """Comprueba mínimo razonable: '=' y al menos una variable X1, X2, ..."""
    if "=" not in linea:
        return False
    return bool(re.search(r"X\d+", linea))


def leer_numero_ecuaciones() -> int:
    """Pide un entero >= 1 hasta que la entrada sea válida."""
    while True:
        raw = input("Número de ecuaciones: ").strip()
        if not raw:
            print("Ingresa un número entero (no dejes la línea vacía).")
            continue
        try:
            m = int(raw)
        except ValueError:
            print("Eso no es un número entero válido. Ejemplo: 2")
            continue
        if m < 1:
            print("El número debe ser al menos 1.")
            continue
        return m


def leer_ecuaciones():
    """Solicita el número de ecuaciones y cada una como texto, con reintentos."""
    m = leer_numero_ecuaciones()
    ecuaciones = []
    for i in range(m):
        while True:
            linea = input(f"Ecuación {i + 1}: ").strip()
            if not linea:
                print("No ingresaste nada. Escribe la ecuación en una sola línea.")
                continue
            if not _linea_parece_ecuacion(linea):
                print(
                    "La línea no parece una ecuación válida: debe incluir '=' "
                    "y variables X1, X2, ... (ej. X1 + 2*X2 = 5)."
                )
                continue
            ecuaciones.append(linea)
            break
    return ecuaciones


def leer_float(prompt: str) -> float:
    """Lee un número real; reintenta si está vacío o no es numérico."""
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
    """Lee un entero >= 1."""
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


def es_sistema_cuadrado(A):
    """True si la matriz de coeficientes es n×n."""
    return A.ndim == 2 and A.shape[0] == A.shape[1]


def main():
    print("=== MÉTODOS PARA SISTEMAS LINEALES ===")
    print("1) Sustitución regresiva (matriz triangular superior)")
    print("2) Eliminación gaussiana con sustitución hacia atrás")
    print("3) Factorización LR (con pivoteo parcial)")
    print("4) Gauss-Seidel (iterativo)")

    opcion = input("Seleccione un método (1-4): ").strip()

    try:
        if opcion == "1":
            print("\n--- Sustitución regresiva ---")
            imprimir_ayuda_opcion_1()
            ecuaciones = leer_ecuaciones()
            R, C, variables = parsear_sistema_sr(ecuaciones)
            print()
            if not es_sistema_cuadrado(R):
                print(
                    "Error: el sistema debe ser cuadrado (mismo número de ecuaciones "
                    "que de incógnitas)."
                )
                return
            mostrar_matriz_sistema(R, C, variables)
            print("Resolviendo mediante sustitución regresiva...")
            print()
            solucion = sustitucion_regresiva(R, C)
            mostrar_solucion_sr(variables, solucion)
            verificar_solucion_sr(R, C, solucion, variables)

        elif opcion == "2":
            print("\n--- Eliminación gaussiana ---")
            imprimir_ayuda_opcion_2()
            ecuaciones = leer_ecuaciones()
            A, b, variables = parsear_sistema(ecuaciones)
            print()
            if not es_sistema_cuadrado(A):
                print(
                    "Error: el sistema debe ser cuadrado (n ecuaciones, n incógnitas)."
                )
                return
            Ab = matriz_aumentada(A, b)
            mostrar_matriz_aumentada(Ab)
            print("Resolviendo por eliminación gaussiana...")
            print()
            exito, x, mensaje = eliminacion_gaussiana(A, b)
            if exito:
                print("Estado: ÉXITO\n")
                mostrar_solucion(variables, x)
                verificar_solucion(A, b, x)
            else:
                print("Estado: FRACASO")
                print(mensaje)

        elif opcion == "3":
            print("\n--- Factorización LR ---")
            imprimir_ayuda_opcion_3()
            ecuaciones = leer_ecuaciones()
            A, b, variables = parsear_sistema(ecuaciones)
            print()
            if not es_sistema_cuadrado(A):
                print(
                    "Error: el sistema debe ser cuadrado (n ecuaciones, n incógnitas)."
                )
                return
            x, L, R_lr, P, b_perm = resolver_sistema_lr(A, b)
            print("Matriz L (triangular inferior):")
            for fila in L:
                print("  " + "  ".join(f"{val:8.4f}" for val in fila))
            print()
            print("Matriz R (triangular superior):")
            for fila in R_lr:
                print("  " + "  ".join(f"{val:8.4f}" for val in fila))
            print()
            print("Vector de permutación P:", P)
            print()
            mostrar_solucion(variables, x)
            verificar_solucion(A, b, x)

        elif opcion == "4":
            print("\n--- Gauss-Seidel ---")
            imprimir_ayuda_opcion_4_antes_ecuaciones()
            ecuaciones = leer_ecuaciones()
            A, b, variables = parsear_sistema(ecuaciones)
            print()
            if not es_sistema_cuadrado(A):
                print(
                    "Error: el sistema debe ser cuadrado (n ecuaciones, n incógnitas)."
                )
                return
            imprimir_ayuda_opcion_4_parametros_iteracion(variables)
            print(f"Vector inicial X0 (una componente por variable, orden {variables}):")
            X0 = []
            for v in variables:
                X0.append(leer_float(f"  {v}: "))
            epsilon = leer_float("Tolerancia (epsilon): ")
            N_max = leer_int_positivo("Máximo de iteraciones: ")
            print()
            x, iteraciones, _historial, _errores, convergio = gauss_seidel(
                A, b, X0, epsilon, N_max
            )
            if convergio:
                print(f"Convergió en {iteraciones} iteraciones.")
            else:
                print(f"No convergió en {N_max} iteraciones (última aproximación mostrada).")
            print()
            mostrar_solucion(variables, x)
            verificar_solucion(A, b, x)

        else:
            print("Opción no válida.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
