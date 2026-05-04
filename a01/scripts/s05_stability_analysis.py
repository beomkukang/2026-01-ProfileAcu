"""
Step 5: RDM stability analysis — Mantel tests and classification reports.
"""
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from scipy.spatial.distance import squareform
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
N_PERMUTATIONS = 10000
DISEASE_K = [5, 7, 9, 11, 13, 14, 15]  # k values for disease levels 1-7
MECHANISM_K = [4, 6, 8, 9, 10, 11, 12, 13]  # k values for mechanism levels 1-8


def mantel_test(rdm1, rdm2, n_perms=N_PERMUTATIONS):
    """Mantel test: Spearman correlation between upper-triangle vectors."""
    vec1 = squareform(rdm1)
    vec2 = squareform(rdm2)

    r_obs, _ = spearmanr(vec1, vec2)

    # Permutation test
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


def compute_sparsity(combined, site_col, category_col, sites, exclude_cats):
    """Compute sparsity (% zero cells) in the site x category matrix."""
    filtered = combined[~combined[category_col].isin(exclude_cats)]
    categories = sorted([c for c in filtered[category_col].unique() if c not in exclude_cats])

    n_cats = len(categories)
    if n_cats == 0:
        return 0, 0, 0

    matrix = np.zeros((len(sites), n_cats))
    for i, site in enumerate(sites):
        site_data = filtered[filtered[site_col] == site]
        for j, cat in enumerate(categories):
            matrix[i, j] = (site_data[category_col] == cat).sum()

    total_cells = matrix.size
    zero_cells = (matrix == 0).sum()
    sparsity_pct = zero_cells / total_cells * 100
    return zero_cells, total_cells, sparsity_pct


