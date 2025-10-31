
from manim import *

class SolutionScene(Scene):
    def construct(self):
        title = Text("Problema: x**2 - 3*x + 2 = 0", font_size=36)
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))

        
        # Paso 1
        step_1 = Text("Paso 1: (x - 2)*(x - 1) = 0", font_size=32)
        rule_1 = Text("Regla: factorización", font_size=26).next_to(step_1, DOWN)
        narr_1 = Text("Factorizamos el trinomio en dos binomios.", font_size=24).next_to(rule_1, DOWN)
        

        # Paso 2
        step_2 = Text("Paso 2: x=1 o x=2", font_size=32)
        rule_2 = Text("Regla: propiedad del producto nulo", font_size=26).next_to(step_2, DOWN)
        narr_2 = Text("Si un producto es cero, uno de los factores debe anularse.", font_size=24).next_to(rule_2, DOWN)
        

        # Paso 3
        step_3 = Text("Paso 3: x = 1, x = 2", font_size=32)
        rule_3 = Text("Regla: aislar la variable", font_size=26).next_to(step_3, DOWN)
        narr_3 = Text("Resolvemos cada ecuación lineal para encontrar los valores de la incógnita.", font_size=24).next_to(rule_3, DOWN)
        

        
        self.play(Write(step_1))
        self.play(Write(rule_1))
        self.play(Write(narr_1))
        self.wait(0.5)
        self.play(FadeOut(step_1, rule_1, narr_1))
        

        self.play(Write(step_2))
        self.play(Write(rule_2))
        self.play(Write(narr_2))
        self.wait(0.5)
        self.play(FadeOut(step_2, rule_2, narr_2))
        

        self.play(Write(step_3))
        self.play(Write(rule_3))
        self.play(Write(narr_3))
        self.wait(0.5)
        self.play(FadeOut(step_3, rule_3, narr_3))
        

        final_txt = Text("Solución: x = 1 , x = 2", font_size=36)
        self.play(Write(final_txt))
        self.wait(2)
