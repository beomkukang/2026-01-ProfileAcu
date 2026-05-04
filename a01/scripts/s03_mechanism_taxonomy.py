"""
Step 3: Build progressive mechanism taxonomy (8 levels, k=4 to k=13).
Molecular keyword-based, deterministic classification with priority ranking.

v2: Expanded keyword lists to reduce unclassified "Other" records.
    Added Neural Circuit/Connectivity category at level 8.
v3: Second keyword expansion pass after inspecting remaining 245
    unclassified records. Targets ~3.8% residual Other.
v4: Final pass on remaining 84 records. ~2.7% truly unclassifiable.
"""
import pandas as pd
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'results', 'datatables')

# --- Taxonomy levels ---
# Level 1 (k=4): Inflammatory/Immune | Neuroprotective | Analgesic/Opioid | Other
# Level 2 (k=6): + Autonomic/Neuroendocrine, + Oxidative Stress
# Level 3 (k=8): + Gut-Brain/Enteric, + Neurochemical Signaling
# Level 4 (k=9): + Cell Survival/Apoptosis
# Level 5 (k=10): + Ion Channel/Pain Transduction (split from Analgesic)
# Level 6 (k=11): + Autophagy/Mitophagy (split from Cell Survival)
# Level 7 (k=12): + Metabolic Pathway Regulation
# Level 8 (k=13): + Neural Circuit/Connectivity

