# Gene Expression Project (Python + R)

This project is a gene expression analysis pipeline that combines R and Python in a single, reproducible workflow.

The idea is:
- Use R for gene expression differential analysis (DESeq2 style)
- Use Python for machine learning, evaluation, and pipeline orchestration

Right now the R step is a placeholder so the project runs end-to-end.
Later I am thinking to replace it with proper DESeq2.

## What it does
1. Loads gene expression counts + sample metadata
2. Runs an R analysis step that outputs a DE results table + plots
3. Trains a simple ML model to predict `control` vs `disease`
4. Saves outputs into a run folder like `results/run_001/`

## Why I built it
I wanted a project that shows:
- bioinformatics workflow skills
- machine learning skills
- software engineering habits

## How to run

## Install Python dependencies
bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
