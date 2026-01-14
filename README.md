# Gene Expression Project (Python + R)

This is a student-level bioinformatics + machine learning pipeline.

The idea is:
- Use **R** for gene expression differential analysis (DESeq2 style)
- Use **Python** for machine learning, evaluation, and pipeline orchestration

Right now the R step is a placeholder so the project runs end-to-end.
Later I plan to replace it with real DESeq2.

## What it does
1. Loads gene expression counts + sample metadata
2. Runs an R analysis step that outputs a DE results table + plots
3. Trains a simple ML model (logistic regression) to predict `control` vs `disease`
4. Saves outputs into a run folder like `results/run_001/`

## Why I built it
I wanted a project that shows:
- bioinformatics workflow skills (counts, metadata, DE-style outputs)
- machine learning skills (feature selection + classification)
- software engineering habits (organized repo, reproducible runs, clear scripts)

## How to run

### 1) Install Python dependencies
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
