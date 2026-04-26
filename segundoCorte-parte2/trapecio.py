def trapecio_compuesto(f, a, b, n):
    """
    Aproxima la integral definida de f en [a, b] con la regla compuesta del trapecio.
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo.")

    h = (b - a) / n
    s0 = f(a) + f(b)
    s1 = 0.0

    for i in range(1, n):
        x = a + i * h
        s1 += f(x)

    s = (h / 2.0) * s0 + h * s1
    return s
