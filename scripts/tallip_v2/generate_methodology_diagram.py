"""
Generate Editable draw.io (.drawio) XML and Matching 400 DPI Publication Diagram
================================================================================
Creates:
  1. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.drawio
     (Standard diagrams.net mxGraphModel XML - directly editable in draw.io)
  2. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.png (400 DPI)
  3. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.pdf (Vector)
  4. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.svg (Vector)
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
FIG_DIR = os.path.join(BASE_DIR, "manuscripts", "01_TALLIP_Short_Note", "figures")

PALETTE = {
    "lane1_bg": "#f0f6fc", "lane1_bd": "#6c8ebf", "lane1_hdr": "#1f4e79",
    "lane2_bg": "#fff9e6", "lane2_bd": "#d6b656", "lane2_hdr": "#7f6000",
    "lane3_bg": "#edf7ed", "lane3_bd": "#82b366", "lane3_hdr": "#274e13",
    "lane4_bg": "#f5eef8", "lane4_bd": "#9673a6", "lane4_hdr": "#4c1130",
    "box_blue_bg": "#dae8fc", "box_blue_bd": "#6c8ebf",
    "box_amber_bg": "#fff2cc", "box_amber_bd": "#d6b656",
    "box_red_bg": "#f8cecc", "box_red_bd": "#b85450",
    "box_green_bg": "#d5e8d4", "box_green_bd": "#82b366",
    "box_purple_bg": "#e1d5e7", "box_purple_bd": "#9673a6",
    "box_gray_bg": "#f5f5f5", "box_gray_bd": "#666666",
}


def write_drawio_xml(out_path: str):
    """Write a genuine, directly editable draw.io (diagrams.net) XML file."""
    xml = """<mxfile host="app.diagrams.net" modified="2026-11-26T07:35:00.000Z" agent="TALLIP-V2-Generator" version="24.7.17" type="device">
  <diagram id="tallip-v2-workflow" name="End-to-End Methodology">
    <mxGraphModel dx="1420" dy="760" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="620" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Swimlane 1: Data Curation -->
        <mxCell id="lane1" value="1. Zero-Overlap Data Curation" style="swimlane;whiteSpace=wrap;html=1;rounded=1;arcSize=8;fillColor=#f0f6fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=13;fontColor=#1f4e79;startSize=32;strokeWidth=1.8;" vertex="1" parent="1">
          <mxGeometry x="20" y="20" width="320" height="560" as="geometry" />
        </mxCell>
        <mxCell id="n1_1" value="&lt;b&gt;Three Public Regional Corpora&lt;/b&gt;&lt;br/&gt;• Chattogram Sent (4,030 native)&lt;br/&gt;• ANUBHUTI (9,892; 7 emotions -&amp;gt; 3-class)&lt;br/&gt;• SAPTAK (2,943; 981 manual Std labels)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane1">
          <mxGeometry x="15" y="50" width="290" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n1_2" value="&lt;b&gt;Canonical Cleaning &amp;amp; Deduplication&lt;/b&gt;&lt;br/&gt;• Unicode NFC (8,341 fixed)&lt;br/&gt;• Drop 23 conflict groups + 436 SHA-256 dups&lt;br/&gt;• Clean Total: &lt;b&gt;16,865 rows&lt;/b&gt; (7,475 groups)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane1">
          <mxGeometry x="15" y="190" width="290" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n1_3" value="&lt;b&gt;Group-Stratified 80 / 10 / 10 Split&lt;/b&gt;&lt;br/&gt;Keyed strictly on Standard_Text hash&lt;br/&gt;• Train: 13,491 | Val: 1,689 | Test: 1,685&lt;br/&gt;• &lt;b&gt;0.00% exact-group overlap&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane1">
          <mxGeometry x="15" y="330" width="290" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n1_4" value="&lt;b&gt;Model-Specific Preprocessing&lt;/b&gt;&lt;br/&gt;• BanglaBERT: csebuetnlp/normalizer&lt;br/&gt;• mBERT / XLM-R / CANINE-C: NFC text" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane1">
          <mxGeometry x="15" y="465" width="290" height="75" as="geometry" />
        </mxCell>
        <mxCell id="e1_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane1" source="n1_1" target="n1_2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e1_2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane1" source="n1_2" target="n1_3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e1_3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane1" source="n1_3" target="n1_4"><mxGeometry relative="1" as="geometry" /></mxCell>

        <!-- Swimlane 2: RQ1 Diagnostics -->
        <mxCell id="lane2" value="2. RQ1: Tokenization &amp; Error Audit" style="swimlane;whiteSpace=wrap;html=1;rounded=1;arcSize=8;fillColor=#fff9e6;strokeColor=#d6b656;fontStyle=1;fontSize=13;fontColor=#7f6000;startSize=32;strokeWidth=1.8;" vertex="1" parent="1">
          <mxGeometry x="370" y="20" width="320" height="560" as="geometry" />
        </mxCell>
        <mxCell id="n2_1" value="&lt;b&gt;Multi-Tokenizer Fertility Profiling&lt;/b&gt;&lt;br/&gt;• BanglaBERT WP: Chat. &lt;b&gt;+48.61%&lt;/b&gt;&lt;br/&gt;• XLM-R SP: Chat. &lt;b&gt;+40.45%&lt;/b&gt; | mBERT: +19.36%&lt;br/&gt;• Hierarchy: Mym &amp;lt; Noak &amp;lt; Sylh &amp;lt;&amp;lt; Chat." style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane2">
          <mxGeometry x="15" y="50" width="290" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n2_2" value="&lt;b&gt;Stage 1 -&amp;gt; Stage 2 Zero-Shot Drop&lt;/b&gt;&lt;br/&gt;• Stage 1 Standard FT: 83.24% / 0.7887 F1&lt;br/&gt;• Stage 2 Dialect Zero-Shot: 74.26% / 0.6217&lt;br/&gt;• BUET Normalizer: &lt;b&gt;+0.0578 F1&lt;/b&gt; (seed 42)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#d6b656;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane2">
          <mxGeometry x="15" y="190" width="290" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n2_3" value="&lt;b&gt;Controlled Error Modeling (N=1,685)&lt;/b&gt;&lt;br/&gt;• Macro fit: r=0.9907 (s42) | r=0.9942 (3-seed)&lt;br/&gt;• Logit Edit Dist: &lt;b&gt;OR=7.28&lt;/b&gt; (p=1.2e-4)&lt;br/&gt;• Logit Fertility: &lt;b&gt;OR=1.59&lt;/b&gt; (p=0.0401)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane2">
          <mxGeometry x="15" y="330" width="290" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n2_4" value="&lt;b&gt;200-Sample 4-Way Error Taxonomy&lt;/b&gt;&lt;br/&gt;Subword 29.5% (55.9% fixed) | OOV 28.0%&lt;br/&gt;Pragmatic 27.5% | Negation Shift 15.0%" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane2">
          <mxGeometry x="15" y="465" width="290" height="75" as="geometry" />
        </mxCell>
        <mxCell id="e2_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane2" source="n2_1" target="n2_2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e2_2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane2" source="n2_2" target="n2_3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e2_3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane2" source="n2_3" target="n2_4"><mxGeometry relative="1" as="geometry" /></mxCell>

        <!-- Swimlane 3: RQ2 Stage-1 Anchor LoRA -->
        <mxCell id="lane3" value="3. RQ2: Stage-1-Initialized Anchor LoRA" style="swimlane;whiteSpace=wrap;html=1;rounded=1;arcSize=8;fillColor=#edf7ed;strokeColor=#82b366;fontStyle=1;fontSize=13;fontColor=#274e13;startSize=32;strokeWidth=1.8;" vertex="1" parent="1">
          <mxGeometry x="720" y="20" width="390" height="560" as="geometry" />
        </mxCell>
        <mxCell id="n3_1" value="&lt;b&gt;Stage 1 Canonical Checkpoint (W_S1)&lt;/b&gt;&lt;br/&gt;Fine-tuned on Standard Bangla (n=13,491; 3 ep, lr=2e-5)&lt;br/&gt;Preserves formal sentiment decision geometry" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane3">
          <mxGeometry x="15" y="50" width="360" height="80" as="geometry" />
        </mxCell>
        <mxCell id="n3_2" value="&lt;b&gt;Frozen Backbone&lt;/b&gt;&lt;br/&gt;12 Layers Locked&lt;br/&gt;110.0M (99.20%)&lt;br/&gt;Zero grad states" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;dashed=1;dashPattern=6 4;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.5;" vertex="1" parent="lane3">
          <mxGeometry x="15" y="160" width="172" height="115" as="geometry" />
        </mxCell>
        <mxCell id="n3_3" value="&lt;b&gt;Trainable LoRA&lt;/b&gt;&lt;br/&gt;Q &amp;amp; V (r=8, alpha=32)&lt;br/&gt;h = W_S1 x + 4 BAx&lt;br/&gt;294,912 (0.27%)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.5;" vertex="1" parent="lane3">
          <mxGeometry x="203" y="160" width="172" height="115" as="geometry" />
        </mxCell>
        <mxCell id="n3_4" value="&lt;b&gt;Unfrozen Head + Single-Anchor Adaptation&lt;/b&gt;&lt;br/&gt;• Classifier Head: 592,899 (0.53%) -&amp;gt; Total &lt;b&gt;0.8004%&lt;/b&gt; of 110.9M&lt;br/&gt;• Trained on 1 anchor (Chat. n=5,201; 5 ep, lr=3e-4)&lt;br/&gt;• Anchor-only val checkpointing (unseen targets isolated)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.5;" vertex="1" parent="lane3">
          <mxGeometry x="15" y="310" width="360" height="125" as="geometry" />
        </mxCell>
        <mxCell id="n3_5" value="&lt;b&gt;Matched GPU Efficiency:&lt;/b&gt; 1,174 MB VRAM (-46.4% vs. Full-FT) | 82.2 s" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=10.5;strokeWidth=1.3;" vertex="1" parent="lane3">
          <mxGeometry x="15" y="465" width="360" height="75" as="geometry" />
        </mxCell>
        <mxCell id="e3_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane3" source="n3_1" target="n3_2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3_2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane3" source="n3_1" target="n3_3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3_3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane3" source="n3_2" target="n3_4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3_4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane3" source="n3_3" target="n3_4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e3_5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane3" source="n3_4" target="n3_5"><mxGeometry relative="1" as="geometry" /></mxCell>

        <!-- Swimlane 4: Evaluation & Controls -->
        <mxCell id="lane4" value="4. Controlled 4×4 Evaluation" style="swimlane;whiteSpace=wrap;html=1;rounded=1;arcSize=8;fillColor=#f5eef8;strokeColor=#9673a6;fontStyle=1;fontSize=13;fontColor=#4c1130;startSize=32;strokeWidth=1.8;" vertex="1" parent="1">
          <mxGeometry x="1140" y="20" width="340" height="560" as="geometry" />
        </mxCell>
        <mxCell id="n4_1" value="&lt;b&gt;Fair PEFT &amp;amp; Architecture Controls&lt;/b&gt;&lt;br/&gt;• Head-Only: 75.43% / 0.6928 F1&lt;br/&gt;• Raw -&amp;gt; LoRA: 77.56% / 0.7173 F1&lt;br/&gt;• Chat. Full-FT: 78.72% / 0.7248 F1&lt;br/&gt;• CANINE-C (pooled): 71.04% / 0.6559" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#9673a6;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane4">
          <mxGeometry x="15" y="50" width="310" height="115" as="geometry" />
        </mxCell>
        <mxCell id="n4_2" value="&lt;b&gt;3-Seed Stage 1 -&amp;gt; Anchor LoRA (Ours)&lt;/b&gt;&lt;br/&gt;• Pooled: &lt;b&gt;80.57 ± 0.60% Acc / 0.7516 F1&lt;/b&gt;&lt;br/&gt;• Unseen Non-Anchor: &lt;b&gt;83.87%&lt;/b&gt; (+2.61)&lt;br/&gt;• McNemar vs. S2: &lt;b&gt;+88 fixes&lt;/b&gt; (p=9.17e-7)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.6;" vertex="1" parent="lane4">
          <mxGeometry x="15" y="195" width="310" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n4_3" value="&lt;b&gt;4×4 Baseline-Gain Transfer Matrix&lt;/b&gt;&lt;br/&gt;All 4 dialects evaluated as single anchors:&lt;br/&gt;• Largest gain in-domain (+12.20 Chat.)&lt;br/&gt;• Unseen non-anchor: &lt;b&gt;+2.61 to +3.23 pts&lt;/b&gt;" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#9673a6;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane4">
          <mxGeometry x="15" y="330" width="310" height="105" as="geometry" />
        </mxCell>
        <mxCell id="n4_4" value="&lt;b&gt;Cross-Backbone Verification&lt;/b&gt;&lt;br/&gt;• mBERT S1-&amp;gt;LoRA: &lt;b&gt;+0.0999 F1&lt;/b&gt; (3 seeds)&lt;br/&gt;• XLM-R sweep: 0.4344 -&amp;gt; &lt;b&gt;0.6746 F1&lt;/b&gt; (s42)" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;align=left;spacingLeft=8;strokeWidth=1.4;" vertex="1" parent="lane4">
          <mxGeometry x="15" y="465" width="310" height="75" as="geometry" />
        </mxCell>
        <mxCell id="e4_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane4" source="n4_1" target="n4_2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e4_2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane4" source="n4_2" target="n4_3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="e4_3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2d3748;strokeWidth=1.5;" edge="1" parent="lane4" source="n4_3" target="n4_4"><mxGeometry relative="1" as="geometry" /></mxCell>

        <!-- Inter-lane connectors -->
        <mxCell id="c12" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1f4e79;strokeWidth=2.0;" edge="1" parent="1" source="lane1" target="lane2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="c23" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#7f6000;strokeWidth=2.0;" edge="1" parent="1" source="lane2" target="lane3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="c34" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#274e13;strokeWidth=2.0;" edge="1" parent="1" source="lane3" target="lane4"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)


