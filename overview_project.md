# Project Overview: Peripheral Nerve Stimulation Site Characterization

## Paper Identity

A peripheral nerve stimulation characterization paper. Eight stimulation sites are characterized across disease and mechanism domains. RSA validates that the characterization is internally consistent and independent of somatotopic location.

## Why Rats?

Inbred/outbred rat strains (SD, Wistar) offer minimal inter-individual anatomical variation — body proportions, vertebral counts, and limb geometry are highly consistent within a strain. This means stimulation site coordinates are reproducible across animals without the variability introduced by differences in body size, limb length, or spinal curvature seen in human studies. The rat is therefore the ideal model for constructing a standardized somatotopic coordinate system against which functional profiles can be compared.

## Data

- **Source:** AcupointDG database (acupointdg-research.com → PubMed)
- **8 stimulation sites:** BL25, GV4, ST25, CV12, PC6, LI4, SP6, ST36
- **1,974 records** (1,565 unique PMIDs), each with Disease and Mechanism annotations
- **101 records** with Mechanism = "Unknown"

## Manuscript Structure

### Methods (2.1–2.7)

| Section                         | Content                                                                                                                                                                                                                                | Analysis source      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| 2.1 Study Design & Data         | 8 sites, three-space RSA framework; AcupointDG → PubMed pipeline; data cleaning (typos, case normalization, special characters); record attrition accounting (1,974 total → exclusions for "Other" and "Unknown")                      | A01 (s00, s01)       |
| 2.2 Classification              | 14-category disease taxonomy (k=15, 877 strings) and 12-category mechanism taxonomy (k=13, 1,470 strings); keyword-based dictionaries with progressive inheritance; RDM stability analysis; inter-rater reliability                    | A01 (s02, s03) + IRR |
| 2.3 Functional Characterization | Proportional profile vectors (8 sites × k categories), cosine distance RDMs; Bayes Factor enrichment (Beta-Binomial, log₂ scale); within-pair chi-square tests with standardized residuals; shared-PMID record independence assessment | A03                  |
| 2.4 Three-Space RSA             | Two somatotopic RDMs: normalized 3D Euclidean surface distance + spinal segmental distance; 5 simple Mantel tests + 6 partial Mantel tests (Spearman, exact permutation with 8! = 40,320), repeated with both somatotopic definitions  | A02, A04             |
| 2.5 Disease–Mechanism Coupling  | Per-site contingency tables (disease × mechanism); NMI, joint entropy, top-3 cell concentration; tautology check for definitional overlap                                                                                              | A05                  |
| 2.6 Dimensionality Reduction    | MDS, PCA, CA biplots; bootstrap confidence ellipses (1,000 resamples); GV4 exclusion sensitivity                                                                                                                                       | A06                  |
| 2.7 Sensitivity Analyses        | Leave-one-out (8 site exclusions), bootstrap CI (1,000 resamples), subsample to n=22 (100 iterations), coordinate perturbation (1,000 iterations), "Other" category inclusion, publication-level collapsing                            | A07                  |

### Results (3.1–3.6)

| Section                             | Content                                                                                                                                                                                                                                                                          | Figures/Tables                  |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| 3.1 Functional Profiles             | Disease profiles show sharp specialist signals (GV4=Neurological, PC6=Cardiovascular, BL25/ST25=GI); mechanism profiles are compressed (max distance 0.73 < median disease distance); all anatomical pairs diverge in disease (p<0.001), SP6–ST36 converge in mechanism (p=0.31) | Fig 2, Fig 3, Table 3, Table S2 |
| 3.2 Somatotopic Independence        | Neither surface (r=-0.026) nor segmental (r=0.008) somatotopic distance correlates with disease or mechanism profiles; partial Mantel confirms no hidden signal; both definitions fail equally; exact permutation (40,320)                                                       | Fig 4, Table 4                  |
| 3.3 Disease–Mechanism Convergence   | Sites treating similar diseases engage similar mechanisms (r=0.426, p=0.032); survives control for both somatotopic definitions; coupling is direct, not mediated by body location                                                                                               | Fig 4 (left panel), Table 4     |
| 3.4 Specialist–Generalist Continuum | Within-site coupling varies: GV4 concentrates 62% in 3 cells, ST36 spreads across 123 cells (19.5% in top 3); PC6 is disease specialist but mechanism generalist; tautology check confirms coupling is not definitional                                                          | Fig 5                           |
| 3.5 Low-Dimensional Organization    | CA biplots capture 68.7% (disease) and 63.5% (mechanism) of association; disease space is spread wide, mechanism space collapses; PC6 shifts from isolation to central cluster; anatomical pair lines cross cluster boundaries                                                   | Fig 6                           |
| 3.6 Robustness                      | LOO r stable 0.31–0.60; bootstrap CI excludes zero (0.167–0.577); 0/1,000 perturbations produce significant somatotopic-disease signal; subsample to n=22 drops significance to 16% (power limitation); publication collapse and "Other" inclusion have zero effect              | Table S5, Fig S3–S7             |

