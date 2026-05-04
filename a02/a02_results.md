# Analysis 02 Results: Somatotopic Coordinate Construction

## Summary
Two somatotopic RDMs were constructed for the 8 stimulation sites: a normalized surface Euclidean distance RDM and a spinal segmental distance RDM. Perturbation analysis confirmed that the surface RDM structure is stable under ±15% coordinate uncertainty (mean Mantel r = 0.896). The two RDMs capture different aspects of body space and disagree on several key site relationships, which is exactly why both are needed.

## Site Coordinates

| Site | x (mm) | y (mm) | z (mm) | Spinal segment | Numeric level | Reference |
|------|--------|--------|--------|----------------|---------------|-----------|
| BL25 | 6.0 | 155.0 | 35.0 | L4 | 25.0 | 2024 standard; Han 2011 |
| GV4 | 0.0 | 145.0 | 38.0 | L2 | 23.0 | 2024 standard; Wang 2016 |
| ST25 | 5.0 | 135.0 | 0.0 | T10-T11 | 18.5 | PMC7306073; PMC9731770 |
| CV12 | 0.0 | 115.0 | 0.0 | T7-T8 | 15.5 | 2024 standard; Wang 2013 |
| PC6 | 20.0 | 90.0 | 15.0 | C8-T1 | 8.5 | 2024 standard; PMC6843597 |
| LI4 | 25.0 | 85.0 | 5.0 | C7-C8 | 7.5 | 2024 standard; Li 2019 |
| SP6 | 8.0 | 185.0 | 8.0 | L4-S1 | 26.5 | 2024 standard; Senna-Fernandes 2011 |
| ST36 | 15.0 | 175.0 | 10.0 | L4-L5 | 25.5 | 2024 standard; multiple |

Coordinate system: Prone position, limbs extended, adult SD rat (~250–300g). x = mm from midline, y = mm from nose tip (caudal), z = mm from table surface (ventral = 0).

## Surface Euclidean RDM (normalized)

Coordinates were z-score normalized before computing Euclidean distance so that each axis (medio-lateral, cranio-caudal, dorso-ventral) contributes equally. Without normalization, the y-axis (range 100mm) would dominate over x (25mm) and z (38mm), reducing the RDM to a one-dimensional cranio-caudal ordering.

### Anatomical pairs — all have the smallest distances
| Pair | Normalized distance | Rank among 28 pairs |
|------|-------------------|---------------------|
| BL25–GV4 | 0.78 | 1st (closest) |
| ST25–CV12 | 0.82 | 2nd |
| SP6–ST36 | 0.87 | 3rd |
| PC6–LI4 | 0.94 | 4th |

All four anatomical pairs occupy the 4 smallest distances out of 28 total pairs. The next closest cross-pair (ST25–SP6: 1.60) is nearly 2x the largest within-pair distance. This clean separation confirms the coordinate system correctly captures the pairing structure.

### Largest cross-pair distances
| Pair | Normalized distance | What separates them |
|------|-------------------|---------------------|
| GV4–LI4 | 4.13 | Dorsal lumbar midline vs dorsal forepaw — maximum separation on all 3 axes |
| BL25–LI4 | 3.69 | Dorsal lumbar paravertebral vs dorsal forepaw |
| SP6–LI4 | 3.51 | Medial hindlimb ankle vs dorsal forepaw |

The largest distances are all between hindlimb/trunk dorsal sites and the forepaw (LI4), which makes anatomical sense — LI4 is the most distal and most laterally positioned site.

### Key dissociations to watch in A04
| Pair | Surface distance | Relationship |
|------|-----------------|--------------|
| BL25–ST25 | 2.59 | Dorsal vs ventral at same vertebral level — large surface distance |
| BL25–ST36 | 2.16 | Different body regions but moderate distance |
| ST25–SP6 | 1.60 | Ventral trunk vs medial hindlimb — relatively close geometrically |

BL25 and ST25 are on **opposite sides of the body** at roughly the same cranio-caudal level. Their surface distance (2.59) correctly reflects this — it's driven by the z-axis (dorsal=35mm vs ventral=0mm). If we had used raw (unnormalized) Euclidean distance, this pair would have appeared the same distance as BL25–SP6 (both ~40mm raw), because the y-difference to SP6 would have swamped the z-difference to ST25. Normalization fixed this.

## Segmental Distance RDM

The segmental RDM measures absolute difference in spinal innervation level. This captures neural wiring rather than geometric position.

### Sites that are segmentally close but geometrically distant
| Pair | Segmental distance | Surface distance | Interpretation |
|------|-------------------|-----------------|----------------|
| BL25–ST36 | 0.5 levels | 2.16 | Both L4–L5 innervation. Dorsal trunk vs lateral hindlimb — geometrically separated but share spinal input |
| BL25–SP6 | 1.5 levels | 2.14 | L4 vs L4-S1. Same core segmental territory despite different body surfaces |
| SP6–ST36 | 1.0 levels | 0.87 | Both hindlimb, both L4–L5 region. Close on both metrics |

### Sites that are segmentally distant but geometrically moderate
| Pair | Segmental distance | Surface distance | Interpretation |
|------|-------------------|-----------------|----------------|
| ST25–SP6 | 8.0 levels | 1.60 | T10–T11 vs L4–S1. Geometrically not that far (ventral trunk to medial hindlimb), but neurally very different segments |
| CV12–ST36 | 10.0 levels | 2.56 | T7–T8 vs L4–L5. Upper thoracic vs lower lumbar innervation |

### Extreme segmental distances (forelimb vs hindlimb)
| Pair | Segmental distance |
|------|-------------------|
| LI4–SP6 | 19.0 levels (C7–C8 vs L4–S1) — maximum |
| LI4–ST36 | 18.0 levels |
| PC6–SP6 | 18.0 levels |
| PC6–ST36 | 17.0 levels |

