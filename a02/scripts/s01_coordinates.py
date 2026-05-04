"""
Analysis 02 - Step 01: Somatotopic Coordinate Construction
Define 3D surface coordinates and spinal segmental innervation for 8 acupoint sites.
Compute Euclidean surface distance RDM and segmental distance RDM.

Coordinates derived from:
  - Primary: 2024 Chinese national standard "Nomenclature and location of
    acupuncture points for laboratory animals Part 2: Rat" (J Trad Chinese Med, 2024)
  - Supporting: Yin et al. 2008, Han et al. 2011, site-specific papers cited below

Coordinate system (prone position, limbs extended, adult SD rat ~250-300g):
  x: medio-lateral (mm from midline, 0 = midline)
  y: cranio-caudal (mm from nose tip, increasing caudally)
  z: dorso-ventral (mm from table surface, 0 = ventral/table)
"""

import os
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')
FIG_DIR = os.path.join(BASE_DIR, 'results', 'figures')
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────
# Coordinate specification from literature
# ──────────────────────────────────────────────────────────────────────
# x: mm from midline (0=midline)
# y: mm from nose tip (caudal direction)
# z: mm from table surface (0=ventral contact)
#
# Spinal level encoding: C1=1,...,C7=7, C8=8, T1=9,...,T13=21, L1=22,...,L6=27, S1=28
# For dual-segment innervation, use midpoint (e.g., C8-T1 → 8.5, L4-L5 → 25.5)

sites_data = {
    'Site': ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36'],

    # x: medio-lateral distance from midline
    # Trunk points: BL25=6mm (2024 std, Han 2011), GV4=0 (midline), ST25=5mm, CV12=0 (midline)
    # Limb points: approximate in prone extended position (most uncertain axis)
    'x': [6.0, 0.0, 5.0, 0.0, 20.0, 25.0, 8.0, 15.0],

    # y: cranio-caudal distance from nose tip
    # Trunk: GV4 at L2 (~145mm), BL25 at L4 (~155mm), ST25 at umbilicus (~135mm), CV12 20mm above (~115mm)
    # Forelimb: PC6 near wrist (~90mm), LI4 at paw (~85mm)
    # Hindlimb: ST36 below knee (~175mm), SP6 above ankle (~185mm)
    'y': [155.0, 145.0, 135.0, 115.0, 90.0, 85.0, 185.0, 175.0],

    # z: height from table surface
    # Dorsal points at top: GV4 ~38mm (spine peak), BL25 ~35mm (paravertebral)
    # Ventral points on table: ST25 ~0mm, CV12 ~0mm
    # Limb points intermediate
    'z': [35.0, 38.0, 0.0, 0.0, 15.0, 5.0, 8.0, 10.0],

    # Spinal segmental innervation
    'spinal_segment': [
        'L4',       # BL25: L4 dorsal ramus (Han 2011)
        'L2',       # GV4: L2 dorsal ramus (Wang 2016)
        'T10-T11',  # ST25: T10-T11 ventral rami (PMC7306073, PMC9731770)
        'T7-T8',    # CV12: T7-T8 ventral rami (2024 standard)
        'C8-T1',    # PC6: median nerve C8-T1 (2024 standard)
        'C7-C8',    # LI4: radial nerve C7-C8 (2024 standard, PMC6624843)
        'L4-S1',    # SP6: tibial nerve L4-L5 (2024 standard, Senna-Fernandes 2011)
        'L4-L5',    # ST36: deep peroneal nerve L4-L5 (2024 standard)
    ],

    # Numeric encoding for distance computation (midpoint for dual segments)
    'spinal_level_numeric': [
        25.0,   # BL25: L4
        23.0,   # GV4: L2
        18.5,   # ST25: T10-T11 midpoint (T10=18, T11=19)
        15.5,   # CV12: T7-T8 midpoint (T7=15, T8=16)
        8.5,    # PC6: C8-T1 midpoint (C8=8, T1=9)
        7.5,    # LI4: C7-C8 midpoint (C7=7, C8=8)
        26.5,   # SP6: L4-S1 midpoint (L4=25, S1=28) → 26.5
        25.5,   # ST36: L4-L5 midpoint (L4=25, L5=26)
    ],

    # References for each site
    'reference': [
        '2024 standard; Han 2011 (PMC3042615)',
        '2024 standard; Wang 2016 (PMC5270441)',
        'PMC7306073; PMC9731770',
        '2024 standard; Wang 2013 (PMC3857851)',
        '2024 standard; PMC6843597',
        '2024 standard; Li 2019 (PMC6624843)',
        '2024 standard; Senna-Fernandes 2011',
        '2024 standard; multiple',
    ],
}


