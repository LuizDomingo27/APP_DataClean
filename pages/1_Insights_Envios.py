"""
Página de Insights — ENVIOS_OFICINAS
Storytelling executivo com filtros dinâmicos e gráficos interativos.
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from core.config import COLUMN_ALIASES
from core.utils import read_file, resolve_column
from ui.styles import STYLES

st.set_page_config(
    page_title="Insights · Envios",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(STYLES, unsafe_allow_html=True)

# ── Paleta (importada do design system em styles.py) ──────────────────────────
C_CYAN   = "#00FFC2"
C_VIOLET = "#9B5CFF"
C_TEAL   = "#00D4AA"
C_AMBER  = "#F59E0B"
C_RED    = "#EF4444"
C_MINT   = "#A8FFE8"
BG_DARK  = "#060A0F"
BG_CARD  = "#0F1923"
BG_SURF  = "#0B1017"
WIRE     = "#1A2A3A"
WIRE_HI  = "#243548"
TEXT_MID = "#8BAAB8"
TEXT_HI  = "#E8F4F0"
MUTED    = "#3D566E"

# ── CSS extra para KPI cards aprimorados ─────────────────────────────────────
st.markdown("""
<style>
.kpi-card {
    background: #0B1017;
    border: 1px solid #1A2A3A;
    border-radius: 8px;
    padding: 1.25rem 1.2rem;
    position: relative;
    transition: all 0.2s ease;
}
.kpi-card:hover {
    border-color: #243548;
    background: #0F1923;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.kpi-card__label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8BAAB8;
    margin: 0 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.kpi-card__icon {
    font-size: 0.9rem;
    opacity: 0.9;
}
.kpi-card__value {
    font-family: 'DM Mono', monospace;
    font-size: 1.0rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin: 0 0 1rem;
}
.kpi-card__sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #3D566E;
    margin: 0;
    line-height: 1.4;
}
.kpi-card__sub b {
    color: #8BAAB8;
    font-weight: 500;
}
.kpi-alert {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #EF4444;
    margin-top: 0.4rem;
    letter-spacing: 0.06em;
}
.chart-container {
    background: linear-gradient(145deg, #0D1822 0%, #0B1017 100%);
    border: 1px solid #1A2A3A;
    border-radius: 14px;
    padding: 1.25rem 1.25rem 0.75rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.chart-container::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00FFC2, #9B5CFF);
    opacity: 0.4;
    border-radius: 14px 14px 0 0;
}
.download-row {
    display: flex;
    justify-content: flex-end;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def plotly_base(title: str = "", height: int = 420) -> dict:
    return dict(
        title=dict(
            text=title,
            font=dict(family="DM Mono", size=11, color=MUTED),
            x=0, xanchor="left", pad=dict(l=2, b=8),
        ),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Mono", color=TEXT_MID, size=11),
        xaxis=dict(
            gridcolor=WIRE, zerolinecolor=WIRE,
            tickfont=dict(size=10), linecolor=WIRE,
        ),
        yaxis=dict(
            gridcolor=WIRE, zerolinecolor=WIRE,
            tickfont=dict(size=10), linecolor=WIRE,
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10),
            bordercolor=WIRE, borderwidth=1,
        ),
        margin=dict(l=10, r=10, t=48, b=10),
        hoverlabel=dict(
            bgcolor="#0D1822",
            font=dict(family="DM Mono", size=11),
            bordercolor=WIRE,
        ),
    )


def kpi_card(col, icon: str, label: str, value: str, sub: str,
             color: str = C_CYAN, alert: str = ""):
    col.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-card__label">
            <span class="kpi-card__icon">{icon}</span>{label}
        </p>
        <p class="kpi-card__value" style="color:{color}">{value}</p>
        <p class="kpi-card__sub">{sub}</p>
        {f'<div class="kpi-alert">⚠ {alert}</div>' if alert else ''}
    </div>
    """, unsafe_allow_html=True)


def section(text: str):
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)


def chart_wrap(fig, height_extra: int = 0):
    """Renderiza gráfico dentro de container estilizado."""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Carregamento de dados com cache ──────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file_bytes: bytes) -> pd.DataFrame:
    """Carrega e normaliza o DataFrame de envios."""
    df = pd.read_excel(io.BytesIO(file_bytes))
    df.columns = [str(c).strip() for c in df.columns]

    # ── Normaliza dtypes: pandas 2.x lê colunas de texto do Excel como
    # ArrowStringDtype (string_arrow) em vez de object. Qualquer fillna/reindex
    # com fill_value int falha nesse dtype. Convertemos tudo para object.
    for _col in df.select_dtypes(include=["string"]).columns:
        df[_col] = df[_col].astype(object)

    # Resolve coluna de data com alias flexível
    col_envio = resolve_column(df, "ENVIO") or "ENVIO"
    if col_envio in df.columns:
        df["ENVIO_DT"] = pd.to_datetime(df[col_envio], format="%d/%m/%Y", errors="coerce")
    else:
        df["ENVIO_DT"] = pd.NaT

    df["MES_NOME"] = df["ENVIO_DT"].dt.strftime("%b/%Y")
    df["MES_NUM"]  = df["ENVIO_DT"].dt.month
    df["ANO"]      = df["ENVIO_DT"].dt.year
    # float64: suporta NaT/NaN nativamente sem a semântica Int64 nullable
    df["SEMANA"] = pd.to_numeric(
        df["ENVIO_DT"].dt.isocalendar().week, errors="coerce"
    )

    # Colunas numéricas com alias flexível — usa colchetes para garantir Series
    col_qtd = resolve_column(df, "QTD") or "QTD"
    col_min = resolve_column(df, "MINUTOS") or "MINUTOS"

    df["QTD"]     = pd.to_numeric(
        df[col_qtd] if col_qtd in df.columns else pd.Series(0, index=df.index),
        errors="coerce",
    ).fillna(0)
    df["MINUTOS"] = pd.to_numeric(
        df[col_min] if col_min in df.columns else pd.Series(0, index=df.index),
        errors="coerce",
    ).fillna(0)
    df["HORAS"]   = df["MINUTOS"] / 60
    return df


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.25rem 0 1rem">
        <p style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.15em;
                  text-transform:uppercase;color:#3D566E;margin:0 0 0.35rem">// módulo</p>
        <p style="font-family:'DM Mono',monospace;font-size:0.88rem;
                  color:#00FFC2;margin:0;font-weight:500">Envios · Oficinas</p>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "ENVIOS_OFICINAS",
        type=["xlsx", "csv"],
        label_visibility="collapsed",
    )

    if not uploaded:
        st.markdown("""
        <div style="border:1px dashed #1A2A3A;border-radius:10px;
                    padding:1.5rem;text-align:center;margin-top:0.5rem">
            <p style="font-family:'DM Mono',monospace;font-size:0.72rem;
                      color:#3D566E;margin:0;line-height:2">
                📊 carregue<br>
                <span style="color:#00FFC2;font-size:0.78rem">ENVIOS_OFICINAS</span><br>
                para ver os insights
            </p>
        </div>""", unsafe_allow_html=True)

# Para fora do with: só interrompe se realmente não há arquivo
if not uploaded:
    st.stop()

# ── Carrega dados (com tratamento de erro) ────────────────────────────────────
try:
    df_raw = load_data(uploaded.read())
except Exception as exc:
    st.error(f"❌ Erro ao carregar o arquivo: {exc}")
    st.stop()

# ── Filtros (dentro do sidebar, após carregamento) ────────────────────────────
with st.sidebar:
    st.markdown('<hr style="border-color:#1A2A3A;margin:1rem 0">', unsafe_allow_html=True)
    st.markdown("""<p style="font-family:'DM Mono',monospace;font-size:0.6rem;
                             letter-spacing:0.15em;text-transform:uppercase;
                             color:#3D566E;margin:0 0 0.75rem">// filtros</p>""",
                unsafe_allow_html=True)

    # ── helper: monta lista de opções com "Todos" no topo ─────────────────────
    def sb_opts(col: str, all_label: str = "Todos") -> list:
        if col not in df_raw.columns:
            return [all_label]
        raw = df_raw[col].dropna().unique().tolist()
        return [all_label] + sorted(raw, key=str)

    # ── Filtro 1: Data (mês/ano) ───────────────────────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:0.58rem;
              letter-spacing:0.12em;text-transform:uppercase;
              color:#3D566E;margin:0.5rem 0 0.25rem">📅 período</p>""",
        unsafe_allow_html=True)

    # Gera lista de meses únicos ordenados cronologicamente
    if "MES_NOME" in df_raw.columns:
        _meses_raw = df_raw["MES_NOME"].dropna().unique().tolist()
        try:
            import pandas as _pd
            _meses = sorted(_meses_raw, key=lambda m: _pd.to_datetime(m, format="%b/%Y"))
        except Exception:
            _meses = sorted(_meses_raw, key=str)
    else:
        _meses = []
    mes_opts = ["Todos os meses"] + _meses
    sel_mes = st.selectbox("Mês", mes_opts, label_visibility="collapsed")

    # ── Filtro 2: Oficina ──────────────────────────────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:0.58rem;
              letter-spacing:0.12em;text-transform:uppercase;
              color:#3D566E;margin:0.85rem 0 0.25rem">🏭 oficina</p>""",
        unsafe_allow_html=True)
    sel_oficina = st.selectbox("Oficina", sb_opts("OFICINA", "Todas as oficinas"),
                               label_visibility="collapsed")

    # ── Filtro 3: PDV ──────────────────────────────────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:0.58rem;
              letter-spacing:0.12em;text-transform:uppercase;
              color:#3D566E;margin:0.85rem 0 0.25rem">🏪 pdv</p>""",
        unsafe_allow_html=True)
    sel_pdv = st.selectbox("PDV", sb_opts("PDV", "Todos os PDVs"),
                           label_visibility="collapsed")

    # ── Filtro 4: Dia (Data) ───────────────────────────────────────────────────
    st.markdown("""
    <p style="font-family:'DM Mono',monospace;font-size:0.58rem;
              letter-spacing:0.12em;text-transform:uppercase;
              color:#3D566E;margin:0.85rem 0 0.25rem">📆 dia</p>""",
        unsafe_allow_html=True)
        
    if "ENVIO_DT" in df_raw.columns:
        df_raw["DIA_NOME"] = df_raw["ENVIO_DT"].dt.strftime("%d/%m/%Y").fillna("Sem data")
    
    sel_dia = st.selectbox("Dia", sb_opts("DIA_NOME", "Todos os dias"),
                           label_visibility="collapsed")

    st.markdown('<hr style="border-color:#1A2A3A;margin:1rem 0">', unsafe_allow_html=True)
    st.caption(f"{len(df_raw):,} registros totais")

