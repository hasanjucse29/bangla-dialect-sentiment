"""
TALLIP V2 Clean Dataset Builder, Zero-Leakage Group Splitter & Blind IAA Sheet Generator
=======================================================================================
Non-destructive pipeline: reads from data/raw/ and writes exclusively to data/tallip_v2/.
Does NOT modify any existing thesis or benchmark files.

Key fixes addressing ACM TALLIP peer-review concerns:
1. Applies Unicode NFC normalization + safe punctuation collapse (preserving Bengali ZWJ/ZWNJ).
2. Includes all 981 labeled SAPTAK utterances (eliminating clipping of 199 negative SAPTAK rows)
   while tagging Source, ANUBHUTI 4-way parallel status, and pure-Surprise flags.
3. Executes true SHA-256 deduplication per (Dialect_Region, normalized_Dialect_Text), removing
   exact duplicates and conflicting-label duplicates.
4. Performs strict zero-leakage Stratified Group Split (80/10/10) grouped by sha256(Standard_Text)
   so no underlying sentence or parallel translation spans Train/Val/Test.
5. Generates a genuine Double-Blind 500-sample Human IAA audit worksheet (original labels stripped)
   paired with a separate ground-truth key file.
"""

import csv
import hashlib
import json
import os
import random
import re
import unicodedata
from collections import Counter, defaultdict

SEED = 42
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
OUT_DIR = os.path.join(BASE_DIR, 'data', 'tallip_v2')
AUDIT_DIR = os.path.join(OUT_DIR, 'human_audit')

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(AUDIT_DIR, exist_ok=True)


