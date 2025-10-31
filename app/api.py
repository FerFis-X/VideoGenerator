# app/api.py (solo referencia)
from fastapi import APIRouter
from .models import SolveRequest, SolveResponse, Step
from .services.sympy_solver import solve_problem
from .services.step_builder import build_steps
from .services.narration_polisher import polish_steps
from .services.manim_generator import generate_manim_code
from .services.video_renderer import render_video
from .storage.save_artifacts import save_artifacts

router = APIRouter()

@router.post("/solve", response_model=SolveResponse)
def solve_endpoint(payload: SolveRequest):
    solver_output = solve_problem(
        problem_text=payload.problem_text,
        input_format=payload.input_format
    )

    steps_raw = build_steps(solver_output, locale=payload.locale)
    steps_polished = polish_steps(steps_raw, locale=payload.locale)

    manim_code = generate_manim_code(
        latex_problem=solver_output["latex_clean"],
        steps=steps_polished,
        solution=solver_output["solution"],
        style=payload.style,
        locale=payload.locale
    )

    # 👇 ahora sí intenta renderizar de verdad
    video_path, job_id = render_video(manim_code, scene_name="SolutionScene", quality="l")

    # guardar artefactos
    save_artifacts(
        job_id=job_id,
        latex=solver_output["latex_clean"],
        solution=solver_output["solution"],
        steps=steps_polished,
        manim_code=manim_code
    )

    return SolveResponse(
        job_id=job_id,
        status="done",
        latex=solver_output["latex_clean"],
        solution=solver_output["solution"],
        validated=solver_output["validated"],
        steps=[Step(**s) for s in steps_polished],
        video_url=video_path,
        manim_code=manim_code
    )
