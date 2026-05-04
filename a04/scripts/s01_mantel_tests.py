"""
Analysis 04 - Step 01: Mantel Tests (Simple and Partial)
Three-Space RSA: comparing Disease, Mechanism, Surface, and Segmental RDMs.

Uses exact permutation test (all 8! = 40,320 permutations) rather than
sampling, since n=8 makes exhaustive enumeration trivial. This gives
exact p-values with no Monte Carlo noise and no seed dependency.

Correlation metric: Spearman rank correlation on upper-triangle vectors
(standard in RSA literature, robust to outliers, no linearity assumption).

Partial Mantel: OLS residualization of both matrices on the control matrix,
then Spearman correlation of residuals. Permutation of site labels in the
residualized space.
"""

import os
import itertools
import numpy as np
import pandas as pd
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_DIR = os.path.dirname(BASE_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)


def load_rdm(path):
    """Load RDM from CSV with first column as index, return numpy array."""
    df = pd.read_csv(path, index_col=0)
    return df.values, list(df.index)


def upper_triangle(rdm):
    """Extract upper triangle as vector (using squareform convention)."""
    return squareform(rdm, checks=False)


def all_permutations(n):
    """Generate all n! permutations of range(n)."""
    return list(itertools.permutations(range(n)))


def mantel_test(rdm1, rdm2):
    """
    Exact Mantel test using Spearman correlation on upper-triangle vectors.
    Enumerates all n! = 40,320 permutations of rdm2 for exact p-value.
    """
    vec1 = upper_triangle(rdm1)
    vec2 = upper_triangle(rdm2)
    observed_r, _ = spearmanr(vec1, vec2)

    n = rdm1.shape[0]
    perms = all_permutations(n)

    count = 0
    for perm in perms:
        perm = list(perm)
        rdm2_perm = rdm2[np.ix_(perm, perm)]
        vec2_perm = upper_triangle(rdm2_perm)
        perm_r, _ = spearmanr(vec1, vec2_perm)
        if perm_r >= observed_r:
            count += 1

    p_value = count / len(perms)
    return observed_r, p_value, len(perms)


def partial_mantel(rdm_a, rdm_b, rdm_c):
    """
    Exact Partial Mantel test: correlation between rdm_a and rdm_b
    after controlling for rdm_c.

    Method: OLS residualize upper-triangle vectors of A and B on C,
    then Spearman correlate residuals. Permute site labels of rdm_b
    exhaustively to get exact p-value.
    """
    vec_a = upper_triangle(rdm_a)
    vec_b = upper_triangle(rdm_b)
    vec_c = upper_triangle(rdm_c)

    def get_residuals(y, x):
        """OLS residuals of y regressed on x."""
        x_design = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(x_design, y, rcond=None)[0]
        return y - x_design @ beta

    resid_a = get_residuals(vec_a, vec_c)
    resid_b = get_residuals(vec_b, vec_c)
    observed_r, _ = spearmanr(resid_a, resid_b)

    n = rdm_a.shape[0]
    perms = all_permutations(n)

    count = 0
    for perm in perms:
        perm = list(perm)
        rdm_b_perm = rdm_b[np.ix_(perm, perm)]
        vec_b_perm = upper_triangle(rdm_b_perm)
        resid_b_perm = get_residuals(vec_b_perm, vec_c)
        perm_r, _ = spearmanr(resid_a, resid_b_perm)
        if perm_r >= observed_r:
            count += 1

    p_value = count / len(perms)
    return observed_r, p_value, len(perms)


