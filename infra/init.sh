#!/bin/bash
set -e

echo "Initializing MinIO Data Lake..."

mc alias set local http://minio:9000 mtgonzalez secret123


echo "Creating buckets..."

mc mb local/datalake-raw --ignore-existing
mc mb local/datalake-silver --ignore-existing
mc mb local/datalake-gold --ignore-existing


echo "Applying policies..."

mc admin policy create local raw-policy infra/policies/raw.json || true
mc admin policy create local silver-policy infra/policies/silver.json || true
mc admin policy create local gold-policy infra/policies/gold.json || true


echo "Creating users..."

mc admin user add local airflow airflow123 || true
mc admin user add local pipeline pipeline123 || true
mc admin user add local readonly readonly123 || true


echo "Attaching policies..."

mc admin policy attach local raw-policy --user airflow || true
mc admin policy attach local silver-policy --user pipeline || true
mc admin policy attach local gold-policy --user readonly || true

echo "Completed."