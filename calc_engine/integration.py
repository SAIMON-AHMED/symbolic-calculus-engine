def trapezoidal_rule(f, a, b, n=100):
    if a > b:
        raise ValueError("Lower limit cannot be greater than upper limit.")
    if n <= 0:
        raise ValueError("Number of subintervals n must be greater than 0")
    del_x = (b - a) / n
    total = f(a) + f(b)

    for i in range(1, n):
        total += (2 * f(a + i * del_x))

    total *= del_x / 2

    return total

def simpsons_rule(f, a, b, n=100):
    if a > b:
        raise ValueError("Lower limit cannot be greater than upper limit.")
    if n <= 0:
        raise ValueError("Number of subintervals n must be greater than 0")
    if n % 2 != 0:
        raise ValueError("Number of subintervals n must be an even integer")

    del_x = (b - a) / n
    total = f(a) + f(b)

    for i in range(1, n):
        if i % 2 == 0:
            total += (2 * f(a + i * del_x))
        else:
            total += (4 * f(a + i * del_x))

    total *= del_x / 3

    return total