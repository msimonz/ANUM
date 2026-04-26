def suma_inferior(f, a, b, n):
    """
    Calcula la suma inferior en [a, b] con n subintervalos.
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo.")

    dx = (b - a) / n
    s = 0.0

    for i in range(1, n + 1):
        x_i = a + i * dx
        x_prev = a + (i - 1) * dx
        fx = min(f(x_prev), f(x_i))
        s += fx * dx

    return s


def suma_superior(f, a, b, n):
    """
    Calcula la suma superior en [a, b] con n subintervalos.
    """
    if n < 1:
        raise ValueError("n debe ser un entero positivo.")

    dx = (b - a) / n
    s = 0.0

    for i in range(1, n + 1):
        x_i = a + i * dx
        x_prev = a + (i - 1) * dx
        fx = max(f(x_prev), f(x_i))
        s += fx * dx

    return s
