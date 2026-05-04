"""
Step 1: Classical MDS on cosine distance matrices.
Produces 2D embeddings for disease and mechanism spaces.
"""
import pandas as pd
import numpy as np
import os
from sklearn.manifold import MDS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A03_DIR = os.path.join(os.path.dirname(BASE_DIR), 'a03', 'results', 'datatables')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')


def main():
    # Load RDMs
    disease_rdm = pd.read_csv(os.path.join(A03_DIR, 'disease_rdm.csv'), index_col=0)
    mechanism_rdm = pd.read_csv(os.path.join(A03_DIR, 'mechanism_rdm.csv'), index_col=0)

    sites = disease_rdm.index.tolist()

    # Classical MDS - Disease
    mds_disease = MDS(
        n_components=2, metric='precomputed', metric_mds=True,
        n_init=4, init='random', random_state=42, normalized_stress=False
    )
    disease_coords = mds_disease.fit_transform(disease_rdm.values)
    disease_stress = mds_disease.stress_

    # Classical MDS - Mechanism
    mds_mechanism = MDS(
        n_components=2, metric='precomputed', metric_mds=True,
        n_init=4, init='random', random_state=42, normalized_stress=False
    )
    mechanism_coords = mds_mechanism.fit_transform(mechanism_rdm.values)
    mechanism_stress = mds_mechanism.stress_

    print(f"Disease MDS stress: {disease_stress:.6f}")
    print(f"Mechanism MDS stress: {mechanism_stress:.6f}")

    # Save coordinates
    result = pd.DataFrame({
        'Site': sites,
        'disease_dim1': disease_coords[:, 0],
        'disease_dim2': disease_coords[:, 1],
        'mechanism_dim1': mechanism_coords[:, 0],
        'mechanism_dim2': mechanism_coords[:, 1],
        'disease_stress': disease_stress,
        'mechanism_stress': mechanism_stress,
    })

    out_path = os.path.join(OUTPUT_DIR, 'mds_coordinates.csv')
    result.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")


if __name__ == '__main__':
    main()
