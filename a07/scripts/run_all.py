"""
Orchestrator: Run all Analysis 07 (Sensitivity and Robustness) scripts sequentially.
"""
import os
import sys
import time
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Ensure output directories exist
os.makedirs(os.path.join(BASE_DIR, 'results', 'datatables'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'results', 'figures'), exist_ok=True)

SCRIPTS = [
    ('s01_leave_one_out.py', 'Leave-one-out sensitivity analysis'),
    ('s02_bootstrap_mantel.py', 'Bootstrap confidence interval for Mantel r'),
    ('s03_subsample.py', 'Subsample sensitivity (n=22 per site)'),
    ('s04_coordinate_perturbation.py', 'Coordinate perturbation analysis'),
    ('s05_other_inclusion.py', 'Other category inclusion analysis'),
    ('s06_publication_collapse.py', 'Publication collapse analysis'),
    ('s07_visualize.py', 'Generating visualizations and summary table'),
]

# Required upstream files
UPSTREAM_FILES = [
    os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables', 'combined_data.csv'),
    os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables', 'disease_dictionary.csv'),
    os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables', 'mechanism_dictionary.csv'),
    os.path.join(PROJECT_DIR, 'a02', 'results', 'datatables', 'perturbed_rdms.pkl'),
    os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables', 'disease_rdm.csv'),
    os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables', 'mechanism_rdm.csv'),
    os.path.join(PROJECT_DIR, 'a04', 'results', 'datatables', 'mantel_results.csv'),
]


def check_upstream():
    """Check if all upstream files exist and warn if any are missing."""
    missing = []
    for fpath in UPSTREAM_FILES:
        if not os.path.exists(fpath):
            missing.append(fpath)
    if missing:
        print("WARNING: The following upstream files are missing:")
        for f in missing:
            print(f"  - {f}")
        print("Some scripts may fail or compute fallback values.\n")
    return missing


def main():
    print("=" * 60)
    print("Analysis 07: Sensitivity and Robustness")
    print("=" * 60)

    check_upstream()

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
