Documentação Técnica do Pipeline de Acidentes Rodoviários

1. Visão Geral e Introdução

O projeto pipeline-indice-acidente implementa um pipeline completo de ETL (Extract, Transform, Load) para o processamento e análise de dados de acidentes de trânsito (DATATRAN 2025). O objetivo central é automatizar a coleta, transformação e armazenamento de dados estruturados, permitindo análises, relatórios e o cálculo de indicadores-chave, como o Índice de Acidentes por região.

A arquitetura foi concebida para ser robusta e escalável, utilizando a orquestração de contêineres Docker e módulos Python modulares, seguindo as melhores práticas de Engenharia de Dados.

2. Arquitetura do Sistema

O sistema adota uma arquitetura de pipeline em ETL, orquestrada pelo Apache Airflow, e segue um modelo de Data Lakehouse simplificado, conforme detalhado abaixo.

2.1. Fluxo do Pipeline

O fluxo de processamento é dividido em etapas modulares, garantindo a rastreabilidade e o reprocessamento:

Etapa
Task na DAG
Módulo Python
Descrição
Extração
ingest_task
pipeline.py
Lê o arquivo datatran2025.csv do volume mapeado.
Validação
validate_columns_task, validate_nulls_task
transformacao.py
Verifica a integridade dos dados (colunas obrigatórias e valores nulos críticos).
Transformação
transform_task
transformacao.py
Aplica limpeza, padronização de tipos e remoção de duplicatas.
Carga
load_task
load.py
Carrega o DataFrame limpo para a tabela datatran2025 no PostgreSQL.
KPIs
kpis_task
kpis.py, load.py
Calcula indicadores (ex: acidentes por período) e carrega o resultado para a tabela kpi_acidentes_por_periodo.


2.2. Tecnologias e Componentes

A infraestrutura é totalmente containerizada via Docker Compose:

Componente
Tecnologia
Função
Orquestração
Apache Airflow
Gerenciamento e agendamento do fluxo de trabalho (DAG).
Data Lake
MinIO
Armazenamento de dados brutos (S3-compatível).
Data Warehouse
PostgreSQL
Persistência de dados limpos e agregados.
Processamento
Python + Pandas
Lógica de ETL e cálculo de KPIs.
Visualização
Metabase
Business Intelligence (BI) e criação de dashboards.


3. Estrutura do Repositório

A organização do projeto segue uma estrutura modular para facilitar a manutenção e a expansão:

Diretório
Conteúdo
database/
Scripts SQL para criação de tabelas (create_table.sql) e views (create_views.sql).
datasets/
Fontes de dados brutos utilizadas como entrada (datatran2025.csv).
docker/
Dockerfiles e scripts de entrada para a construção das imagens personalizadas (Airflow, Python Testes).
docs/
Documentação, especificações e arquivos de progresso.
src/
Código principal do pipeline ETL e a definição da DAG.
docker-compose.yml
Orquestração de todos os serviços (PostgreSQL, Airflow, MinIO, Metabase).
.env
Variáveis de ambiente para configurações sensíveis e de conexão.


4. Módulos do Pipeline (src/)

A pasta src/ concentra a lógica de negócio do pipeline, com responsabilidades bem definidas:

Arquivo
Responsabilidade
acidentes_2025_dag.py
Orquestrador: Define a DAG do Airflow, encadeando as tasks de Extração, Validação, Transformação, Carga e KPI.
pipeline.py
Extração: Contém a função load_csv para ler os dados brutos.
transformacao.py
Transformação e Validação: Contém a lógica de limpeza, padronização de tipos (normalize_types) e validação de dados (validate_columns, validate_nulls).
load.py
Carga: Contém a função load_to_postgres para persistir os DataFrames no banco de dados.
kpis.py
Cálculo de Indicadores: Contém funções para calcular métricas de negócio, como acidentes_por_periodo.


5. Guia de Execução

5.1. Inicialização da Infraestrutura

1.
Pré-requisitos: Docker e Docker Compose instalados.

2.
Subir os Serviços: No diretório raiz do projeto, execute:

Bash


docker-compose up -d




5.2. Execução da DAG (Airflow)

1.
Acessar a Interface Web: Acesse http://localhost:8080 (usuário/senha padrão: airflow/airflow ).

2.
Ativar e Disparar: Ative a DAG acidentes_2025_dag e dispare uma execução manual.

5.3. Configuração do Metabase

1.
Acessar o Metabase: Acesse http://localhost:3000 e complete a configuração inicial.

2.
Adicionar o Banco de Dados: Configure a conexão com o PostgreSQL usando:

•
Host: postgres

•
Database Name: airflow

•
User/Password: airflow/airflow



3.
Criar Views: Execute o script de views no container do PostgreSQL:

Bash


docker exec -it postgres psql -U airflow -d airflow -f /docker-entrypoint-initdb.d/create_views.sql




6. Considerações Finais

O projeto está tecnicamente completo em termos de código e arquitetura. A etapa final de criação dos dashboards no Metabase e a validação da execução da DAG dependem da correta sincronização dos volumes do Docker no ambiente local.









