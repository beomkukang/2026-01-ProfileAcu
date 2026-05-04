# Analysis 01: Taxonomy Optimization — Disease and Mechanism Category Selection

## Objective
Determine the optimal number of disease and mechanism categories for classifying 1,974 acupoint literature records (8 stimulation sites) before building representational dissimilarity matrices (RDMs) for downstream RSA analysis. The goal is to find the granularity where further splitting stops meaningfully changing the RDM structure — providing a data-driven, defensible answer to "why k categories?" for the Methods section.

## Data
- **Source:** AcupointDG database (acupointdg-research.com, channels PubMed), 8 xlsx files in `base_data/`
- **Sites:** BL25 (22), GV4 (33), ST25 (89), CV12 (68), PC6 (181), LI4 (115), SP6 (292), ST36 (1,174)
- **Total records:** 1,974 (1,565 unique PMIDs — shared PMIDs are separate acupoint-level records from multi-site studies)
- **Unknown mechanisms:** 101 records

### Data cleaning (s00)
Before classification, base data was cleaned:
- **Whitespace:** Stripped trailing/leading spaces from Disease and Mechanism strings
- **Typos:** 19 explicit Disease corrections (e.g., "obestiy"→"Obesity", "Braciahl"→"Brachial", "neurophatic"→"Neuropathic")
- **Special characters:** Normalized smart quotes, backticks, en-dashes (e.g., Parkinson's → Parkinson's)
- **Trailing periods:** Stripped from 83 Mechanism strings
- **Case normalization:** Unified 113 Disease and additional Mechanism case-only duplicates to most frequent variant
- All corrections logged in `results/datatables/data_corrections.csv`

## Method

### Classification approach
Deterministic keyword-based taxonomy with progressive inheritance:
- Each disease/mechanism string is classified by (1) keyword match against curated lists, (2) fallback to "Other"
- Each taxonomy level inherits all assignments from the previous level — only records classified as "Other" or records in a category being split get reclassified
- Comorbidity strings classified based on the condition before the separator ("with", "and", "accompanied by")
- All matching is case-insensitive
- Keyword lists were iteratively expanded across 4 versions by inspecting unclassified "Other" records at each round

### Disease taxonomy (7 levels)
| Level | k  | Categories added                          |
|-------|----|-------------------------------------------|
| 1     | 5  | Pain, Neurological, Cardiovascular, Gastrointestinal, Other |
| 2     | 7  | + Metabolic/Endocrine, + Psychiatric (split from Neurological) |
| 3     | 9  | + Reproductive, + Musculoskeletal          |
| 4     | 11 | + Respiratory, + Immune/Inflammatory       |
| 5     | 13 | + Renal/Urological, + Dermatological       |
| 6     | 14 | + Addiction (split from Psychiatric)        |
| 7     | 15 | + Cancer/Oncology                          |

### Mechanism taxonomy (8 levels)
| Level | k  | Categories added                          |
|-------|----|-------------------------------------------|
| 1     | 4  | Inflammatory/Immune, Neuroprotective, Analgesic/Opioid, Other |
| 2     | 6  | + Autonomic/Neuroendocrine, + Oxidative Stress |
| 3     | 8  | + Gut-Brain/Enteric, + Neurochemical Signaling |
| 4     | 9  | + Cell Survival/Apoptosis                  |
| 5     | 10 | + Ion Channel/Pain Transduction (split from Analgesic) |
| 6     | 11 | + Autophagy/Mitophagy (split from Cell Survival) |
| 7     | 12 | + Metabolic Pathway Regulation             |
| 8     | 13 | + Neural Circuit/Connectivity              |

### RDM computation
- For each taxonomy level: build proportional profile vectors for 8 sites (excluding "Other" and "Unknown"), compute cosine distance → 8×8 RDM

### Stability analysis
- **Within-domain:** Mantel correlation (Spearman, 10,000 permutations) between RDM at level k and RDM at level k+1
- **Cross-domain:** Mantel correlation between disease RDM and mechanism RDM at each level combination (7×8 = 56 tests)

## Results

### Disease RDM stability
| Transition | Mantel r | p        |
|------------|----------|----------|
| k=5 → 7   | 0.938    | < 0.001  |
| k=7 → 9   | 0.998    | < 0.001  |
| k=9 → 11  | 1.000    | < 0.001  |
| k=11 → 13 | 1.000    | < 0.001  |
| k=13 → 14 | 0.999    | < 0.001  |
| k=14 → 15 | 1.000    | < 0.001  |

**Interpretation:** The disease RDM stabilized quickly. The k=5→7 split (adding Metabolic/Endocrine and Psychiatric) produced a meaningful change (r=0.938). From k=9 onward, the RDM is essentially identical (r≈1.00). The representational structure is dominated by the 4 core categories (Pain, Neurological, Cardiovascular, Gastrointestinal), with Metabolic/Endocrine and Psychiatric adding modest signal.

### Mechanism RDM stability
| Transition | Mantel r | p        |
|------------|----------|----------|
| k=4 → 6   | 0.834    | 0.003    |
| k=6 → 8   | 0.878    | < 0.001  |
| k=8 → 9   | 0.993    | < 0.001  |
| k=9 → 10  | 0.997    | < 0.001  |
| k=10 → 11 | 0.999    | < 0.001  |
| k=11 → 12 | 0.969    | < 0.001  |
| k=12 → 13 | 0.998    | < 0.001  |

