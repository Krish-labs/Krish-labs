"""Generate the terminal-style profile information card."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "info-card.svg"


def main() -> None:
    rows = [
        ("ROLE", "AI/ML Engineer · GenAI Developer"),
        ("FOCUS", "Agentic AI, RAG, DataOps"),
        ("STACK", "Python, SQL, PySpark, LangGraph"),
        ("RETRIEVAL", "Embeddings, hybrid search, reranking"),
        ("BUILDING", "AI incident-analysis copilot"),
        ("TOOLING", "Databricks, FastAPI, vector DBs"),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="490" height="430" viewBox="0 0 490 430" role="img" aria-labelledby="title desc">',
        '<title id="title">Krish Gupta terminal info card</title>',
        '<desc id="desc">Skills and focus areas shown in an animated terminal panel.</desc>',
        '<rect width="490" height="430" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.muted{fill:#8b949e}.key{fill:#79c0ff}.value{fill:#c9d1d9;opacity:0;animation:appear .55s ease-out forwards}@keyframes appear{to{opacity:1}}</style>',
        '<rect x="1" y="1" width="488" height="36" rx="11" fill="#161b22"/>',
        '<circle cx="18" cy="19" r="5" fill="#ff7b72"/><circle cx="35" cy="19" r="5" fill="#d29922"/><circle cx="52" cy="19" r="5" fill="#3fb950"/>',
        '<text x="72" y="23" font-size="11" class="muted">krish@github — profile.conf</text>',
        '<text x="20" y="61" font-size="13" fill="#39d353">krish@github:~$ neofetch --profile</text>',
        '<text x="20" y="88" font-size="11" class="muted">PROFILE // ENGINEERING NOTES</text>',
    ]
    for i, (key, value) in enumerate(rows):
        y = 125 + i * 44
        delay = i * 180
        out.append(f'<text x="22" y="{y}" font-size="11" class="key">{key}</text>')
        out.append(f'<text x="136" y="{y}" font-size="11" class="value" style="animation-delay:{delay}ms">{value}</text>')
        out.append(f'<path d="M20 {y + 13}H470" stroke="#21262d"/>')
    out.extend([
        '<text x="20" y="397" font-size="10" class="muted">status: learning · shipping · improving</text>',
        '<text x="20" y="416" font-size="10" fill="#39d353">ready for the next challenge_</text>',
        '</svg>',
    ])
    OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Rendered {OUT}")


if __name__ == "__main__":
    main()