# ── Aplica filtros ────────────────────────────────────────────────────────────
df = df_raw.copy()

# Filtro de data (mês/ano)
if sel_mes != "Todos os meses" and "MES_NOME" in df.columns:
    df = df[df["MES_NOME"] == sel_mes]

# Filtro de oficina
if sel_oficina != "Todas as oficinas" and "OFICINA" in df.columns:
    df = df[df["OFICINA"] == sel_oficina]

# Filtro de PDV
if sel_pdv != "Todos os PDVs" and "PDV" in df.columns:
    df = df[df["PDV"] == sel_pdv]

# Filtro de dia
if sel_dia != "Todos os dias" and "DIA_NOME" in df.columns:
    df = df[df["DIA_NOME"] == sel_dia]

n_sel   = len(df)
n_total = len(df_raw)

# ── Header ────────────────────────────────────────────────────────────────────
pct = f"{n_sel / n_total * 100:.0f}%" if n_total else "—"
st.markdown(f"""
<div class="app-header" style="margin-bottom:2rem">
    <h1>Performance de <span class="neon-cyan">Envios</span>
        <span class="neon-violet">· Oficinas</span></h1>
    <p>// visão executiva · {n_sel:,} ordens de {n_total:,} ({pct})</p>
    <div class="header-rule"></div>
</div>""", unsafe_allow_html=True)

