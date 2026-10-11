# IRPT_ANLREQ release 5 -- irpt-status from ONE tree (pin ee3fd7c5e5), build `Iw3FADFr` -- never-widen pair, COO half

COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-11. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Shape ruled by `1.0.0_SA_CTO~DELL2` msg 4572 on row `IRPT_ANLREQ-D2-S36`: one re-pin of the whole entry to one merged commit, a fresh
build, a reach read, a pair; a census of the 12 members that leave an older pin; an after-read for each member that changes a served
answer; rollback `6idtFvAm`. This half signs the ACT'S BLAST RADIUS and both branches. It does not sign any producer's decision.

Claim words below: MEASURED = this seat ran it; WORKER = worker `0.9.0_WK_IRPT_ANLREQ~53`'s census, with the worker's own claim word;
INHERITED = read in another seat's record and not re-run.

## 1. Artifact and pin

- **Built** (MEASURED, this seat's own BUILD_ONLY on the worker's branch; the worker built it twice identical):
  `Iw3FADFrSt5G97zRTSkvZ7txSlXnaNQNpgPZi+G5tw0=`, 49 members; the worker records 376087 bytes.
- **Source map entry** `functions["irpt-status"]` of `infra/aws/lambda/ci/lambda-source-map.json`: 42 of 42 `staged_from` rows at pin
  `ee3fd7c5e520243e1a3f58a6b86d22bfc2b1e4d3`, 0 rows whose sha256 is not the blob at the pin (MEASURED: check `y33-repin` prints
  `Y33-REPIN-OK`). Seven further members come from `files[]`, taken from the building commit's tree.
- **The building commit:** the shared-tree merge `ece5ad3477` (it carries the re-pinned map), or a descendant of it, ON ORIGIN. At this
  signing it is LOCAL. The applier builds at a commit it has read on origin; a build that does not print `Iw3FADFr...` is an ABORT, never
  a re-sign.
- **Live now / ROLLBACK:** revision 6, `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`, LastModified 2026-10-11T04:44:47Z (MEASURED
  2026-10-11 ~09:2xZ). The applier re-reads it at step 0 and records the S3 object version it replaces.
