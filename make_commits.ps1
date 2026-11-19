
$ErrorActionPreference = "Stop"

# Initialize Git repository
git init -b main
if ($LASTEXITCODE -ne 0) { throw "Git init failed" }

# Initial project skeleton
git add .gitignore requirements.txt .env.example .github
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Start recipe-step-autocompleter project skeleton"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# Milestone 1
git add data/recipes.txt app/__init__.py tests/__init__.py
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Milestone 1: compile corpus of recipe instructions"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# Milestone 2
git add app/preprocess.py tests/test_preprocess.py
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Milestone 2: clean and tokenize recipe text"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# Milestone 3
git add app/ngram.py tests/test_ngram.py
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Milestone 3: n-gram counts, MLE probabilities, add-k smoothing and backoff"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# Milestone 4
git add app/generate.py tests/test_generate.py
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Milestone 4: generate recipe step continuations"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# Milestone 5
git add app/cli.py tests/test_cli.py
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Milestone 5: command-line interface"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# README
git add README.md
if ($LASTEXITCODE -ne 0) { throw "Git add failed" }
git commit -m "Add README with setup and usage"
if ($LASTEXITCODE -ne 0) { throw "Git commit failed" }

# Display commit history
git log --oneline

Write-Host "`nAll commits created successfully!"
Write-Host "Next, connect your GitHub repository using:"
Write-Host "git remote add origin https://github.com/YOUR-USERNAME/recipe-step-autocompleter.git"
Write-Host "git push -u origin main"
