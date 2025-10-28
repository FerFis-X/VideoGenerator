from src.pipeline.parser import parse_equation
from src.pipeline.solver import solve_equation


def test_linear():
    eq, sym = parse_equation("2x + 3 = 11")
    steps, sol = solve_equation(eq, sym)
    assert sol == [4]