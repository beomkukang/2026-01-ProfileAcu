"""
Analysis 05 - Step 03: Visualization
=====================================
Generates fig5_coupling.png with:
  Panel A: Bar plot of top-3 concentration per site
  Panel B: Bubble contingency plots for specialist, middle, generalist sites
"""

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
PROJECT_ROOT = os.path.dirname(BASE_DIR)

os.makedirs(FIG_DIR, exist_ok=True)

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def load_inputs():
    """Load coupling metrics and contingency tables."""
    metrics_path = os.path.join(OUTPUT_DIR, 'coupling_metrics.csv')
    pkl_path = os.path.join(OUTPUT_DIR, 'contingency_tables.pkl')

    metrics = pd.read_csv(metrics_path)
    with open(pkl_path, 'rb') as f:
        contingency_tables = pickle.load(f)

    # Try to load cluster labels
    cluster_path = os.path.join(PROJECT_ROOT, 'a03', 'results', 'datatables', 'cluster_labels.csv')
    cluster_labels = None
    if os.path.exists(cluster_path):
        try:
            cluster_labels = pd.read_csv(cluster_path)
            print(f"Loaded cluster labels from {cluster_path}")
        except Exception as e:
            print(f"Warning: Could not load cluster labels: {e}")
    else:
        print(f"Note: cluster_labels.csv not found at {cluster_path} — using single color")

    return metrics, contingency_tables, cluster_labels


def get_cluster_colors(metrics, cluster_labels):
    """Assign colors based on cluster membership if available."""
    if cluster_labels is not None and 'Site' in cluster_labels.columns:
        # Determine which cluster column to use
        cluster_col = None
        for col in ['disease_cluster', 'mechanism_cluster']:
            if col in cluster_labels.columns:
                cluster_col = col
                break

        if cluster_col is not None:
            site_cluster = cluster_labels.set_index('Site')[cluster_col].to_dict()
            unique_clusters = sorted(set(site_cluster.values()))
            palette = sns.color_palette('Set2', n_colors=len(unique_clusters))
            cluster_color_map = {c: palette[i] for i, c in enumerate(unique_clusters)}

            colors = []
            for site in metrics['site']:
                c = site_cluster.get(site, unique_clusters[0])
                colors.append(cluster_color_map[c])
            return colors

    # Fallback: single color
    return ['#4C72B0'] * len(metrics)


