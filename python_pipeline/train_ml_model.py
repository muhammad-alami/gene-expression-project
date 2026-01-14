import os
import json

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix


def train_required_ml(counts_df, meta_df, deseq_results_path, out_dir, top_n, test_size, random_state):
    # Trained the model to classify control vs disease using top genes from DE results.

    de_results = pd.read_csv(deseq_results_path)

    gene_col = "gene_id"
    if gene_col not in de_results.columns:
        raise ValueError("deseq2_results.csv must have a 'gene_id' column.")

    # Decides which genes we will use as ML features
    # The R script already sorts the results, so we just take the first top_n genes.
    top_n = int(top_n)
    top_gene_series = de_results[gene_col].head(top_n)
    top_gene_list = top_gene_series.tolist()

    
    counts_by_gene = counts_df.set_index(gene_col)

    
    usable_genes = []
    for g in top_gene_list:
        if g in counts_by_gene.index:
            usable_genes.append(g)

    if len(usable_genes) < 2:
        raise ValueError("Not enough overlapping genes between counts and DE results.")

    
    gene_subset = counts_by_gene.loc[usable_genes]
    X_df = gene_subset.T

    # Build y labels
    sample_ids = X_df.index.tolist()

    sample_to_condition = dict(zip(meta_df["sample_id"], meta_df["condition"]))

    y_labels_text = []
    for sid in sample_ids:
        y_labels_text.append(sample_to_condition[sid])

    # Converts label for sklearn
    classes = sorted(meta_df["condition"].unique().tolist())
    if len(classes) != 2:
        raise ValueError(f"Expected 2 conditions. Found: {classes}")

    label_to_int = {classes[0]: 0, classes[1]: 1}

    y = []
    for label in y_labels_text:
        y.append(label_to_int[label])
    y = np.array(y)

    # Split into train/test sets
    test_size = float(test_size)
    random_state = int(random_state)

    X_values = X_df.values

    X_train, X_test, y_train, y_test = train_test_split(
        X_values,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    # Train a simple model
    scaler = StandardScaler()
    classifier = LogisticRegression(max_iter=2000)

    model = Pipeline([
        ("scaler", scaler),
        ("clf", classifier)
    ])

    model.fit(X_train, y_train)

    # Evaluate
    test_probs = model.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= 0.5).astype(int)

    acc = accuracy_score(y_test, test_preds)
    auc = roc_auc_score(y_test, test_probs)
    cm = confusion_matrix(y_test, test_preds)

    metrics = {
        "model": "logistic_regression",
        "n_features": int(X_df.shape[1]),
        "accuracy": float(acc),
        "roc_auc": float(auc),
        "confusion_matrix": cm.tolist(),
        "label_mapping": label_to_int
    }

    # Saves outputs
    os.makedirs(out_dir, exist_ok=True)

    metrics_file = os.path.join(out_dir, "ml_metrics.json")
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # gene coefficients
    coef_values = model.named_steps["clf"].coef_[0]

    coef_table = pd.DataFrame({
        "gene_id": usable_genes,
        "coefficient": coef_values
    })

    coef_table_sorted = coef_table.sort_values("coefficient", ascending=False)
    coef_out_path = os.path.join(out_dir, "top_ml_genes.csv")
    coef_table_sorted.to_csv(coef_out_path, index=False)