KEYWORDS = {
    'Analgesic/Opioid': [
        'opioid', 'enkephalin', 'endorphin', 'mu-receptor', 'mu receptor',
        'delta-receptor', 'delta receptor', 'κ-receptor', 'kappa opioid',
        'descending inhibition', 'analgesi', 'dynorphin',
        'PAG', 'periaqueductal gray', 'RVM', 'rostral ventromedial',
        'antinocicepti', 'pain inhibit', 'inhibitory pathways in the spinal cord',
        'spinal cord analges', 'prolongation of anesthetic',
        'CGRP', 'substance P', 'SP,', 'SP and',
        'Penk', 'proenkephalin',
        # v4 expansion
        'endogenous opiate', 'opiate system',
    ],
    'Ion Channel/Pain Transduction': [
        'TRPV1', 'TRPV4', 'TRPA1', 'ASIC', 'Nav1.7', 'Nav1.8', 'Nav1.9',
        'Nav1.1', 'Nav1.6',
        'P2X', 'PANX', 'pannexin', 'calcium channel', 'potassium channel',
        'ion channel', 'sodium channel', 'KCNQ', 'Kv7', 'HCN',
        'Piezo1', 'Piezo2', 'mechanosensitive',
        'NR2B', 'calcium signaling', 'Ca2+ signaling',
        'purinergic', 'ATP signaling',
        # v3 expansion
        'KATP channel', 'Kir2.1', 'Kir2.2',
        'voltage-gated Na', 'Na(v)', 'Nav inactivation',
        'transient outward K+', 'Ito channel', 'cardiac Ito',
        'L-type Ca2+ channel', 'calcium efflux',
        'TRPC6', 'PKC signaling',
        'PKA signaling', 'cAMP pathway', 'beta(1)-adrenoceptor',
    ],
    'Gut-Brain/Enteric': [
        'gut microbiota', 'microbiome', 'SCFA', 'enteric', 'ICC',
        'intestinal flora', 'gut-brain', 'gut brain', 'probiot',
        'fecal microbi', 'bacteroides', 'lactobacill', 'bifidobact',
        'short-chain fatty acid', 'intestinal barrier',
        'brain-gut', 'brain gut', 'gut flora', 'dysbiosis',
        'cecal microbiota', 'intestinal microbiota',
        'intestinal defensin', 'tight junction', 'ZO-1',
        'GI motility', 'gastrointestinal transit', 'colonic motility',
        'gastric motility', 'intestinal motility',
        'brain-gut peptide', 'NPY, CCK', 'SST, GAS',
        'c-kit', 'interstitial cells of cajal',
        'gut peptide',
        # v3 expansion
        'intestinal fungal', 'microbial phenylalanine',
        'occludin', 'intestinal microvascular',
        # v4 expansion
        'gastroduodenal microbiota', 'bile acid metabolism',
        'bowel function', 'VIP expression', 'vasoactive intestinal peptide',
    ],
    'Autophagy/Mitophagy': [
        'PINK1', 'Parkin', 'LC3', 'Beclin', 'autophagy', 'mitophagy',
        'AMPK-mediated autophagy', 'autophagic', 'autolysosome',
        'p62', 'SQSTM1', 'ULK1',
    ],
    'Neural Circuit/Connectivity': [
        'neural circuit', 'neural coding', 'circuitry',
        'rACC', 'DRN', 'BLA', 'CeA', 'central amygdala',
        'basolateral amygdala', 'prefrontal cortex',
        'thalamo-cortico', 'thalamic neuron', 'VPL',
        'infralimbic', 'prelimbic', 'ACC-',
        'BNST', 'bed nucleus',
        'dorsal horn neuron', 'spinal dorsal horn',
        'GABAergic neuron', 'CaMKII',
        'cortical excitability', 'functional connectivity',
        'neural pathway', 'neuronal activity',
        # v3 expansion
        'vHPC', 'mPFC', 'VTA', 'LDTgv',
        'nucleus accumbens', 'NACc', 'FosB',
        'anterior cingulate cortex',
        'anterior pretectal nucleus', 'APtN',
        'dorsolateral funiculus', 'DLF',
        'PVN', 'RVLM',
        'brain network', 'effective connectivity',
        'brain activity', 'brain regions', 'regional brain',
        'medial forebrain bundle', 'reward function',
        'c-fos expression',
        'AGRP', 'deactivation of',
        # v4 expansion
        'neural oscillation', 'firing rate',
        'SRD neuron', 'WDR neuron', 'S1 cortex',
        'brain functional', 'brain hemodynamic', 'CBV modulation',
        'multi-targeting brain', 'PKMzeta', 'NPS/NPSR',
        'afferent nerve', 'primary afferent',
        'glymphatic',
    ],
    'Autonomic/Neuroendocrine': [
        'vagal', 'vagus', 'sympathetic', 'parasympathetic', 'HPA axis',
        'hypothalam', 'autonomic', 'adrenergic', 'norepinephrine',
        'catecholamine', 'CRH', 'CRF', 'corticotropin', 'neuroendocrine',
        'baroreceptor', 'baroreflex', 'heart rate variability',
        'somatic afferent', 'somato', 'afferent C-fiber',
        'GR/GILZ', 'glucocorticoid receptor',
        'hormone level', 'testosterone', 'estrogen',
        'progesterone', 'prolactin',
        'kisspeptin', 'HPG axis', 'HPO axis',
        'blood pressure', 'counteracting CRD',
        # v3 expansion
        'ovarian innervation', 'superior ovarian nerve',
        'endometrial receptivity', 'LIF', 'OPN',
        'cathepsin K', 'CTX-I',
        'pinopode',
        'Tph1', 'Olr883',
    ],
    'Neurochemical Signaling': [
        '5-HT', 'serotonin', 'dopamine', 'GABA', 'glutamate',
        'acetylcholine', 'NMDA', 'AMPA', 'glycine receptor',
        'monoamine', 'neurotransmit',
        'D1 receptor', 'D2 receptor', '5-HT1A', '5-HT3',
        'adenosine', 'A2A receptor', 'A2AR',
        'cannabinoid', 'CB1', 'CB2',
        'muscarinic', 'M3 receptor', 'nicotinic',
        'AChE', 'cholinesterase',
        'endothelin', 'neuropeptide',
        'G protein coupled', 'GPCR',
        'synaptotagmin', 'Syt-1',
        # v3 expansion
        'serotonergic', 'orexin', 'orphanin', 'nociceptin', 'OFQ',
        'CCK(B)', 'CCK-A', 'CCK-NK1', 'cholecystokinin',
        'GluR2', 'PICK1', 'ICA69',
        'P2Y receptor', 'P2Y2R', 'NTPDase',
        'Adora-3',
        'adrenoceptor', 'alpha2-adrenoceptor',
        'cholinergic tone', 'cholinergic signaling', 'DMV cholinergic',
        'tryptophan', 'indole', 'melatonin',
        'DNMT3a', 'MOR signaling',
        'SYT-3', 'GLUA2',
        'α1-AR', 'β2-AR',
        # v4 expansion
        'D1/D5', 'mGluR5',
        'oxytocin', 'nAChR',
        'cholinergic nerve', 'cholinergic mechanism',
    ],
    'Oxidative Stress': [
        'ROS', 'SOD', 'Nrf2', 'ARE', 'ferroptosis', 'lipid peroxidation',
        'oxidative stress', 'antioxidant', 'MDA', 'malondialdehyde',
        'superoxide', 'catalase', 'glutathione peroxidase', 'GPx',
        'HO-1', 'heme oxygenase', 'Keap1', 'thioredoxin',
        'oxidative protein damage', 'oxidative damage',
        'mitochondrial homeostasis', 'mitochondrial dysfunction',
        'mitochondrial membrane potential',
        'HSP20', 'HSP27', 'HSP84', 'HSP86', 'heat shock protein',
        'ER stress', 'endoplasmic reticulum stress',
        'IRE1', 'XBP1', 'PERK', 'ATF6', 'unfolded protein',
        # v3 expansion
        'xCT', 'System Xc',
        'mitochondrial fission', 'FIS1', 'Drp1',
        'mitochondrial dynamics', 'mitochondrial damage',
        'TFEB', 'lysosomal',
        'HSP70', 'Hspb7',
        # v4 expansion
        'NADPH oxidase', 'reactive oxygen species',
        'eNOS', 'NO production',
    ],
    'Cell Survival/Apoptosis': [
        'PI3K', 'AKT', 'Bcl-2', 'Bax', 'caspase', 'apoptosis',
        'mTOR', 'anti-apoptotic', 'pro-apoptotic', 'cell death',
        'survival', 'Mcl-1', 'cytochrome c', 'TUNEL', 'annexin',
        'necroptosis', 'pyroptosis', 'RIPK', 'MLKL',
        'RhoA', 'ROCK', 'focal adhesion',
        'EMT', 'epithelial-mesenchymal',
        'Wnt/β-catenin', 'GSK-3', 'pGSK',
        'cell proliferation', 'cell migration',
        'RANK', 'RANKL', 'OPG', 'MMP-13', 'MMP-9',
        'VEGF', 'angiogenesis', 'HIF-1',
        'STING', 'IFN-1', 'interferon',
        'PD-L1', 'PD-1', 'SHP-1',
        'complement system',
        'exosom', 'miR-', 'miRNA', 'circRNA', 'let-7',
        # v3 expansion
        'Notch signaling', 'Notch1',
        'CDK6', 'CCND1', 'ac4C modification',
        'Hedgehog pathway',
        'BMP2', 'BMPR', 'Smad',
        'IGF', 'IGF-I', 'IGF1R',
        'proteasome', 'GLAST', 'GLT-1',
        'PDGF', 'astrogliosis',
        'matrix metalloproteinase', 'ADAMTS',
        'MAFbx', 'MuRF1',
        'stem cell', 'NSCs', 'HSCs', 'MSCs',
        'ferritinophagy', 'NCOA4',
        'connexin43', 'Cx43',
        'ACE2', 'Ang II', 'AT1R', 'AT2R', 'MasR', 'Ang(1-7)',
        'p-MLC', 'p-MLCK', 'myosin light chain',
        'lncRNA',
        'Ephrin', 'EphB',
        'antiapoptotic',
        # v4 expansion
        'collagen fibril', 'ECM expression', 'fibronectin',
        'α-smooth muscle actin',
        'cell adhesion molecule',
        'BMSC homing',
        'cytoskeletal protein', 'Sertoli cell',
        'tumor-associated vasculature',
    ],
    'Neuroprotective': [
        'BDNF', 'NGF', 'Wnt', 'beta-catenin',
        'synaptic plasticity', 'neurogenesis', 'neuroplasticity',
        'neuroprotect', 'neurotrophic', 'TrkB', 'CREB', 'LTP',
        'long-term potentiation', 'dendritic', 'synaptogenesis',
        'myelin', 'remyelination', 'axon', 'neural stem',
        'neurovascular unit', 'neurovascular',
        'nerve regeneration', 'nerve repair', 'nerve growth',
        'neuregulin', 'ErbB',
        'GDNF', 'CNTF', 'NT-3', 'NT-4',
        'dentate gyrus', 'hippocampal neurogenesis',
        'cerebral blood', 'blood-brain barrier', 'BBB',
        'white matter', 'oligodendrocyte',
        'CD73', 'ADA expression',
        # v3 expansion
        'GFAP', 'satellite glial', 'glial scar', 'vimentin',
        'cerebral microangiopathy',
        'srGAP3', 'Rac1',
        'sciatic nerve mediation', 'nerve mediation',
        'motoneuron', 'nNOS expression',
        'movement function', 'movement recovery',
        # v4 expansion
        'neuronal regeneration', 'GAP-50', 'synaptophysin',
        'neuronal structure', 'cerebral cortical blood oxygen',
        'spinal glial',
        'angiopoietin',
    ],
    'Inflammatory/Immune': [
        'NF-kB', 'NF-κB', 'TLR', 'TNF', 'IL-1', 'IL-6', 'IL-10',
        'macrophage', 'cytokine', 'a7nAChR', 'alpha7',
        'cholinergic anti-inflammatory', 'NLRP3', 'inflammasome',
        'COX-2', 'prostaglandin', 'JAK', 'STAT', 'p38 MAPK',
        'ERK', 'JNK', 'IκB', 'IKK', 'microgli', 'astrocyt',
        'anti-inflammatory', 'pro-inflammatory', 'immune',
        'neutrophil', 'T cell', 'Treg', 'Th17', 'HMGB1',
        'MAPK', 'inflammatory',
        'COX-1', 'PGE2', 'leukotriene',
        'mast cell', 'degranulation',
        'innate immun', 'adaptive immun',
        'DMT1', 'Fpn1', 'iron metabolism',
        'SDF-1', 'CXCR', 'chemokine',
        # v3 expansion
        'p38 mitogen-activated protein kinase',
        'Th1/Th2', 'LTB4', 'CCL2', 'CCR2', 'CCR3', 'eotaxin',
        'IL-33', 'ST2 signaling', 'NLRC4',
        'CD200', 'CD5 expression',
        'lipoxin', 'LXA4',
        'splenic T lymphocyte', 'IL-2', 'CD4+', 'CD8+',
        'MD2 expression', 'efferocytosis', 'ABCA1',
        'CTGF', 'TGF-β', 'TGF-beta',
        'iNOS', 'NOS expression', 'nitric oxide',
        'neuroinflammation', 'tau phosphorylation',
        'transcriptomic modulation',
        # v4 expansion
        'IgE', 'IL-4', 'NLRP6',
        'CX3CL1', 'fractalkine',
        'nociception and inflammation',
        'bone destruction',
        'tryptase', 'PAR-2',
        'mossy fiber sprouting',
    ],
    'Metabolic Pathway': [
        'AMPK', 'SIRT1', 'insulin signaling', 'glucose metabolism',
        'lipid metabolism', 'PGC-1', 'PPAR', 'fatty acid oxidation',
        'glycolysis', 'gluconeogenesis', 'energy metabolism',
        'mitochondrial biogenesis', 'metabolic regulation',
        'adiponectin', 'leptin', 'FGF21',
        'blood glucose', 'hyperglycemia', 'glycemia',
        'IRS-1', 'insulin resistance', 'HOMA-IR',
        'hexokinase', 'pyruvate kinase', 'G6PD',
        'glycometabolic', 'lipid absorption',
        'palmitic acid', 'cholesterol',
        'lactate', 'lactacidemia',
        'cGMP', 'PKG', 'renin',
        'DPP4', 'GLP-1', 'incretin',
        'SRD5A2', 'DHT',
        'acupoint microcirculation', 'microcirculation',
        'Apelin', 'APJ',
        # v3 expansion
        'free fatty acid', 'insulin sensitivity',
        'glycolipid', 'GLO/AGEs', 'RAGE',
        'arachidonic acid', 'pentose phosphate',
        'ASGPR', 'liver reserve',
        'cardiac metabolic demand',
        'skeletal muscle atrophy', 'muscle atrophy',
        # v4 expansion
        'UCP1', 'adipose tissue browning', 'white adipose',
        'SREBP', 'irisin', 'ghrelin',
        'GlyRS', 'muscle protein synthesis',
        'retinoic acid', 'collagen concentration',
        'ACTH release', 'amylase', 'lipase',
    ],
}

