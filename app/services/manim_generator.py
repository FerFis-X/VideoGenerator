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
    Versión sin LaTeX: usa Text en vez de Tex.
    Esto evita tener instalado LaTeX en Windows.
    """

    steps_defs = []
    steps_plays = []

    for step in steps:
        idx = step["index"]
        step_txt = f"Paso {idx}: {step['latex_after']}"
        rule_txt = f"Regla: {step['rule']}"
        narr_txt = step["narration"]

        steps_defs.append(
            f"""
        # Paso {idx}
        step_{idx} = Text("{step_txt}", font_size=32)
        rule_{idx} = Text("{rule_txt}", font_size=26).next_to(step_{idx}, DOWN)
        narr_{idx} = Text("{narr_txt}", font_size=24).next_to(rule_{idx}, DOWN)
        """
        )

        steps_plays.append(
            f"""
        self.play(Write(step_{idx}))
        self.play(Write(rule_{idx}))
        self.play(Write(narr_{idx}))
        self.wait(0.5)
        self.play(FadeOut(step_{idx}, rule_{idx}, narr_{idx}))
        """
        )

    steps_defs_code = "\n".join(steps_defs)
    steps_play_code = "\n".join(steps_plays)
    final_solution_txt = "Solución: " + " , ".join(solution)

    code = f"""
from manim import *

class SolutionScene(Scene):
    def construct(self):
        title = Text("Problema: {latex_problem}", font_size=36)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))

        {steps_defs_code}

        {steps_play_code}

        final_txt = Text("{final_solution_txt}", font_size=36)
        self.play(Write(final_txt))
        self.wait(2)
"""
    return code
