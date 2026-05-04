"""
s01_profiles.py — Build proportional and count profiles for each site × disease/mechanism category.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    # Load data
    combined = pd.read_csv(os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'combined_data.csv'))
    disease_dict = pd.read_csv(os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'disease_dictionary.csv'))
    mechanism_dict = pd.read_csv(os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'mechanism_dictionary.csv'))

    # Merge disease category (dictionary uses 'disease_string', combined uses 'Disease')
    combined = combined.merge(
        disease_dict[['disease_string', 'level_7']].drop_duplicates(),
        left_on='Disease', right_on='disease_string', how='left'
    ).rename(columns={'level_7': 'disease_category'}).drop(columns=['disease_string'])

    # Merge mechanism category (dictionary uses 'mechanism_string', combined uses 'Mechanism')
    combined = combined.merge(
        mechanism_dict[['mechanism_string', 'level_8']].drop_duplicates(),
        left_on='Mechanism', right_on='mechanism_string', how='left'
    ).rename(columns={'level_8': 'mechanism_category'}).drop(columns=['mechanism_string'])

    # Filter to target sites
    combined = combined[combined['Site'].isin(SITES)].copy()

    # Print per-site record counts
    print("Per-site record counts:")
    site_counts = combined.groupby('Site').size()
    for site in SITES:
        count = site_counts.get(site, 0)
        print(f"  {site}: {count}")
    print(f"  Total: {site_counts.sum()}")

    # --- Disease profiles ---
    disease_data = combined[['Site', 'disease_category']].dropna(subset=['disease_category'])
    n_disease_total = len(combined[combined['Site'].isin(SITES)])
    n_disease_excl = disease_data[disease_data['disease_category'] == 'Other'].shape[0]
    disease_data = disease_data[disease_data['disease_category'] != 'Other']
    print(f"\nDisease: excluded {n_disease_excl} 'Other' records ({100*n_disease_excl/n_disease_total:.1f}%)")

    disease_counts = disease_data.groupby(['Site', 'disease_category']).size().unstack(fill_value=0)
    disease_counts = disease_counts.reindex(SITES, fill_value=0)
    disease_profiles = disease_counts.div(disease_counts.sum(axis=1), axis=0).fillna(0)

    disease_counts.index.name = 'Site'
    disease_profiles.index.name = 'Site'
    disease_counts.to_csv(os.path.join(OUTPUT_DIR, 'disease_counts.csv'))
    disease_profiles.to_csv(os.path.join(OUTPUT_DIR, 'disease_profiles.csv'))

    # --- Mechanism profiles ---
    mechanism_data = combined[['Site', 'mechanism_category']].dropna(subset=['mechanism_category'])
    n_mech_total = len(combined[combined['Site'].isin(SITES)])
    exclude_mechs = ['Other', 'Unknown']
    n_mech_excl = mechanism_data[mechanism_data['mechanism_category'].isin(exclude_mechs)].shape[0]
    mechanism_data = mechanism_data[~mechanism_data['mechanism_category'].isin(exclude_mechs)]
    print(f"Mechanism: excluded {n_mech_excl} 'Other'/'Unknown' records ({100*n_mech_excl/n_mech_total:.1f}%)")

    mechanism_counts = mechanism_data.groupby(['Site', 'mechanism_category']).size().unstack(fill_value=0)
    mechanism_counts = mechanism_counts.reindex(SITES, fill_value=0)
    mechanism_profiles = mechanism_counts.div(mechanism_counts.sum(axis=1), axis=0).fillna(0)

    mechanism_counts.index.name = 'Site'
    mechanism_profiles.index.name = 'Site'
    mechanism_counts.to_csv(os.path.join(OUTPUT_DIR, 'mechanism_counts.csv'))
    mechanism_profiles.to_csv(os.path.join(OUTPUT_DIR, 'mechanism_profiles.csv'))

    print("\nDisease profile shape:", disease_profiles.shape)
    print("Mechanism profile shape:", mechanism_profiles.shape)
    print("\nDone. Saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
