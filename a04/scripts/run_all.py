"""
Analysis 04 - Run All Scripts
Three-Space RSA: Mantel tests and visualization.
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def run_script(script_name):
    """Run a script and check for errors."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n{'='*60}")
    print(f"Running: {script_name}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=True, text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        print(f"ERROR in {script_name}:")
        print(result.stderr)
        sys.exit(1)

    if result.stderr:
        print(f"Warnings from {script_name}:")
        print(result.stderr)

    print(f"Completed: {script_name}")


def main():
    print("Analysis 04: Three-Space RSA")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Figures directory: {FIG_DIR}")

    # Step 1: Mantel tests
    run_script('s01_mantel_tests.py')

    # Step 2: Visualization
    run_script('s02_visualize.py')

    print(f"\n{'='*60}")
    print("Analysis 04 complete.")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
