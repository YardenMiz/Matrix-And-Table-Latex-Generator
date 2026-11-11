"""Turn a grid of cells into LaTeX: a matrix or a full-grid table."""
import re

MATRIX_ENVS = ["pmatrix", "bmatrix", "vmatrix", "Bmatrix", "matrix"]

_FRAC = re.compile(r"\s*(-?)\s*([^\s/\\{}]+)\s*/\s*([^\s/\\{}]+)\s*")


def frac(cell: str) -> str:
    """'a/b' -> '\\frac{a}{b}', '-a/b' -> '-\\frac{a}{b}'; anything else unchanged."""
    m = _FRAC.fullmatch(cell)
    if not m:
        return cell.strip()
    sign, num, den = m.groups()
    if num.startswith("-"):
        sign, num = "-", num[1:]
    return f"{sign}\\frac{{{num}}}{{{den}}}"


def matrix_latex(rows, env="pmatrix"):
    """Bare matrix environment; empty cells become 0."""
    body = " \\\\\n".join(
        " & ".join(frac(c) if c.strip() else "0" for c in row) for row in rows
    )
    return f"\\begin{{{env}}}\n{body}\n\\end{{{env}}}"


def _escape_amp(cell: str) -> str:
    return re.sub(r"(?<!\\)&", r"\\&", cell.strip())


def table_latex(rows, align="l", caption=""):
    """Full-grid table (\\hline after every row) inside a table float."""
    cols = max(len(r) for r in rows)
    spec = "|" + "|".join(align * cols) + "|"
    lines = ["\\begin{table}[h]", "\\centering", f"\\begin{{tabular}}{{{spec}}}", "\\hline"]
    for row in rows:
        cells = [_escape_amp(c) for c in row] + [""] * (cols - len(row))
        lines.append(" & ".join(cells) + " \\\\ \\hline")
    lines.append("\\end{tabular}")
    if caption.strip():
        lines.append(f"\\caption{{{caption.strip()}}}")
    lines.append("\\end{table}")
    return "\n".join(lines)


def parse_block(text: str):
    """Tab/newline separated text (e.g. pasted from a spreadsheet) -> padded rows."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n").split("\n")
    rows = [line.split("\t") for line in lines]
    width = max(len(r) for r in rows)
    return [r + [""] * (width - len(r)) for r in rows]
