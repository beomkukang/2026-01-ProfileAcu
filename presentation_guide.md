# Presentation Guide: Functional Profiles of Somatic Stimulation Sites: A Three-Space Representational Similarity Analysis in Rats

## Presentation Structure

| Section      | Slides         | Time (est.) |
| ------------ | -------------- | ----------- |
| Introduction | 1–6            | ~5 min      |
| Methods      | 7–10           | ~4 min      |
| Results      | 11–16          | ~6 min      |
| Discussion   | 17–20          | ~3 min      |
| **Total**    | **~20 slides** | **~18 min** |

---

## Introduction (Slides 1–6)

### Slide 1: Title Slide

**Title:** Functional Profiles of Somatic Stimulation Sites: A Three-Space Representational Similarity Analysis in Rats

▪ Authors, affiliations, conference name
▪ _No figure needed_

---

### Slide 2: The Problem — What Is the Point?

**Title:** Acupoint Specificity: An Unresolved Question

▪ Acupuncture point specificity — whether different points produce different therapeutic effects — remains one of the most debated questions in the field (Langevin & Wayne, 2018)
▪ Individual studies have demonstrated specificity at the circuit level (Liu et al., 2021)
▪ But these are single-point, single-pathway demonstrations — we still lack a systematic characterization of how sites differ across multiple functional domains simultaneously
▪ Neuroimaging has given us a rather collective view of how acupoints work in a higher level
▪ How do we move from "discerning acupoint specificity" to "understanding acupoints"?

**Purpose:** Frame the central question — specificity exists at the single-point level, but we lack a systematic framework for characterizing it across many points simultaneously.
_No figure needed_

> **Framework link:** The sham acupuncture paradox (comparable effects at verum vs sham) reflects a conflation of field specificity (where) with projective specificity (what it does). Our study isolates the projective question.

---

### Slide 3: From Neural Patterns to Bodily Maps

**Title:** A Profile-Centric Understanding of Acupoint Identity

▪ Kang et al. showed that common brain mechanisms may be hard to catch through contemporary neuroimaging for acupuncture across diseases
▪ Yoon et al. stated that acupoint identity is defined by distributed bodily outcomes (sensation patterns, therapeutic indications), not by central representations such as neuroimaging alone
▪ The double-dissociation model proposes crossed selectivity as the standard for specificity claims (Chae et al., 2026; cf. Poldrack, 2006)
▪ We need body-centered characterization: what outcomes does each point produce across disease and mechanism domains?

**Purpose:** Argue that the field needs to move from brain-centered to body/outcome-centered characterization of specificity.
_No figure needed_

> **Framework link:** This maps to the distinction between body-spatial (℘ᴵ) and functional (℘ᴱ) facets of the projective field. Brain imaging captures central encoding; our disease/mechanism profiles sample ℘ᴱ directly.

---

### Slide 4: Prior Data-Driven Approaches

**Title:** Data Mining Approaches to Acupoint Characterization

▪ Classical text mining: tf-idf analysis of acupoint/meridian × disease site associations from Chimgoogyeongheombang and DongUiBoGam showed each acupoint and meridian has distinct constellation patterns associated with its meridian route (Jung et al., 2015; Chae et al., 2019)
▪ Clinical data mining: MDS of five-phase acupoints from 421 RCTs showed stream and sea acupoints cluster distinctly by indication (Lee et al., 2022); hierarchical clustering and MDS of Source acupoints revealed LR3, LI4, HT7, KI3 have distinct properties in reduced space (Choi et al., 2021); acupoint selection patterns differ by pain condition (Hwang et al., 2021); clinician surveys revealed commonality (ST36, LI4, LR3 across diseases) and specificity (three disease clusters with distinct point selections) (Lee et al., 2020); symptom mapping in chronic pain patients showed distal activation along meridian routes vs. local activation near trunk (Jung et al., 2017)
▪ These approaches show WHICH points are selected for WHICH conditions — but not whether their disease X mechanism profiles differ
▪ We need simultaneous characterization across disease AND mechanism domains, not just disease-point associations

**Purpose:** Show that data-driven approaches have been productive, but they characterize selection patterns, not the underlying functional/mechanistic profiles.
_No figure needed_

> **Framework link:** Prior work characterizes field coordinates (ℱₐ — where clinicians select points) and disease associations. We extend to full projective profiles (℘ₐ — what the point does across multiple outcome facets).

---

### Slide 5: Our Approach — Three-Space RSA

**Title:** Three-Space Representational Similarity Analysis

