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

## Results
Evaluated with 5-fold cross-validation on the 117-step corpus (`python -m app.evaluate`,
output saved in `results/evaluation.txt`). Top-k = how often the true next token is among
the model's k best suggestions.

| model | top-1 | top-3 | perplexity |
|---|---|---|---|
| unigram (baseline: always suggest common words) | 8.6% | 22.8% | 127.7 |
| bigram | 32.0% | 46.9% | 45.9 |
| trigram (default) | 37.4% | 49.3% | 94.4 |

Example completions (`results/examples.txt`):
```
Heat the oil in a            -> Heat the oil in a large bowl and mix well.
Preheat the oven to          -> Preheat the oven to 175 degrees and grease a baking tray and drizzle with oil.
Bring a large pot of         -> Bring a large pot of salted water to a boil, then reduce the heat and add the chicken.
Let the dough                -> Let the dough in a large bowl and mix well.
```

## Limitations
- **Small corpus (117 steps).** The trigram model picks the right next word only about 1 time in 3
  and is wrong most of the time on unseen steps. It beats the unigram baseline by a wide margin, though.
- **Sparsity:** the trigram has better accuracy than the bigram but worse perplexity, because many
  trigram contexts are never seen in such a small corpus. More data would fix this.
- **No understanding of cooking.** It only learns word patterns, so completions can be locally fluent
  but illogical (e.g. "Let the dough in a large bowl and mix well").
- Unknown words in your input are ignored and the model backs off to shorter contexts.
- Greedy decoding favors the most common phrases, so output can feel repetitive; use `--sample` for variety.

## Tests
```
pytest
```