# Priority order: first match wins (most specific → broadest)
PRIORITY_ORDER = [
    'Analgesic/Opioid',
    'Ion Channel/Pain Transduction',
    'Gut-Brain/Enteric',
    'Autophagy/Mitophagy',
    'Neural Circuit/Connectivity',
    'Autonomic/Neuroendocrine',
    'Neurochemical Signaling',
    'Oxidative Stress',
    'Cell Survival/Apoptosis',
    'Neuroprotective',
    'Inflammatory/Immune',
    'Metabolic Pathway',
]

# Categories available at each level
LEVEL_CATEGORIES = {
    1: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid'],
    2: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress'],
    3: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress',
        'Gut-Brain/Enteric', 'Neurochemical Signaling'],
    4: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress',
        'Gut-Brain/Enteric', 'Neurochemical Signaling',
        'Cell Survival/Apoptosis'],
    5: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress',
        'Gut-Brain/Enteric', 'Neurochemical Signaling',
        'Cell Survival/Apoptosis', 'Ion Channel/Pain Transduction'],
    6: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress',
        'Gut-Brain/Enteric', 'Neurochemical Signaling',
        'Cell Survival/Apoptosis', 'Ion Channel/Pain Transduction',
        'Autophagy/Mitophagy'],
    7: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress',
        'Gut-Brain/Enteric', 'Neurochemical Signaling',
        'Cell Survival/Apoptosis', 'Ion Channel/Pain Transduction',
        'Autophagy/Mitophagy', 'Metabolic Pathway'],
    8: ['Inflammatory/Immune', 'Neuroprotective', 'Analgesic/Opioid',
        'Autonomic/Neuroendocrine', 'Oxidative Stress',
        'Gut-Brain/Enteric', 'Neurochemical Signaling',
        'Cell Survival/Apoptosis', 'Ion Channel/Pain Transduction',
        'Autophagy/Mitophagy', 'Metabolic Pathway',
        'Neural Circuit/Connectivity'],
}


