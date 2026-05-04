"""
Step 1: Load and combine all 8 acupoint xlsx files.
"""
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'base_data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

SITES = ['BL25', 'GV4', 'ST25', 'CV12', 'PC6', 'LI4', 'SP6', 'ST36']


def main():
    dfs = []
    for site in SITES:
        fpath = os.path.join(DATA_DIR, f'{site}.xlsx')
        df = pd.read_excel(fpath)
        df['Site'] = site
        dfs.append(df)
        print(f"  {site}: {len(df)} records")

    combined = pd.concat(dfs, ignore_index=True)

    print(f"\n--- Summary ---")
    print(f"Total records: {len(combined)}")
    print(f"Unique PMIDs: {combined['PMID'].nunique()}")
    print(f"Records with 'Unknown' mechanism: {(combined['Mechanism'] == 'Unknown').sum()}")
    print(f"Unique Disease strings: {combined['Disease'].nunique()}")
    print(f"Unique Mechanism strings: {combined['Mechanism'].nunique()}")

    out_path = os.path.join(OUTPUT_DIR, 'combined_data.csv')
    combined.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")
    return combined


if __name__ == '__main__':
    main()
