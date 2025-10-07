import os
import pandas as pd

base_dir = os.path.dirname(__file__)
base_files = os.path.join(base_dir, "..", "..", "files")
clean_dir = os.path.join(base_files, "clean")
raw_dir = os.path.join(base_files, "raw")
enrich_dir = os.path.join(base_files, "enrich")

os.makedirs(enrich_dir, exist_ok=True)

empresas_path = os.path.join(clean_dir, "empresas.csv")
nivel_path = os.path.join(raw_dir, "empresas_nivel_atividade.csv")
porte_path = os.path.join(raw_dir, "empresas_porte.csv")
saude_path = os.path.join(raw_dir, "empresas_saude_tributaria.csv")
simples_path = os.path.join(raw_dir, "empresas_simples.csv")
bolsa_path = os.path.join(clean_dir, "bolsa_empresas.csv")
output_path = os.path.join(enrich_dir, "d_empresas.csv")

print("Iniciando enrich de empresas")

try:
    df = pd.read_csv(empresas_path, sep=";", encoding="utf-8", low_memory=False)
    df["empresa_cnpj_numerico"] = pd.to_numeric(df["empresa_cnpj_numerico"], errors="coerce").astype("Int64")
    print(f"Base empresas: {len(df)} registros")

    nivel = pd.read_csv(nivel_path, sep=";", encoding="utf-8", low_memory=False)
    nivel["cnpj"] = pd.to_numeric(nivel["cnpj"], errors="coerce").astype("Int64")
    df = df.merge(nivel[["cnpj", "nivel_atividade"]].drop_duplicates("cnpj"),
                  how="left", left_on="empresa_cnpj_numerico", right_on="cnpj").drop(columns="cnpj", errors="ignore")
    print(f"Merge nível de atividade ({len(nivel)} registros)")

    porte = pd.read_csv(porte_path, sep=";", encoding="utf-8", low_memory=False)
    porte["cnpj"] = pd.to_numeric(porte["cnpj"], errors="coerce").astype("Int64")
    df = df.merge(porte[["cnpj", "empresa_porte"]].drop_duplicates("cnpj"),
                  how="left", left_on="empresa_cnpj_numerico", right_on="cnpj").drop(columns="cnpj", errors="ignore")
    print(f"Merge porte de empresa ({len(porte)} registros)")

    saude = pd.read_csv(saude_path, sep=";", encoding="utf-8", low_memory=False)
    saude["cnpj"] = pd.to_numeric(saude["cnpj"], errors="coerce").astype("Int64")
    df = df.merge(saude[["cnpj", "saude_tributaria"]].drop_duplicates("cnpj"),
                  how="left", left_on="empresa_cnpj_numerico", right_on="cnpj").drop(columns="cnpj", errors="ignore")
    print(f"Merge saúde tributária ({len(saude)} registros)")

    simples = pd.read_csv(simples_path, sep=";", encoding="utf-8", low_memory=False)
    simples["cnpj"] = pd.to_numeric(simples["cnpj"], errors="coerce").astype("Int64")
    df = df.merge(simples[["cnpj", "optante_simples", "optante_simei"]].drop_duplicates("cnpj"),
                  how="left", left_on="empresa_cnpj_numerico", right_on="cnpj").drop(columns="cnpj", errors="ignore")
    print(f"Merge optantes simples/SIMEI ({len(simples)} registros)")

    bolsa = pd.read_csv(bolsa_path, sep=";", encoding="utf-8", low_memory=False)
    bolsa["empresa_bolsa_cnpj_numerico"] = pd.to_numeric(bolsa["empresa_bolsa_cnpj_numerico"], errors="coerce").astype("Int64")
    df = df.merge(bolsa, how="left",
                  left_on="empresa_cnpj_numerico",
                  right_on="empresa_bolsa_cnpj_numerico").drop(columns="empresa_bolsa_cnpj_numerico", errors="ignore")
    print(f"Merge bolsa_empresas ({len(bolsa)} registros)")

    #sinalizar sem informação
    df = df.fillna("Sem informação").replace(r"^\s*$", "Sem informação", regex=True)

    df.to_csv(output_path, sep=";", index=False, encoding="utf-8-sig")
    print(f"\nArquivo final salvo em: {output_path}")
    print(f"Total de registros: {len(df)} | Total de colunas: {len(df.columns)}")

except Exception as e:
    print("Erro ao processar enrich d_empresas:", e)

print("Concluído")
