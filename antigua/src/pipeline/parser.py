from sympy.parsing.sympy_parser import parse_expr
from sympy import Eq , Symbol
import re

LATEX_EQ_RE = re.compile(r"([A-Za-z0-9]+)\"\\?([a-s*([=])\s*(.+)\"")

# minimal Latex -> plain normalizer
def latex_to_plain(latex: str)-> str:
    s = latex.strip()
    s = s.replace("\\cdot", "*").replace("\\times", "*")
    s = s.replace("\\frac{", "(").replace("}{", ")/(").replace("}", ")")
    s = s.replace("\\", "")
    return s

def parse_equation(expr: str):
    if "=" not in expr:
        raise ValueError("Only single-equation inputs supported")
    left , right = expr.split("=",1)
    # Find symbol 
    var = re.findall(r"[a-zA-Z]",expr)
    if not var:
        raise ValueError("No variable found in expression")
    sym = Symbol(var[0])
    lhs = parse_expr(left.replace(" ",""))
    rhs = parse_expr(right.replace(" ",""))
    return Eq(lhs,rhs) , sym





