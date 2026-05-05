"""Airflow DAG for ingestion and quality-control stages."""

from __future__ import annotations

from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
except ImportError:  # Allows importing the module in lightweight test environments.
    DAG = None
    BashOperator = None


if DAG and BashOperator:
    with DAG(
        dag_id="genomic_ingestion_qc",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
        tags=["genomics", "qc"],
    ) as dag:
        run_fastqc = BashOperator(
            task_id="run_fastqc",
            bash_command="python -m pipeline.qc.fastqc_runner --input {{ dag_run.conf['fastq'] }} --output-dir output/qc",
        )
else:
    dag = None
