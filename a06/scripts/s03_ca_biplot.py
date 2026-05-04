"""
Step 3: Correspondence Analysis (CA) biplot.
Manual implementation using SVD of standardized residuals.
Produces site scores and category scores for disease and mechanism spaces.
"""
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A03_DIR = os.path.join(os.path.dirname(BASE_DIR), 'a03', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')


def correspondence_analysis(counts_df):
    """
    Perform Correspondence Analysis on a count matrix.

    Returns:
        row_scores: site principal coordinates (n_sites, 2)
        col_scores: category principal coordinates (n_categories, 2)
        inertia: proportion of inertia explained per dimension
    """
    counts = counts_df.values.astype(float)
    total = counts.sum()

    # Correspondence matrix
    P = counts / total

    # Row and column masses
    r = P.sum(axis=1)  # row masses
    c = P.sum(axis=0)  # column masses

    # Standardized residuals
    # S_ij = (P_ij - r_i * c_j) / sqrt(r_i * c_j)
    Dr_inv_sqrt = np.diag(1.0 / np.sqrt(r))
    Dc_inv_sqrt = np.diag(1.0 / np.sqrt(c))

    expected = np.outer(r, c)
    residuals = P - expected
    S = Dr_inv_sqrt @ residuals @ Dc_inv_sqrt

    # SVD
    U, sigma, Vt = np.linalg.svd(S, full_matrices=False)
    V = Vt.T

    # Inertia (total and per dimension)
    total_inertia = np.sum(sigma**2)
    inertia_explained = sigma**2 / total_inertia

    # Principal coordinates (first 2 dimensions)
    # Row scores: D_r^(-1/2) * U * Sigma
    row_scores = Dr_inv_sqrt @ U[:, :2] * sigma[:2]

    # Column scores: D_c^(-1/2) * V * Sigma
    col_scores = Dc_inv_sqrt @ V[:, :2] * sigma[:2]

    return row_scores, col_scores, inertia_explained


def main():
    # Load count matrices
    disease_counts = pd.read_csv(os.path.join(A03_DIR, 'disease_counts.csv'), index_col=0)
    mechanism_counts = pd.read_csv(os.path.join(A03_DIR, 'mechanism_counts.csv'), index_col=0)

    sites = disease_counts.index.tolist()
    disease_categories = disease_counts.columns.tolist()
    mechanism_categories = mechanism_counts.columns.tolist()

    # CA - Disease
    disease_row_scores, disease_col_scores, disease_inertia = correspondence_analysis(disease_counts)

    # CA - Mechanism
    mech_row_scores, mech_col_scores, mech_inertia = correspondence_analysis(mechanism_counts)

    print(f"Disease CA inertia: Dim1={disease_inertia[0]:.3f}, Dim2={disease_inertia[1]:.3f}")
    print(f"Mechanism CA inertia: Dim1={mech_inertia[0]:.3f}, Dim2={mech_inertia[1]:.3f}")

    # Save scores
    # Site scores
    site_scores = pd.DataFrame({
        'Site': sites,
        'disease_ca_dim1': disease_row_scores[:, 0],
        'disease_ca_dim2': disease_row_scores[:, 1],
        'mechanism_ca_dim1': mech_row_scores[:, 0],
        'mechanism_ca_dim2': mech_row_scores[:, 1],
    })

    # Category scores - disease
    disease_cat_scores = pd.DataFrame({
        'category': disease_categories,
        'disease_cat_dim1': disease_col_scores[:, 0],
        'disease_cat_dim2': disease_col_scores[:, 1],
    })

    # Category scores - mechanism
    mech_cat_scores = pd.DataFrame({
        'category': mechanism_categories,
        'mechanism_cat_dim1': mech_col_scores[:, 0],
        'mechanism_cat_dim2': mech_col_scores[:, 1],
    })

    # Combine into one file
    scores_path = os.path.join(OUTPUT_DIR, 'ca_scores.csv')
    with open(scores_path, 'w') as f:
        f.write("# Site scores\n")
        site_scores.to_csv(f, index=False)
        f.write("\n# Disease category scores\n")
        disease_cat_scores.to_csv(f, index=False)
        f.write("\n# Mechanism category scores\n")
        mech_cat_scores.to_csv(f, index=False)

    # Also save as separate clean CSVs for easier loading
    site_scores.to_csv(os.path.join(OUTPUT_DIR, 'ca_site_scores.csv'), index=False)
    disease_cat_scores.to_csv(os.path.join(OUTPUT_DIR, 'ca_disease_cat_scores.csv'), index=False)
    mech_cat_scores.to_csv(os.path.join(OUTPUT_DIR, 'ca_mechanism_cat_scores.csv'), index=False)
    print(f"\nSaved: {scores_path}")

    # Save inertia
    max_dims = max(len(disease_inertia), len(mech_inertia))
    inertia_df = pd.DataFrame({
        'dimension': [f'Dim{i+1}' for i in range(max_dims)],
        'disease_inertia': list(disease_inertia[:max_dims]) + [np.nan] * (max_dims - len(disease_inertia)),
        'mechanism_inertia': list(mech_inertia[:max_dims]) + [np.nan] * (max_dims - len(mech_inertia)),
    })
    inertia_path = os.path.join(OUTPUT_DIR, 'ca_inertia.csv')
    inertia_df.to_csv(inertia_path, index=False)
    print(f"Saved: {inertia_path}")


if __name__ == '__main__':
    main()
