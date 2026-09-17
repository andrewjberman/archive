# LGIC_ENFORCE-S60 -- disposition, round 4 cell EN-g-27

`0.9.0_WK_LGIC_ENFORCE~4` on cell `EN-g-27` (RULINGS R-16, R-26, R-32). Worktree
`C:/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-4-4`, branch
`wk-lgic-enforce-4-4`, base `3de3a4e32a` (CLOUD).

## Disposition: FIXED

S60's undercount -- `.tools/safe_deploy_core.py` deciding only the S3/DS plane while a single-
classifier split would print at least 5 of the generator's 10 shipping targets as REPO-ONLY -- is
**FIXED** by R-26's per-plane split, already built and merged as round 3's `EN-g-9`
(`lib/opal_naming.py:1810` `targets_report()`, `:1847` `cmd_targets()`) and unchanged since.

## Measurement (live run, no fixture)

```
$ python lib/opal_naming.py targets
TARGETS: 10
SHIP lambda data/firm_registry.json measured: lambda-source-map.json (2 consumer(s): irpt-intake-poller, irpt-ycharts-generate)
SHIP lambda infra/aws/lambda-edge/_shared/firm-config.mjs measured: lambda-source-map.json (3 consumer(s): auth-validator-edge, shared-advisor-router, shared-advisor-router-response)
SHIP s3 data/assets/scripts/gold/investor_reporting/directory_runner.py measured: safe_deploy_core (file_to_s3_target/bundle_for_member)
SHIP s3 data/assets/scripts/gold/investor_reporting/holdings_snapshot.py measured: safe_deploy_core (file_to_s3_target/bundle_for_member)
SHIP lambda infra/aws/lambda/investor-reporting/_authz/loaders.py measured: lambda-source-map.json (7 consumer(s): irpt-directory-search, irpt-export-render, irpt-holdings, irpt-narrative, irpt-performance-adapter)
SHIP s3 data/assets/scripts/gold/runners_49f/perfrp_firm_pin.py measured: safe_deploy_core (file_to_s3_target/bundle_for_member)
REPO-ONLY tools .tools/ds-precommit-check.py measured: no S3/Lambda/Terraform claim (repo-local gate script, never packaged)
SHIP terraform infra/aws/terraform/modules/opal_name/generated_locals.tf measured: consuming root(s) infra/aws/terraform/shared-infra (git grep modules/<name>)
REPO-ONLY terraform infra/aws/terraform/modules/opal_name/tests/vectors.json measured: comp-find root census (test fixture beside the module, not a deploy)
REPO-ONLY terraform infra/aws/terraform/modules/opal_name/tests/opal_name.tftest.hcl measured: comp-find root census (test fixture beside the module, not a deploy)
PLANE lambda: 3
PLANE s3: 3
PLANE terraform: 3
PLANE tools: 1
HASH-PINNED CONSUMERS: 1 of 95 scanned
```
`rc=0`.

**The numbers.**
- **Target count:** 10, equal to the AST denominator (`generate()`'s `known` list: 7 `VIEWS` +
  `LOCALS_PATH` + `VECTORS_PATH` + `TFTEST_PATH`) -- the same 10 S60 measured its shortfall
  against.
- **Per-plane counts:** lambda 3 (all SHIP), s3 3 (all SHIP), terraform 3 (1 SHIP, 2 REPO-ONLY
  test fixtures), tools 1 (REPO-ONLY). 10/10 classified, **0 UNCLASSIFIED**.
- **Distinct instruments called, one per plane, not one classifier over all:**
  1. `.tools/safe_deploy_core.py` `file_to_s3_target`/`bundle_for_member` (`.tools/safe_deploy_core.py:427`,
     `:731`) -- the S3/DS plane, 3 targets (this is the instrument S60 measured as deciding only 3 of 10;
     it still decides only those 3, but is no longer asked to decide the rest).
  2. `infra/aws/lambda/ci/lambda-source-map.json`, read by `lambda_plane_consumers()`
     (`lib/opal_naming.py:1730`, `_lambda_source_map()` at `:1704`) -- the Lambda plane, 3 targets,
     each row naming its consumer functions and count.
  3. the consuming Terraform root, measured via `git grep modules/<name>` outside the module's own
     directory (`terraform_plane_consumers()`, `lib/opal_naming.py:1768`) -- the Terraform plane's
     SHIP row (`generated_locals.tf` -> `infra/aws/terraform/shared-infra`).
  4. `comp-find root census` -- the Terraform plane's two REPO-ONLY rows (test fixtures beside the
     module, never a deploy).
  5. "no S3/Lambda/Terraform claim" -- the tools plane's one REPO-ONLY row
     (`.tools/ds-precommit-check.py`, a repo-local gate script never packaged).

  **5 distinct instruments over 4 planes**, each row's `measured:` field naming the instrument that
  decided it -- never one classifier deciding a plane it cannot see, which was S60's own shape.
