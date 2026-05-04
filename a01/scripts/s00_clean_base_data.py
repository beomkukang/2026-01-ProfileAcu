"""
Step 0: Clean base data — fix typos, misspellings, special characters,
trailing punctuation, and case inconsistencies in Disease and Mechanism
strings. Writes corrected xlsx files back to base_data/.

Corrections are logged to results/datatables/data_corrections.csv.
"""
import pandas as pd
import os
import re
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'base_data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']

# ──────────────────────────────────────────────
# 1. DISEASE: Explicit typo / misspelling fixes
# ──────────────────────────────────────────────
DISEASE_TYPO_CORRECTIONS = {
    # Pure misspellings
    'obestiy': 'Obesity',
    'Diarhhoea': 'Diarrhoea',
    'Diatbet': 'Diabetes',
    'Diabet': 'Diabetes',
    'arhritis': 'Arthritis',
    'arthritic': 'Arthritis',
    'hypertense': 'Hypertension',
    'Braciahl plexus injury': 'Brachial plexus injury',
    'osteopenic': 'Osteopenia',
    'Neurology': 'Neurological disorder',
    'neurophatic pain': 'Neuropathic pain',
    'Infammatory Pain': 'Inflammatory Pain',
    'Infammatory pain': 'Inflammatory pain',
    'Traumatic brain injuny': 'Traumatic brain injury',
    'ischemia stroke': 'Ischemic stroke',
    'ischaemic stroke': 'Ischemic stroke',
    'schemic Stroke': 'Ischemic stroke',
    'Gastrointestinal mobility disorder': 'Gastrointestinal motility disorder',
    'Pakinson\'s disease': 'Parkinson\'s disease',

    # Trailing period
    'Myocardial injury.': 'Myocardial injury',
    'oligozoospermia of insufficiency of Shen (Kidney) essence syndrome (OIKES).': \
        'Oligozoospermia of insufficiency of Shen (Kidney) essence syndrome (OIKES)',

    # Special characters: smart quotes, backtick, en-dash
    'Parkinson\u2019s disease': 'Parkinson\'s disease',   # right single quote
    'Parkinson`s disease': 'Parkinson\'s disease',         # backtick
    'Alzheimer\u2019s disease': 'Alzheimer\'s disease',
    'cerebral ischemia\u2013reperfusion injury (CIRI)': 'Cerebral ischemia-reperfusion injury (CIRI)',

    # Semantic: Hypotension is a real condition, NOT a typo of Hypertension.
    # Keep it as-is. Removed from corrections.

    # "Burn injury" is NOT the same as "Brain injury" — false fuzzy match.
    # Keep it as-is.
}

# ──────────────────────────────────────────────
# 2. MECHANISM: Trailing periods — strip them
# ──────────────────────────────────────────────
# 83 mechanism strings end with '.'; we strip trailing periods universally.


def normalize_case_for_column(values):
    """
    For strings that differ only by case/trailing whitespace,
    pick the most frequent variant as canonical.
    Returns a mapping: original -> canonical.
    """
    groups = {}
    counts = Counter(values)
    for v in values:
        key = v.lower().strip()
        if key not in groups:
            groups[key] = set()
        groups[key].add(v)

    corrections = {}
    for key, variants in groups.items():
        if len(variants) <= 1:
            continue
        # Pick the most frequent variant
        canonical = max(variants, key=lambda v: counts[v])
        for v in variants:
            if v != canonical:
                corrections[v] = canonical

    return corrections


