# app/services/manim_generator.py
from typing import List, Dict

def generate_manim_code(latex_problem: str, steps: List[Dict], solution: List[str], style: str = "clean", locale: str = "es") -> str:
    """
    Genera código Manim como texto.
    Más adelante podemos variar fondo/tema según 'style'.
    """
    # Construimos bloques de Tex por paso
    steps_tex_blocks = []
    for step in steps:
        step_block = f'''
        # Paso {step["index"]}
        step_{step["index"]}_tex = Tex(r"Paso {step["index"]}: {step["latex_after"]}")
        rule_{step["index"]}_tex = Tex(r"Regla: {step["rule"]}")
        narr_{step["index"]}_tex = Tex(r"{step["narration"]}")
        '''
        steps_tex_blocks.append(step_block)

    steps_code_joined = "\n".join(steps_tex_blocks)

    final_solution_tex = " , ".join(solution)

    code = f'''
from manim import *

class SolutionScene(Scene):
    def construct(self):
        title = Tex(r"Problema: {latex_problem}")
        self.play(Write(title))
        self.wait(1)

        {steps_code_joined}

        # (Demo básico: mostramos cada paso secuencialmente)
        self.play(FadeOut(title))

{"".join([
f"""
        self.play(Write(step_{s["index"]}_tex))
        self.play(Write(rule_{s["index"]}_tex))
        self.play(Write(narr_{s["index"]}_tex))
        self.wait(1)
        self.play(FadeOut(step_{s["index"]}_tex, rule_{s["index"]}_tex, narr_{s["index"]}_tex))
""" for s in steps
])}

        final_tex = Tex(r"Solución: {final_solution_tex}")
        self.play(Write(final_tex))
        self.wait(2)
'''
    return code
