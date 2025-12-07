#!/usr/bin/env bash
set -e

# Cria diretórios internos do Airflow
mkdir -p /opt/airflow/logs
mkdir -p /opt/airflow/dags
mkdir -p /opt/airflow/plugins

# Inicializa o banco se ainda não existir
airflow db migrate

# Cria usuário admin se não existir
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || true

exec "$@"
