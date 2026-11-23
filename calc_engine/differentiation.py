def make_secant_approximator(f, h=1e-5):
    def central_difference_approximator(x):
        return (f(x + h) - f(x - h)) / (2 * h)
    return central_difference_approximator
