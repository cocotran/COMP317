# A totally superfluous module to calculate effective branching factor

def deriv(f, h):
    """Given a function f:R->R of one parameter, return a function that approximates the derivative.
    """
    def fprime(x):
        return (f(x+h) - f(x-h))/(2*h)
    return fprime


def newton_raphson(f, guess, epsilon):
    """Perform newton raphson method on a function f : R -> R"""
    fprime = deriv(f,epsilon)
    while abs(f(guess)) > epsilon:
        guess = guess - (f(guess)/fprime(guess))
    return guess



def total_nodes(N, d):
    """How many nodes total in a tree of depth d with branching factor b?
       We want to solve
            b**0 + b**1 + b**2 + ... b**d = N + 1
       Here, we create a function
            f(b) = b**0 + b**1 + b**2 + ... b**d - (N + 1)
       which we'll solve using Newton-Raphson.
    """
    def f(b):
        sum = 0
        for i in range(d+1):
            sum += b**i
        return sum - (N + 1)
    return f


def eff_br_fact(nodes, depth):
    """Calculate the effective branching factor when a solution is found at depth, after expanding nodes."""
    if depth == 0:
        return 0
    else:  
        return newton_raphson(total_nodes(nodes,depth), nodes**(1/depth), 0.0001)

