# app/services/video_renderer.py
import uuid
import subprocess
import sys
from pathlib import Path


def render_video(manim_code: str, scene_name: str = "SolutionScene", quality: str = "l") -> tuple[str, str]:
    """
    Renderiza de verdad un video de Manim.

    Params:
    - manim_code: string con el código Python de la escena
    - scene_name: nombre de la clase de Scene dentro del código
    - quality: "l" (low/rápido), "m", "h", "k" (1080p). Para pruebas: "l".

    Returns:
    - (video_path, job_id)
    """

    # 1. Crear carpeta del job
    job_id = str(uuid.uuid4())[:8]
    base_dir = Path("app/storage/local_store") / job_id
    base_dir.mkdir(parents=True, exist_ok=True)

    # 2. Escribir el código manim a archivo
    manim_file = base_dir / "manim_code.py"
    manim_file.write_text(manim_code, encoding="utf-8")

    # 3. Definir nombre de salida
    output_name = "video.mp4"
    output_path = base_dir / output_name

    # 4. Armar comando manim
    # manim <file> <SceneName> -q<quality> -o <output>
    # Ej: manim manim_code.py SolutionScene -ql -o video.mp4
    manim_cmd = [
        "manim",
        str(manim_file),
        scene_name,
        f"-q{quality}",
        "-o",
        output_name,
    ]

    # 5. Ejecutar
    # En algunos entornos (Windows) es más seguro usar python -m manim ...
    try:
        completed = subprocess.run(
            manim_cmd,
            cwd=base_dir,             # correr dentro de la carpeta del job
            capture_output=True,
            text=True,
            check=False               # no levantes excepción automática
        )
    except FileNotFoundError:
        # fallback: intentar con python -m manim
        manim_cmd = [
            sys.executable,
            "-m",
            "manim",
            str(manim_file),
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
            check=False
        )

    # 6. Revisar si se creó el archivo
    if not output_path.exists():
        # si no se generó, guardamos los logs para depurar
        (base_dir / "manim_stdout.log").write_text(completed.stdout or "", encoding="utf-8")
        (base_dir / "manim_stderr.log").write_text(completed.stderr or "", encoding="utf-8")

        # y devolvemos un error "suave" (seguimos el pipeline pero avisamos)
        # Para el MVP, devolvemos la ruta al log en vez de romper
        return str(base_dir / "RENDER_FAILED.txt"), job_id

    return str(output_path), job_id
