# Documentação do Pipeline
Jefferson Nascimento -6324617
Lucas Henrique- 6324537
Marcelo Luis - 63424637
Vinicius GIgante - 6324558

## 1. Introdução

O projeto **pipeline-indicie-acidente** implementa um pipeline completo de ETL (Extract, Transform, Load), voltado ao processamento e análise de dados relacionados a acidentes de trânsito. O objetivo principal é automatizar a coleta, transformação e armazenamento de dados estruturados, possibilitando análises, relatórios e cálculos de indicadores como o Índice de Acidentes por município ou região. A arquitetura do projeto foi desenvolvida para ser **robusta e escalável**, utilizando contêineres Docker, banco de dados relacional e módulos Python modulares. Toda a estrutura foi pensada para facilitar execução, manutenção e evolução futura.

## 2. Arquitetura do Sistema

O sistema segue uma arquitetura em pipeline em ETL, composta por três estágios fundamentais:

*   **Extração:** A fase responsável por buscar dados brutos externas, como arquivos CSV contidos na pasta `datasets`. A extração lê, valida e converte esses arquivos em estrutura de dados manipuláveis (DataFrames).
*   **Transformações:** Os dados extraídos passam por processos de limpeza, padronização, enriquecimento e cálculos. Nesta fase é aplicado o cálculo do indicador principal: o índice de acidente, medida estática derivada dos dados de acidente e de informações demográficas.
*   **Carregamento:** Por fim, os dados transformados são carregados em um banco relacional, garantindo persistência, integridade e disponibilidade para consultas. O carregamento utiliza SQLAlchemy e scripts do diretório `database`. A orquestração dessas etapas é feita pelo `main.py`, centralizando a execução.

## 3. Estrutura do Repositório

A organização segue boas práticas de modularização e separação de responsabilidades, permitindo fácil manutenção e expansão do projeto:

*   **`docker`**: Contém Dockerfiles que definem o ambiente de execução do pipeline.
*   **`database`**: Scripts SQL responsáveis por criar tabelas, índices e constraints.
*   **`datasets`**: Fontes de dados utilizadas como entrada (CSV).
*   **`docs`**: Documentação, diagramas e especificações.
*   **`src`**: Código principal do ETL.
*   **`docker-compose.yml`**: Orquestra todos os serviços e dependências.
*   **`.env`**: Arquivo com variáveis sensíveis e configurações.

## 4. Pasta SRC – Código do Pipeline

A pasta `src/` reúne os componentes principais do pipeline ETL, cada um com responsabilidades bem definidas, seguindo princípios de modularidade e boa arquitetura. Abaixo, uma descrição detalhada de cada arquivo:

### `extract.py` : Módulo de Extração de Dados

Responsável pela primeira etapa do pipeline, este arquivo contém funções dedicadas à leitura dos dados brutos localizados nos arquivos CSV.

*   Utiliza `pandas.read_csv()` para carregar os conjuntos de dados.
*   Realiza validações preliminares, como verificação de colunas obrigatórias e detecção de valores nulos.
*   Garante que os dados cheguem à memória de forma organizada para as próximas etapas do processo.

### `transform.py` — Módulo de Transformação

Este é o núcleo da lógica de negócio do projeto. Ele aplica as regras e operações que preparam os dados para gerar o Índice de Acidentes.

Operações típicas realizadas:

*   Conversão e padronização de datas.
*   Normalização de colunas e tipos de dados.
*   Remoção de inconsistências, duplicatas e erros de preenchimento.
*   Aplicação de regras de limpeza específicas do domínio.
*   Cálculos estatísticos e agrupamentos para criar indicadores estruturados.

### `load.py` — Módulo de Carga no Banco de Dados

Este arquivo realiza a etapa final do ETL: a inserção dos dados tratados no banco relacional.

Destaques:

*   Estabelece conexão com o banco utilizando SQLAlchemy.
*   Implementa tratamento de exceções e validações antes da gravação.
*   Usa o método `to_sql()` para inserir os DataFrames diretamente nas tabelas.
*   Garante integridade e consistência dos registros inseridos.

### `utils.py` — Funções Auxiliares

Reúne utilitários que dão suporte aos demais módulos, promovendo reutilização de código e padronização.

Funções comuns:

*   Leitura e interpretação do arquivo `.env`.
*   Configuração de logs e mensagens do sistema.
*   Funções de formatação e validações auxiliares.

### `main.py` — Arquivo Orquestrador

É o ponto de entrada do pipeline. Sua função é garantir que todas as etapas sejam executadas na ordem correta: **EXTRAÇÃO → TRANSFORMAÇÃO → CARGA**. Através dele, o processo se torna automatizado, organizado e reprodutível.

## 5. Docker e Orquestração

