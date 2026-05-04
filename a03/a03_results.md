# Analysis 03 Results: First-Order Characterization

## Summary
All 8 stimulation sites were characterized across disease (14 categories) and mechanism (12 categories) domains. The results confirm sharp disease-space differentiation with clear specialist signals, more muted mechanism-space profiles consistent with mechanism compression, and significant within-pair divergence for all anatomical pairs in disease space. Dendrogram analysis reveals interpretable hierarchical structure in both spaces, with key differences in how sites group.

## Disease Profiles

### Specialist signals
| Site | Dominant disease category | Proportion | log₂(BF) |
|------|--------------------------|-----------|-----------|
| GV4 | Neurological | 87.9% | +39.0 |
| BL25 | Gastrointestinal | 68.2% | +24.2 |
| ST25 | Gastrointestinal | 52.8% | +56.7 |
| CV12 | Metabolic/Endocrine | 35.3% | +19.0 |
| PC6 | Cardiovascular | 39.4% | +120.9 |

GV4 is the most extreme specialist — nearly 88% of its records are Neurological. PC6 has the strongest Bayes Factor (120.9) for Cardiovascular because it has both a large sample (181 records) and strong concentration.

### Generalist profiles
| Site | Top category | Proportion | Second category | Proportion |
|------|-------------|-----------|-----------------|-----------|
| ST36 | Pain | 27.1% | Neurological | 24.4% |
| SP6 | Pain | 26.8% | Neurological | 17.2% |
| LI4 | Neurological | 42.1% | Pain | 14.9% |

ST36 is the broadest generalist — its top category (Pain, 27.1%) holds less than a third of its records, with research distributed across 14 categories. SP6 is similar but with a distinct Reproductive signal (12.7%). LI4 leans Neurological but has the most even spread across minor categories.

### Disease-space dendrogram
The dendrogram reveals three natural groupings visible from the merge distances:

**First merges (distance < 0.15):**
- BL25–ST25 merge at distance ~0.08 — the tightest pair, both GI-dominant
- GV4–LI4 merge at ~0.10 — both Neurological-heavy
- SP6–ST36 merge at ~0.12 — both Pain/Neurological generalists

**Mid-level merges (0.30–0.47):**
- CV12 joins the SP6–ST36 branch at ~0.33 — adding the Metabolic/Endocrine profile
- The GV4–LI4 branch joins the CV12–SP6–ST36 branch at ~0.35
- PC6 joins the GV4–LI4 subtree at ~0.47 — its Cardiovascular dominance keeps it distant

**Final merge (~0.66):**
- The BL25–ST25 (GI) branch joins everything else at the highest merge distance — confirming the GI pair is the most distinctive functional group

Key observation: **PC6 does not form its own isolated branch** in the dendrogram. Instead, it joins the GV4–LI4 subtree at 0.47, suggesting its secondary Neurological component (30% of PC6 records) pulls it toward that group. This is more nuanced than the old k=3 clustering which isolated PC6 entirely.

## Mechanism Profiles

### Key observation: compression
The mechanism profiles are more uniform than disease profiles. Every site has Inflammatory/Immune as its largest or second-largest mechanism category (ranging from 10.3% for GV4 to 36.9% for LI4). No site has a single mechanism category exceeding 37% — compare to disease space where GV4 reaches 88%.

### Notable mechanism specializations
| Site | Distinctive mechanism | Proportion | Context |
|------|----------------------|-----------|---------|
| GV4 | Neuroprotective | 34.5% | Consistent with Neurological disease focus |
| GV4 | Autophagy/Mitophagy | 17.2% | Highest of any site — neurodegenerative mechanisms |
| BL25 | Gut-Brain/Enteric | 18.2% | Consistent with GI disease focus |
| BL25 | Autonomic/Neuroendocrine | 18.2% | Vagal/autonomic pathways for GI regulation |
| ST25 | Gut-Brain/Enteric | 19.3% | Highest — GI enteric mechanisms |
| CV12 | Metabolic Pathway | 15.4% | Consistent with Metabolic/Endocrine disease focus |

### Mechanism-space dendrogram
The mechanism dendrogram has a strikingly different structure from disease:

**First merges (distance < 0.10):**
- SP6–ST36 merge at ~0.02 — by far the tightest pair in either space. Their mechanism profiles are virtually identical.
- PC6–SP6/ST36 merge at ~0.05 — PC6 joins the hindlimb sites immediately, because its mechanism profile (Inflammatory/Immune + Cell Survival) is generic
- LI4 joins at ~0.07

**Mid-level merges (0.08–0.24):**
- BL25–ST25 merge at ~0.08 — GI enteric mechanism pair
- CV12 joins the PC6/LI4/SP6/ST36 branch at ~0.15
- BL25–ST25 join the main group at ~0.24

**Final merge (~0.50):**
- GV4 joins last at the highest merge distance — it is the **mechanism-space outlier**, driven by its unique Neuroprotective (34.5%) and Autophagy (17.2%) dominance

Key comparison to disease space:
- **PC6 shifts dramatically.** In disease space, PC6 is distant (merges at 0.47). In mechanism space, PC6 merges at 0.05 — it's one of the most generic sites mechanistically. Its Cardiovascular disease specialty does not translate to a unique mechanism signature.
- **GV4 stays isolated in both spaces** but for different reasons: Neurological disease dominance vs Neuroprotective/Autophagy mechanism dominance.
- **The overall tree is much shallower** in mechanism space (max distance ~0.50) vs disease space (~0.66), quantifying the compression effect.

## RDMs: Disease vs Mechanism Space

### Disease RDM — sharp differentiation
| Notable pair | Cosine distance | Interpretation |
|-------------|----------------|----------------|
| BL25–GV4 | 0.993 | Maximally dissimilar — GI vs Neurological |
| BL25–LI4 | 0.861 | Very different profiles |
| PC6–BL25 | 0.850 | Cardiovascular vs GI |
| BL25–ST25 | 0.079 | Very similar — both GI-dominant |
| GV4–LI4 | 0.102 | Both Neurological-heavy |
| SP6–ST36 | 0.123 | Both Pain/Neurological generalists |

The disease RDM has high dynamic range: distances span from 0.08 (near-identical profiles) to 0.99 (completely non-overlapping). BL25–GV4 at 0.993 is the most dissimilar pair in the dataset — they share almost no disease categories despite being the closest anatomical pair (0.78 surface distance, 2.0 segmental levels).

### Mechanism RDM — compressed
| Notable pair | Cosine distance | Interpretation |
|-------------|----------------|----------------|
| GV4–BL25 | 0.726 | Largest mechanism distance — but still smaller than many disease distances |
| GV4–ST25 | 0.628 | GV4 is the mechanism-space outlier |
| SP6–ST36 | 0.016 | Nearly identical mechanism profiles |
| PC6–ST36 | 0.036 | Very similar mechanisms despite different diseases |
| LI4–ST36 | 0.046 | Very similar mechanisms |

The mechanism RDM is dramatically more compressed than the disease RDM. The largest mechanism distance (GV4–BL25: 0.726) is smaller than 7 of the 28 disease distances. The mean mechanism distance (~0.20) is less than half the mean disease distance (~0.50). This is the mechanism compression effect: sites are far more similar in how they work than in what they treat.

SP6–ST36 is the most striking example: disease distance 0.123 (somewhat similar — both Pain/Neurological), but mechanism distance 0.016 (essentially identical mechanisms). They engage nearly the same biological pathways despite partially different disease applications.

## Within-Pair Tests

### Disease-space divergence
| Pair | χ² | df | p-value | Significant | Key driving categories |
|------|-----|-----|---------|-------------|----------------------|
| BL25–GV4 | 51.9 | 5 | 5.7×10⁻¹⁰ | Yes | GI (+3.67 BL25), Neurological (+2.78 GV4) |
| ST25–CV12 | 26.6 | 7 | 3.9×10⁻⁴ | Yes | GI (+2.11 ST25), Met/Endo (+1.13 CV12), Neuro (+1.97 CV12) |
| PC6–LI4 | 84.6 | 12 | 5.4×10⁻¹³ | Yes | Cardiovascular (+3.82 PC6), Derm (+2.60 LI4), Musculoskeletal (+2.60 LI4) |
| SP6–ST36 | 150.5 | 13 | 1.6×10⁻²⁵ | Yes | Reproductive (+7.11 SP6), Met/Endo (+3.82 SP6), GI (-4.02 SP6) |

