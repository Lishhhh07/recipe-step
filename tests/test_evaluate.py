from app.evaluate import cross_validate
from app.preprocess import load_corpus


def test_trigram_beats_unigram_baseline():
    s = load_corpus("data/recipes.txt")
    u1, _, up, _ = cross_validate(s, 1)
    t1, t3, tp, _ = cross_validate(s, 3)
    assert t1 > u1 and t3 >= t1 and tp < up