def draw_box(ax, x, y, w, h, title, lines, bg, bd, title_color="#111827", dashed=False, lw=1.25):
    ls = (0, (4, 3)) if dashed else "-"
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.14",
        facecolor=bg, edgecolor=bd, linewidth=lw, linestyle=ls, zorder=3
    )
    ax.add_patch(box)
    ax.text(
        x + 0.14, y + h - 0.16, title,
        ha="left", va="top", fontsize=8.0, fontweight="bold",
        color=title_color, family="DejaVu Sans", zorder=4
    )
    line_y = y + h - 0.44
    step = (h - 0.52) / max(1, len(lines))
    for ln in lines:
        ax.text(
            x + 0.14, line_y, ln,
            ha="left", va="top", fontsize=6.9,
            color="#1f2937", family="DejaVu Sans", zorder=4
        )
        line_y -= min(step, 0.27)


def draw_lane(ax, x, y, w, h, header, bg, bd, hdr_bg):
    outer = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.18",
        facecolor=bg, edgecolor=bd, linewidth=1.6, zorder=1
    )
    ax.add_patch(outer)
    hdr_h = 0.46
    hdr = FancyBboxPatch(
        (x, y + h - hdr_h), w, hdr_h,
        boxstyle="round,pad=0.0,rounding_size=0.14",
        facecolor=hdr_bg, edgecolor=bd, linewidth=1.2, zorder=2
    )
    ax.add_patch(hdr)
    ax.text(
        x + w / 2.0, y + h - hdr_h / 2.0, header,
        ha="center", va="center", fontsize=8.6, fontweight="bold",
        color="white", family="DejaVu Sans", zorder=3
    )


