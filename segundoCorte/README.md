# Algoritmos de Análisis Numérico — Sistemas lineales

Este proyecto implementa métodos para resolver sistemas de ecuaciones lineales **\(A\mathbf{x} = \mathbf{b}\)** con \(A \in \mathbb{R}^{n \times n}\) y \(\mathbf{b} \in \mathbb{R}^n\) (en la práctica del código, sistemas cuadrados bien planteados):

- **Sustitución regresiva:** resuelve \(R\mathbf{x} = \mathbf{c}\) cuando \(R\) es **triangular superior** (ya obtenida o dada en ese forma).
- **Eliminación gaussiana con sustitución hacia atrás:** lleva la matriz aumentada \([A\,|\,\mathbf{b}]\) a forma triangular superior y luego obtiene \(\mathbf{x}\).
- **Factorización LR (con pivoteo parcial):** factoriza \(A\) en matrices triangular inferior \(L\) y superior \(R\); luego resuelve dos sistemas triangulares.
- **Gauss-Seidel:** método **iterativo** que actualiza las componentes de \(\mathbf{x}\) usando valores ya corregidos en la misma iteración.

En los archivos, el vector de términos independientes suele llamarse **`b`** o **`C`** según el módulo; las incógnitas se denotan **`X1`, `X2`, …** al escribir las ecuaciones como texto.

---

## Representación del sistema en el código

A partir de cadenas como `"X1 + 2*X2 = 5"`, la función **`parsear_sistema`** (en varios módulos) construye:

- **`A`** (o **`R`** en sustitución regresiva): matriz de coeficientes, fila = ecuación, columna = variable en orden `X1`, `X2`, …
- **`b`** (o **`C`**): vector con los valores a la derecha del signo `=`.

Requisitos habituales en este proyecto: **mismo número de ecuaciones que de incógnitas** (sistema cuadrado) y coeficientes en forma lineal con variables `X` seguidas de un entero.

### Cómo se calculan `A`, `b`, `R`, `C` en el código

1. Se buscan todas las variables que aparecen en las ecuaciones con una expresión regular (`X1`, `X2`, …) y se ordenan por su número; ese orden define las **columnas** de la matriz (`X1` es la columna 0, `X2` la columna 1, etc.).  
2. Para cada ecuación (cada fila `i`):  
   - Se separa en **lado izquierdo** y **lado derecho** usando el signo `=`.  
   - El lado derecho se evalúa como número real → se guarda en `b[i]` (o `C[i]`).  
   - En el lado izquierdo se descompone en términos con signo (`+` o `-`), se localiza la variable de cada término y se toma lo que hay delante como **coeficiente** (si no hay nada es `+1`, si solo hay `-` es `-1`, si hay algo como `2*` se evalúa ese número).  
   - Ese coeficiente se coloca en la matriz en la fila de la ecuación y la columna correspondiente a esa `Xk`.  

En `sustitucionRegresiva.py` el resultado se llama `R, C`; en `factorizacionLR.py` se llama `A, b`, pero el procedimiento es el mismo: se está construyendo el sistema lineal \(A\mathbf{x} = \mathbf{b}\) a partir del texto.

### Cómo se calcula la matriz aumentada `[A | b]`

En `eliminacionGaussiana.py` no se escribe `[A | b]` a mano, sino que se arma con `numpy`: primero se convierte `A` a matriz numérica y `b` a vector columna, y luego se concatenan horizontalmente (`np.hstack([A, b])`). El resultado es una matriz de tamaño \(n \times (n+1)\) donde las primeras \(n\) columnas son los coeficientes de las variables y la última columna es el vector de términos independientes.

### Cómo se calculan `L`, `R` y `P` en la factorización LR

En `factorizacionLR.py` la función `gauss_lr_pivoteo(A, b)` parte de copias de la matriz `A` y del vector `b` y construye:

