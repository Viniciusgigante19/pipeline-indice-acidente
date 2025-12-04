import pandas as pd

# Lista de colunas esperadas no CSV
EXPECTED_COLUMNS = [
    "id", "data_inversa", "dia_semana", "horario", "uf", "br", "km",
    "municipio", "causa_acidente", "tipo_acidente", "classificacao_acidente",
    "fase_dia", "sentido_via", "condicao_metereologica", "tipo_pista",
    "tracado_via", "uso_solo", "pessoas", "mortos", "feridos_leves",
    "feridos_graves", "ilesos", "ignorados", "feridos", "veiculos",
    "latitude", "longitude", "regional", "delegacia", "uop"
]

def check_columns(df: pd.DataFrame):
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    extra = set(df.columns) - set(EXPECTED_COLUMNS)
    return missing, extra

def check_nulls(df: pd.DataFrame):
    return df.isnull().sum()

def check_duplicates(df: pd.DataFrame):
    return df.duplicated().sum()

def validate_dataframe(df: pd.DataFrame):
    missing, extra = check_columns(df)
    nulls = check_nulls(df)
    duplicates = check_duplicates(df)
    
    validation_report = {
        "missing_columns": missing,
        "extra_columns": extra,
        "null_values": nulls.to_dict(),
        "duplicate_rows": duplicates
    }

def validate_required_columns(df: pd.DataFrame, required_columns: list) -> bool:
    """Verifica se todas as colunas obrigatórias estão presentes no DataFrame."""
    missing = set(required_columns) - set(df.columns)
    if missing:
        print(f"Colunas obrigatórias ausentes: {missing}")
        return False
    return True

def validate_no_nulls(df: pd.DataFrame, required_columns: list) -> bool:
    """Verifica se não há valores nulos nas colunas obrigatórias."""
    nulls = df[required_columns].isnull().sum()
    cols_with_nulls = nulls[nulls > 0]
    if not cols_with_nulls.empty:
        print(f"Valores nulos encontrados em colunas críticas: {cols_with_nulls.to_dict()}")
        return False
    return True


    return validation_report
