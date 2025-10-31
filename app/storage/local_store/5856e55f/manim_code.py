
from manim import *

class SolutionScene(Scene):
    def construct(self):
        title = Tex(r"Problema: x**2 - 5*x + 6 = 0")
        self.play(Write(title))
        self.wait(1)

        
        # Paso 1
        step_1 = Tex(r"Paso 1: (x - 3)*(x - 2) = 0")
        rule_1 = Tex(r"Regla: factorización")
        narr_1 = Tex(r"Factorizamos el trinomio en dos binomios.")
        

        # Paso 2
        step_2 = Tex(r"Paso 2: x=2 o x=3")
        rule_2 = Tex(r"Regla: propiedad del producto nulo")
        narr_2 = Tex(r"Si un producto es cero, uno de los factores debe anularse.")
        

        # Paso 3
        step_3 = Tex(r"Paso 3: x = 2, x = 3")
        rule_3 = Tex(r"Regla: aislar la variable")
        narr_3 = Tex(r"Resolvemos cada ecuación lineal para encontrar los valores de la incógnita.")
        

        self.play(FadeOut(title))

        
        self.play(Write(step_1))
        self.play(Write(rule_1))
        self.play(Write(narr_1))
        self.wait(1)
        self.play(FadeOut(step_1, rule_1, narr_1))
        

        self.play(Write(step_2))
        self.play(Write(rule_2))
        self.play(Write(narr_2))
        self.wait(1)
        self.play(FadeOut(step_2, rule_2, narr_2))
        

        self.play(Write(step_3))
        self.play(Write(rule_3))
        self.play(Write(narr_3))
        self.wait(1)
        self.play(FadeOut(step_3, rule_3, narr_3))
        

        final_tex = Tex(r"Solución: x = 2 , x = 3")
        self.play(Write(final_tex))
        self.wait(2)
