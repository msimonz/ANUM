import math
from typing import Callable, Tuple, Dict, Any


def secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tol: float,
    max_iter: int,
) -> Tuple[float | None, Dict[str, Any]]:
    """
    Algoritmo de la Secante: aproxima una raíz de f(x)=0.
    Entrada: f, X0 y X1 (valores iniciales), E=tol (tolerancia), M=max_iter.
    Iteración: Xn+1 = (Xn-1 * f(Xn) - Xn * f(Xn-1)) / (f(Xn) - f(Xn-1)).
    Error: e_n+1 = |Xn+1 - Xn| / |Xn+1|.
    Éxito: si e_n+1 < E entonces se obtuvo una aproximación de P.
    Fracaso: si n = M entonces no se logró la precisión deseada después de M iteraciones.
    """
    # -------- Validaciones básicas de entrada --------
    if tol <= 0:
        raise ValueError("tol debe ser > 0.")
    if max_iter <= 0:
        raise ValueError("max_iter debe ser > 0.")

    if not math.isfinite(f(x0)):
        return None, {
            "status": "fail",
            "reason": "f(x0) no es finito (NaN/inf). Revisa el dominio de f.",
            "iterations": 0,
            "x0": x0,
            "x1": x1,
        }
    if not math.isfinite(f(x1)):
        return None, {
            "status": "fail",
            "reason": "f(x1) no es finito (NaN/inf). Revisa el dominio de f.",
            "iterations": 0,
            "x0": x0,
            "x1": x1,
        }

    # -------- Iteración: para n=1,...,M; Xn+1 = (Xn-1*f(Xn) - Xn*f(Xn-1)) / (f(Xn) - f(Xn-1)) --------
    x_prev = x0  # Xn-1
    x_curr = x1  # Xn

    for n in range(1, max_iter + 1):
        f_prev = f(x_prev)
        f_curr = f(x_curr)

        if not math.isfinite(f_prev) or not math.isfinite(f_curr):
            return None, {
                "status": "fail",
                "reason": "f(x_n) o f(x_n-1) no es finito (NaN/inf). Posible divergencia.",
                "iterations": n,
                "last_x": x_curr,
            }

        denom = f_curr - f_prev
        if abs(denom) < 1e-20:
            return None, {
                "status": "fail",
                "reason": "f(Xn) - f(Xn-1) ≈ 0; no se puede continuar (división por cero).",
                "iterations": n,
                "last_x": x_curr,
            }

        # Xn+1 = (Xn-1 * f(Xn) - Xn * f(Xn-1)) / (f(Xn) - f(Xn-1))
        x_next = (x_prev * f_curr - x_curr * f_prev) / denom

        if not math.isfinite(x_next):
            return None, {
                "status": "fail",
                "reason": "X_n+1 no es finito (NaN/inf). Posible divergencia.",
                "iterations": n,
                "last_x": x_curr,
            }

        # Error relativo: e_n+1 = |Xn+1 - Xn| / |Xn+1|
        if abs(x_next) >= 1e-15:
            error_rel = abs(x_next - x_curr) / abs(x_next)
        else:
            error_rel = abs(x_next - x_curr)

        # Éxito: si e_n+1 < E entonces Salida (Éxito), Xn+1 ≈ P, PARE
        if error_rel < tol:
            return x_next, {
                "status": "ok",
                "reason": "Se obtuvo una aproximación de P (tolerancia alcanzada).",
                "iterations": n,
                "x0": x0,
                "x1": x1,
                "error_rel": error_rel,
            }

        # Fracaso: si n = M entonces Salida (Fracaso), PARE
        if n == max_iter:
            return None, {
                "status": "fail",
                "reason": "No se logró la precisión deseada después de M iteraciones.",
                "iterations": max_iter,
                "last_x": x_next,
                "error_rel": error_rel,
            }

        x_prev = x_curr
        x_curr = x_next

    return None, {
        "status": "fail",
        "reason": "No se logró la precisión deseada después de M iteraciones.",
        "iterations": max_iter,
        "last_x": x_curr,
    }
