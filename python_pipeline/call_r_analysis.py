import os
import shutil
import subprocess
import glob


def find_rscript_exe():
    # Windows PATH can be annoying sometimes, so we try a couple ways to find Rscript.

    # First try whatever is already in PATH
    rscript = shutil.which("Rscript") or shutil.which("Rscript.exe")
    if rscript:
        return rscript

    # If that didn't work, check the common install folder
    # Example: C:\Program Files\R\R-4.5.2\bin\Rscript.exe
    possible = glob.glob(r"C:\Program Files\R\R-*\bin\Rscript.exe")
    if possible:
        possible.sort()  # usually newest ends up last
        return possible[-1]

    return None


def run_r_step(r_script_path, counts_path, metadata_path, out_dir):
    # This runs the main R analysis script and saves results into the run folder.
    os.makedirs(out_dir, exist_ok=True)

    rscript_exe = find_rscript_exe()
    if not rscript_exe:
        # This error message is meant to be readable for "future me"
        raise FileNotFoundError(
            "Could not find Rscript.exe. Make sure R is installed and added to PATH.\n"
            "Try: Rscript --version"
        )

    cmd = [
        rscript_exe,
        r_script_path,
        "--counts", counts_path,
        "--meta", metadata_path,
        "--out", out_dir
    ]

    # Debug print so I can copy/paste the command if R fails
    print("[INFO] Running R command:")
    print("       " + " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        # Print both stdout and stderr so we can see what R complained about
        raise RuntimeError(
            "R analysis step failed.\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}\n"
        )
