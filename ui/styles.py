"""
Tema visual — Dark Neon Terminal
Minimalista com acentos neon: ciano #00FFC2, roxo #9B5CFF, verde-água #00D4AA
Tipografia: Syne (display) + DM Mono (code/labels)
"""

STYLES = """
<style>
/* ── Fontes ───────────────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Tokens ───────────────────────────────────────────────────────────────── */
:root {
    --void:       #060A0F;
    --surface:    #0B1017;
    --panel:      #0F1923;
    --rim:        #131F2D;
    --wire:       #1A2A3A;
    --wire-hi:    #243548;

    --cyan:       #00FFC2;
    --cyan-dim:   rgba(0,255,194,0.08);
    --cyan-glow:  rgba(0,255,194,0.18);
    --cyan-mid:   rgba(0,255,194,0.45);

    --violet:     #9B5CFF;
    --violet-dim: rgba(155,92,255,0.08);
    --violet-glow:rgba(155,92,255,0.18);

    --teal:       #00D4AA;
    --teal-dim:   rgba(0,212,170,0.08);

    --mint:       #A8FFE8;
    --ghost:      rgba(168,255,232,0.55);
    --muted:      #3D566E;
    --faded:      #1E3347;

    --text-hi:    #E8F4F0;
    --text-mid:   #8BAAB8;
    --text-lo:    #3D566E;

    --r-sm: 4px;
    --r-md: 8px;
    --r-lg: 12px;

    --ease: cubic-bezier(0.16, 1, 0.3, 1);
    --t:    180ms;
}

/* ── Reset ────────────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace !important;
    background: var(--void) !important;
    color: var(--text-hi) !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: var(--void) !important;
    min-height: 100vh;
}

/* Ruído sutil de fundo */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
    opacity: 0.4;
}

/* Acento luminoso no topo */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        var(--cyan-mid) 30%,
        var(--violet) 70%,
        transparent
    );
    opacity: 0.5;
    pointer-events: none;
    z-index: 1;
}



/* ── Layout ───────────────────────────────────────────────────────────────── */
.main .block-container {
    padding: 2.5rem 3rem 5rem !important;
    max-width: 1200px !important;
    position: relative;
    z-index: 2;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
.app-header {
    padding: 3rem 0 2rem;
    text-align: center;
    position: relative;
    margin-bottom: 3rem;
}

.app-header h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.25rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--text-hi);
    margin: 0 0 0.5rem;
    line-height: 1.1;
}

.neon-cyan  { color: var(--cyan);   }
.neon-violet{ color: var(--violet); }

.app-header p {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin: 0;
}

/* Linha divisória com glow */
.header-rule {
    margin: 2rem auto 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        var(--wire-hi) 20%,
        var(--cyan-mid) 50%,
        var(--wire-hi) 80%,
        transparent 100%
    );
    position: relative;
}

.header-rule::after {
    content: '';
    position: absolute;
    top: -2px; left: 30%; right: 30%;
    height: 5px;
    background: var(--cyan);
    filter: blur(6px);
    opacity: 0.4;
}

/* ── Label de seção ───────────────────────────────────────────────────────── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.section-label::before {
    content: '//';
    color: var(--cyan);
    opacity: 0.7;
    font-size: 0.7rem;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--wire);
}

/* ── Cards de upload ──────────────────────────────────────────────────────── */
.upload-card {
    background: var(--surface);
    border: 1px solid var(--wire);
    border-radius: var(--r-lg);
    padding: 1.1rem 1.2rem 0.7rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
    transition:
        border-color var(--t) var(--ease),
        background  var(--t) var(--ease),
        box-shadow  var(--t) var(--ease),
        transform   var(--t) var(--ease);
}

/* Corner accent — canto superior esquerdo */
.upload-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 28px; height: 28px;
    border-top: 2px solid var(--cyan);
    border-left: 2px solid var(--cyan);
    border-radius: var(--r-lg) 0 0 0;
    opacity: 0;
    transition: opacity var(--t) var(--ease);
}

/* Ponto de glow no canto */
.upload-card::after {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 6px; height: 6px;
    background: var(--cyan);
    border-radius: 0 0 4px 0;
    opacity: 0;
    box-shadow: 0 0 12px 4px var(--cyan-glow);
    transition: opacity var(--t) var(--ease);
}

.upload-card:hover {
    border-color: var(--wire-hi);
    background: var(--panel);
    box-shadow:
        0 0 0 1px var(--wire-hi),
        0 8px 32px rgba(0,0,0,0.5),
        inset 0 1px 0 rgba(255,255,255,0.02);
    transform: translateY(-2px);
}

.upload-card:hover::before,
.upload-card:hover::after {
    opacity: 1;
}

/* Variante roxo (Envios) */
.upload-card--violet {
    border-color: var(--faded);
    background: var(--surface);
}

.upload-card--violet::before {
    border-color: var(--violet);
}

.upload-card--violet::after {
    background: var(--violet);
    box-shadow: 0 0 12px 4px var(--violet-glow);
}

.upload-card--violet:hover {
    border-color: rgba(155,92,255,0.3);
    box-shadow:
        0 0 0 1px rgba(155,92,255,0.2),
        0 8px 32px rgba(0,0,0,0.5),
        0 0 40px rgba(155,92,255,0.06);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.card-icon { font-size: 1rem; line-height: 1; }

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-hi);
    letter-spacing: -0.01em;
}

.card-desc {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin: 0 0 0.5rem;
    letter-spacing: 0.02em;
    line-height: 1.6;
}

/* ── Chips de status ──────────────────────────────────────────────────────── */
.file-chip {
    border-radius: var(--r-md);
    padding: 0.55rem 0.7rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 400;
    text-align: center;
    border: 1px solid;
    line-height: 1.5;
    transition: all var(--t) var(--ease);
}

.file-chip--ok {
    background: rgba(0,212,170,0.06);
    border-color: rgba(0,212,170,0.25);
    color: var(--teal);
}

.file-chip--wait {
    background: transparent;
    border-color: var(--wire);
    color: var(--text-lo);
}

/* ── Botões ───────────────────────────────────────────────────────────────── */
.stButton > button {
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid var(--cyan-mid) !important;
    border-radius: var(--r-md) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    padding: 0.6rem 1.5rem !important;
    transition: all var(--t) var(--ease) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: var(--cyan-dim) !important;
    opacity: 0 !important;
    transition: opacity var(--t) var(--ease) !important;
}

.stButton > button:hover {
    background: var(--cyan-dim) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 24px var(--cyan-glow), inset 0 0 24px rgba(0,255,194,0.04) !important;
    color: var(--cyan) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 0 8px var(--cyan-glow) !important;
}

.stButton > button:disabled {
    background: transparent !important;
    color: var(--wire-hi) !important;
    border-color: var(--wire) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--teal) !important;
    border: 1px solid rgba(0,212,170,0.3) !important;
    border-radius: var(--r-md) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    transition: all var(--t) var(--ease) !important;
}

.stDownloadButton > button:hover {
    background: var(--teal-dim) !important;
    border-color: var(--teal) !important;
    box-shadow: 0 0 20px rgba(0,212,170,0.15) !important;
    transform: translateY(-1px) !important;
}

/* ── Métricas ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-lg) !important;
    padding: 1.1rem 1.25rem !important;
    transition: all var(--t) var(--ease) !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stMetric"]::after {
    content: '' !important;
    position: absolute !important;
    bottom: 0; left: 0; right: 0;
    height: 1px !important;
    background: linear-gradient(90deg, var(--cyan), var(--violet)) !important;
    opacity: 0 !important;
    transition: opacity var(--t) var(--ease) !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--wire-hi) !important;
    background: var(--panel) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
}

[data-testid="stMetric"]:hover::after { opacity: 1 !important; }

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: var(--cyan) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    color: var(--text-lo) !important;
}

/* ── Tabs ─────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--wire) !important;
    gap: 0 !important;
    padding: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid transparent !important;
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1rem !important;
    margin-bottom: -1px !important;
    transition: all var(--t) var(--ease) !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-mid) !important;
    background: rgba(0,255,194,0.02) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom-color: var(--cyan) !important;
    background: transparent !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding: 1.5rem 0 0 !important;
}

/* ── DataFrames ───────────────────────────────────────────────────────────── */
.stDataFrame {
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
}

/* ── Expander ─────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-mid) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
    transition: all var(--t) var(--ease) !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--wire-hi) !important;
    color: var(--text-hi) !important;
    background: var(--panel) !important;
}

.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--wire) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r-md) var(--r-md) !important;
    padding: 1rem !important;
}

/* ── Preview title ────────────────────────────────────────────────────────── */
.preview-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 0.08em;
    margin: 0 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    text-transform: uppercase;
}

.row-badge {
    display: inline-flex;
    align-items: center;
    background: var(--cyan-dim);
    color: var(--cyan);
    border: 1px solid rgba(0,255,194,0.2);
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    padding: 1px 8px;
    border-radius: 999px;
    letter-spacing: 0.04em;
}

/* ── File uploader ────────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px dashed var(--wire-hi) !important;
    border-radius: var(--r-md) !important;
    transition: all var(--t) var(--ease) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--cyan-mid) !important;
    background: var(--cyan-dim) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--muted) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: var(--wire-hi);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── HR ───────────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--wire) !important;
    margin: 1.5rem 0 !important;
}

/* ── Alertas ──────────────────────────────────────────────────────────────── */
.stAlert {
    border-radius: var(--r-md) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    border-left-color: var(--cyan) !important;
}

/* ── Animações de entrada ─────────────────────────────────────────────────── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0);    }
}

.upload-card {
    animation: fadeIn 0.35s var(--ease) both;
}

/* ── Spinner ──────────────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--cyan) !important; }

/* ── Merge info box ───────────────────────────────────────────────────────── */
.merge-box {
    width: 100%;
    background: transparent;
    border: 1px dashed rgba(0,255,194,0.12);
    border-radius: var(--r-lg);
    padding: 1rem;
    text-align: center;
}

.merge-box p {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.8;
}

.merge-box .accent { color: var(--cyan); font-weight: 500; }
</style>
"""
