# NFRA_OPLGTW.TO-OG-q-2: the five Schwab tools, request validation, envelope and cursors (worker result)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` | **Branch:** `wk-nfra_oplgtw-1-5d` in `/c/tmp/wk-oplgtw-1-5d`, cut from `CLOUD` at
`0fc7c71160` | **Build commit:** `c3728d6bdb` (LOCAL, not pushed) | **Interpreter:** `.venv-og`, Python 3.12.10 with
`--system-site-packages`, built fresh from `requirements.txt` + `msal moto pytest` (mcp 1.28.0, duckdb 1.2.2,
pyarrow 18.1.0, pytest 9.0.2).

## Verdict

25 of 26 mechanical criteria PASS by output. **OGQ2-AC26 FAILS and is refused as written.** The order stays open and
its `<status>` is not flipped. None of the criteria is marked `judgment="true"`.

OGQ2-AC26 requires `app/data_entitlement.py` to differ from the cut base by exactly five added entries. The cut base
already classifies all five contract tools: `SCHWAB_TOOLS` at `:75-81` and `TOOL_CLASSES` at `:103`, both
@`0fc7c71160`, were put there by OG-z-1 (row W3-S23). `schwab_get_access` also has no contract operation class. Adding
five more lines would duplicate or override entries that already exist, and the order says an unclear class is a
surprise row, not an entry. So the file is unchanged. The probe reads `0 added line(s), 0 removed line(s)` and prints
`VERDICT: FAIL-OGQ2-AC26`. The probe itself discriminates: given a synthetic five-entry diff it prints PASS (rc 0), and
given the same diff plus one removed line it prints FAIL (rc 1). Row `NFRA_OPLGTW-W5-S4`, BLOCKING.

## Criteria, each run exactly as written at HEAD c3728d6bdb (WS = /c/tmp/wk-oplgtw-1-5d)

| id | invocation | rc | deciding output |
|---|---|---|---|
| OGQ2-AC1..AC24 | `timeout 120 .venv-og/Scripts/python -m pytest infra/aws/ec2/opal-gateway/tests/test_schwab_query.py::test_ogq2_ac<nn> -q -p no:cacheprovider --color=no` | 0 (24 of 24) | `1 passed` each (1.22s .. 6.17s) |
| OGQ2-AC25 | `timeout 300 ... -m pytest infra/aws/ec2/opal-gateway/tests/test_data_entitlement_guard.py -q -p no:cacheprovider --color=no -m "not live"` | 0 | `12 passed in 13.70s` |
| OGQ2-AC26 | `timeout 120 .venv-og/Scripts/python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/probes/og_q2.py AC26` | 1 | `VERDICT: FAIL-OGQ2-AC26 0 added lines, expected exactly 5; 0 of 5 contract tools have an added entry` |

The per-criterion output is in the proof instance beside this file. Deciding values the tests printed (whole-file `-s`
run, before the build commit):
- AC8: 34 payloads x 17 slots = 578 requests, all 578 refused, 0 engine jobs.
- AC14: grouped pages `AAA000001 1700.1700`, `BBB000002 350.0700`, `CCC000003 -30.3000`, with matched 5 on every page;
  the ungrouped total is `2019.9400`.
- AC16: page_size 500 over 700 matched rows returned 151 rows. The measure counted 302 rows (structured + text),
  70340 codepoints and 130740 UTF-8 bytes; the audited planned_bytes was 130740.
- AC21: a revision bump during the job gave SOURCE_CHANGED with 0 releases and 0 cache entries; an unchanged revision
  released 5 rows.
- AC23: 5 of 5 tools released after one acknowledged `release_authorized`. With the sink down, 0 of 5 released and
  0 tickets were issued.
- AC24: with ENABLED_INTEGRATIONS unset, `enabled []` and no schwab tools; with `schwab`, the 5 tools.

## Controls

- **Mutants.** First, `CursorCodec.open` was changed to skip the HMAC comparison: AC19 went rc=1. Second, the grant
  re-read before the cache write was dropped: AC21 went rc=1 because the stale result was cached, although the later
  re-read still refused it. Both files were restored with sha256 equal before and after, and 0 MUTANT lines remain.
- **Determinism.** Before the commit: one run per test, and the whole file once (`24 passed in 11.41s`). The per-test
  run caught a test defect in AC22 (a json.dumps of tuple keys), which was fixed first. At the committed bytes: the
  recorded run above.
- **Commit gate.** `OK: pre-commit gate clean for 7 of 7 file(s)`.

## Surprise rows

- `NFRA_OPLGTW-W5-S4` (BLOCKING, INERT): OGQ2-AC26 cannot be met as written.
- `NFRA_OPLGTW-W5-S5` (OBSERVATION, INERT): `dim_asset` data refuses UNAVAILABLE until OG-q-3's asset policy exists.
  The schema and grains are declared, not measured.
- `NFRA_OPLGTW-W5-S6` (OBSERVATION, INERT): the 500-row cap counts rows in both representations, so a page holds at
  most 250 rows.

## Exclusions

- The ticket issuer belongs to OG-x-1.
- The `dim_asset` policy and the measured descriptions belong to OG-q-3.
- The criterion tests run OG-q-1's job function in-process, not in its child process.
- Nothing was deployed and no AWS or vendor endpoint was called.
