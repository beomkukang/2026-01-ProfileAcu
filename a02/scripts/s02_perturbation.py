"""
Analysis 02 - Step 02: Coordinate Perturbation Analysis
Jitter each coordinate by +/-15% over 1,000 iterations and recompute Euclidean RDMs.
Assess stability of the distance structure under coordinate uncertainty.
"""

import os
import pickle
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Parameters ---
N_ITER = 1000
JITTER_FRACTION = 0.15
np.random.seed(42)

# --- Load coordinates ---
coords_path = os.path.join(OUTPUT_DIR, 'site_coordinates.csv')
df = pd.read_csv(coords_path)
coords = df[['x', 'y', 'z']].values  # shape (8, 3)
n_sites = coords.shape[0]
n_pairs = n_sites * (n_sites - 1) // 2

print(f"Loaded coordinates for {n_sites} sites.")
print(f"Running {N_ITER} perturbation iterations with +/-{JITTER_FRACTION*100:.0f}% jitter...")

# --- Perturbation loop ---
# Apply same z-score normalization as s01_coordinates.py before computing distances
perturbed_rdms = []

for i in range(N_ITER):
    # Jitter each coordinate by uniform random in [-15%, +15%] of its value
    jitter = np.random.uniform(-JITTER_FRACTION, JITTER_FRACTION, size=coords.shape)
    perturbed_coords = coords * (1.0 + jitter)

    # Z-score normalize (equal axis weighting) then compute Euclidean RDM
    perturbed_norm = (perturbed_coords - perturbed_coords.mean(axis=0)) / perturbed_coords.std(axis=0)
    dist_vec = pdist(perturbed_norm, metric='euclidean')
    rdm = squareform(dist_vec)
    perturbed_rdms.append(rdm)

# --- Save perturbed RDMs ---
pkl_path = os.path.join(OUTPUT_DIR, 'perturbed_rdms.pkl')
with open(pkl_path, 'wb') as f:
    pickle.dump(perturbed_rdms, f)
print(f"Saved {N_ITER} perturbed RDMs to: {pkl_path}")

# --- Summary statistics ---
# Stack all RDMs and compute mean/std for each pairwise distance
all_rdms = np.array(perturbed_rdms)  # shape (1000, 8, 8)

sites = df['Site'].tolist()
print(f"\n--- Pairwise Distance Summary (mean +/- std across {N_ITER} perturbations) ---")
print(f"{'Pair':<12} {'Mean (mm)':>10} {'Std (mm)':>10}")
print("-" * 34)

for i in range(n_sites):
    for j in range(i + 1, n_sites):
        mean_d = all_rdms[:, i, j].mean()
        std_d = all_rdms[:, i, j].std()
        print(f"{sites[i]}-{sites[j]:<6} {mean_d:>10.2f} {std_d:>10.2f}")

print(f"\nDone. Overall mean distance: {all_rdms[all_rdms > 0].mean():.2f} mm")
print(f"Overall std of distances: {all_rdms[all_rdms > 0].std():.2f} mm")
