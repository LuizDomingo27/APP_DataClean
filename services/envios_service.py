"""
Service: processamento dos Arquivos de Envios.

Regras de tratamento de nulos:
  - Colunas de texto  → "Não informado"  (exceto PDV)
  - Coluna PDV        → NaN/vazio → "NÃO_PDV"  |  valor existente (incl. "0") → preserva
  - Colunas numéricas → NaN → 0  |  valor existente → preserva
"""

from __future__ import annotations

import pandas as pd
from typing import Optional


# ─── Mapeamentos canônicos ─────────────────────────────────────────────────────

JEANS_MAP: dict[str, list[str]] = {
    "ORDEM":    ["ORDEM", "ORDEM MESTRE", "ORDEM-MESTRE", "Ordem", "Ordem Mestre"],
    "OFICINA":  ["OFICINAS", "OFICINA", "Oficinas", "Oficina"],
    "QTD":      ["SALDO OPERAÇÃO", "SALDO_OPERACAO", "SALDO OPERACAO",
                 "Saldo Operação", "Saldo Operacao", "QTD", "QUANTIDADE",
                 "Qtde", "Qtd", "QTDE", "Peças", "PEÇAS", "PECAS",
                 "SALDO", "Saldo", "PCS"],
    "MINUTOS":  ["Minutos", "MINUTOS", "MIN", "Min", "MINUTO", "Minuto"],
    "ENVIO":    ["ENVIO", "Envio", "DT ENVIO", "DATA ENVIO"],
    "MP":       ["MP"],
    "PDV":      ["PRIORIDADE", "Prioridade", "PRIORITY", "PDV", "PRIORIDADES", "Prioridades"],
    "FRETE":    ["FRETE", "Frete"],
    "SITUAÇÃO": ["SITUAÇÃO", "SITUACAO", "Situação", "Situacao"],
}

MALHA_MAP: dict[str, list[str]] = {
    "ORDEM":    ["ORDEM", "ORDEM MESTRE", "ORDEM-MESTRE", "Ordem", "Ordem Mestre"],
    "MP":       ["MP"],
    "OFICINA":  ["OFICINAS", "OFICINA", "Oficinas", "Oficina"],
    "QTD":      ["SALDO OPERAÇÃO", "SALDO_OPERACAO", "SALDO OPERACAO",
                 "Saldo Operação", "Saldo Operacao",
                 "QTD", "QUANTIDADE", "Quantidade",
                 "Qtde", "Qtd", "QTDE",
                 "Peças", "PEÇAS", "PECAS",
                 "SALDO", "Saldo", "PCS"],
    "MINUTOS":  ["Minutos", "MINUTOS", "MIN", "Min", "MINUTO", "Minuto"],
    "ENVIO":    ["ENVIO", "Envio", "DT ENVIO", "DATA ENVIO"],
    "PDV":      ["PRIORIDADE", "Prioridade", "PRIORIDADES", "Prioridades", "PDV"],
    "FRETE":    ["FRETE", "Frete"],
    "SITUAÇÃO": ["SITUAÇÃO", "SITUACAO", "Situação", "Situacao", "SIRTUAÇÃO"],
}

FINAL_COLS   = ["ORDEM", "OFICINA", "QTD", "MINUTOS", "ENVIO", "MP", "PDV", "FRETE", "SITUAÇÃO"]
NUMERIC_COLS = {"QTD", "MINUTOS"}


# ─── Utilitários ──────────────────────────────────────────────────────────────

def _resolve(df: pd.DataFrame, aliases: list[str]) -> Optional[str]:
    """Encontra o nome real da coluna pelos aliases (case-insensitive)."""
    norm = {c.strip().upper(): c for c in df.columns}
    for alias in aliases:
        found = norm.get(alias.strip().upper())
        if found:
            return found
    return None


def _diagnostico(df: pd.DataFrame, field_map: dict, nome: str) -> list[str]:
    """Avisa sobre colunas não encontradas, listando as colunas reais do arquivo."""
    nao_encontradas = [
        c for c, aliases in field_map.items()
        if _resolve(df, aliases) is None
    ]
    if not nao_encontradas:
        return []
    colunas_reais = ", ".join(f'"{c}"' for c in df.columns)
    return [
        f"[{nome}] Colunas não mapeadas: {nao_encontradas}. "
        f"Colunas reais do arquivo: {colunas_reais}"
    ]


