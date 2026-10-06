# TI2_RUNS -- OG-ti-2: the schwab test set in ONE pytest process, without the reset seam

Directory: infra/aws/ec2/opal-gateway. Baseline failure (unchanged, r17/Q7_SUITE_BASELINE.txt):
tests/test_schwab_export_stream.py::test_ogx4_ac03. Collected total 138 in every run (137 passed + 1 baseline failure);
no test deleted, skipped or xfailed.

## Fixture design

`tests/conftest.py` no longer touches the session manager (0 references to `_has_started`). Each module that runs the
Gateway app's lifespan (acceptance harness `served_app`, `test_principal_cutover.app_client`,
`test_data_entitlement_guard.served_app`) now calls `tests/fresh_gateway_app.py: fresh_mcp_app(server)` first: FastMCP builds a
NEW StreamableHTTP session manager and a new `/mcp` ASGI app, and the Gateway's `/mcp` mount is pointed at it, so no module
ever reuses another module's once-only manager. The `og_v2` harness fixture also replaces `SchwabIntegration.service` with a
read of the module-level `default_service()` (monkeypatch, restored at teardown), so every og_v2 test reads a fresh service
and not the integration instance's first-built cache (the rl5-only class patch was removed). `tests/conftest.py` also sets
`ENABLED_INTEGRATIONS=schwab` by `setdefault` before any test module is collected: app.config freezes that list at first
import, and yearinreview imports app.config first in a subset run, which left the schwab tools unregistered (q7's
`Unknown tool: schwab_prepare_download`).

## Runs

Before (this tree, S40 subset, one process, first failure shown with -x): `test_ogq7_ac01` FAILED `Unknown tool: schwab_prepare_download`.

| Run | Command (abridged) | Result |
|-----|--------------------|--------|
| 1 default order | `python -m pytest tests -k schwab -q -p no:cacheprovider -rfE` | 1 failed, 137 passed, 0 errors (177.01s) |
| 2 no randomly | same with `-p no:randomly` | 1 failed, 137 passed, 0 errors (148.85s; re-run alone, see note) |
| 3 reversed file order | `-p no:randomly` with `tests/test_*.py` listed in reverse-sorted order | 1 failed, 137 passed, 0 errors (178.12s) |
| S40 subset | yearinreview, q7 download, rl5 asset query, schwab_query, grain_r9, `test_entitlement_admin.py::test_ogz2_ac08`, one process | 48 passed, 0 failed, 0 errors (24.90s) |

Every whole-set run: the only failure is `FAILED tests\test_schwab_export_stream.py::test_ogx4_ac03` (baseline).
Note: runs 1-3 were first started concurrently; run 2 then also failed `test_ogx1_ac27` (FileNotFoundError on a shared export
directory under the temp dir) and was re-run alone with the result above. Filed as row NFRA_OPLGTW-Z-W25-S3.
