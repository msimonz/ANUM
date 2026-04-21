import numpy as np
from copy import deepcopy
import re


def parsear_sistema(ecuaciones):
    """
    Parsea un sistema de ecuaciones desde una lista de strings.
    
    Parámetros:
    -----------
    ecuaciones : list
        Lista de strings, cada uno representando una ecuación lineal
    
    Retorna:
    --------
    A : ndarray
        Matriz de coeficientes de dimensión (n × n)
    b : ndarray
        Vector de términos independientes de dimensión (n,)
    variables : list
        Lista de variables encontradas
    """
    
    # Encontrar todas las variables únicas
    variables = set()
    for ec in ecuaciones:
        matches = re.findall(r'X\d+', ec)
        variables.update(matches)
    
    variables = sorted(list(variables), key=lambda x: int(x[1:]))
    n = len(variables)
    m = len(ecuaciones)
    
    print(f"Variables encontradas: {variables}")
    print(f"Número de ecuaciones: {m}\n")
    
    var_to_idx = {var: i for i, var in enumerate(variables)}
    
    A = np.zeros((m, n))
    b = np.zeros(m)
    
    for i, ecuacion in enumerate(ecuaciones):
        partes = ecuacion.split('=')
        if len(partes) != 2:
            raise ValueError(f"Ecuación mal formada: {ecuacion}")
        
        lado_izq = partes[0].strip()
        lado_der = partes[1].strip()
        
        try:
            b[i] = float(eval(lado_der))
        except:
            raise ValueError(f"No se puede evaluar el lado derecho: {lado_der}")
        
        if lado_izq[0] not in ['+', '-']:
            lado_izq = '+' + lado_izq
        
        terminos = re.findall(r'[+-][^+-]+', lado_izq)
        
        for termino in terminos:
            termino = termino.strip()
            match_var = re.search(r'X\d+', termino)
            if match_var:
                variable = match_var.group()
                idx_var = var_to_idx[variable]
                
                coef_str = termino[:match_var.start()].strip()
                
                if coef_str == '+' or coef_str == '':
                    coef = 1.0
                elif coef_str == '-':
                    coef = -1.0
                else:
                    try:
                        coef_str_clean = coef_str.replace('*', '').strip()
                        coef = float(eval(coef_str_clean))
                    except:
                        raise ValueError(f"No se puede evaluar el coeficiente: {coef_str}")
                
                A[i, idx_var] = coef
    
    return A, b, variables


def gauss_lr_pivoteo(A, b):
    """
    Factorización LR con pivoteo parcial (búsqueda del pivote).
    
    Descompone la matriz A en L*R mediante eliminación gaussiana
    con pivoteo parcial (búsqueda del máximo en la columna).
    
    L = Matriz triangular inferior
    R = Matriz triangular superior
    
    Parámetros:
    -----------
    A : ndarray
        Matriz de coeficientes (n × n)
    b : ndarray
        Vector de términos independientes (n,)
    
    Retorna:
    --------
    L : ndarray
        Matriz triangular inferior
    R : ndarray
        Matriz triangular superior
    P : ndarray
        Vector de permutación
    b_perm : ndarray
        Vector b permutado según P
    
    Raises:
    -------
    ValueError
        Si la matriz es singular (no se puede factorizar)
    """
    
    n = len(A)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    # Inicializar matrices y vector de permutación
    L = np.eye(n)
    R = deepcopy(A)
    P = np.arange(n)  # Vector de permutación
    b_perm = deepcopy(b)
    
    # Eliminación hacia adelante con pivoteo parcial
    for i in range(n):
        # 2.1 PIVOTEO PARCIAL: Buscar el máximo en la columna i
        max_idx = i
        max_val = abs(R[i, i])
        
        for j in range(i + 1, n):
            if abs(R[j, i]) > max_val:
                max_val = abs(R[j, i])
                max_idx = j
        
        # 2.2 CHEQUEO DE SINGULARIDAD
        if abs(R[max_idx, i]) < 1e-10:
            raise ValueError(f"La matriz es singular (elemento pivote = 0 en columna {i})")
        
        # 2.3 INTERCAMBIO DE FILAS si es necesario
        if max_idx != i:
            # Intercambiar filas en R
            R[[i, max_idx]] = R[[max_idx, i]]
            # Intercambiar en L solo las columnas ya construidas [0..i-1].
            # Intercambiar la fila completa rompe la diagonal unitaria y hace
            # inválida la factorización PA = LR.
            if i > 0:
                L[[i, max_idx], :i] = L[[max_idx, i], :i]
            # Intercambiar en b
            b_perm[[i, max_idx]] = b_perm[[max_idx, i]]
            # Actualizar vector de permutación
            P[[i, max_idx]] = P[[max_idx, i]]
            
            print(f"   Intercambio: Fila {i} <-> Fila {max_idx}")
        
        # Eliminación hacia adelante
        for j in range(i + 1, n):
            factor = R[j, i] / R[i, i]
            L[j, i] = factor
            R[j, i:] = R[j, i:] - factor * R[i, i:]
    
    return L, R, P, b_perm


