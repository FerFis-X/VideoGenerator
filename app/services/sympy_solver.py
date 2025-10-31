# app/services/sympy_solver.py
from typing import Dict, List, Tuple
import re
from sympy import symbols, Eq, sympify, solve, factor, simplify
from sympy.parsing.latex import parse_latex
from sympy.core.relational import Relational
from sympy.core.sympify import SympifyError


def _normalize_plaintext_expr(expr_text: str) -> str:
    """
    Limpia una expresión matemática escrita estilo humano para que SymPy la entienda.
    Hace:
    - reemplaza ^ por ** (potencia)
    - inserta * en casos como 5x -> 5*x
    - inserta * en 5(x+1) -> 5*(x+1)
    - inserta * en )(
        (x-2)(x-3) -> (x-2)*(x-3)
    - inserta * en x(x+1) -> x*(x+1)

    Nota: esto es heurístico, pero suficiente para álgebra básica MVP.
    """

    s = expr_text.strip()

    # potencia estilo humano -> python
    s = s.replace("^", "**")

    # )(
    # ejemplo: (x-2)(x-3)  -> (x-2)*(x-3)
    s = re.sub(r"\)\s*\(", ")*(", s)

    # número seguido de variable: 5x -> 5*x
    # (\d)  ( [a-zA-Z] )
    s = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", s)

    # variable seguida de paréntesis: x( -> x*(
    s = re.sub(r"([a-zA-Z])\s*\(", r"\1*(", s)

    # número seguido de paréntesis: 2( -> 2*(
    s = re.sub(r"(\d)\s*\(", r"\1*(", s)

    return s


def _to_equation(expr_text: str, input_format: str) -> Tuple[Eq, List[str]]:
    """
    Convierte el texto/LaTeX del usuario a una ecuación SymPy Eq(lhs, rhs).
    Devuelve:
      - equation: Eq(lhs, rhs)
      - symbols_used: lista de nombres de variables detectadas (["x"], etc.)

    Reglas:
    - Si hay '=', separamos lhs y rhs.
    - Si no hay '=', asumimos "= 0".
    """

    if input_format.lower() == "latex":
        # Para LaTeX, hacemos split manual si trae '='
        if "=" in expr_text:
            left_txt, right_txt = expr_text.split("=", 1)
            lhs = parse_latex(left_txt)
            rhs = parse_latex(right_txt)
        else:
            lhs = parse_latex(expr_text)
            rhs = 0
    else:
        # input_format == "text" (o cualquier otra cosa que no sea latex)
        fixed = _normalize_plaintext_expr(expr_text)

        if "=" in fixed:
            left_txt, right_txt = fixed.split("=", 1)
        else:
            left_txt, right_txt = fixed, "0"

        try:
            lhs = sympify(left_txt)
            rhs = sympify(right_txt)
        except SympifyError as e:
            raise ValueError(
                f"No pude interpretar la expresión matemática: '{expr_text}'. "
                f"Intenté normalizarla como '{fixed}' y aún así SymPy no la aceptó."
            ) from e

    # detectar símbolos
    symbols_used = list(map(str, (lhs.free_symbols | getattr(rhs, "free_symbols", set()))))

    # construir ecuación simbólica
    equation = Eq(lhs, rhs)
    return equation, symbols_used


def _solve_equation(eq: Eq, vars_candidates: List[str]) -> List[Relational]:
    """
    Resuelve la ecuación para la primera variable candidata.
    Retorna lista de ecuaciones tipo Eq(x, 2), Eq(x, 3), etc.
    """
    if len(vars_candidates) == 0:
        return []

    # primera variable como principal
    main_var = symbols(vars_candidates[0])
    sols = solve(eq, main_var, dict=False)

    normalized = []
    for s in sols:
        if isinstance(s, Relational):
            normalized.append(s)
        else:
            # si es un número/expresión, lo envolvemos en Eq(var, value)
            normalized.append(Eq(main_var, s))

    return normalized


def _validate_solutions(eq: Eq, solutions: List[Relational]) -> bool:
    """
    Valida sustituyendo las soluciones en la ecuación original.
    Si TODAS cumplen -> True. Si alguna no, -> False.
    """
    lhs = eq.lhs
    rhs = eq.rhs

    for sol in solutions:
        if not isinstance(sol, Relational):
            continue

        # sol: Eq(x, 2)
        var_symbols = list(sol.free_symbols)
        if not var_symbols:
            continue

        # normalmente es una sola variable, ej x
        main_var = var_symbols[0]
        value = sol.rhs

        diff = simplify(lhs.subs(main_var, value) - rhs.subs(main_var, value))
        # si no da 0 exacto -> no validado
        if diff != 0:
            return False

    return True


def _factor_expression(eq: Eq) -> str:
    """
    Intenta factorizar lhs - rhs.
    Devuelve string estilo "(x - 2)*(x - 3) = 0" o "x**2 - 5*x + 6 = 0".
    """
    lhs = eq.lhs
    rhs = eq.rhs

    expr = simplify(lhs - rhs)
    factored = factor(expr)

    # Si factor() no cambió nada, devolvemos la forma original
    if str(factored) == str(expr):
        return f"{str(expr)} = 0"
    else:
        return f"{str(factored)} = 0"


def _to_latex_clean(eq: Eq) -> str:
    """
    Representación amigable de la ecuación original para mostrar/la respuesta JSON.
    Por ahora devolvemos str() normal de SymPy.
    """
    return f"{str(eq.lhs)} = {str(eq.rhs)}"


def _to_solution_strings(solutions: List[Relational]) -> List[str]:
    """
    Convierte [Eq(x,2), Eq(x,3)] -> ["x = 2", "x = 3"].
    """
    out = []
    for sol in solutions:
        if isinstance(sol, Relational):
            out.append(f"{str(sol.lhs)} = {str(sol.rhs)}")
        else:
            out.append(str(sol))
    return out


def solve_problem(problem_text: str, input_format: str) -> Dict:
    """
    Función principal llamada por /solve.
    Retorna dict con:
    - latex_clean: str
    - solution: List[str]
    - problem_type: str
    - validated: bool
    - factored_form: str
    """

    # 1. Construir ecuación simbólica
    eq, vars_candidates = _to_equation(problem_text, input_format)

    # 2. Resolver para la variable principal
    raw_solutions = _solve_equation(eq, vars_candidates)

    # 3. Validar sustituyendo
    is_valid = _validate_solutions(eq, raw_solutions)

    # 4. Heurística de tipo de problema (lineal, cuadrática, cúbica...)
    problem_type = "generic"
    try:
        if len(vars_candidates) == 1:
            var_symbol = symbols(vars_candidates[0])
            poly_expr = (eq.lhs - eq.rhs)
            poly_degree = poly_expr.as_poly(var_symbol).degree()
            if poly_degree == 1:
                problem_type = "linear"
            elif poly_degree == 2:
                problem_type = "quadratic"
            elif poly_degree == 3:
                problem_type = "cubic"
    except Exception:
        pass

    # 5. Factorización útil para pasos
    factored_form = _factor_expression(eq)

    # 6. Convertir a strings utilizables en el pipeline
    latex_clean = _to_latex_clean(eq)
    solution_strings = _to_solution_strings(raw_solutions)

    return {
        "latex_clean": latex_clean,
        "solution": solution_strings,
        "problem_type": problem_type,
        "validated": is_valid,
        "factored_form": factored_form
    }
