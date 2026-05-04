"""
s04_clustering.py — Hierarchical clustering of sites based on disease and mechanism profiles.
Uses dendrogram leaf order for row sorting. No fixed k — the dendrogram structure
is reported directly, and the reader interprets groupings from merge distances.
"""

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
from scipy.spatial.distance import pdist

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']

plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 150


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(FIG_DIR, exist_ok=True)

    # Load profiles
    disease_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'disease_profiles.csv'), index_col='Site')
    mechanism_profiles = pd.read_csv(os.path.join(OUTPUT_DIR, 'mechanism_profiles.csv'), index_col='Site')

    # Hierarchical clustering — disease
    disease_dist = pdist(disease_profiles.values, metric='cosine')
    disease_dist = np.nan_to_num(disease_dist, nan=0.0)
    disease_linkage = linkage(disease_dist, method='average')

    # Hierarchical clustering — mechanism
    mechanism_dist = pdist(mechanism_profiles.values, metric='cosine')
    mechanism_dist = np.nan_to_num(mechanism_dist, nan=0.0)
    mechanism_linkage = linkage(mechanism_dist, method='average')

    # Get dendrogram leaf order (used for row sorting in all heatmaps)
    disease_leaf_order = leaves_list(disease_linkage).tolist()
    mechanism_leaf_order = leaves_list(mechanism_linkage).tolist()

    disease_row_order = [disease_profiles.index[i] for i in disease_leaf_order]
    mechanism_row_order = [mechanism_profiles.index[i] for i in mechanism_leaf_order]

    # Save row orders (used by s07_visualize.py and downstream)
    cluster_labels = pd.DataFrame({
        'Site': disease_profiles.index,
        'disease_leaf_position': [disease_leaf_order.index(i) for i in range(len(SITES))],
        'mechanism_leaf_position': [mechanism_leaf_order.index(i) for i in range(len(SITES))],
    })
    cluster_labels.to_csv(os.path.join(OUTPUT_DIR, 'cluster_labels.csv'), index=False)

    # Save dendrogram data for visualization and downstream use
    dendrogram_data = {
        'disease_linkage': disease_linkage,
        'mechanism_linkage': mechanism_linkage,
        'sites': list(disease_profiles.index),
        'disease_row_order': disease_row_order,
        'mechanism_row_order': mechanism_row_order,
    }
    with open(os.path.join(OUTPUT_DIR, 'dendrogram_data.pkl'), 'wb') as f:
        pickle.dump(dendrogram_data, f)

    # --- Plot dendrograms ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Disease dendrogram
    dn1 = dendrogram(disease_linkage, labels=list(disease_profiles.index),
                     ax=ax1, leaf_rotation=45, leaf_font_size=10,
                     color_threshold=0)  # single color — no arbitrary cut
    ax1.set_title('Disease-Space Dendrogram', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cosine Distance')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    # Mechanism dendrogram
    dn2 = dendrogram(mechanism_linkage, labels=list(mechanism_profiles.index),
                     ax=ax2, leaf_rotation=45, leaf_font_size=10,
                     color_threshold=0)
    ax2.set_title('Mechanism-Space Dendrogram', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cosine Distance')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'dendrograms.png'), bbox_inches='tight')
    plt.close()
    print("Saved: dendrograms.png")

    # --- Print summary ---
    print("\nDisease-space dendrogram row order:", disease_row_order)
    print("Mechanism-space dendrogram row order:", mechanism_row_order)

    print("\nDisease-space merge distances:")
    for i, row in enumerate(disease_linkage):
        print(f"  Merge {i+1}: distance={row[2]:.4f}")

    print("\nMechanism-space merge distances:")
    for i, row in enumerate(mechanism_linkage):
        print(f"  Merge {i+1}: distance={row[2]:.4f}")

    print("\nDone. Saved to:", OUTPUT_DIR)


if __name__ == '__main__':
    main()
