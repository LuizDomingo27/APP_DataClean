"""
Componentes de UI reutilizáveis para o Streamlit.
"""

import streamlit as st
import pandas as pd
from typing import Optional


def file_uploader_card(
    label: str,
    key: str,
    icon: str,
    description: str,
    file_types: list[str] | None = None,
) -> Optional[object]:
    """Renderiza um card estilizado para upload de arquivo."""
    file_types = file_types or ["xlsx", "csv"]

    with st.container():
        st.markdown(
            f"""
            <div class="upload-card">
                <div class="card-header">
                    <span class="material-symbols-outlined card-icon">{icon}</span>
                    <span class="card-title">{label}</span>
                </div>
                <p class="card-desc">{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return st.file_uploader(
            f"Selecione {label}",
            type=file_types,
            key=key,
            label_visibility="collapsed",
        )


def preview_table(df: pd.DataFrame, title: str, max_rows: int = 8):
    """Exibe prévia de uma tabela com título e contagem de linhas."""
    st.markdown(
        f'<p class="preview-title">📋 {title} <span class="row-badge">'
        f'{len(df):,} linhas</span></p>',
        unsafe_allow_html=True,
    )
    st.dataframe(df.head(max_rows), use_container_width=True)


def status_badge(text: str, kind: str = "success"):
    """Renderiza um badge colorido de status."""
    colors = {
        "success": ("#00E5FF", "#0D2137"),
        "warning": ("#FFB74D", "#1A1200"),
        "error":   ("#FF5252", "#1A0000"),
        "info":    ("#B39DDB", "#120D1A"),
    }
    fg, bg = colors.get(kind, colors["info"])
    st.markdown(
        f'<span class="status-badge" style="color:{fg};background:{bg}">{text}</span>',
        unsafe_allow_html=True,
    )


def download_button_card(
    label: str,
    data: bytes,
    file_name: str,
    icon: str = "download",
):
    """Botão de download estilizado."""
    st.download_button(
        label=f"⬇ {label}",
        data=data,
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
