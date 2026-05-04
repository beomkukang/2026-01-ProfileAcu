"""
Step 4: Compute RDMs at each taxonomy level combination.
Builds proportional profiles for 8 sites, computes cosine distance matrices.
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def build_profile(df, site_col, category_col, sites, exclude_cats=None):
    """Build proportional profile matrix (sites x categories)."""
    if exclude_cats is None:
        exclude_cats = set()

    filtered = df[~df[category_col].isin(exclude_cats)]
    categories = sorted([c for c in filtered[category_col].unique() if c not in exclude_cats])

    profile = np.zeros((len(sites), len(categories)))
    for i, site in enumerate(sites):
        site_data = filtered[filtered[site_col] == site]
        total = len(site_data)
        if total == 0:
            continue
        for j, cat in enumerate(categories):
            count = (site_data[category_col] == cat).sum()
            profile[i, j] = count / total

    return profile, categories


def compute_rdm(profile):
    """Compute cosine distance RDM from a profile matrix."""
    # Handle zero rows (sites with no records after filtering)
    row_sums = profile.sum(axis=1)
    if np.any(row_sums == 0):
        # Replace zero rows with uniform distribution to avoid NaN
        for i in range(len(row_sums)):
            if row_sums[i] == 0:
                profile[i, :] = 1.0 / profile.shape[1]

    sim = cosine_similarity(profile)
    rdm = 1 - sim
    np.fill_diagonal(rdm, 0)
    return rdm


def main():
    combined = pd.read_csv(os.path.join(OUTPUT_DIR, 'combined_data.csv'))
    disease_dict = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_dictionary.csv'))
    mechanism_dict = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_dictionary.csv'))

    # Detect number of levels from dictionary columns
    disease_levels = [c for c in disease_dict.columns if c.startswith('level_')]
    mechanism_levels = [c for c in mechanism_dict.columns if c.startswith('level_')]
    n_disease_levels = len(disease_levels)
    n_mechanism_levels = len(mechanism_levels)

    # Merge classifications into combined data
    combined = combined.merge(
        disease_dict[['disease_string'] + disease_levels],
        left_on='Disease', right_on='disease_string', how='left',
        suffixes=('', '_dis')
    )
    for i in range(1, n_disease_levels + 1):
        combined.rename(columns={f'level_{i}': f'disease_level_{i}'}, inplace=True)

    combined = combined.merge(
        mechanism_dict[['mechanism_string'] + mechanism_levels],
        left_on='Mechanism', right_on='mechanism_string', how='left',
        suffixes=('', '_mech')
    )
    for i in range(1, n_mechanism_levels + 1):
        combined.rename(columns={f'level_{i}': f'mechanism_level_{i}'}, inplace=True)

    # Compute RDMs for all levels
    disease_rdms = {}
    mechanism_rdms = {}
    disease_profiles = {}
    mechanism_profiles = {}

    print("Computing disease RDMs...")
    for level in range(1, n_disease_levels + 1):
        col = f'disease_level_{level}'
        profile, cats = build_profile(combined, 'Site', col, SITES, exclude_cats={'Other'})
        rdm = compute_rdm(profile.copy())
        disease_rdms[level] = rdm
        disease_profiles[level] = (profile, cats)
        print(f"  Level {level}: {len(cats)} categories, RDM shape {rdm.shape}")

    print("Computing mechanism RDMs...")
    for level in range(1, n_mechanism_levels + 1):
        col = f'mechanism_level_{level}'
        # Exclude both Other and Unknown
        profile, cats = build_profile(
            combined, 'Site', col, SITES, exclude_cats={'Other', 'Unknown'}
        )
        rdm = compute_rdm(profile.copy())
        mechanism_rdms[level] = rdm
        mechanism_profiles[level] = (profile, cats)
        print(f"  Level {level}: {len(cats)} categories, RDM shape {rdm.shape}")

    # Save RDMs
    rdm_data = {
        'disease_rdms': disease_rdms,
        'mechanism_rdms': mechanism_rdms,
        'disease_profiles': disease_profiles,
        'mechanism_profiles': mechanism_profiles,
        'sites': SITES,
    }
    rdm_path = os.path.join(OUTPUT_DIR, 'rdm_data.pkl')
    with open(rdm_path, 'wb') as f:
        pickle.dump(rdm_data, f)
    print(f"\nSaved: {rdm_path}")

    return rdm_data


if __name__ == '__main__':
    main()
