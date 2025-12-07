import boto3
from botocore.client import Config
import os

# pegar credenciais do ambiente
MINIO_USER = os.environ.get('MINIO_ROOT_USER')
MINIO_PASS = os.environ.get('MINIO_ROOT_PASSWORD')

s3 = boto3.resource(
    's3',
    endpoint_url='http://minio:9000',
    aws_access_key_id=MINIO_USER,
    aws_secret_access_key=MINIO_PASS,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)

# listar buckets
print("Buckets disponíveis:")
for bucket in s3.buckets.all():
    print(bucket.name)

# exemplo de download de arquivo
bucket_name = 'dados-brutos'
file_name = 'datatran2025_amostra_1000.csv'
s3.Bucket(bucket_name).download_file(file_name, f'/app/src/{file_name}')
print(f"Arquivo {file_name} baixado com sucesso!")
