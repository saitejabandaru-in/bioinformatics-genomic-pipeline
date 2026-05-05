from pipeline.qc.quality_gate import evaluate_quality


def test_quality_gate_passes_with_limited_failures():
    result = evaluate_quality({"Basic Statistics": "PASS", "Adapter Content": "FAIL"}, max_failed_checks=1)

    assert result["passed"] is True
    assert result["failed_checks"] == ["Adapter Content"]


def test_quality_gate_fails_when_threshold_exceeded():
    result = evaluate_quality({"A": "FAIL", "B": "FAIL", "C": "WARN"}, max_failed_checks=1)

    assert result["passed"] is False
    assert result["warning_checks"] == ["C"]
