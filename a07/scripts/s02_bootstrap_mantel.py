"""
Step 2: Bootstrap confidence interval for disease-mechanism Mantel r.
1,000 iterations resampling records within each site.
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
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
N_ITERATIONS = 1000


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


def build_profiles(records_df, disease_col, mechanism_col, sites):
    """
    Build proportional profiles excluding Other and Unknown.
    Returns disease_profile (n_sites x n_disease_cats) and mechanism_profile.
    """
    df_disease = records_df[~records_df[disease_col].isin(['Other', 'Unknown'])].copy()
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

    r_values = []
    print(f"Running {N_ITERATIONS} bootstrap iterations...")
    for i in range(N_ITERATIONS):
        if (i + 1) % 100 == 0:
            print(f"  Iteration {i + 1}/{N_ITERATIONS}")

        # Resample within each site
        resampled_dfs = []
        for site in SITES:
            site_df = combined[combined['Site'] == site]
            n_site = len(site_df)
            resampled = site_df.sample(n=n_site, replace=True)
            resampled_dfs.append(resampled)
        resampled_combined = pd.concat(resampled_dfs, ignore_index=True)

        disease_profile, mechanism_profile = build_profiles(
            resampled_combined, 'disease_cat', 'mechanism_cat', SITES
        )

        disease_rdm = squareform(pdist(disease_profile, metric='cosine'))
        mechanism_rdm = squareform(pdist(mechanism_profile, metric='cosine'))

        disease_rdm = np.nan_to_num(disease_rdm)
        mechanism_rdm = np.nan_to_num(mechanism_rdm)

        r_obs, _ = mantel_test(disease_rdm, mechanism_rdm, n_perms=100)
        r_values.append(r_obs)

    r_values = np.array(r_values)
    ci_lower = np.percentile(r_values, 2.5)
    ci_upper = np.percentile(r_values, 97.5)

    # Save summary
    summary = pd.DataFrame([{
        'mean_r': np.mean(r_values),
        'median_r': np.median(r_values),
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'n_iterations': N_ITERATIONS
    }])
    out_path = os.path.join(OUTPUT_DIR, 'bootstrap_mantel_ci.csv')
    summary.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    print(summary.to_string(index=False))

    # Save distribution
    dist_df = pd.DataFrame({
        'iteration': range(1, N_ITERATIONS + 1),
        'mantel_r': r_values
    })
    dist_path = os.path.join(OUTPUT_DIR, 'bootstrap_mantel_distribution.csv')
    dist_df.to_csv(dist_path, index=False)
    print(f"Saved: {dist_path}")


if __name__ == '__main__':
    main()