- `L` inicial como la identidad,  
- `R` como copia de `A` sobre la que se hace la eliminación,  
- `P` como vector `[0, 1, ..., n-1]` que registra las permutaciones de filas,  
- `b_perm` como copia de `b` que se permuta en paralelo con `A`.

Para cada columna `i` se busca el elemento de **mayor valor absoluto** en esa columna a partir de la fila `i` (pivoteo parcial); si está en otra fila, se intercambian filas en `R`, en `L` (solo la parte ya construida), en `b_perm` y en `P`. Después se hacen operaciones de eliminación \(E_j \leftarrow E_j - \text{factor} \cdot E_i\); los factores `R[j,i] / R[i,i]` se van guardando en `L[j,i]`. Al final del proceso, `L` es triangular inferior con los multiplicadores, `R` es triangular superior y `P` indica cómo se reordenaron las filas con el pivoteo.

---

## Sustitución regresiva

### ¿Qué problema resuelve?

Dado un sistema **\(R\mathbf{x} = \mathbf{c}\)** con \(R\) **triangular superior** (\(R_{ij} = 0\) si \(i > j\)), se despeja \(\mathbf{x}\) empezando por la **última** ecuación.

### Fórmulas

Para \(i = n-1, n-2, \ldots, 0\) (en el código, índices \(0\) a \(n-1\)):

\[
x_i = \frac{c_i - \displaystyle\sum_{j=i+1}^{n-1} R_{ij}\, x_j}{R_{ii}}.
\]

Se necesita **\(R_{ii} \neq 0\)** en cada paso (si no, el sistema puede ser singular o mal planteado en esa forma).

### Rol de las variables

| Símbolo | Significado |
|--------|-------------|
| \(R\) | Matriz triangular superior de coeficientes |
| \(\mathbf{c}\) | Vector de términos independientes |
| \(\mathbf{x}\) | Vector solución buscado |

---

## Eliminación gaussiana con sustitución hacia atrás

### ¿Qué problema resuelve?

Resuelve **\(A\mathbf{x} = \mathbf{b}\)** para \(A\) cuadrada, en dos fases sobre la **matriz aumentada** \([A\,|\,\mathbf{b}]\).

### Fase 1 — Eliminación hacia adelante

Para cada columna pivote \(i = 0,\ldots,n-2\):

1. Elegir fila pivote: la **primera fila** \(p \ge i\) con elemento no nulo en la columna \(i\) (si no existe → sistema sin solución única / infinitas soluciones).
2. Si \(p \neq i\), **intercambiar** filas \(i\) y \(p\).
3. Para cada fila \(j > i\), hacer \(E_j \leftarrow E_j - m_{ji} E_i\) con \(m_{ji} = a_{ji}/a_{ii}\).

Al final, la parte izquierda queda **triangular superior**.

### Fase 2 — Sustitución hacia atrás

Igual que en sustitución regresiva sobre la matriz aumentada ya triangularizada:

\[
x_{n-1} = \frac{\tilde{b}_{n-1}}{\tilde{a}_{n-1,n-1}}, \quad
x_i = \frac{\tilde{b}_i - \sum_{j=i+1}^{n-1} \tilde{a}_{ij} x_j}{\tilde{a}_{ii}}.
\]

( \(\tilde{a}\), \(\tilde{b}\) son los valores tras la eliminación.)

### Rol de las variables

| Símbolo | Significado |
|--------|-------------|
| \(A\), \(\mathbf{b}\) | Sistema original |
| Matriz aumentada | \([A\,|\,\mathbf{b}]\) de tamaño \(n \times (n+1)\) |
| \(\mathbf{x}\) | Solución (única si el proceso no falla) |

---

## Factorización LR (con pivoteo parcial)

### ¿Qué problema resuelve?

También **\(A\mathbf{x} = \mathbf{b}\)**. La idea es escribir (tras permutar filas según pivoteo) algo del estilo **\(A = L R\)** con:

- \(L\): triangular **inferior** (en la implementación, unos en la diagonal implícitos en la sustitución hacia adelante),
- \(R\): triangular **superior**.

### Pasos en el código

