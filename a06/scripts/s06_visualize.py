"""
Step 6: Visualization — CA biplots (Fig 6) and supplementary figures.
"""
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Ellipse
from scipy.cluster.hierarchy import fcluster

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_DIR = os.path.dirname(BASE_DIR)
A03_DIR = os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
ANATOMICAL_PAIRS = [('BL25', 'GV4'), ('ST25', 'CV12'), ('PC6', 'LI4'), ('SP6', 'ST36')]

# 3-cluster color scheme (disease dendrogram)
CLUSTER_PALETTE = {
    1: '#2ca02c',   # GI cluster (BL25, ST25) — green
    2: '#1f77b4',   # Broad cluster (GV4, CV12, LI4, SP6, ST36) — blue
    3: '#d62728',   # Cardiovascular outlier (PC6) — red
}


def get_cluster_colors(sites):
    """Derive cluster assignments from disease dendrogram (3 clusters)."""
    dend_path = os.path.join(A03_DIR, 'dendrogram_data.pkl')
    with open(dend_path, 'rb') as f:
        dend_data = pickle.load(f)

    dend_sites = dend_data['sites']
    labels = fcluster(dend_data['disease_linkage'], t=3, criterion='maxclust')
    cluster_map = dict(zip(dend_sites, labels))

    color_map = {}
    for site in sites:
        c = cluster_map.get(site, 2)
        color_map[site] = CLUSTER_PALETTE[c]
    return color_map, cluster_map


# Per-site label offsets: (x_offset, y_offset) in points
# Adjust these to avoid overlapping labels
SITE_LABEL_OFFSETS = {
    'Disease': {
        'BL25': (20, -3), 'ST25': (20, 3), 'GV4': (0, -20), 'CV12': (0, -18),
        'PC6': (0, 7), 'LI4': (3, -20), 'SP6': (0, 7), 'ST36': (0, 7),
    },
    'Mechanism': {
        'BL25': (0, 10), 'ST25': (0, -18), 'GV4': (0, 10), 'CV12': (0, -18),
        'PC6': (0, 7), 'LI4': (0, -20), 'SP6': (20, -5), 'ST36': (0, -20),
    },
}


def plot_ca_biplot(ax, site_scores, cat_scores, sites, categories,
                   color_map, inertia, space_name, pairs=ANATOMICAL_PAIRS,
                   n_cat_labels=5, offset_overlap=True):
    """Plot CA biplot: sites (colored dots) + categories (triangles) + pair lines."""
    site_idx = {s: i for i, s in enumerate(sites)}
    label_offsets = SITE_LABEL_OFFSETS.get(space_name, {})

    # Anatomical pair connections
    for s1, s2 in pairs:
        if s1 in site_idx and s2 in site_idx:
            i1, i2 = site_idx[s1], site_idx[s2]
            ax.plot([site_scores[i1, 0], site_scores[i2, 0]],
                    [site_scores[i1, 1], site_scores[i2, 1]],
                    '--', color='gray', alpha=0.5, linewidth=1, zorder=1)

    # Category positions (gray triangles)
    ax.scatter(cat_scores[:, 0], cat_scores[:, 1],
               marker='^', s=30, c='gray', alpha=0.5, zorder=3)

    # Only label the most extreme categories (furthest from origin)
    cat_dists = np.sqrt(cat_scores[:, 0]**2 + cat_scores[:, 1]**2)
    top_indices = np.argsort(cat_dists)[-n_cat_labels:]

    for j in top_indices:
        # Check if this category triangle is near any site dot
        cat_pos = cat_scores[j]
        min_dist_to_site = min(
            np.sqrt((site_scores[i, 0] - cat_pos[0])**2 +
                     (site_scores[i, 1] - cat_pos[1])**2)
            for i in range(len(sites))
        )

        if offset_overlap and min_dist_to_site < 0.15:
            # Close to a site — use offset label with connector line
            ax.annotate(categories[j], (cat_scores[j, 0], cat_scores[j, 1]),
                        fontsize=7, alpha=0.7, ha='center', va='bottom',
                        xytext=(20, 20), textcoords='offset points',
                        style='italic',
                        arrowprops=dict(arrowstyle='-', color='gray',
                                        alpha=0.5, linewidth=0.8))
        else:
            # Far from sites — label directly
            ax.annotate(categories[j], (cat_scores[j, 0], cat_scores[j, 1]),
                        fontsize=7, alpha=0.7, ha='center', va='bottom',
                        xytext=(0, 4), textcoords='offset points',
                        style='italic')

    # Site positions (colored circles with labels)
    for i, site in enumerate(sites):
        color = color_map.get(site, '#7f7f7f')
        ax.scatter(site_scores[i, 0], site_scores[i, 1],
                   s=120, c=color, edgecolors='black', linewidth=0.8,
                   zorder=5)
        offset = label_offsets.get(site, (0, 7))
        ax.annotate(site, (site_scores[i, 0], site_scores[i, 1]),
                    fontsize=9, fontweight='bold', ha='center', va='bottom',
                    xytext=offset, textcoords='offset points', zorder=6)

    # Axes
    ax.set_xlabel(f"Dimension 1 ({inertia[0]*100:.1f}% inertia)", fontsize=11)
    ax.set_ylabel(f"Dimension 2 ({inertia[1]*100:.1f}% inertia)", fontsize=11)
    ax.set_title(f"{space_name} Space", fontsize=13, fontweight='bold')
    ax.axhline(0, color='lightgray', linewidth=0.5, zorder=0)
    ax.axvline(0, color='lightgray', linewidth=0.5, zorder=0)


