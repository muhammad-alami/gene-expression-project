import argparse
import os
import yaml

from utils import get_next_run_folder
from prepare_data import load_and_check_data
from call_r_analysis import run_r_step
from train_ml_model import train_required_ml
from evaluate_results import write_run_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    args = parser.parse_args()
    
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    counts_path = cfg["counts_path"]
    metadata_path = cfg["metadata_path"]
    results_dir = cfg["results_dir"]

    # Going to make it so that every new run a new folder is made
    run_dir = get_next_run_folder(results_dir)
    print(f"[INFO] Created run folder: {run_dir}")

    # use the load_and_check_data function I made in the "prepare_data.py" so things run smoothly
    counts_df, meta_df = load_and_check_data(counts_path, metadata_path)
    print("[INFO] Input data looks good.")

    # Run R analysis which will create deseq2_results.csv + plots
    run_r_step(cfg["r_script_path"], counts_path, metadata_path, run_dir)
    print("[INFO] R analysis finished.")

    
    deseq_results_path = os.path.join(run_dir, "deseq2_results.csv")
    if not os.path.exists(deseq_results_path):
        raise FileNotFoundError("R did not produce deseq2_results.csv. Something went wrong.")

    #  ML 
    train_required_ml(
        counts_df=counts_df,
        meta_df=meta_df,
        deseq_results_path=deseq_results_path,
        out_dir=run_dir,
        top_n=int(cfg["top_n_genes_for_ml"]),
        test_size=float(cfg["test_size"]),
        random_state=int(cfg["random_state"])
    )
    print("[INFO] ML training finished.")

    # Write a simple summary
    write_run_summary(run_dir, alpha=float(cfg["alpha"]))
    print("[DONE] Pipeline completed successfully!")


if __name__ == "__main__":
    main()