def _select_and_rename(
    df: pd.DataFrame,
    field_map: dict[str, list[str]],
    nome: str = ""
) -> tuple[pd.DataFrame, list[str]]:
    """Seleciona e renomeia colunas. Retorna (df_renomeado, warnings)."""
    warnings = _diagnostico(df, field_map, nome)
    col_map: dict[str, str] = {}

    for canonical, aliases in field_map.items():
        real = _resolve(df, aliases)
        if real:
            col_map[canonical] = real

    avail_real = [v for v in col_map.values() if v in df.columns]
    df_out = df[avail_real].copy()
    df_out.rename(columns={v: k for k, v in col_map.items()}, inplace=True)
    return df_out, warnings


def _format_date_col(series: pd.Series) -> pd.Series:
    """Converte coluna de data para DD/MM/YYYY (pt-BR). Inválido/vazio → ''."""
    parsed = pd.to_datetime(series, errors="coerce", dayfirst=True)
    return parsed.apply(
        lambda v: v.strftime("%d/%m/%Y") if not pd.isnull(v) else ""
    )


def _fill_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preenche e normaliza valores coluna por coluna:
      - Numéricas (QTD, MINUTOS) : NaN → 0  |  valor real → preserva
      - PDV  : NaN, vazio, "0", "0.0"  → "NÃO_PDV"
      - MP   : NaN, vazio, "0", "0.0"  → "Sem MP Informada"
      - Demais texto : NaN/vazio → "Não informado"
    """
    VAZIOS = {"nan", "none", "nat", "", "0", "0.0"}

    for col in df.columns:

        if col in NUMERIC_COLS:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        elif col == "PDV":
            df[col] = df[col].fillna("NÃO_PDV").astype(str).str.strip()
            df.loc[df[col].str.lower().isin(VAZIOS), col] = "NÃO_PDV"

        elif col == "MP":
            df[col] = df[col].fillna("Sem MP Informada").astype(str).str.strip()
            df.loc[df[col].str.lower().isin(VAZIOS), col] = "Sem MP Informada"

        else:
            df[col] = df[col].fillna("Não informado").astype(str).str.strip()
            sem_zero = VAZIOS - {"0", "0.0"}
            df.loc[df[col].str.lower().isin(sem_zero), col] = "Não informado"

    return df


def _ensure_cols(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Garante que todas as colunas finais existam."""
    for col in cols:
        if col not in df.columns:
            df[col] = 0 if col in NUMERIC_COLS else ""
    return df[cols]


# ─── Processamento público ────────────────────────────────────────────────────

def process_envios_jeans(df_raw: pd.DataFrame) -> dict:
    df, warnings = _select_and_rename(df_raw, JEANS_MAP, "Envios Jeans")

    if "ENVIO" in df.columns:
        df["ENVIO"] = _format_date_col(df["ENVIO"])

    df = _ensure_cols(df, FINAL_COLS)
    df = _fill_nulls(df)

    df.insert(0, "ORIGEM", "JEANS")
    return {"envios_jeans": df, "warnings": warnings}


def process_envios_malha(df_raw: pd.DataFrame) -> dict:
    df, warnings = _select_and_rename(df_raw, MALHA_MAP, "Envios Malha")

    if "ENVIO" in df.columns:
        df["ENVIO"] = _format_date_col(df["ENVIO"])

    df = _ensure_cols(df, FINAL_COLS)
    df = _fill_nulls(df)

    df.insert(0, "ORIGEM", "MALHA")
    return {"envios_malha": df, "warnings": warnings}


def merge_envios(df_jeans: pd.DataFrame, df_malha: pd.DataFrame) -> pd.DataFrame:
    df = pd.concat([df_jeans, df_malha], ignore_index=True)

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    for col in df.columns:
        if col not in NUMERIC_COLS:
            df[col] = df[col].fillna("").astype(str).str.strip()

    if "PDV" in df.columns:
        mask = df["PDV"].str.lower().isin(["", "nan", "none"])
        df.loc[mask, "PDV"] = "NÃO_PDV"

    return df
