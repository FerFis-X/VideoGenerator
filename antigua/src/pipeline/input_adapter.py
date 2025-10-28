from .parser import latex_to_plain

SUPPORTED = {"plain","latex"}

def normalize(raw: str , fmt:str) -> str:
    fmt = (fmt or "plain").lower()
    if fmt not in SUPPORTED:
        raise ValueError(f"Unsupported input format: {fmt}")
    if fmt == "latex":
       return latex_to_plain(raw)

    return raw 
