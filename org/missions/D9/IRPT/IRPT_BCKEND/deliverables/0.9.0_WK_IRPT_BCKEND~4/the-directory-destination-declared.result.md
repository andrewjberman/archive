# IB-rtd-6 RESULT -- the directory destination declared at its LGIC address, and the move packeted

**Cell:** `IB-rtd-6` (decomposition v0.4 s.R4). **Order:**
`IRPT_BCKEND.TO-IB-rtd-6.the-directory-destination-declared-at-its-lgic-address-and-the-move-packeted.md`.
**Worker:** `0.9.0_WK_IRPT_BCKEND~4`. **READ-ONLY on every live plane and the registry -- nothing applied.**
Battery: `battery_ib_rtd_6.py`; output: `IB-rtd-6_R46-AC1_battery_output.txt`; packet:
`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtd-6.md`.

---

## (a) THE ADDRESS, BUILT -- 3 of 3, zero refusals, zero registry rows needed

Tier: **gold** (firm-attributable data). `infra/logic/registry/tiers.json:9-17` @22e86e55f5, `homes.FIRM.gold`
= `{"home": "scope", "rule": "R5; R7 ... firm bucket, MANDATORY"}`. Doctrine:
`infra/logic/02_DOCTRINE.md` R5 `:370-378` "GOLD LIVES IN A PER-PRODUCT OR PER-FIRM BUCKET" + R7 `:401-409`
"ATTRIBUTABILITY DECIDES TENANCY ... firm bucket, gold AND platinum, MANDATORY", grammar R1 `:149-166`
SOURCE-FIRST (superseded 2026-09-13, Andrew-direct card 1) -- all @afd81beb8ad.

Source: **`irpt`** (`infra/logic/registry/systems.json:28-36` @23980d3fbe -- class PRODUCT, long
`investor-reporting`, `owner_directive: D9`, `owner_claim: measured`, basis "mission tree
`org/missions/D9/IRPT/`"). Table: `directory`. Partition: an illustrative date (the grammar is
date-independent; the real value is set by the runner at write time -- round-3 analysis s.4 forward-looking
bar, `IRPT_BCKEND_ROUND3_ANALYSIS.md` @5c59f68d70).

`lib/opal_naming.py` `address()`/`key()` `:1542-1571` @6c87bd0968:

| firm | directory.json | _refresh manifest |
|---|---|---|
| 49financial | `s3://opal-data-49financial/irpt/49financial/gold/directory/<date>/directory.json` | `.../_refresh/manifest.json` |
| inflection | `s3://opal-data-inflection/irpt/inflection/gold/directory/<date>/directory.json` | `.../_refresh/manifest.json` |
| cottonwood | `s3://opal-data-cottonwood/irpt/cottonwood/gold/directory/<date>/directory.json` | `.../_refresh/manifest.json` |

**All 6 calls (3 firms x 2 objects) built cleanly. 0 refusals.** `infra/logic/registry/scopes.json` @22e86e55f5:
49financial `:14-118` (`bucket_provisioned: true`), inflection `:119-156` (`bucket_provisioned: false`),
cottonwood `:157-202` (`bucket_provisioned: false`) -- `bucket_provisioned` is not read by `address()` (it
builds the address regardless), so the clean build does NOT mean the bucket exists; see part (d).

**No registry row is drafted.** Rule 30's refusal contingency ("a builder REFUSAL is a missing registry row")
does not fire: every call resolved against the CURRENT registry with no `RegistryError`/`ValueError`. R46-AC2
records for the CVO whether any OTHER registry action (a `bucket_provisioned` flip, see part c) is owed.

---

## (b) THE CENSUS

**Readers, unscoped over the corpus (`comp-find 'investor-reporting/directory'`):** 485 hit(s) across
35,639 file(s) scanned (6 EPHEMERAL-FLOOR + 2,278 BINARY not searched); bands HEAD=57 DEF=10 SURFACED=58
CONFIG=92 TEST=7 DOC=261 -- battery output lines 34-67.

**Readers, scoped by project:**
- **This project (IRPT_BCKEND Lambda source, `infra/aws/lambda/investor-reporting/`):** 42 hit(s) across
  204 file(s); the 5 DEF hits are the actual reader constants: `_authz/loaders.py:30`,
  `directory/handler.py:53`, `directory/refresh.py:70-71`, `holdings/handler.py:53` (each
  `DIRECTORY_PREFIX = os.environ.get("IRPT_DIRECTORY_PREFIX", "investor-reporting/directory")` or its
  REFRESH_PREFIX sibling) -- all `investor-reporting/` Lambda source, vintages @39cbad4214 (loaders,
  ds-precommit-check, firm_registry), @48313e9c0e (handler), @a4db909717 (refresh), @5a359024a9 (holdings
  handler). **Every direct S3 reader of the legacy prefix lives in this project's own Lambda tree.**
