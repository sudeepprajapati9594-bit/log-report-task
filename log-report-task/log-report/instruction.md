You are given an HTTP access log file:

/app/access.log

Your task is to analyze the log and create a traffic analytics report.

Write the final report to:

/app/report.json

The report must be a valid JSON object containing these fields:

- total_requests: total number of unique requests
- unique_clients: number of distinct client identifiers
- top_pages: the five most requested URL paths ordered by request count descending
- hourly_traffic: request counts grouped by UTC hour
- error_rate: percentage of requests with HTTP status codes >= 400

Each log entry contains:
- request_id
- client identifier
- timestamp with timezone offset
- HTTP method
- URL path
- HTTP status code
- user agent

Important requirements:

1. Requests with the same request_id represent retries of the same request and must only be counted once.

2. Convert all timestamps to UTC before calculating hourly traffic.

3. The parser must correctly handle quoted fields containing escaped characters.

4. The generated report must follow the required JSON structure exactly.

The output file must be created at:

/app/report.json
