"""
Service: processamento do Arquivo 2 — Planilha de Recebimento.

Responsabilidade:
  - Manter apenas: DIA, OFICINA, ORDEM MESTRE, MP, REAL CORTADO/QTD, MIN/MINUTOS
  - Gerar RECEBIMENTO.xlsx
"""

from __future__ import annotations

import pandas as pd
from typing import Optional

from core.utils import resolve_column


# Campos canônicos e aliases específicos deste arquivo
FIELDS_MAP = {
    "DIA":           ["DIA", "DATA", "Data", "data"],
    "OFICINA":       ["OFICINA", "Oficina"],
    "ORDEM MESTRE":  ["ORDEM", "ORDEM MESTRE", "ORDEM-MESTRE", "Ordem", "Ordem Mestre"],
    "MP":            ["MP"],
    "REAL CORTADO":  ["REAL CORTADO", "QTD", "QUANTIDADE", "Real Cortado"],
    "MINUTOS":       ["MIN", "Min", "MINUTOS", "Minutos", "MINUTO"],
}


def _resolve(df: pd.DataFrame, aliases: list[str]) -> Optional[str]:
    norm = {c.strip().upper(): c for c in df.columns}
    for a in aliases:
        found = norm.get(a.strip().upper())
        if found:
            return found
    return None


def process_recebimento(df_raw: pd.DataFrame) -> dict[str, pd.DataFrame | list[str]]:
    """
    Processa o DataFrame bruto do Arquivo 2.

    Retorna dict com:
      - 'recebimento': DataFrame para RECEBIMENTO.xlsx
      - 'warnings':    lista de avisos
    """
    warnings: list[str] = []
    selected_cols: dict[str, str] = {}

    for canonical, aliases in FIELDS_MAP.items():
        real = _resolve(df_raw, aliases)
        if real:
            selected_cols[canonical] = real
        else:
            warnings.append(f"Coluna '{canonical}' não encontrada no Arquivo 2.")

    if not selected_cols:
        raise ValueError("Nenhuma coluna reconhecida no Arquivo 2 (Recebimento).")

    # Seleciona e renomeia para canônico
    df_out = df_raw[[v for v in selected_cols.values()]].copy()
    df_out.rename(columns={v: k for k, v in selected_cols.items()}, inplace=True)

    # Tenta parsear data na coluna DIA
    if "DIA" in df_out.columns:
        df_out["DIA"] = pd.to_datetime(df_out["DIA"], errors="coerce", dayfirst=True)
        ano_atual = pd.Timestamp.now().year
        df_out = df_out[df_out["DIA"].dt.year == ano_atual].reset_index(drop=True)

    # Garante tipo numérico em QTD e MINUTOS
    for num_col in ("REAL CORTADO", "MINUTOS"):
        if num_col in df_out.columns:
            df_out[num_col] = pd.to_numeric(df_out[num_col], errors="coerce")

    # Formata DIA como dd/mm/yyyy
    if "DIA" in df_out.columns:
        df_out["DIA"] = df_out["DIA"].dt.strftime("%d/%m/%Y")

    # ── POLO_RECEBIMENTO — filtra MP = Polo ───────────────────────────────────
    polo_cols = [c for c in ("DIA", "OFICINA", "MP", "REAL CORTADO", "MINUTOS") if c in df_out.columns]
    if "MP" in df_out.columns:
        mask_polo = df_out["MP"].fillna("").astype(str).str.strip().str.lower() == "polo"
        df_polo = df_out.loc[mask_polo, polo_cols].copy().reset_index(drop=True)
        df_polo.rename(columns={"MINUTOS": "MIN"}, inplace=True)
    else:
        warnings.append("Coluna MP não encontrada; POLO_RECEBIMENTO ficará vazio.")
        df_polo = pd.DataFrame()

    return {"recebimento": df_out, "polo_recebimento": df_polo, "warnings": warnings}
