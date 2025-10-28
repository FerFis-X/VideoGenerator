from sympy import Eq , solve
from .explainer import explain_linear_equation

# Router for example : Lineal equiation 

def solve_equation(eq: Eq,sym):
    # Build Steps (simple balancing metod)
    steps = explain_linear_equation(eq,sym)
    sol = solve(eq,sym)
    return steps, sol