"""
Generate Publication-Grade CS/NLP System Architecture & Data-Flow Diagram
=========================================================================
Produces both an editable native draw.io (.drawio) XML file using standard
ISO-5807 / neural-architecture shapes and crisp vector/raster outputs:
  1. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.drawio
  2. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.pdf
  3. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.svg
  4. manuscripts/01_TALLIP_Short_Note/figures/fig_methodology_workflow.png (400 DPI)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (
    Circle,
    Ellipse,
    FancyArrowPatch,
    PathPatch,
    Polygon,
    Rectangle,
)
from matplotlib.path import Path

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
FIG_DIR = os.path.join(BASE_DIR, "manuscripts", "01_TALLIP_Short_Note", "figures")

# Restrained grayscale-first academic palette (60-30-10)
COLORS = {
    "bg": "#FFFFFF",
    "panel_bd": "#CBD5E1",
    "panel_title": "#0F172A",
    "ink": "#1F2937",
    "muted_ink": "#4B5563",
    "neutral_bg": "#F8FAFC",
    "neutral_bd": "#475569",
    "frozen_bg": "#F1F5F9",
    "frozen_bd": "#64748B",
    "train_bg": "#E6EEF8",
    "train_bd": "#2C5282",
    "group_bd": "#94A3B8",
}


def write_drawio_xml(out_path: str) -> None:
    """Write a native editable draw.io XML using standard CS shapes."""
    xml = """<mxfile host="app.diagrams.net" modified="2026-11-26T14:20:00.000Z" agent="TALLIP-V2-ArchDiagram" version="24.7.17" type="device">
  <diagram id="tallip-v2-arch" name="System Architecture and Data-Flow">
    <mxGraphModel dx="1440" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1280" pageHeight="560" math="1" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- Panel (a) Container -->
        <mxCell id="panel_a" value="(a) Data-Flow &amp; Diagnostic Pipeline" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#CBD5E1;strokeWidth=1.2;verticalAlign=top;align=left;spacingLeft=12;spacingTop=8;fontStyle=1;fontSize=12;fontColor=#0F172A;" vertex="1" parent="1">
          <mxGeometry x="20" y="15" width="1240" height="225" as="geometry" />
        </mxCell>

        <mxCell id="a_raw" value="&lt;b&gt;Raw Corpora&lt;/b&gt;&lt;br/&gt;3 Regional Sets" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="40" y="95" width="130" height="76" as="geometry" />
        </mxCell>
        <mxCell id="a_nfc" value="&lt;b&gt;NFC &amp;amp; Dedup&lt;/b&gt;&lt;br/&gt;SHA-256 Clean" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="225" y="102" width="140" height="62" as="geometry" />
        </mxCell>
        <mxCell id="a_split" value="&lt;b&gt;Group Split&lt;/b&gt;&lt;br/&gt;80 / 10 / 10" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="420" y="102" width="135" height="62" as="geometry" />
        </mxCell>
        <mxCell id="a_clean" value="&lt;b&gt;Clean Splits&lt;/b&gt;&lt;br/&gt;0% Overlap" style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=10;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="610" y="95" width="130" height="76" as="geometry" />
        </mxCell>

        <mxCell id="a_norm" value="&lt;b&gt;BUET / NFC Norm.&lt;/b&gt;&lt;br/&gt;Text Stream" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="820" y="55" width="165" height="58" as="geometry" />
        </mxCell>
        <mxCell id="a_rq1" value="&lt;b&gt;RQ1 Audit&lt;/b&gt;&lt;br/&gt;Fertility &amp;amp; Logit" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="1055" y="55" width="165" height="58" as="geometry" />
        </mxCell>

        <mxCell id="a_xstd" value="&lt;b&gt;Standard Input&lt;/b&gt;&lt;br/&gt;&lt;i&gt;X_std&lt;/i&gt;" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;size=16;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="815" y="155" width="175" height="58" as="geometry" />
        </mxCell>
        <mxCell id="a_s1ft" value="&lt;b&gt;Stage 1 FT&lt;/b&gt;&lt;br/&gt;Learn &lt;i&gt;W_S1&lt;/i&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="1055" y="155" width="165" height="58" as="geometry" />
        </mxCell>

        <mxCell id="ea_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_raw" target="a_nfc"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ea_2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_nfc" target="a_split"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ea_3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_split" target="a_clean"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ea_4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_clean" target="a_norm"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ea_5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_norm" target="a_rq1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ea_6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_clean" target="a_xstd"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ea_7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="a_xstd" target="a_s1ft"><mxGeometry relative="1" as="geometry" /></mxCell>

        <!-- Panel (b) Container -->
        <mxCell id="panel_b" value="(b) Stage-1-Initialized Anchor LoRA Architecture" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#CBD5E1;strokeWidth=1.2;verticalAlign=top;align=left;spacingLeft=12;spacingTop=8;fontStyle=1;fontSize=12;fontColor=#0F172A;" vertex="1" parent="1">
          <mxGeometry x="20" y="275" width="1240" height="235" as="geometry" />
        </mxCell>

        <mxCell id="b_xdial" value="&lt;b&gt;Dialect Input&lt;/b&gt;&lt;br/&gt;&lt;i&gt;X_dial&lt;/i&gt;" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;size=14;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="35" y="370" width="130" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b_tok" value="&lt;b&gt;Tokenizer&lt;/b&gt;&lt;br/&gt;&amp;amp; Embedding" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="195" y="370" width="118" height="60" as="geometry" />
        </mxCell>

        <mxCell id="b_layer" value="Transformer Layer (×12, Q &amp;amp; V)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#94A3B8;dashed=1;dashPattern=3 3;strokeWidth=1.1;verticalAlign=top;align=left;spacingLeft=8;spacingTop=5;fontStyle=2;fontSize=10;fontColor=#4B5563;" vertex="1" parent="1">
          <mxGeometry x="348" y="305" width="368" height="185" as="geometry" />
        </mxCell>

        <mxCell id="b_ws1" value="&lt;b&gt;W_S1&lt;/b&gt; ∈ ℝ^(d×d)&lt;br/&gt;(Frozen, ∇ = 0)" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F1F5F9;strokeColor=#64748B;dashed=1;dashPattern=6 4;strokeWidth=1.3;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="405" y="340" width="215" height="52" as="geometry" />
        </mxCell>
        <mxCell id="b_a" value="&lt;b&gt;A&lt;/b&gt;&lt;br/&gt;r×d, N" style="shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;direction=south;size=12;fillColor=#E6EEF8;strokeColor=#2C5282;strokeWidth=1.5;fontSize=10;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="392" y="420" width="72" height="56" as="geometry" />
        </mxCell>
        <mxCell id="b_b" value="&lt;b&gt;B&lt;/b&gt;&lt;br/&gt;d×r, 0" style="shape=trapezoid;perimeter=trapezoidPerimeter;whiteSpace=wrap;html=1;fixedSize=1;direction=north;size=12;fillColor=#E6EEF8;strokeColor=#2C5282;strokeWidth=1.5;fontSize=10;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="488" y="420" width="72" height="56" as="geometry" />
        </mxCell>
        <mxCell id="b_scale" value="× α/r" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#E6EEF8;strokeColor=#2C5282;strokeWidth=1.3;fontSize=10;fontStyle=1;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="584" y="427" width="42" height="42" as="geometry" />
        </mxCell>
        <mxCell id="b_add" value="+" style="ellipse;whiteSpace=wrap;html=1;aspect=fixed;fillColor=#FFFFFF;strokeColor=#1F2937;strokeWidth=1.4;fontSize=14;fontStyle=1;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="660" y="381" width="38" height="38" as="geometry" />
        </mxCell>

        <mxCell id="b_head" value="&lt;b&gt;Classifier Head&lt;/b&gt;&lt;br/&gt;Unfrozen" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#E6EEF8;strokeColor=#2C5282;strokeWidth=1.5;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="820" y="370" width="135" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b_pred" value="&lt;b&gt;Prediction&lt;/b&gt;&lt;br/&gt;ŷ ∈ {-1,0,+1}" style="shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;size=14;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="980" y="370" width="130" height="60" as="geometry" />
        </mxCell>
        <mxCell id="b_eval" value="&lt;b&gt;4×4 Eval&lt;/b&gt;&lt;br/&gt;Unseen Dialects" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#F8FAFC;strokeColor=#475569;strokeWidth=1.2;fontSize=10.5;fontColor=#1F2937;" vertex="1" parent="1">
          <mxGeometry x="1135" y="370" width="115" height="60" as="geometry" />
        </mxCell>

        <!-- Cross-panel connectors -->
        <mxCell id="cross_data" value="Anchor Split" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;fontSize=9.5;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="a_clean" target="b_xdial">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="675" y="250" />
              <mxPoint x="100" y="250" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="cross_init" value="Init W_S1 (freeze)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#4B5563;strokeWidth=1.2;dashed=1;dashPattern=5 3;fontSize=9.5;labelBackgroundColor=#FFFFFF;exitX=0.5;exitY=1;entryX=0.88;entryY=0;" edge="1" parent="1" source="a_s1ft" target="b_ws1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="1137" y="264" />
              <mxPoint x="594" y="264" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Panel (b) edges -->
        <mxCell id="eb_1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="b_xdial" target="b_tok"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eb_2" value="x" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;fontSize=10;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="b_tok" target="b_ws1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="370" y="400" />
              <mxPoint x="370" y="366" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="eb_3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="b_tok" target="b_a">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="370" y="400" />
              <mxPoint x="370" y="448" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="eb_4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2C5282;strokeWidth=1.2;" edge="1" parent="1" source="b_a" target="b_b"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eb_5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2C5282;strokeWidth=1.2;" edge="1" parent="1" source="b_b" target="b_scale"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eb_6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="b_ws1" target="b_add">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="679" y="366" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="eb_7" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#2C5282;strokeWidth=1.2;" edge="1" parent="1" source="b_scale" target="b_add">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="679" y="448" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="eb_8" value="h = W_S1 x + (α/r)BAx" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;fontSize=9.5;labelBackgroundColor=#FFFFFF;" edge="1" parent="1" source="b_add" target="b_head"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eb_9" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="b_head" target="b_pred"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eb_10" style="edgeStyle=orthogonalEdgeStyle;rounded=0;strokeColor=#1F2937;strokeWidth=1.2;" edge="1" parent="1" source="b_pred" target="b_eval"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(xml)


