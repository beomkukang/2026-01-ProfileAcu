"""
Step 2: Build progressive disease taxonomy (7 levels, k=5 to k=15).
Keyword-based, deterministic classification with progressive inheritance.

v2: Expanded keyword lists to catch misspellings, synonyms, and
    near-matches found in the unclassified "Other" bin.
"""
import pandas as pd
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

# --- Taxonomy level definitions ---
# Level 1 (k=5): Pain | Neurological | Cardiovascular | Gastrointestinal | Other
# Level 2 (k=7): + Metabolic/Endocrine, + Psychiatric (split from Neurological)
# Level 3 (k=9): + Reproductive, + Musculoskeletal
# Level 4 (k=11): + Respiratory, + Immune/Inflammatory
# Level 5 (k=13): + Renal/Urological, + Dermatological
# Level 6 (k=14): + Addiction (split from Psychiatric)
# Level 7 (k=15): + Cancer/Oncology

LEVEL_NAMES = {
    1: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal', 'Other'],
    2: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Other'],
    3: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal', 'Other'],
    4: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Other'],
    5: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological', 'Other'],
    6: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological',
        'Addiction', 'Other'],
    7: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological',
        'Addiction', 'Cancer/Oncology', 'Other'],
}

# --- Keyword rules per category ---
# Applied in order; first match wins within each level's available categories.

