"""
Step 8: Subsample sensitivity for top-3 concentration ranking.
1,000 iterations subsampling each site to n=22 (BL25's count).
Tests whether the specialist-generalist ranking is a sample size artifact.
"""
import numpy as np
import pandas as pd
import os

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
INPUT_DIR = os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

os.makedirs(OUTPUT_DIR, exist_ok=True)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
N_ITERATIONS = 1000
SUBSAMPLE_N = 22


def compute_top3_concentration(site_df, disease_col, mechanism_col):
    """Top-3 cell concentration: sum of 3 largest disease x mechanism cells / total * 100."""
    ct = pd.crosstab(site_df[disease_col], site_df[mechanism_col])
    values = ct.values.flatten()
    total = values.sum()
    if total == 0:
        return 0.0
    top3 = np.sort(values)[-3:]
    return np.sum(top3) / total * 100


def main():
    print("=" * 60)
    print("A07 Step 08: Subsample Sensitivity for Top-3 Concentration")
    print("=" * 60)

    # Load and prepare data
    combined = pd.read_csv(os.path.join(INPUT_DIR, 'combined_data.csv'))
    disease_dict = pd.read_csv(os.path.join(INPUT_DIR, 'disease_dictionary.csv'))
    mechanism_dict = pd.read_csv(os.path.join(INPUT_DIR, 'mechanism_dictionary.csv'))

    disease_map = dict(zip(disease_dict['disease_string'], disease_dict['level_7']))
    mechanism_map = dict(zip(mechanism_dict['mechanism_string'], mechanism_dict['level_8']))

    combined['disease_cat'] = combined['Disease'].map(disease_map)
    combined['mechanism_cat'] = combined['Mechanism'].map(mechanism_map)

    # Exclude Other/Unknown
    combined = combined[~combined['disease_cat'].isin(['Other', 'Unknown'])]
    combined = combined[~combined['mechanism_cat'].isin(['Other', 'Unknown'])]
    combined = combined.dropna(subset=['disease_cat', 'mechanism_cat'])

    # Original top-3 concentration
    print("\nOriginal top-3 concentration:")
    original = {}
    for site in SITES:
        site_df = combined[combined['Site'] == site]
        original[site] = compute_top3_concentration(site_df, 'disease_cat', 'mechanism_cat')
        print(f"  {site}: {original[site]:.1f}% (n={len(site_df)})")
    original_ranking = sorted(SITES, key=lambda s: original[s], reverse=True)
    print(f"Original ranking: {' > '.join(original_ranking)}")

    # Subsample iterations
    print(f"\nRunning {N_ITERATIONS} subsample iterations (n={SUBSAMPLE_N} per site)...")
    all_concentrations = {site: [] for site in SITES}
    ranking_preserved_count = 0

    for i in range(N_ITERATIONS):
        if (i + 1) % 100 == 0:
            print(f"  Iteration {i + 1}/{N_ITERATIONS}")

        iter_conc = {}
        for site in SITES:
            site_df = combined[combined['Site'] == site]
            if len(site_df) > SUBSAMPLE_N:
                site_df = site_df.sample(n=SUBSAMPLE_N, replace=False)
            conc = compute_top3_concentration(site_df, 'disease_cat', 'mechanism_cat')
            iter_conc[site] = conc
            all_concentrations[site].append(conc)

        # Check if top-1 and bottom-1 are preserved
        iter_ranking = sorted(SITES, key=lambda s: iter_conc[s], reverse=True)
        if iter_ranking[0] == original_ranking[0] and iter_ranking[-1] == original_ranking[-1]:
            ranking_preserved_count += 1

    # Summary statistics
    print("\nSubsampled top-3 concentration (mean ± SD):")
    summary_rows = []
    for site in SITES:
        vals = all_concentrations[site]
        mean_conc = np.mean(vals)
        sd_conc = np.std(vals)
        ci_low = np.percentile(vals, 2.5)
        ci_high = np.percentile(vals, 97.5)
        summary_rows.append({
            'site': site,
            'original_concentration': original[site],
            'original_n': len(combined[combined['Site'] == site]),
            'subsample_mean': round(mean_conc, 2),
            'subsample_sd': round(sd_conc, 2),
            'ci_2.5': round(ci_low, 2),
            'ci_97.5': round(ci_high, 2),
        })
        print(f"  {site}: {mean_conc:.1f}% ± {sd_conc:.1f}% "
              f"[95% CI: {ci_low:.1f}–{ci_high:.1f}%] (original: {original[site]:.1f}%)")

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df.sort_values('subsample_mean', ascending=False)

    subsample_ranking = summary_df['site'].tolist()
    print(f"\nSubsampled mean ranking: {' > '.join(subsample_ranking)}")
    print(f"Original ranking:       {' > '.join(original_ranking)}")
    print(f"Top-1 & bottom-1 preserved: {ranking_preserved_count}/{N_ITERATIONS} "
          f"({ranking_preserved_count / N_ITERATIONS * 100:.1f}%)")

    # Spearman rank correlation between original and subsampled rankings
    from scipy.stats import spearmanr
    orig_ranks = [original[s] for s in SITES]
    sub_ranks = [np.mean(all_concentrations[s]) for s in SITES]
    rank_r, rank_p = spearmanr(orig_ranks, sub_ranks)
    print(f"Rank correlation (original vs subsampled mean): r={rank_r:.3f}, p={rank_p:.4f}")

    # Save
    out_path = os.path.join(OUTPUT_DIR, 'subsample_coupling.csv')
    summary_df.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")


if __name__ == '__main__':
    main()
