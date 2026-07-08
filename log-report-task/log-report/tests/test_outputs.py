import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")


def load_report():
    assert REPORT_PATH.exists(), "report.json not found"

    with open(REPORT_PATH) as f:
        return json.load(f)


def test_report_exists():
    report = load_report()

    assert isinstance(report, dict)


def test_required_fields():
    report = load_report()

    required = {
        "total_requests",
        "unique_clients",
        "top_pages",
        "hourly_traffic",
        "error_rate",
    }

    assert required.issubset(report.keys())


def test_request_count():
    report = load_report()

    assert report["total_requests"] == 4


def test_unique_clients():
    report = load_report()

    assert report["unique_clients"] == 3


def test_top_pages():
    report = load_report()

    assert "/products" in report["top_pages"]


def test_hourly_traffic():
    report = load_report()

    assert isinstance(report["hourly_traffic"], dict)

    assert (
        "2026-07-08T05:00:00Z"
        in report["hourly_traffic"]
    )


def test_error_rate():
    report = load_report()

    assert report["error_rate"] == 50