def main():
    # Load all data
    all_dfs = {}
    for site in SITES:
        fpath = os.path.join(DATA_DIR, f'{site}.xlsx')
        all_dfs[site] = pd.read_excel(fpath)

    total_records = sum(len(df) for df in all_dfs.values())
    print(f"Total records: {total_records}")

    correction_log = []
    stats = {'whitespace': 0, 'disease_typo': 0, 'disease_case': 0,
             'mech_period': 0, 'mech_case': 0}

    # ── Step 1: Strip whitespace from Disease and Mechanism ──
    for site, df in all_dfs.items():
        for col in ['Disease', 'Mechanism']:
            mask = df[col].str.strip() != df[col]
            n = mask.sum()
            if n > 0:
                stats['whitespace'] += n
                for idx in df[mask].index:
                    correction_log.append({
                        'site': site, 'field': col, 'type': 'whitespace',
                        'original': df.at[idx, col],
                        'corrected': df.at[idx, col].strip(),
                    })
                df[col] = df[col].str.strip()
    print(f"Whitespace stripped: {stats['whitespace']} records")

    # ── Step 2: Apply Disease typo corrections ──
    for site, df in all_dfs.items():
        for orig, corrected in DISEASE_TYPO_CORRECTIONS.items():
            mask = df['Disease'] == orig
            n = mask.sum()
            if n > 0:
                stats['disease_typo'] += n
                for _ in range(n):
                    correction_log.append({
                        'site': site, 'field': 'Disease', 'type': 'typo',
                        'original': orig, 'corrected': corrected,
                    })
                df.loc[mask, 'Disease'] = corrected
    print(f"Disease typo fixes: {stats['disease_typo']} records")

    # ── Step 3: Normalize Disease case ──
    all_diseases = []
    for df in all_dfs.values():
        all_diseases.extend(df['Disease'].tolist())
    disease_case_map = normalize_case_for_column(all_diseases)

    for site, df in all_dfs.items():
        for orig, canonical in disease_case_map.items():
            mask = df['Disease'] == orig
            n = mask.sum()
            if n > 0:
                stats['disease_case'] += n
                for _ in range(n):
                    correction_log.append({
                        'site': site, 'field': 'Disease', 'type': 'case',
                        'original': orig, 'corrected': canonical,
                    })
                df.loc[mask, 'Disease'] = canonical
    print(f"Disease case normalizations: {stats['disease_case']} records")

    # ── Step 4: Strip trailing periods from Mechanism ──
    for site, df in all_dfs.items():
        mask = df['Mechanism'].str.endswith('.')
        n = mask.sum()
        if n > 0:
            stats['mech_period'] += n
            for idx in df[mask].index:
                correction_log.append({
                    'site': site, 'field': 'Mechanism', 'type': 'trailing_period',
                    'original': df.at[idx, 'Mechanism'],
                    'corrected': df.at[idx, 'Mechanism'].rstrip('.'),
                })
            df.loc[mask, 'Mechanism'] = df.loc[mask, 'Mechanism'].str.rstrip('.')
    print(f"Mechanism trailing periods: {stats['mech_period']} records")

    # ── Step 5: Normalize Mechanism case ──
    all_mechs = []
    for df in all_dfs.values():
        all_mechs.extend(df['Mechanism'].tolist())
    mech_case_map = normalize_case_for_column(all_mechs)

    for site, df in all_dfs.items():
        for orig, canonical in mech_case_map.items():
            mask = df['Mechanism'] == orig
            n = mask.sum()
            if n > 0:
                stats['mech_case'] += n
                for _ in range(n):
                    correction_log.append({
                        'site': site, 'field': 'Mechanism', 'type': 'case',
                        'original': orig, 'corrected': canonical,
                    })
                df.loc[mask, 'Mechanism'] = canonical
    print(f"Mechanism case normalizations: {stats['mech_case']} records")

    # ── Summary ──
    total_corrections = sum(stats.values())
    all_diseases_clean = []
    all_mechs_clean = []
    for df in all_dfs.values():
        all_diseases_clean.extend(df['Disease'].tolist())
        all_mechs_clean.extend(df['Mechanism'].tolist())

    print(f"\n--- Summary ---")
    print(f"Total corrections applied: {total_corrections}")
    print(f"Disease: {len(set(all_diseases))} unique -> {len(set(all_diseases_clean))} unique")
    print(f"Mechanism: {len(set(all_mechs))} unique -> {len(set(all_mechs_clean))} unique")

    # Save correction log
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    log_df = pd.DataFrame(correction_log)
    log_path = os.path.join(OUTPUT_DIR, 'data_corrections.csv')
    log_df.to_csv(log_path, index=False)
    print(f"\nCorrection log: {log_path} ({len(correction_log)} entries)")

    # Save corrected xlsx files
    for site, df in all_dfs.items():
        out_path = os.path.join(DATA_DIR, f'{site}.xlsx')
        df.to_excel(out_path, index=False)
    print(f"Corrected xlsx files saved to: {DATA_DIR}")


if __name__ == '__main__':
    main()
