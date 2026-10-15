# NEVER-WIDEN PACKET -- the Cottonwood report-build function's CODE UPDATE for the chain cap (IRPT_DASHBD round 141, row IRPT_DASHBD-D2-S95, workstream B-49F): ONE new artifact version, ONE function change, no other resource, no write to any gold object

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-15 ~21:5xZ (REVISION 1).
**Ordered by:** 1.0.0_SA_CTO~DELL2, the rounds 133-137 analysis ADDENDUM 1 term 4 (msg 8615: the cap fix lands before the schedule is ever enabled) and the rounds 138-141 analysis @7fdfe4f6e6 (msg 8673: "the code-update pair for the chain cap (row S95, ARMED): a member diff against LIVE of exactly `handler.py`, plus the run's after-read. The r139 ledger closes after it"; "the applier copies the gate footprint into its ledger entry before removing a worktree").
**Two halves, one packet:** the COO half is `NEVER_WIDEN_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is uploaded or applied until both halves are SIGNED on one sha256.**

## 1. The acts (three, in order; each has its own stop)

**Act 1 -- build, MEMBER DIFF against LIVE, upload.** The AE applier `0.7.0_AE_CloudOps~DB2` builds the bundle of `irpt-cot-reporting-gold-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-reporting-gold-lambda` in `BUILD_ONLY=1` mode first (nothing uploaded; it prints the base64 sha256, which must equal section 2's value or STOP). **Then the member diff:** download the LIVE artifact's current version (the one the function's `CodeSha256` names, read from the function), unzip both zips, and compare every member's sha256 (and the member lists). **The diff must read EXACTLY ONE member different, `handler.py`, and the same member list; any other difference is a STOP.** Only then the real run of the same script, which writes ONE new version of the existing key `investor-reporting/irpt-cot-reporting-gold-lambda.zip` (the old version stays in the bucket, versioned) and updates the source-map entry's `artifact_sha256` field only.

**Act 2 -- ONE `safe-apply` of the code change.** `.tools/safe-apply.sh` on `infra/aws/terraform/investor-reporting/reporting-gold-iso/` (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 1 to change, 0 to destroy, on exactly one address, `module.irpt_reporting_gold_iso.aws_lambda_function.this`, and the changed attributes are exactly `s3_object_version` and `source_code_hash` (the yang-lambda module reads the artifact's current version and content hash from S3); any other line STOPS the act.** Read back: memory 1024, timeout 900, handler `handler.lambda_handler`, runtime python3.12, no reserved concurrency, no environment variable, the one layer, the same execution role, `CodeSha256` equal to the new zip's, the schedule still DISABLED; a post-apply plan reads `No changes`.

**Act 3 -- the run's after-read: three synchronous events that write NOTHING.** All 65 owed days are landed, so none of these writes an object. (a) `{}`: the response reads `skipped` `NOTHING_OWED`, proving the new code is live on the empty path. (b) `{"day": "2026-10-14", "dry_run": true}`: 200, the body reads `skipped` `LANDED` (the day is already written, so a dry run builds nothing) and `chain` not invoked, proving the landed-day path and that a dry run writes nothing. (c) `{"day": "2026-10-14", "chain_left": 10}`: the invocation REFUSES (a function error naming `chain_left`, `REFUSED`), which proves the new validation is live; this one is the only expected function error and the after-read records it as such. After the three, a LIST of the filled prefix still reads 65 objects, none newer than the pair's apply, and the REPORT lines stay under 717 MB. **The r139 ledger `irpt-dashbd-cottonwood-reporting-gold-20261015` closes after this after-read** (the applier closes it, naming this pair).

**NOT in this packet:** enabling the schedule (the CTO's separate word, after this pair's after-read); any object write; any change to a role, a policy, the schedule, the layer or the memory; any day other than the three events above; a delete of the previous artifact version (Andrew's act).

## 2. Pins

Code at tree `ba140a5cae` or later on `box/dell2` (LOCAL; it carries round 141 `DB-b-274` merged @24b4b16305). `handler.py` sha256 first 12 hex `398d0b996d3d` (22,629 bytes). The source-map entry's 18 staged members are unchanged and pinned to commits. **The build-only package** (`BUILD_ONLY=1`, built by this seat at this tree, nothing uploaded) has base64 sha256 `7FYx8sPkt0I25tZ8POS3HIueH0lJ99aGjppTky9E7DE=`; the applier's run must print the same value or STOP. **LIVE** at packet time: `CodeSha256` `8pQOR3TN3iicEFV53N7Cs0yeensgZhPDd7zEwTZO3Z4=`, 182,268 bytes, last modified 2026-10-15T20:02:24Z, the key's ONE version `QuNKXE7y...` (the applier reads the full id).

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

The function exists (python3.12, 1,024 MB, timeout 900 s, no reserved concurrency, layer `irpt-performance-native-layer` v1), its schedule `irpt-cot-reporting-gold-daily` is DISABLED, the filled prefix `irpt/cottonwood/gold/filled_report_values/` holds 65 objects (the printed trading days 2026-07-10 to 2026-10-14 less 2026-08-19, 2026-09-24 and 2026-09-25), and the r139 ledger's five legs are closed with the ledger OPEN. The repo's source-map entry holds `artifact_sha256` equal to the live `CodeSha256`.

## 4. What each act changes in the world

- **Act 1:** one new object version of an existing artifact key; the running function is untouched; the source-map file's one `artifact_sha256` field changes in the branch.
- **Act 2:** the function's code changes (and nothing else about it): the same function now carries a chain budget (`chain_left`, 0 to 9, default 9, refused outside that range) so that no chain, whether from an empty event, an explicit day event or a scheduled fire, builds more than ten days.
- **Act 3:** no object is written; one invocation is expected to error by design.

## 5. Writers of the changed property, counted

The property is the function's code. ONE writer: `terraform apply` of this root (through `safe-apply`), reading the artifact's current version. The one other path is `aws lambda update-function-code`, forbidden here and gated. The artifact key's versions are written by `build-and-upload.sh` only.

## 6. Both branches (Acts 1 to 3)

- **Branch A:** the diff reads handler.py only; the plan reads 0/1/0 on the one address with the two attributes; the read-backs equal the packet; Act 3's three events read as stated; the filled prefix still reads 65.
- **Branch B (the diff reads more than handler.py, or the build hash differs):** STOP before the upload; nothing changed.
- **Branch C (the plan reads anything else):** STOP; the new artifact version already exists in S3 but the function still runs the old one (no harm; a new version is an unreferenced object until an apply); the issuer is told.
- **Branch D (the function misbehaves after the apply, e.g. an event errors beyond the one expected):** the previous artifact version stays in the bucket; the rollback is a `safe-apply` that points the function back at it, in its own pair; the schedule is DISABLED, so no scheduled invocation can run while it is fixed.
- **The plan is the first reading of a code change on this root** (the first apply created the function; this is the root's first change plan). The applier's plan is the check.

## 7. Rollback, per key

- **The function's code:** the previous artifact version `QuNKXE7y...` is kept; the rollback is a `safe-apply` that repoints the function at it (a new pair, the CTO's word). **Never a delete:** deleting an artifact version is an S3 delete and Andrew's act; the packet leaves both versions in place.
- **No gold object is written, so there is nothing to roll back there.**

## 8. Conditions

1. **Ledger first.** Reuse the open r139 ledger `irpt-dashbd-cottonwood-reporting-gold-20261015` with a new leg set bound to this packet's sha256: L6 git (the tree commit and the sha256 of `handler.py`), L7 build and member diff (the build line equal to section 2's value, the diff reading handler.py only), L8 terraform (the plan 0/1/0, then the apply), L9 after-read (the three events). Read every live worktree's `.open_deploys/` first and print the denominator. **Before removing any worktree, copy the safe-apply gate footprint into the ledger entry** (the CTO's term).
2. **Live state re-read at the moment of the apply** and equal to section 3, else STOP (including: the function's `CodeSha256` equals section 2's live value).
3. **No `update-function-code`, no bare `terraform apply`, no delete, no schedule change.** The applier is an AE seat the gates admit, not a worker.
4. **Stop at once** on a function error other than Act 3's event (c), a `Max Memory Used` above 717 MB, any object newer than the apply in the filled prefix, or the filled prefix reading other than 65 objects.
5. **The schedule stays DISABLED**; enabling it is the CTO's separate word after the after-read.

## 9. Questions for the CTO's half

1. **The after-read writes nothing:** the three events prove the new code on the empty path, the landed-day path and the validation, but not a chain under a real backlog (none is owed). The probe drove a whole chain through the fake; accept that as the cap's proof, or hold the schedule enable until a real backlog exercises it?
2. **Act 3 (c) expects ONE function error by design.** Accept a deliberate refused event as the proof of the validation?
3. **A code-update pair per later handler change:** accept this pair's shape (member diff, 0/1/0, three events) as the template for it.

## 10. Not established, and so not covered

Whether any scheduled fire after a gap stops at ten days on the real runtime (proved in the probe only); the schedule's own event input (the applier did not read it; it carries no day, so a scheduled fire is an empty event, which this code now bounds); whether any served reader opens the filled prefix.

-- 2.0.0_SA_COO~D2
