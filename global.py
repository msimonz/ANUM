from biseccion import biseccion
from puntofijo import punto_fijo
from posicionfalsa import posicion_falsa
from newtonRaphson import newton_raphson
from secante import secante


def f(x):
    return x**3 - x - 2  # raíz cerca de 1.521...


# Bisección
raiz, info = biseccion(f, a=1, b=2, tol=1e-6, max_iter=50)
print("#*#*#*#*# BISECCIÓN #*#*#*#*#*#")
print("Status: ", info["status"])
print("Raíz: ", raiz)
print(info["reason"])
print("Iteraciones: ", info["iterations"])
print()

# Punto fijo: f(x)=0 => x^3-x-2=0 => x = (x+2)^(1/3) = g(x)
def g(x):
    return (x + 2) ** (1.0 / 3.0)


raiz_pf, info_pf = punto_fijo(g, x0=1.0, tol=1e-6, max_iter=50)
print("#*#*#*#*# PUNTO FIJO #*#*#*#*#*#")
print("Status: ", info_pf["status"])
print("Raíz (punto fijo): ", raiz_pf)
print(info_pf["reason"])
print("Iteraciones: ", info_pf["iterations"])
if "error_rel" in info_pf:
    print("Error relativo: ", info_pf["error_rel"])
print()

# Posición falsa (misma f e intervalo que bisección)
raiz_pfalsa, info_pfalsa = posicion_falsa(f, a=1, b=2, tol=1e-6, max_iter=50)
print("#*#*#*#*# POSICIÓN FALSA #*#*#*#*#*#")
print("Status: ", info_pfalsa["status"])
print("Raíz: ", raiz_pfalsa)
print(info_pfalsa["reason"])
print("Iteraciones: ", info_pfalsa["iterations"])
if "error_rel" in info_pfalsa:
    print("Error relativo: ", info_pfalsa["error_rel"])
print()


# Newton-Raphson (ejemplo pizarra: f(x)=x³+4x²-10, f'(x)=3x²+8x, Xo=1)
def f_nr(x):
    return x**3 + 4 * x**2 - 10


def fp_nr(x):
    return 3 * x**2 + 8 * x


raiz_nr, info_nr = newton_raphson(f_nr, fp_nr, x0=1.0, tol=1e-6, max_iter=50)
print("#*#*#*#*# NEWTON-RAPHSON #*#*#*#*#*#")
print("Status: ", info_nr["status"])
print("Raíz: ", raiz_nr)
print(info_nr["reason"])
print("Iteraciones: ", info_nr["iterations"])
if "error_abs" in info_nr:
    print("Error absoluto (e_n): ", info_nr["error_abs"])
print()

# Secante (misma f que Newton-Raphson: f(x)=x³+4x²-10; X0=1, X1=2)
raiz_sec, info_sec = secante(f_nr, x0=1.0, x1=2.0, tol=1e-6, max_iter=50)
print("#*#*#*#*# SECANTE #*#*#*#*#*#")
print("Status: ", info_sec["status"])
print("Raíz: ", raiz_sec)
print(info_sec["reason"])
print("Iteraciones: ", info_sec["iterations"])
if "error_rel" in info_sec:
    print("Error relativo (e_n+1): ", info_sec["error_rel"])
