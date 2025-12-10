# src/scripts/upload_minio.py
import os
from minio import Minio
from minio.error import S3Error

# Carregar variáveis de ambiente (assume que já estão exportadas no container)
MINIO_USER = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "password123")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_HOST = f"minio:{MINIO_PORT}"  # Nome do serviço no Docker Compose
DATASET_PATH = "/opt/airflow/datasets/datatran2025_amostra_100.csv"
BUCKET_NAME = "acidentes"

def main():
    # Conectar ao MinIO
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_USER,
        secret_key=MINIO_PASSWORD,
        secure=False
    )

    # Criar bucket se não existir
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' criado.")
    else:
        print(f"Bucket '{BUCKET_NAME}' já existe.")

    # Fazer upload do CSV
    file_name = os.path.basename(DATASET_PATH)
    try:
        client.fput_object(BUCKET_NAME, file_name, DATASET_PATH)
        print(f"Arquivo '{file_name}' enviado para o bucket '{BUCKET_NAME}' com sucesso!")
    except S3Error as e:
        print(f"Erro ao enviar arquivo: {e}")

if __name__ == "__main__":
    main()
