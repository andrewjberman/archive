# FB-m-1 readiness signal -- BLOCKED, no object chosen (2026-10-14)

Machine record: `READINESS_SIGNAL.json` in this folder (`chosen: null`, `claim: measured`).

## Result

No object in `opal-data-inf` meets the order's criteria (chain-written, carries the gold date, single writer, survives the marker's retirement, not the two excluded sentinels) without conflicting with a governing rule. The order's STOP branch applies: no guard, no test file, no dispatch edit. The blocking row is `ADVI_FIRMBKTS-D1-W84-S1` in the investigation file.

## Candidates rejected

| key | why it fails |
|---|---|
| `gold/meta/pipeline-complete.json` | the Door 6 marker being retired (excluded by the order) |
| `gold/meta/pull-complete.json` | written before compute (`orion-gold-dispatch.sh:1879`) |
| `gold/meta/pipeline-failed.json` | failure-only; a success does not clear it (last modified 2026-09-30) |
| `gold/artifacts/header_metrics.json` | HeadObject 404 today; its `data_as_of` is holdings vintage, not run date |
| `gold/eclipse/_meta/dispatch_eclipse_status.json` | meets the literal fields (`run_date`, `chain`, `chain_exit`; single writer `:2027`) but is a sidecar state object the MDPF remediation register classes as TRASH when read as a gate (`docs/architecture/MDPF_REMEDIATION_REGISTER.md:198`, `:226`); it is written after the best-effort eclipse steps, and the dispatch records the 2026-05-15 directive that eclipse must not gate portal updates (`:1988-1990`) |
| `gold/perf_report.json` | one overwritten key written even on failure (`:1852-1856`), the same sidecar class |
| `gold/artifacts/{id}/{RUN_DATE}` markers | written only under `SKIP_EXISTING` (`:741-743`) |
| `gold/manifests/`, `gold/logs/` | no per-run chain manifest; logs upload on crash as well |
| INF_D_10 output | the last step performs S3 reads only |

## Date the guard would check

`orion-gold-dispatch.sh:71`: `RUN_DATE=$(date -u +%Y-%m-%d)`, overridden by `--run-date` at `:1356`. The Lambda must use the UTC date.

## What the guard would do on each arm

Not implemented. The intended behaviour, once a signal is chosen: signal date equal to the expected date and ready, so the handler proceeds as today; any other date, an absent object, or a read error, so the handler prints one `READINESS HALT` line and returns `halted: True` with zero writes.

## Decision needed from the CTO

1. A new run-dated object written by the chain (a dispatch edit, outside this order's paths).
2. A data-frontier read in the publisher, as the register prescribes, which needs a calendar decision because the Lambda cannot import `lib/trading_calendar.py`.
3. A ruling that the eclipse status is admissible despite the register line.
