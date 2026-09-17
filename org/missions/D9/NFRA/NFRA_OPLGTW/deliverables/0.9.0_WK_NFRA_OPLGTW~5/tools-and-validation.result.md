# NFRA_OPLGTW.TO-OG-q-2: the five Schwab tools, request validation, envelope and cursors (worker result)

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` | **Branch:** `wk-nfra_oplgtw-5e` in `/c/tmp/wk-oplgtw-5e`, fast-forwarded to
`CLOUD @2bb51e2cd0` | **Build commit (this re-hand):** `f089d91a69` (LOCAL, not pushed) | **Prior build commit:**
`c3728d6bdb` (merged @6a7e9f6caf, per the issuer's hand-off context) | **Interpreter:** `.venv-og`, Python 3.12.10
with `--system-site-packages` (mcp 1.28.0, duckdb 1.2.2, pyarrow 18.1.0, pytest 9.0.2).

## Verdict

**All 29 of 29 mechanical criteria PASS by output.** `<status>` flipped to `complete`.

This is the R-OG-11 re-hand. `1.0.0_SA_CTO` ruling msg 97596 (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/RULINGS_NFRA_OPLGTW_20260916.md` @c858a5f239) vacated R-OG-10 and re-cut
OGQ2-AC26 as a byte-identity check instead of a five-added-entries diff, and added OGQ2-AC27..AC29. The prior AC26
(diff-of-five-entries) could not be met as written because the cut base already classified all five tools (row
`NFRA_OPLGTW-W5-S4`, BLOCKING on that superseded criterion, now historical) -- exactly what the ruling fixed.

- **AC1-AC24** (`test_schwab_query.py`): re-run individually at HEAD `f089d91a69`; all `1 passed`. Unchanged from the
  original build.