# Aviso se filtros deixaram DataFrame vazio
if n_sel == 0:
    st.warning("⚠ Nenhum registro corresponde aos filtros selecionados.", icon="⚠️")
    st.stop()

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_pecas  = int(df["QTD"].sum())
total_min    = df["MINUTOS"].sum()
total_horas  = total_min / 60
min_peca     = total_min / max(total_pecas, 1)
total_ordens = len(df)

sem_g = (
    df.dropna(subset=["SEMANA"])
    .groupby("SEMANA")
    .agg(qtd=("QTD", "sum"), min=("MINUTOS", "sum"))
    .sort_index()
)
# Semanas ISO vão até 52 ou 53 — filtramos apenas as inválidas (> 53)
sem_g = sem_g[sem_g.index <= 53]

ultima_sem  = int(sem_g.index.max()) if not sem_g.empty else 0
sem_qtd     = int(sem_g["qtd"].iloc[-1]) if not sem_g.empty else 0
sem_min_val = float(sem_g["min"].iloc[-1]) if not sem_g.empty else 0.0

bloq_qtd = (
    int(df[df["SITUAÇÃO"] != "Enviado"]["QTD"].sum())
    if "SITUAÇÃO" in df.columns else 0
)
bloq_pct = bloq_qtd / max(total_pecas, 1) * 100

