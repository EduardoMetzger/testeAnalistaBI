import os
import shutil

base_dir = os.path.dirname(__file__)
input_folder = os.path.join(base_dir, "..", "..", "files", "raw")
output_folder = os.path.join(base_dir, "..", "..", "files", "clean")

os.makedirs(output_folder, exist_ok=True)

print("Iniciando extração")

#arquivos que não vão sofrer alteração, apenas para organização do ambiente e centralização no clean
files_map = {
    "empresas_nivel_atividade.csv": "empresas_nivel_atividade.csv",
    "empresas_porte.csv": "empresas_porte.csv",
    "empresas_saude_tributaria.csv": "empresas_saude_tributaria.csv",
    "empresas_simples.csv": "empresas_simples.csv"
}

for src, dst in files_map.items():
    src_path = os.path.join(input_folder, src)
    dst_path = os.path.join(output_folder, dst)

    try:
        shutil.copy(src_path, dst_path)
        print(f"{src} copiado para {dst_path}")
    except Exception as e:
        print(f"Erro ao copiar {src}: {e}")

print("Concluído")