def classify_mechanism(mech_str, available_categories):
    """Classify a mechanism string given available categories at a level."""
    text = mech_str.lower()

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

    mechanisms = df['Mechanism'].unique()
    print(f"Unique mechanism strings: {len(mechanisms)}")

    results = []
    for mech in mechanisms:
        row = {'mechanism_string': mech, 'matched_keywords': ''}

        if mech == 'Unknown':
            for level in range(1, 9):
                row[f'level_{level}'] = 'Unknown'
            results.append(row)
            continue

        prev_cat = None
        for level in range(1, 9):
            available = LEVEL_CATEGORIES[level]

            # Progressive inheritance
            if prev_cat is not None and prev_cat != 'Other':
                # Check splits: level 5 splits Ion Channel from Analgesic
                if level == 5 and prev_cat == 'Analgesic/Opioid':
                    cat, kw = classify_mechanism(mech, available)
                    if cat == 'Ion Channel/Pain Transduction':
                        row[f'level_{level}'] = cat
                        if kw:
                            row['matched_keywords'] = kw
                        prev_cat = cat
                        continue
                # Level 6 splits Autophagy from Cell Survival
                elif level == 6 and prev_cat == 'Cell Survival/Apoptosis':
                    cat, kw = classify_mechanism(mech, available)
                    if cat == 'Autophagy/Mitophagy':
                        row[f'level_{level}'] = cat
                        if kw:
                            row['matched_keywords'] = kw
                        prev_cat = cat
                        continue

                row[f'level_{level}'] = prev_cat
                continue

            cat, kw = classify_mechanism(mech, available)
            row[f'level_{level}'] = cat
            if kw and not row['matched_keywords']:
                row['matched_keywords'] = kw
            prev_cat = cat

        results.append(row)

    out_df = pd.DataFrame(results)
    out_path = os.path.join(OUTPUT_DIR, 'mechanism_dictionary.csv')
    out_df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")

    # Print summary
    for level in range(1, 9):
        col = f'level_{level}'
        counts = out_df[col].value_counts()
        other_pct = counts.get('Other', 0) / len(out_df) * 100
        n_cats = out_df[col].nunique()
        print(f"  Level {level} (k={n_cats}): {other_pct:.1f}% Other")

    return out_df


if __name__ == '__main__':
    main()
