"""Convert source-photo.jpg (or the public GitHub avatar) to typing ASCII SVG."""
from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

import requests
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "krish-ascii.svg"
AVATAR_URL = "https://avatars.githubusercontent.com/u/256733070?v=4"
RAMP = " .:-=+*#%@"


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "source-photo.jpg"
    if source.exists():
        image = Image.open(source).convert("RGB")
        label = source.name
    else:
        response = requests.get(AVATAR_URL, timeout=30, headers={"User-Agent": "Krish-labs-profile-art/1.0"})
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
        label = "GitHub avatar"

    gray = ImageOps.autocontrast(ImageOps.grayscale(image))
    cols = 58
    rows = max(12, min(34, round(cols * gray.height / max(gray.width, 1) * 0.55)))
    gray = gray.resize((cols, rows), Image.Resampling.LANCZOS)
    gray = ImageEnhance.Contrast(gray).enhance(1.25)

    width, height = 370, 430
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Animated ASCII portrait of Krish Gupta</title>',
        f'<desc id="desc">Monochrome ASCII rendering based on {label}.</desc>',
        '<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.muted{fill:#8b949e}.art{fill:#c9d1d9;font-size:7.4px;white-space:pre}@keyframes cursor{50%{opacity:0}}.cursor{animation:cursor 1s steps(2,start) infinite}</style>',
        '<text x="14" y="22" font-size="10" class="muted">KRISH // ASCII RENDER</text>',
        '<path d="M14 29H356" stroke="#30363d"/>',
    ]
    row_height = 10
    for r in range(rows):
        chars = []
        for c in range(cols):
            pixel = gray.getpixel((c, r))
            idx = round((255 - pixel) / 255 * (len(RAMP) - 1))
            chars.append(RAMP[idx])
        line = "".join(chars).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        y = 43 + r * row_height
        clip_id = f"reveal{r}"
        begin = r * 0.045
        out.append(
            f'<clipPath id="{clip_id}"><rect x="8" y="{y - 8}" width="0" height="11">'
            f'<animate attributeName="width" from="0" to="354" dur="0.72s" begin="{begin:.3f}s" fill="freeze"/>'
            f'</rect></clipPath>'
        )
        out.append(f'<text x="10" y="{y}" class="art" clip-path="url(#{clip_id})">{line}</text>')
    out.extend([
        '<text x="14" y="412" font-size="9" class="muted">AI / ML · GenAI · Data Systems</text>',
        '<text x="14" y="424" font-size="9" fill="#39d353">krish@github:~$ <tspan class="cursor">█</tspan></text>',
        '</svg>',
    ])
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Rendered {OUT} from {label}")


if __name__ == "__main__":
    main()
