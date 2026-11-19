"""Milestone 4: generate recipe step continuations."""
import random
from pathlib import Path

from app.ngram import NGramModel
from app.preprocess import END, detokenize, load_corpus, tokenize

DEFAULT_CORPUS = Path(__file__).resolve().parent.parent / "data" / "recipes.txt"


def build_model(corpus_path=DEFAULT_CORPUS, n: int = 3, k: float = 0.1) -> NGramModel:
    return NGramModel(n=n, k=k).train(load_corpus(corpus_path))


def continue_step(model: NGramModel, partial: str, max_words: int = 15,
                  sample: bool = False, seed: int | None = None) -> str:
    """Return the predicted continuation (not including the partial text)."""
    rng = random.Random(seed)
    context = tokenize(partial)
    generated: list[str] = []
    for _ in range(max_words):
        dist = model.next_word_distribution(context + generated)
        if not dist:
            break
        recent = (context + generated)[-1:]
        dist = {w: p for w, p in dist.items() if w not in recent or w == END}
        if not dist:
            break
        if sample:
            words, probs = zip(*dist.items())
            word = rng.choices(words, weights=probs)[0]
        else:
            word = max(sorted(dist), key=lambda w: dist[w])
        if word == END:
            break
        generated.append(word)
        if word == ".":
            break
    return detokenize(generated)


def complete_step(model: NGramModel, partial: str, **kwargs) -> str:
    """Partial text followed by its continuation."""
    cont = continue_step(model, partial, **kwargs)
    if not cont:
        return partial.strip()
    sep = "" if cont[0] in ".,;" else " "
    return partial.rstrip() + sep + cont
