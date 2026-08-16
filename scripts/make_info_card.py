import html
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets/me", "maulik-info-card.svg")

STATIC = bool(os.environ.get("STATIC"))

W, H = 660, 360

PAD = 20
TITLEBAR_H = 30

KEY_X = PAD
VAL_X = PAD + 105

LINE_H = 20.5
WRAP_LINE_H = 18

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"
SECTION = "#58a6ff"
GREEN = "#3fb950"
ACCENT = "#22d3ee"


# -------------------------------------------------------------------
# Content
# -------------------------------------------------------------------

ROWS = [
    ("host",),

    ("kv", "Current", "Final-year B.E. Computer Engineering @ ADIT"),
    ("kv", "Education", "CGPA: 8.89/10 · Class of 2027"),
    (
        "kv",
        "Focus",
        "Java backend · Spring Boot · Microservices · Distributed systems",
    ),
    (
        "kv",
        "Open To",
        "Backend / Full-stack roles · Campus + Off-campus",
    ),

    ("gap",),

    ("sec", "Stack"),

    (
        "kv",
        "Backend",
        "Java, Spring Boot, REST APIs, Microservices",
    ),
    (
        "kv",
        "Data",
        "PostgreSQL, MySQL, Redis, Kafka",
    ),
    (
        "kv",
        "Infra",
        "Docker, AWS, Git, GitHub, Jenkins",
    ),

    ("gap",),

    ("sec", "Highlights"),

    (
        "bul",
        "SSIP Gujarat Hackathon Finalist — Team Awaaz",
    ),
    (
        "bul",
        "Innovation AI Shaping Future Finalist — Team Swift AI",
    ),
    (
        "bul",
        "Oracle Cloud Infrastructure (OCI) Foundations Associate",
    ),
]


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def esc(value):
    return html.escape(str(value))


def wrap_text(text, max_chars):
    """
    Wrap text based on approximate monospace character capacity.

    SVG text itself does not wrap, so we split long strings into
    multiple <tspan> lines.
    """
    return textwrap.wrap(
        text,
        width=max_chars,
        break_long_words=False,
        break_on_hyphens=False,
    )


def rise(inner, i):
    """Fade + slight upward slide, staggered by row index."""
    if STATIC:
        return f"<g>{inner}</g>"

    delay = 0.15 + i * 0.06

    return (
        f'<g opacity="0" transform="translate(0,5)">'
        f"{inner}"
        f'<animate attributeName="opacity" '
        f'from="0" to="1" '
        f'begin="{delay:.2f}s" '
        f'dur="0.4s" '
        f'fill="freeze"/>'
        f'<animateTransform '
        f'attributeName="transform" '
        f'type="translate" '
        f'from="0 5" '
        f'to="0 0" '
        f'begin="{delay:.2f}s" '
        f'dur="0.4s" '
        f'fill="freeze" '
        f'calcMode="spline" '
        f'keySplines="0.2 0.8 0.2 1"/>'
        f"</g>"
    )


# -------------------------------------------------------------------
# SVG
# -------------------------------------------------------------------

parts = [
    (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{W}" '
        f'height="{H}" '
        f'viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
    ),

    "<defs>",

    (
        f'<linearGradient id="ibg" '
        f'x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/>'
        f'<stop offset="1" stop-color="{BG}"/>'
        f"</linearGradient>"
    ),

    "</defs>",

    # Background
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',

    # Border
    (
        f'<rect x="0.5" y="0.5" '
        f'width="{W - 1}" '
        f'height="{H - 1}" '
        f'rx="12" '
        f'fill="none" '
        f'stroke="{FRAME}"/>'
    ),

    # Title bar
    (
        f'<line x1="0" y1="{TITLEBAR_H}" '
        f'x2="{W}" y2="{TITLEBAR_H}" '
        f'stroke="{FRAME}"/>'
    ),
]


# -------------------------------------------------------------------
# Window buttons
# -------------------------------------------------------------------

for i, dotcol in enumerate(
    ["#ff5f56", "#ffbd2e", "#27c93f"]
):
    parts.append(
        f'<circle '
        f'cx="{PAD + i * 16}" '
        f'cy="{TITLEBAR_H / 2}" '
        f'r="5" '
        f'fill="{dotcol}"/>'
    )


# -------------------------------------------------------------------
# Terminal title
# -------------------------------------------------------------------

parts.append(
    f'<text '
    f'x="{W / 2}" '
    f'y="{TITLEBAR_H / 2 + 4}" '
    f'fill="{MUTED}" '
    f'font-size="13" '
    f'text-anchor="middle">'
    f"Maulik557-png@github: ~$ neofetch"
    f"</text>"
)


# -------------------------------------------------------------------
# Content rendering
# -------------------------------------------------------------------

