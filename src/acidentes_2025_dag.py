# airflow/dags/acidentes_2025_dag.py

import sys
sys.path.append("/opt/airflow/dags")

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from minio import Minio
import os
import pandas as pd

# Importando funções do ETL já existentes
from pipeline import load_csv
from transformacao import transform_pipeline   # usamos o pipeline completo
from kpis import acidentes_por_periodo

# Função utilitária para inicializar o client MinIO
def get_minio_client():
    return Minio(
        "minio:9000",  # nome do serviço no docker-compose
        access_key=os.getenv("MINIO_ROOT_USER"),
        secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
        secure=False
    )

# Funções intermediárias para tasks
def task_ingest(**context):
    raw_path = "/opt/airflow/datasets/datatran2025_amostra_100.csv"
    df = load_csv(raw_path)

    # salva cópia em sandbox (nunca sobrescreve o bruto)
    sandbox_path = "/opt/airflow/sandbox/datatran2025_amostra_ingest.csv"
    df.to_csv(sandbox_path, index=False)

    # envia para MinIO a cópia
    client = get_minio_client()
    client.fput_object("acidentes", "datatran2025_amostra_ingest.csv", sandbox_path)

def task_clean(**context):
    client = get_minio_client()
    local_path = "/opt/airflow/sandbox/datatran2025_amostra_ingest.csv"
    client.fget_object("acidentes", "datatran2025_amostra_ingest.csv", local_path)

    # usa o pipeline completo de transformação
    df_clean = transform_pipeline(local_path)

    # salva dentro do sandbox
    sandbox_clean = "/opt/airflow/sandbox/df_clean.csv"
    df_clean.to_csv(sandbox_clean, index=False)

    # salva também no volume acessível ao host (outputs)
    path_output = "/opt/airflow/outputs/df_clean.csv"
    df_clean.to_csv(path_output, index=False)

    # envia para MinIO usando o arquivo salvo
    client.fput_object("acidentes", "df_clean.csv", sandbox_clean)

def task_kpis(**context):
    client = get_minio_client()
    local_path = "/opt/airflow/sandbox/df_clean.csv"
    client.fget_object("acidentes", "df_clean.csv", local_path)

    df_clean = pd.read_csv(local_path)
    resultados = acidentes_por_periodo(df_clean)
    print(resultados)

# Definição da DAG
with DAG(
    dag_id='acidentes_2025_dag',
    description='Pipeline de acidentes 2025 com tasks separadas e integração com MinIO',
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
    ingest_task >> clean_task >> kpis_task
