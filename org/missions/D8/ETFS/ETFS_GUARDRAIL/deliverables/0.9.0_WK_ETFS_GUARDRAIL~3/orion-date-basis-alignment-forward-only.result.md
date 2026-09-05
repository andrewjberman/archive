# ETFS_GUARDRAIL.TO-EG-s-13 -- orion-date-basis-alignment-forward-only -- result

`0.9.0_WK_ETFS_GUARDRAIL~3`, worktree `C:/Users/AndrewBerman/Desktop/wk-ETFS_GUARDRAIL-3`, branch
`wk-ETFS_GUARDRAIL-3`, based on CLOUD @afa47031ed. Cell `EG-s-13`.

## Re-grounding (before any edit)

`git rev-parse --abbrev-ref HEAD` -> `wk-ETFS_GUARDRAIL-3`; `test -d org && test -d .tools` ->
`TREE-OK`. TO's `<status>` line premises re-read: PRD v0.3 @`4e30d6b635`, decomposition v0.1.1
@`5376ecaa8b` (the issuance commit that carries this TO) -- both present at HEAD, matched verbatim
against the TO file's own copy.

`orion_normalize_as_of` read at `data/inf/scripts/silver/_orion_vendor_asof.py:128-139`:
`orion_normalize_as_of(labeled_max: date) -> date` returns `prior_trading_day(labeled_max)` --
LABEL-ONLY (never touches values), ORION-ONLY (never call on schwab/bd), stdlib-`datetime`-only
(py3.9-safe, no runner dependency), NYSE closed-dates hardcoded 2025-2027. `render_month_end.py`
confirmed CALLED 0 times under `data/etfs/` before this order (grep against the pre-edit file).

**Where the alignment lands, confirmed by reading the file, not assumed:** `render_month()`
(`:365+`) builds `daily[p]` once per partner via `load_all_daily(p)` and that ONE dict feeds
`_carry_forward_avg`, the month/hist date functions, the charts and the matrix -- confirmed by a
census of every `daily[p]` reference (`grep -n 'daily\['`, 13 hits, all inside `render_month`).
**Surprise (`ETFS_GUARDRAIL-W3-S1`):** the CSVs are NOT produced from that same `daily` dict --
`write_month_csvs(month, out_dir)` is a SEPARATE function with its OWN independent
`load_all_daily(partner)` call per partner, invoked directly from `main()` alongside (not through)
`render_month`. A call wired only inside `render_month`, as the deliverable's call-site sentence
describes, would leave the CSVs on the raw Orion label. Filed and disarmed same-turn: the
alignment is ALSO wired into `write_month_csvs` (below), so the outcome the deliverable actually
states -- "every artifact the month produces shares the one date basis" -- holds for real,
including the CSVs the literal call-site text did not reach.

## What was built

1. **Import (self-bootstrap, `render_month_end.py:57-78`):** primary attempt inserts
   `data/inf/scripts/silver` onto `sys.path` and imports `orion_normalize_as_of` from
   `_orion_vendor_asof` (the repo checkout carries `data/inf/`, so this is what resolves on this
   box and in QA -- verified: `inspect.getsourcefile` resolves to
   `data/inf/scripts/silver/_orion_vendor_asof.py`). On `ImportError` (the EC2 reporter box, which
   EG-s-6's self-bootstrap pulls `render_month_end.py` + `coverage/*.py` onto and never
   `data/inf/`), falls back to a byte-identical vendored copy at
   `data/etfs/scripts/coverage/_orion_vendor_asof.py`. **sha256, both files:**
   `15d28dd8444455e5d4143dca4c62adea109aeb4b50a3ee4e99af0b54890e6f72` (identical; `diff` empty).
   Its imports are `from __future__ import annotations` + `datetime` only (stated in its own
   docstring: "stdlib datetime only, no new runner dependency"), so it runs standalone under
   `coverage/` with no further vendoring. **Fallback verified live**, not just read: copied
   `render_month_end.py` + the vendored file into an isolated temp tree with NO `data/inf/`
   present and re-imported -- `orion_normalize_as_of.__module__` resolved to the vendored copy's
   path, confirming the `except ImportError` branch engages correctly when the primary lane is
   absent (the box's actual condition, not exercised by AC1-AC5 which all run against the full
   repo checkout where the primary import succeeds).
