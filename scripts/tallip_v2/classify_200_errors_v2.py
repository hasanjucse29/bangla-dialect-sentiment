"""
Deterministic Linguistic Error Classifier for TALLIP V2 Stratified Error Audit (N=200)
======================================================================================
Reads `results/tallip_v2/error_audit_candidates_200.csv`, classifies every utterance
into one of four mutually exclusive linguistic categories using explicit,
reproducible lexical/morphological/subword rules, and writes
`results/tallip_v2/error_taxonomy_verified_200.csv`.
"""

import csv
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
IN_CSV = os.path.join(BASE_DIR, "results", "tallip_v2", "error_audit_candidates_200.csv")
OUT_CSV = os.path.join(BASE_DIR, "results", "tallip_v2", "error_taxonomy_verified_200.csv")

NEG_TOKENS_STD = {"না", "নয়", "নি", "নেই", "নাই", "ছাড়া", "বিনা"}
NEG_TOKENS_DIA = {"ন", "নঅ", "নঁ", "নাইক্যা", "নায়"}


def classify_error_row(row: dict) -> str:
    """Assign one of four reproducible linguistic error categories."""
    std_words = set(re.findall(r"[\u0980-\u09FF]+", row.get("Standard_Text", "")))
    dia_words = set(re.findall(r"[\u0980-\u09FF]+", row.get("Dialect_Text", "")))
    subwords = row.get("BanglaBERT_Subwords", "")
    ratio = float(row.get("Subword_Ratio", 1.0))
    hash_count = subwords.count("##")
    dia_text = row.get("Dialect_Text", "")

    # 1. Dialectal Negation Shift
    if (std_words & NEG_TOKENS_STD) or (dia_words & NEG_TOKENS_DIA):
        return "Dialectal_Negation_Shift"

    # 2. Contextual Sarcasm / Pragmatic Ambiguity
    if "?" in dia_text or "!" in dia_text or len(std_words) >= 12 or (ratio <= 1.22 and hash_count <= 2):
        return "Contextual_Sarcasm_Pragmatic"

    # 3. Subword Over-Segmentation Noise (strict > 1.60 keeps moderate 1.60 lexical swaps separate)
    if ratio > 1.60 or hash_count >= 5:
        return "Subword_Over_Segmentation_Noise"

    # 4. OOV Lexical Polarity Blindness
    return "OOV_Lexical_Polarity_Blindness"


def main():
    with open(IN_CSV, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if "Error_Category" not in fieldnames:
        fieldnames.append("Error_Category")

    for r in rows:
        r["Error_Category"] = classify_error_row(r)

    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Classified {len(rows)} rows -> {OUT_CSV}")


if __name__ == "__main__":
    main()
