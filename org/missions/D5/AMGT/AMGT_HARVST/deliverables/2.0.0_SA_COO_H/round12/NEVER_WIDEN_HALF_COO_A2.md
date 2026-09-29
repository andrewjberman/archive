# NEVER-WIDEN -- COO HALF: the scoped API carries the timeline routes (`HVST-a-2`), in ONE combined act with AMGT_RESAPP `AMGT-uu-4`

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~00:5xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s a-2 half (owed).
**Measured at:** CLOUD `f256f7d45b`. **Ruling it implements:** `1.0.0_SA_CTO~Z` msg 26318 -- ONE combined act (one HEAD
build, one apply, one change-management entry naming both orders, one CloudOps seat) under BOTH pairs; each project's
criteria graded separately at its own L9. The other pair: `org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round46/NEVER_WIDEN_HALF_COO_UU4.md`
(amended to admit this pair's change set) and the CTO's uu-4 half.

## VERDICT: SIGNED for HARVST's change set; RESAPP's change set is covered by uu-4's pair, not by this half

## 1. HARVST'S ACTS inside the one combined act

1. **PACKAGE** what the timeline loaders import (row `Z-S35`): `pyarrow` as a sha256-pinned cp311 manylinux2014_x86_64
   wheel through the build script's EXISTING `VENDOR_PINS` pip-download (`build-and-upload-scoped-amgt.sh:129`, the path
   that already vendors `jsonschema`; egress to PyPI declared here, as `AMGT-tt-2`'s half declared it), a version that
   imports against the layer's numpy 2.2.6; `lib/opal_naming` and its registry data added to the closure roots.
2. **MOUNT** the two timeline route keys declared by `HVST-a-1` (`180989c8a8`).
3. **GRANT** ONE statement on `opal-amgt-scoped-api-role`: `s3:GetObject` on `arn:aws:s3:::opal-data-harvest/amgt/harvest/gold/*`
   (row `Z-S36`). No other IAM change.

## 2. WRITERS -- counted

Function code: one mechanism (terraform in `infra/aws/terraform/harvest/`), and after uu-4's refusal (entry
`amgt-resapp-uu4-scoped-amgt-adjusted-base-20260928` CLOSED @`c524129644`) **0 AMGT deploy entries are open**; the
combined act is the only writer. Route set: one writer (`scoped_amgt_routes`, 18 at HEAD). Role grants: one writer (the
inline policy in this root).

## 3. THE CLOSURE -- what moves, MEASURED (no egress)

Deployed artifact VersionId `0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS` (CodeSha256 `vBSCqd71...Mrew=`), byte-compared with the
trunk at `f256f7d45b`: 63 `lib/` members, **60 identical, 3 changed**; `lambda_function.py` identical.

| member | HARVST's part (this pair) | RESAPP's part (uu-4's pair) |
|---|---|---|
| `lib/research/api/scoped_amgt.py` | the timeline dispatch and `_timeline_*` loaders (`HVST-z-0`, `78f11f5a02`); **`scoped_amgt_route_table()` folds in `TIMELINE_ROUTES` (`HVST-a-1`, `180989c8a8`)** | `_model_cases` and its `case_rule` import (uu-3) |
| `lib/research/harvest/publication_gold.py` | the plurality lead (`HVST-a-3`); reached through the timeline loaders | -- |
| `lib/research/print/render_pack.py` | -- | `_model_case_line` (uu-3, `b56fef3032`) |
| NEW `lib/research/harvest/timeline_api.py` | the timeline server module | -- |
| NEW `lib/research/api/case_rule.py` | -- | the adjusted-basis rule |
| NEW `lib/opal_naming` + registry data, pyarrow members | this act's packaging | -- |

**One item for the co-signers:** uu-4's amended limb 3 admits "the timeline route dispatch and the `_timeline_*`
functions HVST-z-0 landed" in `scoped_amgt.py`. **`HVST-a-1` ALSO changed `scoped_amgt_route_table()`** (16 -> 18), which
that limb does not name, so as written the combined build would STOP on it. **This half names it; uu-4's limb 3 needs
the same word** (told to `2.0.0_SA_COO~Z` and `1.0.0_SA_CTO~Z` with this commit).

## 4. STOP LIMBS (the build stops, nothing uploads, the entry closes ABANDONED)

1. The closure names a member that NEITHER pair names (section 3 is this pair's list; uu-4's limb 1 is the other).
2. The unzipped total of package + every layer exceeds **250 MiB** (the layer alone is 121,743,633 B).
3. The build's own verify refuses a packaged module whose in-scope imports are unpackaged (a pyarrow that cannot import
   against numpy 2.2.6 is here).
4. The plan names a resource beyond the function's code, the two routes (and their per-route resources), and the one
   role statement -- plus whatever uu-4's pair names.

## 5. EXPECTED OUTCOME, HARVST's criteria -- both branches

- **SUCCESS:** `a-2.AC1` PASS (both timeline routes on API `7k3ed8px20`; the deployed function answers both for
  `992_HK_Equity` HTTP 200 with data, in-region duration under 29 s) and `a-2.AC2` PASS (code moved off
  `vBSCqd71...Mrew=`, a new artifact version latest, `0XDw5hJW...` standing, `/thesis` `/overlay` `/peers` 200).
  The timeline then serves the round-12 part `date=2026-09-29/part-20260929T002311Z` (8 events; BA 2026-09-08 leads
  with the August deliveries story) -- **a user-visible first for this table**.
- **ANY FAIL after the apply** (either project's criteria): the combined ROLLBACK below, same session.

## 6. ROLLBACK -- per key, forward, one act

Re-point the function to `0XDw5hJWOYgx3P8CSA42oAlkLuTlupkS` (never deleted) and revert this root's route and grant edits;
ONE `safe-apply`. The gold the routes read is untouched either way. Rolling back reverts RESAPP's change too -- the
combined act rolls back as one, which uu-4's pair must also say.

## 7. NOT COVERED BY THIS HALF

RESAPP's served outcome (48 SERVED -> adjusted, 22 ABSENT -> SERVED): uu-4's pair covers it. Any S3 delete. Any gold
change. The portal DEV push of `92a2576254` (Andrew's ruling 3; `0.0.0_AB_MSTR~Z` measures its conditions after this
lands). The executing seat: `0.7.0_AE_CloudOps~A` (HVST-a-2 AMENDMENT 2, same commit as this half).
