"""
Orchestrator: Run all Analysis 03 scripts sequentially.
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
    ('s01_profiles.py', 'Building proportional profiles'),
    ('s02_bayes_factors.py', 'Computing Bayes Factors'),
    ('s03_rdms.py', 'Computing RDMs'),
    ('s04_clustering.py', 'Hierarchical clustering'),
    ('s05_within_pair.py', 'Within-pair statistical tests'),
    ('s06_record_independence.py', 'Record independence assessment'),
    ('s07_visualize.py', 'Generating visualizations (Fig 2, Fig 3, Table 3)'),
]


def main():
    print("=" * 60)
    print("Analysis 03: First-Order Characterization")
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
