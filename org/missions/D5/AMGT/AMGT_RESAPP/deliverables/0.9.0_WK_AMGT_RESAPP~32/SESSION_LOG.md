# AMGT-rk-22 -- SESSION LOG (0.9.0_WK_AMGT_RESAPP~32, 2026-09-18)

CARD 5 was already answered YES (`ad2d1253be`, confirmed present in this worktree before any work
started) and this task order's own bounds state the vendor call is authorized for this cell alone.

## 1. Re-grounding the population (before any code change)

`crosswalk/v1/2026-09-15.json`'s own `denominators` carry `MEASURED: 33` -- the 33 keyed names, over
89 crosswalk records. Cross-referencing each of those 33 against `filings/v1/<key>/` (latest
accession's `status` field) gave 12 with `status: "RESOLVED"` -- management's filing ceiling. This
matched the CTO's card-5 math exactly (5 served today, 7 more to the ceiling; 2 served today, 31
more to the full 33) before any producer ran.

## 2. What was built

- `lib/research/management/enrich.py`: `classify_roster_absence()` (source-lacks vs pull-missed on
  the roster's own absence) and the same class attached to `domain_for()`'s SKIPPED lusha_enrichment
  reason; `ceo_public_profile()` gained `absence_class` (NOTHING_FOUND vs CANNOT_SAY -- rows
  `AMGT_RESAPP-Z-W18-S15` / `-Z-W22-S1`).
- `lib/research/management/management.schema.json`: the three new fields declared (top-level
  `absence_reason_class`/`absence_reason_evidence`, `ceo_profile.absence_class`,
  `lusha_meta.absence_reason_class`) -- the schema is `additionalProperties: false`, so this was
  REQUIRED, not optional.
- `lib/research/posture/judge.py`: `classify_posture_absence()` wired into `_absent_document()`;
  the `subject.get("held") is None` branch now writes to the pool when `write_pool=True` (previously
  it returned without writing REGARDLESS of the flag -- the exact "cannot-say is not no-profile"
  shape the round-11 remediation rows name, extended to this cell's own gap per its ruling item 3).
- `lib/research/posture/posture.schema.json`: `absence_reason_class` declared (also
  `additionalProperties: false`).
- `integrations/bloomberg/research/management_posture_batch.py`: the batch driver neither producer
  had. `report` / `management` / `posture` stages; population and ceiling read live from the pool,
  never hardcoded; additive by default (a name already served under ANY vintage is skipped unless
  `--force`).

## 3. A classifier bug caught before the final run

The first posture probe (`2317_TT_Equity`, `9433_JP_Equity`, `992_HK_Equity`) classified
"source-lacks" via a false-positive: the marker `"unresolved"` matched the substring inside "0
unresolved" in a graded-members COUNT, not a claim about resolution. Fixed to whole-phrase markers
("identity unresolved", "cannot be joined by root without guessing", etc.) before the production
run; re-ran the same three names with `--force` (no vendor cost either way -- these three never
reach the model call) and the corrected classifier reached the SAME final value via the correct
phrase, so no persisted object was ever wrong, only the code path was momentarily wrong pre-run.

## 4. The runs (verbatim tails)

Management (`--write-pool`, 7 targets): 7 of 7 built and written; 5 UNRESOLVED-SOURCE
(ASML_NA_Equity, HAL_US_Equity, INTU_US_Equity, KMB_US_Equity, PBR_US_Equity -- all classed
pull-missed: the filing exists, this module's own parse did not read its shape) and 2 RESOLVED
(NU_US_Equity 9 officers, VLO_US_Equity 5 officers). Lusha/SERP: SKIPPED for all 7 (pull-missed) --
`domains.json` still declares only the original 5 QA names (row `AMGT_RESAPP-Z-W32-S2`); zero
additional Lusha/Bright-Data credits spent.

Posture (`--write-pool`, 31 targets across three calls): 31 of 31 served. 24 absent (source-lacks:
identity resolves but the peer scanner has no non-US coverage to join a comparable against, or the
subject side itself is UNPROVEN), 7 reached a real Anthropic call (6 `better`, 1 `hold`), 0 dropped
claims on any served verdict. `BP/_LN_Equity` and `NG/_LN_Equity` (the two literal-slash names)
served correctly but land one path-segment deeper in S3 (row `AMGT_RESAPP-Z-W32-S3` -- AMGT-rk-23's
own scope, not fixed here).

## 5. What ran outside this cell's own `<paths>`

Running the posture producer transitively rebuilt
`org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~21/candidate_universe.json` (a
shared cache another worker's cell owns) because `lib/research/peers/universe.py`'s own staleness
check correctly found the committed cache pre-dated the preset-bounded retention (row
`AMGT_RESAPP-Z-W32-S4`). That file is NOT committed by this worker -- it sits outside this order's
`<paths>` grant and is left as an uncommitted working-tree diff.

## 6. Full command tails

```
python integrations/bloomberg/research/management_posture_batch.py report
CROSSWALK: crosswalk/v1/2026-09-15.json (denominators {"input_names": 89, "records": 89, "MEASURED": 33, "UNRESOLVED": 56, ...})
KEYED POPULATION: 33 of 89 crosswalk records MEASURED
MANAGEMENT CEILING: 12 of 33 keyed names carry a RESOLVED filing
MANAGEMENT SERVED: 12 of 12 ceiling names (...)
MANAGEMENT TARGETS (not yet served): 0 -- <none>
POSTURE SERVED: 31 of 33 keyed names (...)
POSTURE TARGETS (not yet served): 2 -- BP/_LN_Equity, NG/_LN_Equity
```

(the "31 of 33" line above is `served_names()`'s own first-segment name-parsing undercount, row
`AMGT_RESAPP-Z-W32-S3` -- the true, denominator-correct count is 33 of 33, confirmed directly by
this order's own AC1 invocation.)

```
python -m pytest lib/research/management/tests/test_management.py lib/research/posture/tests/test_posture.py -q
48 passed
```
