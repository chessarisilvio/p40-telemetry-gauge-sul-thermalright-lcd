"""
Gauge Renderer for P40 Telemetry Gauge.
Generates vector gauges (SVG) for temperature and TDP using matplotlib.
"""

import io
import os
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np


def create_gauge(
    value: float,
    min_val: float = 0.0,
    max_val: float = 100.0,
    label: str = "",
    units: str = "",
    width: int = 400,
    height: int = 200,
) -> str:
    """
    Create an SVG gauge as a string.

    Args:
        value: Current value to display.
        min_val: Minimum value of the gauge.
        max_val: Maximum value of the gauge.
        label: Label for the gauge (e.g., "Temperature").
        units: Units to display (e.g., "°C").
        width: Width of the SVG in pixels.
        height: Height of the SVG in pixels.

    Returns:
        SVG string representing the gauge.
    """
    # Clamp value to min/max
    value = max(min_val, min(value, max_val))

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), subplot_kw=dict(aspect="equal"))
    fig.patch.set_alpha(0.0)  # Transparent background

    # Parameters for the gauge
    theta = np.linspace(0, np.pi, 100)
    radius = 0.8
    center = np.array([0, 0])

    # Background arc (light gray)
    ax.plot(
        radius * np.cos(theta),
        radius * np.sin(theta) + 0.1,
        color="lightgray",
        linewidth=10,
        solid_capstyle="round",
    )

    # Value arc (green to red gradient based on value)
    value_ratio = (value - min_val) / (max_val - min_val)
    value_theta = np.linspace(0, np.pi * value_ratio, int(100 * value_ratio))
    if len(value_theta) > 0:
        # Color interpolation: green (0.3, 0.8, 0.3) to red (0.8, 0.3, 0.3)
        r = 0.3 + 0.5 * value_ratio
        g = 0.8 - 0.5 * value_ratio
        b = 0.3
        ax.plot(
            radius * np.cos(value_theta),
            radius * np.sin(value_theta) + 0.1,
            color=(r, g, b),
            linewidth=10,
            solid_capstyle="round",
        )

    # Center circle
    ax.add_artist(plt.Circle((0, 0.1), 0.15, color="white", zorder=10))

    # Text: value and units
    ax.text(
        0,
        -0.2,
        f"{value:.1f}{units}",
        ha="center",
        va="center",
        fontsize=24,
        fontweight="bold",
        color="black",
    )
    if label:
        ax.text(
            0,
            -0.4,
            label,
            ha="center",
            va="center",
            fontsize=14,
            color="gray",
        )

    # Set limits and remove axes
    ax.set_xlim(-radius - 0.1, radius + 0.1)
    ax.set_ylim(-0.2, radius + 0.2)
    ax.axis("off")

    # Save to SVG string
    buf = io.StringIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    return buf.getvalue()


def save_gauge_svg(
    value: float,
    min_val: float = 0.0,
    max_val: float = 100.0,
    label: str = "",
    units: str = "",
    width: int = 400,
    height: int = 200,
    output_path: str = "gauge.svg",
) -> None:
    """
    Create and save an SVG gauge to a file.

    Args:
        value: Current value to display.
        min_val: Minimum value of the gauge.
        max_val: Maximum value of the gauge.
        label: Label for the gauge.
        units: Units to display.
        width: Width of the SVG in pixels.
        height: Height of the SVG in pixels.
        output_path: Path to save the SVG file (relative or absolute).
    """
    svg_content = create_gauge(value, min_val, max_val, label, units, width, height)
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)


if __name__ == "__main__":
    # Example usage: create a temperature gauge and save to assets/example_gauge.svg
    # Temperature range: 0°C to 100°C
    example_value = 65.0  # Example temperature
    save_gauge_svg(
        value=example_value,
        min_val=0.0,
        max_val=100.0,
        label="GPU Temperature",
        units="°C",
        width=400,
        height=200,
        output_path="assets/example_gauge.svg",
    )
    print("Example gauge saved to assets/example_gauge.svg")