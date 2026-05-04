"""
Orchestrator: Run all Analysis 06 scripts sequentially.
"""
import os
import sys
import time
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

# Ensure output directories exist
os.makedirs(os.path.join(BASE_DIR, 'results', 'datatables'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'results', 'figures'), exist_ok=True)

SCRIPTS = [
    ('s01_mds.py', 'Classical MDS on cosine distance matrices'),
    ('s02_pca.py', 'PCA on proportional profiles'),
    ('s03_ca_biplot.py', 'Correspondence Analysis biplot'),
    ('s04_bootstrap.py', 'Bootstrap confidence ellipses'),
    ('s05_gv4_exclusion.py', 'GV4 exclusion sensitivity analysis'),
    ('s06_visualize.py', 'Generating visualizations'),
]


def main():
    print("=" * 60)
    print("Analysis 06: Dimensionality Reduction Pipeline")
    print("=" * 60)

    total_start = time.time()

    for script, description in SCRIPTS:
        print(f"\n{'─' * 60}")
        print(f"▶ Step: {description}")
        print(f"  Script: {script}")
        print(f"{'─' * 60}")

        start = time.time()
        result = subprocess.run(
            [sys.executable, os.path.join(SCRIPT_DIR, script)],
            capture_output=False,
            cwd=SCRIPT_DIR
        )

        elapsed = time.time() - start
        if result.returncode != 0:
            print(f"\n✗ FAILED: {script} (exit code {result.returncode})")
            sys.exit(1)
        print(f"  ✓ Completed in {elapsed:.1f}s")

    total_elapsed = time.time() - total_start
    print(f"\n{'=' * 60}")
    print(f"All steps completed in {total_elapsed:.1f}s")
    print(f"{'=' * 60}")
    print(f"\nOutputs:")
    print(f"  Tables: {os.path.join(BASE_DIR, 'results', 'datatables')}")
    print(f"  Figures: {os.path.join(BASE_DIR, 'results', 'figures')}")


if __name__ == '__main__':
    main()
