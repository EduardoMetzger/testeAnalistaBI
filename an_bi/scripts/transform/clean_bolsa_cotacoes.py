import os
import pandas as pd

base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "..", "..", "files", "raw", "bolsa_cotacoes.csv")
output_folder = os.path.join(base_dir, "..", "..", "files", "clean")
output_path = os.path.join(output_folder, "bolsa_cotacoes.csv")

os.makedirs(output_folder, exist_ok=True)

print("Iniciando clean_bolsa_cotacoes")

try:
    df = pd.read_csv(input_path, sep=";", encoding="utf-8", low_memory=False)

    df["dt_pregao"] = pd.to_numeric(df["dt_pregao"], errors="coerce")
    df = df[(df["dt_pregao"] >= 20211001) & (df["dt_pregao"] <= 20221031)]

    rename_map = {
        "id": "cotacao_id",
        "dt_pregao": "cotacao_data",
        "cd_acao": "cotacao_codigo_acao",
        "nm_empresa_rdz": "cotacao_nome_empresa_reduzido",
        "moeda_ref": "cotacao_tipo_moeda",
        "vl_abertura": "cotacao_valor_abertura",
        "vl_maximo": "cotacao_valor_maximo",
        "vl_minimo": "cotacao_valor_minimo",
        "vl_medio": "cotacao_valor_medio",
        "vl_fechamento": "cotacao_valor_fechamento"
    }

    #limpar a base, manter somente o que for utilizado
    excluir = [
        "tp_reg", "cd_bdi", "tp_merc", "especi", "prazot",
        "vl_mlh_oft_compra", "vl_mlh_oft_venda", "vl_ttl_neg",
        "qt_tit_neg", "vl_volume", "vl_exec_opc", "in_opc",
        "dt_vnct_opc", "ft_cotacao", "vl_exec_moeda_corrente",
        "cd_isin", "cd_acao_rdz", "created_at", "updated_at",
        "__index_level_0__"
    ]

    df.drop(columns=[c for c in excluir if c in df.columns], inplace=True, errors="ignore")
    df.rename(columns=rename_map, inplace=True)

    if "cotacao_id" in df.columns:
        df["cotacao_id"] = pd.to_numeric(df["cotacao_id"], errors="coerce").astype("Int64")

    if "cotacao_data" in df.columns:
        df["cotacao_data"] = pd.to_datetime(df["cotacao_data"].astype(str), format="%Y%m%d", errors="coerce")

    num_cols = [
        "cotacao_valor_abertura", "cotacao_valor_maximo", "cotacao_valor_minimo",
        "cotacao_valor_medio", "cotacao_valor_fechamento"
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    df["ano_mes"] = df["cotacao_data"].dt.to_period("M")
    meses = df.groupby("cotacao_codigo_acao")["ano_mes"].nunique().reset_index()
    acoes_validas = meses.loc[meses["ano_mes"] >= 9, "cotacao_codigo_acao"]
    df = df[df["cotacao_codigo_acao"].isin(acoes_validas)].drop(columns=["ano_mes"])

    df["cotacao_data"] = df["cotacao_data"].dt.strftime("%d/%m/%Y")

    #trocar ponto por decimal
    for col in num_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: f"{x:.2f}".replace(".", ",") if pd.notnull(x) else "")

    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    print(f"Arquivo salvo em {output_path}")
    print(f"Total de registros: {len(df)}")

except Exception as e:
    print("Erro ao processar cotacoes_bolsa:", e)

print("Concluído")
