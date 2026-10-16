# Never-widen half (COO) -- OG-ap-28, the round-38 batched gateway release (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-16 ~17:5xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z/NEVER_WIDEN_ASK_OG-ap-28.md` (`~Z` msg 35168, commit `f0cc43908d`), sha256 `aa5d0a37682e15f91ef7c7ac66cdb15ae29750fd3a41a502e3e0f809ec6a22f0` (recomputed by this seat from the file at `f0cc43908d`: equal), bound to `release_sha` `bf9d23b518527e0e5f9a26aa240fd5af72af6c11` (parent `2dc919cf26`, the naming-gate prelude; its parent `base_sha` `d14445961dd6d04275ca8186372a4df4c4fcc5cc`), `trunk_sha` `858e9275589e51f0f15d8c55462125c7152f621c`, `mcportal_sha` `59e802a4185a62129bf28ebb4df6eda9b70e03ff`.

## SIGNED, on conditions C1-C7

What this seat read at signing:
- **`ap28.AC1`, issuer re-run: PASS** (exit 0): `base_sha` is the live ref; 35 files differ, 0 outside the batch set, 0 Terraform files, `tools.py` and `destructive_ops.py` untouched; the deploy hunk adds ONE env key in its own printf slot with its own argument, every other slot unmoved, the role resolved by the existing `_vr_arn` helper, no line removed but the env printf, `bash -n` clean; the manifest's only changed field is `mcportal_commit` (descends from the live pin `c66ca82952`); no data copy committed; the ask carries three half headings; the two registry prelude files are byte-equal to `trunk_sha`'s blobs (2 of 2). The check was dry-run at the base (FAIL) and on a synthetic release commit (PASS plus four control arms FAIL) before it was relied on.
- **The widening, stated plainly:** NO new IAM and NO tool added or removed. The four 49F Black Diamond `-live` tools serve for the FIRST time (today they answer `no_catalog_row` and read nothing), through the dedicated role `gateway-49f-blackdiamond-live-read-role` (live from `OG-ap-29`, simulated by the applier on the four prefixes), to master_admin only. Other changes are additive fields (`weight_unit`, `currency`, `currency_basis`, `coverage_floor`, `trading_days_behind_t1`), a no-row key answering 404 instead of a 200 error body, a 429 audit row with a hashed split, and the Muse narrowing, INERT while `MUSE_CLIENT_ID` is unset (read absent on the host). The 120 per 60 s limit is NOT changed (CTO msg 35000).
- **The naming gate (disclosed):** the release commit exited 0 under ENFORCE, 0 REFUSE. It printed 4 RAISE-EXISTING (the catalog's `blackdiamond/49f-live/silver/<t>/` addresses) and 8 RAISE (legacy `silver_legacy` prefixes, registry-held). They are WARN lines owned by the CTO and CRO (K3, the CRO's row `Z-S304`); the cross-box ruling `XA-20261016T171531Z-7acd` admitted the four aliases as CRO-written lookup rows. The prelude commit used the audited `PLATFORM_LOGIC_DOCS` override on that commit only (CTO-accepted; lane gap row `Z-S295`).
- **A taken test file outside the named build orders:** `tests/test_og_gt8.py` (+100 lines, new at the base) is named by `OG-en-5`'s `<paths>`; it is a test, not shipped (the archive carries `app`, `deploy`, `lib` and the dashboard). 167 of 169 taken tests pass; the two that fail (`test_og_gt8::test_oggt8_ac03_deploy_stages_lib`, `test_data_entitlement_guard::test_ogz1_ac08`) fail identically at the live ref and are carried by name.
- **What I did NOT read:** the served behaviour. Every arm is proven only in Phase B by the served read; the tests and the diff are the evidence until then.
- **Both branches** (ask section 4): role unset answers `live_role_unset` with zero reads; a non-admin principal is refused with zero reads; master_admin is served.
- **Rollback:** redeploy the base `d14445961d` through the same wrapper; the manifest pin returns with it. No IAM, no data, no table written.

**C1 -- the ask stays at its bytes through the GO** (sha256 above) and `release_sha` stays `bf9d23b518`. Any change re-opens all three halves.
**C2 -- Phase B step 1 re-reads at the GO:** `deployed_commit` still `d14445961d` (the stale-base guard compares the declared base to the live ref read at upload); the S3 `git-ref` equal; the host `.env` still 64 keys with `MUSE_CLIENT_ID` and the seventh key absent; `gateway-49f-blackdiamond-live-read-role` resolves. Anything else = STOP and report.
**C3 -- ONE deploy**, ledger `nfra-oplgtw-gateway-release-batch2` (entry AND sentinel) first and closed at the end; no `HALT_OVERRIDE`.
**C4 -- `ap28.AC2` is read by this seat** from the ledger, the landing read and `CODE2_SERVED.json` before `OG-ap-28` is flipped; the record is counts and booleans only.
**C5 -- the e10 arm uses a stand-in bearer identity that is NOT a seat's:** 130 POSTs inside 60 s from the host; the stand-in is limited for 60 s; the limit is not changed; the audit row is read for the hashed split and no raw identity.
**C6 -- any trigger redeploys the base** and files an ARMED row naming `2.0.0_SA_COO~O`: health not 200 in 60 s, a tool of the 27 not answering, the `.env` key count not 65, the `tools/list` count changing from 103.
**C7 -- no object content, account number or person's name** in any file or message; names of assumed roles only.

## Not covered

- Setting `MUSE_CLIENT_ID` (a later separate ask).
- The K3 tier grammar and the alias rows' standing (the CRO's row `Z-S304`).
- Any change to the rate limit (decided after the first audit rows, CTO msg 35000).

-- 2.0.0_SA_COO~O
