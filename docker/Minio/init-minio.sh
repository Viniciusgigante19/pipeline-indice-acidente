#!/bin/sh
set -e

# Configurar alias para o MinIO
mc alias set myminio http://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

# Criar bucket se não existir
mc mb myminio/acidentes || true

# Criar política full-access para Airflow
cat <<EOF > /tmp/full-access-acidentes.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": [
        "arn:aws:s3:::acidentes",
        "arn:aws:s3:::acidentes/*"
      ]
    }
  ]
}
EOF
mc admin policy add myminio full-access-acidentes /tmp/full-access-acidentes.json

# Criar política readonly para Dev
cat <<EOF > /tmp/readonly-acidentes.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject","s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::acidentes",
        "arn:aws:s3:::acidentes/*"
      ]
    }
  ]
}
EOF
mc admin policy add myminio readonly-acidentes /tmp/readonly-acidentes.json

# Criar usuário airflow com acesso total
mc admin user add myminio airflow airflow123
mc admin policy set myminio full-access-acidentes user=airflow

# Criar usuário dev com acesso somente leitura
mc admin user add myminio dev dev123
mc admin policy set myminio readonly-acidentes user=dev