section("indicadores-chave")

c1, c2, c3, c4, c5 = st.columns(5, gap="small")
kpi_card(c1, "📦", "Total Peças",
         f"{total_pecas:,}",
         f"<b>{total_ordens:,}</b> ordens no período",
         C_CYAN)

kpi_card(c2, "⏱", "Total Horas",
         f"{total_horas:,.0f}h",
         f"<b>{total_min / 1e6:.2f}M</b> minutos acumulados",
         C_VIOLET)

kpi_card(c3, "⚡", "Min / Peça",
         f"{min_peca:.1f}",
         "eficiência média por unidade",
         C_TEAL)

kpi_card(c4, f"📅", f"Semana {ultima_sem}",
         f"{sem_qtd:,}",
         f"<b>{sem_min_val / 60:,.0f}h</b> · última semana",
         C_AMBER)

kpi_card(c5, "🔴", "Bloqueadas",
         f"{bloq_qtd:,}",
         f"<b>{bloq_pct:.1f}%</b> do volume total",
         C_RED,
         alert="alto volume" if bloq_pct > 10 else "")

st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

# ── Gráfico 1 — Tendência Semanal ─────────────────────────────────────────────
section("sazonalidade · tendência semanal")

sem_df      = sem_g.reset_index().sort_values("SEMANA")
sem_df["ma3"] = sem_df["qtd"].rolling(3, center=True, min_periods=1).mean()

fig1 = make_subplots(specs=[[{"secondary_y": True}]])
fig1.add_trace(go.Scatter(
    x=sem_df["SEMANA"], y=sem_df["qtd"], name="Peças",
    mode="lines",
    line=dict(color=C_CYAN, width=2.5),
    fill="tozeroy", fillcolor="rgba(0,255,194,0.06)",
    hovertemplate="Sem %{x} — <b>%{y:,.0f}</b> peças<extra></extra>",
), secondary_y=False)
fig1.add_trace(go.Scatter(
    x=sem_df["SEMANA"], y=sem_df["ma3"], name="Tendência MA3",
    mode="lines",
    line=dict(color=C_AMBER, width=2, dash="dash"),
    hovertemplate="Sem %{x} — tendência %{y:,.0f}<extra></extra>",
), secondary_y=False)
fig1.add_trace(go.Scatter(
    x=sem_df["SEMANA"], y=sem_df["min"] / 60, name="Horas",
    mode="lines+markers",
    line=dict(color=C_VIOLET, width=1.5, dash="dot"),
    marker=dict(size=5, color=C_VIOLET, line=dict(color=BG_DARK, width=1)),
    hovertemplate="Sem %{x} — <b>%{y:,.0f}h</b><extra></extra>",
), secondary_y=True)

