# Analysis 06 Results: Low-Dimensional Embeddings

## Summary
Three dimensionality reduction methods (MDS, PCA, CA) were applied to the disease and mechanism RDMs to produce 2D embeddings of the 8 stimulation sites. Correspondence Analysis (CA) was selected for the main figure because it jointly positions sites and categories in a shared biplot space, making the functional structure self-interpretable. The embeddings confirm three key findings visually: (1) disease space is sharply differentiated with clear cluster separation, (2) mechanism space is compressed with most sites collapsing near the origin, and (3) anatomical pairs consistently cross cluster boundaries — paired sites land in different functional neighborhoods.

## Correspondence Analysis (Main Method)

### Disease Space (Fig 6, left panel)

**Inertia:** Dim 1 captures 43.2%, Dim 2 captures 25.5% — total 68.7% of site-category association in two dimensions. This is a good fit; the 2D plot faithfully represents the major axes of disease profile variation.

**Site positions:**
| Site | Dim 1 | Dim 2 | Interpretation |
|------|-------|-------|----------------|
| BL25 | -0.59 | 1.50 | Far upper-left — pulled by Gastrointestinal |
| ST25 | -0.44 | 1.22 | Upper-left — close to BL25, GI pair |
| PC6 | 1.48 | 0.18 | Far right — pulled by Cardiovascular |
| GV4 | 0.22 | -0.35 | Center-right — near Neurological/Psychiatric |
| LI4 | 0.09 | -0.41 | Center — near GV4 |
| CV12 | -0.22 | 0.37 | Center-left — moderate position |
| SP6 | -0.25 | -0.43 | Lower-left — near Reproductive/Dermatological |
| ST36 | -0.12 | -0.01 | Near origin — generalist, no category pulls it strongly |

**Key observations:**
- **Dim 1** separates Cardiovascular (PC6, far right) from Gastrointestinal (BL25/ST25, left). This is the dominant axis of disease variation — the single biggest contrast in the dataset.
- **Dim 2** separates GI (BL25/ST25, top) from Reproductive/Dermatological (SP6, bottom). This secondary axis distinguishes the GI pair from the generalist sites.
- **ST36 sits near the origin** — no category pulls it in any direction, confirming its generalist identity. It is the most "average" site in disease space.
- **BL25 and ST25 are tightly clustered** (green dots, upper-left), forming a clear GI pair visually separated from everything else.
- **PC6 is isolated** (red dot, far right), driven entirely by its Cardiovascular dominance.

**Category positions (triangles):**
- Gastrointestinal (-0.29, 0.87) sits near BL25/ST25 — the GI category defines their position.
- Cardiovascular (1.75, 0.27) sits near PC6 — the single most extreme category position, reflecting PC6's strong specialization.
- Reproductive (-0.30, -0.63) sits near SP6, consistent with SP6's gynecological tradition.
- Most other categories cluster near the origin — they don't strongly differentiate between sites.

### Mechanism Space (Fig 6, right panel)

**Inertia:** Dim 1 captures 39.5%, Dim 2 captures 24.0% — total 63.5%. Slightly less than disease space, meaning mechanism profiles have more residual complexity beyond 2D.

**Site positions:**
| Site | Dim 1 | Dim 2 | Interpretation |
|------|-------|-------|----------------|
| GV4 | -1.40 | -0.74 | Far lower-left — extreme outlier, pulled by Autophagy/Neuroprotective |
| BL25 | 0.62 | -0.23 | Right — pulled by Gut-Brain/Enteric |
| ST25 | 0.48 | -0.54 | Lower-right — near BL25, GI enteric mechanisms |
| CV12 | 0.09 | -0.38 | Center-right — moderate, Metabolic Pathway |
| PC6 | -0.19 | 0.09 | Near origin — generic mechanisms |
| LI4 | -0.20 | 0.03 | Near origin — generic mechanisms |
| SP6 | 0.02 | 0.13 | Near origin — generic mechanisms |
| ST36 | 0.02 | 0.04 | Near origin — most generic |