▪ Characterize 8 stimulation sites across three representational spaces simultaneously:
  - **Disease space:** What conditions is each site studied for? (14 categories)
  - **Mechanism space:** Through what biological pathways? (12 categories)
  - **Somatotopic space:** Where is each site on the body? (3D coordinates + segmental innervation)
▪ RSA compares the structure of these spaces: Do sites that treat similar diseases engage similar mechanisms? Is functional organization related to body location?
▪ Inbred Rat models: Standardized transpositional acupoint systems have been established for rats, enabling reproducible coordinate-based localization across studies (Yin et al., 2008, PMID: 17559895)

**Purpose:** Introduce the framework and why rats are ideal.
_Figure: Three-space conceptual diagram (Fig 1)_

> **Framework link:** Disease and mechanism profiles are category-discretized samples of the functional projective field ℘ᴱ. Somatotopic coordinates approximate the field coordinate ℱₐ by its mode. The Mantel test between somatotopic and functional RDMs directly tests field-projective dissociability.

---

### Slide 6: Data Overview

**Title:** Data Acquisition and Overview
Dataset: 1,974 Records Across 8 Stimulation Sites

▪ Source: AcupointDG database (PubMed-indexed studies)
▪ 8 sites: BL25, GV4, ST25, CV12, PC6, LI4, SP6, ST36
▪ Each record annotated with Disease and Mechanism
▪ Classified into 14 disease categories and 12 mechanism categories via keyword-based taxonomy (RDM-stable from k=9)
▪ Sample sizes range from 22 (BL25) to 1,174 (ST36)

**Purpose:** Establish the dataset.
_Figure: Table 1 (site characteristics) or a simple site-count bar chart_

---

## Methods (Slides 7–10)

### Slide 7: Profile Construction & RDMs

**Title:** Constructing Functional Profiles and Distance Matrices

▪ Each site's records classified into disease (14) and mechanism (12) categories
▪ Proportional profile vector = fraction of records in each category
▪ Cosine distance between profile vectors → 8x8 Representational Dissimilarity Matrix (RDM)
▪ Bayes Factor enrichment quantifies site-specific specialization vs pooled baseline

**Purpose:** Explain the core analytical objects (profiles → RDMs).
_Figure: Schematic showing records → profiles → RDM pipeline_

---

### Slide 8: Somatotopic Coordinates

**Title:** Two Definitions of Body Space

▪ Surface RDM: 3D Euclidean distance (x, y, z in mm), z-score normalized so each axis contributes equally
▪ Segmental RDM: Spinal segmental distance from dermatomal innervation
▪ Why two? They test different hypotheses:
  - Surface: "Do physically close sites have similar functions?"
  - Segmental: "Do sites sharing spinal cord input have similar functions?"
▪ Both are needed to preempt the reviewer objection "wrong definition of body space"

**Purpose:** Explain the somatotopic RDMs and why both are necessary.
_Figure: Table 2 (coordinates) or body diagram with sites labeled_

---

### Slide 9: Mantel Tests (RSA)

**Title:** Comparing Representational Spaces

▪ RSA originated in computational neuroscience (Kriegeskorte et al., 2008) for comparing neural representations; the underlying Mantel test is domain-general (Mantel, 1967 — spatial epidemiology) and has been widely applied in ecology, genetics, and behavioral science
▪ Mantel test: Spearman correlation between upper triangles of two RDMs (28 pairwise distances)
▪ Exact permutation: all 8! = 40,320 permutations for precise p-values (no Monte Carlo noise)
▪ Key limitation: 8 sites yield only 28 pairwise distances — low statistical power compared to typical neuroimaging RSA (50+ items). Addressed by exact permutation, bootstrap CI, and subsample sensitivity analysis
▪ Simple Mantel + Partial Mantel (controlling for third RDM), repeated with both body-space definitions

**Purpose:** Explain the statistical framework and acknowledge its power limitation transparently.
_No figure needed_

---

### Slide 10: Additional Analyses

**Title:** Coupling, Embeddings, and Robustness

▪ **Disease-mechanism coupling:** Per-site contingency tables, NMI, top-3 concentration → specialist-generalist continuum
▪ **Dimensionality reduction:** Correspondence Analysis biplots (sites + categories in shared 2D space)
▪ **Sensitivity:** Leave-one-out, bootstrap CI, subsample to n=22, coordinate perturbation (1,000 iterations), publication collapsing

**Purpose:** Briefly mention the supporting analyses so results slides make sense.
_No figure needed_

---

## Results (Slides 11–19)

### Slide 11: Functional Profiles

**Title:** Disease Differentiation, Mechanism Compression

