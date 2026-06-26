"""
Service: processamento do Arquivo 1 — Planilha de Acompanhamento.

Responsabilidades:
  - Filtrar SITUAÇÃO = "Costura"
  - Gerar ACOMPANHAMENTO.xlsx  (colunas base)
  - Gerar STATUS.xlsx           (linhas onde RECEBIMENTO é texto)
  - Gerar PREVISAO.xlsx         (linhas onde PREVISÃO RECEBIMENTO é data)
"""

from __future__ import annotations

import datetime
import pandas as pd
from typing import Optional

from core.config import SITUACAO_COSTURA
from core.utils import resolve_column, is_date_value, is_text_value


FIELDS = [
    "ORDEM MESTRE",
    "OFICINA",
    "ENVIO",
    "QTD",
    "MINUTOS",
    "DEAD LINE",
    "SITUAÇÃO",
    "RECEBIMENTO",
    "MP",
    "PREVISÃO RECEBIMENTO",
]


def _build_col_map(df: pd.DataFrame) -> dict[str, Optional[str]]:
    return {f: resolve_column(df, f) for f in FIELDS}


def _validate(col_map: dict) -> list[str]:
    required = ["ORDEM MESTRE", "OFICINA", "SITUAÇÃO"]
    return [k for k in required if col_map[k] is None]


def _is_real_date(value) -> bool:
    """
    True se o valor é uma data válida — tanto Timestamp nativo do Excel
    quanto string que representa data.
    NaT, None, vazio, strings de texto → False.
    """
    # Tipo nativo (Excel lido sem dtype=str)
    if isinstance(value, pd.Timestamp):
        return not pd.isnull(value)
    if isinstance(value, (datetime.datetime, datetime.date)):
        return True
    # Fallback string (ex: arquivo CSV ou célula formatada como texto)
    if not isinstance(value, str):
        return False
    s = value.strip()
    if s.lower() in ("", "nan", "nat", "none"):
        return False
    try:
        result = pd.to_datetime(s, dayfirst=True, errors="coerce")
        return result is not pd.NaT and not pd.isnull(result)
    except Exception:
        return False


