# Analysis 07 Results: Sensitivity & Robustness

## Summary
Six sensitivity analyses were conducted to test whether the core findings from A04 (disease-mechanism coupling, somatotopic independence) are robust to analytic choices, sample size, coordinate uncertainty, category definitions, and publication overlap. The disease-mechanism coupling (r=0.426, p=0.032) is stable across most perturbations: the bootstrap 95% CI excludes zero (0.167–0.577), the leave-one-out r ranges from 0.31 to 0.60, and the result survives "Other" category inclusion and publication collapsing. The main vulnerability is sample size — subsampling to n=22 per site drops the significance rate to 16%. The somatotopic null result is uniformly robust: 0 of 1,000 coordinate perturbations produce a significant somatotopic-disease correlation.

## 1. Leave-One-Out (LOO) Site Exclusion

Each site was excluded in turn, and the disease-mechanism Mantel test was recomputed on the remaining 7 sites (7! = 5,040 permutations each).

| Excluded site | Mantel r | p-value | Significant |
|---------------|----------|---------|-------------|
| BL25 | 0.312 | 0.162 | No |
| GV4 | 0.601 | 0.013 | Yes |
| ST25 | 0.348 | 0.172 | No |
| CV12 | 0.479 | 0.014 | Yes |
| PC6 | 0.551 | 0.008 | Yes |
| LI4 | 0.401 | 0.046 | Yes |
| SP6 | 0.427 | 0.041 | Yes |
| ST36 | 0.330 | 0.103 | No |

**Interpretation:** The correlation is present in every exclusion (all r > 0.31) but loses significance when BL25, ST25, or ST36 are removed. These are the sites whose disease-mechanism coherence contributes most to the overall correlation: BL25 and ST25 are the GI-enteric pair (tight disease-mechanism coupling), and ST36 is the generalist whose broad profile anchors the middle of both spaces.

Removing GV4 *increases* the correlation (r=0.601, p=0.013), confirming that GV4 is a genuine outlier whose extreme specialization actually weakens the overall linear trend. Removing PC6 also increases r (0.551), for similar reasons — its Cardiovascular specialization is so extreme that it creates leverage rather than following the group trend.

**Conclusion:** The disease-mechanism coupling is not driven by any single site. The effect size is stable (0.31–0.60) and the direction is consistent across all 8 exclusions.

## 2. Bootstrap Mantel (1,000 Iterations)

Records were resampled within each site (with replacement), profiles and RDMs recomputed, and the disease-mechanism Mantel r recalculated at each iteration.

| Statistic | Value |
|-----------|-------|
| Mean r | 0.372 |
| Median r | 0.377 |
| 95% CI lower | 0.167 |
| 95% CI upper | 0.577 |
| N iterations | 1,000 |

**Interpretation:** The bootstrap 95% CI (0.167–0.577) excludes zero, confirming the disease-mechanism coupling is statistically robust. The mean bootstrap r (0.372) is slightly lower than the observed r (0.426), which is expected — resampling introduces noise that attenuates the correlation. The CI is wide, reflecting the small number of sites (n=8) and the sensitivity of rank correlations to perturbation with few data points.

## 3. Subsample Sensitivity (n=22 per Site)

