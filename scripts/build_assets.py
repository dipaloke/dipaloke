#!/usr/bin/env python3
"""Generate every SVG panel in assets/, for both colour schemes.

Design system — "control plane":
  Each category owns one hue from GitHub's own accent palette, and that hue
  is reused wherever the category appears (status LED, stack row, card edge)
  so colour carries meaning instead of decoration.

Everything derives from PALETTE below, so the dark and light variants — and
the panels themselves — can't drift apart. Edit the content constants, then:

    python3 scripts/build_assets.py

Text is monospace throughout and every line is width-checked at build time
against the widest common monospace advance, so a panel that builds here
fits on any machine that renders it. Overflow fails the build.

Note these panels are images: they scale with the container but never
reflow. Dense reference content (track record, credentials, the project
table) deliberately stays as markdown + badges in README.md so it stays
readable on a phone.
"""

import pathlib
import sys

# --------------------------------------------------------------- palettes ---

PALETTE = {
    "dark": {
        "page": "#090c11",
        "card": "#0d1117",
        "border": "#21262d",
        "heading": "#f0f6fc",
        "body": "#8b949e",
        "muted": "#6e7681",
        "grid_opacity": "0.07",
        # category hues
        "cyan": "#56d4dd",
        "green": "#3fb950",
        "blue": "#58a6ff",
        "purple": "#bc8cff",
        "amber": "#d29922",
        "pink": "#f778ba",
    },
    "light": {
        "page": "#ffffff",
        "card": "#f6f8fa",
        "border": "#d0d7de",
        "heading": "#1f2328",
        "body": "#57606a",
        "muted": "#6e7681",
        "grid_opacity": "0.09",
        "cyan": "#0f7f8c",
        "green": "#1a7f37",
        "blue": "#0969da",
        "purple": "#8250df",
        "amber": "#9a6700",
        "pink": "#bf3989",
    },
}

# ---------------------------------------------------------------- content ---

NAME = ("DIPALOKE", ".", "BISWAS")
TAGLINE = "I automate a national fibre network — then build the software people use to watch it."
STATUS = "OPEN TO WORK · DHAKA, BD · HYBRID / REMOTE"
ROLE = "FIBER@HOME · FULL-STACK / NETWORK AUTOMATION"

# (hue, label, bold lead-in, rest)
NOW = [
    ("cyan", "SHIPPING", "NAAS v2", "— Fiber@Home's network ops platform, now a DRF API + Next.js 16 console."),
    ("purple", "BUILDING", "Agile East Bangladesh", "— a manufacturing-execution engine for MPO/MTP patch cords."),
    ("amber", "ASK ME", "", "Netmiko vs. NAPALM, Django REST internals, or Next.js 16 at scale."),
]

# (hue, category, tools)
STACK = [
    ("cyan", "LANGUAGES", "Python · TypeScript · JavaScript"),
    ("green", "AUTOMATION", "Netmiko · NAPALM · Paramiko · Ansible"),
    ("purple", "BACKEND", "Django · Django REST Framework · FastAPI · GraphQL · NestJS · Express"),
    ("blue", "FRONTEND", "Next.js 16 · React · shadcn/ui · HeroUI · Tailwind"),
    ("amber", "DATA", "PostgreSQL · InfluxDB · MongoDB · TanStack Table · Zod"),
    ("pink", "INFRA", "Docker · Celery · GitHub Actions · Linux"),
    ("cyan", "TESTING", "Pytest · Jest · Selenium"),
]

CARDS = [
    {
        "title": "NAAS",
        "status": "LIVE",
        "hue": "green",
        "body": [
            "Fiber@Home's network operations platform. Config",
            "automation and scheduled job processing across a",
            "national fibre estate.",
        ],
        "tags": "Python · Django · Netmiko · Celery",
    },
    {
        "title": "NAAS v2",
        "status": "IN REWRITE",
        "hue": "cyan",
        "body": [
            "The same domain, decoupled — a DRF API behind a",
            "Next.js 16 console with grouped-header tables and",
            "CSV / XLSX / PDF export.",
        ],
        "tags": "TypeScript · DRF · HeroUI · TanStack",
    },
]

FOOTER_LEAD = "Got a network that should run itself — or a product that should ship?"
FOOTER_SUB = "Pick a slot. Bring an agenda, I'll bring opinions."
FOOTER_LEFT = "AVAILABLE FOR NEW WORK"
FOOTER_RIGHT = "DHAKA, BD · HYBRID / REMOTE · UTC+06:00"

# ----------------------------------------------------------------- layout ---

