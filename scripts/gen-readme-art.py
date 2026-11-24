"""Generate README section art (headers, build strip, project covers, stat tiles).

Usage: python3 scripts/gen-readme-art.py assets
Edit the text in HEADERS, STEPS, TILES or the cover() calls, then re-run.
hero.svg is hand-written and not produced here.
"""
import os, sys

OUT = sys.argv[1]
BG1, BG2 = "#0d0c11", "#17141c"
RED, AMBER, CREAM, MUTED, LINE = "#d9442b", "#f2a93b", "#efe6d8", "#8f8799", "#2a2230"

FONTS = """
      .sans { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
      .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }
      .fade { animation: rise 0.8s ease-out both; }
      @keyframes rise { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
      .draw { stroke-dasharray: 1; animation: draw 1.4s cubic-bezier(.6,.05,.3,1) both; }
      @keyframes draw { from { stroke-dashoffset: 1; } to { stroke-dashoffset: 0; } }
      @media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, title, body, extra_defs="", extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
  <title>{esc(title)}</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>
    <linearGradient id="heat" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#fff" stroke-opacity="0.035"/></pattern>{extra_defs}
    <style>{FONTS}{extra_css}
    </style>
  </defs>
{body}
</svg>
"""


def write(name, content):
    path = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


# ---------- section headers ----------
def header(num, title, kicker):
    body = f"""  <rect width="1200" height="112" rx="14" fill="url(#bg)"/>
  <rect width="1200" height="112" rx="14" fill="url(#grid)"/>
  <g class="fade">
    <text x="32" y="38" class="mono" font-size="14" fill="{RED}" letter-spacing="4">{num} / {esc(kicker.upper())}</text>
    <text x="30" y="80" class="sans" font-size="38" font-weight="800" fill="{CREAM}" letter-spacing="-0.5">{esc(title)}</text>
  </g>
  <path d="M32 98H1168" stroke="{LINE}" stroke-width="2"/>
  <path class="draw" pathLength="1" d="M32 98H1168" stroke="url(#heat)" stroke-width="2.5" stroke-linecap="round"/>
  <circle r="4.5" cy="98" fill="{AMBER}">
    <animate attributeName="cx" values="32;1168;1168" keyTimes="0;0.35;1" dur="7s" begin="1.4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.03;0.33;0.36;1" dur="7s" begin="1.4s" repeatCount="indefinite"/>
  </circle>
  <text x="1168" y="80" text-anchor="end" class="sans" font-size="56" font-weight="800" fill="{CREAM}" fill-opacity="0.06">{num}</text>"""
    return svg(1200, 112, title, body)


HEADERS = [
    ("01", "The way I build", "process"),
    ("02", "Things I've shipped", "products"),
    ("03", "Beyond the code", "people & product"),
    ("04", "What I build with", "toolkit"),
    ("05", "Shipping log", "live from github"),
]
for num, title, kicker in HEADERS:
    slug = title.lower().replace("'", "").replace(" ", "-")
    write(f"headers/{num}-{slug}.svg", header(num, title, kicker))


# ---------- how I build strip ----------
STEPS = [
    ("01", "Find the user", "who hurts, and how", "do I know?"),
    ("02", "Write it down", "PRD, success metric,", "and the non-goals"),
    ("03", "Ship one flow", "end to end: web, mobile,", "desktop, API"),
    ("04", "Measure it", "did it work? then", "decide what's next"),
]


