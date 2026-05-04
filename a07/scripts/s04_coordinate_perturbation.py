"""
Step 4: Coordinate perturbation sensitivity analysis.
Test somatotopic-disease and somatotopic-mechanism Mantel correlations
across 1,000 perturbed somatotopic RDMs.
"""
import numpy as np
import pandas as pd
import pickle
import os
from scipy.stats import spearmanr
from scipy.spatial.distance import squareform

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
A02_DIR = os.path.join(PROJECT_DIR, 'a02', 'results', 'datatables')
A03_DIR = os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')


def mantel_test(rdm1, rdm2, n_perms=10000):
    """Mantel test using Spearman correlation with permutation."""
    from scipy.stats import spearmanr
    from scipy.spatial.distance import squareform
    vec1 = squareform(rdm1)
    vec2 = squareform(rdm2)
    r_obs, _ = spearmanr(vec1, vec2)
    count = 0
    n = rdm1.shape[0]
    for _ in range(n_perms):
        perm = np.random.permutation(n)
        rdm2_perm = rdm2[np.ix_(perm, perm)]
        vec2_perm = squareform(rdm2_perm)
        r_perm, _ = spearmanr(vec1, vec2_perm)
        if r_perm >= r_obs:
            count += 1
    p_val = (count + 1) / (n_perms + 1)
    return r_obs, p_val


def main():
    print("Loading perturbed somatotopic RDMs...")
    with open(os.path.join(A02_DIR, 'perturbed_rdms.pkl'), 'rb') as f:
        perturbed_rdms = pickle.load(f)

    print("Loading disease and mechanism RDMs...")
    disease_rdm = pd.read_csv(os.path.join(A03_DIR, 'disease_rdm.csv'), index_col=0).values
    mechanism_rdm = pd.read_csv(os.path.join(A03_DIR, 'mechanism_rdm.csv'), index_col=0).values

    n_iterations = len(perturbed_rdms)
    print(f"Running {n_iterations} perturbation iterations...")

    results = []
    for i in range(n_iterations):
        if (i + 1) % 100 == 0:
            print(f"  Iteration {i + 1}/{n_iterations}")

        somat_rdm = perturbed_rdms[i]
        somat_rdm = np.nan_to_num(somat_rdm)

        r_disease, p_disease = mantel_test(somat_rdm, disease_rdm, n_perms=100)
        r_mechanism, p_mechanism = mantel_test(somat_rdm, mechanism_rdm, n_perms=100)

        results.append({
            'iteration': i + 1,
            'somat_disease_r': r_disease,
            'somat_disease_p': p_disease,
            'somat_mechanism_r': r_mechanism,
            'somat_mechanism_p': p_mechanism
        })

    df_results = pd.DataFrame(results)
    out_path = os.path.join(OUTPUT_DIR, 'perturbation_results.csv')
    df_results.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")

    pct_disease_sig = (df_results['somat_disease_p'] < 0.05).mean() * 100
    pct_mechanism_sig = (df_results['somat_mechanism_p'] < 0.05).mean() * 100
    print(f"Somatotopic-Disease: {pct_disease_sig:.1f}% significant (p<0.05)")
    print(f"Somatotopic-Mechanism: {pct_mechanism_sig:.1f}% significant (p<0.05)")


if __name__ == '__main__':
    main()
