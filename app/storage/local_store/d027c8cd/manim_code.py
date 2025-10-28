
from manim import *

class SolutionScene(Scene):
    def construct(self):
        title = Tex(r"Problema: x^2 - 5x + 6 = 0")
        self.play(Write(title))
        self.wait(1)

        
        # Paso 1
        step_1_tex = Tex(r"Paso 1: (x-2)(x-3)=0")
        rule_1_tex = Tex(r"Regla: factorización")
        narr_1_tex = Tex(r"Factorizamos el trinomio en dos binomios.")
        

        # Paso 2
        step_2_tex = Tex(r"Paso 2: x-2=0 \text{ o } x-3=0")
        rule_2_tex = Tex(r"Regla: propiedad del producto nulo")
        narr_2_tex = Tex(r"Si un producto es cero, uno de los factores debe ser cero.")
        

        # Paso 3
        step_3_tex = Tex(r"Paso 3: x=2 \text{ o } x=3")
        rule_3_tex = Tex(r"Regla: aislar la variable")
        narr_3_tex = Tex(r"Despejamos x en cada ecuación lineal.")
        

        # (Demo básico: mostramos cada paso secuencialmente)
        self.play(FadeOut(title))


        self.play(Write(step_1_tex))
        self.play(Write(rule_1_tex))
        self.play(Write(narr_1_tex))
        self.wait(1)
        self.play(FadeOut(step_1_tex, rule_1_tex, narr_1_tex))

        self.play(Write(step_2_tex))
        self.play(Write(rule_2_tex))
        self.play(Write(narr_2_tex))
        self.wait(1)
        self.play(FadeOut(step_2_tex, rule_2_tex, narr_2_tex))

        self.play(Write(step_3_tex))
        self.play(Write(rule_3_tex))
        self.play(Write(narr_3_tex))
        self.wait(1)
        self.play(FadeOut(step_3_tex, rule_3_tex, narr_3_tex))


        final_tex = Tex(r"Solución: x = 2 , x = 3")
        self.play(Write(final_tex))
        self.wait(2)
