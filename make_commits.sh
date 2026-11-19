#!/usr/bin/env bash
# Run once inside the unzipped folder to create one commit per milestone.
set -e
git init -b main
git add .gitignore requirements.txt .env.example .github
git commit -m "Start recipe-step-autocompleter project skeleton"
git add data/recipes.txt app/__init__.py tests/__init__.py
git commit -m "Milestone 1: compile corpus of recipe instructions"
git add app/preprocess.py tests/test_preprocess.py
git commit -m "Milestone 2: clean and tokenize recipe text"
git add app/ngram.py tests/test_ngram.py
git commit -m "Milestone 3: n-gram counts, MLE probabilities, add-k smoothing and backoff"
git add app/generate.py tests/test_generate.py
git commit -m "Milestone 4: generate recipe step continuations"
git add app/cli.py tests/test_cli.py
git commit -m "Milestone 5: command-line interface"
git add README.md
git commit -m "Add README with setup and usage"
git log --oneline
echo "Now: git remote add origin https://github.com/YOUR-USERNAME/recipe-step-autocompleter.git && git push -u origin main"
