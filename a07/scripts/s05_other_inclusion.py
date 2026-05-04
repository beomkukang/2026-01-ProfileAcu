"""
Step 5: Other-inclusion sensitivity analysis.
Recompute profiles WITH "Other" disease category included (still exclude Unknown mechanisms).
Compare to original Mantel r from a04.
"""
import numpy as np
import pandas as pd
import os
from scipy.stats import spearmanr
from scipy.spatial.distance import squareform, pdist

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
INPUT_DIR = os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables')
A04_DIR = os.path.join(PROJECT_DIR, 'a04', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


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


def build_profiles_with_other(records_df, disease_col, mechanism_col, sites):
    """
    Build proportional profiles INCLUDING "Other" disease but excluding "Unknown".
    Still exclude "Unknown" mechanisms.
    """
    # For disease: include Other, exclude Unknown
    df_disease = records_df[~records_df[disease_col].isin(['Unknown'])].copy()
    # For mechanism: exclude both Other and Unknown
    df_mechanism = records_df[~records_df[mechanism_col].isin(['Other', 'Unknown'])].copy()

    disease_cats = sorted(df_disease[disease_col].unique())
    mechanism_cats = sorted(df_mechanism[mechanism_col].unique())

    disease_profile = np.zeros((len(sites), len(disease_cats)))
    mechanism_profile = np.zeros((len(sites), len(mechanism_cats)))

    for i, site in enumerate(sites):
        site_disease = df_disease[df_disease['Site'] == site]
        site_mechanism = df_mechanism[df_mechanism['Site'] == site]

        for j, cat in enumerate(disease_cats):
            disease_profile[i, j] = (site_disease[disease_col] == cat).sum()
        if site_disease.shape[0] > 0:
            disease_profile[i, :] /= site_disease.shape[0]

        for j, cat in enumerate(mechanism_cats):
            mechanism_profile[i, j] = (site_mechanism[mechanism_col] == cat).sum()
        if site_mechanism.shape[0] > 0:
            mechanism_profile[i, :] /= site_mechanism.shape[0]

    return disease_profile, mechanism_profile


def main():
    print("Loading data...")
    combined = pd.read_csv(os.path.join(INPUT_DIR, 'combined_data.csv'))
    disease_dict = pd.read_csv(os.path.join(INPUT_DIR, 'disease_dictionary.csv'))
    mechanism_dict = pd.read_csv(os.path.join(INPUT_DIR, 'mechanism_dictionary.csv'))

    disease_map = dict(zip(disease_dict['disease_string'], disease_dict['level_7']))
    mechanism_map = dict(zip(mechanism_dict['mechanism_string'], mechanism_dict['level_8']))

    combined['disease_cat'] = combined['Disease'].map(disease_map)
    combined['mechanism_cat'] = combined['Mechanism'].map(mechanism_map)

    # Load original Mantel r from a04 if available
    original_r = None
    original_p = None
    mantel_path = os.path.join(A04_DIR, 'mantel_results.csv')
    if os.path.exists(mantel_path):
        mantel_df = pd.read_csv(mantel_path)
        # Look for disease-mechanism row
        dm_row = mantel_df[
            mantel_df.apply(lambda row: 'disease' in str(row).lower() and 'mechanism' in str(row).lower(), axis=1)
        ]
        if len(dm_row) > 0:
            original_r = dm_row.iloc[0].get('mantel_r', dm_row.iloc[0].get('r', None))
            original_p = dm_row.iloc[0].get('p_value', dm_row.iloc[0].get('p', None))

    if original_r is None:
        print("  WARNING: Could not load original Mantel r from a04. Computing from scratch.")
        # Compute original (excluding Other and Unknown)
        from s01_leave_one_out import build_profiles
        disease_profile_orig, mechanism_profile_orig = build_profiles(
            combined, 'disease_cat', 'mechanism_cat', SITES
        )
        disease_rdm_orig = squareform(pdist(disease_profile_orig, metric='cosine'))
        mechanism_rdm_orig = squareform(pdist(mechanism_profile_orig, metric='cosine'))
        disease_rdm_orig = np.nan_to_num(disease_rdm_orig)
        mechanism_rdm_orig = np.nan_to_num(mechanism_rdm_orig)
        original_r, original_p = mantel_test(disease_rdm_orig, mechanism_rdm_orig, n_perms=10000)

    print(f"  Original Mantel r: {original_r:.4f}, p: {original_p}")

    # Compute with Other included
    print("  Computing with Other included...")
    disease_profile, mechanism_profile = build_profiles_with_other(
        combined, 'disease_cat', 'mechanism_cat', SITES
    )

    disease_rdm = squareform(pdist(disease_profile, metric='cosine'))
    mechanism_rdm = squareform(pdist(mechanism_profile, metric='cosine'))

    disease_rdm = np.nan_to_num(disease_rdm)
    mechanism_rdm = np.nan_to_num(mechanism_rdm)

    r_other, p_other = mantel_test(disease_rdm, mechanism_rdm, n_perms=10000)

    results = pd.DataFrame([
        {'condition': 'original', 'mantel_r': original_r, 'p_value': original_p},
        {'condition': 'other_included', 'mantel_r': r_other, 'p_value': p_other}
    ])

    out_path = os.path.join(OUTPUT_DIR, 'other_inclusion.csv')
    results.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    print(results.to_string(index=False))


if __name__ == '__main__':
    main()