- **`portal/`:** 0 hit(s) across **0 file(s) scanned** -- the gitlink is UNINITIALIZED in this worktree
  (`git ls-tree HEAD portal` = `160000 commit 2453a7b4c6...`, no `.gitmodules`, `portal/src` absent). This
  is OUT-OF-CORPUS, not an absence claim (CLAUDE.md s.3 scoped-coverage rule); filed as a surprise row
  (below).
- **`org/missions/D9/IRPT/IRPT_FNTEND/` mission tree:** 12 hit(s) across 176 file(s) (77 BINARY not
  searched) -- every hit is a PROOF-OF-SPEC/result/investigation artifact citing the API ROUTE
  (`/api/scoped/investor-reporting/directory/search|resolve`), never an S3 key. **No FE code reads the S3
  object directly**; the FE consumes the API contract, which the Lambda handler mediates.

**Writers -- the DS's `writer_census_ib_rtc_6.py` instrument re-run LIVE** (`org/missions/D9/IRPT/IRPT_BCKEND/
deliverables/0.4.0_DS_ClientPlatform~X/writer_census_ib_rtc_6.py` @474bdf1dc2), subject `s3:PutObject` on
`opal-data-bd/investor-reporting/directory/2099-01-01/directory.json` (the 49 Financial legacy destination
per `data/firm_registry.json` @39cbad4214):

- RESOURCE plane: bucket policy 2 statements (both CloudFront `GetObject`), 0 allow a write, 0 Deny.
- IDENTITY plane: **263** principals simulated (256 roles, 7 users), 0 unsimulated, 0 UNKNOWN.
- **WRITERS: 12 of 263** -- 8 `bd-*` roles, `mdpf-daily-runner-ec2-role`, and users `Andrew_Berman`,
  `Andrew_Berman_Console`, `Opal_Terminal`.

This instrument is scoped to the 49 Financial/`opal-data-bd` destination only (hardcoded
`firm_id="49financial"`); no equivalent instrument exists yet for `opal-data-inf`/`opal-data-cot` (inflection/
cottonwood's LEGACY destinations) -- named as a gap for `IB-rtd-7`, not built here (READ-ONLY bound).

---

## (c) THE MOVE, PLANNED

Full text: battery output lines 184-240 (`PORT_PLAN`). Summary:

1. **Write model:** the host (`mdpf-daily-runner-ec2-role`) cannot be granted `PutObject` directly on
   `opal-data-49financial` -- its ARN does not match the fence's admit glob `role/*-49f-*` (measured live,
   part d) -- so the write grant uses the SAME assumed-principal shape IB-rtc-6/7 used for reads: one
   builder-named role per firm (`name('irpt', <firm>, 'directory-write', 'role')`), assumed only by the
   host, PutObject on that firm's own LGIC address only.
2. **Artifacts touched (named, not edited):** `directory_runner.py` PROD_PREFIX/destination logic; the four
   Lambda `DIRECTORY_PREFIX`/`REFRESH_PREFIX` readers; `FirmDestinationPolicy`'s bucket source (a gap: today's
   `data/firm_registry.json` carries the ROUTED legacy alias, not `opal-data-{firm}`, so a new field or
   lookup is needed -- drafted, not built); `.tools/ds-precommit-check.py`'s GENERATED
   `_CROSS_FIRM_FOREIGN_BUCKETS`/`_KEY_PREFIXES` (`:69-117` @39cbad4214, `_separations()` in
   `lib/opal_naming.py`) -- these regenerate automatically once `bucket_provisioned` flips, never a hand
   edit; the two Terraform roots this order's `<paths>` grants.
3. **Provisioning gap (measured live):** `opal-data-inflection` and `opal-data-cottonwood` **do not exist**
   (`NoSuchBucket`, battery output lines 251-259). 49 Financial can port alone; the other two firms are
   gated on provisioning their FIRM buckets first -- a prerequisite this order does not perform.
4. **Retirement window:** the legacy prefix retires (readers + writer repointed) in the SAME apply as the
   new grant, never mirrored; rollback = revert the repoint in one apply, legacy objects untouched.
5. **IRPT_FNTEND hand-off (named, addressed to `2.0.0_SA_COO~F`, not this project's edit):** the FE never
   touches the S3 path (0-hit `comp-find` for `'s3://'` and for `'as_of|source_key|directory.json'` over
   `docs/contracts/investor-reporting/`) -- **the port costs IRPT_FNTEND no code change.** The named
   hand-off is a RE-VALIDATION cell: re-run the live-server directory-search/resolve smoke suite once after
   `IB-rtd-7` lands, as a regression confirmation -- distinct from round-3 analysis s.9 item 3 (the per-firm
   as-of consequence), which is IRPT_FNTEND's own already-named round-4 item.

---

## (d) THE PACKET

Written separately: `NEVER_WIDEN_SIGNOFF_PACKET_IB-rtd-6.md`. Live inputs gathered here (battery output
lines 243-298):

- **Fence re-read, `opal-data-49financial`** (live `s3api get-bucket-policy`): `DenyForeignFirmPrincipals`,
  `Deny s3:* Principal *` unless `ArnNotLike aws:PrincipalArn` matches `role/*-49f-*` or one of 16 named
  exemptions. `mdpf-daily-runner-ec2-role` matches neither -> **DENIED for PutObject exactly as it was for
  GetObject** (`infra/aws/terraform/mdpf-pipeline/iam.tf:598-628` @8d18193bcc).
- **`opal-data-inflection` / `opal-data-cottonwood`:** `NoSuchBucket` (live) -- no fence exists to re-read;
  named as the provisioning-gap stop condition, not a K-key.
- **Baseline `terraform plan`, both roots this order's `<paths>` grants:** `investor-reporting/directory` ->
  **No changes**; `mdpf-pipeline` -> **0 to add, 1 to change** (the SAME pre-existing `mdpf_route_bindings`
  CRLF drift IB-rtc-6 already found and excluded -- unchanged, not this act's).
- **Writers-before:** the 12-of-263 writer census above is the BEFORE state `IB-rtd-7` re-reads after any
  apply.
- **Negative control, designed:** NC1 host writes a 49F LGIC key without assuming the write-principal ->
  AccessDenied; NC2 the 49F write-principal writes an INFLECTION/COTTONWOOD LGIC key -> AccessDenied; NC3
  the EXISTING 49f READ principal (`irpt-49f-directory-read-role`) attempts any write -> AccessDenied (a
  separate role, never widened). Proof shape mirrors IB-rtc-6's N1-N5 (SSM command id + error code at the
  event, R-40).

---

## R46-AC2 -- for `3.0.0_SA_CVO` (judgment; no verdict here)

**Conformance framing.** Two readings, both grounded, presented without a verdict:
- **This project's own conformance:** the directory pipeline is NEW -- built entirely inside D9/IRPT_BCKEND
  this quarter (`IB-s-1` on), not inherited from a pre-LGIC monolith. Rule 30's carve-out ("existing
  pipelines... reach conformance through their own migration project, never a rider") reads as NOT applying
  to a pipeline that never had a pre-LGIC form to migrate FROM.
- **A D14 rider:** the pipeline's CURRENT destination (`opal-data-bd`/`-inf`/`-cot`) is the estate's still-live
  routed alias (`_routed_bucket()`, `scopes.json` "routed": true), which every OTHER firm-facing surface
  reads today pending D14's full-name cutover; moving ONE pipeline off it early is itself a partial,
  out-of-order migration of a shared routing fact (MEMORY.md: "legacy bd/inf/cot buckets ACTIVE until D14").
- **What breaks the tie for 49financial only:** its NEW LGIC bucket (`opal-data-49financial`) and its fence
  ALREADY EXIST and are LIVE (measured, part d) -- nothing about D14's timeline blocks that leg. Inflection
  and cottonwood's NEW buckets do not exist; provisioning them may itself be D14-scoped work.

**Registry rows the builder needs:** **NONE** -- part (a)'s 6 of 6 calls built without refusal. No R20
departure is implicated by `address()`/`key()`. A SEPARATE, non-`address()` registry question is real:
`data/firm_registry.json`'s consumer-facing `bucket` field carries the ROUTED legacy alias, not
`opal-data-{firm}`; whether a generated field is added for the LGIC bucket (a DEC-5 view change,
`infra/logic/registry`-owned) or the runner does a second `lookup()` call is the CTO's L4 call, not this
order's.

**What the port costs IRPT_FNTEND:** no code change (part c, item 5); one re-validation smoke run, named as
a hand-off to `2.0.0_SA_COO~F`, not built or committed by this project.

---

## Surprises filed

- `IRPT_BCKEND-W4-S33` -- `portal/` is an uninitialized gitlink in this worker's worktree (no `.gitmodules`
  mapping, `portal/src` absent), so the task order's named census location returns a MEASURED 0-of-0
  (out-of-corpus), never an absence claim. OBSERVATION, INERT, UNDER_INVESTIGATION.
