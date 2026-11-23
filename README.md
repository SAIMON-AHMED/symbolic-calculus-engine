# Symbolic Expression Parser & Numerical Calculus Suite
*Pure-Python Symbolic Calculus, Higher-Order Closures, Numerical Quadratures, and Generator-Driven Optimization from Scratch*

A lightweight, dependency-free mathematical engine implemented entirely in pure Python. Built without NumPy, SciPy, SymPy, or any external scientific libraries, this project demonstrates clean object-oriented architecture, abstract base classes, functional closures, higher-order numerical calculus, and lazy generators for iterative optimization.

---

## 🌟 Key Highlights

- **Zero External Dependencies:** Built strictly using Python's standard library (`abc`, `math`).
- **Polymorphic Architecture:** Enforces a unified contract via an `Expression(ABC)` base class; expressions implement `__call__` so that class instances and standard Python functions/lambdas are interchangeable throughout the numerical suite.
- **Symbolic Differentiation Engine:** Exact analytical differentiation for `Polynomial`, `Trigonometric` ($\sin, \cos$), and `Exponential` expressions adhering to the power, chain, and cycle rules.
- **Higher-Order Closures ($O(h^2)$):** `make_secant_approximator` generates numerical derivative functions using the symmetric central difference quotient, canceling first-order truncation error.
- **High-Order Quadratures:** Numerical integration via the Trapezoidal Rule ($O(\Delta x^2)$) and Simpson’s 1/3 Rule ($O(\Delta x^4)$) with strict interval and parity validation guards.
- **Memory-Efficient Generator Optimizers:** Gradient descent implemented as a Python generator (`yield`), lazily emitting `(x_n, f(x_n))` trajectories at each step and automatically falling back to numerical derivatives when analytical derivatives are unavailable.

---

## 📐 Mathematical Capabilities

### 1. Symbolic Expressions (`expressions.py`)
- **Polynomials:** Defined in descending order $P(x) = c_n x^n + \dots + c_1 x + c_0$. Differentiates via the power rule:
  $$\frac{d}{dx}\left[c_k x^k\right] = k \cdot c_k x^{k-1}$$
  Guarantees immutability and automatically trims vanishing constant terms down to the zero polynomial $P'(x) = 0$.
- **Trigonometric Functions:** Handles $f(x) = A \sin(\omega x)$ and $A \cos(\omega x)$. Differentiates along the closed 4-cycle loop:
  $$\frac{d}{dx}[A \sin(\omega x)] = A\omega \cos(\omega x), \quad \frac{d}{dx}[A \cos(\omega x)] = -A\omega \sin(\omega x)$$
- **Exponentials:** Handles natural exponential growth and decay $f(x) = A e^{kx}$:
  $$\frac{d}{dx}\left[A e^{kx}\right] = A k e^{kx}$$

### 2. Numerical Differentiation & Closures (`differentiation.py`)
Constructs derivative functions dynamically through closure scoping. Employs the symmetric central difference formula:
$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$
By evaluating symmetrically around $x$, the linear error terms cancel out in Taylor expansion, achieving quadratic $O(h^2)$ accuracy compared to standard forward differences ($O(h)$).

### 3. Numerical Quadratures (`integration.py`)
Divides an interval $[a, b]$ into $n$ uniform subintervals of width $\Delta x = \frac{b - a}{n}$:
- **Trapezoidal Rule:**
  $$\int_a^b f(x)\,dx \approx \frac{\Delta x}{2} \left[ f(a) + 2 \sum_{i=1}^{n-1} f(x_i) + f(b) \right]$$
- **Simpson’s 1/3 Rule:** Fits parabolic segments across pairs of subintervals (requires even $n$):
  $$\int_a^b f(x)\,dx \approx \frac{\Delta x}{3} \left[ f(a) + 4 \sum_{i \text{ odd}} f(x_i) + 2 \sum_{i \text{ even}} f(x_i) + f(b) \right]$$
  *(Yields exact analytical solutions for any polynomial up to degree 3 with zero approximation error).*

### 4. Generator Optimization (`optimizers.py`)
Finds local minima of differentiable functions along the negative gradient:
$$x_{n+1} = x_n - \gamma \cdot f'(x_n)$$
Where $\gamma$ is the learning rate. Lazily yields `(x_n, f(x_n))` coordinates, allowing real-time inspection, custom plotting, and early termination without holding complete trajectories in memory.

---

## 🚀 Quick Start & Usage Examples

