"""Milestone 2: clean and tokenize the recipe corpus."""
import re
from pathlib import Path

START, END = "<s>", "</s>"
_TOKEN_RE = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+|[.,;]")


def clean_text(line: str) -> str:
    """Lowercase and normalise whitespace / odd characters."""
    line = line.lower().replace("\u2019", "'")
    line = re.sub(r"\([^)]*\)", " ", line)  # drop parenthetical notes
    line = re.sub(r"[^a-z0-9'.,; ]+", " ", line)
    return re.sub(r"\s+", " ", line).strip()


def tokenize(text: str) -> list[str]:
    """Split text into words, numbers and . , ; punctuation tokens."""
    return _TOKEN_RE.findall(clean_text(text))


def load_corpus(path: str | Path) -> list[list[str]]:
    """Read one recipe step per line; return a list of token lists."""
    sentences = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        tokens = tokenize(line)
        if tokens:
            sentences.append(tokens)
    return sentences


def detokenize(tokens: list[str]) -> str:
    """Join tokens back into readable text."""
    out = " ".join(tokens)
    return re.sub(r"\s+([.,;])", r"\1", out)
