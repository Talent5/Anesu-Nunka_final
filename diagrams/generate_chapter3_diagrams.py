"""
============================================================================
  Generate Academic-Quality Diagrams for Chapter 3: Methodology
  Anesu Nunkha — BSc Capstone Project, University of Zimbabwe
  Explainable ML for Early Diabetes Risk Stratification and Diagnosis
============================================================================
Produces publication-ready figures saved as PNG (300 dpi) for embedding
in the dissertation manuscript.
"""

import matplotlib
matplotlib.use("Agg")                       # non-interactive backend
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
#  FIGURE 3.1 — CRISP-DM Methodology Lifecycle
# ═══════════════════════════════════════════════════════════════════════════

def draw_crisp_dm():
    fig, ax = plt.subplots(figsize=(8.5, 7.5))
    ax.set_xlim(-1.8, 1.8)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect("equal")
    ax.axis("off")

    # Phase definitions (label, short description, angle on circle)
    phases = [
        ("Business\nUnderstanding",   "Define clinical\nobjectives",              90),
        ("Data\nUnderstanding",       "Acquire & explore\nBRFSS 2015 data",       30),
        ("Data\nPreparation",         "Clean, encode,\nSMOTE, scale",            -30),
        ("Modeling",                  "Train LR, RF,\nXGBoost, BRF",             -90),
        ("Evaluation",               "Recall, F1, AUC,\nSHAP & LIME",          -150),
        ("Deployment",               "Flask API +\nReact CDSS",                  150),
    ]

    colors = ["#1565C0", "#0277BD", "#00838F", "#2E7D32", "#6A1B9A", "#C62828"]
    radius = 1.25
    box_w, box_h = 0.55, 0.38

    positions = []
    for i, (label, desc, angle_deg) in enumerate(phases):
        angle = np.radians(angle_deg)
        cx = radius * np.cos(angle)
        cy = radius * np.sin(angle)
        positions.append((cx, cy))

        # Rounded rectangle
        rect = FancyBboxPatch(
            (cx - box_w, cy - box_h), 2 * box_w, 2 * box_h,
            boxstyle="round,pad=0.06", linewidth=1.8,
            edgecolor=colors[i], facecolor=colors[i] + "18"
        )
        ax.add_patch(rect)
        ax.text(cx, cy + 0.10, label, ha="center", va="center",
                fontsize=9, fontweight="bold", color=colors[i])
        ax.text(cx, cy - 0.18, desc, ha="center", va="center",
                fontsize=6.5, color="#424242", style="italic")

    # Curved arrows between consecutive phases
    for i in range(len(phases)):
        j = (i + 1) % len(phases)
        ax.annotate(
            "", xy=positions[j], xytext=positions[i],
            arrowprops=dict(
                arrowstyle="-|>", color="#616161", lw=1.4,
                connectionstyle="arc3,rad=0.20",
                shrinkA=42, shrinkB=42
            )
        )

    # Feedback arrows (Evaluation → Modeling, Evaluation → Data Prep)
    for target_idx, rad in [(3, -0.35), (2, -0.45)]:
        ax.annotate(
            "", xy=positions[target_idx], xytext=positions[4],
            arrowprops=dict(
                arrowstyle="-|>", color="#EF6C00", lw=1.2,
                connectionstyle=f"arc3,rad={rad}",
                shrinkA=42, shrinkB=42, linestyle="dashed"
            )
        )

    # Center label
    ax.text(0, 0.15, "CRISP-DM", ha="center", va="center",
            fontsize=14, fontweight="bold", color="#37474F")
    ax.text(0, -0.10, "Lifecycle", ha="center", va="center",
            fontsize=10, color="#78909C")

    # Legend
    feedback_line = mpatches.FancyArrowPatch((0, 0), (0.3, 0), 
                                              arrowstyle="-|>", color="#EF6C00",
                                              linestyle="dashed", lw=1.2)
    ax.text(-1.55, -1.75, "-->  Sequential flow           - ->  Iterative feedback loop",
            fontsize=7.5, color="#616161", style="italic")

    fig.suptitle("Figure 3.1: CRISP-DM Methodology Lifecycle Adapted\n"
                 "for Diabetes Risk Stratification", fontsize=11,
                 fontweight="bold", y=0.98)
    fig.savefig(os.path.join(OUT, "fig_3_1_crisp_dm.png"))
    plt.close(fig)
    print("✓  Figure 3.1 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 3.2 — Data Preprocessing Pipeline
# ═══════════════════════════════════════════════════════════════════════════

def draw_preprocessing_pipeline():
    fig, ax = plt.subplots(figsize=(14, 4.5))
    ax.set_xlim(-0.5, 13.5)
    ax.set_ylim(-1.5, 3.2)
    ax.axis("off")

    stages = [
        ("Raw BRFSS\nDataset",       "253,680 rows\n22 variables",    "#78909C"),
        ("Missing Value\nImputation", "Median / Mode\n< 2% missing",  "#1565C0"),
        ("Outlier\nHandling",         "IQR capping\non BMI",           "#0277BD"),
        ("Feature\nEncoding",         "One-hot &\nOrdinal",            "#00838F"),
        ("Feature\nScaling",          "StandardScaler\n(Z-score)",     "#00695C"),
        ("Data\nPartitioning",        "70 / 15 / 15\nStratified",      "#2E7D32"),
        ("SMOTE\nBalancing",          "Oversample\nminority classes",  "#E65100"),
        ("Model-Ready\nData",         "Balanced\ntrain set",           "#4CAF50"),
    ]

    bw, bh = 1.3, 1.1
    y_center = 1.0

    for i, (title, desc, color) in enumerate(stages):
        x = i * 1.7 + 0.2
        rect = FancyBboxPatch(
            (x - bw/2, y_center - bh/2), bw, bh,
            boxstyle="round,pad=0.08", linewidth=1.6,
            edgecolor=color, facecolor=color + "15"
        )
        ax.add_patch(rect)
        ax.text(x, y_center + 0.20, title, ha="center", va="center",
                fontsize=8, fontweight="bold", color=color)
        ax.text(x, y_center - 0.25, desc, ha="center", va="center",
                fontsize=6.5, color="#555555", style="italic")

        # Arrow to next stage
        if i < len(stages) - 1:
            ax.annotate(
                "", xy=(x + bw/2 + 0.12, y_center),
                xytext=(x + bw/2 + 0.02, y_center),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3)
            )

    # Branch annotation: SMOTE applied only to training set
    x_split = 5 * 1.7 + 0.2
    ax.annotate("Applied only to\nTraining Set",
                xy=(x_split + 0.65, y_center - 0.35),
                xytext=(x_split + 0.3, y_center - 1.1),
                fontsize=6.5, color="#BF360C", style="italic",
                arrowprops=dict(arrowstyle="->", color="#BF360C", lw=0.8))

    fig.suptitle("Figure 3.2: Data Preprocessing and Transformation Pipeline",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.savefig(os.path.join(OUT, "fig_3_2_preprocessing_pipeline.png"))
    plt.close(fig)
    print("✓  Figure 3.2 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 3.3 — Model Selection & Comparative Architecture
# ═══════════════════════════════════════════════════════════════════════════

def draw_model_architecture():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(-1.5, 7.5)
    ax.axis("off")

    # ── Input layer ─────────────────────────────────────────────────
    input_box = FancyBboxPatch((0, 5.5), 2.8, 1.5,
                                boxstyle="round,pad=0.1", lw=1.5,
                                ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(input_box)
    ax.text(1.4, 6.6, "Input Features", ha="center", fontsize=9,
            fontweight="bold", color="#1565C0")
    ax.text(1.4, 6.15, "21 Clinical, Demographic\n& Lifestyle Variables",
            ha="center", fontsize=7, color="#424242")
    ax.text(1.4, 5.7, "(Scaled & SMOTE-balanced)",
            ha="center", fontsize=6.5, color="#757575", style="italic")

    # ── Four candidate models ───────────────────────────────────────
    models = [
        ("Logistic\nRegression",  "#7986CB", "Baseline\n(Linear)"),
        ("Random\nForest",        "#4DB6AC", "Ensemble\n(Bagging)"),
        ("XGBoost",               "#FFB74D", "Gradient\nBoosting"),
        ("Balanced\nRandom Forest","#66BB6A", "Imbalance-\nAware Ensemble"),
    ]

    model_xs = [3.8, 5.6, 7.4, 9.2]
    for i, (name, color, note) in enumerate(models):
        x = model_xs[i]
        rect = FancyBboxPatch((x - 0.75, 4.6), 1.5, 2.0,
                               boxstyle="round,pad=0.08", lw=1.5,
                               ec=color, fc=color + "20")
        ax.add_patch(rect)
        ax.text(x, 6.0, name, ha="center", va="center", fontsize=8,
                fontweight="bold", color=color)
        ax.text(x, 5.15, note, ha="center", va="center", fontsize=6.5,
                color="#616161", style="italic")

        # Star the best model
        if "Balanced" in name:
            ax.text(x, 6.8, "[Primary]", ha="center", fontsize=7,
                    fontweight="bold", color="#2E7D32")

        # Arrow from input
        ax.annotate("", xy=(x, 6.6), xytext=(2.8, 6.25),
                    arrowprops=dict(arrowstyle="-|>", color="#90A4AE",
                                    lw=1.0, connectionstyle="arc3,rad=0.1",
                                    shrinkB=15))

    # ── Comparison / Selection box ──────────────────────────────────
    comp_box = FancyBboxPatch((4.5, 2.8), 3.0, 1.2,
                               boxstyle="round,pad=0.10", lw=1.6,
                               ec="#5E35B1", fc="#EDE7F6")
    ax.add_patch(comp_box)
    ax.text(6.0, 3.7, "Model Comparison", ha="center", fontsize=9,
            fontweight="bold", color="#5E35B1")
    ax.text(6.0, 3.15, "Recall · F1-Score · AUC-ROC\n5-Fold Cross-Validation",
            ha="center", fontsize=7, color="#424242")

    for x in model_xs:
        ax.annotate("", xy=(6.0, 4.0), xytext=(x, 4.6),
                    arrowprops=dict(arrowstyle="-|>", color="#90A4AE",
                                    lw=1.0, shrinkA=3, shrinkB=8))

    # ── Best model output ───────────────────────────────────────────
    best_box = FancyBboxPatch((4.5, 0.8), 3.0, 1.3,
                               boxstyle="round,pad=0.10", lw=1.8,
                               ec="#2E7D32", fc="#E8F5E9")
    ax.add_patch(best_box)
    ax.text(6.0, 1.8, "Best Model Selected", ha="center", fontsize=9,
            fontweight="bold", color="#2E7D32")
    ax.text(6.0, 1.2, "Balanced Random Forest\n+ SHAP / LIME Explainability",
            ha="center", fontsize=7.5, color="#424242")

    ax.annotate("", xy=(6.0, 2.1), xytext=(6.0, 2.8),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.4))

    # ── Output classes ──────────────────────────────────────────────
    risk_labels = [("Low Risk\n(Class 0)", "#4CAF50"),
                   ("Moderate Risk\n(Class 1)", "#FF9800"),
                   ("High Risk\n(Class 2)", "#F44336")]
    for j, (label, col) in enumerate(risk_labels):
        x = 3.5 + j * 2.5
        rect = FancyBboxPatch((x - 0.7, -0.7), 1.4, 0.9,
                               boxstyle="round,pad=0.06", lw=1.3,
                               ec=col, fc=col + "20")
        ax.add_patch(rect)
        ax.text(x, -0.25, label, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=col)
        ax.annotate("", xy=(x, -0.0), xytext=(6.0, 0.8),
                    arrowprops=dict(arrowstyle="-|>", color="#BDBDBD",
                                    lw=1.0, shrinkB=5))

    fig.suptitle("Figure 3.3: Model Selection and Comparative Architecture",
                 fontsize=11, fontweight="bold", y=0.98)
    fig.savefig(os.path.join(OUT, "fig_3_3_model_architecture.png"))
    plt.close(fig)
    print("✓  Figure 3.3 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 3.4 — Evaluation Framework
# ═══════════════════════════════════════════════════════════════════════════

def draw_evaluation_framework():
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.5)
    ax.axis("off")

    # ── Model box ────────────────────────────────────────────────────
    model_box = FancyBboxPatch((0.3, 4.0), 2.2, 1.6,
                                boxstyle="round,pad=0.10", lw=1.6,
                                ec="#2E7D32", fc="#E8F5E9")
    ax.add_patch(model_box)
    ax.text(1.4, 5.15, "Trained Model", ha="center", fontsize=9,
            fontweight="bold", color="#2E7D32")
    ax.text(1.4, 4.55, "Balanced Random\nForest Classifier",
            ha="center", fontsize=7, color="#424242")

    # ── Test data ────────────────────────────────────────────────────
    test_box = FancyBboxPatch((0.3, 1.8), 2.2, 1.4,
                               boxstyle="round,pad=0.10", lw=1.5,
                               ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(test_box)
    ax.text(1.4, 2.85, "Test Set", ha="center", fontsize=9,
            fontweight="bold", color="#1565C0")
    ax.text(1.4, 2.25, "15% Hold-out\n(Unseen data)",
            ha="center", fontsize=7, color="#424242")

    ax.annotate("Predict", xy=(2.5, 3.6), xytext=(1.4, 3.2),
                fontsize=7, color="#616161",
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.2))

    # ── PERFORMANCE METRICS (left branch) ────────────────────────────
    perf_header = FancyBboxPatch((3.5, 4.6), 2.8, 0.9,
                                  boxstyle="round,pad=0.08", lw=1.4,
                                  ec="#6A1B9A", fc="#F3E5F5")
    ax.add_patch(perf_header)
    ax.text(4.9, 5.3, "Performance Metrics", ha="center", fontsize=9,
            fontweight="bold", color="#6A1B9A")
    ax.text(4.9, 4.85, "(Objective 3)", ha="center", fontsize=7,
            color="#9575CD", style="italic")

    metrics = [
        ("Recall\n(Sensitivity)", "Minimize\nmissed cases"),
        ("F1-Score\n(Macro Avg)", "Balance precision\n& recall"),
        ("AUC-ROC\n(One-vs-Rest)", "Discriminative\npower"),
        ("Confusion\nMatrix",     "Per-class error\nanalysis"),
    ]

    for k, (metric, desc) in enumerate(metrics):
        y = 3.8 - k * 1.1
        rect = FancyBboxPatch((3.6, y - 0.35), 2.6, 0.7,
                               boxstyle="round,pad=0.06", lw=1.0,
                               ec="#CE93D8", fc="#FCE4EC08")
        ax.add_patch(rect)
        ax.text(4.3, y, metric, ha="center", va="center",
                fontsize=7, fontweight="bold", color="#6A1B9A")
        ax.text(5.6, y, desc, ha="center", va="center",
                fontsize=6.5, color="#757575", style="italic")

    ax.annotate("", xy=(3.5, 5.0), xytext=(2.5, 4.8),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.2))

    # ── EXPLAINABILITY (right branch) ────────────────────────────────
    xai_header = FancyBboxPatch((7.2, 4.6), 2.8, 0.9,
                                 boxstyle="round,pad=0.08", lw=1.4,
                                 ec="#E65100", fc="#FFF3E0")
    ax.add_patch(xai_header)
    ax.text(8.6, 5.3, "Explainability", ha="center", fontsize=9,
            fontweight="bold", color="#E65100")
    ax.text(8.6, 4.85, "(Hypothesis Testing)", ha="center", fontsize=7,
            color="#FB8C00", style="italic")

    xai_items = [
        ("SHAP\n(Global)", "Feature importance\nacross all patients"),
        ("SHAP\n(Local)", "Individual prediction\nwaterfall plots"),
        ("LIME", "Local surrogate\nmodel explanations"),
    ]

    for k, (xai, desc) in enumerate(xai_items):
        y = 3.8 - k * 1.1
        rect = FancyBboxPatch((7.3, y - 0.35), 2.6, 0.7,
                               boxstyle="round,pad=0.06", lw=1.0,
                               ec="#FFB74D", fc="#FFF8E108")
        ax.add_patch(rect)
        ax.text(8.0, y, xai, ha="center", va="center",
                fontsize=7, fontweight="bold", color="#E65100")
        ax.text(9.3, y, desc, ha="center", va="center",
                fontsize=6.5, color="#757575", style="italic")

    ax.annotate("", xy=(7.2, 5.0), xytext=(6.3, 5.0),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.2))

    # ── Connecting bracket ───────────────────────────────────────────
    ax.annotate("", xy=(6.3, 5.0), xytext=(2.5, 4.8),
                arrowprops=dict(arrowstyle="-", color="#616161", lw=1.0,
                                connectionstyle="arc3,rad=0"))

    fig.suptitle("Figure 3.4: Model Evaluation and Explainability Framework",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "fig_3_4_evaluation_framework.png"))
    plt.close(fig)
    print("✓  Figure 3.4 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 3.5 — System Architecture (Decision-Support System)
# ═══════════════════════════════════════════════════════════════════════════

def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-0.5, 8.5)
    ax.axis("off")

    # ── Clinician / User ─────────────────────────────────────────────
    user_box = FancyBboxPatch((0.2, 6.0), 2.5, 1.8,
                               boxstyle="round,pad=0.12", lw=2.0,
                               ec="#1565C0", fc="#E3F2FD")
    ax.add_patch(user_box)
    ax.text(1.45, 7.35, "Clinician", ha="center", fontsize=10,
            fontweight="bold", color="#1565C0")
    ax.text(1.45, 6.65, "Enters patient data:\nBMI, Age, BP, Lifestyle\nvia web form",
            ha="center", fontsize=7, color="#424242")

    # ── Frontend ─────────────────────────────────────────────────────
    fe_box = FancyBboxPatch((3.8, 5.5), 3.2, 2.8,
                             boxstyle="round,pad=0.12", lw=1.8,
                             ec="#0277BD", fc="#E1F5FE")
    ax.add_patch(fe_box)
    ax.text(5.4, 7.8, "Frontend Layer", ha="center", fontsize=10,
            fontweight="bold", color="#0277BD")
    ax.text(5.4, 7.3, "React.js + Vite + Bootstrap", ha="center",
            fontsize=7, color="#0277BD", style="italic")
    fe_features = ["• Patient input form (21 features)",
                   "• Risk gauge & color indicator",
                   "• XAI feature-importance table",
                   "• Clinical recommendation panel"]
    for i, f in enumerate(fe_features):
        ax.text(4.05, 6.75 - i * 0.35, f, fontsize=6.5, color="#37474F")

    ax.annotate("", xy=(3.8, 6.9), xytext=(2.7, 6.9),
                arrowprops=dict(arrowstyle="<|-|>", color="#1565C0", lw=1.5))

    # ── Backend ──────────────────────────────────────────────────────
    be_box = FancyBboxPatch((3.8, 1.8), 3.2, 3.0,
                             boxstyle="round,pad=0.12", lw=1.8,
                             ec="#2E7D32", fc="#E8F5E9")
    ax.add_patch(be_box)
    ax.text(5.4, 4.4, "Backend API Layer", ha="center", fontsize=10,
            fontweight="bold", color="#2E7D32")
    ax.text(5.4, 3.95, "Python Flask RESTful API", ha="center",
            fontsize=7, color="#2E7D32", style="italic")
    be_features = ["• /predict endpoint (POST)",
                   "• Data validation & scaling",
                   "• Model inference pipeline",
                   "• SHAP value computation",
                   "• Risk tier mapping logic"]
    for i, f in enumerate(be_features):
        ax.text(4.05, 3.45 - i * 0.32, f, fontsize=6.5, color="#37474F")

    ax.annotate("JSON\nrequest", xy=(5.4, 4.8), xytext=(5.4, 5.5),
                fontsize=7, color="#616161", ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3))
    ax.annotate("JSON\nresponse", xy=(5.4, 5.5), xytext=(6.6, 5.15),
                fontsize=7, color="#616161", ha="center",
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3,
                                connectionstyle="arc3,rad=-0.3"))

    # ── ML Model artifacts ───────────────────────────────────────────
    ml_box = FancyBboxPatch((8.0, 3.3), 3.8, 2.9,
                             boxstyle="round,pad=0.12", lw=1.8,
                             ec="#6A1B9A", fc="#F3E5F5")
    ax.add_patch(ml_box)
    ax.text(9.9, 5.8, "ML Model Layer", ha="center", fontsize=10,
            fontweight="bold", color="#6A1B9A")
    ax.text(9.9, 5.35, "Serialized Artifacts (.joblib)", ha="center",
            fontsize=7, color="#6A1B9A", style="italic")

    artifacts = [
        ("diabetes_model.joblib", "Balanced Random Forest"),
        ("scaler.joblib",         "StandardScaler transform"),
        ("feature_names.joblib",  "Feature ordering metadata"),
    ]
    for i, (fname, desc) in enumerate(artifacts):
        y = 4.8 - i * 0.55
        rect = FancyBboxPatch((8.2, y - 0.2), 3.4, 0.45,
                               boxstyle="round,pad=0.04", lw=0.8,
                               ec="#CE93D8", fc="#F3E5F520")
        ax.add_patch(rect)
        ax.text(9.0, y, fname, fontsize=6.5, fontweight="bold",
                color="#4A148C", va="center")
        ax.text(11.0, y, desc, fontsize=6, color="#757575",
                va="center", style="italic")

    ax.annotate("Load\nmodel", xy=(8.0, 4.5), xytext=(7.0, 3.5),
                fontsize=7, color="#6A1B9A",
                arrowprops=dict(arrowstyle="-|>", color="#6A1B9A", lw=1.2))

    # ── XAI Engine ───────────────────────────────────────────────────
    xai_box = FancyBboxPatch((8.0, 0.5), 3.8, 2.2,
                              boxstyle="round,pad=0.10", lw=1.6,
                              ec="#E65100", fc="#FFF3E0")
    ax.add_patch(xai_box)
    ax.text(9.9, 2.3, "XAI Engine", ha="center", fontsize=10,
            fontweight="bold", color="#E65100")
    ax.text(9.9, 1.8, "SHAP + LIME Explainability", ha="center",
            fontsize=7, color="#E65100", style="italic")
    xai_items = ["• Global feature importance (SHAP bar)",
                 "• Local explanation (SHAP waterfall)",
                 "• Surrogate model (LIME)"]
    for i, item in enumerate(xai_items):
        ax.text(8.25, 1.35 - i * 0.3, item, fontsize=6.5, color="#37474F")

    ax.annotate("Explain\nprediction", xy=(8.0, 1.5), xytext=(7.0, 2.5),
                fontsize=7, color="#E65100",
                arrowprops=dict(arrowstyle="-|>", color="#E65100", lw=1.2))

    # ── Output ───────────────────────────────────────────────────────
    out_box = FancyBboxPatch((0.2, 0.5), 2.5, 2.5,
                              boxstyle="round,pad=0.10", lw=1.8,
                              ec="#C62828", fc="#FFEBEE")
    ax.add_patch(out_box)
    ax.text(1.45, 2.6, "Clinical Output", ha="center", fontsize=10,
            fontweight="bold", color="#C62828")
    out_items = ["Risk Category:\n  Low / Moderate / High",
                 "Probability Scores:\n  [0.12, 0.65, 0.23]",
                 "Top-5 Risk Factors:\n  with SHAP values"]
    y_start = 2.1
    for i, item in enumerate(out_items):
        ax.text(0.45, y_start - i * 0.55, item, fontsize=6.5, color="#424242")

    ax.annotate("", xy=(2.7, 1.75), xytext=(3.8, 2.5),
                arrowprops=dict(arrowstyle="-|>", color="#C62828", lw=1.4))

    fig.suptitle("Figure 3.5: System Architecture — Clinical Decision-Support System (CDSS)",
                 fontsize=11, fontweight="bold", y=0.99)
    fig.savefig(os.path.join(OUT, "fig_3_5_system_architecture.png"))
    plt.close(fig)
    print("✓  Figure 3.5 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 3.6 — End-to-End Research Pipeline Overview
# ═══════════════════════════════════════════════════════════════════════════

def draw_research_pipeline():
    fig, ax = plt.subplots(figsize=(14, 5.5))
    ax.set_xlim(-0.5, 14)
    ax.set_ylim(-1.2, 4.5)
    ax.axis("off")

    stages = [
        ("Problem\nDefinition",
         "Clinical need for\nearly risk stratification",
         "#37474F", "Obj 1-4"),
        ("Data\nAcquisition",
         "BRFSS 2015 dataset\n253,680 records",
         "#1565C0", "Obj 1"),
        ("Feature\nAnalysis",
         "Clinical, demographic\n& lifestyle features",
         "#0277BD", "Obj 1"),
        ("Data\nPreprocessing",
         "Clean, encode, scale\nSMOTE balancing",
         "#00838F", "Obj 2"),
        ("Model\nDevelopment",
         "LR, RF, XGBoost\nBalanced RF",
         "#2E7D32", "Obj 2"),
        ("Model\nEvaluation",
         "Recall, F1, AUC\nConfusion matrix",
         "#6A1B9A", "Obj 3"),
        ("Explainability\n(XAI)",
         "SHAP global/local\nLIME explanations",
         "#E65100", "Obj 3"),
        ("CDSS\nDeployment",
         "Flask API +\nReact interface",
         "#C62828", "Obj 4"),
    ]

    bw, bh = 1.35, 1.4
    y_center = 2.0

    for i, (title, desc, color, obj) in enumerate(stages):
        x = i * 1.7 + 0.3
        rect = FancyBboxPatch(
            (x - bw/2, y_center - bh/2), bw, bh,
            boxstyle="round,pad=0.08", linewidth=1.6,
            edgecolor=color, facecolor=color + "15"
        )
        ax.add_patch(rect)
        ax.text(x, y_center + 0.30, title, ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=color)
        ax.text(x, y_center - 0.25, desc, ha="center", va="center",
                fontsize=6, color="#555555", style="italic")

        # Objective badge
        badge = FancyBboxPatch((x - 0.35, y_center + 0.75), 0.7, 0.32,
                                boxstyle="round,pad=0.04", lw=0.8,
                                ec=color, fc=color + "30")
        ax.add_patch(badge)
        ax.text(x, y_center + 0.91, obj, ha="center", va="center",
                fontsize=6, fontweight="bold", color=color)

        # Arrow
        if i < len(stages) - 1:
            ax.annotate(
                "", xy=(x + bw/2 + 0.12, y_center),
                xytext=(x + bw/2 + 0.02, y_center),
                arrowprops=dict(arrowstyle="-|>", color="#616161", lw=1.3)
            )

    # Research question mapping at the bottom
    rq_map = [
        (1.65, "RQ1: Which features\nare most relevant?"),
        (5.05, "RQ2: How to develop\nmulti-tier ML model?"),
        (8.45, "RQ3: How does the\nmodel perform?"),
        (11.85, "RQ4: How to implement\nas CDSS?"),
    ]
    for xr, txt in rq_map:
        ax.text(xr, -0.5, txt, ha="center", fontsize=6.5,
                color="#455A64", style="italic",
                bbox=dict(boxstyle="round,pad=0.15", fc="#ECEFF1",
                          ec="#90A4AE", lw=0.6))

    fig.suptitle("Figure 3.6: End-to-End Research Methodology Pipeline\n"
                 "Mapped to Research Objectives and Questions",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.savefig(os.path.join(OUT, "fig_3_6_research_pipeline.png"))
    plt.close(fig)
    print("✓  Figure 3.6 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 3.7 — SMOTE Class Balancing Illustration
# ═══════════════════════════════════════════════════════════════════════════

def draw_smote_illustration():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # ── Before SMOTE ──────────────────────────────────────────────────
    labels_before = ["No Diabetes\n(Class 0)", "Prediabetes\n(Class 1)", "Diabetes\n(Class 2)"]
    counts_before = [213703, 4631, 35346]
    colors = ["#4CAF50", "#FF9800", "#F44336"]

    bars1 = axes[0].bar(labels_before, counts_before, color=colors,
                         edgecolor="#424242", linewidth=0.8, width=0.6)
    axes[0].set_title("(a) Before SMOTE", fontsize=10, fontweight="bold",
                       color="#37474F", pad=10)
    axes[0].set_ylabel("Number of Samples", fontsize=8)
    axes[0].set_ylim(0, 250000)
    for bar, count in zip(bars1, counts_before):
        axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3000,
                     f"{count:,}", ha="center", fontsize=7.5, fontweight="bold")
    axes[0].text(0.5, 0.92, "Severe imbalance: Class 1 = 1.8%",
                 transform=axes[0].transAxes, ha="center", fontsize=7,
                 color="#BF360C", style="italic",
                 bbox=dict(boxstyle="round", fc="#FFF3E0", ec="#E65100", lw=0.6))

    # ── After SMOTE ───────────────────────────────────────────────────
    balanced_count = 149592  # approximate after SMOTE on train set
    counts_after = [balanced_count, balanced_count, balanced_count]

    bars2 = axes[1].bar(labels_before, counts_after, color=colors,
                         edgecolor="#424242", linewidth=0.8, width=0.6)
    axes[1].set_title("(b) After SMOTE (Training Set Only)", fontsize=10,
                       fontweight="bold", color="#37474F", pad=10)
    axes[1].set_ylabel("Number of Samples", fontsize=8)
    axes[1].set_ylim(0, 250000)
    for bar, count in zip(bars2, counts_after):
        axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 3000,
                     f"~{count:,}", ha="center", fontsize=7.5, fontweight="bold")
    axes[1].text(0.5, 0.92, "Balanced: each class ≈ 33.3%",
                 transform=axes[1].transAxes, ha="center", fontsize=7,
                 color="#2E7D32", style="italic",
                 bbox=dict(boxstyle="round", fc="#E8F5E9", ec="#2E7D32", lw=0.6))

    for a in axes:
        a.spines["top"].set_visible(False)
        a.spines["right"].set_visible(False)
        a.tick_params(axis="both", labelsize=7.5)

    fig.suptitle("Figure 3.7: Effect of SMOTE Oversampling on Class Distribution",
                 fontsize=11, fontweight="bold", y=1.03)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_3_7_smote_balancing.png"))
    plt.close(fig)
    print("✓  Figure 3.7 saved")


# ═══════════════════════════════════════════════════════════════════════════
#  Main execution
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Output directory: {OUT}")
    print("=" * 60)
    draw_crisp_dm()
    draw_preprocessing_pipeline()
    draw_model_architecture()
    draw_evaluation_framework()
    draw_system_architecture()
    draw_research_pipeline()
    draw_smote_illustration()
    print("=" * 60)
    print("All 7 diagrams generated successfully!")