def main():
    # Load RDMs
    disease_rdm, sites = load_rdm(
        os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables', 'disease_rdm.csv'))
    mechanism_rdm, _ = load_rdm(
        os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables', 'mechanism_rdm.csv'))
    surface_rdm, _ = load_rdm(
        os.path.join(PROJECT_DIR, 'a02', 'results', 'datatables', 'surface_rdm.csv'))
    segmental_rdm, _ = load_rdm(
        os.path.join(PROJECT_DIR, 'a02', 'results', 'datatables', 'segmental_rdm.csv'))

    print(f"Sites: {sites}")
    print(f"RDM shape: {disease_rdm.shape}")
    print(f"Using exact permutation: 8! = 40,320 permutations per test")
    print()

    # --- Simple Mantel Tests ---
    simple_tests = [
        ('Disease', 'Mechanism', disease_rdm, mechanism_rdm),
        ('Disease', 'Surface Somatotopic', disease_rdm, surface_rdm),
        ('Mechanism', 'Surface Somatotopic', mechanism_rdm, surface_rdm),
        ('Disease', 'Segmental Somatotopic', disease_rdm, segmental_rdm),
        ('Mechanism', 'Segmental Somatotopic', mechanism_rdm, segmental_rdm),
    ]

    simple_results = []
    print("=== Simple Mantel Tests ===")
    for name1, name2, rdm1, rdm2 in simple_tests:
        r, p, n_perms = mantel_test(rdm1, rdm2)
        simple_results.append({
            'Test': f'{name1} vs {name2}',
            'Type': 'Simple Mantel',
            'r': r,
            'p_value': p,
            'n_permutations': n_perms,
            'significant': p < 0.05
        })
        sig = '*' if p < 0.05 else ''
        print(f"  {name1} vs {name2}: r={r:.4f}, p={p:.6f} {sig}")

    # --- Partial Mantel Tests ---
    partial_tests = [
        ('Disease', 'Mechanism', 'Surface Somatotopic',
         disease_rdm, mechanism_rdm, surface_rdm),
        ('Disease', 'Surface Somatotopic', 'Mechanism',
         disease_rdm, surface_rdm, mechanism_rdm),
        ('Mechanism', 'Surface Somatotopic', 'Disease',
         mechanism_rdm, surface_rdm, disease_rdm),
        ('Disease', 'Mechanism', 'Segmental Somatotopic',
         disease_rdm, mechanism_rdm, segmental_rdm),
        ('Disease', 'Segmental Somatotopic', 'Mechanism',
         disease_rdm, segmental_rdm, mechanism_rdm),
        ('Mechanism', 'Segmental Somatotopic', 'Disease',
         mechanism_rdm, segmental_rdm, disease_rdm),
    ]

    partial_results = []
    print("\n=== Partial Mantel Tests ===")
    for name_a, name_b, name_c, rdm_a, rdm_b, rdm_c in partial_tests:
        r, p, n_perms = partial_mantel(rdm_a, rdm_b, rdm_c)
        partial_results.append({
            'Test': f'{name_a} vs {name_b} | {name_c}',
            'Type': 'Partial Mantel',
            'r': r,
            'p_value': p,
            'n_permutations': n_perms,
            'significant': p < 0.05
        })
        sig = '*' if p < 0.05 else ''
        print(f"  {name_a} vs {name_b} | {name_c}: r={r:.4f}, p={p:.6f} {sig}")

    # Combine and save
    all_results = simple_results + partial_results
    df_results = pd.DataFrame(all_results)
    df_results.to_csv(os.path.join(OUTPUT_DIR, 'mantel_results.csv'), index=False)
    print(f"\nSaved: mantel_results.csv")

    # Table 4 format
    df_table4 = df_results[['Test', 'Type', 'r', 'p_value', 'n_permutations', 'significant']].copy()
    df_table4['r'] = df_table4['r'].round(4)
    df_table4['p_value'] = df_table4['p_value'].round(6)
    df_table4.to_csv(os.path.join(OUTPUT_DIR, 'table4_mantel.csv'), index=False)
    print(f"Saved: table4_mantel.csv")

    # Summary
    print(f"\n=== Summary ===")
    print(f"Total tests: {len(all_results)} ({len(simple_results)} simple + {len(partial_results)} partial)")
    print(f"Significant (p<0.05): {sum(1 for r in all_results if r['significant'])}")
    print(f"Permutation method: exact (all 40,320)")


if __name__ == '__main__':
    main()
