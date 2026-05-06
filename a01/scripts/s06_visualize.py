"""
Step 6: Visualization — stability curves, heatmaps, sparsity, profiles.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
from scipy.spatial.distance import squareform
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')

DISEASE_K = [5, 7, 9, 11, 13, 14, 15]
MECHANISM_K = [4, 6, 8, 9, 10, 11, 12, 13]
SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']

plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150


def find_elbow(k_values, r_values, plateau_threshold=0.99):
    """Find plateau onset: first k where r reaches plateau_threshold."""
    for i, r in enumerate(r_values):
        if r >= plateau_threshold:
            return i, k_values[i]
    return len(r_values) - 1, k_values[-1]


def plot_stability_curves():
    """Plot 1: RDM stability curves for disease and mechanism."""
    disease_stab = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_rdm_stability.csv'))
    mech_stab = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_rdm_stability.csv'))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Disease stability
    x_d = disease_stab['k_to'].values
    y_d = disease_stab['mantel_r'].values
    ax1.plot(x_d, y_d, 'o-', color='#2196F3', linewidth=2, markersize=8)
    elbow_idx, elbow_k = find_elbow(x_d, y_d)
    ax1.axvline(x=elbow_k, color='red', linestyle=':', alpha=0.7, label=f'Elbow: k={elbow_k}')
    ax1.set_xlabel('Number of Disease Categories (k)')
    ax1.set_ylabel('Mantel r (with previous level)')
    ax1.set_title('Disease RDM Stability')
    ax1.set_ylim(-0.1, 1.05)
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # Mechanism stability
    x_m = mech_stab['k_to'].values
    y_m = mech_stab['mantel_r'].values
    ax2.plot(x_m, y_m, 's-', color='#4CAF50', linewidth=2, markersize=8)
    elbow_idx_m, elbow_k_m = find_elbow(x_m, y_m)
    ax2.axvline(x=elbow_k_m, color='red', linestyle=':', alpha=0.7, label=f'Elbow: k={elbow_k_m}')
    ax2.set_xlabel('Number of Mechanism Categories (k)')
    ax2.set_ylabel('Mantel r (with previous level)')
    ax2.set_title('Mechanism RDM Stability')
    ax2.set_ylim(-0.1, 1.05)
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'rdm_stability_curve.png'), bbox_inches='tight')
    plt.close()
    print("Saved: rdm_stability_curve.png")


def plot_cross_domain_heatmap():
    """Plot 2: Cross-domain Mantel r heatmap."""
    cross = pd.read_csv(os.path.join(OUTPUT_DIR, 'cross_domain_mantel.csv'))

    pivot = cross.pivot(index='mechanism_k', columns='disease_k', values='mantel_r')

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot, annot=True, fmt='.2f', cmap='RdYlBu_r',
                center=0, vmin=-0.5, vmax=1.0, ax=ax,
                xticklabels=DISEASE_K, yticklabels=MECHANISM_K)
    ax.set_xlabel('Disease Categories (k)')
    ax.set_ylabel('Mechanism Categories (k)')
    ax.set_title('Cross-Domain Mantel Correlation\n(Disease RDM vs Mechanism RDM)')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'cross_domain_heatmap.png'), bbox_inches='tight')
    plt.close()
    print("Saved: cross_domain_heatmap.png")


def plot_sparsity_curves():
    """Plot 3: Sparsity curves."""
    report = pd.read_csv(os.path.join(OUTPUT_DIR, 'classification_report.csv'))
    disease_report = report[report['domain'] == 'Disease']
    mech_report = report[report['domain'] == 'Mechanism']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(disease_report['k'], disease_report['sparsity_pct'],
             'o-', color='#2196F3', linewidth=2, markersize=8)
    ax1.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='50% ceiling')
    ax1.set_xlabel('Number of Disease Categories (k)')
    ax1.set_ylabel('Sparsity (%)')
    ax1.set_title('Disease Profile Sparsity')
    ax1.set_ylim(0, 100)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(mech_report['k'], mech_report['sparsity_pct'],
             's-', color='#4CAF50', linewidth=2, markersize=8)
    ax2.axhline(y=50, color='red', linestyle='--', alpha=0.7, label='50% ceiling')
    ax2.set_xlabel('Number of Mechanism Categories (k)')
    ax2.set_ylabel('Sparsity (%)')
    ax2.set_title('Mechanism Profile Sparsity')
    ax2.set_ylim(0, 100)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'sparsity_curve.png'), bbox_inches='tight')
    plt.close()
    print("Saved: sparsity_curve.png")


def plot_other_category_curves():
    """Plot 4: Percentage of records classified as 'Other'."""
    report = pd.read_csv(os.path.join(OUTPUT_DIR, 'classification_report.csv'))
    disease_report = report[report['domain'] == 'Disease']
    mech_report = report[report['domain'] == 'Mechanism']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(disease_report['k'], disease_report['pct_other'],
             'o-', color='#2196F3', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Disease Categories (k)')
    ax1.set_ylabel('% Records as "Other"')
    ax1.set_title('Disease: Unclassified Records')
    ax1.set_ylim(0, max(disease_report['pct_other'].max() * 1.1, 10))
    ax1.grid(True, alpha=0.3)

    ax2.plot(mech_report['k'], mech_report['pct_other'],
             's-', color='#4CAF50', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Mechanism Categories (k)')
    ax2.set_ylabel('% Records as "Other"')
    ax2.set_title('Mechanism: Unclassified Records')
    ax2.set_ylim(0, max(mech_report['pct_other'].max() * 1.1, 10))
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'other_category_curve.png'), bbox_inches='tight')
    plt.close()
    print("Saved: other_category_curve.png")


def plot_profile_comparison():
    """Plot 5: Profile heatmaps at recommended taxonomy level."""
    # Load RDM data to get profiles
    rdm_path = os.path.join(OUTPUT_DIR, 'rdm_data.pkl')
    with open(rdm_path, 'rb') as f:
        rdm_data = pickle.load(f)

    # Determine recommended levels from stability analysis
    disease_stab = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_rdm_stability.csv'))
    mech_stab = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_rdm_stability.csv'))

    # Find elbow: first level where r > 0.9 (use k_to as the recommended level)
    d_rec_level = 3  # default
    for i, r in enumerate(disease_stab['mantel_r']):
        if r >= 0.9:
            d_rec_level = i + 1  # level_from is 0-indexed here
            break

    m_rec_level = 3  # default
    for i, r in enumerate(mech_stab['mantel_r']):
        if r >= 0.9:
            m_rec_level = i + 1
            break

    print(f"Recommended disease level: {d_rec_level} (k={DISEASE_K[d_rec_level-1]})")
    print(f"Recommended mechanism level: {m_rec_level} (k={MECHANISM_K[m_rec_level-1]})")

    d_profile, d_cats = rdm_data['disease_profiles'][d_rec_level]
    m_profile, m_cats = rdm_data['mechanism_profiles'][m_rec_level]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Disease profile heatmap with hierarchical clustering
    if d_profile.shape[0] > 1 and d_profile.shape[1] > 0:
        # Cluster rows (sites)
        from scipy.spatial.distance import pdist
        row_dist = pdist(d_profile, metric='cosine')
        row_dist = np.nan_to_num(row_dist, nan=0.0)
        row_link = linkage(row_dist, method='average')
        row_order = leaves_list(row_link)

        sns.heatmap(d_profile[row_order], ax=ax1, cmap='YlOrRd',
                    xticklabels=d_cats,
                    yticklabels=[SITES[i] for i in row_order],
                    annot=True, fmt='.2f', cbar_kws={'label': 'Proportion'})
    ax1.set_title(f'Disease Profile (Level {d_rec_level}, k={DISEASE_K[d_rec_level-1]})')
    ax1.set_xlabel('Disease Category')
    ax1.set_ylabel('Acupoint Site')
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Mechanism profile heatmap
    if m_profile.shape[0] > 1 and m_profile.shape[1] > 0:
        row_dist_m = pdist(m_profile, metric='cosine')
        row_dist_m = np.nan_to_num(row_dist_m, nan=0.0)
        row_link_m = linkage(row_dist_m, method='average')
        row_order_m = leaves_list(row_link_m)

        sns.heatmap(m_profile[row_order_m], ax=ax2, cmap='YlGnBu',
                    xticklabels=m_cats,
                    yticklabels=[SITES[i] for i in row_order_m],
                    annot=True, fmt='.2f', cbar_kws={'label': 'Proportion'})
    ax2.set_title(f'Mechanism Profile (Level {m_rec_level}, k={MECHANISM_K[m_rec_level-1]})')
    ax2.set_xlabel('Mechanism Category')
    ax2.set_ylabel('Acupoint Site')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'profile_comparison.png'), bbox_inches='tight')
    plt.close()
    print("Saved: profile_comparison.png")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    plot_stability_curves()
    plot_cross_domain_heatmap()
    plot_sparsity_curves()
    plot_other_category_curves()
    plot_profile_comparison()
    print("\nAll figures saved.")


if __name__ == '__main__':
    main()