def plot_mds(ax, coords, sites, color_map, space_name,
             ellipses_data=None, pairs=ANATOMICAL_PAIRS):
    """Plot MDS embedding with optional bootstrap ellipses (supplementary)."""
    site_idx = {s: i for i, s in enumerate(sites)}

    for s1, s2 in pairs:
        if s1 in site_idx and s2 in site_idx:
            i1, i2 = site_idx[s1], site_idx[s2]
            ax.plot([coords[i1, 0], coords[i2, 0]],
                    [coords[i1, 1], coords[i2, 1]],
                    '--', color='gray', alpha=0.5, linewidth=1, zorder=1)

    # Bootstrap ellipses
    if ellipses_data is not None:
        for site in sites:
            if site in ellipses_data:
                ell_data = ellipses_data[site]
                ellipse = Ellipse(
                    xy=ell_data['center'],
                    width=ell_data['width'],
                    height=ell_data['height'],
                    angle=ell_data['angle'],
                    alpha=0.15,
                    color=color_map.get(site, '#7f7f7f'),
                    zorder=2,
                )
                ax.add_patch(ellipse)

    for i, site in enumerate(sites):
        color = color_map.get(site, '#7f7f7f')
        ax.scatter(coords[i, 0], coords[i, 1],
                   s=120, c=color, edgecolors='black', linewidth=0.8, zorder=4)
        ax.annotate(site, (coords[i, 0], coords[i, 1]),
                    fontsize=9, fontweight='bold', ha='center', va='bottom',
                    xytext=(0, 7), textcoords='offset points')

    ax.set_xlabel("MDS Dimension 1", fontsize=11)
    ax.set_ylabel("MDS Dimension 2", fontsize=11)
    ax.set_title(f"{space_name} Space (MDS)", fontsize=13, fontweight='bold')
    ax.axhline(0, color='lightgray', linewidth=0.5, zorder=0)
    ax.axvline(0, color='lightgray', linewidth=0.5, zorder=0)