def build_strip():
    w, h, x0, gap, cw = 1200, 250, 20, 20, 275
    parts = [f'  <rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>',
             f'  <rect width="{w}" height="{h}" rx="18" fill="url(#grid)"/>',
             f'  <path d="M{x0 + 40} 62H{w - 60}" stroke="{LINE}" stroke-width="2" stroke-dasharray="3 7"/>',
             f'  <path class="draw" pathLength="1" d="M{x0 + 40} 62H{w - 60}" stroke="url(#heat)" stroke-width="2.5" style="animation-duration:2.4s"/>']
    for i, (n, t, s1, s2) in enumerate(STEPS):
        x = x0 + i * (cw + gap)
        d = 0.3 + i * 0.35
        parts.append(f"""  <g class="fade" style="animation-delay:{d:.2f}s">
    <rect x="{x}" y="96" width="{cw}" height="134" rx="14" fill="#141119" stroke="{LINE}" stroke-width="1.5"/>
    <text x="{x + 22}" y="138" class="sans" font-size="25" font-weight="800" fill="{CREAM}">{esc(t)}</text>
    <text x="{x + 22}" y="174" class="sans" font-size="18" fill="#b4adbd">{esc(s1)}</text>
    <text x="{x + 22}" y="200" class="sans" font-size="18" fill="#b4adbd">{esc(s2)}</text>
  </g>
  <g transform="translate({x + 40} 62)">
    <circle class="pulse" style="animation-delay:{i * 1.5:.1f}s" r="24" fill="#141119" stroke="{AMBER}" stroke-width="2"/>
    <text y="6" text-anchor="middle" class="mono" font-size="16" font-weight="700" fill="{AMBER}">{n}</text>
  </g>""")
    parts.append(f"""  <circle r="6" cy="62" fill="{AMBER}">
    <animate attributeName="cx" values="{x0 + 40};{w - 60}" dur="6s" repeatCount="indefinite"/>
  </circle>
  <text x="{w - 40}" y="68" text-anchor="end" class="mono" font-size="14" fill="{MUTED}" letter-spacing="2">↺</text>""")
    css = f"""
      .pulse {{ animation: pulse 6s ease-in-out infinite; }}
      @keyframes pulse {{ 0%, 100% {{ stroke-opacity: 0.35; }} 6% {{ stroke-opacity: 1; stroke-width: 4; }} 25% {{ stroke-opacity: 0.35; stroke-width: 2; }} }}"""
    return svg(w, h, "How I build: find the user, write it down, ship one flow, measure it", "\n".join(parts), extra_css=css)


write("how-i-build.svg", build_strip())


# ---------- project covers ----------
def cover(slug, title, tag, label, accent, motif, motif_css=""):
    w, h = 600, 260
    body = f"""  <rect width="{w}" height="{h}" rx="16" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" rx="16" fill="url(#grid)"/>
  <circle cx="470" cy="130" r="150" fill="url(#glow)"/>
  <rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="15.5" fill="none" stroke="{accent}" stroke-opacity="0.35" stroke-width="1.5"/>
{motif}
  <g class="fade">
    <text x="32" y="50" class="mono" font-size="14" fill="{accent}" letter-spacing="3">{esc(label.upper())}</text>
    <text x="30" y="118" class="sans" font-size="54" font-weight="800" fill="{CREAM}" letter-spacing="-1">{esc(title)}</text>
  </g>
  <g class="fade" style="animation-delay:0.3s">
    <text x="32" y="162" class="sans" font-size="20" fill="#b4adbd">{esc(tag[0])}</text>
    <text x="32" y="190" class="sans" font-size="20" fill="#b4adbd">{esc(tag[1])}</text>
  </g>
  <rect x="32" y="214" width="56" height="4" rx="2" fill="{accent}"/>"""
    defs = f"""
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="{accent}" stop-opacity="0.22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>"""
    write(f"projects/{slug}.svg", svg(w, h, f"{title}: {tag[0]} {tag[1]}", body, defs, motif_css))


# Strata: stacked layers with a scan line and a citation chip
cover("strata", "Strata", ("Ask any repo a question.", "Answers cited to the line."), "AI · RAG", AMBER, f"""  <g transform="translate(470 120)">
    <g fill="#141119" stroke="{AMBER}" stroke-width="1.6">
      <path class="lay l3" d="M-90 40L0 0 90 40 0 80Z" stroke-opacity="0.4"/>
      <path class="lay l2" d="M-90 10L0 -30 90 10 0 50Z" stroke-opacity="0.65"/>
      <path class="lay l1" d="M-90 -20L0 -60 90 -20 0 20Z"/>
    </g>
    <path d="M-40 -22h50M-30 -12h44M-48 -32h30" stroke="{CREAM}" stroke-opacity="0.6" stroke-width="2" stroke-linecap="round" transform="skewY(0)"/>
    <rect class="scan" x="-95" y="-62" width="190" height="3" fill="{AMBER}" opacity="0.8"/>
  </g>
  <g transform="translate(392 222)"><g class="chip">
    <rect width="168" height="26" rx="13" fill="{AMBER}" fill-opacity="0.12" stroke="{AMBER}" stroke-opacity="0.6"/>
    <text x="84" y="17.5" text-anchor="middle" class="mono" font-size="12" fill="{AMBER}">src/lib/rag.ts:42</text>
  </g></g>""", """
      .lay { animation: float 4s ease-in-out infinite; }
      .l2 { animation-delay: -1.3s; } .l3 { animation-delay: -2.6s; }
      @keyframes float { 50% { transform: translateY(-4px); } }
      .scan { animation: scan 3.2s ease-in-out infinite; }
      @keyframes scan { 0% { transform: translateY(0); opacity: 0; } 15% { opacity: 0.85; } 85% { opacity: 0.85; } 100% { transform: translateY(140px); opacity: 0; } }
      .chip { animation: rise 0.6s ease-out 1s both; }""")

