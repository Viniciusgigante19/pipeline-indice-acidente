# src/transformacao.py
import pandas as pd
from datetime import datetime

EXPECTED_COLUMNS = [
    "id", "data_inversa", "dia_semana", "horario", "uf", "br", "km",
    "municipio", "causa_acidente", "tipo_acidente", "classificacao_acidente",
    "fase_dia", "sentido_via", "condicao_metereologica", "tipo_pista",
    "tracado_via", "uso_solo", "pessoas", "mortos", "feridos_leves",
    "feridos_graves", "ilesos", "ignorados", "feridos", "veiculos",
    "latitude", "longitude", "regional", "delegacia", "uop"
]

CRITICAL_COLUMNS = [
    "id", "data_inversa", "uf", "br", "km",
    "municipio", "causa_acidente", "tipo_acidente"
]

def load_csv(file_path: str):
    """Carrega CSV e retorna DataFrame com colunas esperadas."""
    try:
        df = pd.read_csv(
            file_path,
            sep=';', 
            encoding="utf-8-sig",
            header=None,              # não usa nenhuma linha como cabeçalho
            names=EXPECTED_COLUMNS    # aplica os nomes corretos
        )
        print(f"CSV carregado com sucesso: {len(df)} linhas")
        print(f"Colunas aplicadas: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()

def validate_columns(df: pd.DataFrame):
    """Valida presença de colunas e duplicadas."""
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS)
    duplicates = df.duplicated().sum()
    if missing:
        print(f"Colunas ausentes: {missing}")
    if extra:
        print(f"Colunas extras ignoradas: {extra}")
    if duplicates > 0:
        print(f"{duplicates} linhas duplicadas encontradas")
    return missing, extra, duplicates

def validate_nulls(df: pd.DataFrame):
    """Verifica colunas críticas para nulos."""
    nulls = df[CRITICAL_COLUMNS].isnull().sum()
    cols_with_nulls = nulls[nulls > 0]
    if not cols_with_nulls.empty:
        print(f"Valores nulos em colunas críticas: {cols_with_nulls.to_dict()}")
        return False
    return True

def normalize_types(df: pd.DataFrame):
    """Converte tipos de dados para os esperados."""
    df['id'] = pd.to_numeric(df['id'], errors='coerce', downcast='integer')
    df['br'] = pd.to_numeric(df['br'], errors='coerce', downcast='integer')
    df['km'] = pd.to_numeric(df['km'], errors='coerce')
    df['pessoas'] = pd.to_numeric(df['pessoas'], errors='coerce', downcast='integer')
    df['mortos'] = pd.to_numeric(df['mortos'], errors='coerce', downcast='integer')
    df['feridos_leves'] = pd.to_numeric(df['feridos_leves'], errors='coerce', downcast='integer')
    df['feridos_graves'] = pd.to_numeric(df['feridos_graves'], errors='coerce', downcast='integer')
    df['ilesos'] = pd.to_numeric(df['ilesos'], errors='coerce', downcast='integer')
    df['ignorados'] = pd.to_numeric(df['ignorados'], errors='coerce', downcast='integer')
    df['feridos'] = pd.to_numeric(df['feridos'], errors='coerce', downcast='integer')
    df['veiculos'] = pd.to_numeric(df['veiculos'], errors='coerce', downcast='integer')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    
    # Data e hora
    df['data_inversa'] = pd.to_datetime(df['data_inversa'], errors='coerce', format='%Y-%m-%d')
    df['horario'] = pd.to_datetime(df['horario'], errors='coerce').dt.time
    return df

def normalize_strings(df: pd.DataFrame):
    """Remove espaços extras e padroniza texto."""
    string_cols = df.select_dtypes(include='object').columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()
    return df

def remove_duplicates(df: pd.DataFrame):
    """Remove linhas duplicadas."""
    return df.drop_duplicates()

def transform_pipeline(file_path: str):
    """Pipeline completa de validação e tratamento de dados."""
    df = load_csv(file_path)
    if df.empty:
        return df
    
    missing, extra, duplicates = validate_columns(df)
    df = normalize_strings(df)
    df = normalize_types(df)
    df = remove_duplicates(df)
    
    if not validate_nulls(df):
        print("Atenção: existem valores nulos em colunas críticas!")
    
    # Garante apenas colunas esperadas e na ordem correta
    df = df[EXPECTED_COLUMNS]
    
    print("Transformação concluída com sucesso.")
    return df

# Exemplo de uso
if __name__ == "__main__":
    df = transform_pipeline("datasets/datatran2025_amostra_100.csv")
    print(df.head())
