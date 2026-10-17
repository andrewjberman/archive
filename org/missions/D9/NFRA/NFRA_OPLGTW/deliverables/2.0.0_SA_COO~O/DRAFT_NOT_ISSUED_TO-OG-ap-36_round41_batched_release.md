# DRAFT, NOT ISSUED -- `OG-ap-36`: the round-41 batched gateway release (items 1 to 3 of the CTO's round-40 analysis)

**Status:** a design note written by `2.0.0_SA_COO~O` at ~09:4xZ on 2026-10-17 WHILE `OG-en-21`, `OG-en-22` and `OG-db-3` are building. It is NOT a task order (no `<status>`, no gate-checked blocks). It is cut as an order, with its own check scripts dry-run at the base, only AFTER the three builds merge and their real diffs are known (the lesson of `OG-ap-33`: an order written against an imagined diff stops on the real one).

## What the release carries (from the CTO's round-40 analysis, `ledger/ROUND_ANALYSIS.round40.md` @66aeb73b0c)

1. `OG-en-21`: the windowed client tools run in a worker thread (`app/tools.py`).
2. `OG-en-22`: the served prefix is listed once per page (`app/client_core.py`, `app/client_adapter_bd49f.py`).
3. `OG-db-3`: the deploy writes `/opt/opal-gateway/.deployed_commit` (`deploy-to-ec2.sh`), and with it `OG-db-2`'s 17-line preflight (already on trunk, never yet deployed).

The release is cut on the LIVE ref (read `deployed_commit` at the cut; `9d5b712557` today), code only, no Terraform, no IAM, no env key, no manifest change, one deploy, under its own never-widen (three halves: CTO, COO, CVO). The CTO's rule: item 1 ships in a batched release under its own never-widen.

## Phase A (read, re-cut, gate, ask) -- additions to the `OG-ap-34` shape

- The take list is the union of the `<paths>` of the complete orders (app files and tests only, plus `deploy-to-ec2.sh`). Taking trunk's `app/tools.py` carries the POSITION move of `harvest_get_published_analysis` that `OG-ap-33` landed on trunk (the same lines, a different order than live) besides `OG-en-21`'s change; the ask attributes every hunk to `OG-en-21`, to the move (position only, each name exactly once) or to the live ref's own, and a hunk it cannot attribute is a STOP. Taking trunk's `deploy-to-ec2.sh` carries `OG-db-2` and `OG-db-3` only.
- `destructive_ops.py`, `EC2_MANIFEST.json`, Terraform and the registry files are NOT in the diff (the check counts them).
- **Memory gate (kept from `OG-ap-34`):** the candidate code's four-page chain in a fresh process on the host: median RSS growth 20 MB per page or less, host peak under 75 percent. The CTO's plateau test (two full chains in one fresh process, second chain net growth 50 MB or less, host under 80 percent, no page over 55 s) is run again.
- **Page wall time BEFORE and AFTER item 2 on the same 13-month window** (CTO criterion): the live code's first page and the candidate's first page, same account, same cursor, one call at a time, wall seconds recorded for both; the candidate's must be shorter (the listing was about 0.4 of each partition read's 0.55 s).
- **Byte equality:** every page of the candidate's chain equals the live code's chain row for row (counts and a hash of the canonical rows per page; no row content printed).
- **Health during a page (item 1):** with a full page running in a fresh process using the candidate's tool wrapper, an HTTP-style health read answers in under 1 s.

## Phase B -- additions

- Triggers as `OG-ap-34` plus: health not 200 within 1 s for three probes taken BETWEEN pages of a chain (never mid-page) is not a trigger (the page may still hold the worker), but `/health` slower than 5 s DURING a page IS (item 1 failed).
- After the deploy: `cat /opt/opal-gateway/.deployed_commit` on the host equals the release sha (CTO criterion for item 3).
- Arms (all one call at a time, a stand-in in-process as before): `e1_cursor_first_page` (30 partitions, a non-null cursor, wall under the live code's), `e1_cursor_pages_to_window_start`, `e1_within_page_newest_first`, `e1_cursor_by_partition`, `e8_memory_flat_and_returned`, `e9_health_answers_during_a_page`, `e10_marker_equals_release_sha`, `e11_pages_equal_live_code_row_for_row`.
- The 30-minute service read-back every 60 s and its triggers (host over 80 percent, service +700 MB over its baseline, median growth over 20 MB per call after the first) stay, and the report counts the `/mcp` window calls served and says plainly if the count is zero (the CTO's amendment 2).
- Z-S338 is re-read on this release's own deploy (the CTO's round-40 analysis).

## Checks to write at the cut (each dry-run at the base first)

`ap36.AC1` (Phase A) from `ap34.AC1.sh`: the allowed set gains `app/tools.py`, `app/client_core.py` and `deploy-to-ec2.sh` and keeps the others; only `destructive_ops.py`, the manifest, Terraform, registry and data copies are counted at 0; the memory gate and plateau record are checked; the before and after page walls are recorded with after < before; the byte-equality record. `ap36.AC2` (Phase B) from `ap34.AC2.sh` with the new arms and the marker equality.

## Why this is a note and not an order yet

The order's `<paths>` and criteria name exact files, a take list and check scripts; all of those depend on the merged builds. Cutting it now would make the next applier stop on a stale premise again.
