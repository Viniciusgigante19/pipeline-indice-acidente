import os
import boto3
from botocore.client import Config

# Carregar variáveis de ambiente (assume que já estão exportadas no container)
MINIO_USER = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "password123")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_HOST = f"http://minio:{MINIO_PORT}"  # Nome do serviço no Docker Compose
DATASET_PATH = "/datasets/datatran2025_amostra_1000.csv"
BUCKET_NAME = "dados-brutos"

def main():
    # Conectar ao MinIO
    s3 = boto3.resource(
        "s3",
        endpoint_url=MINIO_HOST,
        aws_access_key_id=MINIO_USER,
        aws_secret_access_key=MINIO_PASSWORD,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

    # Criar bucket se não existir
    if not s3.Bucket(BUCKET_NAME) in s3.buckets.all():
        s3.create_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket '{BUCKET_NAME}' criado.")
    else:
        print(f"Bucket '{BUCKET_NAME}' já existe.")

    # Fazer upload do CSV
    file_name = os.path.basename(DATASET_PATH)
    s3.Bucket(BUCKET_NAME).upload_file(DATASET_PATH, file_name)
    print(f"Arquivo '{file_name}' enviado para o bucket '{BUCKET_NAME}' com sucesso!")

if __name__ == "__main__":
    main()
