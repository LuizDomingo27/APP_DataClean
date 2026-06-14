# ⚙ Tratador de Dados · Oficina

Aplicação **Streamlit** para tratamento automático de planilhas de produção.

## 📦 Estrutura do Projeto

```
data_processor/
├── app.py                        ← Entrypoint principal
├── requirements.txt
├── output/                       ← Arquivos gerados (criado automaticamente)
├── core/
│   ├── config.py                 ← Constantes, aliases de colunas, paths
│   └── utils.py                  ← Funções utilitárias (resolver colunas, ler arquivos)
├── services/
│   ├── acompanhamento_service.py ← Lógica do Arquivo 1
│   ├── recebimento_service.py    ← Lógica do Arquivo 2
│   ├── estoque_service.py        ← Lógica do Arquivo 3
│   └── export_service.py         ← Serialização para .xlsx com formatação
└── ui/
    ├── components.py             ← Widgets reutilizáveis do Streamlit
    └── styles.py                 ← CSS injetado (tema dark cyan/navy)
```

## 🚀 Como Executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar o app
streamlit run app.py
```

O app abrirá automaticamente em `http://localhost:8501`.

## 📁 Arquivos de Entrada

| # | Arquivo | Colunas Obrigatórias |
|---|---------|---------------------|
| 1 | Acompanhamento | `SITUAÇÃO`, `ORDEM MESTRE`, `OFICINA`, `ENVIO`, `QTD`, `MINUTOS`, `DEAD LINE`, `MP`, `RECEBIMENTO`, `PREVISÃO RECEBIMENTO` |
| 2 | Recebimento | `DIA`, `OFICINA`, `ORDEM MESTRE`, `MP`, `REAL CORTADO` (ou `QTD`), `MINUTOS` |
| 3 | Estoque | `OFICINA`, `POSTOS` (ou `COLABORADORES`), `Cap Peças 65%` |

Formatos aceitos: `.xlsx` e `.csv`

## 📤 Arquivos Gerados (pasta `output/`)

| Arquivo | Conteúdo |
|---------|----------|
| `ACOMPANHAMENTO.xlsx` | Linhas com SITUAÇÃO = Costura; colunas base |
| `STATUS.xlsx` | Linhas onde RECEBIMENTO é texto (status, não data) |
| `PREVISAO.xlsx` | Linhas com PREVISÃO RECEBIMENTO preenchida como data |
| `RECEBIMENTO.xlsx` | Arquivo 2 com colunas selecionadas |
| `ESTOQUE.xlsx` | Arquivo 3 + coluna calculada `CAP PEÇAS SEMANAL` |

## 🔧 Regras de Negócio

- **Filtro Costura**: somente linhas com `SITUAÇÃO` igual a `Costura`, `COSTURA` ou `costura`
- **STATUS**: linhas onde `RECEBIMENTO` contém texto (ex: "EM PRODUÇÃO", "AGUARDANDO")
- **PREVISAO**: linhas onde `PREVISÃO RECEBIMENTO` é uma data válida (não nulo)
- **ESTOQUE**: `CAP PEÇAS SEMANAL = CAP PEÇAS 65% × 5`
- **Aliases**: colunas com nomes variantes são reconhecidas automaticamente (ex: `Min`, `MIN`, `MINUTOS`)