### Main Figures (6)

| Fig | Title                                                                          | Content                                                | Source       |
| --- | ------------------------------------------------------------------------------ | ------------------------------------------------------ | ------------ |
| 1   | Study design and three-space representational framework                        | Study design + three-space conceptual diagram          | A02 + manual |
| 2   | Disease and mechanism enrichment profiles across eight stimulation sites       | BF heatmap (disease + mechanism enrichment)            | A03          |
| 3   | Representational dissimilarity matrices for disease, mechanism, and body space | Three RDMs (disease, mechanism, body space)            | A03 + A02    |
| 4   | Representational similarity analysis across three spaces                       | RSA scatterplots (3 RDM-to-RDM comparisons)            | A04          |
| 5   | Disease–mechanism coupling along a specialist–generalist continuum             | Disease–mechanism coupling (bars + bubble contingency) | A05          |
| 6   | Low-dimensional embedding of disease and mechanism space                       | CA biplots (disease + mechanism space)                 | A06          |

### Main Tables (4)

| Table | Content                                                                | Source           |
| ----- | ---------------------------------------------------------------------- | ---------------- |
| 1     | Acupoint characteristics: meridian, location, indication, record count | Literature + A01 |
| 2     | body space coordinates and spinal segmental innervation                | A02              |
| 3     | Disease and mechanism distributions: counts and % for all 8 sites      | A03              |
| 4     | Predicted dissociations for key pairs + Mantel/partial Mantel results  | A04              |

---

## Analysis Pipeline

### Status

| Analysis | Status | Description                                   |
| -------- | ------ | --------------------------------------------- |
| A01      | DONE   | Taxonomy Optimization                         |
| A02      | DONE   | Somatotopic Coordinate Construction           |
| A03      | DONE   | First-Order Characterization                  |
| A04      | DONE   | Three-Space RSA                               |
| A05      | DONE   | Disease–Mechanism Coupling                    |
| A06      | DONE   | Dimensionality Reduction                      |
| A07      | DONE   | Sensitivity and Robustness                    |
| IRR      | TODO   | Inter-Rater Reliability (parallel human task) |

### Dependencies

```
A01 (DONE) ─── classified dataset ──────────────────────────────┐
    │                                                            │
    ├──→ A02: Somatotopic Coordinates ─────────────────────┐     │
    │                                                      │     │
    ├──→ A03: First-Order Characterization ←───────────────┤     │
    │         (profiles, BFs, RDMs, clustering)            │     │
    │              │                                       │     │
    │              ├──→ A04: Three-Space RSA ←──────────────┘     │
    │              │         (Mantel, partial Mantel)             │
    │              │                                             │
    │              ├──→ A05: Disease–Mechanism Coupling           │
    │              │         (NMI, contingency tables)            │
    │              │                                             │
    │              └──→ A06: Dimensionality Reduction            │
    │                        (MDS, PCA, CA biplots)              │
    │                                                            │
    └──→ A07: Sensitivity (wraps around A03–A06) ←───────────────┘

    IRR: Inter-Rater Reliability (parallel, independent)
```

---

### A01: Taxonomy Optimization — COMPLETE

**Question:** How many disease and mechanism categories should we use?

**What this analysis does:**
We need to classify 877 unique disease strings and 1,470 unique mechanism strings from the AcupointDG database into a manageable number of categories. Too many categories → sparse profiles with many zero cells, unstable distance matrices. Too few → loss of discriminative signal between sites. We want the number where further splitting stops meaningfully changing the representational geometry.

**Method:**

- First, the raw base data is cleaned: typos are corrected (e.g., "obestiy"→"Obesity"), case inconsistencies unified (e.g., "depression"/"Depression" → most frequent variant), special characters normalized (smart quotes, en-dashes), and trailing whitespace/periods stripped. All corrections are logged.
- Then, deterministic keyword-based taxonomies are built at progressively finer granularity. Each disease/mechanism string is matched against curated keyword lists (case-insensitive). For comorbidity strings like "Depression with gastric dysfunction," only the condition before "with" is used. If no keyword matches, the record falls into "Other."
- Disease taxonomy has 7 levels (k=5 to k=15): starting with Pain, Neurological, Cardiovascular, Gastrointestinal, and progressively adding Metabolic/Endocrine, Psychiatric, Reproductive, Musculoskeletal, Respiratory, Immune/Inflammatory, Renal/Urological, Dermatological, Addiction, and Cancer/Oncology.
- Mechanism taxonomy has 8 levels (k=4 to k=13): starting with Inflammatory/Immune, Neuroprotective, Analgesic/Opioid, and progressively adding Autonomic/Neuroendocrine, Oxidative Stress, Gut-Brain/Enteric, Neurochemical Signaling, Cell Survival/Apoptosis, Ion Channel/Pain Transduction, Autophagy/Mitophagy, Metabolic Pathway, and Neural Circuit/Connectivity.
- Each level inherits all assignments from the previous level — only records in "Other" or in a category being split get reclassified. This ensures progressive refinement, not reshuffling.
- At each level, proportional profiles are built for the 8 sites (excluding "Other" and "Unknown"), cosine distance RDMs are computed, and Mantel correlation (Spearman, 10,000 permutations) is calculated between consecutive levels. When Mantel r approaches 1.0 between level k and level k+1, adding that extra category did not change the representational geometry — the elbow has been reached.
- The keyword lists were iteratively expanded across 4 rounds by inspecting unclassified "Other" records at each round, identifying missed synonyms, molecular terminology, and rare conditions.

