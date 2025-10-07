import os
import shutil

base_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(base_dir, "..", "..", "spreadsheets")
output_folder = os.path.join(base_dir, "..", "..", "files", "raw")

os.makedirs(output_folder, exist_ok=True)

print("Iniciando extração")

files_map = {
    "df_empresas.csv": "empresas.csv",
    "empresas_bolsa.csv": "bolsa_empresas.csv",
    "cotacoes_bolsa.csv": "bolsa_cotacoes.csv",
    "empresas_nivel_atividade.csv": "empresas_nivel_atividade.csv",
    "empresas_porte.csv": "empresas_porte.csv",
    "empresas_saude_tributaria.csv": "empresas_saude_tributaria.csv",
    "empresas_simples.csv": "empresas_simples.csv"
}

for src_file, dst_file in files_map.items():
    src_path = os.path.join(input_folder, src_file)
    dst_path = os.path.join(output_folder, dst_file)

    try:
        shutil.copy(src_path, dst_path)
        print(f"{src_file} exportado para {dst_path}")
    except Exception as e:
        print(f"Erro ao processar {src_file}: {e}")

print("Concluído")
