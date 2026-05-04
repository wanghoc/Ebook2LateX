import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import fitz

try:
    import pytesseract
    from PIL import Image
except Exception:  # pragma: no cover - OCR is optional during local import checks.
    pytesseract = None
    Image = None

NON_PRINTING_PATTERN = re.compile(r"[\u200b-\u200f\ufeff]")
PAGE_NOISE_PATTERN = re.compile(r"^\s*(page\s*)?\d+\s*$", re.IGNORECASE)
LATEX_COMMAND_PATTERN = re.compile(r"\\[a-zA-Z]+")
MATH_SYMBOL_PATTERN = re.compile(r"[=+\-*/^_()\[\]{}<>|]")
WORD_PATTERN = re.compile(r"[A-Za-zÀ-ỹ]+")
PROSE_HINT_PATTERN = re.compile(
    r"\b(cach|giải|dieu|điều|đặt|chứng|minh|suy|theo|xét|cho|ta|với|nếu|khi|trong|sau|trước|đó|nên|kết|quả)\b",
    re.IGNORECASE,
)
NOISE_PHRASES = (
    "cach giai",
    "đặt t",
    "dieu kien",
    "điều kiện",
    "gioi han",
    "giải",
    "chứng minh",
    "theo",
    "suy ra",
    "xét",
    "xet",
    "nên",
    "nen",
)


@dataclass(slots=True)
class FormulaCandidate:
    latex_content: str
    confidence_score: float

UNICODE_MATH_REPLACEMENTS = {
    "×": r"\\times",
    "÷": r"\\div",
    "−": "-",
    "–": "-",
    "—": "-",
    "·": r"\\cdot",
    "≈": r"\\approx",
    "≠": r"\\neq",
    "≤": r"\\le",
    "≥": r"\\ge",
    "∞": r"\\infty",
    "∑": r"\\sum",
    "∫": r"\\int",
    "√": r"\\sqrt{}",
    "π": r"\\pi",
    "θ": r"\\theta",
    "α": r"\\alpha",
    "β": r"\\beta",
    "γ": r"\\gamma",
    "Δ": r"\\Delta",
}