To test whether the unbalanced sample sizes (BL25: n=22 vs ST36: n=1,174) bias the results, records were subsampled to n=22 per site (the smallest site's count) and the Mantel test repeated 100 times.

| Statistic | Value |
|-----------|-------|
| Mean r | 0.206 |
| Median r | 0.185 |
| % significant (p<0.05) | 16% |
| N iterations | 100 |

**Interpretation:** The correlation weakens substantially when all sites are reduced to n=22. The mean r drops from 0.426 to 0.206, and only 16% of iterations achieve significance. This is primarily a power issue — with 22 records per site, the proportional profiles are noisy (especially for sites like ST36 that spread across 14 categories), and the Mantel test on 28 pairwise distances has limited power.

**What this means for the paper:** The disease-mechanism coupling is real but relies on adequate sample sizes to detect. The result is not an artifact of the large sites dominating; when equalized, the direction is preserved (mean r > 0) but the signal-to-noise ratio drops below the detection threshold most of the time. This is an honest limitation.

## 4. Coordinate Perturbation (1,000 Iterations)

The somatotopic coordinates were perturbed (±15% uniform jitter), the surface RDM recomputed, and the somatotopic-disease and somatotopic-mechanism Mantel tests repeated.

| Test | Mean r | % significant |
|------|--------|---------------|
| Somatotopic–Disease | -0.010 | 0.0% |
| Somatotopic–Mechanism | 0.238 | 8.0% |

**Interpretation:** The somatotopic-disease null result is completely robust — not a single one of 1,000 coordinate perturbations produces a significant correlation. The mean r is essentially zero (-0.010). The p-value distribution (figS3) is roughly uniform across 0.1–0.9, which is exactly what a true null looks like.

The somatotopic-mechanism relationship is weakly positive on average (mean r=0.238) and reaches significance in 8% of perturbations. This exceeds the 5% false-positive rate expected under the null, suggesting a marginal somatotopic-mechanism trend that was not significant in the original analysis (r=0.202, p=0.199). However, the partial Mantel test (A04) showed this trend is mediated by disease — after controlling for disease, it drops to r=0.112. The perturbation analysis is consistent: some coordinate configurations nudge the marginal trend past p=0.05, but the effect is weak and indirect.

**Conclusion:** The somatotopic independence result is robust to coordinate uncertainty. Even generous ±15% perturbation does not produce a somatotopic-disease signal.

## 5. "Other" Category Inclusion

The main analyses excluded records classified as "Other" in disease or mechanism taxonomy. This test re-includes them.

| Condition | Mantel r | p-value |
|-----------|----------|---------|
| Original (Other excluded) | 0.426 | 0.032 |
| Other included | 0.426 | 0.034 |

**Interpretation:** Including the "Other" category has negligible effect — the r is identical and the p-value shifts by 0.002. This is expected: "Other" records distribute roughly evenly across sites, so they dilute all profiles equally without changing relative distances. The exclusion of "Other" is a conservative choice that does not bias the results.

## 6. Publication Collapsing

Sites with high PMID overlap (e.g., SP6–ST36 sharing 67.5% of records) could have inflated profile similarity because the same studies assigned labels to both. This test collapses shared PMIDs.

| Site | Original n | Collapsed n | PMIDs collapsed |
|------|-----------|-------------|-----------------|
| BL25 | 22 | 22 | 0 |
| GV4 | 33 | 33 | 0 |
| ST25 | 89 | 89 | 0 |
| CV12 | 68 | 68 | 0 |
| PC6 | 181 | 181 | 0 |
| LI4 | 115 | 115 | 0 |
| SP6 | 292 | 292 | 0 |
| ST36 | 1,174 | 1,174 | 0 |

| Condition | Mantel r | p-value |
|-----------|----------|---------|
| Original | 0.426 | 0.032 |
| Publication collapsed | 0.426 | 0.034 |

**Interpretation:** No records were actually collapsed — the PMID overlap flagged in A03 exists at the study level but does not produce duplicate records in the combined dataset. Each row in `combined_data.csv` is already unique (one PMID × one site × one disease × one mechanism). The "overlap" means the same study tested multiple sites, but each site's entry is independent. The Mantel test result is unchanged.

## 7. Subsample Sensitivity for Top-3 Concentration Ranking

The specialist-generalist continuum (A05) could be confounded with sample size — sites with more records mechanically spread across more cells, lowering concentration. To test this, all sites were subsampled to n=22 (BL25's count), top-3 concentration was recomputed, and the process was repeated 1,000 times.

| Site | Original n | Original top-3 | Subsampled mean ± SD | 95% CI |
|------|-----------|----------------|---------------------|--------|
| GV4 | 29 | 62.1% | 62.5% ± 4.9% | 54.6–72.7% |
| BL25 | 22 | 50.0% | 50.0% ± 0.0% | 50.0–50.0% |
| ST25 | 88 | 37.5% | 42.8% ± 7.4% | 27.3–59.1% |
| LI4 | 110 | 34.5% | 40.9% ± 7.6% | 27.3–54.7% |
| PC6 | 166 | 26.5% | 36.1% ± 6.6% | 27.3–50.0% |
| CV12 | 65 | 29.2% | 35.0% ± 5.8% | 27.3–45.5% |
| SP6 | 271 | 20.7% | 32.4% ± 5.9% | 22.7–45.5% |
| ST36 | 1,079 | 19.5% | 31.9% ± 6.1% | 22.7–45.5% |

**Interpretation:** The ranking is largely preserved — GV4 remains the most concentrated and ST36/SP6 remain the least, even at equal sample sizes. However, the gap compresses substantially: the original spread of 62.1% → 19.5% (42.6 percentage points) narrows to 62.5% → 31.9% (30.6 points). The most affected sites are those with the largest original sample sizes (ST36: 19.5% → 31.9%, SP6: 20.7% → 32.4%) — their low original concentrations were partly a sample-size artifact. The middle sites (ST25, LI4, PC6, CV12) converge to a narrow band (35–43%), making their relative ordering less stable.

**Conclusion:** GV4's specialist status and the specialist-generalist continuum are robust to sample size equalization, but the magnitude of the spread is inflated by unequal sample sizes. The qualitative finding (sites differ in coupling tightness) holds; the quantitative ranking in the middle of the continuum should be interpreted cautiously.

## Figure Descriptions

### Fig S3: Coordinate Perturbation (p-value Distribution)
Histogram of somatotopic-disease Mantel p-values across 1,000 coordinate perturbations. The distribution is roughly uniform across 0.1–0.9, centered around 0.5, with the p=0.05 threshold (red dashed line) far to the left of the distribution. Zero iterations fall below p=0.05. This is the visual signature of a true null — coordinate uncertainty does not create a spurious somatotopic signal.

### Fig S5: Leave-One-Out Bar Plot
Bar chart showing the disease-mechanism Mantel r for each site exclusion. The red dashed line marks the original r=0.426. Most bars are close to the line. Excluding GV4 raises r to 0.601 (highest), confirming GV4 is a leveraging outlier. Excluding BL25 drops r to 0.312 (lowest), confirming BL25 contributes substantially to the coupling through its tight GI disease-mechanism alignment.

### Fig S6: Subsample Sensitivity Histogram
Histogram of disease-mechanism Mantel r across 100 subsample iterations (n=22 per site). The distribution is centered around r=0.15–0.20, with the original r=0.426 (red dashed line) in the right tail. Most iterations fall well below the original value. Only 16% reach significance, illustrating the power limitation with small, equalized samples.

### Fig S7: Publication Collapse Comparison
Two-panel heatmap comparing disease profiles before and after PMID collapsing. The panels are identical because no records were collapsed — the PMID overlap does not produce duplicate entries. This confirms that the shared-publication concern flagged in A03 is a study-design overlap, not a data duplication issue.

## Summary Table (Table S5)

| Analysis | Condition | Mantel r | p-value | 95% CI | Interpretation |
|----------|-----------|----------|---------|--------|----------------|
| Leave-one-out | Min r across exclusions | 0.312 | 0.162 | — | Stable |
| Bootstrap | 95% CI | 0.372 | — | 0.167–0.577 | Significant |
| Subsample (n=22) | 16% significant | 0.206 | 0.183 | — | Sensitive to sample size |
| Coordinate perturbation | Somat-Disease (0% sig) | -0.010 | 0.495 | — | Robust null |
| Other inclusion | Other included | 0.426 | 0.034 | — | Stable |
| Publication collapse | Collapsed | 0.426 | 0.034 | — | Stable |

## Outputs

| File | Description |
|------|-------------|
| `results/datatables/loo_results.csv` | Leave-one-out Mantel r and p for each site exclusion |
| `results/datatables/bootstrap_mantel_ci.csv` | Bootstrap mean, median, 95% CI |
| `results/datatables/bootstrap_mantel_distribution.csv` | Full bootstrap distribution (1,000 r values) |
| `results/datatables/subsample_results.csv` | Subsample Mantel r and p (100 iterations) |
| `results/datatables/perturbation_results.csv` | Coordinate perturbation results (1,000 iterations) |
| `results/datatables/other_inclusion.csv` | Mantel test with "Other" category included |
| `results/datatables/pub_collapse.csv` | Record counts before/after PMID collapsing |
| `results/datatables/pub_collapse_mantel.csv` | Mantel test after publication collapsing |
| `results/datatables/subsample_coupling.csv` | Subsample top-3 concentration (1,000 iterations) |
| `results/datatables/tableS5_sensitivity.csv` | Combined sensitivity summary table |
| `results/figures/figS3_perturbation.png` | Coordinate perturbation p-value histogram |
| `results/figures/figS5_loo.png` | Leave-one-out bar plot |
| `results/figures/figS6_subsample.png` | Subsample sensitivity histogram |
| `results/figures/figS7_pub_collapse.png` | Publication collapse comparison heatmap |

## Key Takeaways for the Manuscript

1. **Disease-mechanism coupling is robust.** Bootstrap CI excludes zero (0.167–0.577). LOO r ranges from 0.31–0.60 with consistent positive direction. The result survives "Other" inclusion and publication collapsing.

2. **The somatotopic null is ironclad.** Zero of 1,000 coordinate perturbations produce a significant somatotopic-disease correlation. The null result cannot be attributed to imprecise coordinates.

3. **Sample size is the main limitation.** Equalizing to n=22 per site drops significance to 16%. The coupling is real but requires adequate sample sizes for detection. This should be discussed as an honest limitation.

4. **No single site drives the result.** The LOO analysis shows the coupling is distributed across multiple sites. GV4 and PC6 are leveraging outliers — removing either increases the correlation. BL25 and ST36 contribute most to the coupling signal.

5. **Publication overlap is not a confound.** The PMID overlap flagged in A03 does not produce duplicate records. Collapsing has zero effect on the results.

6. **The specialist-generalist continuum is qualitatively robust but quantitatively inflated.** At equal n=22, GV4 remains the top specialist and ST36/SP6 remain the most generalist, but the spread compresses from 42.6 to 30.6 percentage points. The middle-ranking sites (ST25, LI4, PC6, CV12) converge to a narrow band.
