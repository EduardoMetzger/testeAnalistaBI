import os
import pandas as pd
import numpy as np

base_dir = os.path.dirname(__file__)
input_path = os.path.join(base_dir, "..", "..", "files", "clean", "bolsa_cotacoes.csv")
output_dir = os.path.join(base_dir, "..", "..", "files", "enrich")
output_path = os.path.join(output_dir, "f_cotacoes.csv")

os.makedirs(output_dir, exist_ok=True)

print("Iniciando enrich de cotacoes_bolsa")

try:
    df = pd.read_csv(input_path, sep=";", encoding="utf-8", low_memory=False)

    campos_valores = [
        "cotacao_valor_abertura",
        "cotacao_valor_maximo",
        "cotacao_valor_minimo",
        "cotacao_valor_medio",
        "cotacao_valor_fechamento"
    ]

    #ajuste decimais
    for col in campos_valores:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace(",", ".", regex=False)
                .replace("nan", np.nan)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    #calcular variacao
    if "cotacao_valor_abertura" in df.columns and "cotacao_valor_fechamento" in df.columns:
        df["cotacao_variacao"] = (
            df["cotacao_valor_fechamento"] / df["cotacao_valor_abertura"] - 1
        ).round(4)
    else:
        print("erro ao calcular a variação")

    for col in campos_valores:
        if col not in df.columns:
            continue

        valores_validos = df[col].dropna()
        if valores_validos.empty:
            continue

        #ajustar os casos que estão com problema de decimal (ex:1.08 -> 10800001)
        media = valores_validos.mean()
        if media > 10000:
            print(f"ajustando o decimal de {col}")
            df[col] /= 1000

        if df[col].mean() > 1000:
            print(f"ajustando o decimla de {col}")
            df[col] /= 1000

        df[col] = df[col].round(2)

    for col in campos_valores + ["cotacao_variacao"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: str(x).replace(".", ",") if pd.notnull(x) else "")

    df.to_csv(output_path, sep=";", index=False, encoding="utf-8")

    print(f"Arquivo salvo em {output_path}")
    print(f"Total de registros: {len(df)}")

except Exception as e:
    print("Erro ao processar enrich:", e)

print("Concluído")
