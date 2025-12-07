# src/kpis.py
import pandas as pd

def acidentes_por_periodo(df: pd.DataFrame):
    """Conta acidentes por fase do dia e indica percentual de fatais."""
    # Fatais: mortos > 0
    df['fatal'] = df['mortos'] > 0
    resumo = df.groupby('fase_dia').agg(
        total_acidentes=('id', 'count'),
        acidentes_fatais=('fatal', 'sum')
    )
    resumo['percentual_fatais'] = (resumo['acidentes_fatais'] / resumo['total_acidentes']) * 100
    return resumo.reset_index()

def causas_mais_comuns(df: pd.DataFrame, top_n=10):
    """Top N causas de acidentes mais frequentes."""
    return df['causa_acidente'].value_counts().head(top_n).reset_index().rename(
        columns={'index': 'causa', 'causa_acidente': 'ocorrencias'}
    )

def mortes_por_veiculo(df: pd.DataFrame):
    """Total de mortos e feridos por tipo de veículo."""
    # Se houver separação de veículos por tipo, pode-se adaptar
    resumo = df.groupby('veiculos').agg(
        mortos=('mortos', 'sum'),
        feridos_leves=('feridos_leves', 'sum'),
        feridos_graves=('feridos_graves', 'sum'),
        total_acidentes=('id', 'count')
    )
    return resumo.reset_index()

def acidentes_fatais_vs_nao_fatais(df: pd.DataFrame):
    """Resumo de acidentes fatais vs não fatais."""
    df['fatal'] = df['mortos'] > 0
    resumo = df.groupby('fatal').agg(
        total_acidentes=('id', 'count')
    ).reset_index()
    resumo['tipo'] = resumo['fatal'].map({True: 'Fatais', False: 'Não Fatais'})
    return resumo[['tipo', 'total_acidentes']]

def fatores_impacto(df: pd.DataFrame):
    """Análise cruzada de gravidade do acidente com fatores diversos."""
    df['fatal'] = df['mortos'] > 0
    fatores = ['condicao_metereologica', 'tipo_pista', 'tracado_via']
    resultados = {}
    for fator in fatores:
        resumo = df.groupby(fator).agg(
            total_acidentes=('id', 'count'),
            acidentes_fatais=('fatal', 'sum'),
            mortos=('mortos', 'sum'),
            feridos=('feridos', 'sum')
        ).reset_index()
        resultados[fator] = resumo
    return resultados

def resumo_geral(df: pd.DataFrame):
    """Resumo geral de acidentes, mortos, feridos e veículos envolvidos."""
    resumo = {
        'total_acidentes': len(df),
        'total_mortos': df['mortos'].sum(),
        'total_feridos_leves': df['feridos_leves'].sum(),
        'total_feridos_graves': df['feridos_graves'].sum(),
        'total_ilesos': df['ilesos'].sum(),
        'total_veiculos': df['veiculos'].sum()
    }
    return resumo
