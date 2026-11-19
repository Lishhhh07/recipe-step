# recipe-step-autocompleter

A command-line tool that autocompletes partial recipe steps using an n-gram language model
(trigram by default) trained on a corpus of cooking instructions in `data/recipes.txt`.

## Setup
```
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```
python -m app.cli hello
python -m app.cli complete "Heat the oil in a"
python -m app.cli complete "Preheat the oven to" --top 5
python -m app.cli complete "Add the" --sample --seed 3
python -m app.cli interactive
```
Options: `-n` (n-gram order), `--max-words`, `--top`, `--sample`, `--seed`, `--corpus`.

## How it works
1. **Corpus** (`data/recipes.txt`): one recipe step per line.
2. **Preprocessing** (`app/preprocess.py`): lowercase, strip noise, tokenize words/numbers/punctuation.
3. **Model** (`app/ngram.py`): counts for every context length, maximum-likelihood probability
   `count(ctx,w)/count(ctx)`, add-k smoothing, and backoff to shorter contexts for unseen contexts.
4. **Generation** (`app/generate.py`): greedy (or sampled) word-by-word continuation until the
   sentence ends or `--max-words` is reached.
5. **CLI** (`app/cli.py`): `complete` and `interactive` commands.

## Tests
```
pytest
```
