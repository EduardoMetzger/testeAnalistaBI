import os
import pandas as pd

base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "..", "..", "files", "raw", "bolsa_empresas.csv")
output_folder = os.path.join(base_dir, "..", "..", "files", "clean")
output_path = os.path.join(output_folder, "bolsa_empresas.csv")

os.makedirs(output_folder, exist_ok=True)

print("Iniciando clean_bolsa_empresa")

try:
    df = pd.read_csv(input_path, sep=";", encoding="utf-8", low_memory=False)

    rename_map = {
        "id": "empresa_bolsa_id",
        "cd_acao_rdz": "empresa_bolsa_codigo_acao_reduzido",
        "nm_empresa": "empresa_bolsa_nome_empresa",
        "setor_economico": "empresa_bolsa_setor_economico",
        "subsetor": "empresa_bolsa_subsetor",
        "segmento": "empresa_bolsa_subsegmento",
        "segmento_b3": "empresa_bolsa_segmento_b3",
        "nm_segmento_b3": "empresa_bolsa_nome_segmento_b3",
        "cd_acao": "empresa_bolsa_codigo_acao",
        "tx_cnpj": "empresa_bolsa_cnpj_texto",
        "vl_cnpj": "empresa_bolsa_cnpj_numerico"
    }

    excluir = ["created_at", "updated_at"]
    df.drop(columns=[c for c in excluir if c in df.columns], inplace=True, errors="ignore")
    df.rename(columns=rename_map, inplace=True)

    if "empresa_bolsa_id" in df.columns:
        df["empresa_bolsa_id"] = pd.to_numeric(df["empresa_bolsa_id"], errors="coerce").astype("Int64")

    if "empresa_bolsa_cnpj_numerico" in df.columns:
        df["empresa_bolsa_cnpj_numerico"] = pd.to_numeric(df["empresa_bolsa_cnpj_numerico"], errors="coerce").astype("Int64")

    if "empresa_bolsa_cnpj_texto" in df.columns:
        df["empresa_bolsa_cnpj_texto"] = df["empresa_bolsa_cnpj_texto"].astype(str).str.zfill(14)

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    print(f"Arquivo salvo em {output_path}")
    print(f"Total de registros: {len(df)}")

except Exception as e:
    print("Erro ao processar empresa_bolsa:", e)

print("Concluído")
