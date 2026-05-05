from pathlib import Path

from pipeline.alignment.bwa_mem2 import build_bwa_mem2_command
from pipeline.variant_calling.gatk_haplotype import build_gatk_command


def test_bwa_mem2_command_includes_paired_reads_and_output():
    command = build_bwa_mem2_command(Path("ref.fa"), Path("r1.fq.gz"), Path("r2.fq.gz"), Path("out.sam"), 8)

    assert command == ["bwa-mem2", "mem", "-t", "8", "ref.fa", "r1.fq.gz", "r2.fq.gz", "-o", "out.sam"]


def test_gatk_haplotype_command():
    command = build_gatk_command(Path("ref.fa"), Path("sample.bam"), Path("sample.vcf"))

    assert command == [
        "gatk",
        "HaplotypeCaller",
        "-R",
        "ref.fa",
        "-I",
        "sample.bam",
        "-O",
        "sample.vcf",
    ]
