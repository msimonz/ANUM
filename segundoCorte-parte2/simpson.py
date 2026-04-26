def simpson_compuesto(f, a, b, n):
    """
    Aproxima la integral definida de f en [a, b] con la regla compuesta de Simpson.
    Requiere n par.
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo.")
    if n % 2 != 0:
        raise ValueError("Para Simpson compuesto, n debe ser par.")

    h = (b - a) / n
    s0 = f(a) + f(b)
    s1 = 0.0  # índices impares
    s2 = 0.0  # índices pares (sin extremos)

    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            s2 += f(x)
        else:
            s1 += f(x)

    s = (h / 3.0) * (s0 + 4.0 * s1 + 2.0 * s2)
    return s
