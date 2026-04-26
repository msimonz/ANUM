"""
Punto de entrada interactivo para métodos de integración numérica.
"""

import math

from trapecio import trapecio_compuesto
from simpson import simpson_compuesto
from sumas import suma_inferior, suma_superior


def leer_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Ingresa un número.")
            continue
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print("Eso no es un número válido.")


def leer_int_positivo(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Ingresa un número entero.")
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


def construir_funcion(expr: str):
    expr = expr.strip()
    if not expr:
        raise ValueError("La función no puede estar vacía.")

    entorno = {"__builtins__": {}}
    permitidos = {
        "x": 0.0,
        "abs": abs,
        "pow": pow,
        "pi": math.pi,
        "e": math.e,
    }

    for nombre in dir(math):
        if not nombre.startswith("_"):
            permitidos[nombre] = getattr(math, nombre)

    def f(x):
        permitidos["x"] = x
        try:
            valor = eval(expr, entorno, permitidos)
        except Exception as e:
            raise ValueError(f"No se pudo evaluar f(x) en x={x}: {e}") from e
        try:
            return float(valor)
        except (TypeError, ValueError):
            raise ValueError("La función debe retornar un valor numérico.")

    return f


def leer_datos():
    expresion = input("f(x): ").strip()
    f = construir_funcion(expresion)
    a = leer_float("a: ")
    b = leer_float("b: ")
    n = leer_int_positivo("n: ")
    return f, a, b, n


def opcion_trapecio():
    print("\n--- Regla compuesta del trapecio ---")
    f, a, b, n = leer_datos()
    resultado = trapecio_compuesto(f, a, b, n)
    print(f"T(h) = {resultado:.10f}")


def opcion_simpson():
    print("\n--- Regla compuesta de Simpson ---")
    f, a, b, n = leer_datos()
    resultado = simpson_compuesto(f, a, b, n)
    print(f"S(h) = {resultado:.10f}")


def opcion_sumas():
    print("\n--- Sumas inferior y superior ---")
    f, a, b, n = leer_datos()
    inferior = suma_inferior(f, a, b, n)
    superior = suma_superior(f, a, b, n)
    print(f"L(A) = {inferior:.10f}")
    print(f"U(A) = {superior:.10f}")


def main():
    print("=== MÉTODOS DE INTEGRACIÓN NUMÉRICA ===")
    print("1) Regla compuesta del trapecio")
    print("2) Regla compuesta de Simpson")
    print("3) Sumas inferior y superior")
    opcion = input("Seleccione un método (1-3): ").strip()

    try:
        if opcion == "1":
            opcion_trapecio()
        elif opcion == "2":
            opcion_simpson()
        elif opcion == "3":
            opcion_sumas()
        else:
            print("Opción no válida.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
