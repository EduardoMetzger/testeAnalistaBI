import os
import pandas as pd

base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "..", "..", "files", "raw", "empresas.csv")
output_folder = os.path.join(base_dir, "..", "..", "files", "clean")
output_path = os.path.join(output_folder, "empresas.csv")

os.makedirs(output_folder, exist_ok=True)

print("Iniciando clean_empresas")

try:
    df = pd.read_csv(input_path, sep=";", encoding="utf-8", low_memory=False)

    rename_map = {
        "cnpj": "empresa_cnpj_numerico",
        "dt_abertura": "empresa_data_abertura",
        "matriz.empresaMatriz": "empresa_sinalizador_matriz",
        "cd_cnae_principal": "empresa_cnae_principal_codigo",
        "de_cnae_principal": "empresa_cnae_principal_descricao",
        "de_ramo_atividade": "empresa_ramo_atividade_descricao",
        "de_setor": "empresa_setor_descricao",
        "endereco_cep": "empresa_cep_numerico",
        "endereco_municipio": "empresa_municipio",
        "endereco_uf": "empresa_uf",
        "endereco_regiao": "empresa_regiao",
        "endereco_mesorregiao": "empresa_mesorregiao",
        "situacao_cadastral": "empresa_situacao_cadastral"
    }

    df.rename(columns=rename_map, inplace=True)

    if "empresa_cnpj_numerico" in df.columns:
        df["empresa_cnpj_numerico"] = pd.to_numeric(df["empresa_cnpj_numerico"], errors="coerce").astype("Int64")

    if "empresa_cep_numerico" in df.columns:
        df["empresa_cep_numerico"] = pd.to_numeric(df["empresa_cep_numerico"], errors="coerce").astype("Int64")

    if "empresa_data_abertura" in df.columns:
        df["empresa_data_abertura"] = pd.to_datetime(df["empresa_data_abertura"], errors="coerce", format="%Y-%m-%d")
        df["empresa_data_abertura"] = df["empresa_data_abertura"].dt.strftime("%d/%m/%Y")

    if "empresa_sinalizador_matriz" in df.columns:
        df["empresa_sinalizador_matriz"] = df["empresa_sinalizador_matriz"].astype(str).str.lower()
        df["empresa_sinalizador_matriz"] = df["empresa_sinalizador_matriz"].replace({"true": "Sim", "false": "Não"})

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    print(f"Arquivo salvo em {output_path}")
    print(f"Total de registros: {len(df)}")

except Exception as e:
    print("Erro ao processar empresas:", e)

print("Concluído")
