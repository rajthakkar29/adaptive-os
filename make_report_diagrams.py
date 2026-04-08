from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon


OUTPUT_DIR = Path("report_diagrams")


def setup_figure(title: str, width: float = 14, height: float = 8):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.5,
        0.96,
        title,
        ha="center",
        va="top",
        fontsize=18,
        fontweight="bold",
        color="#1f2937",
    )
    return fig, ax


def draw_box(ax, x, y, w, h, text, facecolor="#eef2ff", edgecolor="#334155", fontsize=11):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.8,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#111827",
        wrap=True,
    )


def draw_diamond(ax, x, y, w, h, text, facecolor="#fff7ed", edgecolor="#b45309", fontsize=11):
    points = [
        (x + w / 2, y + h),
        (x + w, y + h / 2),
        (x + w / 2, y),
        (x, y + h / 2),
    ]
    patch = Polygon(points, closed=True, linewidth=1.8, edgecolor=edgecolor, facecolor=facecolor)
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#111827",
        wrap=True,
    )


def draw_arrow(ax, start, end, text=None, text_offset=(0, 0), color="#475569", connectionstyle="arc3,rad=0"):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", lw=1.8, color=color, connectionstyle=connectionstyle),
    )
    if text:
        ax.text(
            (start[0] + end[0]) / 2 + text_offset[0],
            (start[1] + end[1]) / 2 + text_offset[1],
            text,
            ha="center",
            va="center",
            fontsize=10,
            color=color,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none", alpha=0.85),
        )


def save_figure(fig, stem: str):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def create_architecture_diagram():
    fig, ax = setup_figure("Adaptive-OS System Architecture")

    boxes = [
        (0.03, 0.70, 0.11, 0.12, "User Activity\nSystem State", "#dbeafe", "#1d4ed8"),
        (0.18, 0.70, 0.12, 0.12, "Telemetry\nCollector", "#dcfce7", "#15803d"),
        (0.34, 0.70, 0.12, 0.12, "Preprocess\nFeatures", "#ede9fe", "#7c3aed"),
        (0.50, 0.70, 0.12, 0.12, "Sequence\nBuffer", "#ede9fe", "#7c3aed"),
        (0.66, 0.70, 0.12, 0.12, "LSTM\nModel", "#ffe4e6", "#be123c"),
        (0.82, 0.70, 0.15, 0.12, "Base Risk\nScore", "#fff7ed", "#c2410c"),
        (0.18, 0.36, 0.12, 0.12, "Behavior\nAdjustment", "#fef9c3", "#a16207"),
        (0.34, 0.36, 0.12, 0.12, "Mode\nAdjustment", "#fef9c3", "#a16207"),
        (0.50, 0.36, 0.12, 0.12, "Network\nAdjustment", "#fef9c3", "#a16207"),
        (0.66, 0.36, 0.12, 0.12, "Smoothed\nFinal Risk", "#ffedd5", "#c2410c"),
    ]

    for x, y, w, h, text, fill, edge in boxes:
        draw_box(ax, x, y, w, h, text, facecolor=fill, edgecolor=edge)

    draw_diamond(ax, 0.83, 0.34, 0.14, 0.16, "Security\nTier")

    draw_box(ax, 0.80, 0.10, 0.16, 0.10, "Red Response\nLock + Prompt", facecolor="#fee2e2", edgecolor="#dc2626")
    draw_box(ax, 0.54, 0.10, 0.16, 0.10, "Yellow Response\nWarn / Monitor", facecolor="#fef08a", edgecolor="#ca8a04")
    draw_box(ax, 0.28, 0.10, 0.16, 0.10, "Green Response\nNormal State", facecolor="#dcfce7", edgecolor="#16a34a")

    draw_arrow(ax, (0.14, 0.76), (0.18, 0.76))
    draw_arrow(ax, (0.30, 0.76), (0.34, 0.76))
    draw_arrow(ax, (0.46, 0.76), (0.50, 0.76))
    draw_arrow(ax, (0.62, 0.76), (0.66, 0.76))
    draw_arrow(ax, (0.78, 0.76), (0.82, 0.76))

    draw_arrow(ax, (0.25, 0.70), (0.25, 0.48), connectionstyle="arc3,rad=0")
    draw_arrow(ax, (0.40, 0.70), (0.40, 0.48), connectionstyle="arc3,rad=0")
    draw_arrow(ax, (0.56, 0.70), (0.56, 0.48), connectionstyle="arc3,rad=0")
    draw_arrow(ax, (0.72, 0.70), (0.72, 0.48), connectionstyle="arc3,rad=0")

    draw_arrow(ax, (0.90, 0.34), (0.88, 0.22), text="Red", text_offset=(0.02, 0.02))
    draw_arrow(ax, (0.86, 0.34), (0.62, 0.22), text="Yellow", text_offset=(0.00, 0.02))
    draw_arrow(ax, (0.84, 0.34), (0.36, 0.22), text="Green", text_offset=(-0.01, 0.02))

    draw_arrow(ax, (0.88, 0.20), (0.88, 0.22))
    draw_arrow(ax, (0.62, 0.20), (0.62, 0.22))
    draw_arrow(ax, (0.36, 0.20), (0.36, 0.22))

    save_figure(fig, "01_architecture")


