"""
Publication-Grade 400 DPI Luminance-Ordered & Grayscale-Safe Figure Generator (TALLIP V2)
=========================================================================================
Reads directly from `results/tallip_v2/MASTER_TALLIP_V2_RESULTS.json` and exports:
  1. `manuscripts/01_TALLIP_Short_Note/figures/fig_multi_tokenizer_fragmentation.{png,pdf}`
     - Panel (a): BUET-Normalized Corpus Subword Fertility Inflation (%) across dialects
     - Panel (b): Multivariate Sentence-Level Logistic Regression Odds Ratios (N=1,685)
  2. `manuscripts/01_TALLIP_Short_Note/figures/fig_per_dialect_transfer_matrix.{png,pdf}`
     - Panel (a): 4x4+Pooled Cross-Dialect Anchor Transfer Heatmap (Stage 1 -> LoRA, 3-seed mean)
     - Panel (b): Macro F1 (+/- 1 SD) Across Adaptation Paradigms & Ablation Controls
"""

import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
MASTER_JSON = os.path.join(BASE_DIR, "results", "tallip_v2", "MASTER_TALLIP_V2_RESULTS.json")
FIG_DIR = os.path.join(BASE_DIR, "manuscripts", "01_TALLIP_Short_Note", "figures")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "mathtext.fontset": "stix",
    "font.size": 9.5,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 9.5,
    "axes.edgecolor": "#1F2937",
    "axes.linewidth": 0.9,
    "xtick.labelsize": 8.8,
    "ytick.labelsize": 8.8,
    "legend.fontsize": 8.2,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

REGIONS = ["Chattogram", "Sylhet", "Noakhali", "Mymensingh"]


