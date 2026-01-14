import os


def make_folder(path):
    # This makes sure a folder exists (if it already exists, it's fine)
    os.makedirs(path, exist_ok=True)


def get_next_run_folder(results_dir):
    """
    Makes a new run folder like:
      results/run_001
      results/run_002
    so each pipeline run saves outputs separately.
    """
    make_folder(results_dir)

    # Look for folders that start with "run_"
    existing = []
    for name in os.listdir(results_dir):
        if name.startswith("run_"):
            # name might be run_001, run_002, etc.
            parts = name.split("_")
            if len(parts) == 2 and parts[1].isdigit():
                existing.append(int(parts[1]))

    # Pick the next number
    next_num = max(existing) + 1 if existing else 1
    run_name = f"run_{next_num:03d}"

    run_path = os.path.join(results_dir, run_name)
    make_folder(run_path)

    return run_path