The forelimb sites (PC6, LI4 at C7–T1) and hindlimb sites (SP6, ST36 at L4–S1) are maximally separated segmentally — the entire thoracolumbar cord lies between them. This is the strongest somatotopic contrast in the dataset.

## Why two RDMs? What each one tests

The two RDMs are not just the same question asked with different rulers. They test mechanistically distinct hypotheses about how body location could influence stimulation site function.

**Surface (geometric) RDM** asks: "Do sites that are physically close on the body surface have similar functional profiles?" This tests the simplest somatotopic hypothesis — that nearby skin regions are studied for similar conditions because they share local tissue environment, overlapping practitioner traditions, or proximity-based selection bias.

**Segmental (neuroanatomical) RDM** asks: "Do sites that share spinal cord input have similar functional profiles?" This tests a deeper mechanistic hypothesis — that acupoint function is determined by which spinal segments relay the peripheral signal to the CNS. If two sites feed into the same spinal segments, they access the same autonomic outflow, the same viscerosomatic reflex arcs, and the same ascending pathways. If spinal segmental convergence determines function, segmentally close sites should have similar profiles regardless of their skin distance.

The two RDMs agree on broad structure (forelimb far from hindlimb, paired sites close) but disagree on critical details:

### Key dissociations between the two RDMs

**1. BL25–ST36: Segmentally near-identical, geometrically separated**
- Segmental: 0.5 levels (both L4–L5 — essentially the same spinal input)
- Surface: 2.16 (dorsal lumbar trunk vs lateral hindlimb below knee)
- **Test:** If spinal segmental convergence determines function, BL25 and ST36 should have similar profiles. If they don't — if a dorsal trunk site and a hindlimb site sharing the same spinal segment still have different functional identities — that's direct evidence against the segmental mechanism hypothesis.

**2. ST25–SP6: Geometrically moderate, segmentally distant**
- Surface: 1.60 (ventral trunk to medial hindlimb — not that far geometrically)
- Segmental: 8.0 levels (T10–T11 vs L4–S1 — very different spinal territory)
- **Test:** The geometric RDM would predict some similarity; the segmental RDM predicts divergence. Which definition of "body space" better predicts functional similarity?

**3. BL25–GV4: Close on both metrics**
- Surface: 0.78 (dorsal lumbar, 6mm apart)
- Segmental: 2.0 levels (L4 vs L2 — both lumbar cord)
- **Test:** If ANY pair should show somatotopic functional similarity, it's this one. They are physically adjacent, share lumbar innervation, and are both dorsal midline/paravertebral. The paper's key finding will be that they are functionally divergent (GV4 is Neurological, BL25 is Gastrointestinal) — demonstrating that even maximal somatotopic proximity does not predict functional identity.

### Why this matters for the paper

If we only used the surface RDM and found no correlation with function, a reviewer could object: "Of course skin distance doesn't matter — peripheral nerve stimulation works through spinal segmental reflexes, not skin proximity. You should have tested segmental innervation." The segmental RDM preempts this objection entirely.

The strongest possible outcome is: neither surface nor segmental somatotopic distance correlates with disease or mechanism profiles. This means functional organization is independent of body location regardless of whether "body location" is defined anatomically (where on the skin) or neuroanatomically (where in the spinal cord).

## Perturbation Analysis

1,000 iterations of ±15% uniform jitter on all coordinates, with z-score normalization recomputed at each iteration.

- **Mean Mantel r** between original and perturbed RDMs: **0.896**
- **Distribution**: roughly normal, ranging from ~0.70 to ~0.98
- **Interpretation**: Even with substantial coordinate uncertainty (±15% is generous — vertebral landmarks are more precise than this), the rank ordering of pairwise distances is largely preserved. The ~10% of iterations below r=0.80 are cases where the jitter on limb x-coordinates (the most uncertain axis) happened to reorder some mid-range distances.

This is reassuring but not perfect. The perturbation r is lower than typical for well-defined coordinate systems (which would show r > 0.95). The reason is the limb x-coordinates: PC6 at 20mm and LI4 at 25mm are approximate, and ±15% jitter on these values (±3–4mm) can meaningfully change their relative positions to trunk sites. This is honestly communicated by the perturbation analysis and will be formally tested in A07 (coordinate perturbation sensitivity: do the Mantel test results change across the 1,000 perturbations?).

## Outputs

| File | Description |
|------|-------------|
| `results/datatables/site_coordinates.csv` | 8 sites with x, y, z, spinal segment, references |
| `results/datatables/surface_rdm.csv` | 8×8 normalized Euclidean distance |
| `results/datatables/surface_rdm_raw.csv` | 8×8 raw (unnormalized) Euclidean distance for comparison |
| `results/datatables/segmental_rdm.csv` | 8×8 spinal segmental distance |
| `results/datatables/perturbed_rdms.pkl` | 1,000 perturbed surface RDMs for A07 |
| `results/figures/somatotopic_rdms.png` | Dual heatmap (surface + segmental) |
| `results/figures/perturbation_stability.png` | Mantel r histogram |

## Implications for downstream analyses

- **A04 (RSA)**: Both surface and segmental RDMs will be tested against disease and mechanism RDMs. The prediction is that neither somatotopic RDM correlates significantly with either functional RDM.
- **A07 (Sensitivity)**: The 1,000 perturbed RDMs will be used to test whether the null somatotopic result holds across coordinate uncertainty. Given mean perturbation r = 0.896, we expect the null result to be robust.
- **BL25–GV4 is the critical pair**: Segmentally close (2.0), geometrically close (0.78), but expected to be functionally divergent (Neurological vs Gastrointestinal). This is the strongest single-pair evidence for somatotopic independence.
