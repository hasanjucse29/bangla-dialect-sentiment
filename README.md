# Subword Tokenization Alienation and Cross-Dialect Anchor Low-Rank Adaptation Across the Bangla Dialect Continuum

Official reproducibility repository for our ACM TALLIP Technical Note:

> **Subword Tokenization Alienation and Cross-Dialect Anchor Low-Rank Adaptation Across the Bangla Dialect Continuum**  
> Md Hasan Al Mamun*, Fatima Binte Aziz, Nadia Afrin Ritu, and Md. Musfique Anwar  
> Department of Computer Science and Engineering, Jahangirnagar University, Savar, Dhaka 1342, Bangladesh  
> (\*Corresponding author: `hasan.stu20195@juniv.edu`)

---

## 1. Overview & Key Findings

Pretrained Bengali transformer encoders (`BanglaBERT`, `mBERT`, and `XLM-RoBERTa`) achieve strong sentiment classification accuracy on formal Standard Bangla (*Shuddho*, $83.24 \pm 1.55\%$ Accuracy / $0.7887 \pm 0.0167$ Macro F1 for `BanglaBERT`) yet degrade substantially on unstandardized regional Bangla dialects ($74.26 \pm 0.61\%$ Accuracy / $0.6217 \pm 0.0132$ Macro F1 zero-shot). This repository provides the complete zero-overlap curation pipeline, multi-tokenizer diagnostics, multi-seed PEFT adaptation suite, error taxonomy audit, and 400 DPI figure generation scripts:

1. **Content-Grouped Zero-Overlap Benchmark (`16,865` records, `7,475` unique `Standard_Text` groups):** Harmonizes *Chattogram Sent*, *ANUBHUTI*, and *SAPTAK* (including manual three-class sentiment labels on the `981` underlying *SAPTAK* Standard Bangla sentences projected to Sylhet, Noakhali, and Mymensingh) with Unicode NFC normalization, SHA-256 deduplication, and `0.00%` cross-split exact-group overlap (`train = 13,491`, `val = 1,689`, `test = 1,685`).
2. **Multi-Tokenizer Fragmentation & Controlled Error Modeling:** Under official BUET normalization (`csebuetnlp/normalizer`, which improves `BanglaBERT` Stage 2 zero-shot Macro F1 by $+0.0578$ on seed $42$), Chattogram dialect inflections inflate corpus subword fertility by **$+48.61\%$** in `BanglaBERT` WordPiece ($1.1700 \rightarrow 1.7387$) and **$+40.45\%$** in `XLM-RoBERTa` SentencePiece ($1.7242 \rightarrow 2.4215$). Regional fertility correlates with zero-shot error ($r = 0.9907$, $R^2 = 0.9815$, $p = 0.0093$), and sentence-level logistic regression ($N = 1,685$) confirms that normalized edit distance ($\text{OR} = 7.28, p = 0.00012$) and subword fertility ($\text{OR} = 1.59, p = 0.0401$) significantly predict zero-shot error independently of length.
3. **Stage-1-Initialized Anchor LoRA (`r = 8, alpha = 32` on `W_Q, W_V`):** Updating **$887,811$ trainable parameters (`0.8004%` of `110,914,563` active weights)** on Chattogram ($n = 5,201$) reduces peak GPU VRAM by **$46.4\%$** ($1,174.0\text{ MB}$ vs.\ $2,190.6\text{ MB}$) and lifts three-seed pooled performance to **$80.57 \pm 0.60\%$ Accuracy / $0.7516 \pm 0.0081$ Macro F1** (McNemar net $+88$ fixes, $p = 9.17 \times 10^{-7}$), improving strictly unseen non-anchor accuracy from $81.26\%$ to $83.87\%$ and outperforming head-only tuning ($75.43\% / 0.6928$), raw-initialized LoRA ($77.56\% / 0.7173$), and Chattogram full fine-tuning ($78.72\% / 0.7248$).
4. **Controlled `4 x 4` Cross-Dialect Transfer Matrix & Cross-Backbone Generalization:** Evaluating all four dialects symmetrically as anchors across three seeds shows consistent positive non-anchor gains ($+2.61\%$ to $+3.23\%$ accuracy over Stage 2 baselines), generalizes to `mBERT` ($+0.0999$ Macro F1), and improves `XLM-RoBERTa` via learning-rate and initialization tuning ($0.4344 \rightarrow 0.6746$ Macro F1, seed $42$).

