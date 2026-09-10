"""
================================================================================
 FRACTAL DESIGN — "Cosmic Convergence"
 A Mandelbrot Set rendered with a custom color gradient, built for
 Design Lab 01 (Designing Using Fractals).

 Author:  <YOUR NAME HERE>
 Reg #:   <YOUR REGISTRATION NUMBER HERE>
 Course:  BS(CS) — Design Lab 01

 HOW TO RUN ON GOOGLE COLAB
 --------------------------
 1. Open https://colab.research.google.com and start a New Notebook.
 2. Copy this ENTIRE file into a single code cell (or upload it and
    run `!python fractal_design.py`).
 3. Press Shift+Enter / click Run. No installs needed — numpy and
    matplotlib both ship with Colab by default.
 4. One file will be produced in the Colab file browser (left sidebar,
    folder icon):
        - cosmic_convergence.png   (the final fractal design)
    Right-click it to download, or use the auto-download call at the
    very bottom of this script (it only runs inside Colab).

 WHAT THIS SCRIPT DEMONSTRATES
 ------------------------------
 - Self-similarity & iteration: the Mandelbrot escape-time algorithm.
 - A custom, hand-built color gradient (not a built-in matplotlib cmap).
 - Smooth (continuous) coloring so the bands don't look stepped/banded.
 - Gamma correction to bring out fine boundary detail.
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# ------------------------------------------------------------------
# 1. CUSTOM COLOR GRADIENT
#    A hand-tuned palette: deep space navy -> violet -> magenta ->
#    ember orange -> pale gold, so escape-time bands read like a
#    nebula rather than a default rainbow LUT.
# ------------------------------------------------------------------
COSMIC_COLORS = [
    (0.00, "#020111"),  # near-black navy (points inside the set / slow escape)
    (0.16, "#191654"),  # deep indigo
    (0.35, "#3F1D6B"),  # violet
    (0.52, "#9A2EA8"),  # magenta
    (0.68, "#E4467C"),  # rose
    (0.82, "#F98C4A"),  # ember orange
    (0.93, "#FCD86A"),  # gold
    (1.00, "#FFFDF4"),  # near-white (fastest escape / rim of the set)
]
cosmic_cmap = LinearSegmentedColormap.from_list(
    "cosmic", [c for _, c in COSMIC_COLORS], N=1024
)


# ------------------------------------------------------------------
# 2. ESCAPE-TIME FRACTAL ENGINES (vectorized with NumPy — fast enough
#    for interactive use even at high resolution)
# ------------------------------------------------------------------
def mandelbrot(width, height, x_center, y_center, zoom, max_iter=300):
    """Compute a smooth-shaded Mandelbrot set around (x_center, y_center)."""
    x_range = 3.5 / zoom
    y_range = x_range * height / width

    x = np.linspace(x_center - x_range / 2, x_center + x_range / 2, width)
    y = np.linspace(y_center - y_range / 2, y_center + y_range / 2, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y

    Z = np.zeros_like(C)
    div_time = np.zeros(C.shape, dtype=float)
    mask = np.ones(C.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        escaped = np.abs(Z) > 2
        newly_escaped = escaped & mask
        # smooth coloring formula (avoids visible "banding")
        div_time[newly_escaped] = (
            i + 1 - np.log(np.log(np.abs(Z[newly_escaped]) + 1e-12)) / np.log(2)
        )
        mask &= ~escaped
        if not mask.any():
            break

    div_time[mask] = 0  # points that never escaped -> inside the set
    div_time = np.clip(div_time, 0, max_iter)
    return div_time / div_time.max()


# ------------------------------------------------------------------
# 3. THE FINAL FRACTAL DESIGN (single PNG)
#    One clean, high-resolution Mandelbrot render with the custom
#    color gradient and gamma correction applied.
# ------------------------------------------------------------------
def render_fractal(save_path="cosmic_convergence.png"):
    print("Rendering Mandelbrot set...")
    mandel = mandelbrot(1800, 1800, x_center=-0.5, y_center=0.0, zoom=1.0, max_iter=400)

    # Gamma correction brightens the mid-tones so the delicate boundary
    # detail reads clearly instead of being crushed toward black.
    mandel_display = mandel ** 0.45

    fig, ax = plt.subplots(figsize=(10, 10), facecolor="#020111")
    ax.imshow(mandel_display, cmap=cosmic_cmap, extent=[-2.75, 1.25, -2.0, 2.0], origin="lower")
    ax.axis("off")

    fig.text(
        0.5, 0.965, "COSMIC CONVERGENCE",
        color="#FCD86A", fontsize=17, ha="center", fontfamily="serif", weight="bold"
    )
    fig.text(
        0.5, 0.945, "A Mandelbrot Set Fractal Design",
        color="#E4467C", fontsize=10, ha="center", fontfamily="serif"
    )

    plt.savefig(save_path, dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.show()
    print(f"Saved: {save_path}")


# ------------------------------------------------------------------
# 4. RUN
# ------------------------------------------------------------------
if __name__ == "__main__":
    render_fractal()

    # Optional: auto-download when running inside Google Colab.
    # Safe to leave in — it silently does nothing on a normal machine.
    try:
        from google.colab import files
        files.download("cosmic_convergence.png")
    except ImportError:
        pass