O Docker é empregado no projeto para garantir que o pipeline seja executado de maneira consistente, independentemente das configurações da máquina do usuário. Por meio da containerização, todo o ambiente necessário é padronizado, evitando problemas de compatibilidade e facilitando a reprodução do sistema.

O arquivo `docker-compose.yml` é responsável por definir e orquestrar os principais contêineres, tais como:

*   Banco de dados (PostgreSQL)
*   Aplicação Python (Pipeline ETL)
*   Volumes persistentes para armazenamento de dados

## 6. Como Rodar o Projeto

O projeto utiliza Docker e Docker Compose para orquestrar todos os serviços necessários ao pipeline de acidentes, garantindo que tudo funcione de forma padronizada e independente do ambiente local.

O arquivo `docker-compose.yml` define serviços como:

*   MinIO (Data Lake S3 compatível)
*   PostgreSQL (Banco de dados relacional)
*   Airflow (agendador e executor de DAGs)
*   Contêiner Python responsável pelo pipeline ETL
*   Volumes persistentes para armazenamento de dados
*   Rede Docker interna

### 1. Verifique se o Docker está instalado

É necessário ter:

*   Docker Engine
*   Docker Compose

Basta rodar:
```bash
docker --version
docker compose version
```

### 2. Configure o arquivo `.env`

O projeto depende de variáveis de ambiente como:

*   `POSTGRES_USER`
*   `POSTGRES_PASSWORD`
*   `POSTGRES_DB`
*   `MINIO_ROOT_USER`
*   `MINIO_ROOT_PASSWORD`
*   `MINIO_PORT`
*   `MINIO_CONSOLE_PORT`

Certifique-se de que o arquivo `.env` está preenchido corretamente.

### 3. Acesse a pasta raiz do projeto

No terminal:
```bash
cd pipeline-indice-acidente-main
```

### 4. Suba todos os serviços do pipeline

Use o comando:
```bash
docker compose up –build
```

### 5. O que acontece neste passo:

**5.1 – O Docker cria:**

*   Contêiner do MinIO
*   Contêiner do PostgreSQL
*   Contêiner do Airflow Scheduler
*   Contêiner do Airflow Webserver
*   Contêiner do Pipeline Python (execução da DAG)

**5.2 – O Docker cria e monta volumes:**

*   `minio_data`
*   `postgres_data`
*   `datasets_data`

**5.3 – Inicialização do Airflow**

O Airflow sobe com:

*   DAG `acidentes_2025_dag.py`
*   Scheduler processando automaticamente o pipeline
*   Webserver para monitoramento

### 6. Acessar os contêineres do Airflow

*   Para entrar no terminal do webserver:
    ```bash
    docker exec -it airflow-webserver bash
    ```
*   Para entrar no terminal do scheduler:
    ```bash
    docker exec -it airflow-scheduler bash
    ```

Esses comandos permitem rodar scripts, instalar dependências e manipular a DAG por dentro do Airflow.

### 7. Instalar dependências necessárias

Dentro de qualquer contêiner do Airflow:
```bash
pip install pandas minio
```

Essas bibliotecas são necessárias para:

*   Leitura e manipulação dos dados (`pandas`)
*   Integração com MinIO (`minio SDK`)

### 8. Enviar arquivos para o MinIO

Ainda dentro do contêiner:
```bash
python dags/scripts/upload_minio.py
```

Esse script faz o upload dos dados de acidentes para o bucket S3 compatível do MinIO.

### Atualizar o banco do Airflow

Para aplicar updates no schema interno do Airflow:
```bash
airflow db upgrade
```

### Ativar a DAG

Por padrão, a DAG sobe pausada. Para ativá-la:
```bash
airflow dags unpause acidentes_2025_dag
```

### Disparar a DAG manualmente

Para rodar imediatamente:
```bash
airflow dags trigger acidentes_2025_dag
```

### Verificar histórico de execuções

Para checar se a DAG está sendo executada:
```bash
airflow dags list-runs -d acidentes_2025_dag
```

### Iniciar o Airflow Webserver manualmente (se necessário)

```bash
airflow webserver -p 8081
```

Isso é útil caso o webserver precise ser reiniciado.

### Listar tarefas da DAG

```bash
airflow tasks list acidentes_2025_dag
```

### Testar cada tarefa individualmente

Esses testes NÃO executam dependências, mas simulam a tarefa isolada.

*   Testar a ingestão:
    ```bash
    airflow tasks test acidentes_2025_dag ingest_task 2025-12-10
    ```
*   Testar a limpeza:
    ```bash
    airflow tasks test acidentes_2025_dag clean_task 2025-12-10
    ```
*   Testar o cálculo de KPIs:
    ```bash
    airflow tasks test acidentes_2025_dag kpis_task 2025-12-10
    ```
