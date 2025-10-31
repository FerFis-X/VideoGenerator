# app/services/video_renderer.py
import uuid
import subprocess
import sys
from pathlib import Path


def render_video(
    manim_code: str,
    scene_name: str = "SolutionScene",
    quality: str = "l",
) -> tuple[str, str]:
    """
    Renderiza un video de Manim de verdad.

    Devuelve:
    - video_path (str)
    - job_id (str)
    """

    # 1. Crear carpeta del job
    job_id = str(uuid.uuid4())[:8]
    base_dir = Path("app/storage/local_store") / job_id
    base_dir.mkdir(parents=True, exist_ok=True)

    # 2. Guardar el código
    manim_file = base_dir / "manim_code.py"
    manim_file.write_text(manim_code, encoding="utf-8")

    # 3. Nombre de salida dentro de esa carpeta
    output_name = "video.mp4"
    output_path = base_dir / output_name

    # ⚠️ IMPORTANTE:
    # Como vamos a ejecutar con cwd=base_dir,
    # al comando le pasamos SOLO el nombre del archivo: "manim_code.py"
    manim_input_name = "manim_code.py"

    # 4. Comando manim (intento 1: manim ...)
    manim_cmd = [
        "manim",
        manim_input_name,       # NO ruta absoluta
        scene_name,
        f"-q{quality}",
        "-o",
        output_name,
    ]

    try:
        completed = subprocess.run(
            manim_cmd,
            cwd=base_dir,         # ejecuta dentro de la carpeta del job
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # 5. Fallback: python -m manim ...
        manim_cmd = [
            sys.executable,
            "-m",
            "manim",
            manim_input_name,
            scene_name,
            f"-q{quality}",
            "-o",
            output_name,
        ]
        completed = subprocess.run(
            manim_cmd,
            cwd=base_dir,
            capture_output=True,
            text=True,
            check=False,
        )

    # 6. Verificar que el video exista
    if not output_path.exists():
        # guardar logs para depurar
        (base_dir / "manim_stdout.log").write_text(completed.stdout or "", encoding="utf-8")
        (base_dir / "manim_stderr.log").write_text(completed.stderr or "", encoding="utf-8")

        # para no romper el flujo:
        (base_dir / "RENDER_FAILED.txt").write_text(
            "Manim no generó el video. Revisa manim_stdout.log y manim_stderr.log",
            encoding="utf-8",
        )
        return str(base_dir / "RENDER_FAILED.txt"), job_id

    return str(output_path), job_id