- **AC25** (`test_data_entitlement_guard.py -m "not live"`): `12 passed in 13.58s`.
- **AC26** (re-cut, `probes/og_q2.py AC26`): `app/data_entitlement.py` at HEAD -- blob
  `b543f9279412ff514c58af84881c45263859a9d9` -- is byte-identical to its blob at `d88cd32d0c` (OG-z-1's commit). The
  file is genuinely untouched: `git status --porcelain` on it is empty and `git diff d88cd32d0c -- <file>` is empty.
  `VERDICT: PASS-OGQ2-AC26`.
- **AC27** (new, `probes/og_q2.py AC27`): `org/standards/NFRA_OPLGTW_CONTRACT.json` now carries `tool_operations`
  with exactly the 5 contract tools as keys, values in `operations` or `null`, null only on `schwab_get_access`;
  `operations` and `disabled_operations` are unchanged from the cut base `0fc7c71160`. `VERDICT: PASS-OGQ2-AC27`.
- **AC28** (new test, `test_ogq2_ac28`): `data_entitlement.SCHWAB_TOOLS` and `integration.TOOL_OPERATION` each equal
  the contract's `tool_operations`; the test prints denominator 5. `1 passed`.
- **AC29** (new, mutant control, `probes/og_q2.py AC29`): three pytest subprocess runs of `test_ogq2_ac28` -- one
  clean (`rc=0`), one with `TOOL_OPERATION`'s first value replaced in the child process only (`rc=1`), one with
  `SCHWAB_TOOLS`'s first value replaced the same way (`rc=1`). Neither source file was written; the mutation is
  injected via a throwaway pytest plugin on `PYTHONPATH`, confirmed by `git status --porcelain` staying clean on
  both files through the run. `VERDICT: PASS-OGQ2-AC29`.

`app/data_entitlement.py` was **not edited** on this re-hand, per the ruling: `SCHWAB_TOOLS`, `OPERATIONS`,
`allowed_tools()` and the admin command's allowed set are all unchanged from `d88cd32d0c`. The contract gained only
the `tool_operations` key; `contract_version` stays `1.0` (left for `OG-i-5` to bump to 1.1, per the ruling).

## Criteria, each run exactly as written at HEAD f089d91a69 (WS = /c/tmp/wk-oplgtw-5e)

| id | invocation | rc | deciding output |
|---|---|---|---|
| OGQ2-AC1..AC24 | `timeout 120 .venv-og/Scripts/python -m pytest infra/aws/ec2/opal-gateway/tests/test_schwab_query.py::test_ogq2_ac<nn> -q -p no:cacheprovider --color=no` | 0 (24 of 24) | `1 passed` each (1.03s .. 5.04s) |
| OGQ2-AC25 | `timeout 300 ... -m pytest infra/aws/ec2/opal-gateway/tests/test_data_entitlement_guard.py -q -p no:cacheprovider --color=no -m "not live"` | 0 | `12 passed in 13.58s` |
| OGQ2-AC26 | `timeout 120 .venv-og/Scripts/python .../probes/og_q2.py AC26` | 0 | `VERDICT: PASS-OGQ2-AC26` (HEAD blob == d88cd32d0c blob, both `b543f9279412ff514c58af84881c45263859a9d9`) |
| OGQ2-AC27 | `timeout 120 .venv-og/Scripts/python .../probes/og_q2.py AC27` | 0 | `VERDICT: PASS-OGQ2-AC27` (denominator 5; operations/disabled_operations unchanged) |
| OGQ2-AC28 | `timeout 120 .venv-og/Scripts/python -m pytest .../test_schwab_query.py::test_ogq2_ac28 -q -p no:cacheprovider --color=no -s` | 0 | `1 passed in 0.81s`; denominator 5 printed |
| OGQ2-AC29 | `timeout 180 .venv-og/Scripts/python .../probes/og_q2.py AC29` | 0 | `VERDICT: PASS-OGQ2-AC29` (rc 0 / 1 / 1 across the three runs) |

The per-criterion output is in the proof instance beside this file. Deciding values the tests printed (whole-file
`-s` run, this re-hand):
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
- AC28: contract `tool_operations`, `data_entitlement.SCHWAB_TOOLS` and `integration.TOOL_OPERATION` all print the
  same 5-entry mapping with `schwab_get_access: None`.

## Controls

- **Mutants (original build, unaffected by this re-hand).** `CursorCodec.open` skipping the HMAC comparison: AC19
  went rc=1. Dropping the grant re-read before the cache write: AC21 went rc=1. Both files were restored with sha256
  equal before and after.
- **Mutant control (this re-hand, AC29).** `TOOL_OPERATION` and `SCHWAB_TOOLS` each mutated one value at a time, in
  a child process only, via an injected pytest plugin -- never on disk. Both mutated runs FAIL; the unmutated run
  PASSES. See AC29 above.
- **Determinism.** Every AC1-AC25 criterion re-run individually at this re-hand's HEAD; all pass. Whole-file run:
  `25 passed in 11.80s`. AC26/AC27/AC29 probes each run twice with identical verdicts both times.
- **Commit gate.** `OK: pre-commit gate clean for 2 of 3 file(s)` (the 3rd, the contract JSON, is outside the
  Python-only gate's graded set; `rc=0` overall).

## Surprise rows

- `NFRA_OPLGTW-W5-S4` (superseded, INERT): the pre-R-OG-11 AC26 could not be met as written; the ruling's re-cut is
  what this instance now passes. Historical, not re-filed.
- `NFRA_OPLGTW-W5-S5` (OBSERVATION, INERT): `dim_asset` data refuses UNAVAILABLE until OG-q-3's asset policy exists.
  Unchanged on this re-hand.
- `NFRA_OPLGTW-W5-S6` (OBSERVATION, INERT): the 500-row cap counts rows in both representations, so a page holds at
  most 250 rows. Unchanged on this re-hand.
- `NFRA_OPLGTW-S22` (OBSERVATION, INERT): the COO's row naming the R-OG-10 gap that R-OG-11 resolved.
- No new surprise row filed on this re-hand: the R-OG-11 work went exactly as the order describes.

## Exclusions

- The ticket issuer belongs to OG-x-1.
- The `dim_asset` policy and the measured descriptions belong to OG-q-3.
- The criterion tests run OG-q-1's job function in-process, not in its child process.
- `contract_version` stays at 1.0; `OG-i-5` bumps it to 1.1 per the ruling.
- Nothing was deployed and no AWS or vendor endpoint was called.