**Result:**

- Disease: RDM stable from k=9 onward (r≈1.00). At k=15, only 0.6% of records remain "Other" (12 records).
- Mechanism: RDM stable from k=9 onward (r>0.96). At k=13, only 1.6% remain "Other" (31 records).
- Cross-domain Mantel: peak r=0.484 (disease k=7 × mechanism k=11, p=0.014), confirming moderate disease–mechanism convergence.
- "Other" record trajectory — Disease:

  | k (incl. "Other") | Named categories | "Other" records | % Other            |
  | ----------------- | ---------------- | --------------- | ------------------ |
  | 5                 | 4                | 681             | 34.5%              |
  | 7                 | 6                | 390             | 19.8%              |
  | 9                 | 8                | 223             | 11.3% ← RDM stable |
  | 11                | 10               | 104             | 5.3%               |
  | 13                | 12               | 74              | 3.7%               |
  | 14                | 13               | 20              | 1.0%               |
  | 15                | 14               | 12              | **0.6%**           |

- "Other" record trajectory — Mechanism:

  | k (incl. "Other") | Named categories | "Other" records | % Other            |
  | ----------------- | ---------------- | --------------- | ------------------ |
  | 4                 | 3                | 1,010           | 51.2%              |
  | 6                 | 5                | 690             | 35.0%              |
  | 8                 | 7                | 445             | 22.5%              |
  | 9                 | 8                | 273             | 13.8% ← RDM stable |
  | 10                | 9                | 199             | 10.1%              |
  | 11                | 10               | 184             | 9.3%               |
  | 12                | 11               | 107             | 5.4%               |
  | 13                | 12               | 31              | **1.6%**           |

- **Decision:** Use k=15 disease (14 categories) and k=13 mechanism (12 categories). The RDM is identical from k=9 onward, but "Other" records at k=9 are still 11.3% (disease) and 13.8% (mechanism). Going to the finest level drops these to 0.6% and 1.6%, recovering ~200+ records into the analysis without changing the representational geometry.

**Outputs:** `a01/results/datatables/` — combined_data.csv, disease_dictionary.csv, mechanism_dictionary.csv, stability curves, cross-domain heatmap, classification report.

---

### A02: Body Coordinate Construction

**Question:** How do we quantify how far apart two stimulation sites are on the body?

**What this analysis does:**
The RSA framework compares three representational spaces: disease, mechanism, and somatotopic. Disease and mechanism distances come from the classified data (A03). Somatotopic distance must come from anatomy — we need a number expressing "how far apart are BL25 and PC6 on the rat's body?" This analysis constructs that distance matrix.

**Method:**
Each site is assigned a 3D coordinate (x, y, z in mm) based on the 2024 Chinese national standard "Nomenclature and location of acupuncture points for laboratory animals Part 2: Rat," with supporting measurements from site-specific publications:

- **x** (medio-lateral): mm from midline
- **y** (cranio-caudal): mm from nose tip
- **z** (dorso-ventral): mm from table surface

| Site | x (mm) | y (mm) | z (mm) | Spinal segment | Spinal level | Reference                           |
| ---- | ------ | ------ | ------ | -------------- | ------------ | ----------------------------------- |
| BL25 | 6.0    | 155.0  | 35.0   | L4             | 25.0         | 2024 standard; Han 2011             |
| GV4  | 0.0    | 145.0  | 38.0   | L2             | 23.0         | 2024 standard; Wang 2016            |
| ST25 | 5.0    | 135.0  | 0.0    | T10-T11        | 18.5         | PMC7306073; PMC9731770              |
| CV12 | 0.0    | 115.0  | 0.0    | T7-T8          | 15.5         | 2024 standard; Wang 2013            |
| PC6  | 20.0   | 90.0   | 15.0   | C8-T1          | 8.5          | 2024 standard; PMC6843597           |
| LI4  | 25.0   | 85.0   | 5.0    | C7-C8          | 7.5          | 2024 standard; Li 2019              |
| SP6  | 8.0    | 185.0  | 8.0    | L4-S1          | 26.5         | 2024 standard; Senna-Fernandes 2011 |
| ST36 | 15.0   | 175.0  | 10.0   | L4-L5          | 25.5         | 2024 standard; multiple             |

