import math
from typing import Callable, Tuple, Dict, Any


def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tol: float,
    max_iter: int
) -> Tuple[float | None, Dict[str, Any]]:
    """
    Algoritmo de Punto Fijo: encuentra x tal que x = g(x).
    Iteración: x_{n+1} = g(x_n).
    Criterios de parada: error relativo e_n = |x_n - x_{n-1}|/|x_n| < tol, o máximo de iteraciones.
    """
    # -------- Validaciones básicas de entrada --------
    if tol <= 0:
        raise ValueError("tol debe ser > 0.")
    if max_iter <= 0:
        raise ValueError("max_iter debe ser > 0.")

    x_prev = x0
    if not math.isfinite(g(x0)):
        return None, {
            "status": "fail",
            "reason": "g(x0) no es finito (NaN/inf). Revisa el dominio de g.",
            "iterations": 0,
            "x0": x0,
        }

    for n in range(1, max_iter + 1):
        x_next = g(x_prev)

        if not math.isfinite(x_next):
            return None, {
                "status": "fail",
                "reason": "g(x_n) no es finito (NaN/inf). Posible divergencia.",
                "iterations": n,
                "last_x": x_prev,
            }

        # Error relativo: e_n = |x_n - x_{n-1}| / |x_n| (si x_n != 0)
        if abs(x_next) >= 1e-15:
            error_rel = abs(x_next - x_prev) / abs(x_next)
        else:
            error_rel = abs(x_next - x_prev)

        if error_rel < tol:
            return x_next, {
                "status": "ok",
                "reason": "Tolerancia alcanzada (error relativo)",
                "iterations": n,
                "x0": x0,
                "error_rel": error_rel,
            }

        if n == max_iter:
            return None, {
                "status": "fail",
                "reason": "Se alcanzó el máximo de iteraciones sin cumplir el criterio de precisión.",
                "iterations": max_iter,
                "last_x": x_next,
                "error_rel": error_rel,
            }

        x_prev = x_next

    return None, {
        "status": "fail",
        "reason": "Se alcanzó el máximo de iteraciones.",
        "iterations": max_iter,
        "last_x": x_prev,
    }