- **Hash-pinned-consumer census line:** `HASH-PINNED CONSUMERS: 1 of 95 scanned`
  (`hash_pinned_census()`, `lib/opal_naming.py:1792`, scans tracked `.tools/*.py` for
  `sha_metadata_key` or `index_md5`; `.tools/safe_deploy_core.py` is the one hit). Round 3's own
  result record (`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~5/target-split.r3.result.md:47`)
  printed `1 of 94 scanned` at its own cut; the denominator moved to 95 because one more `.tools/*.py`
  file has landed since (tree drift between round 3 and round 4, not a defect in the census -- the
  scan is unscoped over the tracked set each time it runs, so the denominator is expected to track
  the tree).

## The AC1 regression read, at this tree

```
$ python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r4/check_en_r4.py g27-plane-instruments
DENOMINATOR: TARGETS 10 printed; 10 classified row(s); rc=0
  planes printed: lambda=3, s3=3, terraform=3, tools=1
  distinct measuring instruments: 5 -- comp-find root census; consuming root; lambda-source-map.json; no S3/Lambda/Terraform claim; safe_deploy_core
  UNCLASSIFIED: 0; rows with no instrument: 0
10 of 10 targets classified by 5 plane instruments, 0 UNCLASSIFIED
VERDICT: PASS-G27-PLANE-INSTRUMENTS
```
`rc=0`. This is the same PASS the issuer measured at the cut; nothing in this cell's measurement
changed it.

## What a passing read does NOT prove

`targets` is a **read-only print** (`targets_report()` never calls `generate()`; `lib/opal_naming.py:1810-1846`
writes nothing, per R-16). A correct per-plane split here is evidence about the **classifier**, not
about any deployment that already ran under the old single-classifier reading. In particular, it says
nothing about R-16's own earlier act -- EN-r-6's comment-only re-render that re-minted the
investor_reporting bundle and deployed `perfrp_firm_pin.py` to advi with zero executable bytes
changed (`org/tier1_exec/1.0.0_SA_CTO/deliverables/SELF_DRIVE_LGIC_RULINGS_20260916.md:643-655`, R-16's
own account). That act is **out of this cell's scope**: it is a deploy-gate/ledger question about a
past mint, not a question the `targets` classifier's correctness can answer either way. Nothing in
this cell verifies, re-verifies, or reopens it.

## Not claimed

- No code changed: `lib/opal_naming.py`, `.tools/safe_deploy_core.py` and every file under
  `infra/logic/registry/` are outside this cell's grant and untouched (`git status` after this cell's
  work shows only this record and the surprise channel, if a row is filed).
- Nothing live moved: `generate()` was never invoked.
- This record does not re-derive R-26's ruling; it re-measures the tree R-26's build landed on and
  reports the numbers.

## Criteria

- `G27R4-AC1` (`g27-plane-instruments`): `PASS-G27-PLANE-INSTRUMENTS` (unchanged from the issuer's
  cut measurement, re-verified above).
- `G27R4-AC2` (`g27-disposition`): this record itself; expected `PASS-G27-DISPOSITION` once
  committed (FIXED shape: the word "fixed" and "safe_deploy_core" both present above).
- `G27R4-AC3`: JUDGMENT, for `3.0.0_SA_CVO` at L9. Recorded `UNVERIFIABLE-BY-INSTRUMENT` in the proof
  instance, `status_reason` naming `3.0.0_SA_CVO`. For the CVO's read: this disposition follows from
  the numbers printed above (target count, per-plane counts, 5 distinct instruments, the
  hash-pinned-consumer census line), not from S60's own prose, and it states plainly (the section
  above) what a passing `targets` read does not prove.
