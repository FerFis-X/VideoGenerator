# app/services/step_builder.py
from typing import List, Dict

def build_steps(solver_output: Dict, locale: str = "es") -> List[Dict]:
    """
    MVP:
    - Si el tipo es 'quadratic', damos la secuencia educativa bonita.
    - Si no, damos pasos genéricos: "resolvemos con SymPy".
    """

    latex_clean = solver_output["latex_clean"]              # "x**2 - 5*x + 6 = 0"
    factored_form = solver_output["factored_form"]          # "(x - 2)*(x - 3) = 0"
    sol_list = solver_output["solution"]                    # ["x = 2", "x = 3"]
    problem_type = solver_output["problem_type"]

    if problem_type == "quadratic":
        # Plantilla con factorización + producto nulo + aislamiento
        # Nota: usaremos ' or ' textual; más adelante podemos generar dinámico
        step2_after = " o ".join(s.replace(" = ", "=") for s in sol_list)  # "x=2 o x=3"
        steps = [
            {
                "index": 1,
                "latex_before": latex_clean,
                "latex_after": factored_form,
                "rule": "factorización",
                "narration": "Factorizamos el trinomio en dos binomios."
            },
            {
                "index": 2,
                "latex_before": factored_form,
                "latex_after": step2_after,
                "rule": "propiedad del producto nulo",
                "narration": "Si un producto es cero, uno de los factores debe anularse."
            },
            {
                "index": 3,
                "latex_before": step2_after,
                "latex_after": ", ".join(sol_list),
                "rule": "aislar la variable",
                "narration": "Resolvemos cada ecuación lineal para encontrar los valores de la incógnita."
            }
        ]
        return steps

    else:
        # fallback genérico para ecuaciones no cuadráticas
        generic_solution_text = ", ".join(sol_list) if sol_list else "No se encontraron soluciones cerradas."
        steps = [
            {
                "index": 1,
                "latex_before": latex_clean,
                "latex_after": generic_solution_text,
                "rule": "resolución simbólica",
                "narration": "Usamos un método algebraico/simbólico para despejar la variable."
            }
        ]
        return steps
