"""Verifier for the log-report task.

Each test below maps to exactly one success criterion in instruction.md:
  1. "Save your findings so they can be reviewed."
  2. "how many requests there were"
  3. "the clients involved"
  4. "which pages were popular"
"""

import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected_stats():
    """Independently recompute the expected stats from access.log.

    Deliberately not shared code with solution/solve.py, so the verifier
    can't inherit a bug from the solution it is meant to check.
    """
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def _load_report():
    assert REPORT_PATH.exists(), "no report.json found"
    try:
        return json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_findings_saved():
    """instruction.md: "Save your findings so they can be reviewed."

    A finding that can't be located or parsed can't be reviewed, so this
    checks the report exists and is valid, parseable JSON.
    """
    report = _load_report()
    assert isinstance(report, dict), "report.json must contain a JSON object"


def test_request_count_reported():
    """instruction.md: "how many requests there were"."""
    report = _load_report()
    expected = _expected_stats()
    assert "total_requests" in report, "report.json is missing 'total_requests'"
    assert report["total_requests"] == expected["total_requests"], (
        f"total_requests: got {report['total_requests']!r}, "
        f"expected {expected['total_requests']!r}"
    )


def test_clients_reported():
    """instruction.md: "the clients involved"."""
    report = _load_report()
    expected = _expected_stats()
    assert "unique_ips" in report, "report.json is missing 'unique_ips'"
    assert report["unique_ips"] == expected["unique_ips"], (
        f"unique_ips: got {report['unique_ips']!r}, "
        f"expected {expected['unique_ips']!r}"
    )


def test_popular_pages_reported():
    """instruction.md: "which pages were popular"."""
    report = _load_report()
    expected = _expected_stats()
    assert "top_path" in report, "report.json is missing 'top_path'"
    assert report["top_path"] == expected["top_path"], (
        f"top_path: got {report['top_path']!r}, expected {expected['top_path']!r}"
    )
