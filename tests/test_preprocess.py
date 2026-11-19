from app.preprocess import clean_text, detokenize, load_corpus, tokenize


def test_clean_and_tokenize():
    assert tokenize("Add 2 onions, stir.") == ["add", "2", "onions", ",", "stir", "."]


def test_clean_text_whitespace():
    assert clean_text("  Hello   WORLD! ") == "hello world"


def test_detokenize():
    assert detokenize(["stir", "well", ",", "then", "serve", "."]) == "stir well, then serve."


def test_corpus_loads():
    sents = load_corpus("data/recipes.txt")
    assert len(sents) >= 100
    assert all(s for s in sents)
