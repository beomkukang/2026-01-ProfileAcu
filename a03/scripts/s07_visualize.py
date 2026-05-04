"""
Step 7: Visualization — BF heatmap (Fig 2), RDM triplet (Fig 3), Table 3.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import pdist
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']

plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150


def plot_bf_heatmap():
    """Figure 2: Two-panel BF heatmap (disease + mechanism)."""
    disease_bf = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_bf.csv'), index_col=0)
    mechanism_bf = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_bf.csv'), index_col=0)
    disease_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_counts.csv'), index_col=0)
    mechanism_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_counts.csv'), index_col=0)

    # Load dendrogram data for row ordering
    dendro_path = os.path.join(OUTPUT_DIR, 'dendrogram_data.pkl')
    if os.path.exists(dendro_path):
        with open(dendro_path, 'rb') as f:
            dendro_data = pickle.load(f)
        disease_row_order = dendro_data['disease_row_order']
        mechanism_row_order = dendro_data.get('mechanism_row_order', disease_row_order)
    else:
        # Fallback: compute from profiles
        disease_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_profiles.csv'), index_col=0)
        dist = pdist(disease_profiles.values, metric='cosine')
        dist = np.nan_to_num(dist, nan=0.0)
        Z = linkage(dist, method='average')
        disease_row_order = [disease_profiles.index[i] for i in leaves_list(Z)]
        mechanism_row_order = disease_row_order

    # Reorder each panel by its own dendrogram leaf order
    disease_bf = disease_bf.loc[disease_row_order]
    mechanism_bf = mechanism_bf.loc[mechanism_row_order]
    disease_counts = disease_counts.loc[disease_row_order]
    mechanism_counts = mechanism_counts.loc[mechanism_row_order]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Threshold for annotation: |log2BF| > log2(3) ~ 1.585
    threshold = np.log2(3)

    # Disease BF heatmap
    mask_zero_d = disease_counts.values == 0
    annot_d = np.where(np.abs(disease_bf.values) > threshold,
                       np.round(disease_bf.values, 1).astype(str), '')
    annot_d = np.where(mask_zero_d, '', annot_d)

    data_d = disease_bf.values.copy()
    data_d[mask_zero_d] = np.nan

    sns.heatmap(data_d, ax=ax1, cmap='RdBu_r', center=0, vmin=-5, vmax=5,
                xticklabels=disease_bf.columns, yticklabels=disease_bf.index,
                annot=annot_d, fmt='', annot_kws={'fontsize': 7},
                cbar_kws={'label': 'log\u2082(BF)', 'shrink': 0.8},
                mask=mask_zero_d, linewidths=0.5)
    ax1.set_title('Disease-Domain Enrichment', fontsize=12, fontweight='bold')
    ax1.set_xlabel('')
    ax1.set_ylabel('Acupoint Site')
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # Mechanism BF heatmap
    mask_zero_m = mechanism_counts.values == 0
    annot_m = np.where(np.abs(mechanism_bf.values) > threshold,
                       np.round(mechanism_bf.values, 1).astype(str), '')
    annot_m = np.where(mask_zero_m, '', annot_m)

    data_m = mechanism_bf.values.copy()
    data_m[mask_zero_m] = np.nan

    sns.heatmap(data_m, ax=ax2, cmap='RdBu_r', center=0, vmin=-5, vmax=5,
                xticklabels=mechanism_bf.columns, yticklabels=mechanism_bf.index,
                annot=annot_m, fmt='', annot_kws={'fontsize': 7},
                cbar_kws={'label': 'log\u2082(BF)', 'shrink': 0.8},
                mask=mask_zero_m, linewidths=0.5)
    ax2.set_title('Mechanism-Domain Enrichment', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Acupoint Site')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

    # Italic annotation explaining empty/gray cells
    fig.text(0.98, 0.02,
             'Gray cells: zero records (no data). '
             'Values shown only where |log\u2082(BF)| > 1.58 (BF > 3).',
             ha='right', va='bottom', fontsize=7, fontstyle='italic', color='#555555')

    plt.tight_layout(rect=[0, 0.04, 1, 1])  # leave room for annotation
    plt.savefig(os.path.join(FIG_DIR, 'fig2_bf_heatmap.png'), bbox_inches='tight')
    plt.close()
    print("Saved: fig2_bf_heatmap.png")


def plot_rdms():
    """Figure 3: Three RDMs side by side."""
    disease_rdm = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_rdm.csv'), index_col=0)
    mechanism_rdm = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_rdm.csv'), index_col=0)

    # Try to load somatotopic RDM
    somat_path = os.path.join(PROJECT_ROOT, 'a02', 'results', 'datatables', 'surface_rdm.csv')
    has_somat = os.path.exists(somat_path)
    if has_somat:
        somat_rdm = pd.read_csv(somat_path, index_col=0)
        n_panels = 3
    else:
        n_panels = 2
        print("  Note: Surface distance RDM not found, generating 2-panel version")

    # Row ordering from dendrogram leaf order
    dendro_path = os.path.join(OUTPUT_DIR, 'dendrogram_data.pkl')
    if os.path.exists(dendro_path):
        with open(dendro_path, 'rb') as f:
            dendro_data = pickle.load(f)
        row_order = dendro_data['disease_row_order']
    else:
        row_order = disease_rdm.index.tolist()

    fig, axes = plt.subplots(1, n_panels, figsize=(6 * n_panels, 6))
    if n_panels == 2:
        axes = list(axes)

    # Disease RDM
    d = disease_rdm.loc[row_order, row_order]
    mask_diag = np.eye(len(row_order), dtype=bool)
    sns.heatmap(d.values, ax=axes[0], cmap='viridis', vmin=0, vmax=1,
                xticklabels=row_order, yticklabels=row_order,
                annot=True, fmt='.2f', annot_kws={'fontsize': 7},
                mask=mask_diag, square=True,
                cbar_kws={'label': 'Cosine Distance', 'shrink': 0.7})
    axes[0].set_title('Disease Space RDM', fontsize=12, fontweight='bold')

    # Mechanism RDM
    m = mechanism_rdm.loc[row_order, row_order]
    sns.heatmap(m.values, ax=axes[1], cmap='viridis', vmin=0, vmax=1,
                xticklabels=row_order, yticklabels=row_order,
                annot=True, fmt='.2f', annot_kws={'fontsize': 7},
                mask=mask_diag, square=True,
                cbar_kws={'label': 'Cosine Distance', 'shrink': 0.7})
    axes[1].set_title('Mechanism Space RDM', fontsize=12, fontweight='bold')

    # Somatotopic RDM
    if has_somat:
        s = somat_rdm.loc[row_order, row_order]
        sns.heatmap(s.values, ax=axes[2], cmap='magma',
                    xticklabels=row_order, yticklabels=row_order,
                    annot=True, fmt='.1f', annot_kws={'fontsize': 7},
                    mask=mask_diag, square=True,
                    cbar_kws={'label': 'Euclidean Distance (mm)', 'shrink': 0.7})
        axes[2].set_title('Body Space RDM', fontsize=12, fontweight='bold')

    for ax in axes:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'fig3_rdms.png'), bbox_inches='tight')
    plt.close()
    print("Saved: fig3_rdms.png")


def generate_table3():
    """Table 3: Disease and mechanism distributions per site."""
    disease_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_counts.csv'), index_col=0)
    mechanism_counts = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_counts.csv'), index_col=0)
    disease_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_profiles.csv'), index_col=0)
    mechanism_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_profiles.csv'), index_col=0)

    rows = []
    for site in disease_counts.index:
        row = {'Site': site, 'Domain': 'Disease'}
        for cat in disease_counts.columns:
            row[f'{cat}_n'] = int(disease_counts.loc[site, cat])
            row[f'{cat}_pct'] = round(disease_profiles.loc[site, cat] * 100, 1)
        rows.append(row)

    for site in mechanism_counts.index:
        row = {'Site': site, 'Domain': 'Mechanism'}
        for cat in mechanism_counts.columns:
            row[f'{cat}_n'] = int(mechanism_counts.loc[site, cat])
            row[f'{cat}_pct'] = round(mechanism_profiles.loc[site, cat] * 100, 1)
        rows.append(row)

    table3 = pd.DataFrame(rows)
    out_path = os.path.join(OUTPUT_DIR, 'table3_distributions.csv')
    table3.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    plot_bf_heatmap()
    plot_rdms()
    generate_table3()
    print("\nAll visualizations saved.")


if __name__ == '__main__':
    main()
