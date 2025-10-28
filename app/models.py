# app/models.py
from pydantic import BaseModel
from typing import List, Optional



class Step(BaseModel):
    index: int
    latex_before: str
    latex_after: str
    rule: str
    narration: str


class SolveRequest(BaseModel):
    problem_text: str  # puede ser LaTeX o texto plano
    input_format: str = "latex"  # "latex" | "text"
    locale: str = "es"           # "es" | "en" ...
    style: str = "clean"         # "clean" | "chalkboard"
    context: Optional[str] = None  # opcional, metadatos del ejercicio


class SolveResponse(BaseModel):
    job_id: str
    status: str  # "done" en el MVP síncrono
    latex: str
    solution: List[str]
    validated: bool
    steps: List[Step]
    video_url: str
    manim_code: str  # opcional: para debug/descarga
