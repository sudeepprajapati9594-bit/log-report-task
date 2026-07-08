import json
from collections import Counter
from datetime import datetime, timezone
import re


requests = {}
clients = set()
paths = Counter()
hours = Counter()
errors = 0


with open("/app/access.log") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        request_id = re.search(r"request_id=(\S+)", line).group(1)

        # Ignore retries
        if request_id in requests:
            continue

        requests[request_id] = True

        client = re.search(r"client=(\S+)", line).group(1)
        clients.add(client)

        path = re.search(r"path=(\S+)", line).group(1)
        paths[path] += 1

        status = int(re.search(r"status=(\d+)", line).group(1))

        if status >= 400:
            errors += 1

        timestamp = re.search(r'timestamp="([^"]+)"', line).group(1)

        dt = datetime.strptime(
            timestamp,
            "%d/%b/%Y:%H:%M:%S %z"
        )

        utc_time = dt.astimezone(timezone.utc)

        hour_key = utc_time.strftime("%Y-%m-%dT%H:00:00Z")
        hours[hour_key] += 1


total = len(requests)

report = {
    "total_requests": total,
    "unique_clients": len(clients),
    "top_pages": [
        page for page, count in paths.most_common(5)
    ],
    "hourly_traffic": dict(hours),
    "error_rate": round((errors / total) * 100, 2) if total else 0
}


with open("/app/report.json", "w") as f:
    json.dump(report, f, indent=2)