**Key observations:**
- **GV4 is the mechanism-space outlier**, far from all other sites. Its Neuroprotective (34.5%) and Autophagy/Mitophagy (17.2%) dominance pulls it to the extreme lower-left. This mirrors its disease-space isolation (Neurological specialist) but through a different dimension.
- **PC6 shifts dramatically between spaces.** In disease space, PC6 is the most isolated site (far right, Cardiovascular). In mechanism space, PC6 sits near the origin — its mechanisms are generic. This is the clearest example of a disease specialist being a mechanism generalist.
- **Most sites compress near the origin** in mechanism space. PC6, LI4, SP6, ST36 all sit within a tight cluster. Compare to disease space where these same sites spread across a wide range. This visual compression is the embedding-level manifestation of the mechanism compression effect documented in A03.
- **BL25 and ST25 remain somewhat separated** from the central cluster, pulled by Gut-Brain/Enteric mechanisms — their GI mechanism identity is real, not just a disease label artifact.

### Anatomical Pair Behavior (Dashed Lines)

The dashed lines connecting anatomical pairs cross cluster boundaries in both panels:
- **BL25–GV4:** In disease space, BL25 is upper-left (GI) while GV4 is center-right (Neurological) — the line spans nearly the full Dim 2 range. In mechanism space, BL25 is right (Gut-Brain) while GV4 is far left (Neuroprotective) — the line spans the full Dim 1 range. The closest anatomical pair is the most functionally distant in both spaces.
- **ST25–CV12:** In disease space, ST25 is upper-left while CV12 is center — moderate separation. In mechanism space, the line crosses from lower-right to center.
- **PC6–LI4:** In disease space, PC6 is far right while LI4 is center — large separation. In mechanism space, both collapse near the origin — they converge mechanistically despite diverging in disease application.
- **SP6–ST36:** Both sit in the lower-center of disease space (moderate distance). Both sit near the origin in mechanism space (near-identical mechanisms, consistent with cosine distance 0.016).

No anatomical pair consistently occupies the same cluster in both panels. If anatomy determined function, paired sites would cluster together — instead, every pair shows some degree of cross-cluster separation.

### Cluster Coloring

Sites are colored by disease dendrogram clusters (3 clusters):
- **Green (GI cluster):** BL25, ST25
- **Blue (Broad cluster):** GV4, CV12, LI4, SP6, ST36
- **Red (CV outlier):** PC6

Using the same colors in both panels allows the reader to track how sites rearrange between spaces. The GI cluster (green) stays somewhat cohesive in both — BL25 and ST25 are near each other in both panels. But PC6 (red) shifts from extreme isolation in disease space to the central cluster in mechanism space. The broad cluster (blue) spreads widely in disease space but compresses near the origin in mechanism space.

## MDS Embedding (Alternative Method)

MDS was computed from the cosine distance RDMs using metric MDS with Kruskal stress minimization.

**Disease stress:** 0.093 (good fit — stress < 0.1 indicates faithful distance preservation)
**Mechanism stress:** 0.020 (excellent fit — the compressed distances are easy to represent in 2D)

The MDS coordinates are consistent with the CA biplot: BL25/ST25 cluster together, PC6 is isolated, GV4/LI4 group in disease space. The lower mechanism stress reflects the compression — when most distances are small, 2D representation is trivially good.

## PCA (Alternative Method)

PCA was applied to the profile matrices (not the RDMs) to provide a linear decomposition.

**Disease:** PC1 explains 63.6%, PC2 explains 16.8% — total 80.4%. The dominant PC1 loading is Neurological (+0.72) vs Gastrointestinal (-0.68), confirming that the GI–Neurological axis is the primary source of variance.

**Mechanism:** PC1 explains 65.1%, PC2 explains 15.5% — total 80.6%. The dominant PC1 loading is Neuroprotective (+0.62) vs Inflammatory/Immune (-0.44), confirming that GV4's unique mechanism signature drives the primary axis.

## GV4 Exclusion Sensitivity (figS4)

Removing GV4 (the most extreme outlier) tests whether the embedding structure depends on a single site.