2. **`ORION_ALIGNMENT_CUTOVER = "2026-09"`** (`:78`) -- module constant, string-compared against
   `month` (`"YYYY-MM"`), so `"2026-08" < "2026-09"` (pre-cutover) and `"2026-09" < "2026-09"` is
   False (cutover itself aligns).
3. **`_align_inflection_series(series, month)`** (`:139-161`): forward-only guard returns
   `series` UNCHANGED (identity, no copy) when `month < ORION_ALIGNMENT_CUTOVER`; otherwise
   iterates `sorted(series)` (ascending raw-date order) and re-keys each entry to
   `orion_normalize_as_of(to_date(raw_d)).isoformat()`, so a LATER raw date's payload overwrites
   an earlier raw date's payload written to the same aligned key -- the mapping decision the TO
   asked to be stated in a comment: **later raw date wins**, because it is the more recent pull of
   that settled day's true count. Values are never read or modified -- LABEL-only, matching the
   source function's own contract.
4. **Wired at two call sites**, both `partner == "inflection"` only, both on the ETFS-only
   (`load_all_daily`) series, never on the `--inf-canonical-preview` diagnostic path:
   - `render_month()` (`:376-382`): right after `daily["inflection"] = load_all_daily(...)`,
     BEFORE `_carry_forward_avg`, `month_dates`/`hist_dates`, the charts and the matrix all read
     `daily`.
   - `write_month_csvs()` (`:696-702`, added beyond the deliverable's literal call-site text to
     close row `ETFS_GUARDRAIL-W3-S1`): right after its own independent
     `series = load_all_daily(partner)`, before `_carried_daily`/the CSV write.

## Acceptance criteria, run verbatim under `timeout 120`

**`S13-AC1`** -- `python -m pytest data/etfs/scripts/presentation/tests/test_orion_alignment.py -q`
```
.....                                                                    [100%]
5 passed in 0.52s
```
rc=0. Denominator: 5 of 5 arms green (a, b, c, d, e -- all five the deliverable names). PASS.

**`S13-AC2`** -- the regex census command (verbatim from the TO):
```
ALIGN_CALLS=1 CUTOVER=2026-09 SECOND_IMPL=0
```
rc=0. Matches `CUTOVER=2026-09 SECOND_IMPL=0` exactly. `ALIGN_CALLS=1`: the literal call
`orion_normalize_as_of(` appears once in the file -- inside `_align_inflection_series`'s own
body, which both call sites (render_month, write_month_csvs) route through; this is the estate's
ONE implementation called (not zero), with no second `def orion_normalize_as_of(` anywhere in
the file. Denominator: 1 of 1 pattern group matched (CUTOVER, SECOND_IMPL); ALIGN_CALLS recorded
per the TO's "at least once; the count is recorded". PASS.

**`S13-AC3`** -- `python data/etfs/scripts/presentation/render_month_end.py --month 2026-09 --out .scratch/eg_s13_sept.html`
```
OK: 2026-09 -> .scratch/eg_s13_sept.html
OK: CSV -> .../.scratch/opaletfs_49financial_202609.csv
OK: CSV -> .../.scratch/opaletfs_inflection_202609.csv
OK: CSV -> .../.scratch/opaletfs_cottonwood_202609.csv
```
rc=0. Matches `OK: 2026-09`. etfs-only reads (no `--inf-canonical-preview`); no `--pdf`, no
`--s3-out` -- local HTML + local CSVs only. Denominator: 1 of 1 render, 3 of 3 partner CSVs
written (no partner skipped for lack of in-month data). PASS.

