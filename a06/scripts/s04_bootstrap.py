"""
Step 4: Bootstrap confidence ellipses for MDS embeddings.
1,000 bootstrap iterations with Procrustes alignment.
"""
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.manifold import MDS
from scipy.spatial.distance import cosine
from scipy.linalg import orthogonal_procrustes

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
A01_DIR = os.path.join(PROJECT_DIR, 'a01', 'results', 'datatables')
A03_DIR = os.path.join(PROJECT_DIR, 'a03', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']
N_BOOT = 1000
np.random.seed(42)


def compute_profiles(df, column, categories, sites):
    """Compute proportional profiles from classified data."""
    profiles = np.zeros((len(sites), len(categories)))
    for i, site in enumerate(sites):
        site_data = df[df['Site'] == site]
        total = len(site_data)
        if total == 0:
            continue
        for j, cat in enumerate(categories):
            profiles[i, j] = (site_data[column] == cat).sum() / total
    return profiles


def compute_rdm(profiles):
    """Compute cosine distance RDM from profiles."""
    n = profiles.shape[0]
    rdm = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                rdm[i, j] = cosine(profiles[i], profiles[j])
    return rdm


def procrustes_align(target, source):
    """Align source to target using orthogonal Procrustes."""
    # Center both
    target_centered = target - target.mean(axis=0)
    source_centered = source - source.mean(axis=0)

    # Find optimal rotation
    R, _ = orthogonal_procrustes(source_centered, target_centered)
    aligned = source_centered @ R + target.mean(axis=0)
    return aligned


def compute_confidence_ellipse(points, confidence=0.95):
    """
    Compute 95% confidence ellipse parameters from bootstrap points.
    Returns center, width, height, angle (degrees).
    """
    center = np.mean(points, axis=0)
    cov = np.cov(points.T)

    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    # Sort by descending eigenvalue
    order = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]

    # Chi-squared value for 95% confidence with 2 dof
    from scipy.stats import chi2
    chi2_val = chi2.ppf(confidence, 2)

    width = 2 * np.sqrt(eigenvalues[0] * chi2_val)
    height = 2 * np.sqrt(eigenvalues[1] * chi2_val)
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))

    return {
        'center': center,
        'width': width,
        'height': height,
        'angle': angle,
    }


def main():
    # Load combined data
    combined = pd.read_csv(os.path.join(A01_DIR, 'combined_data.csv'))

    # Load dictionaries and merge categories
    disease_dict = pd.read_csv(os.path.join(A01_DIR, 'disease_dictionary.csv'))
    mechanism_dict = pd.read_csv(os.path.join(A01_DIR, 'mechanism_dictionary.csv'))

    disease_map = disease_dict[['disease_string', 'level_7']].drop_duplicates()
    mechanism_map = mechanism_dict[['mechanism_string', 'level_8']].drop_duplicates()

    combined = combined.merge(disease_map, left_on='Disease', right_on='disease_string', how='left')
    combined = combined.merge(mechanism_map, left_on='Mechanism', right_on='mechanism_string', how='left')
    combined = combined.rename(columns={'level_7': 'disease_category', 'level_8': 'mechanism_category'})
    combined = combined.dropna(subset=['disease_category', 'mechanism_category'])

    # Load original profiles to get category lists
    disease_profiles_df = pd.read_csv(os.path.join(A03_DIR, 'disease_profiles.csv'), index_col=0)
    mechanism_profiles_df = pd.read_csv(os.path.join(A03_DIR, 'mechanism_profiles.csv'), index_col=0)
    disease_categories = disease_profiles_df.columns.tolist()
    mechanism_categories = mechanism_profiles_df.columns.tolist()

    # Load original MDS coordinates as reference for Procrustes
    mds_coords = pd.read_csv(os.path.join(OUTPUT_DIR, 'mds_coordinates.csv'))
    original_disease_coords = mds_coords[['disease_dim1', 'disease_dim2']].values
    original_mechanism_coords = mds_coords[['mechanism_dim1', 'mechanism_dim2']].values

    print(f"Classified records: {len(combined)}")

    # Bootstrap
    print(f"Running {N_BOOT} bootstrap iterations...")
    disease_boot_coords = np.zeros((N_BOOT, len(SITES), 2))
    mechanism_boot_coords = np.zeros((N_BOOT, len(SITES), 2))

    mds_disease = MDS(n_components=2, metric='precomputed', metric_mds=True,
                      n_init=1, init='random', random_state=42, normalized_stress=False)
    mds_mechanism = MDS(n_components=2, metric='precomputed', metric_mds=True,
                        n_init=1, init='random', random_state=42, normalized_stress=False)

    for boot_idx in range(N_BOOT):
        if (boot_idx + 1) % 100 == 0:
            print(f"  Iteration {boot_idx + 1}/{N_BOOT}")

        # Resample within each site
        boot_dfs = []
        for site in SITES:
            site_data = combined[combined['Site'] == site]
            resampled = site_data.sample(n=len(site_data), replace=True)
            boot_dfs.append(resampled)
        boot_combined = pd.concat(boot_dfs, ignore_index=True)

        # Compute profiles
        disease_profiles = compute_profiles(
            boot_combined, 'disease_category', disease_categories, SITES)
        mechanism_profiles = compute_profiles(
            boot_combined, 'mechanism_category', mechanism_categories, SITES)

        # Compute RDMs
        disease_rdm = compute_rdm(disease_profiles)
        mechanism_rdm = compute_rdm(mechanism_profiles)

        # MDS
        try:
            d_coords = mds_disease.fit_transform(disease_rdm)
            m_coords = mds_mechanism.fit_transform(mechanism_rdm)

            # Procrustes alignment to original
            d_coords = procrustes_align(original_disease_coords, d_coords)
            m_coords = procrustes_align(original_mechanism_coords, m_coords)

            disease_boot_coords[boot_idx] = d_coords
            mechanism_boot_coords[boot_idx] = m_coords
        except Exception:
            # If MDS fails, use previous iteration's values
            if boot_idx > 0:
                disease_boot_coords[boot_idx] = disease_boot_coords[boot_idx - 1]
                mechanism_boot_coords[boot_idx] = mechanism_boot_coords[boot_idx - 1]

    # Compute confidence ellipses
    print("Computing confidence ellipses...")
    ellipses = {'disease': {}, 'mechanism': {}}

    for i, site in enumerate(SITES):
        disease_points = disease_boot_coords[:, i, :]
        mechanism_points = mechanism_boot_coords[:, i, :]

        ellipses['disease'][site] = compute_confidence_ellipse(disease_points)
        ellipses['mechanism'][site] = compute_confidence_ellipse(mechanism_points)

    # Save
    out_path = os.path.join(OUTPUT_DIR, 'bootstrap_ellipses.pkl')
    with open(out_path, 'wb') as f:
        pickle.dump(ellipses, f)
    print(f"\nSaved: {out_path}")


if __name__ == '__main__':
    main()
