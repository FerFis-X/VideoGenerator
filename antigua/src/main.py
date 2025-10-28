import argparse
from rich import print as rprint

from .types import SolveRequest, SolveResult
from .pipeline.input_adapter import normalize
from .pipeline.parser import parse_equation
from .pipeline.solver import solve_equation

def run_cli():
    parser = argparse.ArgumentParser(
        description="Math Solver Video Agent — Epoch 1 CLI"
    )
    parser.add_argument(
        "--raw",
        "-r",
        required=True,
        help='La ecuación. Ej: "2x + 3 = 11"',
    )
    parser.add_argument(
        "--fmt",
        "-f",
        default="plain",
        help='Formato de entrada: "plain" o "latex".',
    )
    args = parser.parse_args()

    req = SolveRequest(raw_input=args.raw, input_format=args.fmt)
    expr = normalize(req.raw_input, req.input_format)

    eq, sym = parse_equation(expr)
    steps, sol = solve_equation(eq, sym)
    res = SolveResult(steps=steps, solution=sol)

    rprint("[bold]Steps:[/bold]")
    for i, s in enumerate(res.steps, 1):
        rprint(f"[green]{i}.[/green] {s.description}")

    rprint(f"\n[bold cyan]Solution:[/bold cyan] {res.solution}")

if __name__ == "__main__":
    run_cli()
