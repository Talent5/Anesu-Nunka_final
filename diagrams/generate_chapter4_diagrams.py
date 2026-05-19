"""
============================================================================
  Generate Academic-Quality Diagrams for Chapter 4: Process / Concept / Model Design
  Anesu Nunkha — BSc Capstone Project, University of Zimbabwe
  Explainable ML for Early Diabetes Risk Stratification and Diagnosis
============================================================================
Produces publication-ready figures saved as PNG (300 dpi) for embedding
in the dissertation manuscript.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# ── Global style ──────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.1 — High-Level Conceptual Framework
# ═══════════════════════════════════════════════════════════════════════════

def draw_conceptual_framework():
    fig, ax = plt.subplots(figsize=(14, 7.5))
    ax.set_xlim(-0.5, 14)
    ax.set_ylim(-0.5, 8)
    ax.axis("off")

    # ── Layer 1: Input Layer ─────────────────────────────────────────
    input_box = FancyBboxPatch((0.3, 5.8), 3.0, 1.8,
                                boxstyle="round,pad=0.12", lw=2.0,
                                ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(input_box)
    ax.text(1.8, 7.2, "INPUT LAYER", ha="center", fontsize=10,
            fontweight="bold", color="#1565C0")
    ax.text(1.8, 6.7, "Multi-Modal Patient Data", ha="center",
            fontsize=7.5, color="#1565C0", style="italic")
    inputs = ["Clinical: BMI, BP, Cholesterol",
              "Demographic: Age, Sex, Income",
              "Lifestyle: Smoking, Activity, Diet"]
    for i, inp in enumerate(inputs):
        ax.text(0.55, 6.25 - i * 0.28, inp, fontsize=6.5, color="#37474F")

    # ── Layer 2: Processing Layer ────────────────────────────────────
    proc_box = FancyBboxPatch((4.3, 5.8), 3.2, 1.8,
                               boxstyle="round,pad=0.12", lw=2.0,
                               ec="#00838F", fc="#E0F7FA")
    ax.add_patch(proc_box)
    ax.text(5.9, 7.2, "PROCESSING LAYER", ha="center", fontsize=10,
            fontweight="bold", color="#00838F")
    ax.text(5.9, 6.7, "Data Preprocessing Pipeline", ha="center",
            fontsize=7.5, color="#00838F", style="italic")
    procs = ["Cleaning & Imputation",
             "Outlier Capping (IQR)",
             "Encoding, Scaling & SMOTE"]
    for i, p in enumerate(procs):
        ax.text(4.55, 6.25 - i * 0.28, p, fontsize=6.5, color="#37474F")

    # ── Layer 3: Intelligence Layer ──────────────────────────────────
    ml_box = FancyBboxPatch((8.5, 5.8), 3.2, 1.8,
                             boxstyle="round,pad=0.12", lw=2.0,
                             ec="#2E7D32", fc="#E8F5E9")
    ax.add_patch(ml_box)
    ax.text(10.1, 7.2, "INTELLIGENCE LAYER", ha="center", fontsize=10,
            fontweight="bold", color="#2E7D32")
    ax.text(10.1, 6.7, "ML Classification Engine", ha="center",
            fontsize=7.5, color="#2E7D32", style="italic")
    mls = ["Balanced Random Forest (Primary)",
           "Multi-tier Risk Stratification",
           "Probability Score Generation"]
    for i, m in enumerate(mls):
        ax.text(8.75, 6.25 - i * 0.28, m, fontsize=6.5, color="#37474F")

    # ── Layer 4: Explainability Layer ────────────────────────────────
    xai_box = FancyBboxPatch((4.3, 2.8), 3.2, 1.8,
                              boxstyle="round,pad=0.12", lw=2.0,
                              ec="#E65100", fc="#FFF3E0")
    ax.add_patch(xai_box)
    ax.text(5.9, 4.2, "EXPLAINABILITY LAYER", ha="center", fontsize=10,
            fontweight="bold", color="#E65100")
    ax.text(5.9, 3.7, "XAI Interpretation Engine", ha="center",
            fontsize=7.5, color="#E65100", style="italic")
    xais = ["SHAP: Global & Local Attribution",
            "LIME: Local Surrogate Models",
            "Feature Contribution Ranking"]
    for i, x in enumerate(xais):
        ax.text(4.55, 3.25 - i * 0.28, x, fontsize=6.5, color="#37474F")

    # ── Layer 5: Output / Decision Layer ─────────────────────────────
    out_box = FancyBboxPatch((8.5, 2.8), 3.2, 1.8,
                              boxstyle="round,pad=0.12", lw=2.0,
                              ec="#C62828", fc="#FFEBEE")
    ax.add_patch(out_box)
    ax.text(10.1, 4.2, "DECISION OUTPUT", ha="center", fontsize=10,
            fontweight="bold", color="#C62828")
    ax.text(10.1, 3.7, "Clinical Decision Support", ha="center",
            fontsize=7.5, color="#C62828", style="italic")
    outs = ["Risk Category: Low/Moderate/High",
            "Top-5 Contributing Factors",
            "Personalised Recommendations"]
    for i, o in enumerate(outs):
        ax.text(8.75, 3.25 - i * 0.28, o, fontsize=6.5, color="#37474F")

    # ── Clinician / End User ─────────────────────────────────────────
    user_box = FancyBboxPatch((0.3, 2.8), 3.0, 1.8,
                               boxstyle="round,pad=0.12", lw=2.0,
                               ec="#6A1B9A", fc="#F3E5F5")
    ax.add_patch(user_box)
    ax.text(1.8, 4.2, "END USER", ha="center", fontsize=10,
            fontweight="bold", color="#6A1B9A")
    ax.text(1.8, 3.7, "Healthcare Clinician", ha="center",
            fontsize=7.5, color="#6A1B9A", style="italic")
    users = ["Views risk profile & gauge",
             "Reviews XAI explanations",
             "Makes informed clinical decisions"]
    for i, u in enumerate(users):
        ax.text(0.55, 3.25 - i * 0.28, u, fontsize=6.5, color="#37474F")

    # ── Arrows ───────────────────────────────────────────────────────
    arrow_kw = dict(arrowstyle="-|>", lw=1.8, color="#616161")

    # Input -> Processing
    ax.annotate("", xy=(4.3, 6.7), xytext=(3.3, 6.7),
                arrowprops=arrow_kw)

    # Processing -> Intelligence
    ax.annotate("", xy=(8.5, 6.7), xytext=(7.5, 6.7),
                arrowprops=arrow_kw)

    # Intelligence -> XAI
    ax.annotate("", xy=(7.5, 4.6), xytext=(10.1, 5.8),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#E65100",
                                connectionstyle="arc3,rad=0.25"))

    # Intelligence -> Output
    ax.annotate("", xy=(10.1, 4.6), xytext=(10.1, 5.8),
                arrowprops=dict(arrowstyle="-|>", lw=1.8, color="#C62828"))

    # XAI -> Output
    ax.annotate("", xy=(8.5, 3.7), xytext=(7.5, 3.7),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#E65100"))

    # Output -> User
    ax.annotate("", xy=(3.3, 3.7), xytext=(8.5, 3.7),
                arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#6A1B9A",
                                connectionstyle="arc3,rad=-0.15"))

    # User -> Input (feedback)
    ax.annotate("", xy=(1.8, 5.8), xytext=(1.8, 4.6),
                arrowprops=dict(arrowstyle="-|>", lw=1.2, color="#9E9E9E",
                                linestyle="dashed"))
    ax.text(0.6, 5.2, "New patient\ndata entry", fontsize=6, color="#9E9E9E",
            style="italic")

    # ── Title labels for flow ────────────────────────────────────────
    ax.text(3.75, 7.0, "1", fontsize=18, fontweight="bold", color="#BDBDBD",
            ha="center", va="center")
    ax.text(7.95, 7.0, "2", fontsize=18, fontweight="bold", color="#BDBDBD",
            ha="center", va="center")
    ax.text(10.1, 5.2, "3", fontsize=18, fontweight="bold", color="#BDBDBD",
            ha="center", va="center")
    ax.text(8.0, 4.0, "4", fontsize=18, fontweight="bold", color="#BDBDBD",
            ha="center", va="center")

    # ── Objective mapping ────────────────────────────────────────────
    obj_map = [
        (1.8, 0.8, "Obj 1: Feature\nIdentification", "#1565C0"),
        (5.9, 0.8, "Obj 2: Model\nDevelopment", "#2E7D32"),
        (8.3, 0.8, "Obj 3: Evaluation\n& Explainability", "#E65100"),
        (11.0, 0.8, "Obj 4: Decision\nSupport System", "#C62828"),
    ]
    for x, y, txt, col in obj_map:
        rect = FancyBboxPatch((x - 1.0, y - 0.35), 2.0, 0.7,
                               boxstyle="round,pad=0.06", lw=1.0,
                               ec=col, fc=col + "15")
        ax.add_patch(rect)
        ax.text(x, y, txt, ha="center", va="center", fontsize=6.5,
                fontweight="bold", color=col)

    fig.suptitle("High-Level Conceptual Framework of the Explainable\n"
                 "Diabetes Risk Stratification System",
                 fontsize=11, fontweight="bold", y=1.01)
    fig.savefig(os.path.join(OUT, "fig_4_1_conceptual_framework.png"))
    plt.close(fig)
    print("  Figure 4.1 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.2 — Detailed Data Pipeline Process Flow
# ═══════════════════════════════════════════════════════════════════════════

def draw_data_pipeline():
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(-0.5, 14)
    ax.set_ylim(-0.5, 8.5)
    ax.axis("off")

    # ── Phase 1: Ingestion ───────────────────────────────────────────
    phase_colors = ["#1565C0", "#0277BD", "#00838F", "#00695C", "#2E7D32", "#558B2F"]

    # Row 1: Data Ingestion
    y1 = 7.0
    ing_box = FancyBboxPatch((0.3, y1 - 0.5), 4.0, 1.2,
                              boxstyle="round,pad=0.10", lw=1.8,
                              ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(ing_box)
    ax.text(2.3, y1 + 0.35, "Phase 1: Data Ingestion", ha="center",
            fontsize=9, fontweight="bold", color="#1565C0")
    steps_ing = [
        "1.1  pd.read_csv() loads BRFSS 2015 CSV (253,680 rows x 22 cols)",
        "1.2  df.info() and df.describe() for structural inspection",
        "1.3  Verify Diabetes_012 target: {0, 1, 2} distribution",
    ]
    for i, s in enumerate(steps_ing):
        ax.text(0.5, y1 - 0.05 - i * 0.22, s, fontsize=6, color="#37474F")

    ax.annotate("", xy=(4.5, y1), xytext=(4.3, y1),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.5))

    # Quality check
    qc_box = FancyBboxPatch((4.7, y1 - 0.35), 2.5, 0.9,
                             boxstyle="round,pad=0.08", lw=1.2,
                             ec="#0277BD", fc="#E1F5FE")
    ax.add_patch(qc_box)
    ax.text(5.95, y1 + 0.2, "Quality Check", ha="center",
            fontsize=8, fontweight="bold", color="#0277BD")
    ax.text(5.95, y1 - 0.1, "Nulls < 2%, No schema errors\nAll 21 features confirmed",
            ha="center", fontsize=6, color="#37474F")

    ax.annotate("", xy=(7.4, y1), xytext=(7.2, y1),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.5))

    # Feature categorisation
    fc_box = FancyBboxPatch((7.6, y1 - 0.35), 3.2, 0.9,
                             boxstyle="round,pad=0.08", lw=1.2,
                             ec="#00838F", fc="#E0F7FA")
    ax.add_patch(fc_box)
    ax.text(9.2, y1 + 0.2, "Feature Categorisation", ha="center",
            fontsize=8, fontweight="bold", color="#00838F")
    ax.text(9.2, y1 - 0.1, "Clinical (8) | Demographic (4) | Lifestyle (9)",
            ha="center", fontsize=6, color="#37474F")

    # Row 2: Transformation
    y2 = 5.0
    trans_box = FancyBboxPatch((0.3, y2 - 0.6), 12.5, 1.5,
                                boxstyle="round,pad=0.10", lw=1.8,
                                ec="#00695C", fc="#E0F2F1")
    ax.add_patch(trans_box)
    ax.text(6.55, y2 + 0.55, "Phase 2: Data Transformation Pipeline", ha="center",
            fontsize=9, fontweight="bold", color="#00695C")

    # Sub-stages in transformation
    trans_stages = [
        ("Imputation", "Median (continuous)\nMode (categorical)", "#1565C0"),
        ("Outlier\nCapping", "IQR method on BMI\nCap at 1.5xIQR", "#0277BD"),
        ("Feature\nEncoding", "One-hot (nominal)\nOrdinal (ordered)", "#00838F"),
        ("Standard\nScaling", "Z-score via\nStandardScaler", "#00695C"),
        ("Stratified\nSplit", "70% Train\n15% Val / 15% Test", "#2E7D32"),
        ("SMOTE", "Oversample minority\n(Train set only)", "#E65100"),
    ]

    for i, (title, desc, color) in enumerate(trans_stages):
        x = 0.8 + i * 2.1
        rect = FancyBboxPatch((x - 0.45, y2 - 0.4), 1.8, 0.85,
                               boxstyle="round,pad=0.06", lw=1.0,
                               ec=color, fc=color + "12")
        ax.add_patch(rect)
        ax.text(x + 0.45, y2 + 0.1, title, ha="center", va="center",
                fontsize=6.5, fontweight="bold", color=color)
        ax.text(x + 0.45, y2 - 0.22, desc, ha="center", va="center",
                fontsize=5.5, color="#616161", style="italic")
        if i < len(trans_stages) - 1:
            ax.annotate("", xy=(x + 1.55, y2 - 0.05), xytext=(x + 1.35, y2 - 0.05),
                        arrowprops=dict(arrowstyle="-|>", color="#BDBDBD", lw=1.0))

    # Row 3: Feature Engineering
    y3 = 3.0
    fe_box = FancyBboxPatch((0.3, y3 - 0.5), 6.0, 1.2,
                             boxstyle="round,pad=0.10", lw=1.6,
                             ec="#2E7D32", fc="#E8F5E9")
    ax.add_patch(fe_box)
    ax.text(3.3, y3 + 0.35, "Phase 3: Feature Engineering & Selection", ha="center",
            fontsize=9, fontweight="bold", color="#2E7D32")
    fe_items = [
        "3.1  Correlation analysis (Pearson/Spearman) to identify redundancy",
        "3.2  Domain-guided feature grouping (Clinical / Demographic / Lifestyle)",
        "3.3  All 21 features retained after statistical significance testing",
    ]
    for i, f in enumerate(fe_items):
        ax.text(0.5, y3 - 0.05 - i * 0.22, f, fontsize=6, color="#37474F")

    # Output: Model-ready data
    ready_box = FancyBboxPatch((7.5, y3 - 0.4), 5.0, 1.0,
                                boxstyle="round,pad=0.10", lw=2.0,
                                ec="#4CAF50", fc="#C8E6C9")
    ax.add_patch(ready_box)
    ax.text(10.0, y3 + 0.25, "MODEL-READY DATASET", ha="center",
            fontsize=9, fontweight="bold", color="#2E7D32")
    ax.text(10.0, y3 - 0.1, "Balanced, scaled, encoded training data\n"
            "ready for classifier training",
            ha="center", fontsize=6.5, color="#37474F", style="italic")

    ax.annotate("", xy=(7.5, y3 + 0.1), xytext=(6.3, y3 + 0.1),
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.8))

    # Vertical connector arrows
    ax.annotate("", xy=(6.55, y2 + 0.9), xytext=(6.55, y1 - 0.6),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.5))
    ax.annotate("", xy=(3.3, y3 + 0.7), xytext=(3.3, y2 - 0.6),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.5))

    # Technology annotations
    ax.text(11.5, y1 - 0.15, "Python\nPandas", ha="center", fontsize=6,
            color="#78909C", style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="#ECEFF1", ec="#B0BEC5", lw=0.5))
    ax.text(13.0, y2 + 0.1, "scikit-learn\nimbalanced-learn",
            ha="center", fontsize=6, color="#78909C", style="italic",
            bbox=dict(boxstyle="round,pad=0.1", fc="#ECEFF1", ec="#B0BEC5", lw=0.5))

    fig.suptitle("Detailed Data Pipeline Process Design",
                 fontsize=11, fontweight="bold", y=1.01)
    fig.savefig(os.path.join(OUT, "fig_4_2_data_pipeline.png"))
    plt.close(fig)
    print("  Figure 4.2 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.3 — Balanced Random Forest Internal Architecture
# ═══════════════════════════════════════════════════════════════════════════

def draw_brf_architecture():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-1.0, 8.5)
    ax.axis("off")

    # ── Input ────────────────────────────────────────────────────────
    inp = FancyBboxPatch((4.5, 7.0), 4.0, 1.0,
                          boxstyle="round,pad=0.10", lw=2.0,
                          ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(inp)
    ax.text(6.5, 7.7, "Preprocessed Input Features", ha="center",
            fontsize=9, fontweight="bold", color="#1565C0")
    ax.text(6.5, 7.25, "21 Features (Scaled + SMOTE-balanced Training Set)",
            ha="center", fontsize=7, color="#424242")

    # ── Bootstrap Sampling ───────────────────────────────────────────
    boot = FancyBboxPatch((3.5, 5.5), 6.0, 1.0,
                           boxstyle="round,pad=0.10", lw=1.6,
                           ec="#E65100", fc="#FFF3E0")
    ax.add_patch(boot)
    ax.text(6.5, 6.2, "Class-Balanced Bootstrap Sampling", ha="center",
            fontsize=9, fontweight="bold", color="#E65100")
    ax.text(6.5, 5.75, "For each tree: draw equal samples from each class "
            "(majority under-sampled per tree)",
            ha="center", fontsize=6.5, color="#424242")

    ax.annotate("", xy=(6.5, 6.5), xytext=(6.5, 7.0),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.5))

    # ── Individual Trees ─────────────────────────────────────────────
    tree_labels = ["Tree 1", "Tree 2", "Tree 3", "...", f"Tree N"]
    tree_xs = [1.5, 3.5, 5.5, 7.5, 9.5]
    tree_colors = ["#2E7D32", "#388E3C", "#43A047", "#66BB6A", "#81C784"]

    for i, (label, x) in enumerate(zip(tree_labels, tree_xs)):
        if label == "...":
            ax.text(x + 0.6, 4.5, "...", fontsize=20, ha="center",
                    va="center", color="#9E9E9E", fontweight="bold")
            continue
        rect = FancyBboxPatch((x, 3.8), 1.8, 1.3,
                               boxstyle="round,pad=0.08", lw=1.2,
                               ec=tree_colors[i], fc=tree_colors[i] + "18")
        ax.add_patch(rect)
        ax.text(x + 0.9, 4.8, label, ha="center", fontsize=8,
                fontweight="bold", color=tree_colors[i])

        # Internal structure
        ax.text(x + 0.9, 4.35, "Random Feature\nSubset Selection",
                ha="center", fontsize=5.5, color="#616161", style="italic")
        ax.text(x + 0.9, 4.0, "Gini Split Criteria",
                ha="center", fontsize=5.5, color="#616161")

        # Arrow from bootstrap
        ax.annotate("", xy=(x + 0.9, 5.1), xytext=(x + 0.9, 5.5),
                    arrowprops=dict(arrowstyle="-|>", color="#BDBDBD", lw=1.0))

    # ── Aggregation ──────────────────────────────────────────────────
    agg = FancyBboxPatch((3.5, 2.0), 6.0, 1.2,
                          boxstyle="round,pad=0.10", lw=1.8,
                          ec="#6A1B9A", fc="#F3E5F5")
    ax.add_patch(agg)
    ax.text(6.5, 2.9, "Majority Voting Aggregation", ha="center",
            fontsize=9, fontweight="bold", color="#6A1B9A")
    ax.text(6.5, 2.35, "Each tree casts a vote; final class = argmax(votes)\n"
            "Class probabilities = proportion of votes per class",
            ha="center", fontsize=6.5, color="#424242")

    for x in [1.5, 3.5, 5.5, 9.5]:
        ax.annotate("", xy=(6.5, 3.2), xytext=(x + 0.9, 3.8),
                    arrowprops=dict(arrowstyle="-|>", color="#CE93D8", lw=1.0,
                                    shrinkB=5))

    # ── Output Classes ───────────────────────────────────────────────
    classes = [("Class 0\nLow Risk", "#4CAF50"),
               ("Class 1\nModerate Risk", "#FF9800"),
               ("Class 2\nHigh Risk", "#F44336")]
    for j, (label, col) in enumerate(classes):
        x = 2.5 + j * 3.0
        rect = FancyBboxPatch((x, 0.3), 2.2, 0.9,
                               boxstyle="round,pad=0.06", lw=1.4,
                               ec=col, fc=col + "20")
        ax.add_patch(rect)
        ax.text(x + 1.1, 0.75, label, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=col)
        ax.annotate("", xy=(x + 1.1, 1.2), xytext=(6.5, 2.0),
                    arrowprops=dict(arrowstyle="-|>", color="#BDBDBD", lw=1.0,
                                    shrinkB=3))

    # ── Annotations ──────────────────────────────────────────────────
    ax.text(11.8, 5.85, "Key Advantages:", fontsize=7, fontweight="bold",
            color="#37474F")
    advantages = ["Native class imbalance handling",
                  "Robust against overfitting",
                  "Natural feature importance",
                  "No separate SMOTE required"]
    for i, adv in enumerate(advantages):
        ax.text(11.8, 5.45 - i * 0.3, f"- {adv}", fontsize=6, color="#616161")

    fig.suptitle("Internal Architecture of the Balanced Random Forest Classifier",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "fig_4_3_brf_architecture.png"))
    plt.close(fig)
    print("  Figure 4.3 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.4 — XAI Integration Architecture (SHAP + LIME)
# ═══════════════════════════════════════════════════════════════════════════

def draw_xai_architecture():
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(-0.5, 13)
    ax.set_ylim(-0.5, 8)
    ax.axis("off")

    # ── Trained Model ────────────────────────────────────────────────
    model_box = FancyBboxPatch((4.5, 6.0), 4.0, 1.3,
                                boxstyle="round,pad=0.10", lw=2.0,
                                ec="#2E7D32", fc="#E8F5E9")
    ax.add_patch(model_box)
    ax.text(6.5, 6.95, "Trained Balanced Random Forest", ha="center",
            fontsize=9, fontweight="bold", color="#2E7D32")
    ax.text(6.5, 6.35, "Prediction + Probability Scores\n"
            "diabetes_model.joblib",
            ha="center", fontsize=7, color="#424242")

    # ── Patient Input ────────────────────────────────────────────────
    patient_box = FancyBboxPatch((0.3, 6.2), 3.0, 0.9,
                                  boxstyle="round,pad=0.08", lw=1.5,
                                  ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(patient_box)
    ax.text(1.8, 6.85, "Patient Instance", ha="center",
            fontsize=8, fontweight="bold", color="#1565C0")
    ax.text(1.8, 6.45, "Single patient feature vector",
            ha="center", fontsize=6.5, color="#424242")

    ax.annotate("", xy=(4.5, 6.65), xytext=(3.3, 6.65),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.5))

    # ── SHAP Branch (Left) ───────────────────────────────────────────
    shap_header = FancyBboxPatch((0.5, 3.8), 5.0, 1.5,
                                  boxstyle="round,pad=0.10", lw=1.8,
                                  ec="#E65100", fc="#FFF3E0")
    ax.add_patch(shap_header)
    ax.text(3.0, 5.0, "SHAP (SHapley Additive exPlanations)", ha="center",
            fontsize=9, fontweight="bold", color="#E65100")
    shap_items = [
        "1. TreeExplainer computes exact Shapley values",
        "2. Each feature gets a signed contribution value",
        "3. Sum of SHAP values = model output deviation",
    ]
    for i, s in enumerate(shap_items):
        ax.text(0.7, 4.5 - i * 0.25, s, fontsize=6.5, color="#37474F")

    ax.annotate("", xy=(3.0, 5.3), xytext=(5.5, 6.0),
                arrowprops=dict(arrowstyle="-|>", color="#E65100", lw=1.5,
                                connectionstyle="arc3,rad=0.2"))

    # SHAP outputs
    shap_outs = [
        ("Global: Bar Plot", "Mean |SHAP| across\nall test samples", 0.7),
        ("Global: Beeswarm", "Feature value vs.\nSHAP impact", 2.5),
        ("Local: Waterfall", "Per-patient feature\ncontributions", 4.3),
    ]
    for title, desc, x in shap_outs:
        rect = FancyBboxPatch((x, 2.2), 1.6, 1.1,
                               boxstyle="round,pad=0.06", lw=1.0,
                               ec="#FF8F00", fc="#FFF8E1")
        ax.add_patch(rect)
        ax.text(x + 0.8, 3.0, title, ha="center", fontsize=6.5,
                fontweight="bold", color="#E65100")
        ax.text(x + 0.8, 2.55, desc, ha="center", fontsize=5.5,
                color="#757575", style="italic")
        ax.annotate("", xy=(x + 0.8, 3.3), xytext=(x + 0.8, 3.8),
                    arrowprops=dict(arrowstyle="-|>", color="#FFB74D", lw=0.8))

    # ── LIME Branch (Right) ──────────────────────────────────────────
    lime_header = FancyBboxPatch((6.5, 3.8), 5.5, 1.5,
                                  boxstyle="round,pad=0.10", lw=1.8,
                                  ec="#1B5E20", fc="#E8F5E9")
    ax.add_patch(lime_header)
    ax.text(9.25, 5.0, "LIME (Local Interpretable Model-Agnostic)", ha="center",
            fontsize=9, fontweight="bold", color="#1B5E20")
    lime_items = [
        "1. Generate N perturbations around patient instance",
        "2. Weight perturbations by proximity (kernel width)",
        "3. Fit sparse linear model on weighted samples",
    ]
    for i, l in enumerate(lime_items):
        ax.text(6.7, 4.5 - i * 0.25, l, fontsize=6.5, color="#37474F")

    ax.annotate("", xy=(9.25, 5.3), xytext=(7.5, 6.0),
                arrowprops=dict(arrowstyle="-|>", color="#1B5E20", lw=1.5,
                                connectionstyle="arc3,rad=-0.2"))

    # LIME outputs
    lime_outs = [
        ("Local\nExplanation", "Per-feature\nweight & direction", 6.8),
        ("Feature\nHighlighting", "Top positive/negative\ncontributors", 8.6),
        ("Validation", "Cross-check with\nSHAP results", 10.4),
    ]
    for title, desc, x in lime_outs:
        rect = FancyBboxPatch((x, 2.2), 1.6, 1.1,
                               boxstyle="round,pad=0.06", lw=1.0,
                               ec="#66BB6A", fc="#F1F8E9")
        ax.add_patch(rect)
        ax.text(x + 0.8, 3.0, title, ha="center", fontsize=6.5,
                fontweight="bold", color="#1B5E20")
        ax.text(x + 0.8, 2.55, desc, ha="center", fontsize=5.5,
                color="#757575", style="italic")
        ax.annotate("", xy=(x + 0.8, 3.3), xytext=(x + 0.8, 3.8),
                    arrowprops=dict(arrowstyle="-|>", color="#81C784", lw=0.8))

    # ── Unified Output ───────────────────────────────────────────────
    unified = FancyBboxPatch((3.0, 0.3), 7.0, 1.3,
                              boxstyle="round,pad=0.10", lw=2.0,
                              ec="#6A1B9A", fc="#F3E5F5")
    ax.add_patch(unified)
    ax.text(6.5, 1.25, "Unified Explainability Output", ha="center",
            fontsize=9, fontweight="bold", color="#6A1B9A")
    ax.text(6.5, 0.7, "Top-5 Contributing Factors  |  Direction of Influence (+ / -)  |  "
            "Confidence Calibration", ha="center", fontsize=7, color="#424242")

    for x in [1.5, 3.3, 5.1, 7.6, 9.4, 11.2]:
        ax.annotate("", xy=(6.5, 1.6), xytext=(x, 2.2),
                    arrowprops=dict(arrowstyle="-|>", color="#CE93D8", lw=0.8,
                                    shrinkB=3))

    fig.suptitle("XAI Integration Architecture — SHAP and LIME Explanation Pipeline",
                 fontsize=11, fontweight="bold", y=1.01)
    fig.savefig(os.path.join(OUT, "fig_4_4_xai_architecture.png"))
    plt.close(fig)
    print("  Figure 4.4 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.5 — CDSS User Interface Design / Wireframe
# ═══════════════════════════════════════════════════════════════════════════

def draw_ui_wireframe():
    fig, ax = plt.subplots(figsize=(13, 8.5))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # ── Browser frame ────────────────────────────────────────────────
    browser = FancyBboxPatch((0.3, 0.3), 12.4, 8.2,
                              boxstyle="round,pad=0.05", lw=1.5,
                              ec="#BDBDBD", fc="#FAFAFA")
    ax.add_patch(browser)

    # Title bar
    title_bar = FancyBboxPatch((0.3, 7.8), 12.4, 0.7,
                                boxstyle="square,pad=0", lw=0,
                                fc="#37474F")
    ax.add_patch(title_bar)
    ax.text(6.5, 8.15, "UZ | Diabetes Risk Stratification System (DRSS) — Clinician: Dr. M. Muduva",
            ha="center", fontsize=7, color="white", fontweight="bold")

    # Three dots
    for i, col in enumerate(["#F44336", "#FFC107", "#4CAF50"]):
        ax.plot(0.7 + i * 0.25, 8.15, 'o', color=col, markersize=4)

    # ── Left panel: Patient Form ─────────────────────────────────────
    form_panel = FancyBboxPatch((0.5, 0.5), 7.5, 7.1,
                                 boxstyle="round,pad=0.05", lw=1.0,
                                 ec="#E0E0E0", fc="white")
    ax.add_patch(form_panel)
    ax.text(4.25, 7.25, "Patient Clinical Data Form", ha="center",
            fontsize=9, fontweight="bold", color="#1565C0")

    # Form sections
    sections = [
        ("Diagnostic Metrics", ["BMI: [  25.3  ]", "Mental Hlth Days: [  5  ]",
                                "Physical Hlth Days: [  10  ]"], 6.6),
        ("History & Demographics", ["General Health: [3 - Good]", "Age Group: [9 - 60-64]",
                                    "Education: [5 - College]", "Income: [6 - $50-75k]"], 5.4),
        ("Lifestyle Indicators", ["[x] High Blood Pressure", "[x] High Cholesterol",
                                  "[ ] Smoker", "[x] Physical Activity",
                                  "[ ] Heavy Alcohol"], 4.0),
    ]
    for title, fields, y_start in sections:
        ax.text(0.8, y_start + 0.3, title, fontsize=7, fontweight="bold",
                color="#455A64", style="italic")
        ax.plot([0.8, 7.7], [y_start + 0.2, y_start + 0.2], '-', color="#E0E0E0", lw=0.5)
        for j, field in enumerate(fields):
            ax.text(1.0, y_start - 0.1 - j * 0.28, field, fontsize=6, color="#424242",
                    family="monospace")

    # Submit button
    btn = FancyBboxPatch((1.5, 0.8), 5.5, 0.5,
                          boxstyle="round,pad=0.06", lw=1.5,
                          ec="#1565C0", fc="#1976D2")
    ax.add_patch(btn)
    ax.text(4.25, 1.05, "Run Clinical Risk Analysis", ha="center",
            fontsize=8, fontweight="bold", color="white")

    # ── Right panel: Results ─────────────────────────────────────────
    result_panel = FancyBboxPatch((8.2, 0.5), 4.3, 7.1,
                                   boxstyle="round,pad=0.05", lw=1.5,
                                   ec="#FF9800", fc="#FFF8E1")
    ax.add_patch(result_panel)

    # Risk Header
    risk_header = FancyBboxPatch((8.3, 6.5), 4.1, 0.9,
                                  boxstyle="round,pad=0.04", lw=1.2,
                                  ec="#FF9800", fc="#FF9800")
    ax.add_patch(risk_header)
    ax.text(10.35, 7.05, "Risk Stratification Result", ha="center",
            fontsize=8, fontweight="bold", color="white")
    ax.text(10.35, 6.72, "Moderate Risk (Prediabetes)", ha="center",
            fontsize=7, color="white")

    # Confidence
    ax.text(8.5, 6.2, "AI Confidence:", fontsize=7, fontweight="bold",
            color="#424242")
    conf_bg = FancyBboxPatch((8.5, 5.9), 3.7, 0.25,
                              boxstyle="round,pad=0.02", lw=0.5,
                              ec="#E0E0E0", fc="#E0E0E0")
    ax.add_patch(conf_bg)
    conf_fill = FancyBboxPatch((8.5, 5.9), 2.6, 0.25,
                                boxstyle="round,pad=0.02", lw=0,
                                fc="#FF9800")
    ax.add_patch(conf_fill)
    ax.text(12.0, 6.02, "72.3%", fontsize=6.5, fontweight="bold",
            color="#E65100")

    # Recommendation
    rec_box = FancyBboxPatch((8.4, 5.1), 3.9, 0.65,
                              boxstyle="round,pad=0.06", lw=0.8,
                              ec="#FFA726", fc="#FFF3E0")
    ax.add_patch(rec_box)
    ax.text(10.35, 5.55, "Clinical Recommendation:", ha="center",
            fontsize=6.5, fontweight="bold", color="#E65100")
    ax.text(10.35, 5.25, "Transitional stage detected. Proactive\n"
            "intervention recommended (Diet/Exercise).",
            ha="center", fontsize=5.5, color="#424242")

    # XAI Table
    ax.text(8.5, 4.7, "XAI Analysis (Top Contributors)", fontsize=7,
            fontweight="bold", color="#424242")
    ax.plot([8.4, 12.3], [4.55, 4.55], '-', color="#E0E0E0", lw=0.5)

    xai_rows = [
        ("Factor", "Value", "Impact"),
        ("GenHlth", "3", "||||||||"),
        ("BMI", "25.3", "|||||||"),
        ("Age", "9", "||||||"),
        ("HighBP", "1", "|||||"),
        ("PhysHlth", "10", "||||"),
    ]
    for i, (f, v, imp) in enumerate(xai_rows):
        y = 4.35 - i * 0.28
        weight = "bold" if i == 0 else "normal"
        color = "#37474F" if i == 0 else "#424242"
        ax.text(8.5, y, f, fontsize=5.5, fontweight=weight, color=color)
        ax.text(9.8, y, v, fontsize=5.5, fontweight=weight, color=color)
        if i > 0:
            bar_len = (len(imp) / 8.0) * 2.0
            bar = FancyBboxPatch((10.3, y - 0.06), bar_len, 0.12,
                                  boxstyle="round,pad=0.01", lw=0,
                                  fc="#29B6F6")
            ax.add_patch(bar)
        else:
            ax.text(10.3, y, imp, fontsize=5.5, fontweight=weight, color=color)

    fig.suptitle("Clinical Decision-Support System — UI Wireframe Design",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "fig_4_5_ui_wireframe.png"))
    plt.close(fig)
    print("  Figure 4.5 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.6 — Request-Response Interaction Sequence
# ═══════════════════════════════════════════════════════════════════════════

def draw_interaction_sequence():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    # Lifeline positions
    actors = [
        ("Clinician", 1.5, "#1565C0"),
        ("React.js\nFrontend", 4.0, "#0277BD"),
        ("Flask API\nBackend", 7.0, "#2E7D32"),
        ("ML Model\n(BRF)", 9.5, "#6A1B9A"),
        ("XAI Engine\n(SHAP)", 11.5, "#E65100"),
    ]

    # Draw lifelines
    for name, x, color in actors:
        head = FancyBboxPatch((x - 0.6, 7.5), 1.2, 0.7,
                               boxstyle="round,pad=0.06", lw=1.5,
                               ec=color, fc=color + "18")
        ax.add_patch(head)
        ax.text(x, 7.85, name, ha="center", va="center",
                fontsize=7, fontweight="bold", color=color)
        ax.plot([x, x], [0.5, 7.5], '--', color="#BDBDBD", lw=0.8)

    # Messages (from_x, to_x, y, label, color, direction)
    messages = [
        (1.5, 4.0, 6.8, "1. Enter patient data\n    (21 features via form)", "#1565C0", "right"),
        (4.0, 7.0, 6.0, "2. HTTP POST /predict\n    {JSON: feature values}", "#0277BD", "right"),
        (7.0, 7.0, 5.3, "3. Validate & Scale input\n    (scaler.transform())", "#2E7D32", "self"),
        (7.0, 9.5, 4.6, "4. model.predict_proba(X)\n    Get class probabilities", "#2E7D32", "right"),
        (9.5, 7.0, 3.9, "5. Return [P0, P1, P2]\n    & predicted class", "#6A1B9A", "left"),
        (7.0, 11.5, 3.2, "6. Compute SHAP values\n    TreeExplainer(model)", "#2E7D32", "right"),
        (11.5, 7.0, 2.5, "7. Return feature\n    attributions (top-5)", "#E65100", "left"),
        (7.0, 4.0, 1.8, "8. JSON Response: {risk_label,\n    confidence, top_factors}", "#2E7D32", "left"),
        (4.0, 1.5, 1.1, "9. Render risk gauge, XAI\n    table & recommendations", "#0277BD", "left"),
    ]

    for from_x, to_x, y, label, color, direction in messages:
        if direction == "self":
            # Self-call loop
            ax.annotate("", xy=(from_x + 0.5, y - 0.25),
                        xytext=(from_x + 0.5, y + 0.1),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.2,
                                        connectionstyle="arc3,rad=-0.5"))
            ax.text(from_x + 1.0, y - 0.05, label, fontsize=5.5, color=color)
        else:
            ax.annotate("", xy=(to_x, y), xytext=(from_x, y),
                        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))
            mid_x = (from_x + to_x) / 2
            offset = 0.08
            ax.text(mid_x, y + offset, label, ha="center", fontsize=5.5,
                    color=color)

    fig.suptitle("Request-Response Interaction Sequence Diagram",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "fig_4_6_interaction_sequence.png"))
    plt.close(fig)
    print("  Figure 4.6 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 4.7 — Multi-Tier Risk Stratification Logic
# ═══════════════════════════════════════════════════════════════════════════

def draw_risk_stratification_logic():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-0.5, 12)
    ax.set_ylim(-0.5, 7.5)
    ax.axis("off")

    # ── Input ────────────────────────────────────────────────────────
    inp = FancyBboxPatch((3.5, 6.0), 5.0, 0.9,
                          boxstyle="round,pad=0.08", lw=1.8,
                          ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(inp)
    ax.text(6.0, 6.6, "Model Output: Probability Vector", ha="center",
            fontsize=9, fontweight="bold", color="#1565C0")
    ax.text(6.0, 6.2, "[P(Class 0), P(Class 1), P(Class 2)]",
            ha="center", fontsize=7.5, color="#424242", family="monospace")

    # ── Decision node 1: High Risk ───────────────────────────────────
    d1_x, d1_y = 6.0, 4.7
    diamond1 = plt.Polygon([(d1_x, d1_y + 0.5), (d1_x + 1.2, d1_y),
                             (d1_x, d1_y - 0.5), (d1_x - 1.2, d1_y)],
                            closed=True, fc="#FFEBEE", ec="#C62828", lw=1.5)
    ax.add_patch(diamond1)
    ax.text(d1_x, d1_y, "P(Class 2)\n>= 0.40?", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#C62828")

    ax.annotate("", xy=(d1_x, d1_y + 0.5), xytext=(d1_x, 6.0),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3))

    # Yes -> High Risk
    hr_box = FancyBboxPatch((8.5, 4.2), 2.8, 1.0,
                             boxstyle="round,pad=0.08", lw=1.5,
                             ec="#F44336", fc="#FFCDD2")
    ax.add_patch(hr_box)
    ax.text(9.9, 4.9, "HIGH RISK", ha="center", fontsize=8,
            fontweight="bold", color="#C62828")
    ax.text(9.9, 4.5, "Likely Diabetes (Class 2)\nImmediate clinical attention",
            ha="center", fontsize=6, color="#424242")

    ax.annotate("Yes", xy=(8.5, d1_y), xytext=(d1_x + 1.2, d1_y),
                fontsize=7, color="#C62828", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#F44336", lw=1.3))

    # ── Decision node 2: Moderate Risk ───────────────────────────────
    d2_x, d2_y = 6.0, 2.8
    diamond2 = plt.Polygon([(d2_x, d2_y + 0.5), (d2_x + 1.2, d2_y),
                             (d2_x, d2_y - 0.5), (d2_x - 1.2, d2_y)],
                            closed=True, fc="#FFF3E0", ec="#E65100", lw=1.5)
    ax.add_patch(diamond2)
    ax.text(d2_x, d2_y, "P(Class 1)\n>= 0.25?", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#E65100")

    ax.annotate("No", xy=(d2_x, d2_y + 0.5), xytext=(d2_x, d1_y - 0.5),
                fontsize=7, color="#616161", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3))

    # Yes -> Moderate
    mr_box = FancyBboxPatch((8.5, 2.3), 2.8, 1.0,
                             boxstyle="round,pad=0.08", lw=1.5,
                             ec="#FF9800", fc="#FFE0B2")
    ax.add_patch(mr_box)
    ax.text(9.9, 3.0, "MODERATE RISK", ha="center", fontsize=8,
            fontweight="bold", color="#E65100")
    ax.text(9.9, 2.6, "Prediabetes (Class 1)\nProactive intervention",
            ha="center", fontsize=6, color="#424242")

    ax.annotate("Yes", xy=(8.5, d2_y), xytext=(d2_x + 1.2, d2_y),
                fontsize=7, color="#E65100", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#FF9800", lw=1.3))

    # ── Low Risk (default) ───────────────────────────────────────────
    lr_box = FancyBboxPatch((3.5, 0.5), 2.8, 1.0,
                             boxstyle="round,pad=0.08", lw=1.5,
                             ec="#4CAF50", fc="#C8E6C9")
    ax.add_patch(lr_box)
    ax.text(4.9, 1.2, "LOW RISK", ha="center", fontsize=8,
            fontweight="bold", color="#2E7D32")
    ax.text(4.9, 0.8, "No Diabetes (Class 0)\nRoutine monitoring",
            ha="center", fontsize=6, color="#424242")

    ax.annotate("No", xy=(d2_x - 0.3, d2_y - 0.5), xytext=(d2_x, d2_y - 0.5),
                fontsize=7, color="#616161", fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3,
                                connectionstyle="arc3,rad=0.3"))
    ax.annotate("", xy=(4.9, 1.5), xytext=(d2_x - 0.6, d2_y - 0.45),
                arrowprops=dict(arrowstyle="-|>", color="#4CAF50", lw=1.3,
                                connectionstyle="arc3,rad=0.3"))

    # ── Threshold annotations ────────────────────────────────────────
    ax.text(0.5, 5.0, "Threshold Design:\n\n"
            "Class 2 (Diabetes): >= 0.40\n"
            "  Higher threshold to reduce\n"
            "  false alarms for diabetes.\n\n"
            "Class 1 (Prediabetes): >= 0.25\n"
            "  Lower threshold prioritises\n"
            "  sensitivity for early detection.\n\n"
            "Class 0 (Low Risk): Default\n"
            "  If neither threshold is met.",
            fontsize=6.5, color="#37474F", va="top",
            bbox=dict(boxstyle="round,pad=0.2", fc="#ECEFF1", ec="#90A4AE", lw=0.8))

    fig.suptitle("Multi-Tier Risk Stratification Decision Logic",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "fig_4_7_risk_stratification_logic.png"))
    plt.close(fig)
    print("  Figure 4.7 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  Main execution
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Output directory: {OUT}")
    print("=" * 60)
    draw_conceptual_framework()
    draw_data_pipeline()
    draw_brf_architecture()
    draw_xai_architecture()
    draw_ui_wireframe()
    draw_interaction_sequence()
    draw_risk_stratification_logic()
    print("=" * 60)
    print("All 7 Chapter 4 diagrams generated successfully!")
