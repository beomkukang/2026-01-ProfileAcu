"""
Orchestrator: Run all Analysis 01 scripts sequentially.
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
    ('s00_clean_base_data.py', 'Cleaning base data (typos, case normalization)'),
    ('s01_load_combine.py', 'Loading and combining data'),
    ('s02_disease_taxonomy.py', 'Building disease taxonomy'),
    ('s03_mechanism_taxonomy.py', 'Building mechanism taxonomy'),
    ('s04_compute_rdms.py', 'Computing RDMs'),
    ('s05_stability_analysis.py', 'Running stability analysis'),
    ('s06_visualize.py', 'Generating visualizations'),
]


def main():
    print("=" * 60)
    print("Analysis 01: Taxonomy Optimization Pipeline")
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
