from .differentiation import make_secant_approximator

def gradient_descent(f, x0, learning_rate=0.01, max_iter=1000, tol=1e-6, f_prime=None):
    if f_prime is None:
        if hasattr(f, "derivative"):
            f_prime = f.derivative()
        else:
            f_prime = make_secant_approximator(f)

    for iter in range(max_iter):
        yield (x0, f(x0))
        x_new = x0 - learning_rate * f_prime(x0)

        if abs(x_new - x0) < tol:
            yield (x_new, f(x_new))
            break
        x0 = x_new
        