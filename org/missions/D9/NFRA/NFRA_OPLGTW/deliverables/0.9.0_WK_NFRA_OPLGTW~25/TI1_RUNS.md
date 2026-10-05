# TI1_RUNS -- OG-ti-1: the schwab test set in ONE pytest process

Directory: infra/aws/ec2/opal-gateway. Selector: `-k schwab`. Baseline failure: tests/test_schwab_export_stream.py::test_ogx4_ac03
(unchanged, per r17/Q7_SUITE_BASELINE.txt). Collected total unchanged at 134 (no test deleted, skipped or xfailed).

Before (CLOUD 4e84fd3f2e, one process): 1 failed, 122 passed, 11 errors (134 collected).

| Run | Command (abridged) | Result |
|-----|--------------------|--------|
| 1 default | `python -m pytest tests -k schwab -q -p no:cacheprovider -rfE` | 1 failed, 133 passed, 0 errors (179.25s) |
| 2 no randomly | same with `-p no:randomly` | 1 failed, 133 passed, 0 errors (144.96s) |
| 3 reversed file order | `-p no:randomly` with the test files listed in reverse-sorted order | 1 failed, 133 passed, 0 errors (162.48s) |

Every run: the only failure is `FAILED tests\test_schwab_export_stream.py::test_ogx4_ac03` (baseline).

Fixes (tests only): tests/conftest.py gained a module-scoped autouse fixture that clears the StreamableHTTP session
manager's once-only `_has_started` flag when no run is live; tests/test_schwab_rl5_asset_query.py now makes the integration
read the module-level service afresh (class-level monkeypatch of `SchwabIntegration.service`, restored at teardown).
