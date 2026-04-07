print("##############SUSTITUCIÓN REGRESIVA#############")
from sustitucionRegresiva import (
    parsear_sistema, 
    sustitucion_regresiva,
    mostrar_matriz_sistema,
    mostrar_solucion,
    verificar_solucion
)

ecuaciones = ["X1 + X2 = 5", 
              "X2 = 2"]

print("📝 Sistema de ecuaciones:")
for i, ec in enumerate(ecuaciones, 1):
    print(f"   {i}. {ec}")
print()

R, C, variables = parsear_sistema(ecuaciones)
print()

mostrar_matriz_sistema(R, C, variables)

print("🔄 Resolviendo mediante sustitución regresiva...")
print()

solucion = sustitucion_regresiva(R, C)

mostrar_solucion(variables, solucion)

verificar_solucion(R, C, solucion, variables)

print("")

print("################FACTORIZACIÓN LR#####################")
from factorizacionLR import (
    parsear_sistema,
    resolver_sistema_lr,
    mostrar_solucion,
    verificar_solucion
)

# Define tu sistema de ecuaciones aquí
ecuaciones = [
    "X1 + 2*X2 = 5",
    "3*X1 + 4*X2 = 11"
]

print("📝 Sistema de ecuaciones:")
for i, ec in enumerate(ecuaciones, 1):
    print(f"   {i}. {ec}")
print()

# Parsear el sistema
A, b, variables = parsear_sistema(ecuaciones)
print()

# Resolver
x, L, R, P, b_perm = resolver_sistema_lr(A, b)

# Mostrar matrices
print("\n📋 Matriz L (Triangular Inferior):")
for fila in L:
    print("  " + "  ".join([f"{val:8.4f}" for val in fila]))

print("\n📋 Matriz R (Triangular Superior):")
for fila in R:
    print("  " + "  ".join([f"{val:8.4f}" for val in fila]))

print("\n📋 Vector de permutación P:", P)

# Mostrar solución
print()
mostrar_solucion(variables, x)

# Verificar
verificar_solucion(A, b, x)

print("")

print("################GAUSS SEIDEL#####################")
from gaussSeidel import (
    parsear_sistema,
    gauss_seidel,
    mostrar_solucion,
    verificar_solucion
)

ecuaciones = [
    "5*X1 + 2*X2 = 6",
    "X1 + 3*X2 = 5"
]

X0 = [0, 0]
epsilon = 1e-6
N_max = 50

A, b, variables = parsear_sistema(ecuaciones)
x, iteraciones, historial, errores, convergio = gauss_seidel(A, b, X0, epsilon, N_max)

print(f"\n✅ Convergió en {iteraciones} iteraciones" if convergio else f"\n⚠️  No convergió después de {N_max} iteraciones")
mostrar_solucion(variables, x)
verificar_solucion(A, b, x)