The three axes have very different physical ranges: y spans 100mm, z spans 38mm, x spans 25mm. If Euclidean distance is computed on raw millimeters, the y-axis dominates — the RDM would mostly measure "forelimb vs trunk vs hindlimb" and ignore the dorsal–ventral and medial–lateral dimensions. But somatotopic organization is not one-dimensional: BL25 (dorsal lumbar) and ST25 (ventral abdomen) are on opposite sides of the body at the same vertebral level — this should be a large somatotopic distance, driven by the z-axis. To give each spatial dimension equal weight, coordinates are z-score normalized (mean=0, std=1 per axis) before computing Euclidean distance. This is standard practice when input variables have different scales.

A second somatotopic RDM is computed from spinal segmental innervation. Spinal segments are manually assigned from the dermatome literature (see references below), then encoded numerically (C1=1, C2=2, ... T1=9, T2=10, ... L1=22, L2=23, etc.). For sites spanning two segments (e.g., T10-T11), the midpoint is used (18.5). The segmental RDM is the absolute difference between numeric levels: e.g., BL25 (L4=25.0) vs ST36 (L4-L5=25.5) = 0.5, while BL25 vs PC6 (C8-T1=8.5) = 16.5.

This is not merely a robustness check with a different ruler — it tests a mechanistically distinct hypothesis. The surface RDM asks: "do sites that are physically close on the body have similar functional profiles?" The segmental RDM asks: "do sites that share spinal cord input have similar functional profiles?" These are different questions because sites can be geometrically distant but segmentally close (e.g., BL25 and ST36 are on different body surfaces but both innervated at L4–L5, sharing virtually the same spinal input). If segmentally close sites have similar functional profiles while geometrically close sites don't, that would point to a genuine spinal segmental mechanism underlying acupoint function. If neither RDM correlates with function, the conclusion is airtight: functional identity is independent of somatotopy regardless of whether body space is defined by skin proximity or neural wiring.

The rat dermatome map is well-established through direct neural tracing studies. Key references for the segmental assignments:

