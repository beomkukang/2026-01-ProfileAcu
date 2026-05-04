"""
s02_bayes_factors.py — Compute log2 Bayes Factors for enrichment vs pooled baseline.
Beta-Binomial model with Beta(1,1) uniform prior.
"""

import os
import numpy as np
import pandas as pd
from scipy.special import betaln

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def compute_log2_bf(counts_df):
    """
    For each site x category, compute log2 Bayes Factor.

    Alternative: Beta-Binomial with Beta(1,1) prior
    Null: Binomial with fixed p0 (pooled baseline rate)
    """
    n_per_site = counts_df.sum(axis=1)  # total trials per site
    total_per_category = counts_df.sum(axis=0)  # total in each category across all sites
    total_all = counts_df.sum().sum()  # grand total

    bf_matrix = pd.DataFrame(index=counts_df.index, columns=counts_df.columns, dtype=float)

    for cat in counts_df.columns:
        p0 = total_per_category[cat] / total_all  # baseline rate
        for site in counts_df.index:
            k = counts_df.loc[site, cat]
            n = n_per_site[site]

            # Alternative marginal likelihood: Beta-Binomial with Beta(1,1)
            log_alt = betaln(1 + k, 1 + n - k) - betaln(1, 1)

            # Null likelihood: Binomial with fixed p0
            if p0 == 0 or p0 == 1:
                # Edge case: if category never appears or always appears
                if p0 == 0:
                    log_null = 0.0 if k == 0 else -np.inf
                else:
                    log_null = 0.0 if k == n else -np.inf
            else:
                log_null = k * np.log(p0) + (n - k) * np.log(1 - p0)

            # log2 BF
            if np.isinf(log_null) and log_null < 0:
                bf_matrix.loc[site, cat] = np.inf
            elif log_alt == log_null:
                bf_matrix.loc[site, cat] = 0.0
            else:
                bf_matrix.loc[site, cat] = (log_alt - log_null) / np.log(2)

    return bf_matrix


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load count matrices
    disease_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_counts.csv'), index_col='Site')
    mechanism_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_counts.csv'), index_col='Site')

    # Compute Bayes Factors
    disease_bf = compute_log2_bf(disease_counts)
    mechanism_bf = compute_log2_bf(mechanism_counts)

    # Save
    disease_bf.index.name = 'Site'
    mechanism_bf.index.name = 'Site'
    disease_bf.to_csv(os.path.join(OUTPUT_DIR, 'disease_bf.csv'))
    mechanism_bf.to_csv(os.path.join(OUTPUT_DIR, 'mechanism_bf.csv'))

    print("Disease BF matrix shape:", disease_bf.shape)
    print("Mechanism BF matrix shape:", mechanism_bf.shape)
    print("\nDisease BF summary:")
    print(disease_bf.describe())
    print("\nMechanism BF summary:")
    print(mechanism_bf.describe())
    print("\nDone. Saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
