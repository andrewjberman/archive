# CN-l-3 (round 3) -- ruling A-21, row LGIC_CANON-S4: `state/` plane decided in section 2

**Worker:** `0.9.0_WK_LGIC_CANON~2` · task order `LGIC_CANON.TO-CN-l-3-r3.state-plane.md` · file edited:
`infra/logic/06_CONFORMANCE_LEDGER.md` (v1.2 -> v1.3).

## Branch taken: **ROW**

Section 2 (THE FIRM BUCKETS) named a `state/` plane in prose only -- the `opal-data-49financial/gold/`
row's disposition cell says the bucket "absorbs `opal-data-bd`'s gold/platinum/state/code" -- with no
row carrying that decision. `02_DOCTRINE.md` R21 (`infra/logic/02_DOCTRINE.md:549-557`) names `state/`
as a fifth, non-medallion class and its own census line (`:555`) reads workflow state inside `gold/`,
`config/`, `otp/` and `blackdiamond/` tier planes in `opal-data-bd`, `opal-data-inf` and `opal-data-cot`
as **VIOLATED-LIVE**, with "the D8 migration brief IV.6 maps each to `state/`."

`docs/briefs/d8-legacy-firm-buckets-migration-brief-20260913.md` IV.6 (`:229-244`) is that mapping table
and is the source for the three rows added -- destination strings, family names and the R21 rule are
reproduced from IV.6's own cells, not typed fresh:

| legacy bucket | new §2 row -- plane cell | destination | rule |
|---|---|---|---|
| `opal-data-bd` | `{gold/_state/**, gold/_parity/**, gold/meta/*_watermark.json, gold/manifests/**, gold/canonical/watermarks.json, config/*, otp/state.json, blackdiamond/49f/session-trigger-mode.json, silver/meta/gap_manifest.json}` | `opal-data-49financial/advi/49financial/state/{watermarks,parity,manifests,config}/**`, `blackdiamond/49financial/state/session/trigger-mode.json` | R21 R1 |
| `opal-data-inf` | `{gold/_state/**, gold/_parity/**, gold/meta/*_watermark.json, gold/manifests/**, gold/canonical/watermarks.json, config/*, otp/state.json, silver/meta/gap_manifest.json}` | `opal-data-inflection/advi/inflection/state/{watermarks,parity,manifests,config}/**`, `orion/inflection/state/otp/state.json` (IV.6: "the `inf-otp-state-change` rule follows it") | R21 R1 |
| `opal-data-cot` | `{gold/_state/**, gold/_parity/**, gold/meta/*_watermark.json, gold/manifests/**, gold/canonical/watermarks.json, config/*, blackdiamond/cot/session-trigger-mode.json, silver/meta/gap_manifest.json}` | `opal-data-cottonwood/advi/cottonwood/state/{watermarks,parity,manifests,config}/**`, `blackdiamond/cottonwood/state/session/trigger-mode.json` | R21 R1 |

Each row's disposition applies R21's own grammar (`{source}/{scope}/state/{family}/…`, `02_DOCTRINE.md:551`)
and "in the bucket whose tenancy the state belongs to" -- the bucket is the same firm bucket D10-2 already
ruled for that legacy bucket's gold/platinum/silver/bronze/code rows (49financial / inflection / cottonwood),
so the state row sits beside its bucket's other MIGRATE (home) rows in class.

**Object/newest cells: `UNMEASURED`.** This ledger's census (`01_CENSUS.md`) never counted these specific
keys as their own rows -- they were previously invisible inside the `gold/` bulk counts the existing bd/inf/cot
`gold/` rows already carry. Per the order, no count the ledger has not measured is claimed.

## §7 counts -- reproduced by the script, not typed

`org/missions/D14/LGIC/LGIC_CANON/deliverables/0.9.0_WK_LGIC_CANON~2/ledger_recount.py` (unedited, read-only)
classifies each new row `MIGRATE (home)` (its `rules` cell `R21 R1` is not a subset of {R1,R2,R3}, and the
disposition carries no `(format`/`(grammar` marker immediately after `MIGRATE`) -- the same class as the
tier rows the new row shares a bucket with. Before -> after this edit:

```
MIGRATE (home):                 23 -> 26   (+3, the three new rows)
PLANE ROWS (the denominator):   68 -> 71   (§2: 25 -> 28)
DECIDED:                        65 -> 68   (+3; all three new rows carry rules+disposition+decided filled)
```

§7's own tables were updated FROM the script's printed `TOTAL` lines (not hand-typed), and the header
denominator prose (§0-adjacent line above §7's tables) and the change log (§9, entry v1.3) were updated
to match. Re-run after the edit: `ledger_recount.py` prints `RECOUNT: OK` -- all fourteen §7 checks AGREE,
0 problems.

## Criteria

- **L3R3-AC1** (`check_canon_r3.py l3-state-plane`): `VERDICT: PASS-L3-STATE-PLANE-DECIDED`. Section 2
  denominator 29 table rows; 3 rows name `state/` in the plane cell, all 3 decided under R21; branch `ROW`.
- **L3R3-AC2** (`check_canon_r2.py l2-recount`): `VERDICT: PASS-L2-COUNTS-REPRODUCED` -- all 14 TOTAL
  labels the recount script prints are carried in section 7's own table at the same value.
- **L3R3-AC3** (`check_canon_r2.py l2-header`): `VERDICT: PASS-L2-HEADER-REVERTED` -- unaffected by this
  cell's edit; still passes (section 7's header cell still reads `disposition`, never `disposition class`).
- **L3R3-AC4** (judgment, for `3.0.0_SA_CVO`): the branch taken is **ROW** (stated above); the added rows'
  disposition applies R21 (`02_DOCTRINE.md:549-557`) and R1's grammar as the canon writes them, sourced
  from the D8 brief's own IV.6 mapping table rather than invented. No mechanical instrument can grade
  whether the disposition text is a *correct* reading of R21/R1 against IV.6 -- that is the CVO's read at
  L9, per the order.
