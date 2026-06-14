"""
Utilitários para resolução e normalização de colunas.
"""

import datetime
import pandas as pd
from typing import Optional

from core.config import COLUMN_ALIASES


def resolve_column(df: pd.DataFrame, canonical_key: str) -> Optional[str]:
    """
    Retorna o nome real da coluna no DataFrame para um campo canônico.
    Busca insensível a maiúsculas/minúsculas e espaços extras.
    """
    aliases = COLUMN_ALIASES.get(canonical_key, [canonical_key])
    df_cols_norm = {c.strip().upper(): c for c in df.columns}
    for alias in aliases:
        match = df_cols_norm.get(alias.strip().upper())
        if match:
            return match
    return None


def rename_to_canonical(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    reverse = {v: k for k, v in mapping.items() if v is not None}
    return df.rename(columns=reverse)


def is_date_value(value) -> bool:
    """Retorna True se o valor é Timestamp/datetime nativo (não NaT)."""
    if isinstance(value, pd.Timestamp):
        return not pd.isnull(value)
    if isinstance(value, (datetime.datetime, datetime.date)):
        return True
    return False


def is_text_value(value) -> bool:
    """Retorna True se o valor é string não-vazia e não é 'nan'/'NaT'."""
    if pd.isna(value):
        return False
    if isinstance(value, str):
        s = value.strip().lower()
        return s not in ("", "nan", "nat", "none")
    return False


def read_file(file) -> pd.DataFrame:
    """
    Lê xlsx ou csv sem forçar dtype=str, preservando tipos nativos do Excel.

    Isso é essencial para que colunas de data do Excel cheguem como
    pd.Timestamp — permitindo detecção correta de datas vs texto nas
    colunas mistas (RECEBIMENTO, PREVISÃO RECEBIMENTO).
    """
    name = getattr(file, "name", str(file)).lower()
    if name.endswith(".csv"):
        try:
            return pd.read_csv(file, encoding="utf-8")
        except UnicodeDecodeError:
            return pd.read_csv(file, encoding="latin-1")
    else:
        # Sem dtype=str: datas nativas do Excel viram Timestamp automaticamente
        return pd.read_excel(file)
