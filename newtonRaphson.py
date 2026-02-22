import math
from typing import Callable, Tuple, Dict, Any


def newton_raphson(
    f: Callable[[float], float],
    fp: Callable[[float], float],
    x0: float,
    tol: float,
    max_iter: int,
) -> Tuple[float | None, Dict[str, Any]]:
    """
    Algoritmo de Newton-Raphson: aproxima una raíz de f(x)=0.
    Iteración: Xn = Xn-1 - f(Xn-1) / f'(Xn-1).
    Criterios de parada:
      - Éxito: e_n = |Xn - Xn-1| < tol (se obtuvo una aproximación de p).
      - Fracaso: después de M iteraciones no se logró la precisión deseada.
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
        }
    fpx0 = fp(x0)
    if not math.isfinite(fpx0) or abs(fpx0) < 1e-20:
        return None, {
            "status": "fail",
            "reason": "f'(x0) no es finito o es ≈ 0; no se puede iterar (división por cero).",
            "iterations": 0,
            "x0": x0,
        }

    # -------- Iteración Newton-Raphson: Xn = Xn-1 - f(Xn-1) / f'(Xn-1) --------
    x_prev = x0

    for n in range(1, max_iter + 1):
        f_prev = f(x_prev)
        fp_prev = fp(x_prev)

        if not math.isfinite(f_prev) or not math.isfinite(fp_prev):
            return None, {
                "status": "fail",
                "reason": "f(x_n) o f'(x_n) no es finito (NaN/inf). Posible divergencia.",
                "iterations": n,
                "last_x": x_prev,
            }
        if abs(fp_prev) < 1e-20:
            return None, {
                "status": "fail",
                "reason": "f'(x_n) ≈ 0; no se puede continuar (división por cero).",
                "iterations": n,
                "last_x": x_prev,
            }

        x_next = x_prev - f_prev / fp_prev

        if not math.isfinite(x_next):
            return None, {
                "status": "fail",
                "reason": "X_n no es finito (NaN/inf). Posible divergencia.",
                "iterations": n,
                "last_x": x_prev,
            }

        # Error absoluto: e_n = |Xn - Xn-1| (criterio del algoritmo en la pizarra)
        en = abs(x_next - x_prev)

        # Éxito: si e_n < E entonces Salida (Éxito) PARE
        if en < tol:
            return x_next, {
                "status": "ok",
                "reason": "Se obtuvo una aproximación de p (tolerancia alcanzada).",
                "iterations": n,
                "x0": x0,
                "error_abs": en,
            }

        # Fracaso: si n = M entonces Salida (Fracaso) PARE
        if n == max_iter:
            return None, {
                "status": "fail",
                "reason": "Después de M iteraciones no se logró la precisión deseada.",
                "iterations": max_iter,
                "last_x": x_next,
                "error_abs": en,
            }

        x_prev = x_next

    return None, {
        "status": "fail",
        "reason": "Después de M iteraciones no se logró la precisión deseada.",
        "iterations": max_iter,
        "last_x": x_prev,
    }
