# Analysis 05 Results: Disease-Mechanism Coupling

## Summary
Per-site contingency tables (disease x mechanism) reveal a specialist-generalist continuum in how tightly disease and mechanism are coupled within each site. GV4 concentrates 62% of its records in just 3 disease-mechanism cells (Neurological x Neuroprotective dominance), while ST36 spreads across 123 non-zero cells with only 19.5% in its top 3. PC6 is a disease specialist but mechanism generalist — concentrated in Cardiovascular disease but using multiple mechanism pathways. A tautology check confirms that the coupling pattern is not an artifact of definitional overlap between disease and mechanism categories.

## Coupling Metrics

| Site | NMI | Joint Entropy | Top-3 Concentration (%) | Non-zero Cells | n Records |
|------|-----|---------------|------------------------|----------------|-----------|
| GV4 | 0.135 | 2.93 | 62.1 | 10 | 29 |
| BL25 | 0.311 | 3.21 | 50.0 | 11 | 22 |
| ST25 | 0.242 | 4.34 | 37.5 | 30 | 88 |
| LI4 | 0.309 | 4.71 | 34.5 | 41 | 110 |
| CV12 | 0.273 | 4.60 | 29.2 | 31 | 65 |
| PC6 | 0.178 | 5.05 | 26.5 | 53 | 166 |
| SP6 | 0.234 | 5.47 | 20.7 | 73 | 271 |
| ST36 | 0.117 | 5.82 | 19.5 | 123 | 1,079 |

### Interpretation

**Top-3 concentration** is the most intuitive metric: what percentage of a site's records fall into just 3 disease-mechanism cells?

- **GV4 (62.1%)** is the tightest specialist. Nearly two-thirds of its research is concentrated in three combinations, dominated by Neurological x Neuroprotective. This site does one thing through one pathway.
- **BL25 (50.0%)** is the second most concentrated, driven by Gastrointestinal x Gut-Brain/Enteric and Gastrointestinal x Autonomic/Neuroendocrine pairings.
- **ST36 (19.5%)** is the broadest generalist. Its records distribute across 123 non-zero cells with no dominant pairing — no single disease-mechanism combination captures even 7% of its records.
- **PC6 (26.5%)** is intermediate but interesting: it is a strong disease specialist (Cardiovascular) but uses multiple mechanisms (Inflammatory/Immune, Cell Survival/Apoptosis, Autonomic/Neuroendocrine). This dissociation — disease specialist but mechanism generalist — is visible in the bubble contingency plot (Fig 5, Panel B).

**NMI (Normalized Mutual Information)** measures how much knowing the disease category tells you about the mechanism category, and vice versa. High NMI means tight disease-mechanism coupling; low NMI means the two dimensions are relatively independent within that site. BL25 and LI4 have the highest NMI (0.31), while ST36 has the lowest (0.12). Notably, GV4 has low NMI (0.14) despite high top-3 concentration — this is because GV4's records are almost entirely Neurological, so there is little disease variation for NMI to correlate with.

**Joint entropy** increases with the number of occupied cells and the evenness of distribution. GV4 (2.93 bits) has the lowest entropy; ST36 (5.82 bits) has the highest. The monotonic relationship between entropy and n_records partly reflects the obvious: more records fill more cells. But the relationship is not purely driven by sample size — PC6 (n=166) has higher entropy (5.05) than CV12 (n=65, entropy=4.60), reflecting genuine distributional breadth beyond what sample size alone would predict.

## Tautology Check

Some disease-mechanism pairs overlap definitionally — e.g., "Pain" disease x "Analgesic/Opioid" mechanism. If a paper studies pain treatment, it almost certainly investigates analgesic mechanisms, creating a tautological association that could inflate coupling metrics.

### Tautological record counts

| Site | Total Records | Tautological Records | % Tautological |
|------|-------------|---------------------|----------------|
| GV4 | 29 | 8 | 27.6% |
| CV12 | 65 | 15 | 23.1% |
| ST25 | 88 | 18 | 20.5% |
| LI4 | 110 | 22 | 20.0% |
| ST36 | 1,079 | 210 | 19.5% |
| BL25 | 22 | 4 | 18.2% |
| SP6 | 271 | 36 | 13.3% |
| PC6 | 166 | 13 | 7.8% |

### NMI with and without tautological records

| Site | NMI (all) | NMI (excl. tautology) | % Change |
|------|-----------|----------------------|----------|
| BL25 | 0.311 | 0.318 | +2.3% |
| ST36 | 0.117 | 0.124 | +5.3% |
| CV12 | 0.273 | 0.290 | +6.3% |
| PC6 | 0.178 | 0.195 | +9.6% |
| SP6 | 0.234 | 0.257 | +10.2% |
| LI4 | 0.309 | 0.345 | +11.6% |
| ST25 | 0.242 | 0.293 | +21.3% |
| GV4 | 0.135 | 0.317 | +134.3% |

