#!/usr/bin/env python3
"""Generate the Babylon art: everything that is an image rather than CSS.

  ~/.config/hypr/babylon/wallpaper.svg, wallpaper.png   1920x1080: golden gates (ripples)
        opening in a pitch sky, blade tips coming through some of them, all aimed
        at one point; the brick courses of Uruk rise out of the haze at the bottom
  ~/.config/hypr/babylon/lock-marks.png                 44x54 three incised drums, crimson:
        the mark beside the password line
  ~/.config/hypr/babylon/lock-gate.png                  70x100 one gate with a blade, under the saying
  ~/.config/waybar/babylon/chain.png                    8x20 separator: two links and a bar
  ~/.config/waybar/babylon/gate.png                     30x22 the ripple on each side of the clock
  ~/.config/waybar/babylon/ws-<slot>-<state>.png        24x24 cuneiform numerals 1-10 in five states
  ~/.config/waybar/babylon/ws.css                       the rules that pick them (imported by style.css)
  ~/.config/gtk-3.0/babylon/crumb-wedge.png             Thunar path separator

Deterministic; edit and re-run (needs rsvg-convert):  python3 build-art.py
"""

import math
import random
import subprocess
from pathlib import Path

CONF = Path.home() / ".config"
HYPR = CONF / "hypr/babylon"
BAR = CONF / "waybar/babylon"
GTK = CONF / "gtk-3.0/babylon"

GROUND, LINE = "#0B0908", "#3A2E1A"
GOLD, GOLD_LIT, GOLD_DEEP, GOLD_DIM = "#D4A72C", "#F4D675", "#8E6B1F", "#7A6130"
CRIM, CRIM_DEEP, LAPIS = "#EB4B50", "#C2171F", "#7FA4E2"


def render(svg, out, w=None, h=None):
    src = out.with_suffix(".svg")
    src.write_text(svg)
    cmd = ["rsvg-convert", "-o", str(out)]
    if w:
        cmd += ["-w", str(w), "-h", str(h)]
    subprocess.run(cmd + [str(src)], check=True)
    if out.name != "wallpaper.png":
        src.unlink()


