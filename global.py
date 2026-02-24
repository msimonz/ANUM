import math

from biseccion import biseccion
from puntofijo import punto_fijo
from posicionfalsa import posicion_falsa
from newtonRaphson import newton_raphson
from secante import secante


def construir_funcion(descripcion: str):
    """
    Construye una función f(x) a partir de una cadena, por ejemplo:
    'x**3 - x - 2' o 'math.sin(x) - x/2'.
    """
    descripcion = descripcion.strip()

    def f(x: float) -> float:
        return eval(
            descripcion,
            {"__builtins__": {}, "math": math},
            {"x": x},
        )

    return f


def imprimir_resultado(nombre: str, raiz, info: dict):
    print("#*#*#*#*# ", nombre, " #*#*#*#*#*#", sep="")
    print("Status: ", info.get("status"))
    print("Raíz aproximada: ", raiz)
    print(info.get("reason"))
    print("Iteraciones: ", info.get("iterations"))
    if "error_rel" in info:
        print("Error relativo: ", info["error_rel"])
    if "error_abs" in info:
        print("Error absoluto: ", info["error_abs"])
    print()


def main():
    print("=== MÉTODOS DE BÚSQUEDA DE RAÍCES ===")
    print("1) Bisección")
    print("2) Punto fijo")
    print("3) Posición falsa")
    print("4) Newton-Raphson")
    print("5) Secante")

    opcion = input("Seleccione un método (1-5): ").strip()

    if opcion == "1":
        print("\n--- Bisección ---")
        expr = input("Ingrese f(x): ")
        f = construir_funcion(expr)
        a = float(input("Extremo inferior a: "))
        b = float(input("Extremo superior b: "))
        tol = float(input("Tolerancia: "))
        max_iter = int(input("Máximo de iteraciones: "))

        raiz, info = biseccion(f, a=a, b=b, tol=tol, max_iter=max_iter)
        imprimir_resultado("BISECCIÓN", raiz, info)

    elif opcion == "2":
        print("\n--- Punto fijo ---")
        print("Se construirá automáticamente g(x) = x - λ·f(x) a partir de f(x).")
        expr = input("Ingrese f(x): ")
        f = construir_funcion(expr)
        x0 = float(input("Valor inicial x0: "))

        # Estimación numérica de f'(x0)
        h = 1e-4
        fp_x0 = (f(x0 + h) - f(x0 - h)) / (2 * h)

        if fp_x0 == 0 or not math.isfinite(fp_x0):
            lam = 0.1
        else:
            lam = 0.9 / fp_x0 if abs(fp_x0) > 1 else 0.9 * (1 / fp_x0)

        def g(x, f=f, lam=lam):
            return x - lam * f(x)

        tol = float(input("Tolerancia: "))
        max_iter = int(input("Máximo de iteraciones: "))

        raiz, info = punto_fijo(g, x0=x0, tol=tol, max_iter=max_iter)
        imprimir_resultado("PUNTO FIJO", raiz, info)

    elif opcion == "3":
        print("\n--- Posición falsa ---")
        expr = input("Ingrese f(x): ")
        f = construir_funcion(expr)
        a = float(input("Extremo inferior a: "))
        b = float(input("Extremo superior b: "))
        tol = float(input("Tolerancia: "))
        max_iter = int(input("Máximo de iteraciones: "))

        raiz, info = posicion_falsa(f, a=a, b=b, tol=tol, max_iter=max_iter)
        imprimir_resultado("POSICIÓN FALSA", raiz, info)

    elif opcion == "4":
        print("\n--- Newton-Raphson ---")
        expr = input("Ingrese f(x): ")
        f = construir_funcion(expr)

        # Derivada numérica para no pedir f'(x) por consola
        def fp(x: float, h: float = 1e-6) -> float:
            return (f(x + h) - f(x - h)) / (2 * h)

        x0 = float(input("Valor inicial x0: "))
        tol = float(input("Tolerancia: "))
        max_iter = int(input("Máximo de iteraciones: "))

        raiz, info = newton_raphson(f, fp, x0=x0, tol=tol, max_iter=max_iter)
        imprimir_resultado("NEWTON-RAPHSON", raiz, info)

    elif opcion == "5":
        print("\n--- Secante ---")
        expr = input("Ingrese f(x): ")
        f = construir_funcion(expr)
        x0 = float(input("Valor inicial x0: "))
        x1 = float(input("Segundo valor inicial x1: "))
        tol = float(input("Tolerancia: "))
        max_iter = int(input("Máximo de iteraciones: "))

        raiz, info = secante(f, x0=x0, x1=x1, tol=tol, max_iter=max_iter)
        imprimir_resultado("SECANTE", raiz, info)

    else:
        print("Opción no válida.")


if __name__ == "__main__":
    main()