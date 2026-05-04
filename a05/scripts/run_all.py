"""
Analysis 05 - Run All: Disease-Mechanism Coupling
==================================================
Orchestrates all steps in sequence with timing.
"""

import os
import sys
import time
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ('s01_contingency.py', 'Contingency tables & coupling metrics'),
    ('s02_tautology_check.py', 'Tautology check'),
    ('s03_visualize.py', 'Visualization'),
]


def run_step(script_name, description):
    """Run a single step script and return elapsed time."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n{'='*60}")
    print(f"Running: {script_name} — {description}")
    print('='*60)

    t0 = time.time()
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=SCRIPTS_DIR,
        capture_output=False
    )
    elapsed = time.time() - t0

    if result.returncode != 0:
        print(f"\nERROR: {script_name} exited with code {result.returncode}")
        sys.exit(result.returncode)

    print(f"\nCompleted in {elapsed:.1f}s")
    return elapsed


def main():
    print("=" * 60)
    print("Analysis 05: Disease-Mechanism Coupling — Full Pipeline")
    print("=" * 60)

    total_t0 = time.time()
    timings = []

    for script_name, description in STEPS:
        elapsed = run_step(script_name, description)
        timings.append((script_name, elapsed))

    total_elapsed = time.time() - total_t0

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for script_name, elapsed in timings:
        print(f"  {script_name:<30s} {elapsed:>6.1f}s")
    print(f"  {'TOTAL':<30s} {total_elapsed:>6.1f}s")
    print("\nAll steps completed successfully.")


if __name__ == '__main__':
    main()