- **China Association of Acupuncture and Moxibustion**: Nomenclature and location of acupuncture points for laboratory animals Part 2: Rat (https://www.sciencedirect.com/science/article/pii/S1003525724000801)
- **Takahashi et al. 2003** (PMID: 12761822): Mapped dermatomes and their central projections in the spinal cord dorsal horn using DiI fluorescent tracer applied to 21 reference points on rat trunk and hindlimb skin. Established the definitive rat dermatome map with DRG segmental distributions.
- **Takahashi & Nakajima 1996** (PMID: 8895248): Determined rat limb dermatomes by antidromic C-fiber stimulation of spinal nerves with Evans blue extravasation. Established dermatome boundaries for forelimb (C1–T1) and hindlimb (T12–S2).
- **Takahashi & Ohtori 1994** (PMID: 7518069): Dermatome mapping in rat hindlimb by electrical stimulation of spinal nerves.
- **Li et al. 2019** (PMID: 31275083 / PMC6624843): Neural pathway tracing of acupoints LI4 and LR3 with cholera toxin subunit B (CTB), confirming LI4 sensory neurons span C5–T1 DRG.

One nuance: the segmental RDM uses dermatomal (cutaneous) innervation, but needling also stimulates deep structures (muscle, fascia, periosteum) which can have slightly different segmental innervation than the overlying skin. For most of our 8 sites, cutaneous and deep innervation agree (e.g., ST36 skin and tibialis anterior muscle are both L4–L5 via deep peroneal nerve). The ±15% perturbation on numeric spinal levels partially accounts for any discrepancy.

A coordinate perturbation analysis (±15% uniform jitter, 1,000 iterations) tests whether the distance structure is sensitive to coordinate uncertainty — particularly important for limb x-coordinates, which depend on posture.

**Outputs:** site_coordinates.csv, surface_rdm.csv (normalized), surface_rdm_raw.csv, segmental_rdm.csv, perturbed_rdms.pkl → Table 2, Fig 1 (Panel A), feeds A04 and A07.

---

### A03: First-Order Characterization

**Question:** What is the functional identity of each stimulation site?

**What this analysis does:**
This is the core characterization step. For each site, we ask: what diseases is it studied for, and through what mechanisms? The answer takes the form of a proportional profile — a vector showing the fraction of that site's records in each category. Sites with similar profiles are functionally similar; sites with different profiles have distinct functional identities.

**Method:**

_Profile construction (s01):_ Each record is assigned its disease category (level_7 from A01) and mechanism category (level_8 from A01). Records classified as "Other" or "Unknown" are excluded. For each site, the proportion of records in each category is computed, yielding an 8×14 disease profile matrix and an 8×12 mechanism profile matrix.

_Bayes Factor enrichment (s02):_ For each site × category cell, a Bayes Factor quantifies whether that site is enriched or depleted for that category relative to the pooled baseline (all 8 sites combined). The model is Beta-Binomial: under the null, the site's rate equals the pooled rate; under the alternative, the rate is drawn from a uniform Beta(1,1) prior. The log₂(BF) is computed — positive values indicate enrichment (site has more of this category than expected), negative values indicate depletion. BF > 3 (log₂ > 1.58) is conventionally considered "substantial" evidence.

_RDM construction (s03):_ Cosine distance (1 − cosine similarity) between each pair of sites' profile vectors gives the 8×8 disease RDM and mechanism RDM. These are the primary analytical objects for all downstream RSA.

_Hierarchical clustering (s04):_ Average-linkage clustering on cosine distance reveals natural groupings. Sites are assigned to clusters, which determine row ordering in all heatmaps and RDMs for visual consistency across figures.

_Within-pair tests (s05):_ The 4 anatomical pairs (BL25-GV4, ST25-CV12, PC6-LI4, SP6-ST36) are tested with chi-square to confirm they have significantly different profiles. Standardized residuals identify which specific categories drive divergence within each pair.

_Record independence (s06):_ Because some PMIDs appear in multiple sites (multi-site studies), we count shared PMIDs across all 28 site pairs to assess how much of the data is shared vs independent.

**Key expected findings:**

- GV4 is a neurological specialist (strong enrichment for Neurological disease, depletion elsewhere)
- PC6 is a cardiovascular specialist
- ST25 and BL25 are gastrointestinal
- ST36 is a generalist (no strong enrichment or depletion — profile near the population average)
- The disease panel will show sharp differentiation; the mechanism panel will appear more muted — first evidence of "mechanism compression" (sites are more similar in how they work than in what they treat)
- Anatomically paired sites will NOT be adjacent in the clustering — they have dissimilar functional profiles despite being physically close

**Outputs:** profiles, count matrices, BF matrices, RDMs, cluster labels, within-pair tests, PMID overlap → Fig 2, Fig 3, Table 3, Table S2, S3, S6.

---

### A04: Three-Space RSA

**Question:** Do disease and mechanism representations converge, and is this convergence independent of somatotopy?

**What this analysis does:**
This is the central statistical test of the paper. We have three 8×8 distance matrices (disease, mechanism, somatotopic) and we ask whether their structures are correlated. If disease and mechanism RDMs correlate positively, it means sites that treat similar diseases also engage similar biological mechanisms — convergent validity. If neither functional RDM correlates with the somatotopic RDM, it means functional organization is independent of body location. If the somatotopic–mechanism correlation disappears after controlling for disease (partial Mantel), it means any apparent anatomy–mechanism link is mediated through disease, not direct.

**Method:**

_Simple Mantel test:_ The upper triangle of each RDM is vectorized (28 pairwise distances). Spearman rank correlation between two vectors measures structural correspondence. Significance is assessed by permutation: rows and columns of one RDM are shuffled together 10,000 times, and the proportion of permuted correlations ≥ observed gives the p-value.

_Partial Mantel test:_ To test whether the correlation between two RDMs survives after controlling for a third, each vector is regressed on the control vector, and the residuals are correlated. This asks: "after removing the variance explained by somatotopy, do disease and mechanism distances still correlate?"

Six simple and six partial Mantel tests are run — once with the surface (Euclidean) somatotopic RDM, once with the segmental RDM. This tests whether the results hold under both definitions of body space.

**Key expected findings:**

- Disease × Mechanism: significant positive Mantel r — the core convergence result
- Disease × Surface Somatotopic: not significant — skin proximity doesn't predict disease profile
- Disease × Segmental Somatotopic: not significant — spinal wiring doesn't predict disease profile either
- Mechanism × Somatotopic: possibly weak/marginal — but partial Mantel controlling for disease should eliminate it
- The combination of null results across both somatotopic definitions makes the independence claim airtight against the reviewer objection "you used the wrong definition of body space"
- BL25–ST36 is the critical test case: segmentally nearly identical (0.5 levels, both L4–L5) but expected to have different functional profiles — direct evidence that shared spinal input does not determine acupoint function

**Outputs:** mantel_results.csv, table4_mantel.csv → Fig 4, Table 4.

---

### A05: Disease–Mechanism Coupling

**Question:** Within each site, how tightly are disease and mechanism linked?

**What this analysis does:**
A04 tests cross-site convergence (do sites with similar diseases use similar mechanisms?). A05 asks a different question: within a single site, is there a tight mapping from specific diseases to specific mechanisms, or does the site use the same mechanisms for everything?

**Method:**

_Contingency tables (s01):_ For each site, a disease × mechanism crosstab (14×12) shows how many records fall in each disease–mechanism combination. From this, three metrics are computed:

- **NMI (normalized mutual information):** How much knowing the disease tells you about the mechanism (and vice versa). High NMI = tight coupling (specialist); low NMI = loose coupling (generalist).
- **Joint entropy:** How spread out the records are across the contingency table. High entropy = many different disease–mechanism combinations; low entropy = concentrated in a few.
- **Top-3 concentration:** What percentage of the site's records fall into just the 3 largest disease–mechanism cells. GV4 might have ~60% in three cells (Neurological × Neuroprotective dominates); ST36 might have ~20% (broadly distributed).

_Tautology check (s02):_ Some disease–mechanism pairs overlap definitionally (e.g., "Pain" disease × "Analgesic/Opioid" mechanism — if a paper studies pain treatment, it almost certainly involves analgesic mechanisms). These tautological pairs could inflate NMI artificially. The check: recompute NMI after excluding records in tautological cells and verify that the coupling pattern (specialist vs generalist ranking) survives.

**Key expected findings:**

- GV4: highest concentration (62%) — nearly all bubbles in the Neurological row, but spanning multiple mechanism columns (Neuroprotective 28%, Autophagy 17%, Cell Survival 17%). Disease specialist, mechanism generalist.
- ST36: lowest concentration (19.5%) — records spread across 123 cells, top cell only 8%. Broadest generalist.
- PC6: two disease rows nearly tied (Cardiovascular 10.8%, Neurological 10.2%), both channeling through Inflammatory/Immune — spread across both dimensions.
- CV12: three competing disease rows (Metabolic, Neurological, GI) — intermediate coupling.
- This establishes a specialist–generalist continuum that adds a dimension beyond the profile-level characterization in A03

**Outputs:** contingency_tables.pkl, coupling_metrics.csv, tautology_check.csv → Fig 5, Table S4.

---

### A06: Dimensionality Reduction

**Question:** What does the functional landscape look like?

**What this analysis does:**
The profile vectors and RDMs from A03 live in high-dimensional space (14 or 12 dimensions). Dimensionality reduction projects the 8 sites into 2D so we can visualize their spatial relationships — which sites cluster together, which are outliers, how spread out is disease space vs mechanism space.

**Method:**

_MDS (s01):_ Multidimensional scaling takes the 8×8 cosine distance RDM and finds 2D coordinates that best preserve the pairwise distances. Stress value measures how well the 2D embedding approximates the full-dimensional distances. Applied to both disease and mechanism RDMs.

_PCA (s02):_ Principal component analysis on the proportional profile matrices finds the axes of maximum variance. Unlike MDS (which works on distances), PCA works directly on the profiles and provides loadings — which categories contribute most to each axis.

_Correspondence analysis (s03):_ CA is specifically designed for count data (contingency tables). It positions both sites AND categories in the same space — a biplot where you can see that PC6 sits near the "Cardiovascular" label and GV4 near "Neurological." This makes the embedding self-explanatory. Inertia (analogous to variance explained) is reported per axis.

_Bootstrap confidence ellipses (s04):_ The 8 sites have very different sample sizes (BL25: 22, ST36: 1,174). How stable is each site's position? We resample records within each site 1,000 times, recompute profiles, re-embed, and draw 95% confidence ellipses around each site's position. Large ellipses for small-n sites (BL25, GV4) honestly communicate positional uncertainty.

_GV4 exclusion (s05):_ GV4 is expected to be the most extreme specialist (almost entirely Neurological). Does the cluster structure of the remaining 7 sites survive its removal? This tests whether the characterization depends on one dominant signal.

**Key expected findings:**

- Disease space: well-separated clusters (GI cluster, cardiovascular outlier, broad cluster)
- Mechanism space: same sites but more compressed — closer together, less separation between clusters. This is the "mechanism compression" finding visualized.
- Dashed lines connecting anatomical pairs should cross cluster boundaries — anatomy ≠ function
- GV4 will be an outlier in disease space; removing it should not collapse the remaining structure

**Outputs:** MDS/PCA/CA coordinates, bootstrap ellipses → Fig 6, Fig S1–S2, Fig S4, Table S3.

---

### A07: Sensitivity and Robustness

**Question:** Are the findings stable under perturbation?

**What this analysis does:**
Every finding in the paper depends on choices: which records to include, how many categories, which coordinates, whether to weight by publication. A07 systematically perturbs each choice and checks whether the core findings (disease–mechanism Mantel convergence, somatotopic independence, site characterization) survive.

**Method:**

_Leave-one-out (s01):_ For each of the 8 sites, exclude it entirely, recompute 7×7 RDMs, and re-run the disease–mechanism Mantel test. If any single site drives the result (e.g., the convergence depends entirely on ST36), it will disappear when that site is excluded.

_Bootstrap CI (s02):_ Resample records within each site with replacement (1,000 iterations), recompute profiles and RDMs, compute disease–mechanism Mantel r. This gives a 95% confidence interval for the main Mantel result.

_Subsample to n=22 (s03):_ ST36 has 1,174 records while BL25 has 22. Does ST36's dominance drive the results? Subsample all sites to n=22 (BL25's count, 100 iterations) and check whether Mantel r remains significant with equalized sample sizes.