# Proctra: countdown ring
cover("proctra", "Proctra", ("Timed exams on macOS. Fair,", "without being creepy."), "Desktop · Exams", RED, f"""  <g transform="translate(475 125)">
    <circle r="72" fill="#141119" stroke="{LINE}" stroke-width="10"/>
    <circle class="ring" r="72" fill="none" stroke="{RED}" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1" transform="rotate(-90)"/>
    <text y="4" text-anchor="middle" class="mono" font-size="30" font-weight="700" fill="{CREAM}">29:59</text>
    <text y="30" text-anchor="middle" class="mono" font-size="11" fill="{MUTED}" letter-spacing="3">AUTOSAVED</text>
    <circle class="tick" cx="0" cy="-72" r="6" fill="{AMBER}"/>
  </g>""", """
      .ring { animation: count 8s linear infinite; }
      @keyframes count { from { stroke-dashoffset: 0; } to { stroke-dashoffset: 1; } }
      .tick { transform-origin: 0 0; animation: spin 8s linear infinite; }
      @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(-360deg); } }""")

# Luna: crescent moon with twinkling stars and a sword stroke
stars = "".join(
    f'<circle class="tw" style="animation-delay:-{i * 0.7:.1f}s" cx="{x}" cy="{y}" r="{r}" fill="{CREAM}"/>'
    for i, (x, y, r) in enumerate([(380, 50, 1.8), (420, 210, 1.4), (560, 60, 2), (545, 205, 1.5), (360, 140, 1.3), (520, 30, 1.2)]))
cover("luna", "Luna", ("A pocket dojo for engineers.", "Five-minute fights with real code."), "Mobile · Game", "#c9b8ff", f"""  <g>{stars}</g>
  <g transform="translate(470 125)">
    <mask id="cres"><circle r="66" fill="#fff"/><circle cx="26" cy="-16" r="60" fill="#000"/></mask>
    <circle r="66" fill="#efe6d8" mask="url(#cres)"/>
    <path class="slash" pathLength="1" d="M-110 70L110 -80" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>
  </g>""", """
      .tw { animation: tw 2.8s ease-in-out infinite; }
      @keyframes tw { 50% { opacity: 0.15; } }
      .slash { stroke-dasharray: 1; animation: slash 4s cubic-bezier(.7,0,.2,1) infinite; }
      @keyframes slash { 0% { stroke-dashoffset: 1; opacity: 1; } 18% { stroke-dashoffset: 0; opacity: 1; } 40%, 100% { stroke-dashoffset: 0; opacity: 0; } }""")

# JMusic: equalizer bars inside a terminal window
bars = "".join(
    f'<rect class="bar" style="animation-delay:-{(i * 0.37) % 1.2:.2f}s" x="{-92 + i * 20}" y="-50" width="12" height="70" rx="3" fill="#a8c686"/>'
    for i in range(10))
