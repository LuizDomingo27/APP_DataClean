"""
Tema visual — Light Aqua Modern
Fundo branco · acentos verde neon-água · bordas suaves
Tipografia: Syne (display) + DM Mono (code/labels)
"""

STYLES = """
<style>
/* ── Tokens ───────────────────────────────────────────────────────────────── */
:root {
    --bg:         #F0F7F5;
    --surface:    #FFFFFF;
    --panel:      #E8F4F1;
    --rim:        #D0E8E3;
    --wire:       #B8D8D2;
    --wire-hi:    #8ECAC2;

    --aqua:       #00C4A0;
    --aqua-dim:   rgba(0,196,160,0.07);
    --aqua-glow:  rgba(0,196,160,0.20);
    --aqua-mid:   rgba(0,196,160,0.35);
    --aqua-deep:  #00967A;
    --aqua-neon:  #00E5C3;

    --teal:       #00B894;
    --teal-dim:   rgba(0,184,148,0.09);

    --text-hi:    #0A1F1C;
    --text-mid:   #2E6B61;
    --text-lo:    #7AADA6;
    --muted:      #5E9990;
    --faded:      #D4EDE9;

    --r-sm: 4px;
    --r-md: 10px;
    --r-lg: 16px;

    --ease: cubic-bezier(0.16, 1, 0.3, 1);
    --t:    180ms;

    --shadow-sm: 0 1px 3px rgba(0,80,60,0.06), 0 2px 8px rgba(0,80,60,0.04);
    --shadow-md: 0 2px 12px rgba(0,80,60,0.08), 0 4px 20px rgba(0,80,60,0.05);
    --shadow-lg: 0 4px 24px rgba(0,80,60,0.10), 0 8px 40px rgba(0,80,60,0.07);
}

/* ── Reset ────────────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background: var(--bg) !important;
    color: var(--text-hi) !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: var(--bg) !important;
    min-height: 100vh;
}

/* Faixa neon topo */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg,
        var(--aqua-neon) 0%,
        var(--aqua)      50%,
        var(--teal)      100%
    );
    z-index: 9999;
    pointer-events: none;
}

/* ── Layout ───────────────────────────────────────────────────────────────── */
.main .block-container {
    padding: 2.5rem 3rem 5rem !important;
    max-width: 1200px !important;
    position: relative;
}

/* ── Header ───────────────────────────────────────────────────────────────── */
.app-header {
    padding: 3rem 0 2rem;
    text-align: center;
    margin-bottom: 3rem;
}

.app-header h1 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 2.25rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    color: var(--text-hi);
    margin: 0 0 0.5rem;
    line-height: 1.1;
}

.neon-cyan   { color: var(--aqua);      }
.neon-violet { color: var(--aqua-deep); }

.app-header p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.75rem;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin: 0;
}

/* Linha divisória com glow suave */
.header-rule {
    margin: 2rem auto 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        var(--wire) 20%,
        var(--aqua-mid) 50%,
        var(--wire) 80%,
        transparent 100%
    );
    position: relative;
}

.header-rule::after {
    content: '';
    position: absolute;
    top: -2px; left: 30%; right: 30%;
    height: 5px;
    background: var(--aqua);
    filter: blur(6px);
    opacity: 0.25;
}

/* ── Label de seção ───────────────────────────────────────────────────────── */
.section-label {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
    color: var(--aqua);
    opacity: 0.9;
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
    border: 1px solid var(--rim);
    border-radius: var(--r-lg);
    padding: 1.1rem 1.2rem 0.7rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    transition:
        border-color var(--t) var(--ease),
        box-shadow   var(--t) var(--ease),
        transform    var(--t) var(--ease);
}

/* Linha neon no topo do card no hover */
.upload-card::before {
    content: '';
    position: absolute;
    top: 0; left: 15%; right: 15%;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--aqua), transparent);
    border-radius: 0 0 4px 4px;
    opacity: 0;
    transition: opacity var(--t) var(--ease);
}

/* Canto decorativo */
.upload-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 24px; height: 24px;
    border-top: 2px solid var(--aqua);
    border-left: 2px solid var(--aqua);
    border-radius: var(--r-lg) 0 0 0;
    opacity: 0;
    transition: opacity var(--t) var(--ease);
}

.upload-card:hover {
    border-color: var(--aqua-mid);
    box-shadow: var(--shadow-md), 0 0 0 3px var(--aqua-dim);
    transform: translateY(-2px);
}

.upload-card:hover::before,
.upload-card:hover::after {
    opacity: 1;
}

/* Variante Envios */
.upload-card--violet {
    border-color: var(--faded);
    background: var(--surface);
}

.upload-card--violet::after {
    border-color: var(--teal);
}

.upload-card--violet:hover {
    border-color: rgba(0,184,148,0.4);
    box-shadow: var(--shadow-md), 0 0 0 3px var(--teal-dim);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.25rem;
}

.card-icon  { font-size: 1rem; line-height: 1; }

.card-title {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-hi);
    letter-spacing: -0.01em;
}

.card-desc {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.72rem;
    font-weight: 400;
    text-align: center;
    border: 1px solid;
    line-height: 1.5;
    transition: all var(--t) var(--ease);
}

.file-chip--ok {
    background: var(--teal-dim);
    border-color: rgba(0,184,148,0.3);
    color: var(--aqua-deep);
}

.file-chip--wait {
    background: var(--panel);
    border-color: var(--rim);
    color: var(--text-lo);
}

/* ── Botão principal ──────────────────────────────────────────────────────── */
.stButton > button {
    background: var(--surface) !important;
    color: var(--aqua-deep) !important;
    border: 1.5px solid var(--aqua-mid) !important;
    border-radius: var(--r-md) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    padding: 0.6rem 1.5rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all var(--t) var(--ease) !important;
}

.stButton > button:hover {
    background: var(--aqua) !important;
    border-color: var(--aqua) !important;
    color: #FFFFFF !important;
    box-shadow: var(--shadow-md), 0 0 22px var(--aqua-glow) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:disabled {
    background: var(--panel) !important;
    color: var(--text-lo) !important;
    border-color: var(--rim) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* Botão de download */
.stDownloadButton > button {
    background: var(--surface) !important;
    color: var(--aqua-deep) !important;
    border: 1.5px solid var(--wire) !important;
    border-radius: var(--r-md) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all var(--t) var(--ease) !important;
}

.stDownloadButton > button:hover {
    background: var(--teal-dim) !important;
    border-color: var(--teal) !important;
    box-shadow: var(--shadow-md), 0 0 16px var(--aqua-glow) !important;
    transform: translateY(-1px) !important;
}

/* ── Métricas ─────────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--rim) !important;
    border-radius: var(--r-lg) !important;
    padding: 1.1rem 1.25rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all var(--t) var(--ease) !important;
    position: relative !important;
    overflow: hidden !important;
}

[data-testid="stMetric"]::after {
    content: '' !important;
    position: absolute !important;
    bottom: 0; left: 0; right: 0;
    height: 2px !important;
    background: linear-gradient(90deg, var(--aqua-neon), var(--teal)) !important;
    opacity: 0 !important;
    transition: opacity var(--t) var(--ease) !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--aqua-mid) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMetric"]:hover::after { opacity: 1 !important; }

[data-testid="stMetricValue"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: var(--aqua-deep) !important;
}

[data-testid="stMetricLabel"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

[data-testid="stMetricDelta"] {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
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
    border-bottom: 2px solid transparent !important;
    color: var(--muted) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1rem !important;
    margin-bottom: -1px !important;
    transition: all var(--t) var(--ease) !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-mid) !important;
    background: var(--aqua-dim) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--aqua-deep) !important;
    border-bottom-color: var(--aqua) !important;
    background: transparent !important;
    font-weight: 500 !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding: 1.5rem 0 0 !important;
}

/* ── DataFrames ───────────────────────────────────────────────────────────── */
.stDataFrame {
    border: 1px solid var(--rim) !important;
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Expander ─────────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--rim) !important;
    border-radius: var(--r-md) !important;
    color: var(--text-mid) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.04em !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all var(--t) var(--ease) !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--wire-hi) !important;
    color: var(--text-hi) !important;
    background: var(--panel) !important;
}

.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--rim) !important;
    border-top: none !important;
    border-radius: 0 0 var(--r-md) var(--r-md) !important;
    padding: 1rem !important;
}

/* ── Preview title ────────────────────────────────────────────────────────── */
.preview-title {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
    background: var(--teal-dim);
    color: var(--aqua-deep);
    border: 1px solid rgba(0,184,148,0.25);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.65rem;
    padding: 1px 8px;
    border-radius: 999px;
    letter-spacing: 0.04em;
}

/* ── File uploader ────────────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1.5px dashed var(--wire) !important;
    border-radius: var(--r-md) !important;
    transition: all var(--t) var(--ease) !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: var(--aqua-mid) !important;
    background: var(--aqua-dim) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: var(--muted) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.72rem !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--panel); border-radius: 999px; }
::-webkit-scrollbar-thumb {
    background: var(--wire-hi);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: var(--aqua-mid); }

/* ── HR ───────────────────────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--wire) !important;
    margin: 1.5rem 0 !important;
}

/* ── Alertas ──────────────────────────────────────────────────────────────── */
.stAlert {
    border-radius: var(--r-md) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    font-size: 0.75rem !important;
    border-left-color: var(--aqua) !important;
}

/* ── Animações de entrada ─────────────────────────────────────────────────── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0);   }
}

.upload-card {
    animation: fadeIn 0.35s var(--ease) both;
}

/* ── Spinner ──────────────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--aqua) !important; }

/* ── Merge info box ───────────────────────────────────────────────────────── */
.merge-box {
    width: 100%;
    background: var(--panel);
    border: 1.5px dashed var(--wire);
    border-radius: var(--r-lg);
    padding: 1rem;
    text-align: center;
}

.merge-box p {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    font-size: 0.7rem;
    color: var(--muted);
    margin: 0;
    line-height: 1.8;
}

.merge-box .accent { color: var(--aqua-deep); font-weight: 500; }
</style>
"""