▪ **Disease space is sharply differentiated:** GV4 = 87.9% Neurological, PC6 = 39.4% Cardiovascular, BL25/ST25 = GI dominant, ST36 = generalist (top category only 27%)
▪ **Mechanism space is compressed:** mean mechanism distance (~0.20) vs mean disease distance (~0.50); all sites share Inflammatory/Immune dominance
▪ SP6–ST36: disease-divergent (p = 1.6x10⁻²⁵) but mechanism-identical (cosine distance 0.016, p = 0.31)
▪ Sites are far more differentiated in what they treat than in how they work

**Purpose:** Establish the disease-mechanism asymmetry — the first key finding.
_Figure: Fig 2 (both panels — BF heatmap, disease top, mechanism bottom)_

---

### Slide 12: Three Spaces Compared

**Title:** Disease, Mechanism, and Body Space Have Different Structures

▪ Disease RDM: High contrast (0.08–0.99), clear block structure
▪ Mechanism RDM: Uniformly dark (compressed), only GV4 stands out
▪ Body-space RDM: Completely different pattern — does not map onto either functional RDM
▪ **BL25–GV4:** Closest anatomical pair (surface distance 0.78) but most dissimilar disease profiles (0.993). Zero shared PMIDs. Adjacent on the body, opposite in function.

**Purpose:** Visual comparison of the three spaces, anchored by the strongest single-pair example.
_Figure: Fig 3 (three RDM heatmaps, with BL25-GV4 highlighted)_

---

### Slide 13: RSA Results

**Title:** Body Location Is Independent; Disease and Mechanism Converge

▪ **Somatotopic null:** Disease vs Surface r = -0.026; Disease vs Segmental r = 0.008; all four body-space tests non-significant (p > 0.19)
▪ **Disease-mechanism convergence:** r = 0.426, p = 0.032 — pairs close in disease tend to be close in mechanism (BL25–ST25: 0.079, 0.065) and pairs far in disease tend to be far in mechanism (BL25–GV4: 0.993, 0.726)
▪ Notable departures: GV4–LI4 (disease 0.102, mechanism 0.414) — similar diseases, different mechanisms; BL25–PC6 (disease 0.850, mechanism 0.177) — different diseases, similar mechanisms (mechanism compression)
▪ Partial Mantel: convergence survives control for surface (r = 0.426) and segmental (r = 0.388) — coupling is direct, not mediated by body location
▪ Bootstrap 95% CI: 0.167–0.577 (excludes zero)

**Purpose:** The two central RSA findings on one slide — null (independence) and positive (convergence).
_Figure: Fig 4 (all three panels)_

---

### Slide 14: Specialist–Generalist Continuum

**Title:** Within Each Site, Disease-Mechanism Coupling Varies

▪ Having established that disease and mechanism profiles correlate *across* sites, we ask: *within* each site, how tightly are they coupled?
▪ Panel A ranks sites by top-3 cell concentration: GV4 (62%) → BL25 (50%) → ST25 (38%) → LI4 (35%) → CV12 (29%) → PC6 (27%) → SP6 (21%) → ST36 (20%) — a specialist-generalist continuum
▪ GV4 (top3=62%): Nearly all bubbles confined to the Neurological row, but spanning multiple mechanism columns (Neuroprotective 28%, Autophagy 17%, Cell Survival 17%) — disease specialist, mechanism generalist
▪ CV12 (top3=29%): Three disease rows competing (Metabolic, Neurological, GI) with no single dominant pairing — intermediate coupling
▪ PC6 (top3=27%): Two disease rows nearly tied — Cardiovascular (10.8%) and Neurological (10.2%) both channeling through Inflammatory/Immune — spread across both dimensions
▪ ST36 (top3=20%): Many small bubbles across the grid; top cell is only 8% (Neurological × Inflammatory/Immune) — no dominant pairing
▪ At equal n=22, ranking is preserved (GV4 63%, ST36 32%) but the gap compresses by ~30% — the continuum is real but its magnitude is partly inflated by unequal sample sizes
▪ Tautology check confirms coupling is not a definitional artifact

**Purpose:** Within-site coupling adds a dimension beyond the between-site RSA.
_Figure: Fig 5 (Panel A bar chart + Panel B bubble plots)_

---

### Slide 15: Visualizing the Functional Landscape

**Title:** Low-Dimensional Embeddings Confirm the Structure