**Interpretation:** Mechanism taxonomy showed more sensitivity to splitting. The k=6→8 transition (adding Gut-Brain/Enteric and Neurochemical Signaling) produced the largest RDM change (r=0.878). The k=11→12 transition (adding Metabolic Pathway) showed a notable dip (r=0.969), indicating this category captures real structure. From k=9 onward, all transitions exceed r=0.96. The elbow is at k=9.

### Cross-domain convergence
- Peak convergence: **r=0.484 at disease k=7 × mechanism k=11** (p=0.014)
- Sweet spot band: disease k=7+ × mechanism k=8–11, r=0.46–0.48, all significant (p<0.02)
- Disease and mechanism RDMs show a moderate positive correlation — sites that treat similar diseases engage partially overlapping mechanisms, but the correlation is far from perfect, consistent with the "mechanism compression" hypothesis

### "Other" category coverage (after data cleaning + keyword expansion)
| k    | Disease Other % | Mechanism Other % |
|------|----------------|-------------------|
| 5/4  | 34.5%          | 51.2%             |
| 7/6  | 19.8%          | 35.0%             |
| 9/8  | 11.3%          | 22.5%             |
| 9    | 11.3%          | 13.8%             |
| 11   | 5.3%           | 9.3%              |
| 13   | 3.7%           | 1.6%              |
| 14   | 1.0%           | —                 |
| 15   | 0.6%           | —                 |

### Sparsity
- Disease: 12.5% (k=7) to 34.8% (k=15) — all well below 50% ceiling
- Mechanism: 7.8% (k=9) to 13.5% (k=13) — consistently low

## Decision

**Selected taxonomy — maximize coverage (minimize "Other"):**
- **Disease: k=15** (Level 7, all 14 categories) — Pain, Neurological, Cardiovascular, Gastrointestinal, Metabolic/Endocrine, Psychiatric, Reproductive, Musculoskeletal, Respiratory, Immune/Inflammatory, Renal/Urological, Dermatological, Addiction, Cancer/Oncology. **0.6% Other** (12 records).
- **Mechanism: k=13** (Level 8, all 12 categories) — Inflammatory/Immune, Neuroprotective, Analgesic/Opioid, Autonomic/Neuroendocrine, Oxidative Stress, Gut-Brain/Enteric, Neurochemical Signaling, Cell Survival/Apoptosis, Ion Channel/Pain Transduction, Autophagy/Mitophagy, Metabolic Pathway, Neural Circuit/Connectivity. **1.6% Other** (31 records).

**Rationale:**
- The RDM stability analysis shows that the representational geometry is identical from k=9 onward for both domains (r>0.96 for all transitions). Using the finest granularity (k=15 disease, k=13 mechanism) therefore does **not change the RDM structure** compared to k=9, but it maximizes record retention — only 0.6% disease and 1.6% mechanism records are excluded as "Other."
- More categories give richer profiles for downstream Bayes Factor heatmaps (Fig 2), disease-mechanism contingency tables (Fig 5), and CA biplots (Fig 6), while the RDM-based analyses (Fig 3, Fig 4) produce identical results regardless of the k chosen above the elbow.
- Sparsity at k=15/k=13 remains manageable: 34.8% disease, 13.5% mechanism — both well under the 50% ceiling.
- The 101 "Unknown" mechanism records are excluded from mechanism profiles but retained for disease profiles.

## Outputs
- `results/datatables/combined_data.csv` — 1,974 records with Site column
- `results/datatables/data_corrections.csv` — log of all base data cleaning corrections
- `results/datatables/disease_dictionary.csv` — all unique disease strings × 7 taxonomy levels
- `results/datatables/mechanism_dictionary.csv` — all unique mechanism strings × 8 taxonomy levels
- `results/datatables/disease_rdm_stability.csv` — Mantel r between consecutive disease levels
- `results/datatables/mechanism_rdm_stability.csv` — Mantel r between consecutive mechanism levels
- `results/datatables/cross_domain_mantel.csv` — 56 disease×mechanism Mantel correlations
- `results/datatables/classification_report.csv` — category counts, sparsity, %Other per level
- `results/figures/rdm_stability_curve.png` — stability elbow plot
- `results/figures/cross_domain_heatmap.png` — disease×mechanism convergence heatmap
- `results/figures/sparsity_curve.png` — sparsity vs. k
- `results/figures/other_category_curve.png` — %Other vs. k
- `results/figures/profile_comparison.png` — profile heatmaps at recommended levels

## Scripts
All scripts in `scripts/`. Run from project root: `uv run a01/scripts/run_all.py`

| Script | Description |
|--------|-------------|
| `s00_clean_base_data.py` | Clean base data (typos, case, whitespace, special characters) |
| `s01_load_combine.py` | Load and combine 8 xlsx files |
| `s02_disease_taxonomy.py` | Build 7-level disease taxonomy (k=5→15) |
| `s03_mechanism_taxonomy.py` | Build 8-level mechanism taxonomy (k=4→13) |
| `s04_compute_rdms.py` | Compute RDMs at all taxonomy levels |
| `s05_stability_analysis.py` | Mantel tests (within-domain + cross-domain) |
| `s06_visualize.py` | Generate all figures |
| `run_all.py` | Orchestrator — runs s00 through s06 sequentially |
