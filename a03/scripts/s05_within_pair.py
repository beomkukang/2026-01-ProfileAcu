"""
s05_within_pair.py — Within anatomical-pair chi-squared tests and standardized residuals.
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
PAIRS = [('BL25', 'GV4'), ('ST25', 'CV12'), ('PC6', 'LI4'), ('SP6', 'ST36')]


def compute_pair_test(counts_df, site1, site2):
    """Build 2×k contingency table and run chi2 test."""
    row1 = counts_df.loc[site1].values
    row2 = counts_df.loc[site2].values

    # Remove categories with zero counts in both
    mask = (row1 + row2) > 0
    row1 = row1[mask]
    row2 = row2[mask]
    cats = counts_df.columns[mask]

    contingency = np.array([row1, row2])

    # Chi-squared test
    chi2, p_value, df, expected = chi2_contingency(contingency)

    # Standardized residuals: (O - E) / sqrt(E)
    residuals = (contingency - expected) / np.sqrt(expected)

    return chi2, p_value, df, cats, residuals


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load count matrices
    disease_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_counts.csv'), index_col='Site')
    mechanism_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_counts.csv'), index_col='Site')

    test_results = []
    residual_results = []

    for domain, counts_df in [('disease', disease_counts), ('mechanism', mechanism_counts)]:
        for site1, site2 in PAIRS:
            chi2, p_value, df, cats, residuals = compute_pair_test(counts_df, site1, site2)

            test_results.append({
                'pair': f"{site1}-{site2}",
                'domain': domain,
                'chi2': chi2,
                'p_value': p_value,
                'df': df
            })

            for i, cat in enumerate(cats):
                residual_results.append({
                    'pair': f"{site1}-{site2}",
                    'domain': domain,
                    'category': cat,
                    f'residual_{site1}': residuals[0, i],
                    f'residual_{site2}': residuals[1, i]
                })

    # Save test results
    test_df = pd.DataFrame(test_results)
    test_df.to_csv(os.path.join(OUTPUT_DIR, 'within_pair_tests.csv'), index=False)

    # Save residuals — reshape to have consistent columns
    residual_rows = []
    for domain, counts_df in [('disease', disease_counts), ('mechanism', mechanism_counts)]:
        for site1, site2 in PAIRS:
            chi2, p_value, df, cats, residuals = compute_pair_test(counts_df, site1, site2)
            for i, cat in enumerate(cats):
                residual_rows.append({
                    'pair': f"{site1}-{site2}",
                    'domain': domain,
                    'category': cat,
                    'residual_site1': residuals[0, i],
                    'residual_site2': residuals[1, i]
                })

    residual_df = pd.DataFrame(residual_rows)
    residual_df.to_csv(os.path.join(OUTPUT_DIR, 'within_pair_residuals.csv'), index=False)

    print("Within-pair chi-squared tests:")
    print(test_df.to_string(index=False))
    print(f"\nResiduals: {len(residual_df)} rows")
    print("\nDone. Saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
