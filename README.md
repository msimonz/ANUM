# Algoritmos de Análisis Numérico

Este proyecto implementa algoritmos numéricos para **encontrar raíces** de ecuaciones (valor \(x\) tal que \(f(x)=0\)):

- **Método de bisección**: busca la raíz en un intervalo \([a,b]\) donde \(f\) cambie de signo.
- **Método de punto fijo**: busca \(x\) tal que \(x = g(x)\), iterando \(x_{n+1} = g(x_n)\).
- **Método de posición falsa (regula falsi)**: usa la intersección de la secante con el eje \(x\) para aproximar la raíz en \([a,b]\).
- **Método de Newton-Raphson**: usa la recta tangente a \(f\) en cada aproximación para obtener la siguiente; requiere \(f\) y su derivada \(f'\).

---

## Método de Bisección

### ¿Cómo funciona el método de bisección?

El método se basa en el **Teorema del Valor Intermedio**:

- Si \(f\) es continua en \([a,b]\),
- y \(f(a)\cdot f(b) < 0\) (cambian de signo),
- entonces existe al menos una raíz en ese intervalo.

### Pasos del algoritmo

1. **Escoger un intervalo** \([a,b]\) donde la función cambie de signo.
2. Calcular el punto medio:
   \[
   c = \frac{a+b}{2}
   \]
3. Evaluar \(f(c)\):
   - Si \(f(c)=0\), entonces \(c\) es la raíz.
   - Si \(f(a)\cdot f(c) < 0\), la raíz está en \([a,c]\) → se actualiza \(b=c\).
   - Si \(f(c)\cdot f(b) < 0\), la raíz está en \([c,b]\) → se actualiza \(a=c\).
4. Repetir hasta que el error sea lo suficientemente pequeño.

### Criterios de parada (típicos)

El algoritmo suele detenerse cuando se cumple alguno de estos:

- \(|f(c)| < \varepsilon\)  (la función está “casi” en cero)
- \(\frac{|b-a|}{2} < \varepsilon\) (el intervalo ya es muy pequeño)
- Se alcanza un número máximo de iteraciones

---

## Método de Punto Fijo

### ¿Cómo funciona el método de punto fijo?

Dada una ecuación \(f(x)=0\), se reescribe en la forma **punto fijo** \(x = g(x)\). Un valor \(p\) que cumple \(p = g(p)\) es un **punto fijo** de \(g\) y además es raíz de \(f(x)=0\).

El método consiste en iterar a partir de un valor inicial \(x_0\):

\[
x_{n+1} = g(x_n), \quad n = 0, 1, 2, \ldots
\]

Si la sucesión converge, el límite es un punto fijo de \(g\) (y por tanto una raíz de la ecuación original, según cómo se haya definido \(g\)).

### Pasos del algoritmo

1. **Elegir** una función \(g(x)\) tal que la raíz buscada cumpla \(x = g(x)\) (por ejemplo, despejar \(x\) de \(f(x)=0\)).
2. **Dar** un valor inicial \(x_0\) y una tolerancia \(\varepsilon\), y un máximo de iteraciones \(M\).
3. **Iterar:** \(x_{n+1} = g(x_n)\).
4. **Parar** cuando el error sea menor que la tolerancia o se alcance \(M\).

### Criterios de parada

- **Éxito:** error relativo \(e_n = \frac{|x_n - x_{n-1}|}{|x_n|} < \varepsilon\) (aproximación de la raíz obtenida).
- **Fracaso:** después de \(M\) iteraciones no se alcanza la precisión deseada.

La convergencia depende de que \(|g'(x)|\) sea menor que 1 en una región que contenga al punto fijo (condición de contractividad).

---

## Método de Posición Falsa

### ¿Cómo funciona el método de posición falsa?

Al igual que la bisección, se parte de un intervalo \([a,b]\) con \(f(a)\cdot f(b) < 0\). En lugar de tomar el punto medio, se calcula la intersección de la **secante** que une \((a, f(a))\) y \((b, f(b))\) con el eje \(x\). Ese punto es la nueva aproximación \(x_n\).

### Fórmula recursiva

\[
x_n = \frac{a_n\, f(b_n) - b_n\, f(a_n)}{f(b_n) - f(a_n)}
\]

### Pasos del algoritmo

1. **Entrada:** función \(f\), intervalo \([a,b]\) con \(f(a)\cdot f(b) < 0\), tolerancia \(\varepsilon\) y máximo de iteraciones \(M\).
2. Calcular \(x_n\) con la fórmula anterior.
3. Si \(f(x_n) = 0\), se encontró la raíz exacta → **éxito**.
4. Actualizar el intervalo:
   - Si \(f(x_n)\cdot f(a_n) < 0\), la raíz está en \([a_n, x_n]\) → \(b_{n+1} = x_n\), \(a_{n+1} = a_n\).
   - En caso contrario, la raíz está en \([x_n, b_n]\) → \(a_{n+1} = x_n\), \(b_{n+1} = b_n\).
5. Repetir hasta cumplir un criterio de parada.

### Criterios de parada

- **Éxito:** se obtuvo una aproximación de \(p\) cuando el error relativo \(e_n = \frac{|x_n - x_{n-1}|}{|x_n|} < \varepsilon\), o cuando \(f(x_n) = 0\).
- **Fracaso:** después de \(M\) iteraciones no se logró la precisión deseada.

---

## Método de Newton-Raphson

### ¿Cómo funciona el método de Newton-Raphson?

Se parte de un valor inicial \(x_0\) y se construye la sucesión usando la **recta tangente** a \(f\) en cada punto: la intersección de esa tangente con el eje \(x\) es la siguiente aproximación. Así se obtiene una convergencia muy rápida cuando la raíz es simple y \(x_0\) está suficientemente cerca.

### Fórmula de iteración

\[
x_n = x_{n-1} - \frac{f(x_{n-1})}{f'(x_{n-1})}, \quad n = 1, 2, \ldots, M
\]

### Pasos del algoritmo

1. **Entrada:** función \(f\), derivada \(f'\), valor inicial \(x_0\), tolerancia \(\varepsilon\) y máximo de iteraciones \(M\).
2. **Iterar:** para \(n = 1, 2, \ldots, M\), calcular \(x_n = x_{n-1} - f(x_{n-1}) / f'(x_{n-1})\).
3. **Parar** cuando se cumpla un criterio de parada.

### Criterios de parada

- **Éxito:** se obtuvo una aproximación de la raíz \(p\) cuando el error absoluto \(e_n = |x_n - x_{n-1}| < \varepsilon\).
- **Fracaso:** después de \(M\) iteraciones no se logró la precisión deseada.

El método requiere que \(f'\) no se anule en las aproximaciones (evitar división por cero). La convergencia es típicamente cuadrática cerca de una raíz simple.

---

## ¿Cómo introducir las funciones en `global.py`?

En el archivo **`global.py`** se definen las funciones y se llaman los algoritmos:

- **Bisección:** necesita \(f(x)\) y un intervalo \([a,b]\) con \(f(a)\cdot f(b) < 0\).
- **Punto fijo:** necesita \(g(x)\) tal que la raíz cumpla \(x = g(x)\), y un valor inicial \(x_0\).
- **Posición falsa:** necesita \(f(x)\) y un intervalo \([a,b]\) con \(f(a)\cdot f(b) < 0\) (igual que bisección).
- **Newton-Raphson:** necesita \(f(x)\), su derivada \(f'(x)\) y un valor inicial \(x_0\).

### Ejemplo (misma ecuación con los cuatro métodos)

Para \(f(x) = x^3 - x - 2 = 0\):

- Bisección y posición falsa usan \(f(x)\) en el intervalo \([1, 2]\).
- Punto fijo usa \(g(x) = (x+2)^{1/3}\) (despeje \(x^3 = x + 2\)).

```python
# global.py
from biseccion import biseccion
from puntofijo import punto_fijo
from posicionfalsa import posicion_falsa
from newtonRaphson import newton_raphson

def f(x):
    return x**3 - x - 2

# Bisección
raiz, info = biseccion(f, a=1, b=2, tol=1e-6, max_iter=50)

# Punto fijo: x = (x+2)^(1/3)
def g(x):
    return (x + 2) ** (1.0 / 3.0)
raiz_pf, info_pf = punto_fijo(g, x0=1.0, tol=1e-6, max_iter=50)

# Posición falsa (misma f e intervalo que bisección)
raiz_pfalsa, info_pfalsa = posicion_falsa(f, a=1, b=2, tol=1e-6, max_iter=50)

# Newton-Raphson (necesita f y su derivada f')
def fp(x):
    return 3 * x**2 - 1
raiz_nr, info_nr = newton_raphson(f, fp, x0=1.0, tol=1e-6, max_iter=50)
```

### Ejemplo con trigonometría

Para \(f(x) = \cos(x) - x = 0\), una forma punto fijo es \(x = \cos(x)\), es decir \(g(x) = \cos(x)\):

```python
import math
def f(x):
    return math.cos(x) - x
def g(x):
    return math.cos(x)
raiz, info = punto_fijo(g, x0=1.0, tol=1e-6, max_iter=50)
```

### Ejecutar

```bash
python global.py
# o, según tu instalación:
python3 global.py
```

