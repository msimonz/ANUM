from biseccion import biseccion
from puntofijo import punto_fijo


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
