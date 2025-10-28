from pydantic import BaseModel
from typing import List , Any

class SolveRequest(BaseModel):
    raw_input: str
    input_format: str = "plain"

class Step(BaseModel):
    description : str
    state: Any | None = None

class SolveResult(BaseModel):
    steps: List[Step]
    solution: Any