from manim import Scene , Text
from ..types import Step

class StepsScene(Scene):
    def __init__(self,steps: list[Step], **kwargs):
        self.__steps = steps
        super().__init__(**kwargs)

    def construct(self):
        y = 3.0
        for i , s in enumerate(self.__steps[:5]):
            t = Text(s.description , font_size = 32).to_edge(LEFT).shift([0,y-i*0,8,0])