- **Writers of the property (irpt-status's code): N = 1.** `module "irpt_status"`, `infra/aws/terraform/investor-reporting/ops/lambda.tf:18`
  (the module line MEASURED today; the search of every `.tf` for other writers is INHERITED from the revision 6 pair, section 2).
- **`artifact_sha256` in the map still reads the live digest** and moves only at the apply's own record step. The entry's other
  applied-artifact fields are stale and untouched (row `IRPT_ANLREQ-D2-S33`).

## 2. What moves: 14 of 49 members against the live zip (MEASURED, member-by-member sha256; 0 added, 0 removed)

Two come from `files[]` at the building commit and BOTH change served answers:

| member | change | served effect |
|---|---|---|
| `owned_requests.py` | cell AR-y-32 (`94713492d8`, `ec09824a59`) | history rows gain `client_id` and `client_claim` (SELECTED / UPLOAD / UNREADABLE); the page gains `unreadable_rows` |
| `prospect_dates.py` | cell AR-y-32 (`94713492d8`) | the section-date census reads an `OPAL_ENGINE` report by its own branch (status VALUE / NOT_AVAILABLE) |

Twelve leave an older pin. Census: `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~53/release5/REPIN_CENSUS_IRPT_STATUS.json`
(blob `89725a4ba9`), which carries each member's owning commits and the reading in full.

| member | old pin | owning project(s) | commits | served effect | claim | why, in one line |
|---|---|---|---|---|---|---|
| `owned_report.py` | 361c44fa9d | IRPT_ANLREQ AR-y-32 | 1 | CHANGES SERVED ANSWER | WORKER measured; this seat counted 7 `retained_ref` in the built member | `sections()` adds `retained_ref` |
| `acceptance.py` | 361c44fa9d | IRPT_ANLREQ AR-y-37 | 1 | INERT | WORKER inferred; MEASURED by this seat: 0 `.accept(` call sites in the 49 packaged modules | the changed writer is never called here |
| `resident_installed.py` | 361c44fa9d | IRPT_ANLREQ AR-g-31 | 1 | INERT | WORKER inferred; MEASURED by this seat: `make_packager` is named only in its own file | irpt-status imports `make_authorize` only |
| `loaders.py` | 361c44fa9d | IRPT_LIVE_SCOPE | 1 | INERT | WORKER measured | comment only; the syntax trees are equal |
| `firm_registry.json` | 80a79a7462 | regenerated carriers (XB-282f) | 1 | INERT | WORKER measured | only the generated header differs |
| `lib/opal_naming.py` | 80a79a7462 | ADVI_FIRMBKTS, MDPF_CANON, LGIC_ENFORCE, LGIC_BLANKFIX, NFRA_CTLPLN, ADVI_COTBKF, XB-282f | 21 | INERT | WORKER measured | the four entry points irpt-status calls return equal results on both trees (171 destinations), bar the row below |
| `NAMING_SCHEMA.json` | 80a79a7462 | LGIC_BLANKFIX, NFRA_CTLPLN | 5 | INERT | WORKER measured | same two-tree run |
| `registry/reporting_policies.json` | eab13e88d3 | IRPT_ANLREQ TO-APPLY-t1 | 1 | INERT | WORKER measured | flips `irpt-anlreq-x10-v1` to ACTIVE; irpt-status reads `irpt-x10-v1`, not that row |
| `registry/exemptions.json` | 80a79a7462 | NFRA_CTLPLN | 4 | INERT | WORKER measured | no called entry point reads a row of it |
| `registry/resources.json` | 80a79a7462 | LGIC_BLANKFIX | 1 | INERT | WORKER measured | removes a layer row nothing here selects |
| `registry/scopes.json` | 80a79a7462 | ADVI_COTBKF, LGIC_CANON, IRPT_DASHBD | 3 | INERT | WORKER measured | `lookup()["long"]` equal for the three tenants |
| `registry/systems.json` | 80a79a7462 | NFRA_IAMROLES202609, MDPF_DEMQUE, LGIC_BLANKFIX, ADVI_COTBKF | 5 | INERT | WORKER measured | read only by `name()`, which no packaged module calls |

Limits of the INERT readings, stated: they cover the entry points irpt-status calls TODAY with the arguments it passes; two are readings
and were not executed. An INERT member that turns out to change an answer is a FAILED after-read in section 4 and takes the rollback.

## 3. What does not move, and the reach read

- Reach read on this seat's own build of `Iw3FADFr` (MEASURED):
  `reach_read routes=7 handlers_walked=434 of 559 put=0 reserve=0 get_ac=0 count=0 verdict=PROCEED`; no `repository.put` and no
  `retention.reserve` definition is reachable. Record: `release5/REACH_READ_IRPT_STATUS_Iw3FADFr.json`. The walk is static and
  over-approximates; a dynamic `getattr` dispatch is invisible to it. One sub-directory member is not walked, as on revision 6.
- Routes: 7, the same seven as revision 6. No route is added or removed (the member set is unchanged: 49 and 49).
- No Terraform resource other than the function's code changes: no role, no policy, no environment variable, no route, no schedule.
  The plan must show exactly ONE resource to change (the function, `source_code_hash` and the S3 object version); anything else is an ABORT.
- No other function moves. `irpt-ycharts-generate` is a separate release under its own pair (23 of 88 pinned members older than HEAD).
- No data moves: the function's declared routes write nothing (reach count 0), and the apply writes one S3 code object.

## 4. After-reads (the applier's, in order; every one recorded with its claim)

| # | read | expect |
|---|---|---|
| R0 | `get-function-configuration` before: `CodeSha256` | `6idtFvAm...`; record the S3 object version being replaced |
| R1 | the same after the apply | `Iw3FADFr...` |
| R2 | `GET .../analysis/{jobId}/sections` for a READY owned job, as its owner (`owned_report.py`) | the body carries a `retained_ref` object; before the apply the key is absent; `provider`, `request_ref`, `sections` unchanged |
| R3 | `GET .../analysis/requests` (history) as an owner with at least one accepted request (`owned_requests.py`) | every row carries `client_id` and a `client_claim` in SELECTED / UPLOAD / UNREADABLE; the page carries `unreadable_rows`; the row count equals the count before the apply |
| R4 | the section-date read of a request whose report is `provider: OPAL_ENGINE`, if one exists in a readable tenant (`prospect_dates.py`) | dates are served, not `SECTION_DATE_CENSUS_INVALID`. If no such request exists, record R4 as ABSENT with the census that shows none: ABSENT is not EXERCISED |
| R5 | a YCHARTS-provider request's section-date read (the control of R4) | the same dates as before the apply |
| R6 | release 1's reads 3a, 3b, 4_record, 4_route, re-run (`ar3_checks.py y34-reads` shape) | all true, as on revision 6 |
| R7 | S3 object versions under the R6 request's three artifact directories, before and after R6 | equal (3 and 3 on revision 6); DynamoDB is not counted and the record says so |
| R8 | `GET .../status` once per readable tenant, before and after (the control for the eleven INERT members: naming, registry and scope readers run on every request) | the same HTTP status and the same top-level keys as before the apply |

The laptop holds the decrypt for `irpt-requests`; dell2 does not. R2 to R7 are the laptop applier's, as on revision 6.

## 5. Both branches

- **All of R1 to R8 as expected:** record in the ledger, close it, and the map's `artifact_sha256` moves to `Iw3FADFr...` by the record
  step. The issuer flips the apply order and tells `2.0.0_SA_COO~D2` and `2.0.0_SA_COO~G2` the release is live.
- **R1 wrong, the plan shows more than one resource, or any of R2 to R8 fails:** ROLL BACK in the same session to `6idtFvAm...` (the S3
  object version recorded at R0), re-read `CodeSha256`, close the ledger ROLLED_BACK, and file a row naming the read that failed. No
  second attempt without a new pair.
- **Half-landed** (S3 object replaced, function not updated, or the reverse): finish or roll back in-session; never leave it.

## 6. Owed before the apply

- The CTO half on this file's blob.
- `ece5ad3477` (or a descendant) on origin: the integrator's window. The applier reads it there.
- A NEVER-2 ledger entry opened at the start by the applier; no other open entry on the `investor-reporting/ops` root (every live
  worktree read, per the law).
- The apply order, cut by this seat when the CTO half is in.
