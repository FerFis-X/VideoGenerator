from sympy import Eq
from ..types import Step

# a simplyfied version steps buildes for equaitions

def explain_linear_equation(eq: Eq, sym):
    steps = []
    lhs , rhs = eq.lhs , eq.rhs
    steps.append(Step(description=f"Initial equation: {lhs} = {rhs}"))

    # Move constant terms to th right (heuristic)
    # Epoch 1: we dont symbollicaly isolate terms perfectly
    from sympy import collect , symbols
    a = collect(lhs,sym)
    steps.append(Step(description=f"Group terms with {sym}: {a} = {rhs}"))

    # substract constant (a.as_coef_add return coeff and constants)
    coeff , rest = a.as_coeff_add(sym)
    const_part = sum([t for t in rest if not t.has(sym)] , start = 0)
    if const_part !=0:
        steps.append(Step(descripttion = f"Substract {const_part} both sides" ))
        lhs2 = a - const_part
        rhs2 = rhs - const_part
    else:
        lhs2 ,rhs2 = a , rhs
    # Divide by coeff
    m = lhs2.as_coeff_mul(sym)[0]
    if m != 1:
        steps.append(Step(description=f"Divide both sides by {m}"))
        lhs3 = lhs2 / m
        rhs3 = rhs2 / m
    else:
        lhs3, rhs3 = lhs2, rhs2


    steps.append(Step(description=f"Despeje: {sym} = {rhs3}"))
    return steps