def main():
    np.random.seed(42)

    # Load RDM data
    rdm_path = os.path.join(OUTPUT_DIR, 'rdm_data.pkl')
    with open(rdm_path, 'rb') as f:
        rdm_data = pickle.load(f)

    disease_rdms = rdm_data['disease_rdms']
    mechanism_rdms = rdm_data['mechanism_rdms']

    # Load combined data with classifications
    combined = pd.read_csv(os.path.join(OUTPUT_DIR, 'combined_data.csv'))
    disease_dict = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_dictionary.csv'))
    mechanism_dict = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_dictionary.csv'))

    n_disease_levels = len(DISEASE_K)
    n_mechanism_levels = len(MECHANISM_K)

    combined = combined.merge(
        disease_dict[['disease_string'] + [f'level_{i}' for i in range(1, n_disease_levels + 1)]],
        left_on='Disease', right_on='disease_string', how='left'
    )
    for i in range(1, n_disease_levels + 1):
        combined.rename(columns={f'level_{i}': f'disease_level_{i}'}, inplace=True)

    combined = combined.merge(
        mechanism_dict[['mechanism_string'] + [f'level_{i}' for i in range(1, n_mechanism_levels + 1)]],
        left_on='Mechanism', right_on='mechanism_string', how='left'
    )
    for i in range(1, n_mechanism_levels + 1):
        combined.rename(columns={f'level_{i}': f'mechanism_level_{i}'}, inplace=True)

    # --- Within-domain stability: Disease ---
    print("Computing disease RDM stability...")
    disease_stability = []
    for level in range(1, n_disease_levels):
        r, p = mantel_test(disease_rdms[level], disease_rdms[level + 1])
        disease_stability.append({
            'level_from': level,
            'level_to': level + 1,
            'k_from': DISEASE_K[level - 1],
            'k_to': DISEASE_K[level],
            'mantel_r': r,
            'p_value': p,
        })
        print(f"  Disease level {level}→{level+1} (k={DISEASE_K[level-1]}→{DISEASE_K[level]}): r={r:.4f}, p={p:.4f}")

    disease_stab_df = pd.DataFrame(disease_stability)
    disease_stab_df.to_csv(os.path.join(OUTPUT_DIR, 'disease_rdm_stability.csv'), index=False)

    # --- Within-domain stability: Mechanism ---
    print("\nComputing mechanism RDM stability...")
    mechanism_stability = []
    for level in range(1, n_mechanism_levels):
        r, p = mantel_test(mechanism_rdms[level], mechanism_rdms[level + 1])
        mechanism_stability.append({
            'level_from': level,
            'level_to': level + 1,
            'k_from': MECHANISM_K[level - 1],
            'k_to': MECHANISM_K[level],
            'mantel_r': r,
            'p_value': p,
        })
        print(f"  Mechanism level {level}→{level+1} (k={MECHANISM_K[level-1]}→{MECHANISM_K[level]}): r={r:.4f}, p={p:.4f}")

    mechanism_stab_df = pd.DataFrame(mechanism_stability)
    mechanism_stab_df.to_csv(os.path.join(OUTPUT_DIR, 'mechanism_rdm_stability.csv'), index=False)

    # --- Cross-domain Mantel ---
    print("\nComputing cross-domain Mantel correlations...")
    cross_domain = []
    for d_level in range(1, n_disease_levels + 1):
        for m_level in range(1, n_mechanism_levels + 1):
            r, p = mantel_test(disease_rdms[d_level], mechanism_rdms[m_level])
            cross_domain.append({
                'disease_level': d_level,
                'mechanism_level': m_level,
                'disease_k': DISEASE_K[d_level - 1],
                'mechanism_k': MECHANISM_K[m_level - 1],
                'mantel_r': r,
                'p_value': p,
            })
            print(f"  Disease L{d_level} x Mechanism L{m_level}: r={r:.4f}")

    cross_df = pd.DataFrame(cross_domain)
    cross_df.to_csv(os.path.join(OUTPUT_DIR, 'cross_domain_mantel.csv'), index=False)

    # --- Classification report ---
    print("\nGenerating classification report...")
    report_rows = []

    for level in range(1, n_disease_levels + 1):
        d_col = f'disease_level_{level}'
        d_cats = [c for c in combined[d_col].unique() if c != 'Other']
        d_other = (combined[d_col] == 'Other').sum()
        d_other_pct = d_other / len(combined) * 100
        d_zero, d_total, d_sparsity = compute_sparsity(
            combined, 'Site', d_col, SITES, {'Other'}
        )

        report_rows.append({
            'domain': 'Disease',
            'level': level,
            'k': DISEASE_K[level - 1],
            'n_categories': len(d_cats),
            'n_other': d_other,
            'pct_other': d_other_pct,
            'zero_cells': d_zero,
            'total_cells': d_total,
            'sparsity_pct': d_sparsity,
        })

    for level in range(1, n_mechanism_levels + 1):
        m_col = f'mechanism_level_{level}'
        m_cats = [c for c in combined[m_col].unique() if c not in ('Other', 'Unknown')]
        m_other = (combined[m_col] == 'Other').sum()
        m_unknown = (combined[m_col] == 'Unknown').sum()
        m_other_pct = m_other / len(combined) * 100
        m_zero, m_total, m_sparsity = compute_sparsity(
            combined, 'Site', m_col, SITES, {'Other', 'Unknown'}
        )

        report_rows.append({
            'domain': 'Mechanism',
            'level': level,
            'k': MECHANISM_K[level - 1],
            'n_categories': len(m_cats),
            'n_other': m_other,
            'n_unknown': m_unknown,
            'pct_other': m_other_pct,
            'zero_cells': m_zero,
            'total_cells': m_total,
            'sparsity_pct': m_sparsity,
        })

    report_df = pd.DataFrame(report_rows)
    report_df.to_csv(os.path.join(OUTPUT_DIR, 'classification_report.csv'), index=False)
    print(f"Saved classification report.")

    print("\nDone. All stability outputs saved.")


if __name__ == '__main__':
    main()
