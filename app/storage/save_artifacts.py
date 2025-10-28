# app/storage/save_artifacts.py
from pathlib import Path
import json
from typing import Dict, List

def save_artifacts(job_id: str, latex: str, solution: List[str], steps: List[Dict], manim_code: str) -> str:
    """
    Guarda los artefactos de un job en disco.
    Devuelve el directorio base.
    """
    base_dir = Path("app/storage/local_store") / job_id
    base_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "latex": latex,
        "solution": solution,
        "steps": steps,
        "manim_code": manim_code
    }

    (base_dir / "metadata.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    return str(base_dir)
