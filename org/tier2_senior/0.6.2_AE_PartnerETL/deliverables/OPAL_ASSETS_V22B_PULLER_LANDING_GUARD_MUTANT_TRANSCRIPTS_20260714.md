# OPAL_ASSETS V2-2(b) -- si2 puller SET-IDENTITY LANDING GUARD: mutant transcripts (shortfall + surplus + collision)

**Author:** 0.6.2_AE_PartnerETL . 2026-07-14 ~17:5xZ
**Function under test:** `Get-LandingGuardVerdict` in `infra/aws/ec2/canonical-schwab-si2/sdd-daily-pull.ps1`
**Method:** the function extracted BYTE-IDENTICAL from the committed file via the PowerShell AST
(`FunctionDefinitionAst`, single match asserted) and exercised with synthetic plan/listing sets -- the
verdict logic itself is pure (no I/O), so the mutants measure the instrument, not the plumbing. The C2
lesson binds the design: the verdict reads DISTINCT LANDED KEYS from a FRESH post-run ListObjectsV2
pass, never the write tally.

**Scope law (documented in-function):** shortfall over every planned filename; surplus + collision over
keys inside (type, date) partitions the plan names. Full-lane bronze<->silver identity is the silver
sweep guard's job (set_identity_guard.py) -- the out-of-window control below proves the puller guard
does NOT fire on history the run never touched.

## Transcript (verbatim, 2026-07-14)

```
PARSE CLEAN: whole file, 0 syntax errors
EXTRACTED: Get-LandingGuardVerdict (byte-identical via AST)
BASELINE(clean): ok=True shortfall_n=0 surplus_n=0 collision_n=0 shortfall=[] surplus=[] collisions=[]
MUTANT(a-shortfall): ok=False shortfall_n=1 surplus_n=0 collision_n=0 shortfall=[08242234.CRS20260713.RLD.zip] surplus=[] collisions=[]
MUTANT(b-surplus+collision): ok=False shortfall_n=0 surplus_n=1 collision_n=1 shortfall=[] surplus=[99999999.CRS20260713.ACC.zip] collisions=[acc/20260713 (landed=2 planned=1)]
CONTROL(out-of-window-alien): ok=True shortfall_n=0 surplus_n=0 collision_n=0 shortfall=[] surplus=[] collisions=[]
MUTANT(c-both): ok=False shortfall_n=1 surplus_n=1 collision_n=1 shortfall=[08242234.CRS20260713.ACC.zip] surplus=[99999999.CRS20260713.RPS.zip] collisions=[rps/20260713 (landed=2 planned=1)]
CONTROL(two-planned-one-partition): ok=True shortfall_n=0 surplus_n=0 collision_n=0 shortfall=[] surplus=[] collisions=[]
```

## Reading

- **MUTANT (a) shortfall** -- a planned file absent from the fresh listing (the write-tally-lied /
  hung-cp class): verdict FAILS, offender named. In the live script this is `Die 6` AFTER the manifest
  (record-then-raise) when download failures are zero -- the tally said done, the bucket disagreed.
- **MUTANT (b) surplus + collision** -- an alien key planted inside a plan-named partition: both axes
  fire; collision names the double-occupied PARTITION at partition grain (reader sees WHICH (type,date)
  without diffing filename lists).
- **MUTANT (c) both** -- shortfall and surplus/collision simultaneously; neither masks the other.
- **CONTROL out-of-window** -- an alien in a partition the plan never named does NOT fire the run guard
  (window discipline; the full-lane instrument is the sweep guard). A guard that fired on all history
  would FAIL every run against 3 years of backlog and teach operators to ignore it.
- **CONTROL two-planned-one-partition** -- collision is COUNT-AWARE (landed > planned), not
  one-per-partition dogma: a vendor enumeration that legitimately names two files for one partition
  passes when exactly those two land.

## Live wiring (committed alongside)

- Guard runs post-loop on a FRESH `s3 ls --recursive` of the landing prefix (the pre-loop index is the
  RESUMABILITY instrument; reusing it would let a failed write inherit a PASS from history).
- Verdict + offender lists (first 50) fold into the run manifest; manifest `ok` is now
  `(fail == 0) AND guard.ok`; manifests write to `_ops/daily_pull/` (continuity) AND
  `schwab/{master}/meta/pulls/` (ruling-21 home; WARN-not-die until the
  `MonolithSchwabMetaPullsWrite` grant applies at CTO's gate -- TF authored, plan 0/1/0 pure
  statement-add on the inline policy).
- `Die 6` on guard-fail with zero download failures -- loud, after the record lands.

## NOT yet deployed

The box pulls this script from `s3://opal-data-schwab/_ops/canonical-schwab-si2/sdd-daily-pull.ps1` at
each scheduled fire (Rule 12 chain). The S3 upload is DELIBERATELY HELD until after tonight's
21:45/22:15Z fires verify against the V2-8 expectation report -- one variable per observation window
(AC-3 is watching the CONVERTER; the puller must not move the same evening). Upload lands with the next
morning window unless CTO orders otherwise.
