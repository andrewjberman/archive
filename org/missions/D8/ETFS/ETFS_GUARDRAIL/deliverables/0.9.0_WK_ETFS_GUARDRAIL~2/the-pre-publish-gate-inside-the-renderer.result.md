# EG-s-6 result -- the pre-publish gate INSIDE the renderer, and the ONE artifact upload

**TO:** `ETFS_GUARDRAIL.TO-EG-s-6` | **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~2` | **Source (edited):**
`data/etfs/scripts/presentation/render_month_end.py`. **Read-only, imported/invoked:**
`data/etfs/scripts/coverage/` (classifier.py EG-s-4, remediate.py EG-s-7/EG-sb-7), the three
producers (cot/bd-49f/inf-etf-ownership-daily). Not edited: the orchestrator
(`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`, EG-s-8's cell).

---

## 1. Where the gate lives (line numbers, at HEAD after this order's edit)

- `_PROBE_CAPABLE_PARTNERS` (cottonwood, 49financial only -- see s.4 below): `:827-830`.
- `_parse_fixture_remove`: `:833-838`.
- `_make_probe` (classify_month's injected probe, real `lam.invoke`, tests stub it): `:841-865`.
- `_make_invoke` (remediate_month's rung-1 invoke): `:871-885`.
- `coverage_gate` (the gate itself -- classify, remediate (if `ladder`), re-classify, verdict): `:890-949`.
- Self-bootstrap for the box layout (`from coverage import classifier, remediate` with an
  `except ImportError:` pull-and-retry): `:80-102` (module top, alongside the existing Orion
  import).
- `main()`'s `--gate`/`--no-ladder`/`--fixture-remove` argparse flags and the gate call site:
  `:998-1010` (flags), `:1023-1073` (the gate branch: verdict compute, artifact writes,
  REFUSE upload + `sys.exit(3)`, PUBLISH fall-through).

## 2. Acceptance criteria, verbatim with rc and denominator

### S6-AC1 -- the six-arm battery is green

```
......                                                                   [100%]
6 passed in 1.38s
```
rc=0. Denominator: 6 of 6 arms passed (a-f). **PASS.**
Sanity (not itself a criterion): all 15 sibling tests in `data/etfs/scripts/presentation/tests/`
(orion_alignment 5 + coverage_line 4 + coverage_gate 6) still pass together, rc=0.

### S6-AC2 -- property 3 first half: pre-09-01-repair August REFUSES with exactly 5 holes

```
OK: 2026-08 -> .scratch/eg_s6_pre_repair.html
OK: CSV -> .../opaletfs_49financial_202608.csv
OK: CSV -> .../opaletfs_inflection_202608.csv
OK: CSV -> .../opaletfs_cottonwood_202608.csv
VERDICT: REFUSE holes=5
rc=3
```
The probe answered from the DEPLOYED `cot-etf-ownership-daily` producer's real probe mode
(EG-s-1) for each of the 5 removed dates -- a genuine live `lambda:InvokeFunction` call per
date, 5 total, classifying each as C (upstream ready, priced, never fired). **PASS.**

### S6-AC3 -- property 3 second half: current August PUBLISHES

```
OK: 2026-08 -> .scratch/s6_now/eg_s6_now.html
...
VERDICT: PUBLISH holes=0
rc=0
```
No `--s3-out` was passed -- per this order's own design, the gate's S3 writes (verdict/
unresolved/refused-upload) are conditioned on `--s3-out`, matching the CLI's existing
publish-upload gating; nothing was uploaded by this QA run. Zero probe invokes fired (every
trading day for all three partners was already COVERED -- classify_month's `date_str in
series` check short-circuits before ever calling `probe`). **PASS.**

### S6-AC4 -- the refused deck still carries every partner's coverage line

```
COVERAGE_LINES_ON_REFUSE=3
```
Denominator: 3 of 3 present partners. The three live lines on the refused deck:
```
49 Financial -> 21/21 trading days; 0 carried for missing data
Cottonwood   -> 16/21 trading days; 5 carried for missing data
Inflection   -> 21/21 trading days; 0 carried for missing data
```
And the matching CSV last row for cottonwood (the fixture-modified partner):
```
# coverage: 16/21 trading days; 5 carried for missing data
```
**PASS.**

### S6-AC5 -- the commit gate is clean

```
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 2 of 2 file(s)
```
rc=0. **PASS.**

### S6-AC6 -- the 6 uploaded artifacts match their local sources, 6 of 6

```
PAIR ec2/etfs-reports/render_month_end.py           local_md5=9f7bbe4a3d5e73c8c065b9844a41d262 served_etag=9f7bbe4a3d5e73c8c065b9844a41d262 MATCH
PAIR ec2/etfs-reports/coverage/__init__.py          local_md5=477c6d83d39c067a13b2bd56bb9840a0 served_etag=477c6d83d39c067a13b2bd56bb9840a0 MATCH
PAIR ec2/etfs-reports/coverage/classifier.py        local_md5=8818cb93b256fa4502a6b4ef7e69409e served_etag=8818cb93b256fa4502a6b4ef7e69409e MATCH
PAIR ec2/etfs-reports/coverage/remediate.py         local_md5=5bdae45804c6b6896cccc48e4bf5c2e5 served_etag=5bdae45804c6b6896cccc48e4bf5c2e5 MATCH
PAIR ec2/etfs-reports/coverage/trading_calendar.py  local_md5=3de6a337e268614698943b038248113b served_etag=3de6a337e268614698943b038248113b MATCH
PAIR ec2/etfs-reports/coverage/_orion_vendor_asof.py local_md5=2a6134275b957bc82b5dc3510658b2fb served_etag=2a6134275b957bc82b5dc3510658b2fb MATCH
VERDICT: MATCH 6 of 6
```
rc=0. Every ETag == local md5 (single-part uploads, well under the 8 MiB multipart
threshold, so ETag == md5 is the correct equality). **PASS.**

### S6-AC7 -- the coverage package is at the box's pull prefix

```
ec2/etfs-reports/coverage/__init__.py	ec2/etfs-reports/coverage/_orion_vendor_asof.py	ec2/etfs-reports/coverage/classifier.py	ec2/etfs-reports/coverage/remediate.py	ec2/etfs-reports/coverage/trading_calendar.py
```
`ec2/etfs-reports/coverage/classifier.py` present, matching the expectation. **PASS.**

### S6-AC8 -- judgment, RECORD; NO VERDICT

The gate is a render precondition, not a standing service: `coverage_gate` is one function
called once per `--gate` invocation of `render_month_end.py`, holding no state between runs,
starting no schedule, listener, or process of its own. Catch-up runs BEFORE the gate by
construction: the reporting-obligation catch-up ports (EG-s-1 cot, EG-s-2 bd-49f) run on the
PRODUCERS' own daily schedules, entirely independent of and prior to this renderer's monthly
fire; this order neither triggers nor depends on triggering them -- it only reads their
CURRENT state (via probe) and, when `ladder=True`, re-runs them for specific dates (rung 1).
The ladder runs INSIDE the gate (rungs 0-2 via `remediate.remediate_month`; rung 3's ask,
`EG-sb-7`'s own artifact, fires from inside `remediate_month` when `unresolved` remains
non-empty and `ladder=True`). A REFUSE writes NO report at the publish key (confirmed:
`test_d_refuse_writes_verdict_artifact_not_publish_key` asserts no `etf_ownership.pdf` key
among the S3 puts) and surfaces on the EXISTING topic through the orchestrator's OWN
pre-existing branch (`_run`'s `if status != "Success": _alert(...)` at
`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:310-314`, read but not
edited) -- `sys.exit(3)` makes the SSM command status `Failed`, which that branch already
catches; no orchestrator change was needed or made. B is never a hole: `coverage_gate`'s own
`holes` computation (`:937`) and the verdict gate (`:938`, `if summary["C"] > 0`) both
exclude B by construction, matching `classifier.summarize`'s own `holes = C + UNKNOWN + D`.
FWD-2's EXERCISED grade ("has actually refused a month, and the refusal reached a person")
is a real refusal on a scheduled fire -- this order rehearses that exact mechanism on the
pre-09-01-repair fixture (S6-AC2) and does not manufacture a live refusal itself, per the
BOUNDS ("No probe in the QA runs beyond the deployed producers' probe mode... `--no-ladder`
on every QA run").

---

## 3. THE DEPLOY -- the ONE artifact upload, ledger, hashes

| step | invocation | result |
|---|---|---|
| commit source | `safe-commit.sh` (render_month_end.py, test_coverage_gate.py, surprise row) | `7cd25f5998` |
| compile-check | `py_compile` on all 6 files to be uploaded | `All 6 files pass py_compile.` |
| ledger open | `deploy_ledger.py open --slug etfs-guardrail-eg-s-6-renderer-artifact-upload --leg "s3-code\|activation\|ec2/etfs-reports/render_month_end.py\|..."` | 1 leg opened |
| commit ledger open | `safe-commit.sh` | `d0823cd564` |
| upload (6x) | `.tools/aws s3 cp` render_month_end.py, coverage/{__init__,classifier,remediate}.py, lib/trading_calendar.py -> coverage/trading_calendar.py, data/inf/scripts/silver/_orion_vendor_asof.py -> coverage/_orion_vendor_asof.py | 6 of 6 uploads rc=0 |
| verify | see S6-AC6/AC7 | MATCH 6 of 6; prefix listing confirms classifier.py present |
| close-leg | `deploy_ledger.py close-leg --leg-id s3-code --proof "..."` | leg closed |
| close | `deploy_ledger.py close --slug etfs-guardrail-eg-s-6-renderer-artifact-upload` | `CLOSED ... all 1 legs proven` |
| commit ledger close | `safe-commit.sh` (excluding the ambient .tf eol-only noise the issuer flagged) | `4cc172fe3d` |

**Entry:** `org/critical_paths/change_management/20260905T0644Z_etfs-guardrail-eg-s-6-renderer-artifact-upload_deploy_completion.md`
-- CLOSED, not merely committed. No leg left open.

**The scheduled 10-01 fire is the EXERCISED read** (FWD-2's own DONE-WHEN bar) -- this order
lands the artifact and proves it byte-identical on the box's pull prefix; it does not
manufacture that fire.

---

## 4. Bounds honored

- No fabrication: the gate writes verdict/unresolved/ask artifacts and the refused HTML/CSVs;
  it never writes a slice or a number. `--fixture-remove` was verified to change memory only
  (nothing on S3 is touched by it -- confirmed by S6-AC2/AC3's own live runs never differing
  in which S3 objects exist, only in what the in-memory series contained).
- No probe beyond the deployed producers' probe mode: `_PROBE_CAPABLE_PARTNERS` names ONLY
  cottonwood and 49financial (see the surprise row below for why Inflection is excluded);
  every QA run in this order used `--no-ladder`, making zero rung-1 invokes (S6-AC1 arm (f)
  and the module docstring's own accounting).
- No served delete: nothing under `platinum/reports/` or `daily/` was ever deleted by this
  order's code or its live runs (only `put_object` calls exist in the gate's write paths).
- NEVER-2 for the upload: ledger entry opened before, proof supplied after, both committed;
  `.tools/aws` shim used for every upload and list call; every upload OVERWROTE the existing
  key at that prefix (an ordinary `s3 cp`, no `--delete`), nothing was deleted.
- No new monitor/alarm/topic/schedule: the refusal rides the orchestrator's EXISTING
  `REPORTS_SNS_TOPIC` alert branch, read but not edited.

## 5. Push state (measured)

See the WORKER REPORT for the value read at report time.
