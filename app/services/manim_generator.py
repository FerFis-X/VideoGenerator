# app/services/manim_generator.py
from typing import List, Dict


def generate_manim_code(
    latex_problem: str,
    steps: List[Dict],
    solution: List[str],
    style: str = "clean",
    locale: str = "es"
) -> str:
    """
    Genera código Manim para una escena llamada SolutionScene.
    Muestra:
    - título con el problema
    - cada paso con su texto
    - solución final
    """

    # Construir bloques de definición de textos de cada paso
    steps_defs = []
    steps_plays = []

    for step in steps:
        idx = step["index"]
        # ojo con las barras en LaTeX, dejamos r"" para que no se rompa
        step_tex = step["latex_after"].replace('"', '\\"')
        rule_tex = step["rule"].replace('"', '\\"')
        narr_tex = step["narration"].replace('"', '\\"')

        steps_defs.append(
            f"""
        # Paso {idx}
        step_{idx} = Tex(r"Paso {idx}: {step_tex}")
        rule_{idx} = Tex(r"Regla: {rule_tex}")
        narr_{idx} = Tex(r"{narr_tex}")
        """
        )

        steps_plays.append(
            f"""
        self.play(Write(step_{idx}))
        self.play(Write(rule_{idx}))
        self.play(Write(narr_{idx}))
        self.wait(1)
        self.play(FadeOut(step_{idx}, rule_{idx}, narr_{idx}))
        """
        )

    steps_defs_code = "\n".join(steps_defs)
    steps_play_code = "\n".join(steps_plays)

    final_solution_tex = " , ".join(solution)

    code = f"""
from manim import *

class SolutionScene(Scene):
    def construct(self):
        title = Tex(r"Problema: {latex_problem}")
        self.play(Write(title))
        self.wait(1)

        {steps_defs_code}

        self.play(FadeOut(title))

        {steps_play_code}

        final_tex = Tex(r"Solución: {final_solution_tex}")
        self.play(Write(final_tex))
        self.wait(2)
"""
    return code
