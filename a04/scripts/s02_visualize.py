"""
Analysis 04 - Step 02: Visualization
Three-Space RSA scatterplots (fig4_rsa_scatterplots.png)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr
from itertools import combinations

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_DIR = os.path.dirname(BASE_DIR)

os.makedirs(FIG_DIR, exist_ok=True)

# Sites and anatomical pairs
SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
ANATOMICAL_PAIRS = [('BL25', 'GV4'), ('ST25', 'CV12'), ('PC6', 'LI4'), ('SP6', 'ST36')]
LABEL_PAIRS = ['BL25-GV4', 'BL25-ST25', 'ST25-CV12']


def load_rdm(path):
    """Load RDM from CSV with first column as index, return numpy array."""
    df = pd.read_csv(path, index_col=0)
    return df.values, list(df.index)


def get_pair_indices(sites):
    """Get all upper-triangle pair indices and labels."""
    pairs = list(combinations(range(len(sites)), 2))
    pair_labels = [f"{sites[i]}-{sites[j]}" for i, j in pairs]
    return pairs, pair_labels


def is_anatomical_pair(site_i, site_j, anatomical_pairs):
    """Check if a pair of sites is an anatomical pair."""
    for a, b in anatomical_pairs:
        if (site_i == a and site_j == b) or (site_i == b and site_j == a):
            return True
    return False


def main():
    # Load RDMs
    disease_rdm, sites = load_rdm(
        os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables', 'disease_rdm.csv'))
    mechanism_rdm, _ = load_rdm(
        os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables', 'mechanism_rdm.csv'))
    surface_rdm, _ = load_rdm(
        os.path.join(PROJECT_DIR, 'a02', 'results', 'datatables', 'surface_rdm.csv'))

    # Load mantel results for significance
    mantel_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'mantel_results.csv'))

    # Extract upper triangle vectors
    disease_vec = squareform(disease_rdm, checks=False)
    mechanism_vec = squareform(mechanism_rdm, checks=False)
    surface_vec = squareform(surface_rdm, checks=False)

    # Get pair info
    pairs, pair_labels = get_pair_indices(sites)

    # Color coding: anatomical pairs in red, rest in blue
    colors = []
    for i, j in pairs:
        if is_anatomical_pair(sites[i], sites[j], ANATOMICAL_PAIRS):
            colors.append('red')
        else:
            colors.append('blue')
    colors = np.array(colors)

    # Panel definitions
    panels = [
        {
            'x': disease_vec, 'y': mechanism_vec,
            'xlabel': 'Disease Distance', 'ylabel': 'Mechanism Distance',
            'title': 'Disease vs Mechanism',
            'test_name': 'Disease vs Mechanism'
        },
        {
            'x': surface_vec, 'y': disease_vec,
            'xlabel': 'Surface Body Distance', 'ylabel': 'Disease Distance',
            'title': 'Surface vs Disease',
            'test_name': 'Disease vs Surface'
        },
        {
            'x': surface_vec, 'y': mechanism_vec,
            'xlabel': 'Surface Body Distance', 'ylabel': 'Mechanism Distance',
            'title': 'Surface vs Mechanism',
            'test_name': 'Mechanism vs Surface'
        },
    ]

    # Create figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=150)

    for ax_idx, panel in enumerate(panels):
        ax = axes[ax_idx]
        x = panel['x']
        y = panel['y']

        # Get significance from mantel results
        mask = mantel_df['Test'] == panel['test_name']
        if mask.any():
            row = mantel_df[mask].iloc[0]
            r_val = row['r']
            p_val = row['p_value']
            is_sig = row['significant']
        else:
            r_val, _ = spearmanr(x, y)
            p_val = 1.0
            is_sig = False

        # Scatter plot
        for i in range(len(x)):
            ax.scatter(x[i], y[i], c=colors[i], alpha=0.7, s=50, edgecolors='k', linewidth=0.5)

        # Label key pairs
        for i, (pi, pj) in enumerate(pairs):
            label = pair_labels[i]
            if label in LABEL_PAIRS:
                ax.annotate(label, (x[i], y[i]), fontsize=7,
                           xytext=(5, 5), textcoords='offset points',
                           fontweight='bold')

        # Significance-dependent decoration
        if is_sig:
            # Add regression trend line
            sns.regplot(x=x, y=y, ax=ax, scatter=False,
                       color='gray', line_kws={'linewidth': 2, 'linestyle': '--'})
        else:
            # Add shaded 95% CI from permutation null
            np.random.seed(42)
            n = disease_rdm.shape[0]
            null_corrs = []
            for _ in range(10000):
                perm_idx = np.random.permutation(n)
                # Permute y-variable RDM
                if ax_idx == 0:
                    rdm_to_perm = mechanism_rdm
                elif ax_idx == 1:
                    rdm_to_perm = disease_rdm
                else:
                    rdm_to_perm = mechanism_rdm
                rdm_perm = rdm_to_perm[np.ix_(perm_idx, perm_idx)]
                vec_perm = squareform(rdm_perm, checks=False)
                null_r, _ = spearmanr(x, vec_perm)
                null_corrs.append(null_r)

            ci_low = np.percentile(null_corrs, 2.5)
            ci_high = np.percentile(null_corrs, 97.5)
            ax.axhspan(ax.get_ylim()[0], ax.get_ylim()[1], alpha=0.0)  # force ylim
            # Convert r-based CI to a horizontal band (visual indication)
            y_mean = np.mean(y)
            y_std = np.std(y)
            ax.axhline(y_mean, color='gray', linestyle=':', alpha=0.5)
            ax.fill_between(ax.get_xlim(),
                          y_mean + ci_low * y_std,
                          y_mean + ci_high * y_std,
                          alpha=0.15, color='gray', label='95% null CI')
            ax.legend(fontsize=8, loc='upper right')

        # Annotation with r and p
        p_str = f"p={p_val:.4f}" if p_val >= 0.0001 else "p<0.0001"
        sig_marker = " *" if is_sig else ""
        ax.text(0.5, 0.95, f"r={r_val:.3f}, {p_str}{sig_marker}",
               transform=ax.transAxes, fontsize=10, verticalalignment='top',
               horizontalalignment='center',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        ax.set_xlabel(panel['xlabel'], fontsize=11)
        ax.set_ylabel(panel['ylabel'], fontsize=11)
        ax.set_title(panel['title'], fontsize=13, fontweight='bold')

    # Legend for colors
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red',
               markersize=8, label='Anatomical pairs'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue',
               markersize=8, label='Other pairs'),
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=2, fontsize=10,
              bbox_to_anchor=(0.5, -0.02))

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.12)

    fig_path = os.path.join(FIG_DIR, 'fig4_rsa_scatterplots.png')
    plt.savefig(fig_path, bbox_inches='tight')
    plt.close()
    print(f"Saved: {fig_path}")


if __name__ == '__main__':
    main()