l1 = plotly_base("peças enviadas por semana · média móvel 3 semanas · horas", 440)
l1["yaxis"]["title"]  = "Peças"
l1["yaxis2"] = dict(
    title="Horas", overlaying="y", side="right",
    gridcolor=WIRE, tickfont=dict(size=10), showgrid=False,
    zerolinecolor=WIRE,
)
l1["xaxis"]["title"] = "Semana do Ano"
fig1.update_layout(**l1)
chart_wrap(fig1)

# ── Gráfico 2 — Volume por Matéria-Prima ──────────────────────────────────────
section("composição · volume por matéria-prima")

if "MP" in df.columns:
    mp_df = (
        df.groupby("MP")["QTD"]
        .sum()
        .sort_values(ascending=True)
        .reset_index()
    )
    bar_colors = [
        C_CYAN if str(m).lower() not in ("sem mp informada", "nan", "")
        else WIRE_HI
        for m in mp_df["MP"]
    ]
    fig2 = go.Figure(go.Bar(
        x=mp_df["QTD"], y=mp_df["MP"], orientation="h",
        marker=dict(color=bar_colors, opacity=0.88,
                    line=dict(color=BG_DARK, width=0.5)),
        text=[f"{v:,.0f}" for v in mp_df["QTD"]],
        textposition="outside", textfont=dict(size=9, color=TEXT_MID),
        hovertemplate="%{y}<br><b>%{x:,.0f}</b> peças<extra></extra>",
    ))
    l2 = plotly_base("volume por matéria-prima", max(380, len(mp_df) * 32 + 80))
    l2["showlegend"] = False
    l2["xaxis"]["title"] = "Peças"
    l2["yaxis"]["tickfont"] = dict(size=10)
    fig2.update_layout(**l2)
    chart_wrap(fig2)
else:
    st.info("Coluna **MP** não encontrada nos dados.")

# ── Gráfico 3 — Pareto de Oficinas ────────────────────────────────────────────
section("concentração de oficinas · pareto top 20")

if "OFICINA" in df.columns:
    ofc_df = (
        df[df["OFICINA"].astype(str).str.lower() != "não informado"]
        .groupby("OFICINA")["QTD"]
        .sum()
        .sort_values(ascending=False)
        .head(20)
        .reset_index()
    )
    ofc_df["acum"] = ofc_df["QTD"].cumsum() / ofc_df["QTD"].sum() * 100

    bar_c = [
        C_CYAN   if p <= 50 else
        C_TEAL   if p <= 80 else
        C_VIOLET
        for p in ofc_df["acum"]
    ]

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(
        x=ofc_df["OFICINA"], y=ofc_df["QTD"], name="Peças",
        marker=dict(color=bar_c, opacity=0.88,
                    line=dict(color=BG_DARK, width=0.5)),
        hovertemplate="%{x}<br><b>%{y:,.0f}</b> peças<extra></extra>",
    ), secondary_y=False)
    fig3.add_trace(go.Scatter(
        x=ofc_df["OFICINA"], y=ofc_df["acum"], name="Acum %",
        mode="lines+markers",
        line=dict(color=C_AMBER, width=2.5),
        marker=dict(size=6, color=C_AMBER, line=dict(color=BG_DARK, width=1)),
        hovertemplate="%{x}<br>%{y:.1f}%<extra></extra>",
    ), secondary_y=True)
    fig3.add_hline(
        y=80, secondary_y=True,
        line=dict(color=C_AMBER, dash="dot", width=1.5),
        annotation_text="80%",
        annotation_font=dict(color=C_AMBER, size=9),
    )
    l3 = plotly_base("pareto · top 20 oficinas por volume", 460)
    l3["xaxis"]["tickangle"] = -42
    l3["xaxis"]["tickfont"]  = dict(size=8)
    l3["yaxis"]["title"]     = "Peças"
    l3["yaxis2"] = dict(
        title="Acum %", overlaying="y", side="right",
        range=[0, 105], showgrid=False,
        tickfont=dict(size=9), ticksuffix="%",
        zerolinecolor=WIRE,
    )
    fig3.update_layout(**l3)
    chart_wrap(fig3)
else:
    st.info("Coluna **OFICINA** não encontrada nos dados.")

