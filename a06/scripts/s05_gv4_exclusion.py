"""
Step 5: Sensitivity analysis — recompute embeddings excluding GV4.
"""
import pandas as pd
import numpy as np
import os
import sys
from sklearn.manifold import MDS
from sklearn.decomposition import PCA
from scipy.spatial.distance import cosine

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
A01_DIR = os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables')
A03_DIR = os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

sys.path.insert(0, os.path.join(PROJECT_DIR, 'a01', 'scripts'))

SITES_ALL = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
SITES_EXCL = [s for s in SITES_ALL if s != 'GV4']


def compute_rdm(profiles):
    """Compute cosine distance RDM from profiles."""
    n = profiles.shape[0]
    rdm = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                rdm[i, j] = cosine(profiles[i], profiles[j])
    return rdm


def correspondence_analysis(counts_df):
    """Perform CA on a count matrix. Returns row_scores, col_scores, inertia."""
    counts = counts_df.values.astype(float)
    total = counts.sum()
    P = counts / total
    r = P.sum(axis=1)
    c = P.sum(axis=0)

    Dr_inv_sqrt = np.diag(1.0 / np.sqrt(r))
    Dc_inv_sqrt = np.diag(1.0 / np.sqrt(c))

    expected = np.outer(r, c)
    residuals = P - expected
    S = Dr_inv_sqrt @ residuals @ Dc_inv_sqrt

    U, sigma, Vt = np.linalg.svd(S, full_matrices=False)
    V = Vt.T

    total_inertia = np.sum(sigma**2)
    inertia_explained = sigma**2 / total_inertia

    row_scores = Dr_inv_sqrt @ U[:, :2] * sigma[:2]
    col_scores = Dc_inv_sqrt @ V[:, :2] * sigma[:2]

    return row_scores, col_scores, inertia_explained


def main():
    # Load profiles and counts, exclude GV4
    disease_profiles = pd.read_csv(os.path.join(A03_DIR, 'disease_profiles.csv'), index_col=0)
    mechanism_profiles = pd.read_csv(os.path.join(A03_DIR, 'mechanism_profiles.csv'), index_col=0)
    disease_counts = pd.read_csv(os.path.join(A03_DIR, 'disease_counts.csv'), index_col=0)
    mechanism_counts = pd.read_csv(os.path.join(A03_DIR, 'mechanism_counts.csv'), index_col=0)

    # Exclude GV4
    disease_profiles_excl = disease_profiles.loc[SITES_EXCL]
    mechanism_profiles_excl = mechanism_profiles.loc[SITES_EXCL]
    disease_counts_excl = disease_counts.loc[SITES_EXCL]
    mechanism_counts_excl = mechanism_counts.loc[SITES_EXCL]

    # --- MDS ---
    disease_rdm = compute_rdm(disease_profiles_excl.values)
    mechanism_rdm = compute_rdm(mechanism_profiles_excl.values)

    mds_disease = MDS(n_components=2, metric='precomputed', metric_mds=True,
                      n_init=4, init='random', random_state=42, normalized_stress=False)
    disease_mds_coords = mds_disease.fit_transform(disease_rdm)

    mds_mechanism = MDS(n_components=2, metric='precomputed', metric_mds=True,
                        n_init=4, init='random', random_state=42, normalized_stress=False)
    mechanism_mds_coords = mds_mechanism.fit_transform(mechanism_rdm)

    mds_df = pd.DataFrame({
        'Site': SITES_EXCL,
        'disease_dim1': disease_mds_coords[:, 0],
        'disease_dim2': disease_mds_coords[:, 1],
        'mechanism_dim1': mechanism_mds_coords[:, 0],
        'mechanism_dim2': mechanism_mds_coords[:, 1],
        'disease_stress': mds_disease.stress_,
        'mechanism_stress': mds_mechanism.stress_,
    })
    mds_path = os.path.join(OUTPUT_DIR, 'gv4_exclusion_mds.csv')
    mds_df.to_csv(mds_path, index=False)
    print(f"Saved: {mds_path}")

    # --- PCA ---
    pca_disease = PCA(n_components=2)
    disease_pca_coords = pca_disease.fit_transform(disease_profiles_excl.values)

    pca_mechanism = PCA(n_components=2)
    mechanism_pca_coords = pca_mechanism.fit_transform(mechanism_profiles_excl.values)

    pca_df = pd.DataFrame({
        'Site': SITES_EXCL,
        'disease_pc1': disease_pca_coords[:, 0],
        'disease_pc2': disease_pca_coords[:, 1],
        'mechanism_pc1': mechanism_pca_coords[:, 0],
        'mechanism_pc2': mechanism_pca_coords[:, 1],
    })
    pca_path = os.path.join(OUTPUT_DIR, 'gv4_exclusion_pca.csv')
    pca_df.to_csv(pca_path, index=False)
    print(f"Saved: {pca_path}")

    # --- CA ---
    disease_row_scores, disease_col_scores, disease_inertia = correspondence_analysis(disease_counts_excl)
    mech_row_scores, mech_col_scores, mech_inertia = correspondence_analysis(mechanism_counts_excl)

    ca_df = pd.DataFrame({
        'Site': SITES_EXCL,
        'disease_ca_dim1': disease_row_scores[:, 0],
        'disease_ca_dim2': disease_row_scores[:, 1],
        'mechanism_ca_dim1': mech_row_scores[:, 0],
        'mechanism_ca_dim2': mech_row_scores[:, 1],
        'disease_inertia_dim1': disease_inertia[0],
        'disease_inertia_dim2': disease_inertia[1],
        'mechanism_inertia_dim1': mech_inertia[0],
        'mechanism_inertia_dim2': mech_inertia[1],
    })
    ca_path = os.path.join(OUTPUT_DIR, 'gv4_exclusion_ca.csv')
    ca_df.to_csv(ca_path, index=False)
    print(f"Saved: {ca_path}")

    # Save category scores for CA (needed for biplot)
    disease_cat_scores = pd.DataFrame({
        'category': disease_counts_excl.columns.tolist(),
        'disease_cat_dim1': disease_col_scores[:, 0],
        'disease_cat_dim2': disease_col_scores[:, 1],
    })
    disease_cat_scores.to_csv(
        os.path.join(OUTPUT_DIR, 'gv4_exclusion_ca_disease_cat.csv'), index=False)

    mech_cat_scores = pd.DataFrame({
        'category': mechanism_counts_excl.columns.tolist(),
        'mechanism_cat_dim1': mech_col_scores[:, 0],
        'mechanism_cat_dim2': mech_col_scores[:, 1],
    })
    mech_cat_scores.to_csv(
        os.path.join(OUTPUT_DIR, 'gv4_exclusion_ca_mechanism_cat.csv'), index=False)

    print("\nGV4 exclusion analysis complete.")


if __name__ == '__main__':
    main()