_Coordinate perturbation (s04):_ Load the 1,000 perturbed somatotopic RDMs from A02, and for each, recompute somatotopic–disease and somatotopic–mechanism Mantel tests. If the null somatotopic result holds across 95%+ of perturbations, it's robust to coordinate uncertainty.

_"Other" inclusion (s05):_ In the main analysis, records classified as "Other" are excluded. What if we include them as a category? Recompute profiles and Mantel r. If the result changes substantially, the findings depend on the exclusion choice.

_Publication-level collapsing (s06):_ Some PMIDs appear multiple times within a site (same study, multiple records). Collapse to one record per PMID per site (majority-vote category), recompute everything. Tests whether the findings reflect genuine research diversity or lab-clustering artifacts.

_Subsample coupling (s08):_ The specialist–generalist continuum (A05) could be confounded with sample size — sites with more records mechanically spread across more cells, lowering top-3 concentration. All sites are subsampled to n=22, top-3 concentration is recomputed, and the process is repeated 1,000 times. Tests whether the ranking is a sample size artifact.

**Key expected findings:**

- Leave-one-out: Mantel r should remain positive across all 8 exclusions (no single site drives convergence)
- Bootstrap: 95% CI should exclude zero
- Subsample: Mantel r should remain positive, though possibly not significant at n=22 (expected — power is low with only 7×7/2=21 pairs)
- Coordinate perturbation: >95% of iterations should show non-significant somatotopic–disease and somatotopic–mechanism Mantel tests
- "Other" inclusion and publication collapsing should not qualitatively change the Mantel result
- Subsample coupling: GV4 remains the most concentrated and ST36/SP6 the least at equal n=22, but the spread compresses from 42.6 to 30.6 percentage points. The qualitative ranking holds; the quantitative gap is inflated by unequal sample sizes.