---

## 2. Repository Structure

```text
├── data/
│   └── tallip_v2/
│       ├── tallip_v2_clean_benchmark.csv        # Clean 16,865-record 4-dialect benchmark (0.00% group overlap)
│       └── tallip_v2_data_audit.json            # Deduplication, NFC normalization, & split verification report
├── notebooks/
│   └── TALLIP_V2_Master_Experiments.ipynb       # Complete multi-seed Colab/A100 experimental pipeline
├── results/
│   └── tallip_v2/
│       ├── MASTER_TALLIP_V2_RESULTS.json        # All 3-seed metrics, 95% CIs, McNemar tests, VRAM & timing logs
│       ├── error_taxonomy_verified_200.csv      # 200-sample stratified Stage 2 error taxonomy & LoRA fixes
│       └── utterance_diagnostics.csv            # Utterance-level fertility, edit distance, & length diagnostics
├── scripts/
│   └── tallip_v2/
│       ├── build_clean_v2_dataset.py            # Reproducible dataset harmonization, NFC, dedup & group splitting
│       ├── build_tallip_v2_notebook.py          # Deterministic generator for TALLIP_V2_Master_Experiments.ipynb
│       ├── classify_200_errors_v2.py            # Deterministic 4-way linguistic error taxonomy classifier
│       └── generate_tallip_v2_figures.py        # Publication-grade 400 DPI colorblind-safe figure generator
├── requirements.txt                             # Python package dependencies
├── LICENSE                                      # CC BY 4.0 data/annotations & MIT code license
└── README.md
```

---

## 3. Source Corpora & Licensing

The clean benchmark (`16,865` rows: `13,491` train / `1,689` validation / `1,685` test) harmonizes three publicly accessible academic corpora:

- **Chattogram Sent** — Uddin et al. (2025), Mendeley Data V1 (`doi:10.17632/k6hts2ktxw.1`): `4,030` Chatgaiya–Standard pairs with native 3-class sentiment labels.
- **ANUBHUTI** — Kundu et al. (2025), `arXiv:2506.21686`: `9,892` parallel 4-dialect utterances deterministically mapped from 7 Ekman emotions to 3 sentiment polarities.
- **SAPTAK** — Ullah et al. (2026), Mendeley Data V1 (`doi:10.17632/v9cf66fk2t.1`): `2,943` aligned Sylhet, Noakhali, and Mymensingh pairs (`981` per dialect) with manual 3-class sentiment labels on the `981` Standard Bangla source sentences.

All curation scripts, deduplicated splits, manual *SAPTAK* source sentiment annotations, and audit logs in this repository are released under **Creative Commons Attribution 4.0 International (CC BY 4.0)** (code under **MIT License**), subject to the original terms of the underlying source datasets.

---

## 4. Reproducing the Results

### Step 1: Environment Setup
```bash
pip install -r requirements.txt
pip install git+https://github.com/csebuetnlp/normalizer
```

### Step 2: Re-run Multi-Seed Experiments (A100 GPU Recommended)
Open and run `notebooks/TALLIP_V2_Master_Experiments.ipynb` (reproducible across seeds `{42, 101, 2026}` with automatic JSON checkpoint caching).

### Step 3: Re-generate Publication Figures & Error Taxonomy
```bash
python scripts/tallip_v2/classify_200_errors_v2.py
python scripts/tallip_v2/generate_tallip_v2_figures.py
```

---

## 5. Citation

If you use this benchmark split, error taxonomy, or adaptation pipeline, please cite:

```bibtex
@article{Mamun_2026_TALLIP,
  author  = {Mamun, Md Hasan Al and Aziz, Fatima Binte and Ritu, Nadia Afrin and Anwar, Md. Musfique},
  title   = {Subword Tokenization Alienation and Cross-Dialect Anchor Low-Rank Adaptation Across the Bangla Dialect Continuum},
  journal = {ACM Transactions on Asian and Low-Resource Language Information Processing (TALLIP)},
  year    = {2026},
  note    = {Submitted}
}
```
