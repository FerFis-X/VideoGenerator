# app/services/step_builder.py
from typing import List, Dict

def build_steps(solver_output: Dict, locale: str = "es") -> List[Dict]:
    """
    TODO MVP real:
    - generar pasos según tipo de ecuación
    - por ahora: plantilla cuadrática factorizable
    """
    steps = [
        {
            "index": 1,
            "latex_before": solver_output["latex_clean"],
            "latex_after": solver_output["factored_form"],
            "rule": "factorización",
            "narration": "Factorizamos el trinomio en dos binomios."
        },
        {
            "index": 2,
            "latex_before": solver_output["factored_form"],
            "latex_after": "x-2=0 \\text{ o } x-3=0",
            "rule": "propiedad del producto nulo",
            "narration": "Si un producto es cero, uno de los factores debe ser cero."
        },
        {
            "index": 3,
            "latex_before": "x-2=0 \\text{ o } x-3=0",
            "latex_after": "x=2 \\text{ o } x=3",
            "rule": "aislar la variable",
            "narration": "Despejamos x en cada ecuación lineal."
        }
    ]
    return steps
