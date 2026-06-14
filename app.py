"""
Tratador de Dados — Oficina
Entrypoint: streamlit run app.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import io, zipfile
import streamlit as st
import pandas as pd

from core.config   import OUTPUT_DIR
from core.utils    import read_file
from services.acompanhamento_service import process_acompanhamento
from services.recebimento_service    import process_recebimento
from services.estoque_service        import process_estoque
from services.envios_service         import process_envios_jeans, process_envios_malha, merge_envios
from services.export_service         import df_to_excel_bytes, save_all
from ui.styles     import STYLES
from ui.components import preview_table, download_button_card

st.set_page_config(
    page_title="DataWrangling · Oficina",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(STYLES, unsafe_allow_html=True)
#st.markdown("""
#<style>
#section[data-testid="stSidebar"],
#button[data-testid="collapsedControl"] { display: none !important; }
#</style>""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <h1>Data-Wrangling&nbsp;<span class="neon-cyan">·</span>&nbsp;<span class="neon-violet">Oficina</span></h1>
    <p>// carregue os arquivos · processe · faça o download</p>
    <div class="header-rule"></div>
</div>
""", unsafe_allow_html=True)

# ── Sessão ────────────────────────────────────────────────────────────────────
if "results"      not in st.session_state: st.session_state["results"]      = None
if "all_warnings" not in st.session_state: st.session_state["all_warnings"] = []


# ═══════════════════════════════════════════════════════════════════════════════
#  UPLOADS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="section-label">Arquivos de entrada</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(
        '<div class="upload-card"><div class="card-header">'
        '<span class="card-icon">📋</span>'
        '<span class="card-title">Acompanhamento</span></div>'
        '<p class="card-desc">situação · dead line · recebimento · previsão</p></div>',
        unsafe_allow_html=True)
    file_acomp = st.file_uploader("Acompanhamento", type=["xlsx","csv"],
                                   key="f_acomp", label_visibility="collapsed")

with c2:
    st.markdown(
        '<div class="upload-card"><div class="card-header">'
        '<span class="card-icon">📦</span>'
        '<span class="card-title">Recebimento</span></div>'
        '<p class="card-desc">dia · oficina · ordem · qtd · min</p></div>',
        unsafe_allow_html=True)
    file_receb = st.file_uploader("Recebimento", type=["xlsx","csv"],
                                   key="f_receb", label_visibility="collapsed")

with c3:
    st.markdown(
        '<div class="upload-card"><div class="card-header">'
        '<span class="card-icon">🏭</span>'
        '<span class="card-title">Estoque</span></div>'
        '<p class="card-desc">oficina · postos · cap peças 65%</p></div>',
        unsafe_allow_html=True)
    file_estoque = st.file_uploader("Estoque", type=["xlsx","csv"],
                                     key="f_estoque", label_visibility="collapsed")

st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

c4, c5, c6 = st.columns([1, 1, 1], gap="medium")

with c4:
    st.markdown(
        '<div class="upload-card upload-card--violet"><div class="card-header">'
        '<span class="card-icon">👖</span>'
        '<span class="card-title">Envios — Jeans</span></div>'
        '<p class="card-desc">ordem · saldo operação · prioridade · frete</p></div>',
        unsafe_allow_html=True)
    file_jeans = st.file_uploader("Envios Jeans", type=["xlsx","csv"],
                                   key="f_jeans", label_visibility="collapsed")

with c5:
    st.markdown(
        '<div class="upload-card upload-card--violet"><div class="card-header">'
        '<span class="card-icon">🧵</span>'
        '<span class="card-title">Envios — Malha</span></div>'
        '<p class="card-desc">ordem · oficinas · saldo operação · prioridade · frete</p></div>',
        unsafe_allow_html=True)
    file_malha = st.file_uploader("Envios Malha", type=["xlsx","csv"],
                                   key="f_malha", label_visibility="collapsed")

with c6:
    st.markdown("""
    <div style="display:flex;align-items:flex-end;height:100%;padding-bottom:0.5rem">
        <div class="merge-box">
            <p>👖 + 🧵<br>
            <span class="accent">→ ENVIOS_OFICINAS.xlsx</span><br>
            merge automático</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Status chips ──────────────────────────────────────────────────────────────