cover("jmusic", "JMusic", ("Stream Creative Commons music", "without leaving the terminal."), "CLI · TUI", "#a8c686", f"""  <g transform="translate(470 130)">
    <rect x="-112" y="-88" width="224" height="170" rx="10" fill="#141119" stroke="{LINE}" stroke-width="1.5"/>
    <circle cx="-96" cy="-74" r="4" fill="{RED}"/><circle cx="-84" cy="-74" r="4" fill="{AMBER}"/><circle cx="-72" cy="-74" r="4" fill="#a8c686"/>
    <g transform="translate(0 4)">{bars}</g>
    <text x="-96" y="62" class="mono" font-size="12" fill="#a8c686">▶ now playing  02:14</text>
  </g>""", """
      .bar { transform-box: fill-box; transform-origin: bottom; animation: eq 1.2s ease-in-out infinite; }
      @keyframes eq { 0%, 100% { transform: scaleY(0.25); } 50% { transform: scaleY(1); } }""")

# Loop: chat bubbles with typing dots
cover("loop", "Loop", ("Campus chat shaped like the", "university really is."), "Mobile · Realtime · Building", "#6ea8ff", f"""  <g transform="translate(470 125)">
    <g class="b1"><rect x="-110" y="-78" width="150" height="40" rx="14" fill="#141119" stroke="#6ea8ff" stroke-opacity="0.6"/>
      <rect x="-94" y="-62" width="96" height="8" rx="4" fill="{CREAM}" fill-opacity="0.6"/></g>
    <g class="b2"><rect x="-30" y="-24" width="140" height="40" rx="14" fill="#6ea8ff"/>
      <rect x="-14" y="-8" width="90" height="8" rx="4" fill="{BG1}" fill-opacity="0.7"/></g>
    <g class="b3"><rect x="-110" y="30" width="78" height="36" rx="14" fill="#141119" stroke="#6ea8ff" stroke-opacity="0.6"/>
      <circle class="dot" cx="-88" cy="48" r="4" fill="{CREAM}"/><circle class="dot d2" cx="-71" cy="48" r="4" fill="{CREAM}"/><circle class="dot d3" cx="-54" cy="48" r="4" fill="{CREAM}"/></g>
    <text x="108" y="38" text-anchor="end" class="mono" font-size="11" fill="#6ea8ff">✓✓ read</text>
  </g>""", """
      .b1 { animation: rise 0.5s ease-out 0.2s both; } .b2 { animation: rise 0.5s ease-out 0.7s both; } .b3 { animation: rise 0.5s ease-out 1.2s both; }
      .dot { animation: bob 1.2s ease-in-out infinite; } .d2 { animation-delay: 0.15s; } .d3 { animation-delay: 0.3s; }
      @keyframes bob { 0%, 60%, 100% { transform: translateY(0); opacity: 0.4; } 30% { transform: translateY(-5px); opacity: 1; } }""")


# ---------- stat tiles ----------
TILES = [
    ("1,000+", "students upskilled", "through 20+ bootcamps", RED),
    ("8", "hackathons run", "400 to 600+ sign-ups each", AMBER),
    ("2×", "product case finalist", "BITS Pilani · Masters' Union", "#c9b8ff"),
    ("240%", "LinkedIn growth", "25 product teardowns", "#a8c686"),
]


def tiles():
    w, h, x0, gap, tw = 1200, 200, 0, 20, 285
    parts = []
    for i, (big, l1, l2, c) in enumerate(TILES):
        x = x0 + i * (tw + gap)
        parts.append(f"""  <g class="fade" style="animation-delay:{i * 0.2:.1f}s">
    <rect x="{x + 0.75}" y="0.75" width="{tw - 1.5}" height="{h - 1.5}" rx="16" fill="url(#bg)" stroke="{c}" stroke-opacity="0.35" stroke-width="1.5"/>
    <rect x="{x + 26}" y="28" width="36" height="4" rx="2" fill="{c}"/>
    <text x="{x + 24}" y="98" class="sans" font-size="54" font-weight="800" fill="{c}" letter-spacing="-1">{esc(big)}</text>
    <text x="{x + 26}" y="138" class="sans" font-size="21" font-weight="700" fill="{CREAM}">{esc(l1)}</text>
    <text x="{x + 26}" y="166" class="sans" font-size="16" fill="{MUTED}">{esc(l2)}</text>
  </g>""")
    return svg(w, h, "1,000+ students upskilled, 8 hackathons run, 2x product case finalist, 240% LinkedIn growth", "\n".join(parts))


write("beyond.svg", tiles())
print("ok")