**Outputs:** loo_results.csv, bootstrap CI, subsample results, perturbation results, other_inclusion, pub_collapse, subsample_coupling.csv → Table S5, Fig S3, S5–S7.

---

### IRR: Inter-Rater Reliability — PARALLEL HUMAN TASK

**Not computational.** A second rater independently reviews the disease and mechanism dictionaries (877 + 1,470 strings). Cohen's kappa is computed overall and for ambiguous subsets (strings that could plausibly belong to multiple categories). Disagreements are resolved by discussion. Dictionaries are frozen after resolution.

**Outputs → Table S1 (kappa values)**

---

## Key Concepts

### What is a profile vector?

A proportional profile vector is simply: for each site, count how many of its records fall in each category, then divide by the total. BL25 with 22 records might have 0/22=0% Pain, 2/22=9% Neurological, 0/22=0% Cardiovascular, 15/22=68% Gastrointestinal, etc. This vector IS the site's functional identity in that domain.

### What is an RDM?

A representational dissimilarity matrix is an 8×8 matrix where cell (i,j) contains the distance between site i and site j's profile vectors. We use cosine distance (1 − cosine similarity), which measures the angle between two vectors regardless of their magnitude. Two sites with identical proportional profiles have distance 0; two sites with completely non-overlapping profiles have distance 1.

### What is RSA?

Representational Similarity Analysis compares RDMs across different domains. If the disease RDM and mechanism RDM have similar structure (same pairs of sites are close/far), it means disease-space organization and mechanism-space organization are aligned. The Mantel test quantifies this: it correlates the 28 unique pairwise distances from one RDM against the 28 from another.

RSA originated in computational neuroscience (Kriegeskorte et al., 2008) for comparing neural population representations across brain regions, species, and computational models. In neuroimaging, each "item" is a stimulus that evokes a measurable neural response pattern, and the RDM captures pairwise distances between these patterns. Our application differs in three ways: (1) items are stimulation sites rather than stimuli, (2) representations are literature-derived proportional profiles rather than neural activity patterns, and (3) we have only 8 items (28 pairwise distances) rather than the dozens-to-hundreds typical in neuroimaging RSA.

However, RSA is not inherently a neuroimaging method. The underlying Mantel test (Mantel, 1967) was developed for spatial epidemiology and has been widely applied in ecology (comparing species assemblage matrices), population genetics (comparing genetic and geographic distance matrices), and behavioral science. RSA is agnostic to the source of the representations — it only requires that items can be characterized by profile vectors and that pairwise distances between profiles are meaningful. Our proportional profiles and cosine distance RDMs satisfy these requirements.

The primary methodological consequence of 8 items is low statistical power — 28 pairwise distances provide limited degrees of freedom for correlation testing. We mitigate this through: (a) exact permutation (all 8! = 40,320 permutations, eliminating Monte Carlo noise), (b) bootstrap confidence intervals (1,000 resamples), and (c) subsample sensitivity analysis (equalizing to n=22 per site) that honestly reports the power limitation (16% significance rate at equalized sample sizes).

### What is a Mantel test?