FILES_META = [
    ("📋", "Acompanhamento", file_acomp),
    ("📦", "Recebimento",    file_receb),
    ("🏭", "Estoque",        file_estoque),
    ("👖", "Envios Jeans",   file_jeans),
    ("🧵", "Envios Malha",   file_malha),
]
chip_cols = st.columns(5, gap="small")
for idx, (icon, nome, arq) in enumerate(FILES_META):
    with chip_cols[idx]:
        if arq:
            label = arq.name[:18] + ("…" if len(arq.name) > 18 else "")
            st.markdown(
                f'<div class="file-chip file-chip--ok">'
                f'{icon} {nome}<br>'
                f'<span style="font-size:0.65rem;opacity:0.65">{label}</span>'
                f'</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="file-chip file-chip--wait">'
                f'{icon} {nome}<br>'
                f'<span style="font-size:0.65rem">aguardando…</span>'
                f'</div>', unsafe_allow_html=True)

st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)

# ── Botão ─────────────────────────────────────────────────────────────────────
all_core = all([file_acomp, file_receb, file_estoque])
uploaded = sum(1 for _, _, f in FILES_META if f)

_, bc, _ = st.columns([1.2, 1.6, 1.2])
with bc:
    run_btn = st.button(
        f"[ PROCESSAR  {uploaded}/5 ARQUIVOS ]",
        use_container_width=True,
        disabled=not all_core,
        type="primary",
    )
    if not all_core:
        st.markdown(
            '<p style="text-align:center;font-family:\'DM Mono\',monospace;'
            'font-size:0.65rem;color:#3D566E;margin-top:0.4rem;letter-spacing:0.06em">'
            '// arquivos 1-3 obrigatórios</p>',
            unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PROCESSAMENTO
# ═══════════════════════════════════════════════════════════════════════════════
if run_btn and all_core:
    all_warnings, results = [], {}
    with st.spinner("processando…"):
        try:
            r1 = process_acompanhamento(read_file(file_acomp))
            results["ACOMPANHAMENTO"] = r1["acompanhamento"]
            results["STATUS"]         = r1["status"]
            results["PREVISAO"]       = r1["previsao"]
            all_warnings.extend(r1["warnings"])

            r2 = process_recebimento(read_file(file_receb))
            results["RECEBIMENTO"] = r2["recebimento"]
            all_warnings.extend(r2["warnings"])

            r3 = process_estoque(read_file(file_estoque))
            results["ESTOQUE"] = r3["estoque"]
            all_warnings.extend(r3["warnings"])

            if file_jeans and file_malha:
                r4 = process_envios_jeans(read_file(file_jeans))
                r5 = process_envios_malha(read_file(file_malha))
                all_warnings.extend(r4["warnings"] + r5["warnings"])
                results["ENVIOS_OFICINAS"] = merge_envios(r4["envios_jeans"], r5["envios_malha"])
            elif file_jeans:
                r4 = process_envios_jeans(read_file(file_jeans))
                results["ENVIOS_OFICINAS"] = r4["envios_jeans"]
                all_warnings.extend(r4["warnings"])
            elif file_malha:
                r5 = process_envios_malha(read_file(file_malha))
                results["ENVIOS_OFICINAS"] = r5["envios_malha"]
                all_warnings.extend(r5["warnings"])

            save_all(results, OUTPUT_DIR)
            st.session_state["results"]      = results
            st.session_state["all_warnings"] = all_warnings

        except Exception as exc:
            st.error(f"erro: {exc}")
            st.exception(exc)


# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTADOS
# ═══════════════════════════════════════════════════════════════════════════════
results      = st.session_state.get("results")
all_warnings = st.session_state.get("all_warnings", [])

if results:
    if all_warnings:
        with st.expander(f"⚠  {len(all_warnings)} aviso(s)", expanded=False):
            for w in all_warnings:
                st.warning(w)

    st.markdown('<p class="section-label" style="margin-top:1.5rem">resumo</p>',
                unsafe_allow_html=True)

    METRIC_META = {
        "ACOMPANHAMENTO":  "📋 Acompanhamento",
        "STATUS":          "🔴 Status",
        "PREVISAO":        "📅 Previsão",
        "RECEBIMENTO":     "📦 Recebimento",
        "ESTOQUE":         "🏭 Estoque",
        "ENVIOS_OFICINAS": "🚚 Envios Oficinas",
    }
    mc = st.columns(len(results), gap="small")
    for idx, (key, df_r) in enumerate(results.items()):
        label = METRIC_META.get(key, key)
        rows  = len(df_r) if df_r is not None and not df_r.empty else 0
        ncols = len(df_r.columns) if df_r is not None and not df_r.empty else 0
        with mc[idx]:
            st.metric(label=label, value=f"{rows:,}", delta=f"{ncols} cols")

    st.markdown("<hr>", unsafe_allow_html=True)

    TAB_META = {
        "ACOMPANHAMENTO":  "📋 Acompanhamento",
        "STATUS":          "🔴 Status",
        "PREVISAO":        "📅 Previsão",
        "RECEBIMENTO":     "📦 Recebimento",
        "ESTOQUE":         "🏭 Estoque",
        "ENVIOS_OFICINAS": "🚚 Envios Oficinas",
    }
    tab_keys   = [k for k in TAB_META if k in results]
    tab_labels = [TAB_META[k] for k in tab_keys]
    tabs = st.tabs(tab_labels)

    for tab, key in zip(tabs, tab_keys):
        with tab:
            df_tab = results.get(key)
            if df_tab is None or df_tab.empty:
                st.info(f"sem dados para {key}")
                continue
            cp, cd = st.columns([3, 1], gap="medium")
            with cp:
                preview_table(df_tab, key)
            with cd:
                st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
                download_button_card(
                    label=f"{key}.xlsx",
                    data=df_to_excel_bytes(df_tab, sheet_name=key[:31]),
                    file_name=f"{key}.xlsx",
                )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="section-label">download em lote</p>', unsafe_allow_html=True)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, df_z in results.items():
            if df_z is not None and not df_z.empty:
                zf.writestr(f"{name}.xlsx", df_to_excel_bytes(df_z, sheet_name=name[:31]))
    buf.seek(0)

    _, bz, _ = st.columns([1, 1.6, 1])
    with bz:
        st.download_button(
            label="⬇  baixar todos os arquivos  [ .zip ]",
            data=buf.getvalue(),
            file_name="tratamento_dados_oficina.zip",
            mime="application/zip",
            use_container_width=True,
            type="primary",
        )

else:
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    with st.expander("// como usar", expanded=True):
        st.markdown("""
| # | Arquivo | Colunas principais | Gera |
|---|---------|-------------------|------|
| 1 | **Acompanhamento** | SITUAÇÃO, ORDEM MESTRE, OFICINA, ENVIO, QTD, MIN, DEAD LINE, MP, RECEBIMENTO, PREVISÃO RECEBIMENTO | ACOMPANHAMENTO · STATUS · PREVISAO |
| 2 | **Recebimento** | DIA, OFICINA, ORDEM, MP, QTD, MIN | RECEBIMENTO |
| 3 | **Estoque** | OFICINA, POSTOS, Cap Peças 65% | ESTOQUE |
| 4 | **Envios Jeans** *(opcional)* | ORDEM, SALDO OPERAÇÃO → QTD, PRIORIDADE → PDV, FRETE | — |
| 5 | **Envios Malha** *(opcional)* | ORDEM, OFICINAS, SALDO OPERAÇÃO → QTD, PRIORIDADE → PDV | — |

> Arquivos 4+5 juntos → **ENVIOS_OFICINAS.xlsx**
> Nulos: numérico → `0` · PDV nulo ou zero → `NÃO_PDV` · MP nulo ou zero → `Sem MP Informada` · texto → `Não informado`
        """)