y = TITLEBAR_H + 30

for i, row in enumerate(ROWS):
    kind = row[0]

    # ---------------------------------------------------------------
    # Gap
    # ---------------------------------------------------------------

    if kind == "gap":
        y += LINE_H * 0.5
        continue

    # ---------------------------------------------------------------
    # Host
    # ---------------------------------------------------------------

    if kind == "host":

        inner = (
            f'<text '
            f'x="{KEY_X}" '
            f'y="{y:.1f}" '
            f'font-size="14" '
            f'font-weight="700">'
            f'<tspan fill="{GREEN}">Maulik557-png</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{ACCENT}">github</tspan>'
            f"</text>"

            f'<line '
            f'x1="{KEY_X + 157}" '
            f'y1="{y - 4:.1f}" '
            f'x2="{W - PAD}" '
            f'y2="{y - 4:.1f}" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.8"/>'
        )

        parts.append(rise(inner, i))
        y += LINE_H
        continue

    # ---------------------------------------------------------------
    # Section
    # ---------------------------------------------------------------

    if kind == "sec":

        title = esc(row[1])

        line_start = KEY_X + 12 + len(row[1]) * 8

        inner = (
            f'<text '
            f'x="{KEY_X}" '
            f'y="{y:.1f}" '
            f'fill="{SECTION}" '
            f'font-size="13" '
            f'font-weight="700">'
            f'&#8212; {title}'
            f"</text>"

            f'<line '
            f'x1="{line_start}" '
            f'y1="{y - 4:.1f}" '
            f'x2="{W - PAD}" '
            f'y2="{y - 4:.1f}" '
            f'stroke="{FRAME}" '
            f'stroke-opacity="0.8"/>'
        )

        parts.append(rise(inner, i))
        y += LINE_H
        continue

    # ---------------------------------------------------------------
    # Key / Value
    # ---------------------------------------------------------------

    if kind == "kv":

        key = esc(row[1])
        value = row[2]

        # Available width in approximate monospace characters.
        available_width = W - VAL_X - PAD

        # Approximate character width for 13.5px monospace font.
        char_width = 8

        max_chars = max(
            20,
            int(available_width / char_width),
        )

        lines = wrap_text(value, max_chars)

        tspans = []

        for line_index, line in enumerate(lines):

            dy = 0 if line_index == 0 else WRAP_LINE_H

            tspans.append(
                f'<tspan '
                f'x="{VAL_X}" '
                f'dy="{dy:.1f}">'
                f'{esc(line)}'
                f"</tspan>"
            )

        inner = (
            f'<text '
            f'x="{KEY_X}" '
            f'y="{y:.1f}" '
            f'fill="{KEY}" '
            f'font-size="13.5" '
            f'font-weight="700">'
            f"{key}"
            f"</text>"

            f'<text '
            f'x="{VAL_X}" '
            f'y="{y:.1f}" '
            f'fill="{INK}" '
            f'font-size="13.5">'
            f'{"".join(tspans)}'
            f"</text>"
        )

        parts.append(rise(inner, i))

        # Move down according to number of wrapped lines.
        y += max(
            LINE_H,
            len(lines) * WRAP_LINE_H,
        )

        continue

    # ---------------------------------------------------------------
    # Bullet
    # ---------------------------------------------------------------

    if kind == "bul":

        text = row[1]

        available_width = W - (KEY_X + 10) - PAD
        char_width = 8

        max_chars = max(
            20,
            int(available_width / char_width),
        )

        lines = wrap_text(text, max_chars)

        tspans = []

        for line_index, line in enumerate(lines):

            if line_index == 0:
                x = KEY_X + 10
                dy = 0
            else:
                x = KEY_X + 10
                dy = WRAP_LINE_H

            tspans.append(
                f'<tspan '
                f'x="{x}" '
                f'dy="{dy:.1f}">'
                f'{esc(line)}'
                f"</tspan>"
            )

        inner = (
            f'<circle '
            f'cx="{KEY_X + 3}" '
            f'cy="{y - 4:.1f}" '
            f'r="2.5" '
            f'fill="{GREEN}"/>'

            f'<text '
            f'x="{KEY_X + 10}" '
            f'y="{y:.1f}" '
            f'fill="{INK}" '
            f'font-size="13.5">'
            f'{"".join(tspans)}'
            f"</text>"
        )

        parts.append(rise(inner, i))

        y += max(
            LINE_H,
            len(lines) * WRAP_LINE_H,
        )

        continue


parts.append("</svg>")

svg = "".join(parts)


# -------------------------------------------------------------------
# Write SVG
# -------------------------------------------------------------------

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)


print(
    "wrote",
    OUT,
    len(svg),
    "bytes;",
    W,
    "x",
    H,
    "content_bottom",
    round(y),
)
