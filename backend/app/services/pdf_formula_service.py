import re
from pathlib import Path

import fitz

MATH_HINT_PATTERN = re.compile(
    r"(=|\\frac|\\sqrt|\\int|\\sum|\\lim|\^|_|[0-9]+\s*[\+\-\*/]\s*[0-9]+|[A-Za-z]\([A-Za-z0-9]+\))"
)


def _normalize_formula_line(line: str) -> str:
    cleaned = line.strip().strip("-").strip("*").strip()
    if cleaned.startswith("$") and cleaned.endswith("$") and len(cleaned) > 2:
        cleaned = cleaned[1:-1].strip()
    return re.sub(r"\s+", " ", cleaned)


def _looks_like_formula(line: str) -> bool:
    if len(line) < 3:
        return False
    return bool(MATH_HINT_PATTERN.search(line))


def extract_latex_from_pdf(file_path: str | Path, max_pages: int = 100, max_formulas: int = 200) -> list[str]:
    # Lightweight heuristic extractor: scans PDF text lines and keeps math-like content.
    document = fitz.open(str(file_path))
    formulas: list[str] = []
    seen: set[str] = set()

    try:
        page_count = min(len(document), max_pages)
        for page_index in range(page_count):
            page = document[page_index]
            for raw_line in page.get_text("text").splitlines():
                line = _normalize_formula_line(raw_line)
                if not line or not _looks_like_formula(line):
                    continue
                if line in seen:
                    continue
                formulas.append(line)
                seen.add(line)
                if len(formulas) >= max_formulas:
                    return formulas
    finally:
        document.close()

    return formulas