def create_runtime_flow_diagram():
    fig, ax = setup_figure("Adaptive-OS Runtime Decision Flow")

    draw_box(ax, 0.37, 0.84, 0.26, 0.08, "Start inference.py", facecolor="#dbeafe", edgecolor="#1d4ed8")
    draw_box(ax, 0.33, 0.72, 0.34, 0.08, "Load context_model.pth", facecolor="#e0f2fe", edgecolor="#0284c7")
    draw_box(ax, 0.32, 0.60, 0.36, 0.08, "Collect telemetry and preprocess", facecolor="#dcfce7", edgecolor="#15803d")
    draw_box(ax, 0.34, 0.48, 0.32, 0.08, "Append to rolling buffer", facecolor="#ede9fe", edgecolor="#7c3aed")
    draw_diamond(ax, 0.37, 0.33, 0.26, 0.13, "Buffer has\n10 samples?")
    draw_box(ax, 0.33, 0.18, 0.34, 0.08, "Run LSTM inference", facecolor="#ffe4e6", edgecolor="#be123c")
    draw_box(ax, 0.32, 0.06, 0.36, 0.08, "Adjust, clamp, and smooth risk", facecolor="#fff7ed", edgecolor="#c2410c")

    draw_box(ax, 0.04, 0.14, 0.22, 0.09, "Green tier\nWallpaper update", facecolor="#dcfce7", edgecolor="#16a34a", fontsize=10)
    draw_box(ax, 0.04, 0.30, 0.22, 0.09, "Yellow tier\nWallpaper update", facecolor="#fef08a", edgecolor="#ca8a04", fontsize=10)
    draw_box(ax, 0.04, 0.46, 0.22, 0.11, "Red tier\nLock folder if needed\nPrompt for password", facecolor="#fee2e2", edgecolor="#dc2626", fontsize=10)

    draw_arrow(ax, (0.50, 0.84), (0.50, 0.80))
    draw_arrow(ax, (0.50, 0.72), (0.50, 0.68))
    draw_arrow(ax, (0.50, 0.60), (0.50, 0.56))
    draw_arrow(ax, (0.50, 0.48), (0.50, 0.46))
    draw_arrow(ax, (0.50, 0.33), (0.50, 0.26))
    draw_arrow(ax, (0.50, 0.18), (0.50, 0.14))

    draw_arrow(ax, (0.37, 0.40), (0.26, 0.52), text="No", text_offset=(-0.02, 0.02), connectionstyle="arc3,rad=0.1")
    draw_arrow(ax, (0.63, 0.40), (0.52, 0.26), text="Yes", text_offset=(0.02, 0.00), connectionstyle="arc3,rad=-0.1")

    draw_arrow(ax, (0.30, 0.20), (0.26, 0.19))
    draw_arrow(ax, (0.30, 0.36), (0.26, 0.35))
    draw_arrow(ax, (0.30, 0.52), (0.26, 0.50))

    save_figure(fig, "02_runtime_flow")


