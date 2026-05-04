"""
Step 2: PCA on proportional profiles.
Produces 2D embeddings, loadings, and variance explained.
"""
import pandas as pd
import numpy as np
import os
from sklearn.decomposition import PCA

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A03_DIR = os.path.join(os.path.dirname(BASE_DIR), 'a03', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')


def main():
    # Load profiles
    disease_profiles = pd.read_csv(os.path.join(A03_DIR, 'disease_profiles.csv'), index_col=0)
    mechanism_profiles = pd.read_csv(os.path.join(A03_DIR, 'mechanism_profiles.csv'), index_col=0)

    sites = disease_profiles.index.tolist()

    # PCA - Disease
    pca_disease = PCA(n_components=2)
    disease_coords = pca_disease.fit_transform(disease_profiles.values)
    disease_loadings = pca_disease.components_.T  # (n_features, n_components)
    disease_var = pca_disease.explained_variance_ratio_

    # PCA - Mechanism
    pca_mechanism = PCA(n_components=2)
    mechanism_coords = pca_mechanism.fit_transform(mechanism_profiles.values)
    mechanism_loadings = pca_mechanism.components_.T
    mechanism_var = pca_mechanism.explained_variance_ratio_

    print(f"Disease PCA variance explained: PC1={disease_var[0]:.3f}, PC2={disease_var[1]:.3f}")
    print(f"Mechanism PCA variance explained: PC1={mechanism_var[0]:.3f}, PC2={mechanism_var[1]:.3f}")

    # Save coordinates
    coords_df = pd.DataFrame({
        'Site': sites,
        'disease_pc1': disease_coords[:, 0],
        'disease_pc2': disease_coords[:, 1],
        'mechanism_pc1': mechanism_coords[:, 0],
        'mechanism_pc2': mechanism_coords[:, 1],
    })
    coords_path = os.path.join(OUTPUT_DIR, 'pca_coordinates.csv')
    coords_df.to_csv(coords_path, index=False)
    print(f"\nSaved: {coords_path}")

    # Save loadings
    disease_categories = disease_profiles.columns.tolist()
    mechanism_categories = mechanism_profiles.columns.tolist()

    # Combine loadings into one table (pad shorter list with NaN)
    max_len = max(len(disease_categories), len(mechanism_categories))
    disease_cats_padded = disease_categories + [None] * (max_len - len(disease_categories))
    mechanism_cats_padded = mechanism_categories + [None] * (max_len - len(mechanism_categories))

    disease_load_padded = np.vstack([
        disease_loadings,
        np.full((max_len - len(disease_categories), 2), np.nan)
    ]) if len(disease_categories) < max_len else disease_loadings

    mechanism_load_padded = np.vstack([
        mechanism_loadings,
        np.full((max_len - len(mechanism_categories), 2), np.nan)
    ]) if len(mechanism_categories) < max_len else mechanism_loadings

    loadings_df = pd.DataFrame({
        'disease_category': disease_cats_padded,
        'disease_pc1_loading': disease_load_padded[:, 0],
        'disease_pc2_loading': disease_load_padded[:, 1],
        'mechanism_category': mechanism_cats_padded,
        'mechanism_pc1_loading': mechanism_load_padded[:, 0],
        'mechanism_pc2_loading': mechanism_load_padded[:, 1],
    })
    loadings_path = os.path.join(OUTPUT_DIR, 'pca_loadings.csv')
    loadings_df.to_csv(loadings_path, index=False)
    print(f"Saved: {loadings_path}")

    # Save variance explained
    variance_df = pd.DataFrame({
        'component': ['PC1', 'PC2'],
        'disease_var_explained': disease_var,
        'mechanism_var_explained': mechanism_var,
    })
    variance_path = os.path.join(OUTPUT_DIR, 'pca_variance.csv')
    variance_df.to_csv(variance_path, index=False)
    print(f"Saved: {variance_path}")


if __name__ == '__main__':
    main()