**Disease space (GV4 excluded):** Inertia increases slightly (Dim 1: 46.1%, Dim 2: 27.0%, total 73.1% vs 68.7%). The remaining structure is preserved — BL25/ST25 still cluster in the upper-left near Gastrointestinal, PC6 remains isolated on the right near Cardiovascular. The broad cluster (CV12, ST36, LI4, SP6) occupies the center-left. Removing GV4 does not collapse the disease-space structure.

**Mechanism space (GV4 excluded):** Inertia increases (Dim 1: 42.8%, Dim 2: 24.6%, total 67.4% vs 63.5%). Without GV4 dominating Dim 1, the remaining sites redistribute. BL25 moves to the upper-left (Gut-Brain/Enteric influence), CV12 drops to the bottom (Metabolic Pathway). The main mechanism-space finding — compression of most sites — persists. The GI sites (BL25, ST25) remain somewhat separated from the rest, confirming their mechanism identity is not an artifact of GV4's presence.

**Conclusion:** GV4 is a genuine outlier, not a data artifact. Its removal changes the geometry but does not invalidate the structure. All key patterns (GI pairing, PC6 disease specialization, mechanism compression) are robust to GV4 exclusion.

## Figure Descriptions

### Fig 6: CA Biplots (Main Figure)
Two-panel CA biplot — disease space (left) and mechanism space (right). Each panel shows 8 sites as colored circles (green = GI cluster, blue = broad cluster, red = CV outlier), disease/mechanism categories as gray triangles, and anatomical pairs connected by dashed lines. Only the 5 most extreme categories (furthest from origin) are labeled to reduce clutter. Categories near sites that would overlap are offset with thin connector lines for readability.

**What to look for:** (1) The GI pair (green, BL25/ST25) clusters tightly in both panels but in different regions — upper-left in disease, right side in mechanism. (2) PC6 (red) shifts from far-right isolation in disease space to the central cluster in mechanism space. (3) Dashed anatomical pair lines cross cluster boundaries — no pair stays together. (4) Disease space shows wide spread; mechanism space shows compression toward the origin.

### Fig S1: MDS Disease Space (Supplementary)
Single-panel MDS embedding of disease space with bootstrap 95% confidence ellipses. Each ellipse shows the uncertainty in that site's position from 1,000 bootstrap iterations (resample records within each site, recompute profiles and RDM, fit MDS, Procrustes-align to original).

**Ellipse sizes reflect sample size:** BL25 (n=22) and GV4 (n=29) have moderate ellipses but are still well-separated from each other. ST36 (n=1,079) has a small, tight ellipse — its position is stable. CV12 has the largest disease-space ellipse (width=0.61), reflecting both its moderate sample size (n=65) and its intermediate profile that is sensitive to resampling.

**Key observation:** Despite the ellipses, the cluster structure is preserved — BL25/ST25 ellipses overlap with each other but not with the PC6 or GV4/LI4 ellipses. The GI pair's proximity is stable under resampling.

### Fig S2: MDS Mechanism Space (Supplementary)
Single-panel MDS embedding of mechanism space with bootstrap 95% confidence ellipses. The visual compression is dramatic — most sites and their ellipses overlap near the center.

**Ellipse sizes:** ST36 has the tightest ellipse (width=0.099) — its mechanism profile is extremely stable with 1,079 records. GV4's ellipse is the largest (width=0.386) and clearly separated from the central cluster, confirming that its mechanism-outlier status is genuine. BL25 and ST25 have large overlapping ellipses in the lower-left, partially separated from the central cluster but not fully resolved — their GI mechanism identity is real but less sharply defined than in disease space.

**Key observation:** The mechanism-space ellipses overlap heavily for the central sites (PC6, LI4, SP6, ST36), confirming that their mechanism profiles are not meaningfully distinguishable. This is the bootstrap-level confirmation of mechanism compression — these sites are not just close in the point estimate, they are statistically indistinguishable in mechanism space.

