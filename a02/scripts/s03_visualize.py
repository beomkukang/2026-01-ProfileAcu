"""
Analysis 02 - Step 03: Visualization
Plot 1: Dual heatmap of surface and segmental RDMs.
Plot 2: Histogram of Mantel r (Spearman) between original and perturbed RDMs.
"""

import os
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
os.makedirs(FIG_DIR, exist_ok=True)

# --- Load data ---
surface_rdm_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'surface_rdm.csv'), index_col=0)
segmental_rdm_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'segmental_rdm.csv'), index_col=0)

surface_rdm = surface_rdm_df.values
segmental_rdm = segmental_rdm_df.values
sites = surface_rdm_df.index.tolist()

# ============================================================
# Plot 1: Somatotopic RDMs (two-panel heatmap)
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=150)

# Surface RDM
im1 = axes[0].imshow(surface_rdm, cmap='viridis', aspect='equal')
axes[0].set_xticks(range(len(sites)))
axes[0].set_xticklabels(sites, rotation=45, ha='right')
axes[0].set_yticks(range(len(sites)))
axes[0].set_yticklabels(sites)
axes[0].set_title('Surface Euclidean Distance (mm)', fontsize=12)
# Annotate values
for i in range(len(sites)):
    for j in range(len(sites)):
        val = surface_rdm[i, j]
        color = 'white' if val < surface_rdm.max() * 0.6 else 'black'
        axes[0].text(j, i, f'{val:.1f}', ha='center', va='center', fontsize=7, color=color)
plt.colorbar(im1, ax=axes[0], fraction=0.046, pad=0.04)

# Segmental RDM
im2 = axes[1].imshow(segmental_rdm, cmap='viridis', aspect='equal')
axes[1].set_xticks(range(len(sites)))
axes[1].set_xticklabels(sites, rotation=45, ha='right')
axes[1].set_yticks(range(len(sites)))
axes[1].set_yticklabels(sites)
axes[1].set_title('Segmental Distance (levels)', fontsize=12)
# Annotate values
for i in range(len(sites)):
    for j in range(len(sites)):
        val = segmental_rdm[i, j]
        color = 'white' if val < segmental_rdm.max() * 0.6 else 'black'
        axes[1].text(j, i, f'{int(val)}', ha='center', va='center', fontsize=7, color=color)
plt.colorbar(im2, ax=axes[1], fraction=0.046, pad=0.04)

plt.suptitle('Body-Space Representational Dissimilarity Matrices', fontsize=14, y=0.98)
plt.tight_layout()

fig_path_1 = os.path.join(FIG_DIR, 'somatotopic_rdms.png')
plt.savefig(fig_path_1, bbox_inches='tight')
plt.close()
print(f"Saved: {fig_path_1}")

# ============================================================
# Plot 2: Perturbation stability (Mantel r histogram)
# ============================================================
# Load perturbed RDMs
pkl_path = os.path.join(OUTPUT_DIR, 'perturbed_rdms.pkl')
with open(pkl_path, 'rb') as f:
    perturbed_rdms = pickle.load(f)

# Compute Mantel r (Spearman correlation between upper-triangle vectors)
original_vec = squareform(surface_rdm)  # condensed form (upper triangle)

mantel_rs = []
for prdm in perturbed_rdms:
    perturbed_vec = squareform(prdm)
    r, _ = spearmanr(original_vec, perturbed_vec)
    mantel_rs.append(r)

mantel_rs = np.array(mantel_rs)

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
ax.hist(mantel_rs, bins=50, color='steelblue', edgecolor='white', alpha=0.85)
ax.axvline(mantel_rs.mean(), color='red', linestyle='--', linewidth=1.5,
           label=f'Mean r = {mantel_rs.mean():.4f}')
ax.set_xlabel('Mantel r (Spearman)', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('Perturbation Stability: Original vs. Jittered RDMs\n'
             f'(N = {len(perturbed_rdms)} iterations, +/-15% jitter)', fontsize=12)
ax.legend(fontsize=10)
plt.tight_layout()

fig_path_2 = os.path.join(FIG_DIR, 'perturbation_stability.png')
plt.savefig(fig_path_2, bbox_inches='tight')
plt.close()
print(f"Saved: {fig_path_2}")

print(f"\nMantel r summary: mean={mantel_rs.mean():.4f}, std={mantel_rs.std():.4f}, "
      f"min={mantel_rs.min():.4f}, max={mantel_rs.max():.4f}")
