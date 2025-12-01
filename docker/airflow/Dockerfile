FROM apache/airflow:2.9.1-python3.10

# Instala dependências extras necessárias para o pipeline
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libsasl2-dev \
    libssl-dev \
    libpq-dev \
    && apt-get clean

USER airflow

# Instala os providers essenciais
RUN pip install --no-cache-dir \
    apache-airflow-providers-amazon \
    apache-airflow-providers-postgres \
    pandas \
    numpy \
    pyarrow \
    boto3

# Copia configurações (opcional)
COPY ./config/airflow.cfg /opt/airflow/config/airflow.cfg

# Ajusta permissões
USER root
RUN chown -R airflow: /opt/airflow
USER airflow
