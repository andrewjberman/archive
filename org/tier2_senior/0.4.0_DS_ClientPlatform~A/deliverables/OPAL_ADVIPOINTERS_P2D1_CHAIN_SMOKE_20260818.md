# P2D-1 CHAIN SMOKE -- dry-run composition evidence (0.4.0_DS_ClientPlatform~A, 2026-08-18)

**Invocation:** `python chain_49f_entrypoint.py --date 2026-08-10 --workdir <scratch>` (dry-run posture: every stage --dry-run, a07 workdir-local, no S3 writes anywhere). rc captured BARE (no pipe): **rc=1, the designed abort** -- see reading.

## Stage results (verbatim)
```
CHAIN START date=2026-08-10 mode=dry-run workdir=C:\Users\ANDREW~1\AppData\Local\Temp\claude\C--Users-AndrewBerman-Desktop-ajb-workspace\7f36b8bf-86fb-49e9-9d89-650b5ac3f7e9\scratchpad\chain_dryrun stages=16
STAGE OK a00_dim_account rc=0 wall=30.4s
STAGE OK a01_dim_relationship rc=0 wall=2.2s
STAGE OK a02_dim_boundary rc=0 wall=127.6s
STAGE OK a03_dim_security rc=0 wall=2.0s
STAGE OK a04_dim_calendar rc=0 wall=1.9s
STAGE OK a05_ref_txn_class rc=0 wall=1.9s
STAGE OK a06_identity_crosswalk rc=0 wall=2.3s
STAGE OK a07_asset_class_pair rc=0 wall=6.4s
CHAIN ABORT stage=b00_canonical_valuation rc=1 wall=1.9s -- nothing after this stage ran
```

## Reading
- **a-stages 8/8 GREEN**, measured dry wall-clocks: a00 30.4s / a01 2.2 / a02 127.6 (FRM leg sweep dominates) / a03 2.0 / a04 1.9 / a05 1.9 / a06 2.3 / a07 6.4 = **~175s for the dim plane** (dry lower bound; upload adds write time).
- **The b00 abort is CORRECT-BY-DESIGN in dry-run**: a-stages wrote nothing (--dry-run), so b00's same-date `dimensions/dim_boundary/date=2026-08-10/` S3 read finds no partition and the chain aborts LOUDLY (`CHAIN ABORT stage=b00_canonical_valuation rc=1`) -- the fail-loud composition exercised on a real missing-input, which is the control this smoke wanted. Dry-run validates per-stage reachability up to the first cross-stage data dependency; the full a->b->c with writes is P2D-3's QA exercise (08-19, S3-code path).
- **First smoke run found a REAL DEFECT**: `a01_runner.py` is import-broken at repo HEAD (imports `build_relationships`; the 08-11 P1 rewrite of `a01_dim_relationship.py` exports `build_dim_relationship`) -- the runner CANNOT have executed since the rewrite. The live module IS S3-native, so the entrypoint invokes it directly; a01_runner.py = stale predecessor, FILED not fixed, P5 candidate.
- Also exercised: the fail-loud abort on run 1 (`CHAIN ABORT stage=a01_dim_relationship rc=1` on the ImportError) -- two distinct abort classes observed, both loud, neither swallowed.