A permutation-based correlation test for distance matrices. Correlate the upper triangles of two RDMs (Spearman rank correlation). Assess significance by shuffling rows/columns of one RDM together (preserving the dependence structure among pairwise distances) and computing the proportion of permuted correlations ≥ observed. Originally developed by Mantel (1967) for testing spatial clustering of disease cases, it predates neuroimaging RSA by four decades. In our study, we use exact (exhaustive) permutation with all 8! = 40,320 possible site-label permutations, yielding exact p-values with no sampling error.

### What is record attrition?

A PRISMA-style accounting of how many records are available at each stage. We start with 1,974 records. Some are excluded because their disease string didn't match any keyword category ("Other": 12 for disease, 31 for mechanism). Some have unknown mechanisms (101). The remaining records form the basis of all profiles and analyses. This is reported so reviewers can assess whether exclusions bias the results.

### What is mechanism compression?

The hypothesis that stimulation sites are more differentiated in what diseases they treat than in what biological mechanisms they engage. Disease profiles show sharp specialist signals (GV4 is almost entirely Neurological). Mechanism profiles look more uniform — all sites engage Inflammatory/Immune and Neuroprotective pathways to some degree. The mechanism RDM should appear "darker" (lower distances, more similarity between sites) than the disease RDM.

### What is the specialist–generalist continuum?

Sites vary in how concentrated their research is. A specialist site (GV4) has most records in a few disease–mechanism cells. A generalist site (ST36) has records spread broadly across many combinations. This isn't about sample size — it's about how tightly the site's disease applications are coupled to specific mechanisms.

---

## Directory Structure

```
2026-01-ProfileAcu/
├── base_data/                  8 cleaned xlsx files
├── overview_project.md         this file
├── analysisplan.md             figure-level design spec
├── pyproject.toml              shared dependencies (uv)
│
├── a01/                        Taxonomy Optimization (DONE)
│   ├── a01_plan.md
│   ├── scripts/
│   └── results/{datatables,figures}/
│
├── a02/                        Somatotopic Coordinates
│   ├── scripts/
│   └── results/{datatables,figures}/
│
├── a03/                        First-Order Characterization
│   ├── scripts/
│   └── results/{datatables,figures}/
│
├── a04/                        Three-Space RSA
│   ├── scripts/
│   └── results/{datatables,figures}/
│
├── a05/                        Disease–Mechanism Coupling
│   ├── scripts/
│   └── results/{datatables,figures}/
│
├── a06/                        Dimensionality Reduction
│   ├── scripts/
│   └── results/{datatables,figures}/
│
└── a07/                        Sensitivity and Robustness
    ├── scripts/
    └── results/{datatables,figures}/
```

## Supplementary Materials

### Supplementary Data (2)

| #       | Content                                                                    |
| ------- | -------------------------------------------------------------------------- |
| Data S1 | Disease controlled vocabulary dictionary (877 strings → 14 categories)     |
| Data S2 | Mechanism controlled vocabulary dictionary (1,470 strings → 12 categories) |

### Supplementary Tables (6)

| #   | Content                                                                                             | What it proves                                                     |
| --- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| S1  | Dataset quality: per-site attrition, exclusion rates, inter-rater kappa, unique first-author groups | Classified dataset is reliable, balanced, not driven by a few labs |
| S2  | Within-pair chi-square and standardized residuals                                                   | Paired sites differ, with category-level detail                    |
| S3  | Bayes Factors (disease + mechanism) with MDS/PCA coordinates                                        | Exact values behind Fig 2 and Fig 6                                |
| S4  | Tautology check: flagged disease–mechanism pairs, NMI with/without                                  | Coupling is not an artifact of category overlap                    |
| S5  | Sensitivity: profiles under 3 conditions (original, publication-collapsed, Other-included)          | Core findings survive alternative choices                          |
| S6  | Full cosine similarity matrices (disease + mechanism, all 28 pairs)                                 | Exact pairwise values behind Fig 3                                 |

### Supplementary Figures (7)

| #     | Content                                                             | What it proves                                                    |
| ----- | ------------------------------------------------------------------- | ----------------------------------------------------------------- |
| S1    | Disease space: (A) MDS with bootstrap ellipses, (B) PCA            | Low-dimensional structure is method-independent                   |
| S2    | Mechanism space: (A) MDS with bootstrap ellipses, (B) PCA          | Mechanism compression confirmed across embedding methods          |
| S3    | Coordinate perturbation: Mantel p-values across 1,000 jittered sets | Null somatotopic result holds under coordinate uncertainty        |
| S4    | GV4-exclusion: embeddings recomputed without extreme site           | Cluster structure survives strongest single-domain signal removal |
| S5    | Leave-one-out: disease–mechanism Mantel r across 8 exclusions       | No single site drives the convergence finding                     |
| S6    | Subsampling: Mantel r when all sites subsampled to n=22             | Finding isn't a sample-size artifact of ST36                      |
| S7    | Publication-collapsing: profiles before vs. after for small-n sites | Profiles reflect research diversity, not lab-clustering           |