def _normalize_text(text: str) -> str:
    cleaned = unicodedata.normalize("NFKC", text)
    cleaned = NON_PRINTING_PATTERN.sub("", cleaned)
    for source, replacement in UNICODE_MATH_REPLACEMENTS.items():
        cleaned = cleaned.replace(source, replacement)
    cleaned = cleaned.replace("\xa0", " ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" ,.;:")


def _normalize_formula_line(line: str) -> str:
    cleaned = _normalize_text(line)
    cleaned = re.sub(r"^[\s•·*\-–—]+", "", cleaned)
    if cleaned.startswith("$") and cleaned.endswith("$") and len(cleaned) > 2:
        cleaned = cleaned[1:-1].strip()
    return cleaned


def _is_noise_line(line: str) -> bool:
    if not line:
        return True
    if PAGE_NOISE_PATTERN.match(line):
        return True
    if len(line) <= 2:
        return True
    normalized = _normalize_text(line).lower()
    if any(phrase in normalized for phrase in NOISE_PHRASES):
        return True
    if any(token in normalized for token in ("http://", "https://", "www.")):
        return True
    if len(normalized.split()) > 6 and PROSE_HINT_PATTERN.search(normalized):
        return True
    return False


def _math_score(line: str) -> float:
    if not line:
        return 0.0

    letters = sum(char.isalpha() for char in line)
    digits = sum(char.isdigit() for char in line)
    spaces = sum(char.isspace() for char in line)
    symbols = len(MATH_SYMBOL_PATTERN.findall(line)) + line.count("\\")
    latex_commands = len(LATEX_COMMAND_PATTERN.findall(line))
    operators = len(re.findall(r"[=+\-*/^_<>]", line))
    word_count = len(WORD_PATTERN.findall(line))
    length = max(len(line), 1)

    score = 0.0
    score += symbols * 1.6
    score += latex_commands * 2.5
    score += operators * 1.2
    score += digits * 0.15
    score += (digits / length) * 8
    score += (symbols / length) * 10
    score += 2.0 if re.search(r"\d\s*[=+\-*/^_]\s*\d", line) else 0.0
    score += 1.5 if re.search(r"\\[a-zA-Z]+", line) else 0.0
    score += 1.2 if re.search(r"[a-zA-Z]\s*\^\s*\d|\d\s*\^\s*[a-zA-Z]", line) else 0.0
    score += 0.8 if re.search(r"[A-Za-z]\([A-Za-z0-9,+\-*/\s]+\)", line) else 0.0

    score -= max(word_count - 8, 0) * 1.25
    score -= max(letters - digits - symbols - spaces, 0) * 0.05
    score -= max(word_count - 3, 0) * 0.35
    if word_count >= 5 and symbols <= 1 and latex_commands == 0:
        score -= 3.0
    if word_count >= 4 and digits == 0 and symbols <= 1 and latex_commands == 0:
        score -= 2.5
    if PROSE_HINT_PATTERN.search(line) and latex_commands == 0 and symbols <= 2:
        score -= 3.5
    if len(line) > 120:
        score -= 1.5

    return score


def _normalize_confidence(score: float) -> float:
    normalized = (score - 1.2) / 8.0
    return round(max(0.0, min(0.99, normalized)), 2)


def _is_short_equation(line: str) -> bool:
    return bool(
        re.fullmatch(
            r"[A-Za-z0-9\\\s\(\)\[\]\{\}\^_\+\-\*/=<>.,]+",
            line,
        )
        and any(symbol in line for symbol in ("=", "<", ">", "\\"))
    )


def _looks_like_formula(line: str) -> bool:
    if len(line) < 3 or _is_noise_line(line):
        return False
    score = _math_score(line)
    word_count = len(WORD_PATTERN.findall(line))
    symbol_count = len(re.findall(r"[=+\-*/^_()\[\]{}<>|]", line))

    if PROSE_HINT_PATTERN.search(line) and word_count > 3 and symbol_count <= 2 and "\\" not in line:
        return False

    if _is_short_equation(line):
        return True

    if score < 3.1:
        return False

    if word_count > 8:
        return False
    if word_count >= 4 and symbol_count <= 1 and "\\" not in line:
        return False

    if len(line) > 100 and symbol_count < 2:
        return False

    return True


def _iter_candidate_lines(page: fitz.Page) -> list[str]:
    candidate_lines: list[str] = []
    text_dict = page.get_text("dict", sort=True)

    for block in text_dict.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = " ".join(span.get("text", "") for span in spans)
            text = _normalize_formula_line(text)
            if text:
                candidate_lines.append(text)

    if candidate_lines:
        return candidate_lines

    return [
        _normalize_formula_line(raw_line)
        for raw_line in page.get_text("text", sort=True).splitlines()
        if raw_line.strip()
    ]


def _ocr_page_lines(page: fitz.Page) -> list[str]:
    if pytesseract is None or Image is None:
        return []

    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    ocr_text = pytesseract.image_to_string(image, config="--oem 1 --psm 11")
    if not ocr_text.strip():
        return []

    return [
        _normalize_formula_line(raw_line)
        for raw_line in ocr_text.splitlines()
        if raw_line.strip()
    ]


def _page_text_is_noisy(lines: list[str]) -> bool:
    if not lines:
        return True

    total = len(lines)
    noisy = 0
    formula_hits = 0
    for line in lines:
        if _is_noise_line(line):
            noisy += 1
        if _looks_like_formula(line):
            formula_hits += 1

    if formula_hits >= 2:
        return False
    if noisy / max(total, 1) >= 0.5:
        return True
    if formula_hits == 0 and total >= 3:
        return True
    return False


def _split_hybrid_line(line: str) -> list[str]:
    if ":" not in line:
        return [line]

    left, right = [part.strip() for part in line.split(":", 1)]
    candidates = []
    if left and _math_score(left) >= 2.6:
        candidates.append(left)
    if right and _math_score(right) >= 2.6:
        candidates.append(right)
    return candidates or [line]


def _canonical_key(line: str) -> str:
    return re.sub(r"\s+", "", line).lower()


def extract_latex_from_pdf(file_path: str | Path, max_pages: int = 100, max_formulas: int = 200) -> list[FormulaCandidate]:
    # Lightweight heuristic extractor: scans PDF text lines and keeps math-like content.
    document = fitz.open(str(file_path))
    formulas: list[FormulaCandidate] = []
    seen: set[str] = set()

    try:
        page_count = min(len(document), max_pages)
        for page_index in range(page_count):
            page = document[page_index]
            candidate_lines = _iter_candidate_lines(page)
            if _page_text_is_noisy(candidate_lines):
                candidate_lines = candidate_lines + _ocr_page_lines(page)

            for raw_line in candidate_lines:
                for line in _split_hybrid_line(raw_line):
                    line = _normalize_formula_line(line)
                    if not line or not _looks_like_formula(line):
                        continue
                    canonical_line = _canonical_key(line)
                    if canonical_line in seen:
                        continue
                    score = _normalize_confidence(_math_score(line))
                    formulas.append(FormulaCandidate(latex_content=line, confidence_score=score))
                    seen.add(canonical_line)
                    if len(formulas) >= max_formulas:
                        return formulas
    finally:
        document.close()

    return formulas
