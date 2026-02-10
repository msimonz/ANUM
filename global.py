from biseccion import biseccion

def f(x):
    return x**3 - x - 2  # raíz cerca de 1.521...

raiz, info = biseccion(f, a=1, b=2, tol=1e-6, max_iter=50)

print("#*#*#*#*# BISECCIÓN #*#*#*#*#*#")
print("Status: ", info["status"])
print("Raíz: ", raiz)
print( info["reason"])
print("Iteraciones: ", info["iterations"])