KEYWORDS = {
    'Pain': [
        'pain', 'nocicepti', 'analges', 'headache', 'migraine', 'fibromyalgia',
        'dysmenorrh', 'neuralgia', 'hyperalgesia', 'allodynia', 'colic',
        'visceral hypersensitivity', 'chronic prostatitis', 'endometriosis pain',
        'complex regional pain', 'postoperative pain', 'cancer pain',
        'neuropathic pain', 'inflammatory pain', 'orofacial pain',
        'low back pain', 'sciatica', 'trigeminal', 'toothache',
        'hyperalgesic priming', 'excruciating pain',
        'chronic constrictive injury',
    ],
    'Neurological': [
        'stroke', 'cerebral isch', 'MCAO', 'brain injury', 'traumatic brain',
        'spinal cord injury', 'SCI', 'epilepsy', 'seizure', 'alzheimer',
        'parkinson', 'dementia', 'multiple sclerosis', 'EAE',
        'neuropathy', 'peripheral nerve', 'nerve injury', 'neurodegenerat',
        'cerebral palsy', 'encephalitis', 'meningitis', 'cognitive impairment',
        'vascular dementia', 'brain isch', 'cerebral hemorrhage',
        'intracerebral', 'subarachnoid', 'ischemia reperfusion brain',
        'neuroinflammation', 'motor dysfunction', 'paralysis', 'hemiplegia',
        'ataxia', 'huntington', 'ALS', 'amyotrophic',
        'CIPN', 'chemotherapy-induced peripheral neuropathy',
        # Synonyms and variants found in data
        'cerebral infarction', 'cerebral infarct',
        'cognitive dysfunction', 'cognitive deficit', 'cognitive deficits',
        'memory deficit', 'memory impairment', 'learning and memory',
        'neurocognitive disorder', 'neurocognitive dysfunction',
        'encephalopathy', 'neuronal apoptosis', 'neurological injury',
        'neurological disorder', 'neurology',
        'cerebral hypoperfusion', 'white matter injury', 'white matter damage',
        'hippocampal injury', 'cerebral injury',
        'brachial plexus',
        'nerve ligation', 'ganglionectom',
        'ischemia-reperfusion', 'ischemia reperfusion',
        'I/R injury', 'cerebral I/R',
        'autism', 'autism spectrum', 'ASD',
        'delirium', 'hydrocephalus',
        'nervous discharge',
        'retinal ischemia',
        'myasthenia gravis',
        'dopamine release',  # "Excessive dopamine release"
    ],
    'Cardiovascular': [
        'cardiac', 'heart', 'myocardial', 'hypertension', 'atherosclerosis',
        'arrhythmia', 'atrial fibrillation', 'heart failure', 'coronary',
        'cardiomyopathy', 'ischemia reperfusion heart', 'vascular',
        'angina', 'thrombosis', 'aneurysm', 'hypotension', 'shock',
        'cardio', 'aortic', 'ventricular', 'blood pressure',
        'pulmonary hypertension', 'peripheral arterial',
        # Synonyms found in data
        'CVD', 'QT interval', 'blood stasis',
        'vessel disease', 'CSVD',
        'flap survival',  # "Random pattern flap survival" — vascular
    ],
    'Gastrointestinal': [
        'gastric', 'intestin', 'colitis', 'IBS', 'irritable bowel',
        'constipation', 'diarrhea', 'dyspepsia', 'gastroparesis',
        'inflammatory bowel', 'crohn', 'ulcerative colitis', 'GERD',
        'reflux', 'nausea', 'vomiting', 'emesis', 'POI',
        'postoperative ileus', 'functional dyspepsia', 'GI motility',
        'bowel', 'colon', 'rectal', 'abdominal', 'gut', 'digestive',
        'hepatic', 'liver', 'cirrhosis', 'NAFLD', 'fatty liver',
        'pancreatitis', 'cholestasis', 'gallbladder',
        # Synonyms found in data
        'ileus', 'gastritis', 'gastroenteric',
        'diarrhoe',  # British spelling variant
        'anorexia', 'motion sickness',
        'cecitis', 'enteritis', 'ulcer',
        'jejun', 'defaecation', 'hepatitis',
        'atrophic gastritis',
    ],
    'Metabolic/Endocrine': [
        'diabetes', 'diabetic', 'insulin', 'glucose', 'obesity', 'metabolic syndrome',
        'hyperlipidemia', 'dyslipidemia', 'thyroid', 'hyperthyroid', 'hypothyroid',
        'PCOS', 'polycystic ovary', 'adrenal', 'cushing', 'osteoporosis',
        'hyperglycemia', 'type 2 diabetes', 'type 1 diabetes', 'HFD',
        'high-fat diet', 'weight', 'adipos',
        # Synonyms found in data
        'hyperglycaemia',  # British spelling
        'lipid metabolic disorder', 'osteopenia',
        'HPA axis',  # "Hyperactivity of the HPA axis"
    ],
    'Psychiatric': [
        'depression', 'anxiety', 'PTSD', 'stress', 'insomnia', 'sleep',
        'schizophrenia', 'bipolar', 'OCD', 'panic', 'phobia',
        'chronic fatigue', 'chronic unpredictable', 'CUS', 'CUMS',
        'learned helplessness', 'social defeat', 'anhedonia',
        'postpartum depression', 'mood',
        # Synonyms found in data
        'major depressive', 'fatigue',
    ],
    'Reproductive': [
        'fertil', 'ovarian', 'uterine', 'endometri', 'pregnancy',
        'preeclampsia', 'labor', 'menopaus', 'sperm', 'erectile',
        'testicular', 'prostate', 'PCOS', 'implantation', 'IVF',
        'reproductive', 'sexual', 'premature ovarian',
        # Synonyms found in data
        'prostatitis', 'prostatic hyperplasia', 'BPH',
        'superovulation', 'vaginal', 'uterine atrophy',
        'premature ejaculation', 'ejaculat',
    ],
    'Musculoskeletal': [
        'arthritis', 'osteoarthritis', 'rheumatoid', 'joint', 'tendon',
        'muscle atrophy', 'sarcopenia', 'fracture', 'bone loss',
        'intervertebral disc', 'disc degeneration', 'cartilage',
        'skeletal muscle', 'muscular', 'ligament', 'knee',
        'cervical spondyl', 'lumbar', 'rotator cuff',
        # Synonyms and typos found in data
        'ankylosing spondylitis',
        'muscle injury', 'myopathy',
        'spondylitis',
    ],
    'Respiratory': [
        'asthma', 'COPD', 'pulmonary fibrosis', 'lung injury', 'ALI',
        'ARDS', 'pneumonia', 'bronchitis', 'airway', 'respiratory',
        'lung cancer', 'cough', 'dyspnea', 'ventilat',
        'acute lung injury', 'cigarette smoke', 'allergic rhinitis',
        # Synonyms found in data
        'pulmonary disease', 'pulmonary dysplasia',
        'emphysema', 'lung damage', 'smoke exposed',
        'diesel exhaust', 'pulmonary inflammatory',
        'obstructive pulmonary',
    ],
    'Immune/Inflammatory': [
        'sepsis', 'systemic lupus', 'lupus', 'autoimmune',
        'organ transplant', 'graft', 'anaphylaxis', 'allerg',
        'immunodeficiency', 'HIV', 'inflammation', 'immune',
        'mast cell', 'urticaria', 'immunosuppress', 'cytokine storm',
        # Synonyms found in data
        'periodontitis', 'pulpitis',
        'peritonitis', 'inflammatory injury', 'inflammatory disease',
        'parasite infection', 'lyme disease',
        'herpes simplex', 'HSV',
        'hand-foot-mouth', 'HFMD',
        'immunosenescence', 'aging',
        'oxidative damage', 'surgical trauma',
        'postoperative complication',
        'telomerase-deficient',
    ],
    'Renal/Urological': [
        'kidney', 'renal', 'nephro', 'bladder', 'urinary', 'incontinence',
        'cystitis', 'dialysis', 'CKD', 'acute kidney', 'AKI',
        'overactive bladder', 'ureter', 'urethra', 'nephrolithiasis',
    ],
    'Dermatological': [
        'skin', 'dermatitis', 'eczema', 'psoriasis', 'wound healing',
        'burn', 'scar', 'pruritus', 'itch', 'atopic dermatitis',
        'alopecia', 'hair loss', 'acne', 'vitiligo', 'cutaneous',
    ],
    'Addiction': [
        'addiction', 'substance abuse', 'drug dependence', 'withdrawal',
        'alcohol', 'nicotine', 'opioid use disorder', 'cocaine',
        'methamphetamine', 'morphine dependence', 'heroin', 'smoking cessation',
        'relapse', 'drug seeking', 'self-administration',
        # Synonyms found in data
        'opioid tolerance', 'morphine tolerance',
        'drug abuse',
    ],
    'Cancer/Oncology': [
        'cancer', 'tumor', 'tumour', 'carcinoma', 'neoplasm', 'oncolog',
        'leukemia', 'lymphoma', 'melanoma', 'sarcoma', 'metastas',
        'chemotherapy', 'cisplatin', 'doxorubicin', 'radiotherapy',
        'antitumor', 'anti-tumor',
        # Synonyms found in data
        'glioma',
    ],
}