def make_figure1_fragmentation_and_logit(data: dict):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.6), gridspec_kw={"width_ratios": [1.15, 1.0]})

    # --- Panel (a): BUET-Normalized Corpus Fertility Delta (%) ---
    buet = data["tokenizer_diagnostics"]["buet_norm"]
    toks = [
        ("BanglaBERT", "BanglaBERT (WordPiece)", "#1E3A5F"),
        ("XLM-RoBERTa", "XLM-RoBERTa (SentencePiece)", "#5B8DBE"),
        ("mBERT", "mBERT (WordPiece)", "#CBD5E1"),
    ]
    x = np.arange(len(REGIONS)) * 1.08
    w = 0.27

    for idx, (m_key, label, color) in enumerate(toks):
        vals = [buet[m_key][r]["corpus_delta_pct"] for r in REGIONS]
        offset = (idx - 1) * w
        bars = ax1.bar(
            x + offset,
            vals,
            width=w,
            color=color,
            edgecolor="#1F2937",
            linewidth=0.75,
            label=label,
            zorder=3,
        )
        for r_idx, (b, v) in enumerate(zip(bars, vals)):
            # Stagger slightly at Mymensingh where BanglaBERT (16.46%) and XLM-R (16.61%) are identical height
            y_off = 2.6 if (r_idx == 3 and idx == 1) else 0.85
            ax1.text(
                b.get_x() + b.get_width() / 2.0,
                v + y_off,
                f"+{v:.1f}%",
                ha="center",
                va="bottom",
                fontsize=6.9,
                fontweight="bold" if idx == 0 else "normal",
                color="#111827",
            )

    ax1.set_xticks(x)
    ax1.set_xticklabels(REGIONS, fontweight="bold")
    ax1.set_ylabel(r"Corpus Subword Fertility Inflation $\Delta F_{\mathrm{corpus}}$ (%)")
    ax1.set_ylim(0, 57)
    ax1.grid(axis="y", linestyle="--", alpha=0.55, color="#CBD5E1", zorder=0)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.set_title("(a) Multi-Tokenizer Over-Segmentation Surge (BUET-Norm)")
    ax1.legend(loc="upper right", frameon=True, edgecolor="#CBD5E1", facecolor="white")

    # --- Panel (b): Multivariate Sentence-Level Logistic Regression Odds Ratios ---
    logit = data["sentence_level_logit"]
    predictors = [
        ("norm_edit_dist", r"Norm. Edit Distance ($\delta_{\mathrm{orth}}$)", True),
        ("C(Source)[T.SAPTAK_Manual_Annotation]", "Source: SAPTAK vs ANUBHUTI", True),
        ("C(Source)[T.Original_Chattogram_Dataset]", "Source: Chatgaiya vs ANUBHUTI", True),
        ("fert_bb_buet", "Subword Fertility (BanglaBERT)", True),
        ("word_count", "Utterance Word Count", False),
        ("C(Dialect_Region)[T.Mymensingh]", "Region: Mymensingh vs Chat.", False),
        ("C(Dialect_Region)[T.Sylhet]", "Region: Sylhet vs Chat.", False),
        ("C(Dialect_Region)[T.Noakhali]", "Region: Noakhali vs Chat.", False),
    ]
    predictors = list(reversed(predictors))
    y_pos = np.arange(len(predictors))
    ors = [logit[k]["odds_ratio"] for k, _, _ in predictors]
    pvals = [logit[k]["p_value"] for k, _, _ in predictors]
    labels = [lbl for _, lbl, _ in predictors]
    sig_flags = [sig for _, _, sig in predictors]

    bar_colors = ["#2C5282" if s else "#F1F5F9" for s in sig_flags]
    bar_edges = ["#1F2937" if s else "#475569" for s in sig_flags]

    ax2.axvline(1.0, color="#475569", linestyle="--", linewidth=1.15, zorder=2)
    ax2.barh(
        y_pos,
        ors,
        height=0.58,
        color=bar_colors,
        edgecolor=bar_edges,
        linewidth=0.75,
        zorder=3,
    )

    for yp, ov, pv in zip(y_pos, ors, pvals):
        p_txt = f"p={pv:.4f}" if pv >= 0.001 else f"p={pv:.1e}"
        sig_mark = "*" if pv < 0.05 else "n.s."
        if pv < 0.001:
            sig_mark = "***"
        x_txt = max(ov, 1.02) * 1.12
        ax2.text(
            x_txt,
            yp,
            f"OR={ov:.2f} ({p_txt}, {sig_mark})",
            va="center",
            ha="left",
            fontsize=7.3,
            fontweight="bold" if pv < 0.05 else "normal",
            color="#111827",
        )

    ax2.set_xscale("log")
    ax2.set_xlim(0.55, 72.0)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.set_xlabel("Odds Ratio for Stage 2 Zero-Shot Error (Log Scale)")
    ax2.grid(axis="x", linestyle=":", alpha=0.55, color="#CBD5E1", zorder=0)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_title("(b) Sentence-Level Logit Odds Ratios (N=1,685; Polarity Ctrl.)")
    legend_handles = [
        Patch(facecolor="#2C5282", edgecolor="#1F2937", linewidth=0.75, label="Significant (p < 0.05)"),
        Patch(facecolor="#F1F5F9", edgecolor="#475569", linewidth=0.75, label="Non-significant (n.s.)"),
    ]
    ax2.legend(handles=legend_handles, loc="lower right", frameon=True, edgecolor="#CBD5E1", facecolor="white", fontsize=7.8)

    fig.tight_layout(w_pad=2.4)
    os.makedirs(FIG_DIR, exist_ok=True)
    for ext in ("png", "pdf"):
        out_p = os.path.join(FIG_DIR, f"fig_multi_tokenizer_fragmentation.{ext}")
        fig.savefig(out_p, dpi=400, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def make_figure2_transfer_matrix(data: dict):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.9), gridspec_kw={"width_ratios": [1.02, 1.28]})

    # --- Panel (a): 4x4 + Pooled Directional Anchor Transfer Heatmap (Stage 1 -> LoRA, 3-seed Mean) ---
    mat_data = data["transfer_4x4_stage1_lora"]
    target_cols = REGIONS + ["Pooled"]
    acc_mat = np.zeros((4, 5), dtype=float)
    f1_mat = np.zeros((4, 5), dtype=float)
    anchor_ns = {}

    for i, src in enumerate(REGIONS):
        skeys = ["s42", "s101", "s2026"]
        anchor_ns[src] = mat_data[src]["s42"]["train_n"]
        for j, tgt in enumerate(target_cols):
            if tgt == "Pooled":
                accs = [mat_data[src][s]["eval"]["pooled"]["accuracy"] * 100 for s in skeys]
                f1s = [mat_data[src][s]["eval"]["pooled"]["macro_f1"] for s in skeys]
            else:
                accs = [mat_data[src][s]["eval"]["per_dialect"][tgt]["accuracy"] * 100 for s in skeys]
                f1s = [mat_data[src][s]["eval"]["per_dialect"][tgt]["macro_f1"] for s in skeys]
            acc_mat[i, j] = np.mean(accs)
            f1_mat[i, j] = np.mean(f1s)

    academic_blues = LinearSegmentedColormap.from_list(
        "academic_blues", ["#F8FAFC", "#DBEAFE", "#93C5FD", "#3B72A8", "#162E4D"]
    )
    ax1.imshow(acc_mat, cmap=academic_blues, vmin=62.0, vmax=89.0, aspect="auto")
    ax1.set_xticks(np.arange(5))
    ax1.set_xticklabels(["Chat.", "Sylhet", "Noak.", "Mym.", "Pooled"], fontweight="bold")
    ax1.set_yticks(np.arange(4))
    ax1.set_yticklabels([f"{r}\n(n={anchor_ns[r]:,})" for r in REGIONS], fontweight="bold")
    ax1.set_xlabel("Zero-Shot Evaluation Target")
    ax1.set_ylabel("LoRA Source Anchor")
    ax1.set_title("(a) 4×4 Cross-Dialect Transfer Matrix (3-Seed Mean)")

    # Separator before Pooled column
    ax1.axvline(3.5, color="#0F172A", linewidth=1.5, linestyle="-")
    for i in range(4):
        for j in range(5):
            av = acc_mat[i, j]
            fv = f1_mat[i, j]
            txt_color = "white" if av >= 78.0 else "#0F172A"
            is_diag = (i == j)
            weight = "bold" if (is_diag or j == 4) else "normal"
            ax1.text(
                j,
                i,
                f"{av:.2f}%\n({fv:.3f})",
                ha="center",
                va="center",
                fontsize=7.9,
                fontweight=weight,
                color=txt_color,
            )
            if is_diag:
                edge_col = "white" if av >= 78.0 else "#0F172A"
                rect = plt.Rectangle(
                    (j - 0.45, i - 0.45), 0.90, 0.90,
                    fill=False, edgecolor=edge_col, linewidth=1.6, linestyle="-"
                )
                ax1.add_patch(rect)

    # --- Panel (b): Adaptation & Control Comparison (Macro F1 +/- 1 SD across 3 seeds) ---
    seeds = [42, 101, 2026]
    methods = [
        ("Stage 2 Zero-Shot", lambda s: data["stage1_stage2_multi_seed"]["BanglaBERT"][f"seed_{s}"]["stage2"]["eval"], "#FFFFFF"),
        ("Stage 1 → Head-Only", lambda s: data["stage4_peft_controls_and_xlmr_sweep"][f"bb_s1_head_only_s{s}"]["eval"], "#D1D5DB"),
        ("Raw → Anchor LoRA", lambda s: data["stage4_peft_controls_and_xlmr_sweep"][f"bb_raw_lora_s{s}"]["eval"], "#8EAAC4"),
        ("Chattogram Full-FT", lambda s: data["stage3_upper_bounds_and_canine"]["anchor_chattogram_full_ft"][f"BanglaBERT_s{s}"]["eval"], "#46739E"),
        ("Stage 1 → Anchor LoRA", lambda s: data["stage4_peft_controls_and_xlmr_sweep"][f"bb_s1_lora_s{s}"]["eval"], "#162E4D"),
    ]

    eval_splits = ["Chattogram", "Sylhet", "Noakhali", "Mymensingh", "Pooled"]
    x2 = np.arange(len(eval_splits))
    w2 = 0.165

    for idx, (m_name, getter, col) in enumerate(methods):
        means, sds = [], []
        for sp in eval_splits:
            vals = []
            for s in seeds:
                ev = getter(s)
                if sp == "Pooled":
                    vals.append(ev["pooled"]["macro_f1"])
                else:
                    vals.append(ev["per_dialect"][sp]["macro_f1"])
            means.append(float(np.mean(vals)))
            sds.append(float(np.std(vals, ddof=1)))

        offset = (idx - 2.0) * w2
        ax2.bar(
            x2 + offset,
            means,
            yerr=sds,
            width=w2,
            color=col,
            edgecolor="#1F2937",
            linewidth=0.75,
            capsize=2.0,
            error_kw={"elinewidth": 0.9, "ecolor": "#1F2937"},
            label=m_name,
            zorder=3,
        )

    ax2.set_xticks(x2)
    ax2.set_xticklabels(["Chat.\n(Anchor)", "Sylhet\n(0-Shot)", "Noak.\n(0-Shot)", "Mym.\n(0-Shot)", "Pooled\n(All 4)"], fontweight="bold")
    ax2.set_ylabel("Macro F1 Score (Mean ± SD, 3 Seeds)")
    ax2.set_ylim(0.45, 0.89)
    ax2.grid(axis="y", linestyle="--", alpha=0.55, color="#CBD5E1", zorder=0)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.set_title("(b) Controlled Ablations & Zero-Shot Transfer (BanglaBERT)")
    ax2.legend(loc="upper left", ncol=2, frameon=True, edgecolor="#CBD5E1", facecolor="white", fontsize=7.5)

    fig.tight_layout(w_pad=2.4)
    os.makedirs(FIG_DIR, exist_ok=True)
    for ext in ("png", "pdf"):
        out_p = os.path.join(FIG_DIR, f"fig_per_dialect_transfer_matrix.{ext}")
        fig.savefig(out_p, dpi=400, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    make_figure1_fragmentation_and_logit(data)
    make_figure2_transfer_matrix(data)
    print("Generated 400 DPI V2 luminance-ordered/grayscale-safe figures in:", FIG_DIR)


if __name__ == "__main__":
    main()