W = 1000  # every panel shares one viewBox width so type scales identically
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
EM = 0.6  # widest common monospace advance; budget against it
PAD = 28
LABEL_X = 64  # category label column
TEXT_X = 210  # content column, clear of the widest label

_problems = []


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fits(text, size, start_x, where, end_x=None):
    """Record an overflow instead of raising, so one run reports them all."""
    limit = (end_x or W - PAD) - start_x
    width = len(text) * size * EM
    if width > limit:
        over = int(width - limit)
        _problems.append(f"  {where}: {int(width)}px in {int(limit)}px (over by {over}) — {text[:52]!r}")
    return text


def panel(height, body, t, label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" viewBox="0 0 {W} {height}" role="img" aria-label="{esc(label)}">
  <rect x="0.5" y="0.5" width="{W - 1}" height="{height - 1}" rx="6" fill="{t['card']}" stroke="{t['border']}"/>
  <g font-family="{MONO}">
{body}
  </g>
</svg>
"""


# ---------------------------------------------------------------- banners ---

BANNER_H = 200


def build_banner(t):
    first, dot, last = NAME
    fits(TAGLINE, 15, 42, "banner tagline")
    fits(STATUS + ROLE, 12, 60, "banner bottom row", W - 40)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{BANNER_H}" viewBox="0 0 {W} {BANNER_H}" role="img" aria-label="Dipaloke Biswas — full-stack developer and network automation engineer. {esc(STATUS)}">
  <defs>
    <pattern id="grid" width="44" height="44" patternUnits="userSpaceOnUse">
      <path d="M44 0H0v44" fill="none" stroke="{t['cyan']}" stroke-width="1" opacity="{t['grid_opacity']}"/>
    </pattern>
    <clipPath id="round"><rect x="0.5" y="0.5" width="{W - 1}" height="{BANNER_H - 1}" rx="6"/></clipPath>
  </defs>
  <g clip-path="url(#round)">
    <rect width="{W}" height="{BANNER_H}" fill="{t['page']}"/>
    <rect width="{W}" height="{BANNER_H}" fill="url(#grid)"/>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{BANNER_H - 1}" rx="6" fill="none" stroke="{t['border']}"/>
  <g font-family="{MONO}">
    <text x="40" y="86" font-size="44" font-weight="700" letter-spacing="5.5" fill="{t['heading']}">{first}<tspan fill="{t['cyan']}">{dot}</tspan>{last}</text>
    <text x="42" y="122" font-size="15" fill="{t['body']}">{esc(TAGLINE)}</text>
    <line x1="42" y1="150" x2="{W - 40}" y2="150" stroke="{t['border']}"/>
    <circle cx="46" cy="171" r="3.5" fill="{t['green']}"/>
    <text x="60" y="175" font-size="12" letter-spacing="0.8" fill="{t['green']}">{esc(STATUS)}</text>
    <text x="{W - 40}" y="175" text-anchor="end" font-size="12" letter-spacing="0.8" fill="{t['muted']}">{esc(ROLE)}</text>
  </g>
</svg>
"""


# ------------------------------------------------------------- work cards ---

CARD_W, CARD_H, GAP = 488, 200, 24


def card_svg(card, x, t):
    hue = t[card["hue"]]
    label_w = len(card["status"]) * (11 * EM + 1)
    dot_x = CARD_W - PAD - label_w - 11

    body = "\n".join(
        f'    <text x="{PAD}" y="{y}" font-size="13" fill="{t["body"]}">{esc(line)}</text>'
        for y, line in zip((104, 124, 144), card["body"])
    )
    for line in card["body"]:
        fits(line, 13, 0, f"card {card['title']}", CARD_W - PAD * 2)

    return f"""  <g transform="translate({x} 0)">
    <rect x="0.5" y="0.5" width="{CARD_W - 1}" height="{CARD_H - 1}" rx="6" fill="{t['card']}" stroke="{t['border']}"/>
    <rect x="1" y="12" width="3" height="{CARD_H - 24}" rx="1.5" fill="{hue}"/>
    <text x="{PAD}" y="50" font-size="19" font-weight="700" letter-spacing="0.5" fill="{t['heading']}">{esc(card['title'])}</text>
    <circle cx="{dot_x:.1f}" cy="45" r="3.5" fill="{hue}"/>
    <text x="{CARD_W - PAD}" y="49" text-anchor="end" font-size="11" letter-spacing="1" fill="{hue}">{esc(card['status'])}</text>
    <line x1="{PAD}" y1="74" x2="{CARD_W - PAD}" y2="74" stroke="{t['border']}"/>
{body}
    <text x="{PAD}" y="176" font-size="11.5" letter-spacing="0.3" fill="{t['muted']}">{esc(card['tags'])}</text>
  </g>"""


def build_work(t):
    label = "; ".join(f"{c['title']} ({c['status']}) — {' '.join(c['body'])} {c['tags']}" for c in CARDS)
    cards = "\n".join(card_svg(c, i * (CARD_W + GAP), t) for i, c in enumerate(CARDS))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{CARD_H}" viewBox="0 0 {W} {CARD_H}" role="img" aria-label="{esc(label)}">
  <g font-family="{MONO}">
{cards}
  </g>
</svg>
"""


# -------------------------------------------------------------- now board ---

def build_now(t):
    rows, y = [], 52
    for hue, label, lead, rest in NOW:
        c = t[hue]
        fits(f"{lead} {rest}".strip(), 14, TEXT_X, f"now/{label}")
        lead_tspan = (
            f'<tspan font-weight="700" fill="{t["heading"]}">{esc(lead)}</tspan> ' if lead else ""
        )
        rows.append(
            f'    <circle cx="{PAD + 16}" cy="{y - 5}" r="4" fill="{c}"/>\n'
            f'    <text x="{LABEL_X}" y="{y}" font-size="12" font-weight="700" letter-spacing="1" fill="{c}">{esc(label)}</text>\n'
            f'    <text x="{TEXT_X}" y="{y}" font-size="14" fill="{t["body"]}">{lead_tspan}{esc(rest)}</text>'
        )
        y += 44
    height = y - 44 + 34
    alt = " ".join(f"{lab}: {lead} {rest}".strip() for _, lab, lead, rest in NOW)
    return panel(height, "\n".join(rows), t, f"Now — {alt}")


# ------------------------------------------------------------ stack panel ---

def build_stack(t):
    rows, y = [], 50
    for hue, label, tools in STACK:
        c = t[hue]
        fits(tools, 14, TEXT_X, f"stack/{label}")
        rows.append(
            f'    <circle cx="{PAD + 16}" cy="{y - 5}" r="4" fill="{c}"/>\n'
            f'    <text x="{LABEL_X}" y="{y}" font-size="12" font-weight="700" letter-spacing="1" fill="{c}">{esc(label)}</text>\n'
            f'    <text x="{TEXT_X}" y="{y}" font-size="14" fill="{t["body"]}">{esc(tools)}</text>'
        )
        y += 40
    height = y - 40 + 32
    alt = "; ".join(f"{label}: {tools}" for _, label, tools in STACK)
    return panel(height, "\n".join(rows), t, f"Stack — {alt}")


# ----------------------------------------------------------------- footer ---

FOOTER_H = 168


def build_footer(t):
    fits(FOOTER_LEAD, 20, PAD + 12, "footer lead")
    fits(FOOTER_LEFT + FOOTER_RIGHT, 12, PAD + 30, "footer bottom row")
    body = f"""    <text x="{PAD + 12}" y="62" font-size="20" font-weight="700" fill="{t['heading']}">{esc(FOOTER_LEAD)}</text>
    <text x="{PAD + 12}" y="94" font-size="14" fill="{t['body']}">{esc(FOOTER_SUB)}</text>
    <line x1="{PAD + 12}" y1="120" x2="{W - PAD - 12}" y2="120" stroke="{t['border']}"/>
    <circle cx="{PAD + 16}" cy="141" r="4" fill="{t['green']}"/>
    <text x="{PAD + 30}" y="146" font-size="12" font-weight="700" letter-spacing="1" fill="{t['green']}">{esc(FOOTER_LEFT)}</text>
    <text x="{W - PAD - 12}" y="146" text-anchor="end" font-size="12" letter-spacing="0.8" fill="{t['muted']}">{esc(FOOTER_RIGHT)}</text>"""
    return panel(FOOTER_H, body, t, f"{FOOTER_LEAD} {FOOTER_SUB} {FOOTER_LEFT}. {FOOTER_RIGHT}")


# ------------------------------------------------------------------- main ---

BUILDERS = {
    "banner": build_banner,
    "work": build_work,
    "now": build_now,
    "stack": build_stack,
    "footer": build_footer,
}


def main():
    out = pathlib.Path(__file__).resolve().parent.parent / "assets"
    written = []
    for theme, t in PALETTE.items():
        for kind, build in BUILDERS.items():
            svg = build(t)
            if _problems:
                break
            written.append((out / f"{kind}-{theme}.svg", svg))

    if _problems:
        print("Content overflows its panel:", *dict.fromkeys(_problems), sep="\n")
        return 1

    for path, svg in written:
        path.write_text(svg)
    print(f"wrote {len(written)} panels to assets/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