**`S13-AC4`** -- `python data/etfs/scripts/presentation/render_month_end.py --month 2026-08 --out .scratch/eg_s13_aug.html`
```
OK: 2026-08 -> .scratch/eg_s13_aug.html
OK: CSV -> .../.scratch/opaletfs_49financial_202608.csv
OK: CSV -> .../.scratch/opaletfs_inflection_202608.csv
OK: CSV -> .../.scratch/opaletfs_cottonwood_202608.csv
```
rc=0. Matches `OK: 2026-08`. **One date key from each run, side by side (forward-only proof):**
Inflection's raw daily slice `daily/inflection/2026-09-02.json` (S3, read live) carries
`ownership_value: 18895738.68` for DIVZ under the raw label `2026-09-02`. In the **September**
(aligned, post-cutover) CSV `opaletfs_inflection_202609.csv`, that exact value
(`18895738.68`) appears under column **`2026-09-01`** -- re-labelled to the settled close one
NYSE trading day earlier, value untouched (LABEL-only, confirmed). In the **August**
(pre-cutover, unaligned) CSV `opaletfs_inflection_202608.csv`, the first column is still
**`2026-08-01`** -- the raw key, exactly as it has always rendered; nothing published is
restated. Denominator: 1 of 1 render, 3 of 3 CSVs; 1 value-identity check (raw JSON vs. aligned
CSV cell) confirming label-only re-keying. PASS.

