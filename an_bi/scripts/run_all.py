import os
import subprocess
import sys

base_dir = os.path.dirname(__file__)

scripts = [
    os.path.join(base_dir, "extract", "extract_raw.py"),
    os.path.join(base_dir, "transform", "clean_bolsa_cotacoes.py"),
    os.path.join(base_dir, "transform", "clean_bolsa_empresas.py"),
    os.path.join(base_dir, "transform", "clean_empresas.py"),
    os.path.join(base_dir, "transform", "keep_raw.py"),
    os.path.join(base_dir, "load", "enrich_d_empresas.py"),
    os.path.join(base_dir, "load", "enrich_f_cotacoes.py")
]

print("Iniciando execução do pipeline\n")

for path in scripts:
    print(f"Executando: {path}")
    try:
        result = subprocess.run(
            [sys.executable, path],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        print(result.stdout or "")
        print(f"Concluído: {path}\n{'-'*80}\n")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar {path}")
        print(e.stderr)
        sys.exit(1)

print("Pipeline finalizado com sucesso!")