def create_state_machine_diagram():
    fig, ax = setup_figure("Adaptive-OS Security State Machine")

    nodes = {
        "Green": (0.12, 0.52),
        "Yellow": (0.44, 0.78),
        "Red": (0.76, 0.52),
        "Prompt": (0.44, 0.26),
    }

    draw_box(ax, 0.05, 0.47, 0.14, 0.10, "Green", facecolor="#dcfce7", edgecolor="#16a34a", fontsize=12)
    draw_box(ax, 0.37, 0.73, 0.14, 0.10, "Yellow", facecolor="#fef08a", edgecolor="#ca8a04", fontsize=12)
    draw_box(ax, 0.69, 0.47, 0.14, 0.10, "Red", facecolor="#fee2e2", edgecolor="#dc2626", fontsize=12)
    draw_box(ax, 0.37, 0.21, 0.14, 0.10, "Prompt /\nUnlock", facecolor="#e0f2fe", edgecolor="#0284c7", fontsize=11)

    draw_arrow(ax, (0.19, 0.57), (0.37, 0.78), text="risk rises", text_offset=(-0.02, 0.03), connectionstyle="arc3,rad=0.1")
    draw_arrow(ax, (0.44, 0.73), (0.19, 0.57), text="risk drops", text_offset=(0.00, -0.03), connectionstyle="arc3,rad=0.1")
    draw_arrow(ax, (0.51, 0.78), (0.69, 0.57), text="risk rises", text_offset=(0.02, 0.03), connectionstyle="arc3,rad=-0.1")
    draw_arrow(ax, (0.69, 0.52), (0.51, 0.78), text="unlock success", text_offset=(0.00, 0.05), connectionstyle="arc3,rad=-0.1")
    draw_arrow(ax, (0.76, 0.47), (0.51, 0.31), text="password prompt", text_offset=(0.03, -0.03), connectionstyle="arc3,rad=0.1")
    draw_arrow(ax, (0.44, 0.31), (0.19, 0.57), text="hold ends", text_offset=(-0.01, 0.03), connectionstyle="arc3,rad=0.1")

    ax.text(0.76, 0.40, "folder locked", ha="center", va="center", fontsize=10, color="#dc2626")
    ax.text(0.44, 0.16, "verified unlock returns to a safer state if risk remains low", ha="center", va="center", fontsize=9, color="#0f172a")

    save_figure(fig, "03_state_machine")


def create_training_pipeline_diagram():
    fig, ax = setup_figure("Adaptive-OS Training Pipeline")

    steps = [
        (0.04, 0.52, 0.15, 0.12, "telemetry_logs.json", "#dbeafe", "#1d4ed8"),
        (0.22, 0.52, 0.15, 0.12, "Load and slice\n10-step sequences", "#dcfce7", "#15803d"),
        (0.40, 0.52, 0.15, 0.12, "Preprocess\nfeatures", "#ede9fe", "#7c3aed"),
        (0.58, 0.52, 0.15, 0.12, "Create heuristic\nlabels", "#fef9c3", "#a16207"),
        (0.76, 0.52, 0.15, 0.12, "Train\nContextLSTM", "#ffe4e6", "#be123c"),
        (0.40, 0.22, 0.23, 0.12, "CrossEntropy + MSE loss", "#fff7ed", "#c2410c"),
        (0.68, 0.22, 0.20, 0.12, "Save context_model.pth", "#e0f2fe", "#0284c7"),
    ]

    for x, y, w, h, text, fill, edge in steps:
        draw_box(ax, x, y, w, h, text, facecolor=fill, edgecolor=edge)

    draw_arrow(ax, (0.19, 0.58), (0.22, 0.58))
    draw_arrow(ax, (0.37, 0.58), (0.40, 0.58))
    draw_arrow(ax, (0.55, 0.58), (0.58, 0.58))
    draw_arrow(ax, (0.73, 0.58), (0.76, 0.58))
    draw_arrow(ax, (0.83, 0.52), (0.83, 0.34), connectionstyle="arc3,rad=0")
    draw_arrow(ax, (0.58, 0.22), (0.68, 0.28))

    save_figure(fig, "04_training_pipeline")


def generate_all():
    create_architecture_diagram()
    create_runtime_flow_diagram()
    create_state_machine_diagram()
    create_training_pipeline_diagram()
    print(f"Saved diagrams to {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    generate_all()
