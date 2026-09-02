import json
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))

IN_PATH = os.path.join(
    HERE, "..", "data", "contributions.json"
)

OUT_PATH = os.path.join(
    HERE, "..", "assets", "graphs", "Maulik-activity-graph.svg"
)

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

MONTHS_TO_SHOW = 12

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"

TEXT = "#e6edf3"
MUTED = "#7d8590"

ACCENT = "#539bf5"
ACCENT_BRIGHT = "#58a6ff"

GREEN = "#39d353"
GOLD = "#f2cc60"

WIDTH = 1100
HEIGHT = 390

PAD_X = 55
PAD_TOP = 70
PAD_BOTTOM = 70

GRAPH_LEFT = PAD_X
GRAPH_RIGHT = WIDTH - PAD_X
GRAPH_TOP = 95
GRAPH_BOTTOM = 285

GRAPH_WIDTH = GRAPH_RIGHT - GRAPH_LEFT
GRAPH_HEIGHT = GRAPH_BOTTOM - GRAPH_TOP


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def load_data():
    with open(IN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_last_months(data, count):
    """
    Return the most recent `count` months from contributions.json.

    contributions.json already contains:
        [
            {"month": "2025-10", "total": 42},
            {"month": "2025-11", "total": 57},
            ...
        ]
    """

    monthly = data.get("monthly", [])

    if not monthly:
        raise ValueError("No monthly contribution data found.")

    months = monthly[-count:]

    return [
        {
            "month": item["month"],
            "total": int(item["total"])
        }
        for item in months
    ]


def format_month(month):
    """
    Convert:
        2026-08
    into:
        Aug
    """

    date = datetime.strptime(month, "%Y-%m")

    return date.strftime("%b")


def nice_number(value):
    if value >= 1000:
        return f"{value / 1000:.1f}k"

    return str(value)


def build_points(months):
    """
    Convert monthly values into SVG coordinates.
    """

    values = [m["total"] for m in months]

    max_value = max(values)

    # Prevent a zero-height graph.
    if max_value == 0:
        max_value = 1

    points = []

    for index, month in enumerate(months):

        if len(months) == 1:
            x = GRAPH_LEFT + GRAPH_WIDTH / 2
        else:
            x = (
                GRAPH_LEFT
                + index * GRAPH_WIDTH / (len(months) - 1)
            )

        y = (
            GRAPH_BOTTOM
            - (month["total"] / max_value) * GRAPH_HEIGHT
        )

        points.append({
            "x": x,
            "y": y,
            "month": month["month"],
            "total": month["total"],
        })

    return points, max_value


# -------------------------------------------------------------------
# SVG rendering
# -------------------------------------------------------------------

def render(data):

    months = get_last_months(
        data,
        MONTHS_TO_SHOW
    )

    points, max_value = build_points(months)

    total = sum(m["total"] for m in months)

    highest_month = max(
        months,
        key=lambda item: item["total"]
    )

    average = round(
        total / len(months),
        1
    )

    start_month = months[0]["month"]
    end_month = months[-1]["month"]

    # ---------------------------------------------------------------
    # SVG root
    # ---------------------------------------------------------------

    parts = [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH}" '
            f'height="{HEIGHT}" '
            f'viewBox="0 0 {WIDTH} {HEIGHT}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, '
            f'Consolas, monospace">'
        ),

        # -----------------------------------------------------------
        # Definitions
        # -----------------------------------------------------------

        """
        <defs>
          <linearGradient id="activity-bg"
                          x1="0" y1="0"
                          x2="0" y2="1">
            <stop offset="0%" stop-color="#0d1420"/>
            <stop offset="100%" stop-color="#0a0e14"/>
          </linearGradient>

          <linearGradient id="activity-fill"
                          x1="0" y1="0"
                          x2="0" y2="1">
            <stop offset="0%" stop-color="#539bf5"
                  stop-opacity="0.30"/>
            <stop offset="100%" stop-color="#539bf5"
                  stop-opacity="0.02"/>
          </linearGradient>

          <filter id="glow">
            <feGaussianBlur stdDeviation="3"
                            result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        """,

        # -----------------------------------------------------------
        # Background
        # -----------------------------------------------------------

        (
            f'<rect width="{WIDTH}" '
            f'height="{HEIGHT}" '
            f'rx="12" '
            f'fill="url(#activity-bg)"/>'
        ),

        # -----------------------------------------------------------
        # Border
        # -----------------------------------------------------------

        (
            f'<rect x="0.5" y="0.5" '
            f'width="{WIDTH - 1}" '
            f'height="{HEIGHT - 1}" '
            f'rx="12" '
            f'fill="none" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.55"/>'
        ),

        # -----------------------------------------------------------
        # Title bar
        # -----------------------------------------------------------

        (
            f'<line x1="0" y1="30" '
            f'x2="{WIDTH}" y2="30" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.35"/>'
        ),
    ]

    # Window buttons
    for i, color in enumerate(
        ["#ff5f56", "#ffbd2e", "#27c93f"]
    ):
        parts.append(
            f'<circle '
            f'cx="{PAD_X + i * 16}" '
            f'cy="15" '
            f'r="5" '
            f'fill="{color}"/>'
        )

    # Terminal title
    parts.append(
        f'<text '
        f'x="{WIDTH / 2}" '
        f'y="19" '
        f'fill="{MUTED}" '
        f'font-size="12" '
        f'text-anchor="middle">'
        f'Maulik557-png@github: ~/activity --growth'
        f'</text>'
    )

    # ---------------------------------------------------------------
    # Main heading
    # ---------------------------------------------------------------

    parts.append(
        f'<text '
        f'x="{PAD_X}" '
        f'y="58" '
        f'fill="{TEXT}" '
        f'font-size="16" '
        f'font-weight="700">'
        f'GitHub Activity — Last {len(months)} Months'
        f'</text>'
    )

    # ---------------------------------------------------------------
    # Grid
    # ---------------------------------------------------------------

    # 4 horizontal reference lines.
    grid_lines = 4

    for i in range(grid_lines + 1):

        ratio = i / grid_lines

        y = GRAPH_TOP + ratio * GRAPH_HEIGHT

        value = round(
            max_value * (1 - ratio)
        )

        parts.append(
            f'<line '
            f'x1="{GRAPH_LEFT}" '
            f'y1="{y:.1f}" '
            f'x2="{GRAPH_RIGHT}" '
            f'y2="{y:.1f}" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.20"/>'
        )

        parts.append(
            f'<text '
            f'x="{GRAPH_LEFT - 10}" '
            f'y="{y + 4:.1f}" '
            f'fill="{MUTED}" '
            f'font-size="9" '
            f'text-anchor="end">'
            f'{nice_number(value)}'
            f'</text>'
        )

    # ---------------------------------------------------------------
    # Area under graph
    # ---------------------------------------------------------------

    point_string = " ".join(
        f'{p["x"]:.1f},{p["y"]:.1f}'
        for p in points
    )

    area_points = (
        f'{points[0]["x"]:.1f},{GRAPH_BOTTOM} '
        f'{point_string} '
        f'{points[-1]["x"]:.1f},{GRAPH_BOTTOM}'
    )

    parts.append(
        f'<polygon '
        f'points="{area_points}" '
        f'fill="url(#activity-fill)"/>'
    )

    # ---------------------------------------------------------------
    # Graph line
    # ---------------------------------------------------------------

    parts.append(
        f'<polyline '
        f'points="{point_string}" '
        f'fill="none" '
        f'stroke="{ACCENT}" '
        f'stroke-width="3" '
        f'stroke-linejoin="round" '
        f'stroke-linecap="round"/>'
    )

    # ---------------------------------------------------------------
    # Points
    # ---------------------------------------------------------------

    for point in points:

        x = point["x"]
        y = point["y"]

        parts.append(
            f'<circle '
            f'cx="{x:.1f}" '
            f'cy="{y:.1f}" '
            f'r="5" '
            f'fill="{BG}" '
            f'stroke="{ACCENT_BRIGHT}" '
            f'stroke-width="2">'
            f'<title>'
            f'{point["month"]}: '
            f'{point["total"]:,} contributions'
            f'</title>'
            f'</circle>'
        )

    # ---------------------------------------------------------------
    # X-axis labels
    # ---------------------------------------------------------------

    for point in points:

        parts.append(
            f'<text '
            f'x="{point["x"]:.1f}" '
            f'y="{GRAPH_BOTTOM + 25}" '
            f'fill="{MUTED}" '
            f'font-size="10" '
            f'text-anchor="middle">'
            f'{format_month(point["month"])}'
            f'</text>'
        )

    # ---------------------------------------------------------------
    # Stats
    # ---------------------------------------------------------------

    stats_y = 350

    parts.append(
        f'<text '
        f'x="{PAD_X}" '
        f'y="{stats_y}" '
        f'fill="{GREEN}" '
        f'font-size="12">'
        f'<tspan font-weight="700">'
        f'{total:,}'
        f'</tspan>'
        f'<tspan fill="{MUTED}">'
        f' contributions'
        f'</tspan>'
        f'</text>'
    )

    parts.append(
        f'<text '
        f'x="{WIDTH / 2}" '
        f'y="{stats_y}" '
        f'fill="{MUTED}" '
        f'font-size="12" '
        f'text-anchor="middle">'
        f'avg '
        f'<tspan fill="{ACCENT}" font-weight="700">'
        f'{average:,}'
        f'</tspan>'
        f' / month'
        f'</text>'
    )

    parts.append(
        f'<text '
        f'x="{WIDTH - PAD_X}" '
        f'y="{stats_y}" '
        f'fill="{MUTED}" '
        f'font-size="12" '
        f'text-anchor="end">'
        f'best '
        f'<tspan fill="{GOLD}" font-weight="700">'
        f'{highest_month["total"]:,}'
        f'</tspan>'
        f' in {format_month(highest_month["month"])}'
        f'</text>'
    )

    # ---------------------------------------------------------------
    # Footer range
    # ---------------------------------------------------------------

    parts.append(
        f'<text '
        f'x="{WIDTH / 2}" '
        f'y="{HEIGHT - 12}" '
        f'fill="{MUTED}" '
        f'font-size="9" '
        f'text-anchor="middle">'
        f'{start_month} → {end_month}'
        f'</text>'
    )

    parts.append("</svg>")

    return "".join(parts)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":

    data = load_data()

    svg = render(data)

    os.makedirs(
        os.path.dirname(OUT_PATH),
        exist_ok=True
    )

    with open(
        OUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(svg)

    print(
        f"wrote {OUT_PATH} "
        f"({len(svg)} bytes)"
    )
