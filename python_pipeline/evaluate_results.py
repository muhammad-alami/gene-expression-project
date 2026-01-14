import os
import pandas as pd


def write_run_summary(run_dir, alpha):
    # Read the DE results created by the R step
    de_path = os.path.join(run_dir, "deseq2_results.csv")
    de_df = pd.read_csv(de_path)

    # Count significant genes if padj exists (in real DESeq2 it will)
    if "padj" in de_df.columns:
        sig_count = int((de_df["padj"] < alpha).sum())
    else:
        sig_count = "N/A"

    top_genes = de_df["gene_id"].head(10).tolist()

    summary_path = os.path.join(run_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("Run Summary\n")
        f.write("==========\n\n")
        f.write(f"Significant genes (padj < {alpha}): {sig_count}\n\n")
        f.write("Top 10 genes from DE results:\n")
        for g in top_genes:
            f.write(f"- {g}\n")