1. **Pivoteo parcial por columnas:** en la columna \(i\), se elige la fila con **mayor valor absoluto** en esa columna (debajo del pivote) y se intercambian filas en \(A\), se actualiza el registro de permutación \(P\) y el vector \(\mathbf{b}\) permutado.
2. **Eliminación gaussiana** guardando los multiplicadores en \(L\) y la parte triangular superior en \(R\).
3. Resolver **\(L\mathbf{y} = P\mathbf{b}\)** (sustitución **hacia adelante**).
4. Resolver **\(R\mathbf{x} = \mathbf{y}\)** (sustitución **hacia atrás**).

### Rol de las variables

| Símbolo | Significado |
|--------|-------------|
| \(L\) | Factor triangular inferior |
| \(R\) | Factor triangular superior |
| \(P\) | Permutación de filas (vector de índices) |
| \(\mathbf{y}\) | Vector intermedio |
| \(\mathbf{x}\) | Solución final |

---

## Gauss-Seidel (iterativo)

### ¿Qué problema resuelve?

Aproxima la solución de **\(A\mathbf{x} = \mathbf{b}\)** sin factorizar por completo la matriz; útil cuando la diagonal es fuerte o el sistema es grande.

### Fórmula de una iteración

En la iteración \(k\), para cada ecuación \(i\) (en orden \(0,1,\ldots,n-1\)):

\[
x_i^{(k)} = \frac{1}{a_{ii}}\left(
b_i - \sum_{j<i} a_{ij}\, x_j^{(k)} - \sum_{j>i} a_{ij}\, x_j^{(k-1)}
\right).
\]

Es decir: a la **izquierda** del índice \(i\) se usan valores **ya actualizados** en la misma iteración; a la **derecha**, los del vector anterior.

### Criterio de parada (en el código)

Se calcula \(\|\mathbf{x}^{(k)} - \mathbf{x}^{(k-1)}\|\) (norma euclídea). Si es **menor que \(\varepsilon\)** (`epsilon`), se considera convergido; si no, se sigue hasta **\(N_{\max}\)** iteraciones.

### Rol de las variables

| Símbolo | Significado |
|--------|-------------|
| \(\mathbf{x}^{(0)}\) | Vector inicial (`X0`), elegido por el usuario |
| \(\varepsilon\) | Tolerancia |
| \(N_{\max}\) | Máximo de iteraciones |
| \(\mathbf{x}\) | Aproximación final |

La **verificación** de \(A\mathbf{x} \approx \mathbf{b}\) en este módulo usa una tolerancia numérica algo más relajada que en métodos directos, coherente con el error de truncamiento iterativo.

---

## Uso de `global.py`

El archivo **`segundoCorte/global.py`** ofrece un **menú interactivo**:

1. Sustitución regresiva  
2. Eliminación gaussiana  
3. Factorización LR  
4. Gauss-Seidel  

En cada caso se pide el **número de ecuaciones** y el **texto de cada ecuación**; en Gauss-Seidel también **valores iniciales** por variable, **tolerancia** y **máximo de iteraciones**.

### Ejecutar

```bash
cd segundoCorte
python global.py
```

Según tu instalación:

```bash
python3 global.py
```

---

## Archivos principales

| Archivo | Contenido resumido |
|---------|-------------------|
| `sustitucionRegresiva.py` | Parseo de ecuaciones, `sustitucion_regresiva`, visualización y verificación |
| `eliminacionGaussiana.py` | Eliminación gaussiana + sustitución hacia atrás sobre \([A\,|\,\mathbf{b}]\) |
| `factorizacionLR.py` | Factorización LR con pivoteo, sustituciones adelante/atrás, `resolver_sistema_lr` |
| `gaussSeidel.py` | `gauss_seidel`, verificación adaptada al método iterativo |
| `global.py` | Menú y lectura por consola |

---

## Dependencias

- **Python 3**
- **NumPy** (`numpy`)

Instalación típica de NumPy:

```bash
pip install numpy
```