def main():
    df = pd.DataFrame(sites_data)

    # Save coordinates
    coords_path = os.path.join(OUTPUT_DIR, 'site_coordinates.csv')
    df.to_csv(coords_path, index=False)
    print(f"Saved site coordinates to: {coords_path}")

    # ── Compute normalized Euclidean surface distance RDM (8×8) ──
    # Raw axes have very different ranges (y: 100mm, z: 38mm, x: 25mm).
    # Without normalization, y (cranio-caudal) dominates the distance and
    # the RDM mostly measures "forelimb vs trunk vs hindlimb," ignoring
    # dorsal-ventral and medial-lateral separation.
    # Z-score normalization gives each axis equal weight.
    coords_raw = df[['x', 'y', 'z']].values.astype(float)
    coords_norm = (coords_raw - coords_raw.mean(axis=0)) / coords_raw.std(axis=0)

    dist_vec = pdist(coords_norm, metric='euclidean')
    surface_rdm = squareform(dist_vec)

    surface_rdm_df = pd.DataFrame(surface_rdm, index=df['Site'], columns=df['Site'])
    surface_rdm_path = os.path.join(OUTPUT_DIR, 'surface_rdm.csv')
    surface_rdm_df.to_csv(surface_rdm_path)
    print(f"Saved surface distance RDM (normalized) to: {surface_rdm_path}")

    # Also save raw (unnormalized) RDM for comparison
    dist_vec_raw = pdist(coords_raw, metric='euclidean')
    raw_rdm = squareform(dist_vec_raw)
    raw_rdm_df = pd.DataFrame(raw_rdm, index=df['Site'], columns=df['Site'])
    raw_rdm_df.to_csv(os.path.join(OUTPUT_DIR, 'surface_rdm_raw.csv'))
    print(f"Saved surface distance RDM (raw) to: surface_rdm_raw.csv")

    # ── Compute segmental distance RDM (8×8) ──
    spinal_levels = df['spinal_level_numeric'].values
    segmental_rdm = np.abs(spinal_levels[:, None] - spinal_levels[None, :])

    segmental_rdm_df = pd.DataFrame(segmental_rdm, index=df['Site'], columns=df['Site'])
    segmental_rdm_path = os.path.join(OUTPUT_DIR, 'segmental_rdm.csv')
    segmental_rdm_df.to_csv(segmental_rdm_path)
    print(f"Saved segmental distance RDM to: {segmental_rdm_path}")

    # ── Summary ──
    print("\n--- Site Coordinates ---")
    print(df[['Site', 'x', 'y', 'z', 'spinal_segment', 'spinal_level_numeric']].to_string(index=False))

    print("\n--- Surface Distance RDM (normalized Euclidean) ---")
    print(surface_rdm_df.round(2).to_string())

    print("\n--- Segmental Distance RDM (spinal levels) ---")
    print(segmental_rdm_df.round(1).to_string())

    # Axis contribution report
    print("\n--- Axis ranges (raw) ---")
    for axis, name in [(0, 'x (medio-lateral)'), (1, 'y (cranio-caudal)'), (2, 'z (dorso-ventral)')]:
        vals = coords_raw[:, axis]
        print(f"  {name}: range={vals.max()-vals.min():.0f} mm, std={vals.std():.1f} mm")
    print("  → All axes z-score normalized before Euclidean distance computation")

    print("\n" + "=" * 70)
    print("NOTE: Limb x-coordinates (PC6, LI4, ST36, SP6) are the most uncertain.")
    print("They depend on limb posture (adducted vs extended). The ±15% perturbation")
    print("analysis (s02) tests sensitivity to these values.")
    print("=" * 70)


if __name__ == '__main__':
    main()
