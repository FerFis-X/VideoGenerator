# app/services/video_renderer.py
import uuid
from pathlib import Path

def render_video(manim_code: str) -> str:
    """
    FUTURO:
    - Guardar manim_code en un archivo temporal.
    - Llamar a manim (subprocess) para renderizar.
    - Guardar el mp4 final.
    MVP:
    - simular un archivo mp4 y devolver su "ruta".
    """
    fake_job_id = str(uuid.uuid4())[:8]
    output_dir = Path("app/storage/local_store") / fake_job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # Guardamos el código manim para depuración
    (output_dir / "manim_code.py").write_text(manim_code, encoding="utf-8")

    # Simular video
    fake_video_path = output_dir / "video.mp4"
    fake_video_path.write_text("VIDEO_PLACEHOLDER", encoding="utf-8")

    # Devolver ruta 'pública' (por ahora es local)
    return str(fake_video_path), fake_job_id
