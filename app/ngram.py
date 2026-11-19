"""Milestone 3: n-gram counting, MLE probabilities and add-k smoothing."""
from collections import Counter, defaultdict

from app.preprocess import START, END


class NGramModel:
    def __init__(self, n: int = 3, k: float = 0.1):
        if n < 1:
            raise ValueError("n must be >= 1")
        self.n = n
        self.k = k
        # counts[context][word] for every context length 0..n-1
        self.counts: dict[tuple, Counter] = defaultdict(Counter)
        self.vocab: set[str] = set()

    def train(self, sentences: list[list[str]]) -> "NGramModel":
        for sent in sentences:
            tokens = [START] * (self.n - 1) + sent + [END]
            for i in range(self.n - 1, len(tokens)):
                self.vocab.add(tokens[i])
                for m in range(self.n):  # context length m
                    context = tuple(tokens[i - m:i])
                    self.counts[context][tokens[i]] += 1
        return self

    def _context(self, context) -> tuple:
        context = list(context)
        padded = [START] * (self.n - 1) + context
        return tuple(padded[len(padded) - (self.n - 1):]) if self.n > 1 else ()

    def mle_prob(self, word: str, context) -> float:
        """Maximum-likelihood estimate: count(ctx, w) / count(ctx)."""
        ctx = self._context(context)
        total = sum(self.counts[ctx].values()) if ctx in self.counts else 0
        return self.counts[ctx][word] / total if total else 0.0

    def prob(self, word: str, context) -> float:
        """Add-k smoothed probability (never zero for vocabulary words)."""
        ctx = self._context(context)
        counter = self.counts.get(ctx, Counter())
        total = sum(counter.values())
        v = len(self.vocab)
        return (counter[word] + self.k) / (total + self.k * v)

    def next_word_distribution(self, context) -> dict[str, float]:
        """Distribution over next words, backing off to shorter contexts
        when the full context was never seen in training."""
        ctx = self._context(context)
        while ctx and ctx not in self.counts:
            ctx = ctx[1:]
        counter = self.counts.get(ctx, Counter())
        candidates = [w for w in counter if w != START]
        if not candidates:
            return {}
        total = sum(counter[w] for w in candidates)
        v = len(candidates)
        return {w: (counter[w] + self.k) / (total + self.k * v) for w in candidates}

    def top_next(self, context, k: int = 5) -> list[tuple[str, float]]:
        dist = self.next_word_distribution(context)
        return sorted(dist.items(), key=lambda x: (-x[1], x[0]))[:k]