def clean_bengali_text(text: str) -> str:
    """Apply Unicode NFC normalization, collapse whitespace and repeated punctuation runs."""
    if text is None:
        return ""
    s = unicodedata.normalize('NFC', str(text))
    # Remove invisible BOM / zero-width space noise except ZWJ (\u200d) & ZWNJ (\u200c) inside conjuncts
    s = s.replace('\ufeff', '').replace('\u200b', '')
    # Collapse repeated punctuation noise (e.g., ...... or ????? or ,,,,) to single mark
    s = re.sub(r'([।.?!,;:\-])\1+', r'\1', s)
    # Normalize spaces/newlines to single space
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def sha256_short(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def load_all_raw_sources():
    records = []

    # 1. Chattogram Sent (Original Chattogram Dataset)
    chat_csv = os.path.join(RAW_DIR, 'chattogram_sentiment_dataset.csv')
    with open(chat_csv, 'r', encoding='utf-8') as f:
        for idx, row in enumerate(csv.DictReader(f)):
            sent = str(row.get('Sentiment', '')).strip().lower()
            if sent not in {'negative', 'neutral', 'positive'}:
                continue
            std_raw = str(row.get('Bengali', '')).strip()
            dia_raw = str(row.get('Chattogram', '')).strip()
            if not std_raw or not dia_raw:
                continue
            records.append({
                'Standard_Text_Raw': std_raw,
                'Dialect_Text_Raw': dia_raw,
                'Standard_Text': clean_bengali_text(std_raw),
                'Dialect_Text': clean_bengali_text(dia_raw),
                'Sentiment': sent,
                'Dialect_Region': 'Chattogram',
                'Source': 'Original_Chattogram_Dataset',
                'Is_Pure_Surprise': 0,
                'Anubhuti_Row_Id': -1,
            })

    # 2. ANUBHUTI Parallel 4-Dialect Corpus
    anu_lbl_path = os.path.join(RAW_DIR, 'anubhuti', 'ANUBHUTI.csv')
    anu_txt_path = os.path.join(RAW_DIR, 'anubhuti', 'ANUBHUTI_Translated_Texts.csv')
    with open(anu_lbl_path, 'r', encoding='utf-8') as f1, open(anu_txt_path, 'r', encoding='utf-8') as f2:
        lbl_rows = list(csv.DictReader(f1))
        txt_rows = list(csv.DictReader(f2))
    assert len(lbl_rows) == len(txt_rows), "ANUBHUTI label/text length mismatch!"

    neg_cols = ['anger', 'contempt', 'disgust', 'fear', 'sadness']
    region_col_map = [
        ('Chittagong', 'Chattogram'),
        ('Noakhali', 'Noakhali'),
        ('Sylhet', 'Sylhet'),
        ('Mymenshingh', 'Mymensingh'),
    ]

    conflict_dropped = 0
    for idx, (lr, tr) in enumerate(zip(lbl_rows, txt_rows)):
        is_neg = any(str(lr.get(c, '0')).strip() == '1' for c in neg_cols)
        is_pos = str(lr.get('enjoyment', '0')).strip() == '1'
        is_surp_only = (
            str(lr.get('surprise', '0')).strip() == '1'
            and not is_neg
            and not is_pos
        )
        if is_neg and is_pos:
            conflict_dropped += 1
            continue
        sentiment = 'negative' if is_neg else ('positive' if is_pos else 'neutral')

        std_raw = str(tr.get('Standard Bangla', '')).strip()
        std_clean = clean_bengali_text(std_raw)
        if not std_clean:
            continue

        for raw_col, canonical_reg in region_col_map:
            dia_raw = str(tr.get(raw_col, '')).strip()
            dia_clean = clean_bengali_text(dia_raw)
            if not dia_clean or dia_clean.lower() == 'nan':
                continue
            records.append({
                'Standard_Text_Raw': std_raw,
                'Dialect_Text_Raw': dia_raw,
                'Standard_Text': std_clean,
                'Dialect_Text': dia_clean,
                'Sentiment': sentiment,
                'Dialect_Region': canonical_reg,
                'Source': 'ANUBHUTI_Corpus',
                'Is_Pure_Surprise': 1 if is_surp_only else 0,
                'Anubhuti_Row_Id': idx,
            })

    # 3. SAPTAK Manual Annotation (Include ALL 981 labeled sentences cleanly)
    sap_path = os.path.join(RAW_DIR, 'saptak_3dialects_labeled.csv')
    with open(sap_path, 'r', encoding='utf-8') as f:
        sap_rows = list(csv.DictReader(f))

    sap_col_map = [
        ('Sylhet_Text', 'Sylhet'),
        ('Noakhali_Text', 'Noakhali'),
        ('Mymensingh_Text', 'Mymensingh'),
    ]
    for r in sap_rows:
        sent = str(r.get('Sentiment', '')).strip().lower()
        if sent not in {'negative', 'neutral', 'positive'}:
            continue
        std_raw = str(r.get('Standard_Bangla', '')).strip()
        std_clean = clean_bengali_text(std_raw)
        if not std_clean:
            continue
        for raw_col, canonical_reg in sap_col_map:
            dia_raw = str(r.get(raw_col, '')).strip()
            dia_clean = clean_bengali_text(dia_raw)
            if not dia_clean:
                continue
            records.append({
                'Standard_Text_Raw': std_raw,
                'Dialect_Text_Raw': dia_raw,
                'Standard_Text': std_clean,
                'Dialect_Text': dia_clean,
                'Sentiment': sent,
                'Dialect_Region': canonical_reg,
                'Source': 'SAPTAK_Manual_Annotation',
                'Is_Pure_Surprise': 0,
                'Anubhuti_Row_Id': -1,
            })

    return records, conflict_dropped


def deduplicate_records(records):
    """Exact SHA-256 deduplication per (Dialect_Region, clean Dialect_Text).
    If identical text in the same dialect has conflicting sentiment labels, drop all conflicting copies.
    """
    by_key = defaultdict(list)
    for r in records:
        key_str = f"{r['Dialect_Region']}||{r['Dialect_Text']}"
        key_hash = hashlib.sha256(key_str.encode('utf-8')).hexdigest()
        r['dialect_text_sha256'] = key_hash[:16]
        by_key[key_hash].append(r)

    deduped = []
    exact_same_label_dropped = 0
    label_conflict_dropped = 0
    for key_hash, items in by_key.items():
        labels = set(x['Sentiment'] for x in items)
        if len(labels) > 1:
            label_conflict_dropped += len(items)
            continue
        deduped.append(items[0])
        exact_same_label_dropped += len(items) - 1

    # Compute canonical Standard_Text group_id
    std_group_regions = defaultdict(set)
    for r in deduped:
        gid = sha256_short(r['Standard_Text'])
        r['group_id'] = gid
        if r['Source'] == 'ANUBHUTI_Corpus':
            std_group_regions[gid].add(r['Dialect_Region'])

    for r in deduped:
        r['Is_Pure_4Dialect_Parallel'] = (
            1 if (r['Source'] == 'ANUBHUTI_Corpus' and len(std_group_regions[r['group_id']]) == 4) else 0
        )

    return deduped, exact_same_label_dropped, label_conflict_dropped


def assign_zero_leakage_group_splits(records, seed=SEED):
    """Deterministic Stratified Group Split (80/10/10) grouped strictly by group_id (clean Standard_Text)."""
    rng = random.Random(seed)
    groups = defaultdict(list)
    for r in records:
        groups[r['group_id']].append(r)

    # Stratum per group: (Source signature, Sentiment set, Dialect count bucket)
    strata = defaultdict(list)
    for gid, items in groups.items():
        sources = "+".join(sorted(set(x['Source'] for x in items)))
        sents = "+".join(sorted(set(x['Sentiment'] for x in items)))
        n_dial = len(set(x['Dialect_Region'] for x in items))
        strat_key = f"{sources}|{sents}|{n_dial}"
        strata[strat_key].append(gid)

    group_split = {}
    for skey in sorted(strata.keys()):
        gids = sorted(strata[skey])
        rng.shuffle(gids)
        n = len(gids)
        if n >= 10:
            n_test = max(1, round(n * 0.10))
            n_val = max(1, round(n * 0.10))
        elif n >= 3:
            n_test = 1
            n_val = 1
        elif n == 2:
            n_test = 1
            n_val = 0
        else:
            n_test = 0
            n_val = 0
        test_g = set(gids[:n_test])
        val_g = set(gids[n_test:n_test + n_val])
        train_g = set(gids[n_test + n_val:])
        for g in train_g:
            group_split[g] = 'train'
        for g in val_g:
            group_split[g] = 'val'
        for g in test_g:
            group_split[g] = 'test'

    for idx, r in enumerate(records):
        r['sample_id'] = f"TV2_{idx:05d}"
        r['split'] = group_split[r['group_id']]

    return records


def verify_zero_leakage(records):
    by_split = defaultdict(list)
    for r in records:
        by_split[r['split']].append(r)

    gids = {s: set(r['group_id'] for r in rs) for s, rs in by_split.items()}
    stds = {s: set(r['Standard_Text'] for r in rs) for s, rs in by_split.items()}
    dkeys = {s: set((r['Dialect_Region'], r['Dialect_Text']) for r in rs) for s, rs in by_split.items()}

    checks = {
        'group_id_train_test_overlap': len(gids['train'] & gids['test']),
        'group_id_train_val_overlap': len(gids['train'] & gids['val']),
        'group_id_val_test_overlap': len(gids['val'] & gids['test']),
        'std_text_train_test_overlap': len(stds['train'] & stds['test']),
        'dialect_pair_train_test_overlap': len(dkeys['train'] & dkeys['test']),
    }
    assert all(v == 0 for v in checks.values()), f"LEAKAGE DETECTED: {checks}"
    return checks


def generate_blind_iaa_sheet(records, n_samples=500, seed=SEED):
    """Create a 500-sample double-blind IAA audit file WITHOUT exposing Annotator_1 labels."""
    rng = random.Random(seed)
    strata = defaultdict(list)
    for r in records:
        strata[(r['Dialect_Region'], r['Source'], r['Sentiment'])].append(r)

    total = len(records)
    selected = []
    # Proportional stratified draw across Dialect x Source x Sentiment
    remainders = []
    for key in sorted(strata.keys()):
        pool = list(strata[key])
        rng.shuffle(pool)
        exact = (len(pool) / total) * n_samples
        take = int(exact)
        selected.extend(pool[:take])
        remainders.append((exact - take, key, pool[take:]))

    remainders.sort(reverse=True, key=lambda x: x[0])
    i = 0
    while len(selected) < n_samples and i < len(remainders):
        _, key, leftover = remainders[i]
        if leftover:
            selected.append(leftover[0])
        i += 1

    selected = selected[:n_samples]
    rng.shuffle(selected)

    blind_path = os.path.join(AUDIT_DIR, 'iaa_blind_500_for_annotator2.csv')
    key_path = os.path.join(AUDIT_DIR, 'iaa_ground_truth_key_500.csv')

    with open(blind_path, 'w', encoding='utf-8-sig', newline='') as fb, \
         open(key_path, 'w', encoding='utf-8', newline='') as fk:
        bw = csv.DictWriter(fb, fieldnames=[
            'audit_id', 'sample_id', 'Dialect_Region', 'Source',
            'Standard_Text', 'Dialect_Text',
            'Annotator_2_Sentiment', 'Translation_Fidelity_1to5', 'Auditor_Notes'
        ])
        kw = csv.DictWriter(fk, fieldnames=[
            'audit_id', 'sample_id', 'Dialect_Region', 'Source',
            'Standard_Text', 'Dialect_Text', 'Original_Sentiment'
        ])
        bw.writeheader()
        kw.writeheader()
        for k, r in enumerate(selected, start=1):
            aid = f"IAA_{k:03d}"
            bw.writerow({
                'audit_id': aid,
                'sample_id': r['sample_id'],
                'Dialect_Region': r['Dialect_Region'],
                'Source': r['Source'],
                'Standard_Text': r['Standard_Text'],
                'Dialect_Text': r['Dialect_Text'],
                'Annotator_2_Sentiment': '',
                'Translation_Fidelity_1to5': '',
                'Auditor_Notes': ''
            })
            kw.writerow({
                'audit_id': aid,
                'sample_id': r['sample_id'],
                'Dialect_Region': r['Dialect_Region'],
                'Source': r['Source'],
                'Standard_Text': r['Standard_Text'],
                'Dialect_Text': r['Dialect_Text'],
                'Original_Sentiment': r['Sentiment']
            })
    return blind_path, key_path


def main():
    print("=" * 72)
    print("BUILDING TALLIP V2 CLEAN BENCHMARK (ZERO-LEAKAGE GROUP SPLIT)")
    print("=" * 72)
    raw_records, anu_conflict = load_all_raw_sources()
    non_nfc_before = sum(1 for r in raw_records if not unicodedata.is_normalized('NFC', r['Dialect_Text_Raw']))
    deduped, same_dup_drop, lbl_conflict_drop = deduplicate_records(raw_records)
    assigned = assign_zero_leakage_group_splits(deduped, seed=SEED)
    leak_checks = verify_zero_leakage(assigned)

    out_csv = os.path.join(OUT_DIR, 'tallip_v2_clean_benchmark.csv')
    fieldnames = [
        'sample_id', 'group_id', 'dialect_text_sha256', 'split',
        'Dialect_Region', 'Sentiment', 'Source',
        'Is_Pure_4Dialect_Parallel', 'Is_Pure_Surprise',
        'Standard_Text', 'Dialect_Text',
        'Standard_Text_Raw', 'Dialect_Text_Raw'
    ]
    with open(out_csv, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in assigned:
            w.writerow({k: r[k] for k in fieldnames})

    blind_path, key_path = generate_blind_iaa_sheet(assigned, n_samples=500, seed=SEED)

    # Summarize audit statistics
    split_counts = Counter(r['split'] for r in assigned)
    reg_sent = Counter((r['Dialect_Region'], r['Sentiment']) for r in assigned)
    src_reg = Counter((r['Source'], r['Dialect_Region']) for r in assigned)
    src_sent = Counter((r['Source'], r['Sentiment']) for r in assigned)
    test_reg_sent = Counter((r['Dialect_Region'], r['Sentiment']) for r in assigned if r['split'] == 'test')
    par4_split = Counter(r['split'] for r in assigned if r['Is_Pure_4Dialect_Parallel'] == 1)

    audit = {
        'raw_loaded_rows': len(raw_records),
        'anubhuti_conflict_groups_dropped': anu_conflict,
        'non_nfc_raw_dialect_rows_normalized': non_nfc_before,
        'sha256_exact_duplicates_dropped': same_dup_drop,
        'sha256_label_conflict_rows_dropped': lbl_conflict_drop,
        'clean_total_rows': len(assigned),
        'unique_group_ids': len(set(r['group_id'] for r in assigned)),
        'split_counts': dict(split_counts),
        'pure_4dialect_parallel_split_counts': dict(par4_split),
        'leakage_verification': leak_checks,
        'region_x_sentiment': {f"{k[0]}_{k[1]}": v for k, v in sorted(reg_sent.items())},
        'test_region_x_sentiment': {f"{k[0]}_{k[1]}": v for k, v in sorted(test_reg_sent.items())},
        'source_x_region': {f"{k[0]}_{k[1]}": v for k, v in sorted(src_reg.items())},
        'source_x_sentiment': {f"{k[0]}_{k[1]}": v for k, v in sorted(src_sent.items())},
    }
    audit_json_path = os.path.join(OUT_DIR, 'tallip_v2_data_audit.json')
    with open(audit_json_path, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2)

    print(f"Raw Loaded Rows                : {len(raw_records):,}")
    print(f"Non-NFC Raw Dialect Rows Fixed : {non_nfc_before:,}")
    print(f"SHA-256 Exact Dups Removed     : {same_dup_drop:,}")
    print(f"SHA-256 Label Conflicts Removed: {lbl_conflict_drop:,}")
    print(f"Clean Benchmark Total Rows     : {len(assigned):,} (Groups: {audit['unique_group_ids']:,})")
    print(f"Splits (Train/Val/Test)        : {dict(split_counts)}")
    print(f"Pure 4-Dialect ANUBHUTI Splits : {dict(par4_split)}")
    print(f"Leakage Verification           : {leak_checks}")
    print("\nTest Set Per-Dialect Sentiment Supports:")
    for reg in ['Chattogram', 'Sylhet', 'Noakhali', 'Mymensingh']:
        c_n = test_reg_sent[(reg, 'negative')]
        c_z = test_reg_sent[(reg, 'neutral')]
        c_p = test_reg_sent[(reg, 'positive')]
        print(f"  {reg:<11}: Neg={c_n:<4} Neu={c_z:<4} Pos={c_p:<4} | Total={c_n+c_z+c_p}")
    print(f"\nSaved Clean CSV : {out_csv}")
    print(f"Saved Audit JSON: {audit_json_path}")
    print(f"Saved Blind IAA : {blind_path}")


if __name__ == '__main__':
    main()
