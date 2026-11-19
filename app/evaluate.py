"""Evaluate the n-gram model with 5-fold cross-validation.

Metrics (computed on held-out recipe steps):
  top1 / top3 : how often the true next token is the model's #1 / top-3 suggestion
  perplexity  : exp(-mean log p(token)) using add-k smoothed probabilities
Baselines: unigram (n=1) always suggests the most common token.
"""
import argparse
import math
import random

from app.generate import DEFAULT_CORPUS
from app.ngram import NGramModel
from app.preprocess import END, load_corpus


def evaluate_fold(train, test, n, k=0.1):
    model = NGramModel(n=n, k=k).train(train)
    hits1 = hits3 = total = 0
    log_prob = 0.0
    for sent in test:
        tokens = sent + [END]
        for i, target in enumerate(tokens):
            ctx = tokens[:i]
            top = [w for w, _ in model.top_next(ctx, 3)]
            hits1 += bool(top) and top[0] == target
            hits3 += target in top
            log_prob += math.log(model.prob(target, ctx))
            total += 1
    return hits1, hits3, log_prob, total


def cross_validate(sentences, n, folds=5, seed=42, k=0.1):
    data = sentences[:]
    random.Random(seed).shuffle(data)
    h1 = h3 = tot = 0
    lp = 0.0
    for f in range(folds):
        test = data[f::folds]
        train = [s for i, s in enumerate(data) if i % folds != f]
        a, b, c, d = evaluate_fold(train, test, n, k)
        h1 += a; h3 += b; lp += c; tot += d
    return h1 / tot, h3 / tot, math.exp(-lp / tot), tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=str(DEFAULT_CORPUS))
    ap.add_argument("--k", type=float, default=0.1)
    args = ap.parse_args()
    sentences = load_corpus(args.corpus)