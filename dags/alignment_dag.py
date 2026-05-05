"""Airflow DAG for alignment stages."""

from __future__ import annotations

from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator
except ImportError:
    DAG = None
    BashOperator = None


if DAG and BashOperator:
    with DAG(
        dag_id="genomic_alignment",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
        tags=["genomics", "alignment"],
    ) as dag:
        align = BashOperator(
            task_id="bwa_mem2_align",
            bash_command=(
                "python -m pipeline.alignment.bwa_mem2 "
                "--reference {{ dag_run.conf['reference'] }} "
                "--read1 {{ dag_run.conf['read1'] }} "
                "--read2 {{ dag_run.conf.get('read2', '') }} "
                "--output-sam output/alignment/sample.sam"
            ),
        )

        sort = BashOperator(
            task_id="samtools_sort",
            bash_command=(
                "python -m pipeline.alignment.samtools_sort "
                "--input-sam output/alignment/sample.sam "
                "--output-bam output/alignment/sample.sorted.bam --index"
            ),
        )

        align >> sort
else:
    dag = None