def main():
    # Load data
    ca_site_scores = pd.read_csv(os.path.join(OUTPUT_DIR, 'ca_site_scores.csv'))
    ca_disease_cat = pd.read_csv(os.path.join(OUTPUT_DIR, 'ca_disease_cat_scores.csv'))
    ca_mech_cat = pd.read_csv(os.path.join(OUTPUT_DIR, 'ca_mechanism_cat_scores.csv'))
    ca_inertia = pd.read_csv(os.path.join(OUTPUT_DIR, 'ca_inertia.csv'))
    mds_coords = pd.read_csv(os.path.join(OUTPUT_DIR, 'mds_coordinates.csv'))

    # Cluster-based colors (same for both panels)
    sites = ca_site_scores['Site'].tolist()
    color_map, cluster_map = get_cluster_colors(sites)

    # Extract coordinates
    disease_site_coords = ca_site_scores[['disease_ca_dim1', 'disease_ca_dim2']].values
    mechanism_site_coords = ca_site_scores[['mechanism_ca_dim1', 'mechanism_ca_dim2']].values
    disease_cat_coords = ca_disease_cat[['disease_cat_dim1', 'disease_cat_dim2']].values
    mechanism_cat_coords = ca_mech_cat[['mechanism_cat_dim1', 'mechanism_cat_dim2']].values
    disease_categories = ca_disease_cat['category'].tolist()
    mechanism_categories = ca_mech_cat['category'].tolist()
    disease_inertia = ca_inertia['disease_inertia'].values
    mechanism_inertia = ca_inertia['mechanism_inertia'].values

    # --- Fig 6: CA biplots (no ellipses) ---
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    plot_ca_biplot(axes[0], disease_site_coords, disease_cat_coords,
                   sites, disease_categories, color_map,
                   disease_inertia, "Disease")

    plot_ca_biplot(axes[1], mechanism_site_coords, mechanism_cat_coords,
                   sites, mechanism_categories, color_map,
                   mechanism_inertia, "Mechanism")

    # Shared legend
    legend_handles = [
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=CLUSTER_PALETTE[1],
                       markersize=10, markeredgecolor='black', markeredgewidth=0.5,
                       label='GI cluster (BL25, ST25)'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=CLUSTER_PALETTE[2],
                       markersize=10, markeredgecolor='black', markeredgewidth=0.5,
                       label='Broad cluster'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor=CLUSTER_PALETTE[3],
                       markersize=10, markeredgecolor='black', markeredgewidth=0.5,
                       label='CV outlier (PC6)'),
        mlines.Line2D([], [], linestyle='--', color='gray', alpha=0.5,
                       label='Anatomical pair'),
        mlines.Line2D([], [], marker='^', color='w', markerfacecolor='gray',
                       markersize=8, alpha=0.6, label='Category position'),
    ]
    fig.legend(handles=legend_handles, loc='lower center', ncol=5, fontsize=9,
               bbox_to_anchor=(0.5, -0.05), columnspacing=2.0, handletextpad=0.8)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.10)
    fig_path = os.path.join(FIG_DIR, 'fig6_embeddings.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {fig_path}")

    # Load bootstrap ellipses for supplementary figures
    ellipses_path = os.path.join(OUTPUT_DIR, 'bootstrap_ellipses.pkl')
    if os.path.exists(ellipses_path):
        with open(ellipses_path, 'rb') as f:
            ellipses = pickle.load(f)
    else:
        print("Warning: bootstrap_ellipses.pkl not found. Supplementary plots without ellipses.")
        ellipses = None

    # Load PCA data
    pca_coords = pd.read_csv(os.path.join(OUTPUT_DIR, 'pca_coordinates.csv'))
    pca_var = pd.read_csv(os.path.join(OUTPUT_DIR, 'pca_variance.csv'))

    # --- Supplementary: S1 (Disease: MDS + PCA) and S2 (Mechanism: MDS + PCA) ---
    for space, mds_dim1, mds_dim2, ell_key, pca_dim1, pca_dim2, var_col, fig_label in [
        ('Disease', 'disease_dim1', 'disease_dim2', 'disease',
         'disease_pc1', 'disease_pc2', 'disease_var_explained', 'S1'),
        ('Mechanism', 'mechanism_dim1', 'mechanism_dim2', 'mechanism',
         'mechanism_pc1', 'mechanism_pc2', 'mechanism_var_explained', 'S2'),
    ]:
        fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(14, 6))

        # Panel A: MDS with bootstrap ellipses
        mds_xy = mds_coords[[mds_dim1, mds_dim2]].values
        ell_data = ellipses[ell_key] if ellipses else None
        plot_mds(ax_a, mds_xy, sites, color_map, space, ellipses_data=ell_data)
        ax_a.set_title(f"(A) {space} Space (MDS)", fontsize=13, fontweight='bold')

        # Panel B: PCA
        pca_xy = pca_coords[[pca_dim1, pca_dim2]].values
        site_idx_pca = {s: i for i, s in enumerate(sites)}
        for s1, s2 in ANATOMICAL_PAIRS:
            if s1 in site_idx_pca and s2 in site_idx_pca:
                i1, i2 = site_idx_pca[s1], site_idx_pca[s2]
                ax_b.plot([pca_xy[i1, 0], pca_xy[i2, 0]],
                          [pca_xy[i1, 1], pca_xy[i2, 1]],
                          '--', color='gray', alpha=0.5, linewidth=1, zorder=1)
        for i, site in enumerate(sites):
            color = color_map.get(site, '#7f7f7f')
            ax_b.scatter(pca_xy[i, 0], pca_xy[i, 1],
                         s=120, c=color, edgecolors='black', linewidth=0.8, zorder=4)
            ax_b.annotate(site, (pca_xy[i, 0], pca_xy[i, 1]),
                          fontsize=9, fontweight='bold', ha='center', va='bottom',
                          xytext=(0, 7), textcoords='offset points')
        var1 = pca_var[var_col].iloc[0] * 100
        var2 = pca_var[var_col].iloc[1] * 100
        ax_b.set_xlabel(f"PC1 ({var1:.1f}% variance)", fontsize=11)
        ax_b.set_ylabel(f"PC2 ({var2:.1f}% variance)", fontsize=11)
        ax_b.set_title(f"(B) {space} Space (PCA)", fontsize=13, fontweight='bold')
        ax_b.axhline(0, color='lightgray', linewidth=0.5, zorder=0)
        ax_b.axvline(0, color='lightgray', linewidth=0.5, zorder=0)

        plt.tight_layout()
        fig_path = os.path.join(FIG_DIR, f'fig{fig_label}_alt_{space.lower()}.png')
        fig.savefig(fig_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved: {fig_path}")

    # --- Supplementary: GV4 exclusion ---
    gv4_ca_path = os.path.join(OUTPUT_DIR, 'gv4_exclusion_ca.csv')
    if os.path.exists(gv4_ca_path):
        gv4_ca = pd.read_csv(gv4_ca_path)
        gv4_disease_cat = pd.read_csv(
            os.path.join(OUTPUT_DIR, 'gv4_exclusion_ca_disease_cat.csv'))
        gv4_mech_cat = pd.read_csv(
            os.path.join(OUTPUT_DIR, 'gv4_exclusion_ca_mechanism_cat.csv'))

        sites_excl = gv4_ca['Site'].tolist()
        pairs_excl = [(s1, s2) for s1, s2 in ANATOMICAL_PAIRS
                      if s1 != 'GV4' and s2 != 'GV4']

        fig, axes = plt.subplots(1, 2, figsize=(15, 6))

        disease_site_excl = gv4_ca[['disease_ca_dim1', 'disease_ca_dim2']].values
        mechanism_site_excl = gv4_ca[['mechanism_ca_dim1', 'mechanism_ca_dim2']].values
        disease_cat_excl = gv4_disease_cat[['disease_cat_dim1', 'disease_cat_dim2']].values
        mechanism_cat_excl = gv4_mech_cat[['mechanism_cat_dim1', 'mechanism_cat_dim2']].values

        disease_inertia_excl = [gv4_ca['disease_inertia_dim1'].iloc[0],
                                gv4_ca['disease_inertia_dim2'].iloc[0]]
        mechanism_inertia_excl = [gv4_ca['mechanism_inertia_dim1'].iloc[0],
                                  gv4_ca['mechanism_inertia_dim2'].iloc[0]]

        plot_ca_biplot(axes[0], disease_site_excl, disease_cat_excl,
                       sites_excl, gv4_disease_cat['category'].tolist(),
                       color_map, disease_inertia_excl,
                       "Disease (GV4 excluded)", pairs=pairs_excl)

        plot_ca_biplot(axes[1], mechanism_site_excl, mechanism_cat_excl,
                       sites_excl, gv4_mech_cat['category'].tolist(),
                       color_map, mechanism_inertia_excl,
                       "Mechanism (GV4 excluded)", pairs=pairs_excl,
                       offset_overlap=False)

        plt.tight_layout()
        fig_path = os.path.join(FIG_DIR, 'figS4_gv4_exclusion.png')
        fig.savefig(fig_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"Saved: {fig_path}")
    else:
        print("Warning: GV4 exclusion CA results not found. Skipping figS4.")

    print("\nAll visualizations complete.")


if __name__ == '__main__':
    main()