▪ CA biplots capture 68.7% (disease) and 63.5% (mechanism) of site-category association
▪ Disease space: GI cluster (BL25, ST25) separated from CV outlier (PC6) and broad cluster
▪ Mechanism space: Most sites collapse near origin — PC6 shifts from extreme isolation to central cluster
▪ Anatomical pair lines (dashed) cross cluster boundaries in both panels — body proximity ≠ functional proximity
▪ MDS and PCA (Fig S1, S2) confirm the same structure — GI pairing, PC6 space-shifting, mechanism compression, and anatomical pair crossing are method-independent

**Purpose:** Visual summary confirming all prior findings in one figure.
_Figure: Fig 6 (CA biplots — disease and mechanism space)_

---

### Slide 16: Robustness

**Title:** The Findings Are Robust

▪ Leave-one-out: Disease-mechanism r stable 0.31–0.60 across all 8 exclusions
▪ Bootstrap CI excludes zero (0.167–0.577)
▪ Coordinate perturbation: 0 of 1,000 iterations produce significant somatotopic-disease signal
▪ Subsample to n=22: Significance drops to 16% — honest power limitation, not artifact
▪ Subsample coupling: Specialist-generalist ranking preserved at equal n=22 (GV4 62.5% → ST36 31.9%), but spread compresses — quantitative gap partly inflated by sample size
▪ GV4 exclusion: removing the most extreme specialist preserves cluster structure in CA biplots — GI pairing, PC6 isolation, and anatomical pair crossing all survive (Fig S4)
▪ Publication collapse and "Other" inclusion: zero effect

**Purpose:** Preempt skepticism — the results are not fragile.
_Figure: Fig S5 (LOO bar chart) or Fig S3 (perturbation histogram)_

---

## Discussion (Slides 17–20)

### Slide 17: What We Found

**Title:** Summary of Key Findings

▪ Each stimulation site has a distinct functional identity in disease space, with sharp specialist signals
▪ Mechanism space is compressed — sites are more similar in how they work than in what they treat
▪ Functional organization may be independent of somatotopic organization (both surface and segmental)
▪ Disease and mechanism spaces are coupled (r = 0.426) — sites have internal functional coherence
▪ Sites vary along a specialist-generalist continuum in disease-mechanism coupling

**Purpose:** Recap for the audience before interpretation.
_No figure needed_

---

### Slide 18: Interpretation — What This Means

**Title:** Implications for Acupoint Specificity Research

▪ Sites have reproducibly distinct functional identities — acupoint specificity exists at the population level, not just in single-pair experiments
▪ The somatotopic null result: functional identity is NOT determined by peripheral anatomy or spinal segmental wiring — consistent with findings that local neural architecture (e.g., PROKR2 neuron distribution; Liu et al., 2021), rather than body-surface coordinates or spinal segment, determines which pathways a site engages
▪ Mechanism compression: most sites engage shared anti-inflammatory and neuroprotective pathways (Oh & Kim, 2022; Lin & Chen, 2008) — specificity resides in disease application, not mechanism selection
▪ The specialist-generalist continuum: sites differ not just in what they do but in how tightly disease and mechanism are coupled — specialist sites (GV4, PC6) are natural candidates for double-dissociation designs (Chae et al., 2026)
▪ Low-dimensional geometry: disease space is organized by indication poles (GI, Cardiovascular, Neurological), consistent with MDS analyses of five-phase and source acupoints in clinical trial databases (Lee et al., 2022; Choi et al., 2021) — our CA biplots extend this by showing that these indication poles collapse in mechanism space — sites that are well-separated by what they treat become nearly indistinguishable in how they work
▪ Implications for sham design: proximity-based sham selection assumes nearby sites are functionally neutral, but our data shows no relationship between physical proximity and profile similarity (Mantel r = −0.026). Even SP6–ST36, the most mechanism-similar pair (cosine distance 0.016), diverges significantly in disease (p = 1.6×10⁻²⁵) — suggesting that proximity-based sham sites may share biological pathways while differing in disease-specific research patterns, a distinction worth considering in trial design (cf. Langevin & Wayne, 2018)
▪ Our literature-level characterization complements neuroimaging-based decoding of acupoint specificity (Yoon et al., 2026)

**Purpose:** Connect findings to the broader field and prior references.
_No figure needed_

> **Framework link:** These results validate two framework predictions: (1) projective specificity — distinct ℘ₐᴱ profiles across sites, and (2) field-projective dissociability — dᶠ(BL25,GV4) is minimal but dᵖ(BL25,GV4) is maximal. Mechanism compression suggests specificity is concentrated in the disease facet of ℘ᴱ.

---

### Slide 19: Limitations

**Title:** Limitations and Future Directions

