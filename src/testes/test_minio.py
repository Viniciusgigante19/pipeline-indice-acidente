# src/testes/test_minio.py
import os
from minio import Minio
from minio.error import S3Error

# pegar credenciais do ambiente
MINIO_USER = os.getenv("MINIO_ROOT_USER", "admin")
MINIO_PASS = os.getenv("MINIO_ROOT_PASSWORD", "password123")
MINIO_PORT = os.getenv("MINIO_PORT", "9000")
MINIO_HOST = f"minio:{MINIO_PORT}"

BUCKET_NAME = "acidentes"
FILE_NAME = "datatran2025_amostra_100.csv"
DOWNLOAD_PATH = f"/app/src/{FILE_NAME}"

def main():
    client = Minio(
        MINIO_HOST,
        access_key=MINIO_USER,
        secret_key=MINIO_PASS,
        secure=False
    )

    print("Buckets disponíveis:")
    for bucket in client.list_buckets():
        print(bucket.name)

    try:
        client.fget_object(BUCKET_NAME, FILE_NAME, DOWNLOAD_PATH)
        print(f"Arquivo {FILE_NAME} baixado com sucesso em {DOWNLOAD_PATH}!")
    except S3Error as e:
        print(f"Erro ao baixar arquivo: {e}")

if __name__ == "__main__":
    main()