def plot_panel_a(ax, metrics, colors):
    """Panel A: Bar plot of top-3 concentration, ordered descending."""
    # Sort by top3_concentration descending
    metrics_sorted = metrics.sort_values('top3_concentration', ascending=False).reset_index(drop=True)

    # Reorder colors to match
    color_order = []
    for site in metrics_sorted['site']:
        idx = metrics[metrics['site'] == site].index[0]
        color_order.append(colors[idx])

    bars = ax.bar(
        range(len(metrics_sorted)),
        metrics_sorted['top3_concentration'],
        color=color_order,
        edgecolor='black',
        linewidth=0.5
    )

    ax.set_xticks(range(len(metrics_sorted)))
    ax.set_xticklabels(metrics_sorted['site'], rotation=0, fontsize=9)
    ax.set_ylabel('% in top 3 cells', fontsize=10)
    ax.set_xlabel('Acupoint', fontsize=10)
    ax.set_title('(A) Top-3 Cell Concentration', fontsize=11, fontweight='bold', loc='left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0, max(metrics_sorted['top3_concentration']) * 1.15)

    # Add value labels
    for i, v in enumerate(metrics_sorted['top3_concentration']):
        ax.text(i, v + 0.5, f'{v:.1f}%', ha='center', va='bottom', fontsize=7)


def plot_bubble(ax, ct, title, max_pct):
    """Single bubble contingency plot using within-site percentages."""
    # Compute within-site percentages
    total = ct.values.sum()
    rows_list = []
    for disease in ct.index:
        for mechanism in ct.columns:
            count = ct.loc[disease, mechanism]
            if count > 0:
                rows_list.append({
                    'disease': disease,
                    'mechanism': mechanism,
                    'pct': count / total * 100
                })

    if not rows_list:
        ax.set_title(title)
        return

    bubble_df = pd.DataFrame(rows_list)

    # Map to numeric positions (each plot uses its own categories)
    diseases = sorted(ct.index.tolist())
    mechanisms = sorted(ct.columns.tolist())

    disease_pos = {d: i for i, d in enumerate(diseases)}
    mech_pos = {m: i for i, m in enumerate(mechanisms)}

    x = bubble_df['mechanism'].map(mech_pos)
    y = bubble_df['disease'].map(disease_pos)

    # Size scaling: consistent across panels via shared max_pct
    sizes = bubble_df['pct'] / max_pct * 500

    ax.scatter(x, y, s=sizes, alpha=0.6, c='#4C72B0', edgecolors='black', linewidth=0.3)

    ax.set_xticks(range(len(mechanisms)))
    ax.set_xticklabels(mechanisms, rotation=45, ha='right', fontsize=7)
    ax.set_yticks(range(len(diseases)))
    ax.set_yticklabels(diseases, fontsize=7)
    ax.set_xlim(-0.5, len(mechanisms) - 0.5)
    ax.set_ylim(-0.5, len(diseases) - 0.5)
    ax.set_title(title, fontsize=9, fontweight='bold', loc='left')
    ax.grid(True, alpha=0.2)


def plot_panel_b(axes, metrics, contingency_tables):
    """Panel B: 4 bubble plots for specialist, middle, PC6, generalist."""
    metrics_sorted = metrics.sort_values('top3_concentration', ascending=False).reset_index(drop=True)

    # Pick top (specialist), middle, PC6 (disease specialist / mechanism generalist), bottom (generalist)
    n = len(metrics_sorted)
    specialist_site = metrics_sorted.iloc[0]['site']
    middle_site = metrics_sorted.iloc[n // 2]['site']
    generalist_site = metrics_sorted.iloc[-1]['site']

    selected = [
        (specialist_site, 'Specialist'),
        (middle_site, 'Middle'),
        ('PC6', 'Disease specialist'),
        (generalist_site, 'Generalist'),
    ]

    # Determine consistent size scaling: max within-site percentage across all selected
    max_pct = 1
    for site, _ in selected:
        if site in contingency_tables:
            ct = contingency_tables[site]
            total = ct.values.sum()
            site_max_pct = ct.values.max() / total * 100
            if site_max_pct > max_pct:
                max_pct = site_max_pct

    # Pick legend tick values based on max_pct
    if max_pct > 20:
        legend_sizes_pct = [5, 10, 20]
    elif max_pct > 10:
        legend_sizes_pct = [2, 5, 15]
    else:
        legend_sizes_pct = [1, 3, 8]

    for i, (site, label) in enumerate(selected):
        if site in contingency_tables:
            ct = contingency_tables[site]
            top3_val = metrics[metrics['site'] == site]['top3_concentration'].values[0]
            prefix = '(B) ' if i == 0 else ''
            title = f'{prefix}{site} ({label}, top3={top3_val:.1f}%)'
            plot_bubble(axes[i], ct, title, max_pct)
        else:
            axes[i].set_title(f'{site} — no data')

    # Single shared size legend on the top-right bubble plot
    legend_bubbles = []
    legend_labels = []
    for pct_val in legend_sizes_pct:
        s = pct_val / max_pct * 500
        legend_bubbles.append(
            axes[0].scatter([], [], s=s, c='#4C72B0', alpha=0.6,
                            edgecolors='black', linewidth=0.3)
        )
        legend_labels.append(f'{pct_val:.0f}%')
    axes[0].legend(legend_bubbles, legend_labels, title='% of site',
                   loc='lower right', bbox_to_anchor=(1.0, 1.05),
                   ncol=3, fontsize=8, title_fontsize=9,
                   framealpha=0.9, handletextpad=1.5, borderpad=1.2,
                   columnspacing=2.0, labelspacing=1.5)


def main():
    print("=" * 60)
    print("A05 Step 03: Visualization")
    print("=" * 60)

    metrics, contingency_tables, cluster_labels = load_inputs()
    colors = get_cluster_colors(metrics, cluster_labels)

    # Create figure with GridSpec: 3 columns (bar chart | 2 bubbles | 2 bubbles)
    fig = plt.figure(figsize=(22, 12), dpi=150)
    gs = gridspec.GridSpec(2, 3, width_ratios=[0.3, 0.35, 0.35], hspace=0.5, wspace=0.35)

    # Panel A: left column, spanning both rows
    ax_a = fig.add_subplot(gs[:, 0])
    plot_panel_a(ax_a, metrics, colors)

    # Panel B: 4 bubble plots in a 2x2 grid (columns 2-3)
    ax_b1 = fig.add_subplot(gs[0, 1])  # specialist (top-left)
    ax_b2 = fig.add_subplot(gs[1, 1])  # middle (bottom-left)
    ax_b3 = fig.add_subplot(gs[0, 2])  # PC6 (top-right)
    ax_b4 = fig.add_subplot(gs[1, 2])  # generalist (bottom-right)
    axes_b = [ax_b1, ax_b2, ax_b3, ax_b4]

    plot_panel_b(axes_b, metrics, contingency_tables)


    # Save
    fig_path = os.path.join(FIG_DIR, 'fig5_coupling.png')
    plt.savefig(fig_path, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"\nSaved: {fig_path}")
    print("Done.")


if __name__ == '__main__':
    main()