def draw_cylinder(ax, xc, yc, w, h, title, sub="", fc=COLORS["neutral_bg"], ec=COLORS["neutral_bd"], lw=1.15):
    """Draw a classic CS data-store cylinder."""
    ry = h * 0.14
    x0, x1 = xc - w / 2, xc + w / 2
    y_bot, y_top = yc - h / 2 + ry, yc + h / 2 - ry

    angles = np.linspace(np.pi, 2 * np.pi, 40)
    arc_pts = [(xc + (w / 2) * np.cos(a), y_bot + ry * np.sin(a)) for a in angles]
    path_pts = [(x0, y_top)] + arc_pts + [(x1, y_top), (x0, y_top)]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(path_pts) - 2) + [Path.CLOSEPOLY]
    body = PathPatch(Path(path_pts, codes), facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(body)

    top_cap = Ellipse((xc, y_top), width=w, height=2 * ry, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=4)
    ax.add_patch(top_cap)

    ax.text(xc, yc + 0.03, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=COLORS["ink"], zorder=5)
    if sub:
        ax.text(xc, yc - 0.14, sub, ha="center", va="center", fontsize=7.5, color=COLORS["muted_ink"], zorder=5)


def draw_parallelogram(ax, xc, yc, w, h, title, sub="", skew=0.14, fc=COLORS["neutral_bg"], ec=COLORS["neutral_bd"], lw=1.15):
    """Draw a standard ISO-5807 I/O parallelogram."""
    x0, x1 = xc - w / 2, xc + w / 2
    y0, y1 = yc - h / 2, yc + h / 2
    s = skew / 2.0
    pts = [
        (x0 + s, y1),
        (x1 + s, y1),
        (x1 - s, y0),
        (x0 - s, y0),
    ]
    poly = Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(poly)
    if sub:
        ax.text(xc, yc + 0.09, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=COLORS["ink"], zorder=4)
        ax.text(xc, yc - 0.11, sub, ha="center", va="center", fontsize=8.0, color=COLORS["muted_ink"], zorder=4)
    else:
        ax.text(xc, yc, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=COLORS["ink"], zorder=4)


def draw_rect(ax, xc, yc, w, h, title, sub="", fc=COLORS["neutral_bg"], ec=COLORS["neutral_bd"], lw=1.15, ls="-"):
    """Draw a standard CS process or neural layer rectangle."""
    rect = Rectangle(
        (xc - w / 2, yc - h / 2), w, h,
        facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=3
    )
    ax.add_patch(rect)
    if sub:
        ax.text(xc, yc + 0.09, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=COLORS["ink"], zorder=4)
        ax.text(xc, yc - 0.11, sub, ha="center", va="center", fontsize=7.6, color=COLORS["muted_ink"], zorder=4)
    else:
        ax.text(xc, yc, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color=COLORS["ink"], zorder=4)


def draw_trapezoid(ax, xc, yc, w, h_left, h_right, title, sub="", fc=COLORS["train_bg"], ec=COLORS["train_bd"], lw=1.45):
    """Draw LoRA down-projection (h_left > h_right) or up-projection (h_left < h_right) trapezoid."""
    x0, x1 = xc - w / 2, xc + w / 2
    pts = [
        (x0, yc + h_left / 2),
        (x1, yc + h_right / 2),
        (x1, yc - h_right / 2),
        (x0, yc - h_left / 2),
    ]
    poly = Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(poly)
    ax.text(xc, yc + 0.08, title, ha="center", va="center", fontsize=9.0, fontweight="bold", color=COLORS["ink"], zorder=4)
    if sub:
        ax.text(xc, yc - 0.10, sub, ha="center", va="center", fontsize=7.4, color=COLORS["train_bd"], zorder=4)


def draw_polyline_arrow(ax, pts, color=COLORS["ink"], lw=1.15, ls="-", label=None, label_pos=None):
    """Draw clean orthogonal multi-segment line ending with a crisp arrowhead."""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if len(pts) > 2:
        ax.plot(xs[:-1], ys[:-1], color=color, linewidth=lw, linestyle=ls, solid_capstyle="butt", zorder=2)
    arrow = FancyArrowPatch(
        pts[-2], pts[-1],
        arrowstyle="-|>,head_length=4.5,head_width=2.6",
        color=color, linewidth=lw, linestyle=ls,
        shrinkA=0, shrinkB=0, zorder=2
    )
    ax.add_patch(arrow)
    if label and label_pos:
        ax.text(
            label_pos[0], label_pos[1], label,
            ha="center", va="center", fontsize=7.8, color=color,
            bbox=dict(boxstyle="square,pad=0.14", facecolor="#FFFFFF", edgecolor="none"),
            zorder=6
        )


def render_publication_figure(out_dir: str) -> None:
    """Render crisp vector PDF/SVG and 400 DPI PNG."""
    plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["mathtext.fontset"] = "stix"

    fig, ax = plt.subplots(figsize=(12.8, 5.6))
    ax.set_xlim(0, 12.8)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    fig.patch.set_facecolor(COLORS["bg"])

    # ------------------------------------------------------------------
    # Panel Frames
    # ------------------------------------------------------------------
    panel_a = Rectangle((0.15, 3.22), 12.50, 2.22, facecolor="none", edgecolor=COLORS["panel_bd"], linewidth=1.1, zorder=1)
    ax.add_patch(panel_a)
    ax.text(0.28, 5.24, "(a) Data-Flow & Diagnostic Pipeline", ha="left", va="center",
            fontsize=10.0, fontweight="bold", color=COLORS["panel_title"], zorder=5)

    panel_b = Rectangle((0.15, 0.56), 12.50, 2.34, facecolor="none", edgecolor=COLORS["panel_bd"], linewidth=1.1, zorder=1)
    ax.add_patch(panel_b)
    ax.text(0.28, 2.70, "(b) Stage-1-Initialized Anchor LoRA Architecture", ha="left", va="center",
            fontsize=10.0, fontweight="bold", color=COLORS["panel_title"], zorder=5)

    # ------------------------------------------------------------------
    # Panel (a) Nodes
    # ------------------------------------------------------------------
    y_main = 4.14
    draw_cylinder(ax, 0.96, y_main, 1.30, 0.72, "Raw Corpora", "3 Regional Sets")
    draw_rect(ax, 2.86, y_main, 1.44, 0.62, "NFC & Dedup", "SHA-256 Clean")
    draw_rect(ax, 4.82, y_main, 1.38, 0.62, "Group Split", "80 / 10 / 10")
    draw_cylinder(ax, 6.72, y_main, 1.30, 0.72, "Clean Splits", "0% Overlap")

    # Right-side parallel tracks
    y_top = 4.62
    y_bot = 3.66
    draw_rect(ax, 9.10, y_top, 1.72, 0.56, "BUET / NFC Norm.", "Text Stream")
    draw_rect(ax, 11.50, y_top, 1.66, 0.56, "RQ1 Audit", "Fertility & Logit")

    draw_parallelogram(ax, 9.10, y_bot, 1.74, 0.56, "Standard Input", r"$X_{\mathrm{std}}$", skew=0.20)
    draw_rect(ax, 11.50, y_bot, 1.66, 0.56, "Stage 1 FT", r"Learn $W_{\mathrm{S1}}$")

    # Panel (a) Arrows
    draw_polyline_arrow(ax, [(1.61, y_main), (2.14, y_main)])
    draw_polyline_arrow(ax, [(3.58, y_main), (4.13, y_main)])
    draw_polyline_arrow(ax, [(5.51, y_main), (6.07, y_main)])
    # Branch from Clean Splits
    draw_polyline_arrow(ax, [(7.37, y_main), (7.74, y_main), (7.74, y_top), (8.24, y_top)])
    draw_polyline_arrow(ax, [(9.96, y_top), (10.67, y_top)])
    draw_polyline_arrow(ax, [(7.37, y_main), (7.74, y_main), (7.74, y_bot), (8.18, y_bot)])
    draw_polyline_arrow(ax, [(10.02, y_bot), (10.67, y_bot)])

    # ------------------------------------------------------------------
    # Panel (b) Nodes
    # ------------------------------------------------------------------
    yb_mid = 1.56
    draw_parallelogram(ax, 0.88, yb_mid, 1.24, 0.58, "Dialect Input", r"$X_{\mathrm{dial}}$", skew=0.18)
    draw_rect(ax, 2.40, yb_mid, 1.18, 0.58, "Tokenizer", "& Embedding")

    # Grouping box for Transformer Layer (left-aligned title leaves top-right clear for dashed arrow!)
    layer_box = Rectangle((3.36, 0.72), 3.68, 1.72, facecolor="none", edgecolor=COLORS["group_bd"],
                          linewidth=1.05, linestyle=":", zorder=2)
    ax.add_patch(layer_box)
    ax.text(3.46, 2.31, r"Transformer Layer ($\times 12$, Q & V)", ha="left", va="center",
            fontsize=8.0, style="italic", color=COLORS["muted_ink"], zorder=4)

    # Frozen path
    y_frz = 1.92
    draw_rect(ax, 5.04, y_frz, 2.08, 0.50, r"$W_{\mathrm{S1}} \in \mathbb{R}^{d \times d}$",
              r"Frozen ($\nabla = 0$)", fc=COLORS["frozen_bg"], ec=COLORS["frozen_bd"], lw=1.25, ls="--")

    # Trainable LoRA path
    y_lora = 1.10
    draw_trapezoid(ax, 4.18, y_lora, 0.72, 0.56, 0.30, r"$A$", r"$r{\times}d,\,\mathcal{N}$")
    draw_trapezoid(ax, 5.12, y_lora, 0.72, 0.30, 0.56, r"$B$", r"$d{\times}r,\,\mathbf{0}$")

    scale_circle = Circle((5.96, y_lora), radius=0.21, facecolor=COLORS["train_bg"],
                          edgecolor=COLORS["train_bd"], linewidth=1.35, zorder=3)
    ax.add_patch(scale_circle)
    ax.text(5.96, y_lora, r"$\times\frac{\alpha}{r}$", ha="center", va="center",
            fontsize=8.8, fontweight="bold", color=COLORS["ink"], zorder=4)

    # Addition node
    add_circle = Circle((6.72, yb_mid), radius=0.18, facecolor="#FFFFFF",
                        edgecolor=COLORS["ink"], linewidth=1.35, zorder=3)
    ax.add_patch(add_circle)
    ax.text(6.72, yb_mid + 0.005, "+", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=COLORS["ink"], zorder=4)

    # Downstream trainable head, output, evaluation (with comfortable padding!)
    draw_rect(ax, 8.95, yb_mid, 1.38, 0.58, "Classifier Head", "Unfrozen",
              fc=COLORS["train_bg"], ec=COLORS["train_bd"], lw=1.45)
    draw_parallelogram(ax, 10.52, yb_mid, 1.30, 0.58, "Prediction", r"$\hat{y}\in\{-1,0,+1\}$", skew=0.16)
    draw_rect(ax, 11.96, yb_mid, 1.18, 0.58, r"4$\times$4 Eval", "Unseen Dialects")

    # Panel (b) Arrows
    draw_polyline_arrow(ax, [(1.55, yb_mid), (1.81, yb_mid)])
    # Split x -> frozen and LoRA
    draw_polyline_arrow(ax, [(2.99, yb_mid), (3.58, yb_mid), (3.58, y_frz), (4.00, y_frz)],
                        label=r"$x$", label_pos=(3.18, yb_mid + 0.14))
    draw_polyline_arrow(ax, [(3.58, yb_mid), (3.58, y_lora), (3.82, y_lora)])
    # LoRA internal arrows
    draw_polyline_arrow(ax, [(4.54, y_lora), (4.76, y_lora)], color=COLORS["train_bd"], lw=1.2)
    draw_polyline_arrow(ax, [(5.48, y_lora), (5.75, y_lora)], color=COLORS["train_bd"], lw=1.2)
    # Merge into (+)
    draw_polyline_arrow(ax, [(6.08, y_frz), (6.72, y_frz), (6.72, yb_mid + 0.18)])
    draw_polyline_arrow(ax, [(6.17, y_lora), (6.72, y_lora), (6.72, yb_mid - 0.18)], color=COLORS["train_bd"], lw=1.2)
    # (+) -> Head with generous 1.36-unit gap for equation label!
    draw_polyline_arrow(ax, [(6.90, yb_mid), (8.26, yb_mid)],
                        label=r"$h = W_{\mathrm{S1}} x + \frac{\alpha}{r} B A x$",
                        label_pos=(7.60, yb_mid + 0.24))
    draw_polyline_arrow(ax, [(9.64, yb_mid), (9.83, yb_mid)])
    draw_polyline_arrow(ax, [(11.21, yb_mid), (11.37, yb_mid)])

    # ------------------------------------------------------------------
    # Inter-Panel Connectors (Zero Text Collisions, Zero Crossings)
    # ------------------------------------------------------------------
    # Clean Splits -> Dialect Input
    draw_polyline_arrow(
        ax,
        [(6.72, 3.78), (6.72, 3.11), (0.88, 3.11), (0.88, 1.85)],
        color=COLORS["ink"], lw=1.15, ls="-",
        label="Anchor Split", label_pos=(3.80, 3.11)
    )
    # Stage 1 FT -> Frozen W_S1 (drops at x=5.94, strictly right of Panel (b) title & Transformer title!)
    draw_polyline_arrow(
        ax,
        [(11.50, 3.38), (11.50, 2.98), (5.94, 2.98), (5.94, 2.17)],
        color=COLORS["muted_ink"], lw=1.15, ls="--",
        label=r"Init $W_{\mathrm{S1}}$ (freeze)", label_pos=(8.85, 2.98)
    )

    # ------------------------------------------------------------------
    # Compact Bottom Shape & Parameter Legend
    # ------------------------------------------------------------------
    yl = 0.25
    draw_cylinder(ax, 1.10, yl, 0.34, 0.24, "", "", lw=0.95)
    ax.text(1.35, yl, "Corpus / Store", ha="left", va="center", fontsize=8.0, color=COLORS["ink"])

    draw_parallelogram(ax, 2.90, yl, 0.38, 0.20, "", "", skew=0.08, lw=0.95)
    ax.text(3.18, yl, "Data I/O", ha="left", va="center", fontsize=8.0, color=COLORS["ink"])

    draw_rect(ax, 4.45, yl, 0.36, 0.20, "", "", lw=0.95)
    ax.text(4.71, yl, "Process / Layer", ha="left", va="center", fontsize=8.0, color=COLORS["ink"])

    draw_trapezoid(ax, 6.42, yl, 0.34, 0.22, 0.11, "", "", lw=1.05)
    ax.text(6.67, yl, "Low-Rank Proj.", ha="left", va="center", fontsize=8.0, color=COLORS["ink"])

    draw_rect(ax, 8.38, yl, 0.36, 0.20, "", "", fc=COLORS["frozen_bg"], ec=COLORS["frozen_bd"], lw=1.1, ls="--")
    ax.text(8.64, yl, "Frozen (99.2%)", ha="left", va="center", fontsize=8.0, color=COLORS["ink"])

    draw_rect(ax, 10.42, yl, 0.36, 0.20, "", "", fc=COLORS["train_bg"], ec=COLORS["train_bd"], lw=1.2, ls="-")
    ax.text(10.68, yl, "Trainable (0.8%)", ha="left", va="center", fontsize=8.0, color=COLORS["ink"])

    os.makedirs(out_dir, exist_ok=True)
    for ext, dpi in [("pdf", None), ("svg", None), ("png", 400)]:
        out_path = os.path.join(out_dir, f"fig_methodology_workflow.{ext}")
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.05, "facecolor": COLORS["bg"]}
        if dpi is not None:
            kwargs["dpi"] = dpi
        fig.savefig(out_path, **kwargs)
    plt.close(fig)


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    drawio_path = os.path.join(FIG_DIR, "fig_methodology_workflow.drawio")
    write_drawio_xml(drawio_path)
    render_publication_figure(FIG_DIR)
    print(f"Generated draw.io XML + PDF/SVG/PNG in: {FIG_DIR}")


if __name__ == "__main__":
    main()