# ── Gráfico 4 — Evolução Mensal por Origem ────────────────────────────────────
section("evolução mensal · peças por origem")

# Meses derivados dinamicamente dos dados (não hardcodados)
if "MES_NOME" in df.columns and not df["MES_NOME"].dropna().empty:
    try:
        mes_order = sorted(
            df["MES_NOME"].dropna().unique(),
            key=lambda m: pd.to_datetime(m, format="%b/%Y"),
        )
    except Exception:
        mes_order = sorted(df["MES_NOME"].dropna().unique())
else:
    mes_order = []

if mes_order:
    if "ORIGEM" in df.columns:
        mes_df = df.groupby(["MES_NOME", "ORIGEM"])["QTD"].sum().reset_index()
    else:
        mes_df = df.groupby("MES_NOME")["QTD"].sum().reset_index()
        mes_df["ORIGEM"] = "TOTAL"

    palette = [C_CYAN, C_VIOLET, C_TEAL, C_AMBER, C_MINT]
    origens  = mes_df["ORIGEM"].unique()
    cores_orig = {o: palette[i % len(palette)] for i, o in enumerate(origens)}

    fig4 = go.Figure()
    for orig in origens:
        # Seleciona APENAS a coluna numérica antes do reindex para evitar
        # que colunas de string (ORIGEM) recebam fill_value=0 (int) →
        # TypeError com ArrowStringDtype do pandas 2.x
        sub_qtd = (
            mes_df[mes_df["ORIGEM"] == orig]
            .set_index("MES_NOME")["QTD"]
            .reindex(mes_order, fill_value=0)
            .reset_index()
        )
        sub_qtd.columns = ["MES_NOME", "QTD"]
        fig4.add_trace(go.Bar(
            x=sub_qtd["MES_NOME"], y=sub_qtd["QTD"], name=str(orig),
            marker=dict(
                color=cores_orig.get(orig, C_CYAN), opacity=0.88,
                line=dict(color=BG_DARK, width=0.5),
            ),
            hovertemplate=f"%{{x}} · {orig}<br><b>%{{y:,.0f}}</b> peças<extra></extra>",
        ))
    l4 = plotly_base("evolução mensal de peças por origem", 420)
    l4["barmode"] = "group"
    l4["yaxis"]["title"] = "Peças"
    l4["legend"] = dict(
        orientation="h", yanchor="bottom", y=1.02,
        bgcolor="rgba(0,0,0,0)", font=dict(size=10),
    )
    fig4.update_layout(**l4)
    chart_wrap(fig4)
else:
    st.info("Não há dados de mês para exibir no gráfico de evolução mensal.")

# ── Gráfico 5 — Donut e Tabela Lado a Lado ───────────────────────────────────
col_donut, col_table = st.columns([1.1, 2], gap="large")

with col_donut:
    section("status · distribuição de situação")

    if "SITUAÇÃO" in df.columns:
        status_counts = df.groupby("SITUAÇÃO")["QTD"].sum().reset_index()
        env_qt  = int(df[df["SITUAÇÃO"] == "Enviado"]["QTD"].sum())
        bloq_qt = int(df[df["SITUAÇÃO"] != "Enviado"]["QTD"].sum())

        pie_labels = ["Enviado", "Não Enviado / Bloqueado"]
        pie_values = [env_qt, bloq_qt]
        pie_colors = [C_CYAN, C_RED]

        fig5 = go.Figure(go.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.70,
            marker=dict(
                colors=pie_colors,
                line=dict(color=BG_DARK, width=4),
            ),
            textinfo="label+percent",
            textfont=dict(family="DM Mono", size=11, color=TEXT_MID),
            hovertemplate="%{label}<br><b>%{value:,.0f}</b> peças (%{percent})<extra></extra>",
            rotation=90,
        ))
        env_pct = env_qt / max(total_pecas, 1) * 100
        fig5.add_annotation(
            text=f"<b>{env_pct:.0f}%</b>",
            x=0.5, y=0.55, showarrow=False,
            font=dict(family="Syne", size=28, color=C_CYAN),
        )
        fig5.add_annotation(
            text="enviado",
            x=0.5, y=0.42, showarrow=False,
            font=dict(family="DM Mono", size=10, color=MUTED),
        )
        l5 = plotly_base("status das ordens · % total", 380)
        l5["legend"] = dict(
            orientation="h", yanchor="bottom", y=-0.12,
            bgcolor="rgba(0,0,0,0)", font=dict(size=10),
        )
        fig5.update_layout(**l5)
        chart_wrap(fig5)
    else:
        st.info("Coluna **SITUAÇÃO** não encontrada.")

