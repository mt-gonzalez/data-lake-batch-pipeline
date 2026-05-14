#!/bin/bash
set -e

echo "Initializing MinIO Data Lake..."

mc alias set local http://minio:9000 mtgonzalez secret123


echo "Creating buckets..."

mc mb local/datalake-bronze --ignore-existing
mc mb local/datalake-silver --ignore-existing
mc mb local/datalake-gold --ignore-existing


echo "Applying policies..."

mc admin policy create local orchestration-policy infra/policies/orch_policy.json || true
mc admin policy create local job-policy infra/policies/job_policy.json || true
mc admin policy create local bi-policy infra/policies/bi_policy.json || true


echo "Creating users..."

mc admin user add local airflow airflow123 || true
mc admin user add local jobs secret-jobs123 || true
mc admin user add local bi-analyst bi-analyst123 || true


echo "Attaching policies..."

mc admin policy attach local orchestration-policy --user airflow || true
mc admin policy attach local job-policy --user jobs || true
mc admin policy attach local bi-policy --user bi-analyst || true

echo "Completed."