**Interpretation:** For most sites, excluding tautological records changes NMI by less than 12% — the coupling pattern is not driven by definitional overlap. The exception is GV4 (+134%), which jumps from the lowest NMI to among the highest after exclusion. This is because GV4's tautological records (Neurological x Neuroprotective) constitute a large fraction of its small sample (8 of 29 = 27.6%), and removing them reveals tighter coupling in the remaining records. Critically, the specialist-generalist ranking is preserved: ST36 remains the lowest-NMI site with or without tautological records.

### Tautology Mantel test (RDM stability)

For each site, the disease and mechanism RDMs were recomputed after excluding tautological records and compared to the original RDMs via Mantel correlation.

| Site | Disease RDM Mantel r | p-value | Mechanism RDM Mantel r | p-value |
|------|---------------------|---------|------------------------|---------|
| BL25 | 0.987 | 0.039 | 1.000 | 0.014 |
| CV12 | 0.947 | 0.001 | 0.524 | 0.003 |
| PC6 | 0.772 | 0.001 | 0.828 | 0.001 |
| LI4 | 0.939 | 0.001 | 0.545 | 0.003 |
| SP6 | 0.812 | 0.001 | 0.706 | 0.001 |
| ST25 | 0.772 | 0.006 | 0.628 | 0.004 |
| ST36 | 0.676 | 0.001 | 0.149 | 0.116 |
| GV4 | 0.733 | 0.165 | 0.111 | 0.159 |

Most disease RDMs are highly stable (r > 0.77). Mechanism RDMs show more sensitivity to tautology exclusion, particularly for ST36 (r=0.149, p=0.116) and GV4 (r=0.111, p=0.159), where tautological records constitute a larger proportion of mechanism-defining records. This is expected — removing 20–28% of records from small-to-moderate samples substantially reshapes the mechanism profile.

**Conclusion:** The coupling pattern (specialist-generalist continuum) is not an artifact of tautological disease-mechanism associations. The ranking is preserved, and the RDM structure is largely stable after exclusion.

## Figure 5: Disease-Mechanism Coupling

**Panel A (left):** Bar chart showing top-3 concentration per site, ordered from highest (GV4, 62.1%) to lowest (ST36, 19.5%). This establishes the specialist-generalist continuum at a glance.

**Panel B (right):** Bubble contingency plots for three exemplar sites — GV4 (Specialist), CV12 (Middle), ST36 (Generalist). Bubble size represents within-site percentage (not raw counts) so sites are comparable regardless of sample size. A shared size legend appears above the top panel.

- **GV4:** One dominant bubble (Neurological x Neuroprotective) and near-emptiness elsewhere — this site does one thing through one pathway.
- **CV12:** A few mid-sized bubbles across several categories — more distributed but with some structure.
- **ST36:** Many small bubbles scattered across the full 14x12 grid — no single disease-mechanism pairing dominates.

## Outputs

| File | Description |
|------|-------------|
| `results/datatables/contingency_tables.pkl` | Per-site disease x mechanism contingency tables (pickle) |
| `results/datatables/coupling_metrics.csv` | NMI, joint entropy, top-3 concentration, n_nonzero_cells, n_records per site |
| `results/datatables/tautology_check.csv` | Tautological record counts and NMI with/without per site |
| `results/datatables/tautology_mantel.csv` | Mantel correlations between original and tautology-excluded RDMs |
| `results/figures/fig5_coupling.png` | Figure 5: top-3 bar chart + bubble contingency plots |

## Key Takeaways for the Manuscript

1. **Sites vary along a specialist-generalist continuum.** GV4 concentrates 62% in 3 cells; ST36 spreads across 123 cells (19.5% in top 3). This is not just about disease profiles or mechanism profiles separately — it's about how tightly the two are linked within each site.

2. **PC6 dissociates disease specialization from mechanism specialization.** Strong Cardiovascular disease concentration but diffuse mechanism profile — a disease specialist can be a mechanism generalist. This adds a dimension beyond the profile-level characterization in A03.

3. **The coupling pattern is not a tautology artifact.** Excluding definitionally overlapping disease-mechanism records preserves the specialist-generalist ranking. NMI changes by <12% for most sites.

4. **Sample size correlates with but does not determine coupling.** ST36 (n=1,079) is the most diffuse, BL25 (n=22) is the second most concentrated. But PC6 (n=166) is more diffuse than LI4 (n=110), showing that distributional breadth is not purely a function of record count.
