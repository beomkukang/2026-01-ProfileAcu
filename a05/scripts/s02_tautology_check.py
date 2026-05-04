"""
Analysis 05 - Step 02: Tautology Check
=======================================
Tests whether disease-mechanism coupling is inflated by tautological pairs
(e.g., Pain studies that investigate Analgesic mechanisms).

Computes NMI with/without tautological records and performs Mantel tests on
RDMs derived from disease and mechanism profiles.
"""

import os
import numpy as np
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score
from scipy.spatial.distance import pdist, squareform, cosine
from itertools import combinations

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']

# Tautological pairs: (disease_category, mechanism_category)
TAUTOLOGICAL_PAIRS = [
    ('Pain', 'Analgesic/Opioid'),
    ('Pain', 'Ion Channel/Pain Transduction'),
    ('Neurological', 'Neuroprotective'),
    ('Neurological', 'Neural Circuit/Connectivity'),
    ('Gastrointestinal', 'Gut-Brain/Enteric'),
    ('Immune/Inflammatory', 'Inflammatory/Immune'),
    ('Metabolic/Endocrine', 'Metabolic Pathway'),
]


def load_data():
    """Load combined data merged with dictionaries."""
    combined_path = os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'combined_data.csv')
    disease_dict_path = os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'disease_dictionary.csv')
    mechanism_dict_path = os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'mechanism_dictionary.csv')

    combined = pd.read_csv(combined_path)
    disease_dict = pd.read_csv(disease_dict_path)
    mechanism_dict = pd.read_csv(mechanism_dict_path)

    # Merge disease categories
    if 'level_7' in disease_dict.columns:
        disease_map = disease_dict[['disease_string', 'level_7']].drop_duplicates()
        disease_map = disease_map.rename(columns={'level_7': 'disease_category'})
    else:
        level_cols = [c for c in disease_dict.columns if c.startswith('level_')]
        disease_map = disease_dict[['disease_string', level_cols[-1]]].drop_duplicates()
        disease_map = disease_map.rename(columns={level_cols[-1]: 'disease_category'})

    # Merge mechanism categories
    if 'level_8' in mechanism_dict.columns:
        mech_map = mechanism_dict[['mechanism_string', 'level_8']].drop_duplicates()
        mech_map = mech_map.rename(columns={'level_8': 'mechanism_category'})
    else:
        level_cols = [c for c in mechanism_dict.columns if c.startswith('level_')]
        mech_map = mechanism_dict[['mechanism_string', level_cols[-1]]].drop_duplicates()
        mech_map = mech_map.rename(columns={level_cols[-1]: 'mechanism_category'})

    df = combined.merge(disease_map, left_on='Disease', right_on='disease_string', how='left')
    df = df.merge(mech_map, left_on='Mechanism', right_on='mechanism_string', how='left')

    # Exclude "Other" disease, "Other" mechanism, "Unknown" mechanism
    df = df[~df['disease_category'].isin(['Other'])]
    df = df[~df['mechanism_category'].isin(['Other', 'Unknown'])]
    df = df.dropna(subset=['disease_category', 'mechanism_category'])

    return df


def is_tautological(row):
    """Check if a record is a tautological pair."""
    pair = (row['disease_category'], row['mechanism_category'])
    return pair in TAUTOLOGICAL_PAIRS


def compute_nmi_comparison(df):
    """Compute NMI with and without tautological records for each site."""
    rows = []

    for site in SITES:
        site_df = df[df['Site'] == site].copy()
        if len(site_df) == 0:
            continue

        # Flag tautological records
        site_df['is_tautological'] = site_df.apply(is_tautological, axis=1)
        n_taut = site_df['is_tautological'].sum()
        n_total = len(site_df)

        # NMI with all records
        nmi_all = normalized_mutual_info_score(
            site_df['disease_category'].values,
            site_df['mechanism_category'].values
        )

        # NMI excluding tautological records
        non_taut_df = site_df[~site_df['is_tautological']]
        if len(non_taut_df) > 10:
            nmi_excl = normalized_mutual_info_score(
                non_taut_df['disease_category'].values,
                non_taut_df['mechanism_category'].values
            )
        else:
            nmi_excl = np.nan

        # Relative change
        if nmi_all > 0:
            pct_change = (nmi_excl - nmi_all) / nmi_all * 100
        else:
            pct_change = np.nan

        rows.append({
            'site': site,
            'n_total': n_total,
            'n_tautological': n_taut,
            'pct_tautological': round(n_taut / n_total * 100, 1),
            'NMI_all': round(nmi_all, 4),
            'NMI_excl_tautology': round(nmi_excl, 4) if not np.isnan(nmi_excl) else np.nan,
            'NMI_pct_change': round(pct_change, 2) if not np.isnan(pct_change) else np.nan,
        })

        print(f"  {site}: NMI_all={nmi_all:.4f}, NMI_excl={nmi_excl:.4f}, "
              f"taut={n_taut}/{n_total} ({n_taut/n_total*100:.1f}%)")

    return pd.DataFrame(rows)


def build_profile_matrix(df, row_var, col_var):
    """Build a profile matrix: rows = unique values of row_var, cols = unique values of col_var."""
    ct = pd.crosstab(df[row_var], df[col_var])
    # Normalize rows to proportions
    row_sums = ct.sum(axis=1)
    profile = ct.div(row_sums, axis=0)
    return profile


