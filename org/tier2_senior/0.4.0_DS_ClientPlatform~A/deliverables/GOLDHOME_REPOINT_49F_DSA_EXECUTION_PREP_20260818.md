# GOLDHOME-REPOINT-49F -- DS~A leg execution prep (staged, EXECUTES ON AE's MINT MCP; 0.4.0_DS_ClientPlatform~A, 2026-08-18 ~1745Z)

**TO:** `OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F` @1b2ee34db7 (joint; AE primary). My legs =
RP-DSA-1 + RP-DSA-2, sequenced AFTER RP-AE-1 (bucket mint). This file exists so the leg executes
in minutes on the mint MCP -- including by a successor seat if the fabric recycles first.
**Nothing here has run. No writes to any new bucket have occurred from this seat.**

## RP-DSA-1 -- the two-sided sync (P3-copy precedent bar)

Source: `s3://opal-data-assets/portal/gold/advi/49financial/` (measured this session: 4,222
objects / 327,275,368 bytes -- re-measure at execution, numbers move if the 23:01Z-adjacent
period wrote anything).
Target: `s3://opal-data-49financial/gold/advi/` -- **the TO's grammar verbatim; note the tree
keeps `{product}` = advi; 49financial leaves the KEY and becomes the BUCKET.**

```
# 1. pre-sync census BOTH sides (expect target 0 -- first-fill explicit)
python -c "<paginated count+bytes of source and target>"   # print both, keep as manifest part 1
# 2. sync (server-side copy; .tools/aws shim)
.tools/aws s3 sync s3://opal-data-assets/portal/gold/advi/49financial/ s3://opal-data-49financial/gold/advi/
# 3. post-sync two-sided verify: object count AND bytes, source vs target, per top-level table
#    (10 tables) -- actuals printed beside expecteds; ETag spot-set on the 5 largest objects.
# 4. manifest (rollback instrument) -> this folder + committed: per-table {objects, bytes} both
#    sides + the sync stdout tail.
```

## RP-DSA-2 -- the one-commit code flips (prepared diffs, apply verbatim)

1. `data/assets/scripts/gold/runners_49f/runner_common.py`:
   - `BUCKET = "opal-data-assets"` -> `"opal-data-49financial"`
   - `OUT_ROOT = "portal/gold/advi/49financial"` -> `"gold/advi"` (comment: GOLDHOME re-point
     2026-08-18 @1b2ee34db7, Andrew ~1730Z)
   - ⚠ **MEASURED, not a maybe (this session, runner_common.py:27-65): ONE `BUCKET` constant
     serves BOTH silver reads (`SILVER` prefix -> `read_partition` -> `Bucket=BUCKET`, 7 call
     sites) AND gold R/W (`OUT_ROOT` through the same helpers -- b00 reads dim_boundary via
     rc.OUT_ROOT).** A naive BUCKET flip sends every silver read to the new bucket where no
     silver exists (loud total failure); leaving BUCKET sends gold writes to the old root
     (silent two-homes). **The flip is therefore a SPLIT**: silver stays `opal-data-assets`;
     gold moves to `opal-data-49financial`; the helpers must resolve bucket per prefix family
     (two-row map or explicit param at OUT_ROOT call sites -- design finalized at execution
     with the code in front, exercised by a dry-run stage read against BOTH planes before
     commit). Same split check in `a00_runner.py` (:43-52 BUCKET/GOLD_ROOT) + every stage
     importing them.
2. `.tools/safe_deploy_core.py` advi row: `"bucket": "opal-data-49financial"`, layer target
   `("data/assets/scripts/gold/runners_49f", "gold/advi/_code/")` -- wait on the TO's _code
   grammar: **"_code/ rides the root"** = `s3://opal-data-49financial/gold/advi/_code/`.
3. `chain_49f_entrypoint.py`: `BUCKET`/`GOLD_ROOT` constants follow runner_common's split.
4. `_code` MOVE (no twin): **enumerate the old prefix AT EXECUTION TIME -- never carry a count**
   (MSTR banked line 174144Z: the 1739-40Z integrator push @b7fce2ed09 minted 3 MORE objects at
   the old home via the advi row -- chain_49f_entrypoint.py, d13_firm_partner_analytics.py,
   d_publisher_port.py -- so any pre-1739Z "51" enumeration is short; an exec-time listing
   covers late writers by construction). Copy ALL listed objects
   `opal-data-assets/portal/gold/advi/_code/*` -> `opal-data-49financial/gold/advi/_code/`
   (metadata preserved), verify N/N ETag with N printed from the listing, then DELETE the old
   `_code/` prefix in the same act (delete evidence: zero-key listing + adjacent positive
   control). The old-GOLD-prefix delete is NOT mine -- RP-SPINE-2, AE executes after RP-SPINE-1.
5. Commit: commit-gate + pipescript-suite will run; re-run `.tools/test_safe_deploy.py`
   (mapping cases updated to the new bucket/prefix) BEFORE the commit.

## After my legs land (same turn)
- MCP AE: re-issued P2D-4 FIELD 3 (code key = `s3://opal-data-49financial/gold/advi/_code/`;
  SSM sync line + IAM surface lines updated -- the 173547Z contract's old key is DEAD).
- MCP CVO (RP-CVO-1 next in spine) + COO leg-landed report cc CTO/MSTR/DS~B.
- Proof instance `PROOF_OF_SPEC_GOLDHOME_REPOINT_49F_DSA_20260818.json` (grammar per TO), rc=0.

## Standing cautions carried into the act
- Bucket name FULL, never truncated (`opal-data-49financial`, never `49f`) -- the TO's own Do-not
  + the two-buckets naming law.
- Nothing executes before AE's mint MCP; nothing touches the bd platinum chain or the 23:01Z
  fixture's reads.
- My P2-DISPATCH/P3-CLOSE TOs are amended BY REFERENCE @1b2ee34db7 (roots read through this act;
  ids/dates/criteria unchanged; P2D-3 runs against the NEW root).
- P2D-2 issuer ruling (COO 173651Z): the instance's P2D-2 row cites comp-pipescript `deployed`
  MATCH post-REG, or carries the disclosure if REG slips.
