# Algoritmo de Bisección

Este proyecto implementa el **método de bisección**, un algoritmo numérico para **encontrar raíces** de una función continua.  
En otras palabras: busca el valor \(x\) tal que \(f(x)=0\) dentro de un intervalo \([a,b]\).

---

## ¿Cómo funciona el método de bisección?

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

## ¿Cómo introducir la función en `global.py`?

En este proyecto la función \(f(x)\) se define en el archivo **`global.py`** para que el algoritmo la use directamente.

1. Abre `global.py`
2. Define tu función como una función de Python (recibiendo `x`):

Ejemplo:

```python
# global.py
import math

def f(x):
    return x**3 - x - 2

Ejemplo con trigonometría
# global.py
import math

def f(x):
    return math.cos(x) - x



Próximamente este repositorio se irá ampliando con más algoritmos numéricos, por ejemplo:
Punto Fijo