def compute_rdm(profile_matrix):
    """Compute RDM (cosine distance) from profile matrix."""
    if len(profile_matrix) < 2:
        return None, None
    distances = pdist(profile_matrix.values, metric='cosine')
    labels = profile_matrix.index.tolist()
    return squareform(distances), labels


def mantel_test(rdm1, rdm2, n_permutations=9999):
    """
    Mantel test: correlation between two distance matrices.
    Returns observed r and p-value.
    """
    if rdm1 is None or rdm2 is None:
        return np.nan, np.nan

    n = rdm1.shape[0]
    if n < 3:
        return np.nan, np.nan

    # Extract upper triangle
    idx = np.triu_indices(n, k=1)
    v1 = rdm1[idx]
    v2 = rdm2[idx]

    # Handle constant vectors
    if np.std(v1) == 0 or np.std(v2) == 0:
        return np.nan, np.nan

    # Observed correlation
    r_obs = np.corrcoef(v1, v2)[0, 1]

    # Permutation test
    count = 0
    for _ in range(n_permutations):
        perm = np.random.permutation(n)
        rdm2_perm = rdm2[np.ix_(perm, perm)]
        v2_perm = rdm2_perm[idx]
        r_perm = np.corrcoef(v1, v2_perm)[0, 1]
        if r_perm >= r_obs:
            count += 1

    p_value = (count + 1) / (n_permutations + 1)
    return r_obs, p_value


def compute_mantel_comparison(df):
    """
    Compute disease & mechanism RDMs with/without tautological records.
    Mantel test comparing the two versions.
    """
    rows = []

    for site in SITES:
        site_df = df[df['Site'] == site].copy()
        if len(site_df) < 10:
            continue

        site_df['is_tautological'] = site_df.apply(is_tautological, axis=1)
        non_taut_df = site_df[~site_df['is_tautological']]

        if len(non_taut_df) < 10:
            continue

        # Disease RDMs (profiles over mechanism categories)
        disease_profile_all = build_profile_matrix(site_df, 'disease_category', 'mechanism_category')
        disease_profile_excl = build_profile_matrix(non_taut_df, 'disease_category', 'mechanism_category')

        # Align to common diseases
        common_diseases = sorted(set(disease_profile_all.index) & set(disease_profile_excl.index))
        if len(common_diseases) < 3:
            continue

        # Align columns
        all_mechs = sorted(set(disease_profile_all.columns) | set(disease_profile_excl.columns))
        dp_all = disease_profile_all.reindex(index=common_diseases, columns=all_mechs, fill_value=0)
        dp_excl = disease_profile_excl.reindex(index=common_diseases, columns=all_mechs, fill_value=0)

        rdm_all, _ = compute_rdm(dp_all)
        rdm_excl, _ = compute_rdm(dp_excl)

        # Mantel test: how similar are the two disease RDMs?
        r_disease, p_disease = mantel_test(rdm_all, rdm_excl, n_permutations=999)

        # Mechanism RDMs (profiles over disease categories)
        mech_profile_all = build_profile_matrix(site_df, 'mechanism_category', 'disease_category')
        mech_profile_excl = build_profile_matrix(non_taut_df, 'mechanism_category', 'disease_category')

        common_mechs = sorted(set(mech_profile_all.index) & set(mech_profile_excl.index))
        if len(common_mechs) < 3:
            continue

        all_diseases = sorted(set(mech_profile_all.columns) | set(mech_profile_excl.columns))
        mp_all = mech_profile_all.reindex(index=common_mechs, columns=all_diseases, fill_value=0)
        mp_excl = mech_profile_excl.reindex(index=common_mechs, columns=all_diseases, fill_value=0)

        rdm_m_all, _ = compute_rdm(mp_all)
        rdm_m_excl, _ = compute_rdm(mp_excl)

        r_mechanism, p_mechanism = mantel_test(rdm_m_all, rdm_m_excl, n_permutations=999)

        rows.append({
            'site': site,
            'mantel_r_disease_RDM': round(r_disease, 4) if not np.isnan(r_disease) else np.nan,
            'mantel_p_disease_RDM': round(p_disease, 4) if not np.isnan(p_disease) else np.nan,
            'mantel_r_mechanism_RDM': round(r_mechanism, 4) if not np.isnan(r_mechanism) else np.nan,
            'mantel_p_mechanism_RDM': round(p_mechanism, 4) if not np.isnan(p_mechanism) else np.nan,
        })

        print(f"  {site}: disease_RDM r={r_disease:.4f} (p={p_disease:.4f}), "
              f"mechanism_RDM r={r_mechanism:.4f} (p={p_mechanism:.4f})")

    return pd.DataFrame(rows)


def main():
    print("=" * 60)
    print("A05 Step 02: Tautology Check")
    print("=" * 60)

    np.random.seed(42)

    # Load data
    df = load_data()
    print(f"Loaded {len(df)} records after filtering\n")

    # NMI comparison
    print("NMI with/without tautological pairs:")
    tautology_df = compute_nmi_comparison(df)

    csv_path = os.path.join(OUTPUT_DIR, 'tautology_check.csv')
    tautology_df.to_csv(csv_path, index=False)
    print(f"\nSaved: {csv_path}")

    # Mantel test
    print("\nMantel tests (RDM stability after removing tautological records):")
    mantel_df = compute_mantel_comparison(df)

    mantel_path = os.path.join(OUTPUT_DIR, 'tautology_mantel.csv')
    mantel_df.to_csv(mantel_path, index=False)
    print(f"Saved: {mantel_path}")

    print("\nDone.")


if __name__ == '__main__':
    main()
