# airflow/dags/acidentes_2025_dag.py
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Importando funções do ETL já existentes
from src.pipeline import load_csv
from transformacao import validate_required_columns, validate_no_nulls
from src.kpis import calcular_kpis  # substitua pelo nome real da função de KPI

# Colunas obrigatórias do CSV DATATRAN 2025
REQUIRED_COLUMNS = [
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

# Funções intermediárias para tasks
def task_ingest(**context):
    df = load_csv()
    context['ti'].xcom_push(key='df', value=df)

def task_validate_columns(**context):
    df = context['ti'].xcom_pull(key='df', task_ids='ingest_task')
    if not validate_required_columns(df, REQUIRED_COLUMNS):
        raise ValueError("Colunas obrigatórias ausentes")

def task_validate_nulls(**context):
    df = context['ti'].xcom_pull(key='df', task_ids='ingest_task')
    if not validate_no_nulls(df, REQUIRED_COLUMNS):
        raise ValueError("Valores nulos encontrados em colunas críticas")

def task_clean(**context):
    df = context['ti'].xcom_pull(key='df', task_ids='ingest_task')
    df_clean = df[REQUIRED_COLUMNS]
    context['ti'].xcom_push(key='df_clean', value=df_clean)

def task_kpis(**context):
    df_clean = context['ti'].xcom_pull(key='df_clean', task_ids='clean_task')
    calcular_kpis(df_clean)

# Definição da DAG
with DAG(
    dag_id='acidentes_2025_dag',
    description='Pipeline de acidentes 2025 com tasks separadas',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['pipeline', 'acidentes', '2025']
) as dag:

    ingest_task = PythonOperator(
        task_id='ingest_task',
        python_callable=task_ingest,
        provide_context=True
    )

    validate_columns_task = PythonOperator(
        task_id='validate_columns_task',
        python_callable=task_validate_columns,
        provide_context=True
    )

    validate_nulls_task = PythonOperator(
        task_id='validate_nulls_task',
        python_callable=task_validate_nulls,
        provide_context=True
    )

    clean_task = PythonOperator(
        task_id='clean_task',
        python_callable=task_clean,
        provide_context=True
    )

    kpis_task = PythonOperator(
        task_id='kpis_task',
        python_callable=task_kpis,
        provide_context=True
    )

    # Encadeamento
    ingest_task >> validate_columns_task >> validate_nulls_task >> clean_task >> kpis_task
