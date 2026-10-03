#!/usr/bin/env python3
"""Generate the Babylon icon theme next to this file.

scalable/  64-unit SVGs. Folders are black tablets in a gold line with a gold
           tab and a row of cuneiform wedges (a gold mark for the special
           folders); the home folder is the treasure: solid gold with black
           wedges. Documents are clay tablets with incised wedge rows and one
           mark for their type (crimson only on PDF, lapis on images and code).
           Devices are sharp black boxes in a gold line with a lit-gold light.
           The trash is a gate: things go back into the treasury; when it is
           full a blade shows in it.
16/        sidebar size: plain line icons in Muted.
Anything not drawn here falls through to Adwaita.
Run: python3 build.py   (then gtk-update-icon-cache runs by itself)
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAME = "Babylon"

GROUND, BODY, LINE = "#0B0908", "#1E1810", "#3A2E1A"
GOLD, GOLD_LIT, GOLD_DEEP = "#D4A72C", "#F4D675", "#8E6B1F"
CLAY, CLAY_EDGE, CLAY_INK = "#B89A6A", "#6B5320", "#2A2116"
LAPIS, LAPIS_DEEP, CRIM = "#7FA4E2", "#2E5AA8", "#C2171F"
SIDE = "#A99B80"


def svg64(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">{body}</svg>\n'


def write(rel, content, names):
    for name in names:
        path = ROOT / rel / f"{name}.svg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def wedge(x, y, h, color, w=3.0):
    """One vertical cuneiform wedge: a triangular head and its tail."""
    return (f'<polygon points="{x - w},{y} {x + w},{y} {x},{y + w * 1.9:.1f}" fill="{color}"/>'
            f'<line x1="{x}" y1="{y + w}" x2="{x}" y2="{y + h}" stroke="{color}" stroke-width="{w * 0.55:.2f}"/>')


def wedges(xs, y, h, color, w=3.0):
    return "".join(wedge(x, y, h, color, w) for x in xs)


def stroke(d, color, w=2.4):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="square" stroke-linejoin="miter"/>'


# ---- folders: tablets of the treasury ------------------------------------------------
def marks(color):
    return {
        None: wedges((24, 32, 40), 32, 17, color),
        "home": wedges((24, 32, 40), 32, 17, color),
        "documents": "".join(f'<rect x="22" y="{y}" width="{w}" height="2.6" fill="{color}"/>' for y, w in ((32, 20), (38.5, 20), (45, 13))),
        "downloads": stroke("M32 30 V45 M26 39.5 L32 45.5 L38 39.5 M24 50 H40", color),
        "music": stroke("M28 47 V32 L39 30 V45", color) + f'<rect x="23" y="44.5" width="5.6" height="5" fill="{color}"/><rect x="34" y="42.5" width="5.6" height="5" fill="{color}"/>',
        "pictures": f'<path d="M21 50 L29 38 L33.5 44 L37 40 L44 50 Z" fill="{color}"/><rect x="36.5" y="31" width="5" height="5" fill="{color}" transform="rotate(45 39 33.5)"/>',
        "videos": f'<path d="M27 31 L42 40 L27 49 Z" fill="{color}"/>',
        "desktop": stroke("M22 32 H42 V45 H22 Z M27 50 H37", color, 2.2),
        "templates": f'<rect x="23" y="31" width="18" height="18" fill="none" stroke="{color}" stroke-width="2.2" stroke-dasharray="3.4 2.8"/>',
        "share": stroke("M26 40.5 L38 34 M26 40.5 L38 47.5", color, 1.8) + "".join(f'<rect x="{x - 3}" y="{y - 3}" width="6" height="6" fill="{color}"/>' for x, y in ((26, 40.5), (38, 33.5), (38, 47.5))),
        "remote": "".join(f'<ellipse cx="32" cy="40.5" rx="{rx}" ry="{ry}" fill="none" stroke="{color}" stroke-width="{sw}"/>' for rx, ry, sw in ((8.5, 10.5, 1.8), (5.4, 6.8, 1.4), (2.2, 2.8, 1.2))),
    }


def folder(kind=None):
    treasure = kind == "home"
    fill, mark = (GOLD, GROUND) if treasure else (BODY, GOLD)
    body = (f'<path d="M5.75 11.75 H25 L30 18 H58.25 V54 H5.75 Z" fill="{GROUND}" stroke="{GOLD}" stroke-width="1.5"/>'
            f'<path d="M5.75 11.75 H25 L30 18 H5.75 Z" fill="{GOLD}"/>'
            f'<rect x="4.75" y="23.75" width="54.5" height="32.5" fill="{fill}" stroke="{GOLD_LIT if treasure else GOLD}" stroke-width="1.5"/>'
            + marks(mark)[kind])
    return svg64(body)


FOLDERS = {
    None: ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
    "home": ["user-home", "folder-home"],
    "documents": ["folder-documents"],
    "downloads": ["folder-download"],
    "music": ["folder-music"],
    "pictures": ["folder-pictures"],
    "videos": ["folder-videos"],
    "templates": ["folder-templates"],
    "share": ["folder-publicshare"],
    "desktop": ["user-desktop"],
    "remote": ["folder-remote", "network-workgroup"],
}
for kind, names in FOLDERS.items():
    write("scalable/places", folder(kind), names)
    if kind is None:
        write("scalable/mimetypes", folder(kind), names)


# ---- documents: clay tablets -----------------------------------------------------------
def tablet():
    return (f'<path d="M17 4.75 H47 C50.5 4.75 52.25 6.5 52.25 10 V54 C52.25 57.5 50.5 59.25 47 59.25 H17 C13.5 59.25 11.75 57.5 11.75 54 V10 C11.75 6.5 13.5 4.75 17 4.75 Z" '
            f'fill="{CLAY}" stroke="{CLAY_EDGE}" stroke-width="1.5"/>'
            f'<path d="M15 9 C15 7.5 16 7 17.5 7 H46.5 C48 7 49 7.5 49 9" fill="none" stroke="#D8C08F" stroke-width="1.2"/>')


def rows(ys, color=CLAY_INK, n=5):
    return "".join(wedges([18.5 + k * (27 / (n - 1)) for k in range(n)], y, 7.5, color, 2.1) for y in ys)


def band(color):
    return f'<rect x="12.5" y="44" width="39" height="9" fill="{color}"/>'


DOC_MARKS = {
    None: rows([13]),
    "text": rows([13, 24, 35, 46]),
    "script": rows([13]) + stroke("M19 29 L26 35 L19 41", LAPIS_DEEP) + stroke("M30 42 H43", LAPIS_DEEP) + rows([48], CLAY_INK, 5),
    "code": rows([13]) + stroke("M27 27 L20 35.5 L27 44", LAPIS_DEEP) + stroke("M37 27 L44 35.5 L37 44", LAPIS_DEEP),
    "exec": rows([13]) + f'<path d="M32 25 L43 36.5 L32 48 L21 36.5 Z" fill="{CLAY_INK}"/>',
    "image": rows([13]) + f'<rect x="18" y="25" width="28" height="24" fill="{LAPIS_DEEP}"/><path d="M18 49 L27 36 L33 43 L37 39 L46 49 Z" fill="{LAPIS}"/>'
             f'<rect x="38" y="28.5" width="4.4" height="4.4" fill="{GOLD_LIT}" transform="rotate(45 40.2 30.7)"/>',
    "pdf": rows([13, 24]) + band(CRIM),
    "audio": rows([13]) + stroke("M19 38 C22 27 25 49 29 38 C33 27 36 49 45 36", CLAY_INK),
    "video": rows([13]) + f'<path d="M25 27 L42 37.5 L25 48 Z" fill="{CLAY_INK}"/>',
    "archive": rows([13]) + f'<rect x="12.5" y="30" width="39" height="6" fill="{GOLD_DEEP}"/><rect x="27" y="27.5" width="10" height="11" fill="{GOLD}" stroke="{CLAY_INK}" stroke-width="1.4"/>',
    "grid": rows([13]) + stroke("M18 27 H46 M18 35 H46 M18 43 H46 M18 51 H46 M27.3 27 V51 M36.6 27 V51 M18 27 V51 M46 27 V51", CLAY_INK, 1.4),
    "slide": rows([13]) + f'<rect x="18" y="26" width="28" height="17" fill="{GOLD_DEEP}"/>' + stroke("M32 43 V51 M26 52 H38", CLAY_INK, 2),
    "font": rows([13]) + stroke("M22 51 L32 26 L42 51 M25.5 42.5 H38.5", CLAY_INK),
}
DOCUMENTS = {
    None: ["application-x-generic", "unknown", "empty"],
    "text": ["text-x-generic", "text-plain", "x-office-document", "text-markdown", "text-x-readme"],
    "script": ["text-x-script", "application-x-shellscript", "text-x-python", "text-x-makefile"],
    "exec": ["application-x-executable", "application-x-sharedlib"],
    "image": ["image-x-generic"],
    "audio": ["audio-x-generic"],
    "video": ["video-x-generic"],
    "archive": ["package-x-generic", "application-x-archive", "application-zip", "application-x-compressed-tar", "application-x-tar"],
    "pdf": ["application-pdf"],
    "code": ["text-html", "application-json", "text-x-csrc", "text-x-c++src", "text-x-javascript"],
    "grid": ["x-office-spreadsheet"],
    "slide": ["x-office-presentation"],
    "font": ["font-x-generic"],
}
for kind, names in DOCUMENTS.items():
    write("scalable/mimetypes", svg64(tablet() + DOC_MARKS[kind]), names)


# ---- devices and trash -----------------------------------------------------------------
def box(x, y, w, h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BODY}" stroke="{GOLD}" stroke-width="1.5"/>'


def led(cx, cy):
    return f'<rect x="{cx - 2.6}" y="{cy - 2.6}" width="5.2" height="5.2" fill="{GOLD_LIT}" transform="rotate(45 {cx} {cy})"/>'


DRIVE = box(8.75, 21.75, 46.5, 22.5) + wedges((16, 22, 28), 27, 11, GOLD_DEEP, 2.2) + led(46, 33)
write("scalable/devices", svg64(DRIVE), ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"])
REMOVABLE = (f'<rect x="24.75" y="8.75" width="14.5" height="12" fill="{LINE}" stroke="{GOLD}" stroke-width="1.5"/>'
             + box(18.75, 20.75, 26.5, 35.5) + led(32, 40))
write("scalable/devices", svg64(REMOVABLE), ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"])


def gate(cx, cy, rx, ry, blade=False):
    rings = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * f:.1f}" ry="{ry * f:.1f}" fill="none" stroke="{GOLD_LIT if i < 2 else GOLD}" '
                    f'stroke-width="{sw}" opacity="{o}"/>' for i, (f, sw, o) in enumerate(((1, 1.8, 1), (0.74, 1.4, 0.9), (0.48, 1.2, 0.75), (0.22, 1, 0.6))))
    b = (f'<polygon points="{cx - 3},{cy} {cx + 3},{cy} {cx + 2.2},{cy + ry * 0.95:.1f} {cx},{cy + ry * 1.3:.1f} {cx - 2.2},{cy + ry * 0.95:.1f}" fill="{GOLD}"/>'
         if blade else "")
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{GOLD}" opacity="0.14"/>' + rings + b


OPTICAL = f'<circle cx="32" cy="32" r="21.25" fill="{BODY}" stroke="{GOLD}" stroke-width="1.5"/>' + gate(32, 32, 12, 12) 
write("scalable/devices", svg64(OPTICAL), ["drive-optical", "media-optical"])
COMPUTER = box(9.75, 10.75, 44.5, 31.5) + stroke("M32 42.5 V53 M23 54 H41", GOLD, 2) + led(32, 26.5)
write("scalable/devices", svg64(COMPUTER), ["computer", "video-display"])
write("scalable/places", svg64(gate(32, 32, 22, 27)), ["user-trash"])
write("scalable/places", svg64(gate(32, 27, 20, 23, blade=True)), ["user-trash-full"])


# ---- 16px sidebar: plain line icons ------------------------------------------------------
SYM = {
    "home": '<path d="M2 8 L8 2.5 L14 8"/><path d="M4 7 V14 H12 V7"/>',
    "desktop": '<rect x="2" y="3" width="12" height="8"/><path d="M6 14 H10"/>',
    "documents": '<path d="M4 2 H10 L13 5 V14 H4 Z"/><path d="M6.5 8 H10.5 M6.5 11 H9.5"/>',
    "downloads": '<path d="M8 2 V11"/><path d="M4 7.5 L8 11.5 L12 7.5"/><path d="M3 14 H13"/>',
    "music": '<path d="M5.5 12.5 V3.5 L12.5 2.5 V11.5"/><circle cx="4" cy="12.5" r="1.6"/><circle cx="11" cy="11.5" r="1.6"/>',
    "pictures": '<path d="M2 13 L6 7 L9 10.5 L11 8.5 L14 13 Z"/><circle cx="11.5" cy="4.5" r="1.2"/>',
    "videos": '<path d="M5 3 V13 L13 8 Z"/>',
    "templates": '<rect x="2.5" y="2.5" width="11" height="11" stroke-dasharray="2.2 2"/>',
    "share": '<circle cx="4" cy="8" r="1.6"/><circle cx="12" cy="3.8" r="1.6"/><circle cx="12" cy="12.2" r="1.6"/><path d="M5.4 7.2 L10.6 4.6 M5.4 8.8 L10.6 11.4"/>',
    "folder": '<path d="M2 4 H6.5 L8 5.5 H14 V13 H2 Z"/>',
    "recent": '<circle cx="8" cy="8" r="6"/><path d="M8 4.5 V8 L10.5 9.5"/>',
    "trash": '<ellipse cx="8" cy="8" rx="5" ry="6"/><ellipse cx="8" cy="8" rx="2.6" ry="3.2"/>',
    "bookmark": '<path d="M4 2 H12 V14 L8 10.5 L4 14 Z"/>',
    "drive": '<rect x="2" y="5" width="12" height="6"/><path d="M10.5 8 H11.5"/>',
    "removable": '<rect x="4.5" y="5" width="7" height="9"/><path d="M6 5 V2 H10 V5"/>',
    "optical": '<circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="1.5"/>',
    "computer": '<rect x="2" y="2.5" width="12" height="8"/><path d="M5 14 H11 M8 10.5 V14"/>',
    "network": '<circle cx="8" cy="8" r="6"/><path d="M2 8 H14 M8 2 C5 5 5 11 8 14 M8 2 C11 5 11 11 8 14"/>',
}


def sym16(key):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" '
            f'stroke="{SIDE}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{SYM[key]}</svg>\n')


SIDEBAR = {
    "places": {
        "home": ["user-home", "folder-home", "go-home"], "desktop": ["user-desktop"], "documents": ["folder-documents"],
        "downloads": ["folder-download"], "music": ["folder-music"], "pictures": ["folder-pictures"],
        "videos": ["folder-videos"], "templates": ["folder-templates"], "share": ["folder-publicshare"],
        "folder": ["folder", "inode-directory", "folder-open", "folder-drag-accept", "folder-visiting"],
        "recent": ["document-open-recent", "folder-recent"], "trash": ["user-trash", "user-trash-full"],
        "bookmark": ["user-bookmarks", "bookmark-new"], "network": ["folder-remote", "network-workgroup", "network-server"],
    },
    "devices": {
        "drive": ["drive-harddisk", "drive-harddisk-system", "drive-multidisk"],
        "removable": ["drive-removable-media", "drive-harddisk-usb", "media-removable", "media-flash"],
        "optical": ["drive-optical", "media-optical"], "computer": ["computer", "video-display"],
    },
}
for ctx, groups in SIDEBAR.items():
    for key, names in groups.items():
        write(f"16/{ctx}", sym16(key), names)

(ROOT / "index.theme").write_text(f"""[Icon Theme]
Name={NAME}
Comment=Babylon: black tablets with gold wedges for folders, clay tablets for documents, a gate for the trash
Inherits=Adwaita,hicolor
Example=folder

Directories=16/places,16/devices,scalable/places,scalable/mimetypes,scalable/devices

[16/places]
Size=16
Context=Places
Type=Fixed

[16/devices]
Size=16
Context=Devices
Type=Fixed

[scalable/places]
Size=64
MinSize=20
MaxSize=512
Context=Places
Type=Scalable

[scalable/mimetypes]
Size=64
MinSize=16
MaxSize=512
Context=MimeTypes
Type=Scalable

[scalable/devices]
Size=64
MinSize=20
MaxSize=512
Context=Devices
Type=Scalable
""")
subprocess.run(["gtk-update-icon-cache", "-f", "-t", str(ROOT)], check=False,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"{NAME} icons written to {ROOT}")
