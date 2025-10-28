# app/services/sympy_solver.py
from typing import List, Dict

def solve_problem(problem_text: str, input_format: str) -> Dict:
    """
    TODO MVP real:
    - parse LaTeX (si input_format == "latex")
    - resolver con sympy.solve o sympy.dsolve
    - validar sustituyendo
    """
    # Dummy temporal para probar el esqueleto:
    return {
        "latex_clean": "x^2 - 5x + 6 = 0",
        "solution": ["x = 2", "x = 3"],
        "problem_type": "quadratic",
        "validated": True,
        "factored_form": "(x-2)(x-3)=0"  # útil para steps
    }
