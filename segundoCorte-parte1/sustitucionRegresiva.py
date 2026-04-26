import numpy as np
import re


def parsear_sistema(ecuaciones):
    """
    Parsea un sistema de ecuaciones desde una lista de strings.
    
    Detecta automáticamente las variables y construye la matriz de coeficientes
    y el vector de términos independientes.
    
    Ejemplo:
    --------
    ecuaciones = [
        "X1 - X2 + X3 - X4 = -8",
        "2*X2 - X3 + X4 = 6",
        "-X3 - X4 = -4",
        "2*X4 = 4"
    ]
    R, C, variables = parsear_sistema(ecuaciones)
    
    Parámetros:
    -----------
    ecuaciones : list
        Lista de strings, cada uno representando una ecuación lineal
        Formatos válidos: "X1 + 2*X2 = 5", "-X1 + X2 = 3", etc.
    
    Retorna:
    --------
    R : ndarray
        Matriz de coeficientes de dimensión (m × n)
    C : ndarray
        Vector de términos independientes de dimensión (m,)
    variables : list
        Lista de variables encontradas ordenadas (X1, X2, ...)
    
    Raises:
    -------
    ValueError
        Si la ecuación está mal formada o no se pueden evaluar los coeficientes
    """
    
    # Encontrar todas las variables únicas
    variables = set()
    for ec in ecuaciones:
        # Buscar patrones como X1, X2, etc.
        matches = re.findall(r'X\d+', ec)
        variables.update(matches)
    
    variables = sorted(list(variables), key=lambda x: int(x[1:]))
    n = len(variables)
    m = len(ecuaciones)
    
    print(f"Variables encontradas: {variables}")
    print(f"Número de ecuaciones: {m}\n")
    
    # Crear mapeo de variables a índices
    var_to_idx = {var: i for i, var in enumerate(variables)}
    
    # Construir matriz R y vector C
    R = np.zeros((m, n))
    C = np.zeros(m)
    
    for i, ecuacion in enumerate(ecuaciones):
        # Separar lado izquierdo y derecho del =
        partes = ecuacion.split('=')
        if len(partes) != 2:
            raise ValueError(f"Ecuación mal formada: {ecuacion}")
        
        lado_izq = partes[0].strip()
        lado_der = partes[1].strip()
        
        # Procesar lado derecho (término independiente)
        try:
            C[i] = float(eval(lado_der))
        except:
            raise ValueError(f"No se puede evaluar el lado derecho: {lado_der}")
        
        # Procesar lado izquierdo (coeficientes)
        # Agregar un + al inicio si no empieza con + o -
        if lado_izq[0] not in ['+', '-']:
            lado_izq = '+' + lado_izq
        
        # Encontrar todos los términos
        terminos = re.findall(r'[+-][^+-]+', lado_izq)
        
        for termino in terminos:
            termino = termino.strip()
            
            # Buscar variable en el término
            match_var = re.search(r'X\d+', termino)
            if match_var:
                variable = match_var.group()
                idx_var = var_to_idx[variable]
                
                # Extraer coeficiente (todo lo que viene antes de la variable)
                coef_str = termino[:match_var.start()].strip()
                
                if coef_str == '+' or coef_str == '':
                    coef = 1.0
                elif coef_str == '-':
                    coef = -1.0
                else:
                    try:
                        # Limpiar caracteres y evaluar
                        coef_str_clean = coef_str.replace('*', '').strip()
                        coef = float(eval(coef_str_clean))
                    except:
                        raise ValueError(f"No se puede evaluar el coeficiente: {coef_str}")
                
                R[i, idx_var] = coef
    
    return R, C, variables


def sustitucion_regresiva(R, C):
    """
    Algoritmo de sustitución regresiva para resolver sistemas triangulares superiores.
    
    Resuelve el sistema R * x = C donde R es una matriz triangular superior.
    El algoritmo comienza desde la última ecuación y va hacia atrás.
    
    Parámetros:
    -----------
    R : array_like
        Matriz triangular superior de dimensión (n × n)
    C : array_like
        Vector de términos independientes de dimensión (n,)
    
    Retorna:
    --------
    x : ndarray
        Vector solución de dimensión (n,)
    
    Raises:
    -------
    ValueError
        Si hay división por cero (elemento diagonal es 0)
    
    Complejidad: O(n²)
    """
    
    # Convertir a arrays de numpy si es necesario
    R = np.array(R, dtype=float)
    C = np.array(C, dtype=float)
    
    n = len(C)
    x = np.zeros(n)
    
    # Sustitución regresiva: comenzar desde la última ecuación
    for i in range(n - 1, -1, -1):
        # Calcular suma de términos posteriores: Σ R[i,j] * x[j] para j > i
        suma = 0
        for j in range(i + 1, n):
            suma += R[i, j] * x[j]
        
        # Calcular x[i]
        if R[i, i] == 0:
            raise ValueError(f"División por cero en la fila {i}. La matriz no es triangular superior válida.")
        
        x[i] = (C[i] - suma) / R[i, i]
    
    return x


def mostrar_matriz_sistema(R, C, variables):
    """
    Muestra la matriz aumentada del sistema de forma legible.
    
    Parámetros:
    -----------
    R : ndarray
        Matriz de coeficientes
    C : ndarray
        Vector de términos independientes
    variables : list
        Lista de nombres de variables
    """
    print("Matriz aumentada [R | C]:")
    print()
    for i in range(len(C)):
        fila = ""
        for j in range(len(variables)):
            coef = R[i, j]
            if coef != 0:
                if j == 0:
                    fila += f"{coef:6.1f}*{variables[j]}  "
                else:
                    signo = "+" if coef > 0 else "-"
                    fila += f" {signo} {abs(coef):6.1f}*{variables[j]}  "
        fila += f" = {C[i]:6.1f}"
        print(fila)
    print()


def verificar_solucion(R, C, x, variables):
    """
    Verifica que la solución obtenida sea correcta.
    
    Parámetros:
    -----------
    R : ndarray
        Matriz de coeficientes
    C : ndarray
        Vector de términos independientes
    x : ndarray
        Vector solución
    variables : list
        Lista de nombres de variables
    
    Retorna:
    --------
    bool
        True si la solución es correcta
    """
    print("Verificación (R × x = C):")
    print()
    resultado = R @ x
    es_correcto = True
    
    for i, (original, calculado) in enumerate(zip(C, resultado)):
        estado = "✓" if abs(original - calculado) < 1e-10 else "✗"
        print(f"   Ecuación {i+1}: {original:8.1f} = {calculado:8.1f}  {estado}")
        if abs(original - calculado) > 1e-10:
            es_correcto = False
    
    print()
    print(f"   Sistema resuelto correctamente: {es_correcto}")
    return es_correcto


def mostrar_solucion(variables, x):
    """
    Muestra la solución de forma clara y organizada.
    
    Parámetros:
    -----------
    variables : list
        Lista de nombres de variables
    x : ndarray
        Vector solución
    """
    print("SOLUCIÓN:")
    print("="*70)
    for var, valor in zip(variables, x):
        print(f"   {var} = {valor:.6g}")
    print("="*70)
    print()