with col_table:
    section("detalhe semanal · métricas executivas")

    if not sem_df.empty:
        tbl = (
            sem_df[["SEMANA", "qtd", "min", "ma3"]]
            .rename(columns={
                "SEMANA": "Semana",
                "qtd":    "Peças",
                "min":    "Minutos",
                "ma3":    "Tendência MA3",
            })
            .copy()
        )
        tbl["Semana"]        = tbl["Semana"].fillna(0).astype(int)
        tbl["Horas"]         = (tbl["Minutos"] / 60).round(1)
        tbl["Min/Peça"]      = (tbl["Minutos"] / tbl["Peças"].replace(0, 1)).round(1)
        tbl["Peças"]         = tbl["Peças"].fillna(0).astype(int)
        tbl["Minutos"]       = tbl["Minutos"].round(0).fillna(0).astype(int)
        tbl["Tendência MA3"] = tbl["Tendência MA3"].round(0).astype("Int64")

        # Formatação visual amigável (ponto de milhar e centralizado)
        def fmt_int(v):
            if pd.isna(v): return ""
            return f"{int(v):,}".replace(",", ".")
            
        def fmt_float(v):
            if pd.isna(v): return ""
            return f"{float(v):,.1f}".replace(".", ",").replace(",", ".", 1) if float(v) >= 1000 else f"{float(v):.1f}".replace(".", ",")

        cols_ordem = ["Semana", "Peças", "Minutos", "Horas", "Min/Peça", "Tendência MA3"]
        df_view = tbl[cols_ordem].copy()
        
        df_view["Peças"] = df_view["Peças"].apply(fmt_int)
        df_view["Minutos"] = df_view["Minutos"].apply(fmt_int)
        df_view["Tendência MA3"] = df_view["Tendência MA3"].apply(fmt_int)
        df_view["Horas"] = df_view["Horas"].apply(fmt_float)
        df_view["Min/Peça"] = df_view["Min/Peça"].apply(fmt_float)
        
        # Cria Tabela Moderna no Plotly
        fig_tbl = go.Figure(data=[go.Table(
            header=dict(
                values=[f"<b>{c}</b>" for c in df_view.columns],
                fill_color=WIRE_HI,
                font=dict(color=TEXT_HI, size=11, family="DM Mono"),
                align="center",
                line_color=WIRE,
                height=32
            ),
            cells=dict(
                values=[df_view[k].tolist() for k in df_view.columns],
                fill_color="#0B1017",
                font=dict(color=TEXT_MID, size=12, family="Syne"),
                align="center",
                line_color=WIRE,
                height=30
            )
        )])
        
        l_tbl = plotly_base("resumo semanal de performance", 380)
        fig_tbl.update_layout(**l_tbl)
        chart_wrap(fig_tbl)
    else:
        st.info("Nenhum dado semanal disponível.")

# ── Download dos dados filtrados ──────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

col_dl, col_info = st.columns([1, 3])
with col_dl:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados Filtrados")
        if not sem_df.empty:
            tbl.to_excel(writer, index=False, sheet_name="Resumo Semanal")
    st.download_button(
        label="⬇ Exportar dados filtrados",
        data=buf.getvalue(),
        file_name="envios_filtrado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
with col_info:
    st.markdown(
        f"""<p style="font-family:'DM Mono',monospace;font-size:0.72rem;
                     color:#3D566E;margin-top:0.6rem">
            {n_sel:,} ordens filtradas · {n_total:,} totais
        </p>""",
        unsafe_allow_html=True,
    )
