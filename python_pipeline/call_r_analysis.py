import os
import shutil
import subprocess
import glob


def find_rscript_exe():
    rscript = shutil.which("Rscript") or shutil.which("Rscript.exe")
    if rscript:
        return rscript
    possible = glob.glob(r"C:\Program Files\R\R-*\bin\Rscript.exe")
    if possible:
        possible.sort()  # usually newest ends up last
        return possible[-1]

    return None


def run_r_step(r_script_path, counts_path, metadata_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    rscript_exe = find_rscript_exe()
    if not rscript_exe:
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

    # Debug print
    print("[INFO] Running R command:")
    print("       " + " ".join(cmd))

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(
            "R analysis step failed.\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}\n"
        )