▪ Sample size imbalance: BL25 (n=22) vs ST36 (n=1,174) — subsample analysis shows power limitation
▪ Literature-based profiles reflect research trends, not necessarily ground-truth physiology
▪ Only 8 sites — expanding to more sites would test generalizability
▪ Rat model — translating somatotopic coordinates to humans requires additional validation
▪ Future: Apply double-dissociation experimental designs (Chae et al., 2026) to empirically test the functional profiles characterized here

**Purpose:** Honest limitations and natural next steps.
_No figure needed_

---

### Slide 20: Conclusion

**Title:** Take-Home Message

▪ Peripheral nerve stimulation sites have distinct, reproducible functional identities across disease and mechanism domains
▪ These identities are organized by disease-mechanism coherence, NOT by body location
▪ The functional landscape spans a specialist-generalist continuum — from GV4 (one disease, one mechanism) to ST36 (many diseases, many mechanisms)
▪ RSA provides a principled framework for systematic acupoint characterization that complements single-point mechanistic studies (Liu et al., 2021) and clinical data mining approaches (Lee et al., 2020)

**Purpose:** Final slide before Q&A — one clear message the audience takes away.
_Figure: Fig 6 (CA biplots) as a visual summary_

> **Framework link:** This is an empirical demonstration that field distance and projective distance are dissociable — body location does not predict functional identity. The framework's prediction holds across 8 sites, 14 disease categories, and 12 mechanism categories.

---

## References Cited in Presentation

1. Langevin, H. M., & Wayne, P. M. (2018). What is the point? The problem with acupuncture research that no one wants to talk about. _J Altern Complement Med_, 24(3), 200-207.
2. Xing, J. J., Zeng, B. Y., Li, J., Zhuang, Y., & Liang, F. R. (2013). Acupuncture point specificity. _Int Rev Neurobiol_, 111, 49-65.
3. Jung, W. M., Lee, T., Lee, I. S., et al. (2015). Spatial patterns of the indications of acupoints using data mining in classic medical text. _Evid Based Complement Alternat Med_, 2015, 457071.
4. Chae, Y., Ryu, Y., & Jung, W. M. (2019). An analysis of indications of meridians in DongUiBoGam using data mining. _Korean J Acupunct_, 36(4), 292-299.
5. Poldrack, R. A. (2006). Can cognitive processes be inferred from neuroimaging data? _Trends Cogn Sci_, 10(2), 59-63.
6. Lee, Y. S., Ryu, Y., Yoon, D. E., et al. (2020). Commonality and specificity of acupuncture point selections. _Evid Based Complement Alternat Med_, 2020, 2948292.
7. Lee, S., Ryu, Y., Park, H. J., et al. (2022). Characteristics of five-phase acupoints from data mining of RCTs followed by multidimensional scaling. _Integr Med Res_, 11(2), 100829.
8. Hwang, Y. C., Lee, I. S., Ryu, Y., et al. (2021). Exploring traditional acupuncture point selection patterns for pain control. _Acupunct Med_, 39(3), 184-191.
9. Jung, W. M., Lee, S. H., Lee, Y. S., & Chae, Y. (2017). Exploring spatial patterns of acupoint indications from clinical data. _Medicine_, 96(17), e6768.
10. Choi, D. H., Lee, S., Lee, I. S., et al. (2021). Characteristics of source acupoints: data mining of clinical trials database. _Korean J Acupunct_, 38(2), 100-109.
11. Yoon, D. E., Ryu, Y., & Chae, Y. (2026). Decoding acupoint specificity: From neural patterns to bodily maps. _Front Neurosci_, 20, 1815538.
12. Chae, Y., Yoon, D. E., Tu, C. H., & Lee, M. S. (2026). A new framework for acupoint specificity: Advancing acupuncture studies using the double-dissociation model. _Integr Med Res_, 101316.
13. Liu, S., Wang, Z., Su, Y., et al. (2021). A neuroanatomical basis for electroacupuncture to drive the vagal-adrenal axis. _Nature_, 598(7882), 641-645.
14. Oh, J. E., & Kim, S. N. (2022). Anti-inflammatory effects of acupuncture at ST36 point. _Front Immunol_, 13, 813748.
15. Lin, J. G., & Chen, W. L. (2008). Acupuncture analgesia: a review of its mechanisms of actions. _Am J Chin Med_, 36(4), 635-645.
16. Li, J., Li, J., Chen, Z., et al. (2012). The influence of PC6 on cardiovascular disorders: a review of central neural mechanisms. _Acupunct Med_, 30(1), 47-50.
