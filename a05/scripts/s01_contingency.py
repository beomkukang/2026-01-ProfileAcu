"""
Analysis 05 - Step 01: Disease-Mechanism Contingency Tables & Coupling Metrics
===============================================================================
Builds per-site contingency tables (disease x mechanism) and computes coupling
metrics: NMI, joint entropy, top-3 concentration, n_nonzero_cells, n_records.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def load_data():
    """Load combined data and merge with disease/mechanism dictionaries."""
    combined_path = os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'combined_data.csv')
    disease_dict_path = os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'disease_dictionary.csv')
    mechanism_dict_path = os.path.join(PROJECT_ROOT, 'a01', 'results', 'datatables', 'mechanism_dictionary.csv')

    combined = pd.read_csv(combined_path)
    disease_dict = pd.read_csv(disease_dict_path)
    mechanism_dict = pd.read_csv(mechanism_dict_path)

    print(f"Combined data: {len(combined)} records")
    print(f"Disease dictionary: {len(disease_dict)} entries")
    print(f"Mechanism dictionary: {len(mechanism_dict)} entries")

    return combined, disease_dict, mechanism_dict


def merge_and_filter(combined, disease_dict, mechanism_dict):
    """Merge dictionaries and exclude Other/Unknown categories."""
    # Merge disease categories (level_7 = final disease category)
    if 'level_7' in disease_dict.columns:
        disease_map = disease_dict[['disease_string', 'level_7']].drop_duplicates()
        disease_map = disease_map.rename(columns={'level_7': 'disease_category'})
    else:
        # Fallback: use last level column available
        level_cols = [c for c in disease_dict.columns if c.startswith('level_')]
        disease_map = disease_dict[['disease_string', level_cols[-1]]].drop_duplicates()
        disease_map = disease_map.rename(columns={level_cols[-1]: 'disease_category'})

    # Merge mechanism categories (level_8 = final mechanism category)
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
    exclude_disease = ['Other']
    exclude_mechanism = ['Other', 'Unknown']

    before = len(df)
    df = df[~df['disease_category'].isin(exclude_disease)]
    df = df[~df['mechanism_category'].isin(exclude_mechanism)]
    df = df.dropna(subset=['disease_category', 'mechanism_category'])
    after = len(df)

    print(f"After filtering: {after} records (excluded {before - after})")
    return df


def compute_joint_entropy(contingency_table):
    """Compute joint entropy: -sum(p * log2(p)) for non-zero cells."""
    values = contingency_table.values.flatten()
    values = values[values > 0]
    total = values.sum()
    probs = values / total
    entropy = -np.sum(probs * np.log2(probs))
    return entropy


def compute_top3_concentration(contingency_table):
    """Sum of 3 largest cells / total * 100."""
    values = contingency_table.values.flatten()
    total = values.sum()
    if total == 0:
        return 0.0
    top3 = np.sort(values)[-3:]
    return np.sum(top3) / total * 100


def build_contingency_and_metrics(df):
    """For each site, build contingency table and compute metrics."""
    contingency_tables = {}
    metrics_rows = []

    for site in SITES:
        site_df = df[df['Site'] == site]

        if len(site_df) == 0:
            print(f"  WARNING: No records for site {site}")
            continue

        # Build contingency table
        ct = pd.crosstab(site_df['disease_category'], site_df['mechanism_category'])
        contingency_tables[site] = ct

        # NMI
        nmi = normalized_mutual_info_score(
            site_df['disease_category'].values,
            site_df['mechanism_category'].values
        )

        # Joint entropy
        joint_entropy = compute_joint_entropy(ct)

        # Top-3 concentration
        top3_conc = compute_top3_concentration(ct)

        # Non-zero cells
        n_nonzero = int((ct.values > 0).sum())

        metrics_rows.append({
            'site': site,
            'NMI': round(nmi, 4),
            'joint_entropy': round(joint_entropy, 4),
            'top3_concentration': round(top3_conc, 2),
            'n_nonzero_cells': n_nonzero,
            'n_records': len(site_df)
        })

        print(f"  {site}: NMI={nmi:.4f}, H_joint={joint_entropy:.3f}, "
              f"Top3={top3_conc:.1f}%, nonzero={n_nonzero}, n={len(site_df)}")

    metrics_df = pd.DataFrame(metrics_rows)
    return contingency_tables, metrics_df


def main():
    print("=" * 60)
    print("A05 Step 01: Disease-Mechanism Contingency & Coupling Metrics")
    print("=" * 60)

    # Load data
    combined, disease_dict, mechanism_dict = load_data()

    # Merge and filter
    df = merge_and_filter(combined, disease_dict, mechanism_dict)

    # Build contingency tables and compute metrics
    print("\nComputing per-site coupling metrics...")
    contingency_tables, metrics_df = build_contingency_and_metrics(df)

    # Save outputs
    pkl_path = os.path.join(OUTPUT_DIR, 'contingency_tables.pkl')
    with open(pkl_path, 'wb') as f:
        pickle.dump(contingency_tables, f)
    print(f"\nSaved contingency tables: {pkl_path}")

    csv_path = os.path.join(OUTPUT_DIR, 'coupling_metrics.csv')
    metrics_df.to_csv(csv_path, index=False)
    print(f"Saved coupling metrics: {csv_path}")

    print("\nDone.")


if __name__ == '__main__':
    main()
