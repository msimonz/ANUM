# Algoritmos de Análisis Numérico

Este proyecto implementa algoritmos numéricos para **encontrar raíces** de ecuaciones (valor \(x\) tal que \(f(x)=0\)):

- **Método de bisección**: busca la raíz en un intervalo \([a,b]\) donde \(f\) cambie de signo.
- **Método de punto fijo**: busca \(x\) tal que \(x = g(x)\), iterando \(x_{n+1} = g(x_n)\).

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

## ¿Cómo introducir las funciones en `global.py`?

En el archivo **`global.py`** se definen las funciones y se llaman los algoritmos:

- **Bisección:** necesita \(f(x)\) y un intervalo \([a,b]\) con \(f(a)\cdot f(b) < 0\).
- **Punto fijo:** necesita \(g(x)\) tal que la raíz cumpla \(x = g(x)\), y un valor inicial \(x_0\).

### Ejemplo (misma ecuación con ambos métodos)

Para \(f(x) = x^3 - x - 2 = 0\):

- Bisección usa \(f(x)\) en el intervalo \([1, 2]\).
- Punto fijo usa \(g(x) = (x+2)^{1/3}\) (despeje \(x^3 = x + 2\)).

```python
# global.py
from biseccion import biseccion
from puntofijo import punto_fijo

def f(x):
    return x**3 - x - 2

# Bisección
raiz, info = biseccion(f, a=1, b=2, tol=1e-6, max_iter=50)

# Punto fijo: x = (x+2)^(1/3)
def g(x):
    return (x + 2) ** (1.0 / 3.0)
raiz_pf, info_pf = punto_fijo(g, x0=1.0, tol=1e-6, max_iter=50)
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