All 4 anatomical pairs are significantly different in disease space (p < 0.001). The standardized residuals reveal which categories drive each divergence:
- **BL25–GV4:** Classic dissociation. BL25 is enriched for GI (+3.67), GV4 for Neurological (+2.78). The most anatomically close pair is the most functionally divergent.
- **SP6–ST36:** The largest χ² (150.5). Driven primarily by SP6's Reproductive enrichment (+7.11) — SP6 (Sanyinjiao) is a classical gynecological point, ST36 (Zusanli) is not.
- **PC6–LI4:** PC6's Cardiovascular signal (+3.82) versus LI4's broader profile with Dermatological and Musculoskeletal enrichment (+2.60 each).

### Mechanism-space divergence
| Pair | χ² | df | p-value | Significant |
|------|-----|-----|---------|-------------|
| BL25–GV4 | 31.0 | 9 | 3.0×10⁻⁴ | Yes |
| ST25–CV12 | 24.3 | 11 | 0.011 | Yes |
| PC6–LI4 | 23.0 | 11 | 0.018 | Yes |
| SP6–ST36 | 12.7 | 11 | 0.311 | **No** |

SP6–ST36 is the only pair that does NOT significantly differ in mechanism space (p=0.311). This is consistent with mechanism compression: despite significant disease-space divergence (p=1.6×10⁻²⁵), they use essentially the same biological pathways. The mechanism χ² values are uniformly smaller than disease χ² values across all 4 pairs.

## Record Independence (PMID Overlap)

### Flagged pairs (>20% shared PMIDs)
| Pair | Shared PMIDs | % of smaller site | Concern |
|------|-------------|-------------------|---------|
| BL25–ST25 | 12 | 54.6% | High — over half of BL25's records share a PMID with ST25 |
| CV12–ST36 | 44 | 64.7% | High — most of CV12's studies also used ST36 |
| SP6–ST36 | 197 | 67.5% | Highest — two-thirds of SP6's records come from studies that also used ST36 |

The SP6–ST36 overlap (67.5%) is notable because many studies used both sites. This could inflate their profile similarity — their mechanism profiles being nearly identical (cosine distance 0.016) needs to be interpreted cautiously. The publication-collapsing analysis (A07) will test whether collapsing shared PMIDs changes the results.

### Low-overlap pairs
Most pairs share few or no PMIDs: BL25–GV4 (0%), BL25–PC6 (0%), GV4–ST25 (0%), GV4–CV12 (0%). The anatomical pair BL25–GV4 sharing zero PMIDs is important — their disease-space divergence cannot be attributed to the same studies assigning different labels.

## Figures

### Fig 2: BF Heatmap
Two panels, each with rows ordered by its own domain's dendrogram leaf order.

**Disease panel (top):** Clear specialist signals visible. GV4 row is dark red for Neurological (+39.0) and dark blue everywhere else. PC6 has an intense Cardiovascular cell (+120.9). ST25 and BL25 show GI enrichment (+56.7 and +24.2). ST36 row is predominantly light — near-zero BFs across most categories, confirming its generalist identity. Gray cells mark zero-record entries. Values are shown only where |log₂(BF)| > 1.58 (BF > 3).

**Mechanism panel (bottom):** Visibly more muted — fewer extreme values, more cells near white/zero, and the overall color range is narrower. GV4 shows the only strong positive signal (Neuroprotective +6.7, Autophagy +8.3). Most other sites show modest enrichment in Inflammatory/Immune or mild depletion across categories. This visual contrast between panels is the first direct evidence of mechanism compression.

Note: The color scale (±5) clips the strongest disease signals (PC6 Cardiovascular at +120.9, ST25 GI at +56.7 both appear as maximum red). This preserves gradation for weaker signals. Exact values are in `disease_bf.csv`.

### Fig 3: Three RDMs
Three panels with shared row ordering (disease dendrogram leaf order).

**Disease RDM (left):** High contrast — bright yellow cells (high distance, ~0.9+) and dark purple cells (low distance, ~0.08). Clear block structure visible: the BL25–ST25 pair forms a tight dark block, as does SP6–ST36. GV4 row/column is bright against most sites except LI4.