def arrow(ax, x1, y1, x2, y2, color="#2d3748", lw=1.4):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=11,
        color=color, linewidth=lw, zorder=5
    )
    ax.add_patch(a)


def render_diagram():
    fig, ax = plt.subplots(figsize=(15.4, 5.9))
    ax.set_xlim(0, 17.2)
    ax.set_ylim(0, 6.45)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    lanes = [
        (0.15, 0.15, 3.70, 6.15, "1. Zero-Overlap Data Curation", PALETTE["lane1_bg"], PALETTE["lane1_bd"], PALETTE["lane1_hdr"]),
        (4.20, 0.15, 3.75, 6.15, "2. RQ1: Tokenization & Error Audit", PALETTE["lane2_bg"], PALETTE["lane2_bd"], PALETTE["lane2_hdr"]),
        (8.30, 0.15, 4.55, 6.15, "3. RQ2: Stage-1-Initialized Anchor LoRA", PALETTE["lane3_bg"], PALETTE["lane3_bd"], PALETTE["lane3_hdr"]),
        (13.20, 0.15, 3.85, 6.15, "4. Controlled 4x4 Evaluation", PALETTE["lane4_bg"], PALETTE["lane4_bd"], PALETTE["lane4_hdr"]),
    ]
    for lx, ly, lw, lh, ltitle, lbg, lbd, lhdr in lanes:
        draw_lane(ax, lx, ly, lw, lh, ltitle, lbg, lbd, lhdr)

    # Lane 1
    x1, w1 = 0.30, 3.40
    draw_box(ax, x1, 4.35, w1, 1.28, "Three Public Regional Corpora", [
        "• Chattogram Sent: 4,030 native pairs",
        "• ANUBHUTI: 9,892 (7 emotions -> 3-class)",
        "• SAPTAK: 2,943 (981 manual Std labels)",
    ], PALETTE["box_blue_bg"], PALETTE["box_blue_bd"], "#1f4e79")

    draw_box(ax, x1, 2.85, w1, 1.22, "Canonical Cleaning & Deduplication", [
        "• Unicode NFC (8,341 raw strings fixed)",
        "• Drop 23 conflict + 436 SHA-256 dups",
        "• Clean Corpus: 16,865 rows (7,475 groups)",
    ], "#ffffff", PALETTE["box_blue_bd"], "#1f4e79")

    draw_box(ax, x1, 1.35, w1, 1.22, "Group-Stratified 80 / 10 / 10 Split", [
        "• Grouped strictly by Standard_Text hash",
        "• Train 13,491 | Val 1,689 | Test 1,685",
        "• Verified 0.00% exact-group overlap",
    ], PALETTE["box_blue_bg"], PALETTE["box_blue_bd"], "#1f4e79")

    draw_box(ax, x1, 0.30, w1, 0.80, "Model-Specific Preprocessing", [
        "• BanglaBERT: csebuetnlp/normalizer",
        "• mBERT / XLM-R / CANINE-C: NFC text",
    ], PALETTE["box_gray_bg"], PALETTE["box_gray_bd"], "#374151")

    arrow(ax, x1 + w1 / 2, 4.35, x1 + w1 / 2, 4.07)
    arrow(ax, x1 + w1 / 2, 2.85, x1 + w1 / 2, 2.57)
    arrow(ax, x1 + w1 / 2, 1.35, x1 + w1 / 2, 1.10)

    # Lane 2
    x2, w2 = 4.35, 3.45
    draw_box(ax, x2, 4.35, w2, 1.28, "Multi-Tokenizer Fertility Profiling", [
        "• BanglaBERT WP: Chat. +48.61% inflation",
        "• XLM-R SP: Chat. +40.45% | mBERT +19.36%",
        "• Hierarchy: Mym < Noak < Sylh << Chat.",
    ], PALETTE["box_amber_bg"], PALETTE["box_amber_bd"], "#7f6000")

    draw_box(ax, x2, 2.85, w2, 1.22, "Stage 1 -> Stage 2 Zero-Shot Drop", [
        "• Stage 1 Standard FT: 83.24% / 0.7887 F1",
        "• Stage 2 Dialect Zero-Shot: 74.26% / 0.6217",
        "• BUET Normalizer: +0.0578 F1 (seed 42)",
    ], "#ffffff", PALETTE["box_amber_bd"], "#7f6000")

    draw_box(ax, x2, 1.35, w2, 1.22, "Controlled Error Modeling (N=1,685)", [
        "• Macro r = 0.9907 (s42) | r = 0.9942 (3-seed)",
        "• Logit Edit Dist: OR = 7.28 (p = 1.2e-4)",
        "• Logit Fertility: OR = 1.59 (p = 0.0401)",
    ], PALETTE["box_amber_bg"], PALETTE["box_amber_bd"], "#7f6000")

    draw_box(ax, x2, 0.30, w2, 0.80, "200-Sample 4-Way Error Taxonomy", [
        "• Subword 29.5% (55.9% fixed) | OOV 28.0%",
        "• Pragmatic 27.5% | Negation Shift 15.0%",
    ], PALETTE["box_gray_bg"], PALETTE["box_gray_bd"], "#374151")

    arrow(ax, x2 + w2 / 2, 4.35, x2 + w2 / 2, 4.07)
    arrow(ax, x2 + w2 / 2, 2.85, x2 + w2 / 2, 2.57)
    arrow(ax, x2 + w2 / 2, 1.35, x2 + w2 / 2, 1.10)

    # Lane 3 (extra wide for clear text margins)
    x3, w3 = 8.45, 4.25
    draw_box(ax, x3, 4.65, w3, 0.98, "Stage 1 Canonical Checkpoint (W_S1)", [
        "• Fine-tuned on Std Bangla (n = 13,491; 3 ep, lr=2e-5)",
        "• Preserves formal syntactic & polarity geometry",
    ], PALETTE["box_green_bg"], PALETTE["box_green_bd"], "#274e13")

    draw_box(ax, x3, 2.85, 2.05, 1.48, "Frozen Backbone", [
        "12 Layers Locked",
        "110.0M (99.20%)",
        "Zero grad states",
        "Preserves W_S1",
    ], PALETTE["box_gray_bg"], PALETTE["box_gray_bd"], "#374151", dashed=True, lw=1.4)

    draw_box(ax, x3 + 2.20, 2.85, 2.05, 1.48, "Trainable LoRA", [
        "Q & V projections",
        "r = 8, alpha = 32",
        "h = W_S1 x + 4 BAx",
        "294,912 (0.27%)",
    ], PALETTE["box_amber_bg"], PALETTE["box_amber_bd"], "#7f6000", lw=1.4)

    draw_box(ax, x3, 1.25, w3, 1.28, "Unfrozen Head + Anchor Adaptation", [
        "• Head: 592,899 (0.53%) -> Total 0.8004% of 110.9M",
        "• 1 anchor only (Chat. n=5,201; 5 ep, lr=3e-4)",
        "• Anchor-only val selection (targets unseen)",
    ], PALETTE["box_red_bg"], PALETTE["box_red_bd"], "#8b1d1d", lw=1.4)

    draw_box(ax, x3, 0.30, w3, 0.72, "Matched A100 Hardware Footprint", [
        "• Peak VRAM: 1,174 MB (-46.4% vs. Full-FT) | 82.2 s",
    ], PALETTE["box_green_bg"], PALETTE["box_green_bd"], "#274e13")

    arrow(ax, x3 + 1.02, 4.65, x3 + 1.02, 4.33)
    arrow(ax, x3 + 3.22, 4.65, x3 + 3.22, 4.33)
    arrow(ax, x3 + 1.02, 2.85, x3 + 1.02, 2.53)
    arrow(ax, x3 + 3.22, 2.85, x3 + 3.22, 2.53)
    arrow(ax, x3 + w3 / 2, 1.25, x3 + w3 / 2, 1.02)

    # Lane 4
    x4, w4 = 13.35, 3.55
    draw_box(ax, x4, 4.25, w4, 1.38, "Fair PEFT & Architecture Controls", [
        "• Head-Only: 75.43% / 0.6928 F1",
        "• Raw -> LoRA: 77.56% / 0.7173 F1",
        "• Chattogram Full-FT: 78.72% / 0.7248 F1",
        "• CANINE-C (pooled, s42): 71.04% / 0.6559",
    ], "#ffffff", PALETTE["box_purple_bd"], "#4c1130")

    draw_box(ax, x4, 2.75, w4, 1.22, "Stage 1 -> Anchor LoRA (3 Seeds)", [
        "• Pooled: 80.57% Acc / 0.7516 F1",
        "• Unseen Non-Anchor: 83.87% (+2.61)",
        "• McNemar vs. S2: +88 fixes (p = 9.2e-7)",
    ], PALETTE["box_purple_bg"], PALETTE["box_purple_bd"], "#4c1130", lw=1.5)

    draw_box(ax, x4, 1.30, w4, 1.18, "4x4 Baseline-Gain Transfer Matrix", [
        "• All 4 dialects tested as single anchors",
        "• Largest gain in-domain (+12.20 Chat.)",
        "• Unseen non-anchor: +2.61 to +3.23 pts",
    ], "#ffffff", PALETTE["box_purple_bd"], "#4c1130")

    draw_box(ax, x4, 0.30, w4, 0.78, "Cross-Backbone Verification", [
        "• mBERT S1->LoRA: +0.0999 F1 (3 seeds)",
        "• XLM-R sweep: 0.4344 -> 0.6746 (s42)",
    ], PALETTE["box_gray_bg"], PALETTE["box_gray_bd"], "#374151")

    arrow(ax, x4 + w4 / 2, 4.25, x4 + w4 / 2, 3.97)
    arrow(ax, x4 + w4 / 2, 2.75, x4 + w4 / 2, 2.48)
    arrow(ax, x4 + w4 / 2, 1.30, x4 + w4 / 2, 1.08)

    # Inter-lane flow arrows
    arrow(ax, 3.85, 3.22, 4.20, 3.22, color=PALETTE["lane1_hdr"], lw=2.2)
    arrow(ax, 7.95, 3.22, 8.30, 3.22, color=PALETTE["lane2_hdr"], lw=2.2)
    arrow(ax, 12.85, 3.22, 13.20, 3.22, color=PALETTE["lane3_hdr"], lw=2.2)

    os.makedirs(FIG_DIR, exist_ok=True)
    for ext in ("png", "pdf", "svg"):
        out_p = os.path.join(FIG_DIR, f"fig_methodology_workflow.{ext}")
        fig.savefig(out_p, dpi=400, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    drawio_path = os.path.join(FIG_DIR, "fig_methodology_workflow.drawio")
    write_drawio_xml(drawio_path)
    render_diagram()
    print("Generated editable draw.io XML + 400 DPI PNG/PDF/SVG in:", FIG_DIR)


if __name__ == "__main__":
    main()