### 1. Package Import & Symbolic Calculus
```python
import calc_engine as ce

# Polynomial: 3x^2 + 2x + 4
p = ce.Polynomial([3, 2, 4])
print("p(x)  =", p)                       # 3x^2 + 2x + 4
print("p(2)  =", p(2))                    # 20

# Symbolic derivative: 6x + 2
dp = p.derivative()
print("p'(x) =", dp)                      # 6x + 2
print("p'(2) =", dp(2))                   # 14

# Trigonometric: 2 sin(3x)
t = ce.Trigonometric("sin", amp=2.0, freq=3.0)
dt = t.derivative()
print("t(x)  =", t)                       # 2.0sin(3.0x)
print("t'(x) =", dt)                      # 6.0cos(3.0x)

# Exponential: 2 e^(3x)
e = ce.Exponential(amp=2.0, k=3.0)
de = e.derivative()
print("e(x)  =", e)                       # 2.0e^(3.0x)
print("e'(x) =", de)                      # 6.0e^(3.0x)
```

---

### 2. Analytical vs. Numerical Differentiation (Closures)
```python
import math
import calc_engine as ce

# Target function: f(x) = 3x^2 - 2
poly = ce.Polynomial([3, 0, -2])

# Generate a numerical derivative closure
num_derivative = ce.make_secant_approximator(poly, h=1e-5)

x = 4.0
exact_slope = poly.derivative()(x)        # 24.0
approx_slope = num_derivative(x)          # 24.0000000004

print(f"Exact Slope:     {exact_slope}")
print(f"Numerical Slope: {approx_slope}")
assert math.isclose(exact_slope, approx_slope, rel_tol=1e-5)
```

---

### 3. Numerical Integration (Trapezoidal vs. Simpson's)
```python
import math
import calc_engine as ce

# Integrate sin(x) from 0 to pi (Exact analytical area = 2.0)
trig = ce.Trigonometric("sin")

trap_res = ce.trapezoidal_rule(trig, 0.0, math.pi, n=10)
simp_res = ce.simpsons_rule(trig, 0.0, math.pi, n=10)

print(f"Trapezoidal Result (n=10): {trap_res:.6f} (Error: {abs(trap_res - 2.0):.6f})")
print(f"Simpson's Result   (n=10): {simp_res:.6f} (Error: {abs(simp_res - 2.0):.6f})")
# Simpson's Rule achieves >150x greater accuracy on the same number of subdivisions!
```

---

### 4. Lazy Gradient Descent Trajectory
```python
import calc_engine as ce

# Minimize f(x) = (x - 3)^2 = x^2 - 6x + 9 starting at x0 = 10.0
loss_fn = ce.Polynomial([1, -6, 9])

optimizer = ce.gradient_descent(loss_fn, x0=10.0, learning_rate=0.1, tol=1e-6)

print("Optimization Steps:")
for step, (x, fx) in enumerate(optimizer):
    if step % 10 == 0:
        print(f"Step {step:02d}: x = {x:.5f}, f(x) = {fx:.8f}")

# Seamlessly converges to x = 3.0, f(x) = 0.0!
```

---

## 🏛️ Architecture & File Structure

```
Symbolic Expression Parser and Numerical Calculus Suite/
│
├── calc_engine/
│   ├── __init__.py           # Package-level exports (Single front-door API)
│   ├── expressions.py        # Expression(ABC), Polynomial, Trigonometric, Exponential
│   ├── differentiation.py    # make_secant_approximator (Higher-order functional closures)
│   ├── integration.py        # trapezoidal_rule, simpsons_rule (Numerical quadratures)
│   └── optimizers.py         # gradient_descent (Lazy generator-based optimization)
│
├── .gitignore                # Bytecode, caches, and environment exclusions
├── README.md                 # Complete documentation and mathematical reference
└── # Role & Objective.md     # Learning objectives and portfolio roadmap
```

---

## 🧪 Comprehensive Verification

To verify every feature and module across the suite, run:

```bash
python -c "import math, calc_engine as ce; p = ce.Polynomial([3, 2, 4]); dp = p.derivative(); assert p(2) == 20 and dp(2) == 14; t = ce.Trigonometric('sin', amp=2.0, freq=3.0); dt = t.derivative(); assert dt.func == 'cos' and dt.amp == 6.0; e = ce.Exponential(amp=2.0, k=3.0); de = e.derivative(); assert de.amp == 6.0; f_num = ce.make_secant_approximator(p); assert math.isclose(f_num(2), dp(2), rel_tol=1e-5); p3 = ce.Polynomial([1, 0, 0, 0]); res_s = ce.simpsons_rule(p3, 0, 2, n=10); assert math.isclose(res_s, 4.0, rel_tol=1e-6); poly_min = ce.Polynomial([1, -6, 9]); steps = list(ce.gradient_descent(poly_min, x0=10.0, learning_rate=0.1)); assert math.isclose(steps[-1][0], 3.0, abs_tol=1e-4); print('All systems nominal!')"
```
