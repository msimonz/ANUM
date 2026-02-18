import math
from typing import Callable, Tuple, Dict, Any


def posicion_falsa(
    f: Callable[[float], float],
    a: float,
    b: float,
    tol: float,
    max_iter: int
) -> Tuple[float | None, Dict[str, Any]]:
    """
    Algoritmo de Posición Falsa (Regula Falsi): aproxima una raíz de f(x)=0 en [a,b].
    Fórmula: Xn = (a*f(b) - b*f(a)) / (f(b) - f(a)).
    Criterios de parada: f(Xn)=0, error relativo e_n = |Xn - Xn-1|/|Xn| < tol, o máximo M iteraciones.
    """
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
            "fa": fa, "fb": fb,
        }
    if fb == 0.0:
        return b, {
            "status": "ok",
            "reason": "f(b)=0",
            "iterations": 0,
            "a": a, "b": b,
            "fa": fa, "fb": fb,
        }

    if fa * fb > 0:
        return None, {
            "status": "fail",
            "reason": "No hay cambio de signo: f(a)*f(b) > 0. Posición falsa requiere raíz en [a,b].",
            "iterations": 0,
            "a": a, "b": b,
            "fa": fa, "fb": fb,
        }

    # -------- Iteración posición falsa --------
    # Xn = (an*f(bn) - bn*f(an)) / (f(bn) - f(an))
    an, bn = a, b
    fan, fbn = fa, fb
    x_prev = None
    error_rel = None

    for n in range(1, max_iter + 1):
        denom = fbn - fan
        if abs(denom) < 1e-20:
            return None, {
                "status": "fail",
                "reason": "Denominador f(b)-f(a) ≈ 0; no se puede calcular Xn.",
                "iterations": n,
                "last_a": an, "last_b": bn,
            }
        xn = (an * fbn - bn * fan) / denom
        fxn = f(xn)

        if not math.isfinite(fxn):
            return None, {
                "status": "fail",
                "reason": "f(Xn) no es finito (NaN/inf). Posible discontinuidad.",
                "iterations": n,
                "last_a": an, "last_b": bn,
                "last_xn": xn,
            }

        if fxn == 0.0:
            return xn, {
                "status": "ok",
                "reason": "f(Xn)=0, raíz exacta",
                "iterations": n,
                "a": an, "b": bn,
                "xn": xn, "fxn": fxn,
            }

        # Error relativo: e_n = |Xn - Xn-1| / |Xn| (desde n>=2)
        if x_prev is not None:
            if abs(xn) >= 1e-15:
                error_rel = abs(xn - x_prev) / abs(xn)
            else:
                error_rel = abs(xn - x_prev)
            if error_rel < tol:
                return xn, {
                    "status": "ok",
                    "reason": "Se obtuvo una aproximación de p (tolerancia alcanzada).",
                    "iterations": n,
                    "a": an, "b": bn,
                    "xn": xn, "fxn": fxn,
                    "error_rel": error_rel,
                }

        # Actualizar intervalo: si f(Xn)*f(an) < 0 entonces bn+1 = Xn, an+1 = an; si no an+1 = Xn, bn+1 = bn
        if fxn * fan < 0:
            bn = xn
            fbn = fxn
        else:
            an = xn
            fan = fxn

        x_prev = xn

    # Fracaso: después de M iteraciones no se logró la precisión deseada
    return None, {
        "status": "fail",
        "reason": "Después de M iteraciones no se logró la precisión deseada.",
        "iterations": max_iter,
        "last_a": an, "last_b": bn,
        "last_xn": x_prev,
        "error_rel": error_rel,
    }
