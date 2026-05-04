"""
s03_rdms.py — Compute Representational Dissimilarity Matrices (cosine distance) for disease and mechanism profiles.
"""

import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def compute_rdm(profiles_df):
    """Compute cosine distance RDM (1 - cosine similarity), diagonal = 0."""
    sim = cosine_similarity(profiles_df.values)
    rdm = 1 - sim
    np.fill_diagonal(rdm, 0)
    rdm_df = pd.DataFrame(rdm, index=profiles_df.index, columns=profiles_df.index)
    return rdm_df


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load profiles
    disease_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_profiles.csv'), index_col='Site')
    mechanism_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_profiles.csv'), index_col='Site')

    # Compute RDMs
    disease_rdm = compute_rdm(disease_profiles)
    mechanism_rdm = compute_rdm(mechanism_profiles)

    # Save
    disease_rdm.to_csv(os.path.join(OUTPUT_DIR, 'disease_rdm.csv'))
    mechanism_rdm.to_csv(os.path.join(OUTPUT_DIR, 'mechanism_rdm.csv'))

    print("Disease RDM:")
    print(disease_rdm.round(3))
    print("\nMechanism RDM:")
    print(mechanism_rdm.round(3))
    print("\nDone. Saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
