import math
from typing import Callable, Tuple, Dict, Any

def biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float,
    max_iter: int
) -> Tuple[float | None, Dict[str, Any]]:
    # -------- Validaciones básicas de entrada --------
    if tol <= 0:
        raise ValueError("tol debe ser > 0.")
    if max_iter <= 0:
        raise ValueError("max_iter debe ser > 0.")
    if a >= b:
        raise ValueError("Se requiere a < b.")

    fa = f(a)
    fb = f(b)
    if not (math.isfinite(fa) and math.isfinite(fb)):
        raise ValueError("f(a) o f(b) no es finito (NaN/inf). Revisa el dominio o discontinuidades.")

    if fa == 0.0:
        return a, {
            "status": "ok",
            "reason": "f(a)=0",
            "iterations": 0,
            "a": a, "b": b,
            "fa": fa, "fb": fb
        }
    if fb == 0.0:
        return b, {
            "status": "ok",
            "reason": "f(b)=0",
            "iterations": 0,
            "a": a, "b": b,
            "fa": fa, "fb": fb
        }

    if fa * fb > 0:
        return None, {
            "status": "fail",
            "reason": "No hay cambio de signo: f(a)*f(b) > 0. Bisección no garantiza raíz en [a,b].",
            "iterations": 0,
            "a": a, "b": b,
            "fa": fa, "fb": fb
        }

    # -------- Iteración de bisección --------
    c = None
    fc = None

    for k in range(1, max_iter + 1):
        c = (a + b) / 2.0
        fc = f(c)

        if not math.isfinite(fc):
            return None, {
                "status": "fail",
                "reason": "f(c) no es finito (NaN/inf). Posible discontinuidad dentro del intervalo.",
                "iterations": k,
                "a": a, "b": b, "c": c,
                "fa": f(a), "fb": f(b), "fc": fc
            }

        if (b - a) / 2.0 < tol:
            return c, {
                "status": "Success",
                "reason": "Tolerancia alcanzada por tamaño de intervalo",
                "iterations": k,
                "a": a, "b": b, "c": c,
                "fa": f(a), "fb": f(b), "fc": fc,
                "error_bound": (b - a) / 2.0
            }

        if abs(fc) < tol:
            return c, {
                "status": "ok",
                "reason": "Tolerancia alcanzada por |f(c)|",
                "iterations": k,
                "a": a, "b": b, "c": c,
                "fa": f(a), "fb": f(b), "fc": fc,
                "error_bound": (b - a) / 2.0
            }

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return None, {
        "status": "fail",
        "reason": "Se alcanzó el máximo de iteraciones sin cumplir el criterio de precisión.",
        "iterations": max_iter,
        "last_a": a, "last_b": b,
        "last_c": c,
        "last_fc": fc,
        "error_bound": (b - a) / 2.0 if c is not None else None
    }
