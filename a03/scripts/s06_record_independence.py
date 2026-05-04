"""
s06_record_independence.py — Assess PMID overlap between all 28 site pairs.
"""

import os
import itertools
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load combined data
    combined = pd.read_csv(os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'combined_data.csv'))
    combined = combined[combined['Site'].isin(SITES)].copy()

    # Get PMIDs per site
    site_pmids = {}
    for site in SITES:
        site_pmids[site] = set(combined[combined['Site'] == site]['PMID'].unique())

    # Compute pairwise overlap
    results = []
    for site1, site2 in itertools.combinations(SITES, 2):
        pmids1 = site_pmids[site1]
        pmids2 = site_pmids[site2]
        shared = pmids1 & pmids2
        n_shared = len(shared)
        n_site1 = len(pmids1)
        n_site2 = len(pmids2)
        min_n = min(n_site1, n_site2)
        pct_shared = (n_shared / min_n * 100) if min_n > 0 else 0.0
        flagged = pct_shared > 50  # flag if more than 50% overlap

        results.append({
            'site1': site1,
            'site2': site2,
            'n_shared': n_shared,
            'n_site1': n_site1,
            'n_site2': n_site2,
            'pct_shared': round(pct_shared, 2),
            'flagged': flagged
        })

    overlap_df = pd.DataFrame(results)
    overlap_df.to_csv(os.path.join(OUTPUT_DIR, 'pmid_overlap.csv'), index=False)

    print("PMID overlap between site pairs:")
    print(overlap_df.to_string(index=False))
    print(f"\nFlagged pairs (>50% overlap): {overlap_df['flagged'].sum()}")
    print("\nDone. Saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
