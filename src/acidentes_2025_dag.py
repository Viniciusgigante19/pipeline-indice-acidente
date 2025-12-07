# src/pipeline_dag.py
from pipeline import load_csv
from transformacao import validate_required_columns, validate_no_nulls

def run_pipeline():
    # 1. Carregar CSV
    df = load_csv()
    if df.empty:
        print("Pipeline interrompido: CSV vazio ou falha no carregamento.")
        return
    print("CSV carregado com sucesso.")

    # 2. Validações (todas as colunas reais do CSV DATATRAN 2025)
    required_columns = [
        "id",
        "data_inversa",
        "dia_semana",
        "horario",
        "uf",
        "br",
        "km",
        "municipio",
        "causa_acidente",
        "tipo_acidente",
        "classificacao_acidente",
        "fase_dia",
        "sentido_via",
        "condicao_metereologica",
        "tipo_pista",
        "tracado_via",
        "uso_solo",
        "pessoas",
        "mortos",
        "feridos_leves",
        "feridos_graves",
        "ilesos",
        "ignorados",
        "feridos",
        "veiculos",
        "latitude",
        "longitude",
        "regional",
        "delegacia",
        "uop"
    ]

    if not validate_required_columns(df, required_columns):
        print("Pipeline interrompido: colunas obrigatórias ausentes.")
        return

    if not validate_no_nulls(df, required_columns):
        print("Pipeline interrompido: existem valores nulos em colunas críticas.")
        return

    # 3. Pipeline continua (limpeza, normalização, análises, etc.)
    print("Validações concluídas. Pipeline pronto para próximos passos.")

    # Exemplo: dataset reduzido com apenas as colunas do schema
    df_clean = df[required_columns]

    # Aqui você continua com limpeza, normalização, KPIs, etc.
    # Exemplo: df_clean = clean_data(df)

if __name__ == "__main__":
    run_pipeline()