# Categories available at each level
LEVEL_CATEGORIES = {
    1: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal'],
    2: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric'],
    3: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal'],
    4: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory'],
    5: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological'],
    6: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological',
        'Addiction'],
    7: ['Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
        'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
        'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological',
        'Addiction', 'Cancer/Oncology'],
}

# Priority order for classification (first match wins)
PRIORITY_ORDER = [
    'Pain', 'Neurological', 'Cardiovascular', 'Gastrointestinal',
    'Metabolic/Endocrine', 'Psychiatric', 'Reproductive', 'Musculoskeletal',
    'Respiratory', 'Immune/Inflammatory', 'Renal/Urological', 'Dermatological',
    'Addiction', 'Cancer/Oncology',
]


def extract_primary_condition(disease_str):
    """For comorbidity strings, extract the primary (first) condition."""
    separators = [' with comorbid', ' accompanied by', ' with ', ' and ']
    lower = disease_str.lower()
    for sep in separators:
        idx = lower.find(sep)
        if idx > 0:
            return disease_str[:idx]
    return disease_str


def classify_disease(disease_str, available_categories):
    """Classify a disease string given available categories at a level."""
    primary = extract_primary_condition(disease_str)
    text = primary.lower()

    for cat in PRIORITY_ORDER:
        if cat not in available_categories:
            continue
        for kw in KEYWORDS[cat]:
            if kw.lower() in text:
                return cat, kw
    return 'Other', ''


def main():
    combined_path = os.path.join(OUTPUT_DIR, 'combined_data.csv')
    df = pd.read_csv(combined_path)
    diseases = df['Disease'].unique()
    print(f"Unique disease strings: {len(diseases)}")

    results = []
    for disease in diseases:
        row = {'disease_string': disease, 'matched_keyword': ''}
        prev_cat = None

        for level in range(1, 8):
            available = LEVEL_CATEGORIES[level]
            # Progressive inheritance: if previously classified as non-Other, keep it
            # unless it needs to be split (Psychiatric->Addiction handled below)
            if prev_cat is not None and prev_cat != 'Other':
                # Check if this category was split at this level
                if level == 6 and prev_cat == 'Psychiatric':
                    # Re-classify to check for Addiction
                    cat, kw = classify_disease(disease, available)
                    if cat == 'Addiction':
                        row[f'level_{level}'] = cat
                        if kw:
                            row['matched_keyword'] = kw
                        prev_cat = cat
                        continue
                row[f'level_{level}'] = prev_cat
                continue

            cat, kw = classify_disease(disease, available)
            row[f'level_{level}'] = cat
            if kw and not row['matched_keyword']:
                row['matched_keyword'] = kw
            prev_cat = cat

        results.append(row)

    out_df = pd.DataFrame(results)
    out_path = os.path.join(OUTPUT_DIR, 'disease_dictionary.csv')
    out_df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")

    # Print summary
    for level in range(1, 8):
        col = f'level_{level}'
        counts = out_df[col].value_counts()
        other_pct = counts.get('Other', 0) / len(out_df) * 100
        n_cats = out_df[col].nunique()
        print(f"  Level {level} (k={n_cats}): {other_pct:.1f}% Other")

    return out_df


if __name__ == '__main__':
    main()
