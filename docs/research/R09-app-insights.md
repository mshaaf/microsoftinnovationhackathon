# R09: Application Insights without PII

## Answer
- Package: `azure-monitor-opentelemetry`. Call `configure_azure_monitor(connection_string=...)` **before** importing `fastapi.FastAPI`, or the requests table stays empty (documented FastAPI gotcha). Only in live mode, and only when `APPLICATIONINSIGHTS_CONNECTION_STRING` is set.
- **Request bodies aren't captured** by the Python HTTP instrumentation by default. URLs and query strings are. Our query strings carry only state, county FIPS, and lang, none of which are personal. Never put user text in a URL.
- The distro exports Python `logging` records, so our redaction filter must sit on the **root logger** before `configure_azure_monitor` runs. Log categories and counts only.
- Add a span processor that drops any attribute whose key contains `body`, `content`, or `prompt`. It's one small class. Belt and braces.
- Verify at Gate 3: search App Insights logs for L01's fake name. Expect zero hits.

## Evidence
- https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-configuration
- https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-filter
- https://learn.microsoft.com/en-us/troubleshoot/azure/azure-monitor/app-insights/telemetry/opentelemetry-troubleshooting-python

## Impact
P3-04, backend `core/logging.py` (P0-04).