def _is_real_text(value) -> bool:
    """
    True se o valor é string não-vazia e não interpretável como data.
    Valores como 'Coletando datas', 'Agua. Reposição' retornam True.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    if isinstance(value, (pd.Timestamp, datetime.datetime, datetime.date)):
        return False  # é data, não texto
    s = str(value).strip()
    if s.lower() in ("", "nan", "nat", "none"):
        return False
    # Tenta parsear como data; se conseguir, não é texto
    try:
        r = pd.to_datetime(s, dayfirst=True, errors="coerce")
        if r is not pd.NaT and not pd.isnull(r):
            return False
    except Exception:
        pass
    return True


def _fmt_recebimento(val) -> str:
    """Formata célula mista de RECEBIMENTO: data → DD/MM/YYYY, texto → texto, vazio → ''."""
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    if isinstance(val, (pd.Timestamp, datetime.datetime, datetime.date)):
        if isinstance(val, pd.Timestamp) and pd.isnull(val):
            return ""
        return val.strftime("%d/%m/%Y")
    s = str(val).strip()
    if s.lower() in ("", "nan", "nat", "none"):
        return ""
    try:
        r = pd.to_datetime(s, dayfirst=True, errors="coerce")
        if r is not pd.NaT and not pd.isnull(r):
            return r.strftime("%d/%m/%Y")
    except Exception:
        pass
    return s


def _format_dates_ptbr(df: pd.DataFrame, date_cols: list[str]) -> pd.DataFrame:
    """
    Converte colunas de data para string no formato DD/MM/YYYY (pt-BR).
    Aceita Timestamp, datetime ou string parseável.
    Deixa NaT / vazios como string vazia.
    """
    for col in date_cols:
        if col not in df.columns:
            continue
        parsed = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
        df[col] = parsed.apply(
            lambda v: v.strftime("%d/%m/%Y") if not pd.isnull(v) else ""
        )
    return df


def process_acompanhamento(df_raw: pd.DataFrame) -> dict[str, pd.DataFrame | list[str]]:
    """
    Processa o DataFrame bruto do Arquivo 1.

    Retorna:
      - 'acompanhamento': DataFrame → ACOMPANHAMENTO.xlsx
      - 'status':         DataFrame → STATUS.xlsx
      - 'previsao':       DataFrame → PREVISAO.xlsx
      - 'warnings':       lista de avisos
    """
    col_map = _build_col_map(df_raw)
    missing = _validate(col_map)
    if missing:
        raise ValueError(f"Colunas obrigatórias não encontradas: {missing}")

    warnings: list[str] = []
    for key, real in col_map.items():
        if real is None:
            warnings.append(f"Coluna '{key}' não encontrada — será ignorada.")

    # ── 1. Filtro SITUAÇÃO = Costura ──────────────────────────────────────────
    sit_col = col_map["SITUAÇÃO"]
    mask_costura = df_raw[sit_col].fillna("").astype(str).str.strip().isin(SITUACAO_COSTURA)
    df = df_raw[mask_costura].copy().reset_index(drop=True)

    rec_col  = col_map.get("RECEBIMENTO")
    prev_col = col_map.get("PREVISÃO RECEBIMENTO")

    # ── 2. Máscaras calculadas sobre valores RAW (antes de qualquer conversão) ──
    #
    # RECEBIMENTO: coluna mista — pode ter Timestamp (data nativa) OU string (texto)
    # Regra: se é Timestamp válido → data; se é string não-data → texto (STATUS)
    #
    # PREVISÃO RECEBIMENTO: coluna com TODOS os valores sendo datas (Timestamp)
    # Regra: pegar tudo que é data válida (inclui Timestamps e strings de data)

    if rec_col and rec_col in df.columns:
        mask_status = df[rec_col].apply(_is_real_text)
    else:
        mask_status = pd.Series(False, index=df.index)
        warnings.append("Coluna RECEBIMENTO não encontrada; STATUS.xlsx ficará vazio.")

    if rec_col and rec_col in df.columns:
        mask_previsao = df[rec_col].apply(_is_real_date)
    else:
        mask_previsao = pd.Series(False, index=df.index)
        warnings.append("Coluna RECEBIMENTO não encontrada; PREVISAO.xlsx ficará vazio.")

    # ── 3. Helper de seleção + renomeio ───────────────────────────────────────
    def _select(fields: list[str], source: pd.DataFrame) -> pd.DataFrame:
        cols  = [col_map[f] for f in fields if col_map.get(f) is not None]
        avail = [c for c in cols if c in source.columns]
        sub   = source[avail].copy()
        sub.rename(
            columns={col_map[f]: f for f in fields
                     if col_map.get(f) is not None and col_map[f] in avail},
            inplace=True,
        )
        return sub

    DATE_COLS = ["ENVIO", "DEAD LINE", "RECEBIMENTO"]

    # ── 4. ACOMPANHAMENTO ─────────────────────────────────────────────────────
    df_acomp = _select(
        ["ORDEM MESTRE", "OFICINA", "ENVIO", "QTD", "MINUTOS", "DEAD LINE", "MP"],
        df,
    )
    _format_dates_ptbr(df_acomp, [c for c in DATE_COLS if c in df_acomp.columns])

    # ── 5. STATUS — RECEBIMENTO é texto ───────────────────────────────────────
    df_status = _select(
        ["ORDEM MESTRE", "OFICINA", "ENVIO", "QTD", "MINUTOS",
         "DEAD LINE", "SITUAÇÃO", "MP", "RECEBIMENTO"],
        df.loc[mask_status],
    )
    # RECEBIMENTO no STATUS é texto puro — não passa pelo formatador de datas
    _format_dates_ptbr(df_status, [c for c in DATE_COLS if c in df_status.columns and c != "RECEBIMENTO"])
    # RECEBIMENTO já é string; garante limpeza
    if "RECEBIMENTO" in df_status.columns:
        df_status["RECEBIMENTO"] = df_status["RECEBIMENTO"].astype(str).str.strip()

    # ── 6. PREVISAO — PREVISÃO RECEBIMENTO é data válida ─────────────────────
    df_prev = _select(
        ["ORDEM MESTRE", "OFICINA", "ENVIO", "QTD", "MINUTOS",
         "DEAD LINE", "SITUAÇÃO", "MP", "RECEBIMENTO"],
        df.loc[mask_previsao],
    )
    _format_dates_ptbr(df_prev, [c for c in DATE_COLS if c in df_prev.columns])

    # ── 7. POLO COSTURA — SITUAÇÃO = Costura AND MP = Polo ────────────────────
    mp_col = col_map.get("MP")
    if mp_col and mp_col in df.columns:
        mask_polo = df[mp_col].fillna("").astype(str).str.strip().str.lower() == "polo"
    else:
        mask_polo = pd.Series(False, index=df.index)
        warnings.append("Coluna MP não encontrada; POLO_COSTURA ficará vazio.")

    df_polo = _select(
        ["RECEBIMENTO", "ENVIO", "DEAD LINE", "MP", "OFICINA", "SITUAÇÃO", "QTD", "MINUTOS"],
        df.loc[mask_polo],
    )
    _format_dates_ptbr(df_polo, [c for c in ["ENVIO", "DEAD LINE"] if c in df_polo.columns])

    # RECEBIMENTO é misto (data OU texto) — preserva texto, formata datas
    if "RECEBIMENTO" in df_polo.columns:
        df_polo["RECEBIMENTO"] = df_polo["RECEBIMENTO"].apply(_fmt_recebimento)

    df_polo.rename(columns={"MINUTOS": "MIN"}, inplace=True)

    return {
        "acompanhamento": df_acomp,
        "status":         df_status,
        "previsao":       df_prev,
        "polo_costura":   df_polo,
        "warnings":       warnings,
    }
