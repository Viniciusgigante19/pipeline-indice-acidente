# src/pipeline.py
import pandas as pd
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent / "datasets"
CSV_SAMPLE = DATASET_DIR / "datatran2025_amostra_1000.csv"

def load_csv(file_path=CSV_SAMPLE):
    """
    Lê o CSV e retorna um DataFrame Pandas.
    """
    try:
        df = pd.read_csv(file_path)
        print(f"CSV carregado com sucesso: {len(df)} linhas")
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()  # retorna vazio em caso de erro

if __name__ == "__main__":
    df = load_csv()
    print(df.head())
