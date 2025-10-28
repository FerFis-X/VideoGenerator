# app/services/narration_polisher.py
from typing import List, Dict

def polish_steps(steps: List[Dict], locale: str = "es") -> List[Dict]:
    """
    FUTURO:
    - llamar a LLM con temperature=0
    - reescribir narration en tono educativo
    MVP:
    - devolver igual
    """
    return steps
