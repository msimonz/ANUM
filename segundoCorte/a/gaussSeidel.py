import numpy as np
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
    
    print(f"📊 Variables encontradas: {variables}")
    print(f"📝 Número de ecuaciones: {m}\n")
    
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


def gauss_seidel(A, b, X0, epsilon, N_max):
    """
    Método Iterativo Gauss-Seidel para resolver Ax = b.
    
    En cada iteración k, calcula:
    xi^(k) = (bi - Σ(aij * xj^(k)) - Σ(aij * xj^(k-1))) / aii
             j<i              j>i
    
    Parámetros:
    -----------
    A : ndarray
        Matriz de coeficientes (n × n)
    b : ndarray
        Vector de términos independientes (n,)
    X0 : ndarray
        Vector inicial (aproximación inicial X^(0))
    epsilon : float
        Tolerancia de convergencia (ε)
    N_max : int
        Número máximo de iteraciones (N)
    
    Retorna:
    --------
    x : ndarray
        Vector solución aproximada
    iteraciones : int
        Número de iteraciones realizadas
    historial : list
        Historial de vectores solución en cada iteración
    errores : list
        Historial de errores en cada iteración
    convergio : bool
        True si convergió dentro de N_max iteraciones
    """
    
    n = len(b)
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x = np.array(X0, dtype=float)
    
    historial = [x.copy()]
    errores = []
    convergio = False
    
    print(f"🔄 Iniciando método Gauss-Seidel")
    print(f"   Tolerancia (ε) = {epsilon}")
    print(f"   Máximo de iteraciones (N) = {N_max}\n")
    
    for k in range(1, N_max + 1):
        x_anterior = x.copy()
        
        # Iteración k del método Gauss-Seidel
        for i in range(n):
            suma1 = 0
            suma2 = 0
            
            # Suma de términos con índices j < i (usa valores nuevos de x)
            for j in range(i):
                suma1 += A[i, j] * x[j]
            
            # Suma de términos con índices j > i (usa valores anteriores de x)
            for j in range(i + 1, n):
                suma2 += A[i, j] * x_anterior[j]
            
            # Calcular xi^(k)
            if abs(A[i, i]) < 1e-10:
                raise ValueError(f"❌ División por cero: A[{i},{i}] ≈ 0")
            
            x[i] = (b[i] - suma1 - suma2) / A[i, i]
        
        # Calcular error: ||x^(k) - x^(k-1)||
        error = np.linalg.norm(x - x_anterior)
        errores.append(error)
        historial.append(x.copy())
        
        print(f"   Iteración {k}: error = {error:.2e}")
        
        # Verificar convergencia
        if error < epsilon:
            convergio = True
            print(f"\n✅ ¡Convergió en iteración {k}!")
            break
    
    if not convergio:
        print(f"\n⚠️  No convergió después de {N_max} iteraciones")
        print(f"    Último error: {errores[-1]:.2e}")
    
    return x, k, historial, errores, convergio


def verificar_solucion(A_original, b_original, x):
    """Verifica que la solución sea correcta"""
    print("\n🔍 Verificación (A × x = b):")
    print()
    resultado = A_original @ x
    
    es_correcto = True
    for i, (original, calculado) in enumerate(zip(b_original, resultado)):
        estado = "✓" if abs(original - calculado) < 1e-6 else "✗"
        print(f"   Ecuación {i+1}: {original:10.4f} = {calculado:10.4f}  {estado}")
        if abs(original - calculado) > 1e-6:
            es_correcto = False
    
    print()
    print(f"   ¿Sistema resuelto correctamente? {es_correcto}")
    return es_correcto


def mostrar_solucion(variables, x):
    """Muestra la solución de forma clara"""
    print("✅ SOLUCIÓN:")
    print("="*70)
    for var, valor in zip(variables, x):
        print(f"   {var} = {valor:.6g}")
    print("="*70)
    print()


def mostrar_historial(historial, variables, mostrar_todos=False):
    """Muestra el historial de iteraciones"""
    print("\n📋 Historial de iteraciones:")
    print()
    
    if mostrar_todos or len(historial) <= 10:
        for k, iteracion in enumerate(historial):
            print(f"   X^({k}) = [ {', '.join([f'{v:.4f}' for v in iteracion])} ]")
    else:
        # Mostrar primeras y últimas
        for k in range(3):
            print(f"   X^({k}) = [ {', '.join([f'{v:.4f}' for v in historial[k]])} ]")
        print(f"   ... ({len(historial) - 6} iteraciones omitidas) ...")
        for k in range(len(historial) - 3, len(historial)):
            print(f"   X^({k}) = [ {', '.join([f'{v:.4f}' for v in historial[k]])} ]")
    print()


def mostrar_errores(errores):
    """Muestra el histórico de errores"""
    print("\n📈 Histórico de errores:")
    print()
    for k, error in enumerate(errores, 1):
        print(f"   Iteración {k}: error = {error:.2e}")
    print()