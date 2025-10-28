# app/services/sympy_solver.py
from typing import Dict, List, Tuple, Union
from sympy import symbols, Eq, sympify, solve, factor, simplify
from sympy.parsing.latex import parse_latex
from sympy.core.relational import Relational


def _to_equation(expr_text: str, input_format: str) -> Tuple[Eq, List[str]]:
    """
    Convierte el texto del usuario en una ecuación SymPy Eq(lhs, rhs)
    y devuelve también una lista con los símbolos detectados (variables).

    Regla básica:
    - Si hay un "=", separamos en lhs y rhs.
    - Si no hay "=", asumimos "= 0".
    """

    if input_format.lower() == "latex":
        # Intentar parsear LaTeX a expresión simbólica
        # OJO: si viene con '=', parse_latex no va a partir automáticamente,
        # así que hacemos split manual, luego parse_latex a cada lado.
        if "=" in expr_text:
            left_txt, right_txt = expr_text.split("=", 1)
            lhs = parse_latex(left_txt)
            rhs = parse_latex(right_txt)
        else:
            lhs = parse_latex(expr_text)
            rhs = 0
    else:
        # input_format == "text"
        # sympify entiende strings matemáticos tipo "x^2 - 5*x + 6"
        # pero en Python el exponente es **, no ^. Vamos a reemplazar ^ -> **.
        fixed = expr_text.replace("^", "**")

        if "=" in fixed:
            left_txt, right_txt = fixed.split("=", 1)
            lhs = sympify(left_txt)
            rhs = sympify(right_txt)
        else:
            lhs = sympify(fixed)
            rhs = sympify("0")

    # Detectar símbolos variables (ej: x, y, etc.)
    symbols_used = list(map(str, (lhs.free_symbols | getattr(rhs, "free_symbols", set()))))

    # Crear Eq(lhs, rhs)
    equation = Eq(lhs, rhs)
    return equation, symbols_used


def _solve_equation(eq: Eq, vars_candidates: List[str]) -> List:
    """
    Resuelve la ecuación simbólica para las variables.
    Estrategia:
    - Si hay una sola variable candidata (ej. ['x']), resolvemos para esa.
    - Si hay varias, intentamos la primera por simplicidad MVP.
    """
    if len(vars_candidates) == 0:
        # sin variables? raro, devolvemos lista vacía
        return []

    main_var = symbols(vars_candidates[0])
    sols = solve(eq, main_var, dict=False)

    # solve puede devolver:
    # - una lista de valores [2, 3]
    # - una lista de ecuaciones tipo [Eq(x,2), Eq(x,3)]
    # vamos a normalizar a Eq(x, value) para consistencia interna
    normalized = []
    for s in sols:
        if isinstance(s, Relational):
            normalized.append(s)
        else:
            normalized.append(Eq(main_var, s))

    return normalized


def _validate_solutions(eq: Eq, solutions: List[Eq]) -> bool:
    """
    Valida sustituyendo cada solución en la ecuación original.
    Para ecuaciones algebraicas simples, basta evaluar lhs - rhs.
    Si TODAS cuadran => True, si alguna falla => False.
    """
    lhs = eq.lhs
    rhs = eq.rhs

    for sol in solutions:
        # sol es tipo Eq(x, 2)
        if not isinstance(sol, Relational):
            # no es Eq(...)? saltamos validación estricta
            continue

        var = list(sol.free_symbols)[0]  # ej. x
        value = sol.rhs                 # ej. 2

        diff = simplify(lhs.subs(var, value) - rhs.subs(var, value))
        # Debe ser 0 si satisface la ecuación
        if diff != 0:
            return False

    return True


def _factor_expression(eq: Eq) -> str:
    """
    Para ayudar al Step Builder, intentamos factorizar lhs - rhs.
    Ejemplo:
      x^2 - 5x + 6 = 0  -> (x-2)*(x-3)
    Retornamos string LaTeX " (x-2)(x-3)=0 " si se ve diferente.
    """
    lhs = eq.lhs
    rhs = eq.rhs

    expr = simplify(lhs - rhs)
    factored = factor(expr)

    # Si no hay cambio, igual devolvemos la forma factorizada como LaTeX-like
    # Nota: usamos str(...) como aproximación; más adelante podemos usar sympy.latex
    if str(factored) == str(expr):
        # no factoriza mejor, devolvemos algo tipo "x^2 - 5x + 6 = 0"
        return f"{str(expr)} = 0"
    else:
        # ejemplo "(x - 2)*(x - 3) = 0"
        return f"{str(factored)} = 0"


def _to_latex_clean(eq: Eq) -> str:
    """
    Representación limpia tipo "x^2 - 5x + 6 = 0" para que fluya en los pasos.
    Para ahora usamos str(...) por simplicidad.
    Más adelante podemos usar sympy.latex(eq) para código LaTeX perfecto.
    """
    return f"{str(eq.lhs)} = {str(eq.rhs)}"


def _to_solution_strings(solutions: List[Eq]) -> List[str]:
    """
    Convierte [Eq(x,2), Eq(x,3)] -> ["x = 2", "x = 3"] como strings.
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
    Punto de entrada usado por el endpoint /solve.

    Retorna dict con:
    - latex_clean (string representable)
    - solution (lista de strings tipo "x = 2")
    - problem_type ("quadratic", "linear", "generic"... best-effort)
    - validated (bool)
    - factored_form (string tipo "(x-2)*(x-3) = 0")
    """

    # 1. Parsear y construir Eq(lhs, rhs)
    eq, vars_candidates = _to_equation(problem_text, input_format)

    # 2. Resolver
    raw_solutions = _solve_equation(eq, vars_candidates)

    # 3. Validar
    is_valid = _validate_solutions(eq, raw_solutions)

    # 4. Clasificar tipo de problema (simple heuristic)
    #    - si el grado (polinomio en 1 variable) es 1 -> linear
    #    - grado 2 -> quadratic
    #    - otro -> generic
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
        # si no podemos sacar grado, lo dejamos en generic
        pass

    # 5. Factorización (para builder)
    factored_form = _factor_expression(eq)

    # 6. Limpio para mostrar
    latex_clean = _to_latex_clean(eq)
    solution_strings = _to_solution_strings(raw_solutions)

    return {
        "latex_clean": latex_clean,                 # ej "x**2 - 5*x + 6 = 0"
        "solution": solution_strings,               # ej ["x = 2", "x = 3"]
        "problem_type": problem_type,               # ej "quadratic"
        "validated": is_valid,                      # ej True
        "factored_form": factored_form              # ej "(x - 2)*(x - 3) = 0"
    }
