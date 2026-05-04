"""
Analysis 02 - Run All Scripts
Somatotopic Coordinate Construction
Executes s01, s02, s03 sequentially.
"""

import os
import sys
import time
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

os.makedirs(os.path.join(BASE_DIR, 'results', 'datatables'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'results', 'figures'), exist_ok=True)

SCRIPTS = [
    's01_coordinates.py',
    's02_perturbation.py',
    's03_visualize.py',
]

def run_script(script_name):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True
    )
    elapsed = time.time() - t0
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        print(f"FAILED: {script_name} (exit code {result.returncode})")
        sys.exit(result.returncode)
    print(f"Completed: {script_name} ({elapsed:.1f}s)")
    return elapsed

if __name__ == '__main__':
    total_t0 = time.time()
    print("Analysis 02: Somatotopic Coordinate Construction")
    print(f"Base directory: {BASE_DIR}")

    for script in SCRIPTS:
        run_script(script)

    total_elapsed = time.time() - total_t0
    print(f"\n{'='*60}")
    print(f"All scripts completed successfully. Total time: {total_elapsed:.1f}s")
    print(f"{'='*60}")
