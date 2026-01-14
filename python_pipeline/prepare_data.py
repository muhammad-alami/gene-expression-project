import pandas as pd


def load_and_check_data(counts_path, metadata_path):
    counts_df = pd.read_csv(counts_path)
    meta_df = pd.read_csv(metadata_path)
    
    if "gene_id" not in counts_df.columns:
        raise ValueError("expression_counts.csv must have a column named 'gene_id'.")

    if "sample_id" not in meta_df.columns or "condition" not in meta_df.columns:
        raise ValueError("sample_metadata.csv must have columns: sample_id, condition")

    # except gene_id for the sample columns
    sample_cols = [c for c in counts_df.columns if c != "gene_id"]

    
    meta_samples = meta_df["sample_id"].tolist()

    missing_in_meta = sorted(list(set(sample_cols) - set(meta_samples)))
    missing_in_counts = sorted(list(set(meta_samples) - set(sample_cols)))

    if missing_in_meta:
        raise ValueError(f"These sample columns are missing from metadata: {missing_in_meta}")

    if missing_in_counts:
        raise ValueError(f"These metadata sample_ids are missing from counts: {missing_in_counts}")

    # I am doing exactly 2 groups for now, I am gonna stick with control vs disease
    conditions = meta_df["condition"].unique().tolist()
    if len(conditions) != 2:
        raise ValueError(
            f"For this version, expected exactly 2 conditions (like control/disease). Found: {conditions}"
        )

    # Make sure counts are numeric and not negative
    counts_only = counts_df[sample_cols]

    # Convert to numbers (if someone accidentally saved as strings)
    counts_df[sample_cols] = counts_only.apply(pd.to_numeric, errors="raise")

    if (counts_df[sample_cols] < 0).any().any():
        raise ValueError("Counts must be non-negative numbers.")

    return counts_df, meta_df
