# Imagem mais completa baseada em Debian Bullseye
FROM python:3.10-bullseye

# Usamos root por padrão nessa imagem
USER root

# Configura repositórios Debian com HTTPS
RUN echo "deb https://deb.debian.org/debian bullseye main" > /etc/apt/sources.list && \
    echo "deb https://deb.debian.org/debian bullseye-updates main" >> /etc/apt/sources.list && \
    echo "deb https://security.debian.org/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libsasl2-dev \
        libssl-dev \
        libpq-dev \
        build-essential \
        curl \
        wget \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instala o Apache Airflow e os providers necessários
RUN pip install --no-cache-dir \
    apache-airflow==2.9.1 \
    apache-airflow-providers-amazon \
    apache-airflow-providers-postgres \
    pandas \
    numpy \
    pyarrow \
    boto3

# Cria diretório de configuração do Airflow
RUN mkdir -p /opt/airflow/config

# Copia configurações personalizadas (opcional)
COPY ./config/airflow.cfg /opt/airflow/config/airflow.cfg

# Cria usuário airflow para rodar o serviço
RUN useradd -ms /bin/bash airflow && chown -R airflow: /opt/airflow
USER airflow

# Define diretório de trabalho
WORKDIR /opt/airflow

# Comando padrão (pode ser sobrescrito no docker-compose)
CMD ["airflow", "version"]