**`S13-AC5`** -- `bash .tools/commit-gate.sh data/etfs/scripts/presentation/render_month_end.py data/etfs/scripts/presentation/tests/test_orion_alignment.py`
```
All checks passed!
OK: no unguarded strict-utf8 log reads.
All checks passed!
OK: no unguarded strict-utf8 log reads.
OK: pre-commit gate clean for 2 of 2 file(s)
```
rc=0. Denominator: 2 of 2 files clean. (At the time of this first run the vendored
`data/etfs/scripts/coverage/_orion_vendor_asof.py` also existed and was separately run through
the same gate: `OK: pre-commit gate clean for 1 of 1 file(s)`, rc=0. That file was later `git
rm`'d per the "Amendment" section below -- see its own re-run of this criterion.) PASS.

**`S13-AC6`** -- judgment="true". RECORD, NO VERDICT. From the cutover month forward the three
partners' series share one date basis: 49F and Cottonwood were always settled-labelled (brief
s.6a); Inflection is now re-keyed at read time in both artifacts the renderer produces (deck +
CSVs). Nothing published is restated -- the pre-cutover August render (S13-AC4) is byte-for-byte
the same date keys it has always carried; no partner was notified (no send touched by this
order; the July `ETFS_ORION_LABEL_CORRECTION` is untouched). This order gates the SEND (`EG-s-9`)
per ruling 5, not the guardrail (`EG-s-6`'s pre-publish gate is a separate cell, `depends_on: --`
here, and this order performs no upload -- FWD-6's APPLIED grade reads the first aligned render
on the box after `EG-s-6`'s ONE artifact upload, which this order does not perform).

## Controls (mutant + determinism, informal -- proof_of_spec instance carries the formal record)

**Mutant:** `for raw_d in sorted(series):` temporarily flipped to
`sorted(series, reverse=True)` (collision resolution inverted to EARLIER-wins). Re-ran
`test_orion_alignment.py`: `1 failed, 4 passed` -- `test_e_a_collision_keeps_the_later_raw_dates_values`
failed with `AssertionError: the LATER raw date (d3) wins the collision`, the other four arms
(a, b, c, d) stayed green because they carry no multi-date collision. File restored
byte-identical to pre-mutant (`diff` empty) before re-running the full green suite (`5 passed`).

**Determinism:** AC1 (pure local computation, no network) run twice, `5 passed` both times,
identical output. AC2 (pure regex over static source) run twice, identical
`ALIGN_CALLS=1 CUTOVER=2026-09 SECOND_IMPL=0` both times. AC3/AC4 (live S3 renders) each run
twice; both runs of each produced identical `OK:` lines and identical CSV values (Sept DIVZ
`2026-09-01` column `18895738.68` on both runs).

## Push state (measured)

`git ls-remote origin refs/heads/CLOUD` -- not queried mid-work; stated at commit time in the
worker report per the record-face convention (a value read here would age before the report).

## Declared exclusions

- No deploy, no `--s3-out`, no PDF: none run, per the order's explicit bound. `EG-s-6`'s ONE
  artifact upload is the deploy vector; out of this order's scope.
- `data/etfs/scripts/coverage/__init__.py`, `classifier.py`, `remediate.py`,
  `trading_calendar.py` (the coverage package proper) are NOT created here -- they are `EG-s-4`/
  `EG-s-7`/`EG-s-6`'s cells (a different worker slot, concurrent). `_orion_vendor_asof.py` was
  originally vendored under `data/etfs/scripts/coverage/` by this order, then `git rm`'d per the
  issuer's amendment (`ETFS_GUARDRAIL-W1-S1`, below) -- `data/etfs/scripts/coverage/` carries no
  file from this order after the amendment.
- `write_month_csvs`'s independent alignment call is an extension beyond the deliverable's
  literal call-site sentence, filed as `ETFS_GUARDRAIL-W3-S1` (OBSERVATION, INERT, disarmed
  same-turn by this order's own second call site) rather than silently left as a gap.

## Second surprise: the proof-of-spec instance filename the pipeline gate actually needs

The TO's own `<proof_of_spec>` section names the instance path with the short `to_id` form
(`ETFS_GUARDRAIL.TO-EG-s-13.proof_of_spec.json`). `.tools/to-pipeline-gate.py`'s
`check_complete_flip` (the gate `safe-commit.sh` runs on a staged `<status>complete</status>`
flip for a `dep_stage`-registered project, which `ETFS_GUARDRAIL` is) derives the expected
instance filename from the **TASK-ORDER FILE'S OWN BASENAME** instead
(`ETFS_GUARDRAIL.TO-EG-s-13.orion-date-basis-alignment-forward-only.proof_of_spec.json`), never
from `to_id`. Measured live: with only the TO-instructed short-named instance staged, the gate
REFUSED the flip ("NO proof-of-spec instance was found beside it"); with a second,
byte-identical copy additionally staged under the long-stem name, it passed clean ("OK: 0
newly-added TO file(s) carry `<decomp_ref>` and a complete `<preflight>` block."). Filed as
`ETFS_GUARDRAIL-W3-S2` (OBSERVATION, INERT, disarmed same-turn for this order by committing
both filenames; the generic mismatch is left named for a wider owner since it will recur on
every ETFS_GUARDRAIL TO whose `<proof_of_spec>` section names the short form).

## Amendment (issuer, 2.0.0_SA_COO~B, after the first commit)

The issuer's drain confirmed row `ETFS_GUARDRAIL-W3-S2` at `.tools/to-pipeline-gate.py:1262-1263`
and fixed it on all 14 faces; for THIS order the final resolution is to keep ONE instance under
the gate-expected long-stem filename only (the short-name duplicate git rm'd, superseding this
document's earlier "commit both" disarm). Separately, on row `ETFS_GUARDRAIL-W1-S1` (CTO~Z
ruling @`1da1e2b73b`, "MINT THE LAYER, NOT A FIFTH COPY"): a committed first-party module copy
is REFUSED -- `data/etfs/scripts/coverage/_orion_vendor_asof.py` was `git rm`'d. The import
bootstrap's fallback path is unchanged code (a sibling `_orion_vendor_asof.py` beside the
coverage package, which `EG-s-6`'s deploy places on the reporter box at build time and which
this repo never carries); only the committed vendored copy is gone. S13-AC1 re-run clean from
the repo's primary import lane (`5 passed in 0.45s`); the amended S13-AC2 invocation (adding
`COMMITTED_ORION_COPY=os.path.exists(...)`) returns `ALIGN_CALLS=1 CUTOVER=2026-09
SECOND_IMPL=0 COMMITTED_ORION_COPY=False`; S13-AC5 re-run clean on the now-two-file .py surface.
