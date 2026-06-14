"""
Service: processamento do Arquivo 3 — Planilha de Estoque/Colaboradores.

Responsabilidade:
  - Manter: OFICINA, COLABORADORES (Postos), Cap Peças 65%
  - Calcular: Cap Peças Semanal = Cap Peças 65% * 5
  - Gerar ESTOQUE.xlsx
"""

from __future__ import annotations

import pandas as pd
from typing import Optional


FIELDS_MAP = {
    "OFICINA":           ["OFICINA", "Oficina", "oficina"],
    "COLABORADORES":     [
        "Postos", "POSTOS", "COLABORADORES", "COLABORADOR",
        "Colaboradores", "Colaborador",
    ],
    "CAP PEÇAS 65%":     [
        "Cap Peças 65%", "CAP PEÇAS 65%", "CAP_PECAS_65",
        "Cap Pecas 65%", "CAP PECAS 65%",
    ],
}


def _resolve(df: pd.DataFrame, aliases: list[str]) -> Optional[str]:
    norm = {c.strip().upper(): c for c in df.columns}
    for a in aliases:
        found = norm.get(a.strip().upper())
        if found:
            return found
    return None


def process_estoque(df_raw: pd.DataFrame) -> dict[str, pd.DataFrame | list[str]]:
    """
    Processa o DataFrame bruto do Arquivo 3.

    Retorna dict com:
      - 'estoque':  DataFrame para ESTOQUE.xlsx
      - 'warnings': lista de avisos
    """
    warnings: list[str] = []
    selected_cols: dict[str, str] = {}

    for canonical, aliases in FIELDS_MAP.items():
        real = _resolve(df_raw, aliases)
        if real:
            selected_cols[canonical] = real
        else:
            warnings.append(f"Coluna '{canonical}' não encontrada no Arquivo 3.")

    if not selected_cols:
        raise ValueError("Nenhuma coluna reconhecida no Arquivo 3 (Estoque).")

    df_out = df_raw[[v for v in selected_cols.values()]].copy()
    df_out.rename(columns={v: k for k, v in selected_cols.items()}, inplace=True)

    # Converte cap para numérico
    if "CAP PEÇAS 65%" in df_out.columns:
        df_out["CAP PEÇAS 65%"] = pd.to_numeric(df_out["CAP PEÇAS 65%"], errors="coerce")
        df_out['CAP PEÇAS 65'] = df_out['CAP PEÇAS 65%'] 
        df_out["CAP PEÇAS SEMANAL"] = df_out["CAP PEÇAS 65"] * 5
    else:
        warnings.append(
            "Cap Peças 65% não encontrada; CAP PEÇAS SEMANAL não pôde ser calculada."
        )

    if "COLABORADORES" in df_out.columns:
        df_out["COLABORADORES"] = pd.to_numeric(df_out["COLABORADORES"], errors="coerce")

    return {"estoque": df_out, "warnings": warnings}
