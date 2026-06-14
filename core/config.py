"""
Configurações e constantes da aplicação.
"""

from pathlib import Path

# ─── Diretórios ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Nomes dos arquivos de saída ──────────────────────────────────────────────
OUTPUT_FILES = {
    "acompanhamento": OUTPUT_DIR / "ACOMPANHAMENTO.xlsx",
    "status":         OUTPUT_DIR / "STATUS.xlsx",
    "previsao":       OUTPUT_DIR / "PREVISAO.xlsx",
    "recebimento":    OUTPUT_DIR / "RECEBIMENTO.xlsx",
    "estoque":        OUTPUT_DIR / "ESTOQUE.xlsx",
}

# ─── Mapeamento de colunas ────────────────────────────────────────────────────
# Aliases aceitos para cada campo canônico
COLUMN_ALIASES = {
    # Acompanhamento
    "ORDEM MESTRE":          ["ORDEM MESTRE", "ORDEM_MESTRE", "ORDEM-MESTRE"],
    "OFICINA":               ["OFICINA"],
    "ENVIO":                 ["ENVIO"],
    "QTD":                   ["QTD", "QUANTIDADE"],
    "MINUTOS":               ["MIN", "Min", "MINUTOS", "MINUTO", "Minutos"],
    "DEAD LINE":             ["DEAD LINE", "DEADLINE", "DEAD_LINE"],
    "SITUAÇÃO":              ["SITUAÇÃO", "SITUACAO", "Situação", "Situacao"],
    "RECEBIMENTO":           ["RECEBIMENTO"],
    "MP":                    ["MP"],
    "PREVISÃO RECEBIMENTO":  [
        "PREVISÃO RECEBIMENTO", "PREVISAO RECEBIMENTO",
        "PREVISÃO_RECEBIMENTO", "PREVISAO_RECEBIMENTO",
        "Previsão Recebimento", "Previsao Recebimento",
    ],
    # Recebimento (arquivo 2)
    "DIA":                   ["DIA", "Data", "DATA"],
    "ORDEM_REC":             ["ORDEM", "ORDEM MESTRE", "ORDEM-MESTRE"],
    "REAL_CORTADO":          ["REAL CORTADO", "QTD", "QUANTIDADE"],
    # Estoque (arquivo 3)
    "COLABORADORES":         [
        "Postos", "POSTOS", "COLABORADORES", "COLABORADOR",
        "Colaboradores", "Colaborador",
    ],
    "CAP_65":                ["Cap Peças 65%", "CAP PEÇAS 65%", "CAP_PECAS_65"],
}

# Valores aceitos para filtro de SITUAÇÃO
SITUACAO_COSTURA = {"costura", "COSTURA", "Costura"}
