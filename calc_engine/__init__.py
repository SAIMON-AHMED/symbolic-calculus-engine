from .expressions import Expression, Polynomial, Trigonometric, Exponential
from .differentiation import make_secant_approximator
from .integration import trapezoidal_rule, simpsons_rule
from .optimizers import gradient_descent