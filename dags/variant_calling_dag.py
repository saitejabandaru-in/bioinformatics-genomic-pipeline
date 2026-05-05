"""Airflow DAG for variant calling, annotation, and export."""

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
        dag_id="genomic_variant_calling",
        start_date=datetime(2024, 1, 1),
        schedule=None,
        catchup=False,
        tags=["genomics", "variants"],
    ) as dag:
        gatk = BashOperator(
            task_id="gatk_haplotypecaller",
            bash_command=(
                "python -m pipeline.variant_calling.gatk_haplotype "
                "--reference {{ dag_run.conf['reference'] }} "
                "--input-bam {{ dag_run.conf['bam'] }} "
                "--output-vcf output/variants/sample.vcf"
            ),
        )

        annotate = BashOperator(
            task_id="vep_annotate",
            bash_command=(
                "python -m pipeline.annotation.vep_annotator "
                "--input-vcf output/variants/sample.vcf "
                "--output-vcf output/variants/sample.annotated.vcf"
            ),
        )

        export = BashOperator(
            task_id="vcf_to_parquet",
            bash_command=(
                "python -m transforms.vcf_to_parquet "
                "--input-vcf output/variants/sample.annotated.vcf "
                "--output output/results/sample.parquet"
            ),
        )

        gatk >> annotate >> export
else:
    dag = None