def sustitucion_hacia_adelante(L, y):
    """
    Sustitución hacia adelante: resuelve L*y = b
    
    Parámetros:
    -----------
    L : ndarray
        Matriz triangular inferior (con 1 en la diagonal)
    y : ndarray
        Vector de términos independientes
    
    Retorna:
    --------
    sol : ndarray
        Vector solución
    """
    n = len(y)
    y = np.array(y, dtype=float)
    sol = np.zeros(n)
    
    for i in range(n):
        suma = 0
        for j in range(i):
            suma += L[i, j] * sol[j]
        sol[i] = y[i] - suma
    
    return sol


def sustitucion_hacia_atras(R, z):
    """
    Sustitución hacia atrás: resuelve R*x = z
    
    Parámetros:
    -----------
    R : ndarray
        Matriz triangular superior
    z : ndarray
        Vector de términos independientes
    
    Retorna:
    --------
    x : ndarray
        Vector solución
    """
    n = len(z)
    z = np.array(z, dtype=float)
    x = np.zeros(n)
    
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma += R[i, j] * x[j]
        x[i] = (z[i] - suma) / R[i, i]
    
    return x


def resolver_sistema_lr(A, b):
    """
    Resuelve el sistema Ax = b usando factorización LR con pivoteo parcial.
    
    Proceso:
    1. Factorizar A = LR (con pivoteo)
    2. Resolver Ly = Pb (sustitución hacia adelante)
    3. Resolver Rx = y (sustitución hacia atrás)
    
    Parámetros:
    -----------
    A : ndarray
        Matriz de coeficientes
    b : ndarray
        Vector de términos independientes
    
    Retorna:
    --------
    x : ndarray
        Vector solución
    L : ndarray
        Matriz L de la factorización
    R : ndarray
        Matriz R de la factorización
    P : ndarray
        Vector de permutación
    b_perm : ndarray
        Vector b permutado
    """
    
    print("Iniciando factorización LR con pivoteo parcial...\n")
    
    L, R, P, b_perm = gauss_lr_pivoteo(A, b)
    
    print("\nFactorización completada\n")
    
    # Resolver L*y = b_perm (sustitución hacia adelante)
    y = sustitucion_hacia_adelante(L, b_perm)
    
    # Resolver R*x = y (sustitución hacia atrás)
    x = sustitucion_hacia_atras(R, y)
    
    return x, L, R, P, b_perm


def mostrar_matriz(matriz, nombre):
    """Muestra una matriz de forma legible"""
    print(f"\n{nombre}:")
    for i, fila in enumerate(matriz):
        print("  " + "  ".join([f"{val:8.4f}" for val in fila]))
    print()


def mostrar_solucion(variables, x):
    """Muestra la solución de forma clara"""
    print("SOLUCIÓN:")
    print("="*70)
    for var, valor in zip(variables, x):
        print(f"   {var} = {valor:.6g}")
    print("="*70)
    print()


def verificar_solucion(A_original, b_original, x):
    """Verifica que la solución sea correcta"""
    print("Verificación (A × x = b):")
    print()
    resultado = A_original @ x
    
    es_correcto = True
    for i, (original, calculado) in enumerate(zip(b_original, resultado)):
        estado = "✓" if abs(original - calculado) < 1e-8 else "✗"
        print(f"   Ecuación {i+1}: {original:10.4f} = {calculado:10.4f}  {estado}")
        if abs(original - calculado) > 1e-8:
            es_correcto = False
    
    print()
    print(f"   ¿Sistema resuelto correctamente? {es_correcto}")
    return es_correcto