# src/pipeline.py
import pandas as pd
from pathlib import Path

# Caminho para a pasta de datasets
DATASET_DIR = Path(__file__).parent.parent / "datasets"
CSV_SAMPLE = DATASET_DIR / "datatran2025_amostra_100.csv"

EXPECTED_COLUMNS = [
    "id", "data_inversa", "dia_semana", "horario", "uf", "br", "km",
    "municipio", "causa_acidente", "tipo_acidente", "classificacao_acidente",
    "fase_dia", "sentido_via", "condicao_metereologica", "tipo_pista",
    "tracado_via", "uso_solo", "pessoas", "mortos", "feridos_leves",
    "feridos_graves", "ilesos", "ignorados", "feridos", "veiculos",
    "latitude", "longitude", "regional", "delegacia", "uop"
]

def load_csv(file_path=CSV_SAMPLE):
    """
    Lê o CSV e retorna um DataFrame Pandas usando encoding utf-8,
    forçando as colunas esperadas.
    """
    try:
        df = pd.read_csv(
            file_path,
            sep=';', 
            encoding="utf-8-sig",
            header=None,              # ignora o cabeçalho original
            names=EXPECTED_COLUMNS # aplica os nomes corretos
        )
        print(f"CSV carregado com sucesso: {len(df)} linhas")
        print(f"Colunas aplicadas: {df.columns.tolist()}")
        print(df.head(1))
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    df = load_csv()
    print(df.head())
