"""
Step 7: Visualize sensitivity and robustness results.
Generates figS3, figS5, figS6, figS7, and tableS5.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.spatial.distance import squareform, pdist

np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
INPUT_DIR = os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables')
A04_DIR = os.path.join(PROJECT_DIR, 'a04', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


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

    return disease_profile, mechanism_profile, disease_cats


def majority_vote(series):
    """Return most frequent value; if tied, first alphabetically."""
    counts = series.value_counts()
    max_count = counts.max()
    tied = counts[counts == max_count].index.tolist()
    return sorted(tied)[0]


def get_original_mantel_r():
    """Attempt to load original Mantel r from a04 results."""
    mantel_path = os.path.join(A04_DIR, 'mantel_results.csv')
    if os.path.exists(mantel_path):
        mantel_df = pd.read_csv(mantel_path)
        dm_row = mantel_df[
            mantel_df.apply(lambda row: 'disease' in str(row).lower() and 'mechanism' in str(row).lower(), axis=1)
        ]
        if len(dm_row) > 0:
            r_val = dm_row.iloc[0].get('mantel_r', dm_row.iloc[0].get('r', None))
            if r_val is not None:
                return float(r_val)
    # Fallback: try other_inclusion.csv from our own results
    other_path = os.path.join(OUTPUT_DIR, 'other_inclusion.csv')
    if os.path.exists(other_path):
        df = pd.read_csv(other_path)
        orig_row = df[df['condition'] == 'original']
        if len(orig_row) > 0:
            return float(orig_row.iloc[0]['mantel_r'])
    return None


def main():
    print("Generating sensitivity visualizations...")

    original_r = get_original_mantel_r()
    if original_r is None:
        print("  WARNING: Could not determine original Mantel r. Using None for reference lines.")

    # --- figS3: Perturbation p-value histogram ---
    print("  figS3_perturbation.png")
    perturbation_path = os.path.join(OUTPUT_DIR, 'perturbation_results.csv')
    if os.path.exists(perturbation_path):
        perturb_df = pd.read_csv(perturbation_path)
        pct_sig = (perturb_df['somat_disease_p'] < 0.05).mean() * 100

        fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
        ax.hist(perturb_df['somat_disease_p'], bins=50, edgecolor='black', alpha=0.7)
        ax.axvline(x=0.05, color='red', linestyle='--', linewidth=2, label='p = 0.05')
        ax.set_xlabel('Somatotopic-Disease Mantel p-value')
        ax.set_ylabel('Count')
        ax.set_title(f'Coordinate Perturbation: {pct_sig:.1f}% of iterations significant')
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'figS3_perturbation.png'))
        plt.close()
    else:
        print("    SKIPPED: perturbation_results.csv not found")

    # --- figS5: Leave-one-out bar plot ---
    print("  figS5_loo.png")
    loo_path = os.path.join(OUTPUT_DIR, 'loo_results.csv')
    if os.path.exists(loo_path):
        loo_df = pd.read_csv(loo_path)

        fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
        ax.bar(loo_df['excluded_site'], loo_df['mantel_r'], color='steelblue', edgecolor='black')
        if original_r is not None:
            ax.axhline(y=original_r, color='red', linestyle='--', linewidth=2,
                       label=f'Original r = {original_r:.3f}')
            ax.legend()
        ax.set_xlabel('Excluded Site')
        ax.set_ylabel('Disease-Mechanism Mantel r')
        ax.set_title('Leave-One-Out Sensitivity Analysis')
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'figS5_loo.png'))
        plt.close()
    else:
        print("    SKIPPED: loo_results.csv not found")

    # --- figS6: Subsample histogram ---
    print("  figS6_subsample.png")
    subsample_path = os.path.join(OUTPUT_DIR, 'subsample_results.csv')
    if os.path.exists(subsample_path):
        sub_df = pd.read_csv(subsample_path)

        fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
        ax.hist(sub_df['mantel_r'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
        if original_r is not None:
            ax.axvline(x=original_r, color='red', linestyle='--', linewidth=2,
                       label=f'Original r = {original_r:.3f}')
            ax.legend()
        ax.set_xlabel('Disease-Mechanism Mantel r')
        ax.set_ylabel('Count')
        ax.set_title('Subsample Sensitivity (n=22 per site)')
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'figS6_subsample.png'))
        plt.close()
    else:
        print("    SKIPPED: subsample_results.csv not found")

    # --- figS7: Publication collapse heatmap comparison ---
    print("  figS7_pub_collapse.png")
    combined_path = os.path.join(INPUT_DIR, 'combined_data.csv')
    if os.path.exists(combined_path):
        combined = pd.read_csv(combined_path)
        disease_dict = pd.read_csv(os.path.join(INPUT_DIR, 'disease_dictionary.csv'))
        mechanism_dict = pd.read_csv(os.path.join(INPUT_DIR, 'mechanism_dictionary.csv'))

        disease_map = dict(zip(disease_dict['disease_string'], disease_dict['level_7']))
        mechanism_map = dict(zip(mechanism_dict['mechanism_string'], mechanism_dict['level_8']))

        combined['disease_cat'] = combined['Disease'].map(disease_map)
        combined['mechanism_cat'] = combined['Mechanism'].map(mechanism_map)

        # Original profiles
        disease_profile_orig, _, disease_cats = build_profiles(
            combined, 'disease_cat', 'mechanism_cat', SITES
        )

        # Collapsed profiles
        collapsed_records = []
        for site in SITES:
            site_df = combined[combined['Site'] == site]
            for pmid, group in site_df.groupby('PMID'):
                record = {
                    'PMID': pmid,
                    'Site': site,
                    'disease_cat': majority_vote(group['disease_cat']),
                    'mechanism_cat': majority_vote(group['mechanism_cat'])
                }
                collapsed_records.append(record)
        collapsed = pd.DataFrame(collapsed_records)

        disease_profile_coll, _, disease_cats_coll = build_profiles(
            collapsed, 'disease_cat', 'mechanism_cat', SITES
        )

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=150)

        sns.heatmap(
            pd.DataFrame(disease_profile_orig, index=SITES, columns=disease_cats),
            ax=ax1, cmap='YlOrRd', annot=True, fmt='.2f', cbar_kws={'shrink': 0.8}
        )
        ax1.set_title('Disease Profiles (Before Collapse)')
        ax1.set_xlabel('Disease Category')
        ax1.set_ylabel('Site')

        sns.heatmap(
            pd.DataFrame(disease_profile_coll, index=SITES, columns=disease_cats_coll),
            ax=ax2, cmap='YlOrRd', annot=True, fmt='.2f', cbar_kws={'shrink': 0.8}
        )
        ax2.set_title('Disease Profiles (After Collapse)')
        ax2.set_xlabel('Disease Category')
        ax2.set_ylabel('Site')

        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, 'figS7_pub_collapse.png'))
        plt.close()
    else:
        print("    SKIPPED: combined_data.csv not found")

    # --- tableS5: Summary sensitivity table ---
    print("  tableS5_sensitivity.csv")
    rows = []

    # LOO
    if os.path.exists(loo_path):
        loo_df = pd.read_csv(loo_path)
        rows.append({
            'analysis': 'Leave-one-out',
            'condition': 'Min r across exclusions',
            'mantel_r': loo_df['mantel_r'].min(),
            'p_value': loo_df.loc[loo_df['mantel_r'].idxmin(), 'p_value'],
            'ci_lower': np.nan,
            'ci_upper': np.nan,
            'interpretation': 'Stable' if loo_df['mantel_r'].min() > 0 else 'Unstable'
        })

    # Bootstrap
    bootstrap_path = os.path.join(OUTPUT_DIR, 'bootstrap_mantel_ci.csv')
    if os.path.exists(bootstrap_path):
        boot_df = pd.read_csv(bootstrap_path)
        rows.append({
            'analysis': 'Bootstrap',
            'condition': '95% CI',
            'mantel_r': boot_df.iloc[0]['mean_r'],
            'p_value': np.nan,
            'ci_lower': boot_df.iloc[0]['ci_lower'],
            'ci_upper': boot_df.iloc[0]['ci_upper'],
            'interpretation': 'Significant' if boot_df.iloc[0]['ci_lower'] > 0 else 'Includes zero'
        })

    # Subsample
    if os.path.exists(subsample_path):
        sub_df = pd.read_csv(subsample_path)
        pct_sig = (sub_df['p_value'] < 0.05).mean() * 100
        rows.append({
            'analysis': 'Subsample (n=22)',
            'condition': f'{pct_sig:.0f}% significant',
            'mantel_r': sub_df['mantel_r'].mean(),
            'p_value': sub_df['p_value'].median(),
            'ci_lower': np.nan,
            'ci_upper': np.nan,
            'interpretation': 'Robust' if pct_sig > 80 else 'Sensitive to sample size'
        })

    # Perturbation
    if os.path.exists(perturbation_path):
        perturb_df = pd.read_csv(perturbation_path)
        pct_dis = (perturb_df['somat_disease_p'] < 0.05).mean() * 100
        rows.append({
            'analysis': 'Coordinate perturbation',
            'condition': f'Somat-Disease ({pct_dis:.0f}% sig)',
            'mantel_r': perturb_df['somat_disease_r'].mean(),
            'p_value': perturb_df['somat_disease_p'].median(),
            'ci_lower': np.nan,
            'ci_upper': np.nan,
            'interpretation': 'Robust' if pct_dis > 80 else 'Sensitive to coordinates'
        })

    # Other inclusion
    other_path = os.path.join(OUTPUT_DIR, 'other_inclusion.csv')
    if os.path.exists(other_path):
        other_df = pd.read_csv(other_path)
        other_row = other_df[other_df['condition'] == 'other_included']
        if len(other_row) > 0:
            rows.append({
                'analysis': 'Other category inclusion',
                'condition': 'Other included',
                'mantel_r': other_row.iloc[0]['mantel_r'],
                'p_value': other_row.iloc[0]['p_value'],
                'ci_lower': np.nan,
                'ci_upper': np.nan,
                'interpretation': 'Stable' if other_row.iloc[0]['p_value'] < 0.05 else 'Not significant'
            })

    # Publication collapse
    pub_mantel_path = os.path.join(OUTPUT_DIR, 'pub_collapse_mantel.csv')
    if os.path.exists(pub_mantel_path):
        pub_df = pd.read_csv(pub_mantel_path)
        coll_row = pub_df[pub_df['condition'] == 'pub_collapsed']
        if len(coll_row) > 0:
            rows.append({
                'analysis': 'Publication collapse',
                'condition': 'Collapsed',
                'mantel_r': coll_row.iloc[0]['mantel_r'],
                'p_value': coll_row.iloc[0]['p_value'],
                'ci_lower': np.nan,
                'ci_upper': np.nan,
                'interpretation': 'Stable' if coll_row.iloc[0]['p_value'] < 0.05 else 'Not significant'
            })

    if rows:
        summary_df = pd.DataFrame(rows)
        summary_path = os.path.join(OUTPUT_DIR, 'tableS5_sensitivity.csv')
        summary_df.to_csv(summary_path, index=False)
        print(f"  Saved: {summary_path}")
        print(summary_df.to_string(index=False))
    else:
        print("  WARNING: No results found to build summary table.")

    print("\nVisualization complete.")


if __name__ == '__main__':
    main()