**Mechanism RDM (center):** Dramatically darker and more uniform. Most cells are in the 0.05–0.20 range (deep purple). Only GV4's row/column shows lighter colors (0.40–0.73). The compression is visually striking when viewed next to the disease RDM.

**Somatotopic RDM (right):** Completely different pattern from both functional RDMs. Uses magma colormap on a different scale (mm). Anatomical pairs (BL25–GV4, ST25–CV12, PC6–LI4, SP6–ST36) are the dark cells. The forelimb–hindlimb distances dominate (PC6/LI4 vs SP6/ST36 in bright yellow). This structural dissimilarity between somatotopic and functional RDMs is visually apparent even before formal Mantel testing.

### Dendrograms
Two-panel dendrogram plot showing full hierarchical trees.

**Disease dendrogram (left):** BL25–ST25 merge first (lowest branch, ~0.08), then GV4–LI4 and SP6–ST36 form their own early pairs. PC6 merges late (0.47). The final merge at 0.66 connects the GI pair to everything else — this is the deepest split, confirming the GI functional identity is the most distinctive.

**Mechanism dendrogram (right):** SP6–ST36 merge first at the lowest point (~0.02), followed by rapid aggregation of PC6, LI4, CV12 into one large group. BL25–ST25 form their own branch (GI enteric mechanisms). GV4 merges last at ~0.50. The tree is shallower overall (max height 0.50 vs 0.66), and most sites merge before distance 0.25 — quantifying the compression that is visible in the RDM heatmap.

## Outputs

| File | Description |
|------|-------------|
| `disease_profiles.csv` | 8×14 proportional profiles |
| `mechanism_profiles.csv` | 8×12 proportional profiles |
| `disease_counts.csv` | 8×14 raw counts |
| `mechanism_counts.csv` | 8×12 raw counts |
| `disease_bf.csv` | 8×14 log₂(BF) enrichment values |
| `mechanism_bf.csv` | 8×12 log₂(BF) enrichment values |
| `disease_rdm.csv` | 8×8 cosine distance matrix |
| `mechanism_rdm.csv` | 8×8 cosine distance matrix |
| `cluster_labels.csv` | Dendrogram leaf positions for row ordering |
| `dendrogram_data.pkl` | Linkage matrices and row orders |
| `within_pair_tests.csv` | Chi-square results for 4 anatomical pairs × 2 domains |
| `within_pair_residuals.csv` | Standardized residuals per category per pair |
| `pmid_overlap.csv` | Shared PMID counts for all 28 site pairs |
| `table3_distributions.csv` | Formatted distribution table |
| `fig2_bf_heatmap.png` | Main Figure 2 |
| `fig3_rdms.png` | Main Figure 3 |
| `dendrograms.png` | Disease and mechanism hierarchical clustering |

## Key takeaways for the manuscript

1. **Disease space is sharply differentiated.** Each site has a clear functional identity: GV4=Neurological, PC6=Cardiovascular, BL25/ST25=Gastrointestinal, CV12=Metabolic, SP6=Reproductive+Pain, ST36=generalist.

2. **Mechanism space is compressed.** Sites are far more similar in their mechanisms than in their diseases. The largest mechanism distance (0.73) is smaller than many disease distances. Inflammatory/Immune is the dominant mechanism across almost all sites. The mechanism dendrogram is shallower (max 0.50 vs 0.66) and most sites merge before distance 0.25.

3. **Anatomical pairs diverge in disease space but converge in mechanism space.** All 4 pairs are significantly different in disease (p<0.001). But SP6–ST36 are NOT significantly different in mechanism (p=0.31) despite being the most disease-divergent pair (χ²=150.5).

4. **BL25–GV4 is the strongest somatotopic independence case.** Zero shared PMIDs, closest anatomical pair, maximally dissimilar disease profiles (0.993). They are adjacent on the body and functionally opposite.

5. **PC6 shifts between spaces.** In disease space, PC6 is a late-merging outlier (Cardiovascular specialist). In mechanism space, PC6 merges early at distance 0.05 — its mechanisms are generic. This dissociation illustrates that a site can be a disease specialist but a mechanism generalist.

6. **PMID overlap needs monitoring.** SP6–ST36 share 67.5% of their records. Their mechanism similarity (0.016) could partly reflect shared studies. A07 publication-collapsing will test this.