# ---- wallpaper -------------------------------------------------------------------
def wallpaper():
    W, H = 1920, 1080
    random.seed(5)
    tx, ty = 380, 1180                       # what every blade is aimed at
    spots, tries = [], 0
    while len(spots) < 22 and tries < 4000:
        tries += 1
        x, y = random.uniform(430, 1870), random.uniform(90, 700)
        r = random.uniform(38, 96) * (0.6 + 0.5 * (x / 1920))
        if all(math.hypot(x - a, y - b) > (r + c) * 1.45 for a, b, c in spots):
            spots.append((x, y, r))
    spots.sort(key=lambda s: s[2])
    gates = []
    for i, (x, y, r) in enumerate(spots):
        ang = math.degrees(math.atan2(ty - y, tx - x))
        op = 0.35 + 0.65 * (r / 110)
        rings = "".join(
            f'<ellipse rx="{r * f * 0.80:.1f}" ry="{r * f:.1f}" fill="none" stroke="url(#gold)" stroke-width="{w}" opacity="{o}"/>'
            for f, w, o in ((1.0, 1.8, 1.0), (0.80, 1.2, 0.75), (0.58, 1.0, 0.55), (0.34, 0.8, 0.45), (1.22, 0.9, 0.32), (1.46, 0.7, 0.14)))
        blade = ""
        if i % 3 != 1:
            L = r * random.uniform(0.95, 1.5)
            wd = r * random.choice([0.10, 0.14, 0.2])
            blade = (f'<polygon points="0,{-wd:.1f} {L * 0.72:.1f},{-wd * 0.8:.1f} {L:.1f},0 {L * 0.72:.1f},{wd * 0.8:.1f} 0,{wd:.1f}" fill="url(#blade)"/>'
                     f'<line x1="0" y1="0" x2="{L:.1f}" y2="0" stroke="#FFF1B8" stroke-width="0.8" opacity="0.7"/>')
        gates.append(f'<g transform="translate({x:.0f} {y:.0f}) rotate({ang:.1f})" opacity="{op:.2f}">'
                     f'<ellipse rx="{r * 1.5:.1f}" ry="{r * 1.8:.1f}" fill="url(#halo)"/>'
                     f'<ellipse rx="{r * 0.74:.1f}" ry="{r * 0.92:.1f}" fill="url(#pool)"/>{rings}{blade}</g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070605"/><stop offset="0.62" stop-color="#0E0B08"/><stop offset="0.86" stop-color="#1D150A"/><stop offset="1" stop-color="#3A2A0F"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FBE69A"/><stop offset="0.5" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_DEEP}"/></linearGradient>
<linearGradient id="blade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{GOLD_DEEP}" stop-opacity="0.2"/><stop offset="0.5" stop-color="{GOLD}"/><stop offset="1" stop-color="#FFF1B8"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="{GOLD_LIT}" stop-opacity="0.30"/><stop offset="1" stop-color="{GOLD_LIT}" stop-opacity="0"/></radialGradient>
<radialGradient id="pool"><stop offset="0" stop-color="#FFF1B8" stop-opacity="0.55"/><stop offset="0.6" stop-color="{GOLD}" stop-opacity="0.22"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<radialGradient id="haze" gradientUnits="userSpaceOnUse" cx="960" cy="1180" r="1100"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.28"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>
<filter id="dust" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.004 0.012" numOctaves="4" seed="2"/><feColorMatrix values="0 0 0 0 0.83  0 0 0 0 0.65  0 0 0 0 0.17  0 0 0 0.75 -0.30"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 0.85  0 0 0 0 0.6  0 0 0 0.09 0"/></filter>
<pattern id="brick" width="96" height="44" patternUnits="userSpaceOnUse"><path d="M0,0H96M0,22H96M0,0V22M48,22V44" stroke="{GOLD}" stroke-width="1" fill="none"/></pattern>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
<mask id="m"><rect x="0" y="860" width="{W}" height="220" fill="url(#fade)"/></mask>
</defs>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<rect width="{W}" height="{H}" filter="url(#dust)" opacity="0.20"/>
<rect width="{W}" height="{H}" fill="url(#haze)"/>
{"".join(gates)}
<rect x="0" y="860" width="{W}" height="220" fill="url(#brick)" opacity="0.30" mask="url(#m)"/>
<rect x="0" y="1076" width="{W}" height="4" fill="{GOLD}" opacity="0.5"/>
<rect width="{W}" height="{H}" filter="url(#grain)"/>
</svg>
'''
    render(svg, HYPR / "wallpaper.png", W, H)


# ---- a gate (ripple), used small on the bar and larger on the lock ------------------
def gate(w, h, blade=False, glow=True):
    cx, cy = w / 2, (h * 0.40 if blade else h / 2)
    rx, ry = w * 0.42, (h * 0.34 if blade else h * 0.46)
    rings = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * f:.2f}" ry="{ry * f:.2f}" fill="none" '
                    f'stroke="{GOLD_LIT if i < 2 else GOLD}" stroke-width="{sw}" opacity="{o}"/>'
                    for i, (f, sw, o) in enumerate(((1.0, 1.4, 1), (0.74, 1.1, 0.85), (0.48, 0.9, 0.7), (0.24, 0.8, 0.55))))
    g = (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GOLD_LIT}" opacity="0.30" filter="url(#g)"/>' if glow else "")
    b = ""
    if blade:
        tip = h - 2
        b = (f'<polygon points="{cx - 3.2},{cy} {cx + 3.2},{cy} {cx + 2.4},{tip - 12} {cx},{tip} {cx - 2.4},{tip - 12}" fill="{GOLD}"/>'
             f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{tip}" stroke="#FFF1B8" stroke-width="0.8" opacity="0.8"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs><filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{w / 14:.1f}"/></filter></defs>'
            f'{g}{rings}{b}</svg>')


def chain():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="8" height="20" viewBox="0 0 8 20">'
           f'<ellipse cx="4" cy="4" rx="2.4" ry="3.4" fill="none" stroke="{GOLD_DEEP}" stroke-width="1.1"/>'
           f'<line x1="4" y1="6.4" x2="4" y2="13.6" stroke="{GOLD_DEEP}" stroke-width="1.6"/>'
           f'<ellipse cx="4" cy="16" rx="2.4" ry="3.4" fill="none" stroke="{GOLD_DEEP}" stroke-width="1.1"/></svg>')
    render(svg, BAR / "chain.png")


def lock_marks():
    out = []
    for i, y in enumerate((2, 20, 38)):
        out.append(f'<rect x="4" y="{y}" width="36" height="14" fill="none" stroke="{CRIM_DEEP}" stroke-width="1.4"/>')
        for k in range(5):
            x = 9 + k * 6.4 + (i % 2) * 3
            out.append(f'<path d="M{x:.1f},{y + 3} v4 h3 v4" fill="none" stroke="{CRIM_DEEP}" stroke-width="1"/>')
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="44" height="54" viewBox="0 0 44 54">{"".join(out)}</svg>',
           HYPR / "lock-marks.png", 88, 108)


# ---- workspace numerals ---------------------------------------------------------------
def wedge(x, y0, y1, color):
    return (f'<polygon points="{x - 2.8:.1f},{y0} {x + 2.8:.1f},{y0} {x:.1f},{y0 + 5}" fill="{color}"/>'
            f'<line x1="{x:.1f}" y1="{y0 + 3}" x2="{x:.1f}" y2="{y1}" stroke="{color}" stroke-width="1.5"/>')


def numeral(n, color):
    """Vertical wedges: 1-3 in one row, 4-6 in two, 7-9 in three; 10 is the corner wedge."""
    def row(k, y0, y1):
        return "".join(wedge(12 + (i - (k - 1) / 2) * 6.4, y0, y1, color) for i in range(k))
    if n == 10:
        return f'<polygon points="17.5,4 6.5,12 17.5,20 14.5,12" fill="{color}"/>'
    if n <= 3:
        return row(n, 4, 20)
    if n <= 6:
        return row(3, 2.5, 11) + row(n - 3, 13, 21.5)
    return row(3, 1.5, 8) + row(3, 8.7, 15.2) + row(n - 6, 15.9, 22.5)


def workspaces():
    states = {"empty": (GOLD_DIM, None), "occupied": (GOLD, None), "active": (GOLD_LIT, LINE),
              "focused": (GROUND, GOLD), "urgent": (CRIM, None)}
    css = ["/* Generated by ~/.config/hypr/babylon/build-art.py: the numeral image for every slot and state. */"]
    for n in range(1, 11):
        for state, (color, bg) in states.items():
            back = f'<rect width="24" height="24" fill="{bg}"/>' if bg else ""
            render(f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">{back}{numeral(n, color)}</svg>',
                   BAR / f"ws-{n}-{state}.png")
            sel = f"#custom-ws-{n}" if state == "occupied" else f"#custom-ws-{n}.{state}"
            css.append(f'{sel} {{ background-image: url("ws-{n}-{state}.png"); }}')
    (BAR / "ws.css").write_text("\n".join(css) + "\n")


def crumb():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="18" viewBox="0 0 10 18">'
           f'<polygon points="2.5,5.5 8,9 2.5,12.5" fill="{GOLD_DEEP}"/></svg>')
    render(svg, GTK / "crumb-wedge.png")


if __name__ == "__main__":
    for d in (HYPR, BAR, GTK):
        d.mkdir(parents=True, exist_ok=True)
    wallpaper()
    render(gate(30, 22), BAR / "gate.png")
    render(gate(70, 100, blade=True), HYPR / "lock-gate.png", 140, 200)
    chain()
    lock_marks()
    workspaces()
    crumb()
    print("Babylon art written")
