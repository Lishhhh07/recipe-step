from app.ngram import NGramModel

DATA = [["add", "the", "salt", "."], ["add", "the", "oil", "."], ["add", "the", "salt", "."]]


def test_mle():
    m = NGramModel(n=3).train(DATA)
    assert abs(m.mle_prob("salt", ["add", "the"]) - 2 / 3) < 1e-9
    assert m.mle_prob("flour", ["add", "the"]) == 0.0


def test_smoothing_nonzero_and_ordered():
    m = NGramModel(n=3, k=0.5).train(DATA)
    assert m.prob("oil", ["add", "the"]) > 0
    assert m.prob("salt", ["add", "the"]) > m.prob("oil", ["add", "the"])


def test_backoff_on_unseen_context():
    m = NGramModel(n=3).train(DATA)
    assert m.next_word_distribution(["zzz", "qqq"])
    assert m.top_next(["add", "the"], 1)[0][0] == "salt"