### Fig S4: GV4 Exclusion CA Biplots (Supplementary)
Two-panel CA biplot after removing GV4 from the dataset. Disease space (left) shows the same structure as Fig 6 — BL25/ST25 in the upper-left near Gastrointestinal, PC6 isolated on the right near Cardiovascular, remaining sites in the center. The dashed pair lines for ST25–CV12, PC6–LI4, and SP6–ST36 still cross cluster boundaries. Mechanism space (right) redistributes without GV4's dominant pull — BL25 moves to the upper-left, CV12 drops to the bottom near Metabolic Pathway. The broad-cluster sites (LI4, SP6, ST36, PC6) group on the right side.

**What this shows:** The core finding — functional organization is independent of somatotopic organization — does not depend on GV4. The remaining anatomical pairs still diverge in both spaces. The embedding structure is robust.

## Outputs

| File | Description |
|------|-------------|
| `results/datatables/mds_coordinates.csv` | MDS 2D coordinates for 8 sites (disease + mechanism) with stress values |
| `results/datatables/pca_coordinates.csv` | PCA 2D coordinates for 8 sites |
| `results/datatables/pca_loadings.csv` | PCA loadings per category |
| `results/datatables/pca_variance.csv` | PCA variance explained |
| `results/datatables/ca_site_scores.csv` | CA site coordinates (disease + mechanism) |
| `results/datatables/ca_disease_cat_scores.csv` | CA disease category coordinates |
| `results/datatables/ca_mechanism_cat_scores.csv` | CA mechanism category coordinates |
| `results/datatables/ca_inertia.csv` | CA inertia (variance explained) per dimension |
| `results/datatables/bootstrap_ellipses.pkl` | Bootstrap 95% confidence ellipse parameters (1,000 iterations) |
| `results/datatables/gv4_exclusion_mds.csv` | MDS coordinates with GV4 excluded |
| `results/datatables/gv4_exclusion_pca.csv` | PCA coordinates with GV4 excluded |
| `results/datatables/gv4_exclusion_ca.csv` | CA site coordinates with GV4 excluded |
| `results/datatables/gv4_exclusion_ca_disease_cat.csv` | CA disease category coordinates (GV4 excluded) |
| `results/datatables/gv4_exclusion_ca_mechanism_cat.csv` | CA mechanism category coordinates (GV4 excluded) |
| `results/figures/fig6_embeddings.png` | Main Figure 6: CA biplots |
| `results/figures/figS1_alt_disease.png` | Supplementary: MDS disease with bootstrap ellipses |
| `results/figures/figS2_alt_mechanism.png` | Supplementary: MDS mechanism with bootstrap ellipses |
| `results/figures/figS4_gv4_exclusion.png` | Supplementary: CA biplots with GV4 excluded |

## Key Takeaways for the Manuscript

1. **Disease space is sharply structured.** CA captures 68.7% of site-category association in 2D. The GI pair (BL25/ST25) and CV outlier (PC6) are clearly separated from the broad cluster. The primary axis is Gastrointestinal vs Cardiovascular.

2. **Mechanism space is compressed.** Most sites collapse near the origin — PC6, LI4, SP6, ST36 are mechanistically indistinguishable. Only GV4 (Neuroprotective/Autophagy) and the GI pair (Gut-Brain/Enteric) maintain some separation. Bootstrap ellipses confirm the central-cluster overlap is genuine, not a visualization artifact.

3. **PC6 is the clearest space-shifting example.** Disease-space outlier (Cardiovascular specialist, furthest from origin) becomes a mechanism-space centrist (near origin, generic mechanisms). This demonstrates that disease specialization does not imply mechanism specialization.

4. **Anatomical pairs cross cluster boundaries.** Every pair line crosses functional neighborhoods. BL25–GV4 spans the widest range in both spaces. No anatomical pair clusters together in both disease and mechanism space.

5. **The structure is robust to GV4 exclusion.** Removing the most extreme site does not collapse the embedding. The GI pair stays together, PC6 stays isolated, pair lines still cross boundaries. The findings are not driven by a single outlier.

6. **Three methods agree.** MDS, PCA, and CA all produce consistent spatial arrangements. The choice of method affects the geometry but not the conclusions.
