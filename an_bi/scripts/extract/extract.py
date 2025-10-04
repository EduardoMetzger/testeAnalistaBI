import os
import duckdb

con = duckdb.connect(r"C:\Users\eduar\OneDrive\Área de Trabalho\EduardoMetzger\testeAnalistaBI\an_bi\analise.duckdb")

output_folder = r"C:\Users\eduar\OneDrive\Área de Trabalho\EduardoMetzger\testeAnalistaBI\an_bi\files\raw"
os.makedirs(output_folder, exist_ok=True)

tables = ["extract_empresas"]

for t in tables:
    out_path = os.path.join(output_folder, f"{t}.csv")
    con.execute(f"COPY {t} TO '{out_path}' (FORMAT CSV, HEADER TRUE);")
    print(f"{t} exportado para {out_path}")

con.close()
