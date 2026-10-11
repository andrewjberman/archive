# IRPT_ANLREQ release 1 REVISION 6 -- irpt-status from ONE commit (IB-pr-416's build) -- never-widen pair

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2` (or the CTO's named substitute). **Live-call actor:** `2.0.0_SA_COO~G2`.
Supersedes revision 5 (`NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV5_IRPT_STATUS.md`), which went live at 2026-10-09T17:42Z, raised
`TypeError RetentionPolicy.reference() takes 3 positional arguments but 4 were given` at 17:57:56Z and was rolled back to rev 3 at 18:02Z
(row `IRPT_YCDGEN-D2-S24`; TO-APPLY-Y1 AMENDMENT 7).

**COO half: SIGNED by this file, 2026-10-11 ~03:2xZ.** CTO half: owed (section 7).

This pair signs the irpt-status function ONLY. `irpt-performance-adapter` and `irpt-narrative` are `2.0.0_SA_COO~P2`'s, on the IB-pr-416 packet.

## 1. What is different from revisions 4 and 5

- Revisions 4 and 5 re-pinned members one at a time; each left a sibling older than its caller. CTO msg 3856: no more member re-pins.
- This revision is NOT built by this seat. It is IB-pr-416's irpt-status build (issuer `2.0.0_SA_COO~P2`, worker `0.9.0_WK_IRPT_BCKEND~278`; order
  complete @c2644f24a4, read by this seat in the shared tree). Every investor-reporting member comes from commit `361c44fa9d`.
- Evidence this half reads: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md`,
  blob `43ea93d2ee` (`git hash-object` by this seat equals the blob `2.0.0_SA_COO~P2` names in msg 3954). Section 3 below quotes it; it is the
  builder's report, re-run by its issuer, and is NOT re-measured by this seat. The applier re-measures on the UPLOADED zip (section 5).

## 2. Pin and artifact

- **Built** (packet, built twice identical): `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`, 361122 bytes, 49 members.
- **Pin: NOT YET A COMMIT.** The packet built from a candidate map through `BAU_SOURCE_MAP_OVERRIDE`. The real map
  `infra/aws/lambda/ci/lambda-source-map.json` does not carry the entry (measured by this seat 2026-10-11 ~03:2xZ: the `functions/irpt-status` entry of the
  real map is not equal to the candidate's). Landing it is `2.0.0_SA_COO~P2`'s act (row `IRPT_BCKEND-D2-W278-S2`, ARMED). The pin is the commit that
  lands it, on origin. TO-APPLY-Y1 AMENDMENT 8 names that commit; this half is signed against the BUILT SHA, so a build at the pin that does not print
  `6idtFvAm...` is an ABORT, not a re-sign.
- **Live now / ROLLBACK:** rev 3 `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`, LastModified 2026-10-09T18:02:51Z (read by this seat 2026-10-11
  ~02:36Z and ~02:51Z). Its object version per the rev 5 ledger and the packet is `iDIQPfNUQM8EH4pjrG.codFMMaR071yi`. The applier re-reads both at step 0
  and records the version it replaces.
- **Writers of the property (irpt-status's code): N = 1.** `module "irpt_status"` at `infra/aws/terraform/investor-reporting/ops/lambda.tf:18`
  (function name at `ops/main.tf:64`); found by a search of every `.tf` under `infra/aws/terraform` for the module, the function name and the artifact
  key, 4 lines in 2 files, all in the `investor-reporting/ops` root. No other root, no schedule and no pipeline writes the function's code.

## 3. Gates at the build (quoted from the packet; the applier re-reads them on the uploaded zip)

| gate | reading |
|---|---|
| per-member diff of the BUILT zip vs live rev 3 (both 49 members) | **13 changed**, 0 added, 0 removed: `composition.py`, `data/custodian_key_seam.json`, `durable_job.py`, `entry.py`, `ids.py`, `interactive_access.py`, `loaders.py`, `owned_report.py`, `repository.py`, `resident_installed.py`, `retention.py`, `served.py`, `status_installed.py` |
| signature closure, name / attribute / method limbs | 0 / 0 / 0 mismatches (calls=129, attr_checked=60, method_call checked=243). Live rev 3 reads 1 / 0 / 0 (`InteractiveAccess(profile_reader=)`) |
| method-call limb's negative control | the rev 5 pairing reads 2 mismatches, `.reference(4 positional)`: the live rev 5 failure, so the limb can see this class |
| untested import pairings (`pin_coherence.py`) | live 21 -> built 0 |
| replay, live zip against built zip | 42 binding cases over 7 routes: none differing. 7 method-call arms (one per route): 0 call-arity errors. Verdicts `identical` or `expected-diff` only |
| ADDENDUM 18 red list at the pin | 2 failed, 198 passed; both failures are `analysis-request-original` contract tests in `_contracts`; 0 intersection with the changed members |

Limit stated by the packet and carried here: the replay stores are in-memory fakes answering empty, so no retained-record path ran on real rows.
ABSENT != EXERCISED-AGAINST. The live reads in section 5 are the only exercise against real rows.

## 4. Blast radius (what moves on irpt-status, and what does not)

One tree means every member that lagged arrives with the commits in between. What rides beyond revision 5's three members:
- `retention.py` (bdd74e5f9b90 -> 9da406b7d6e4): commits `3fc99be70f`, `20534db618`, `f60e6f1d2a`. This is the co-staging rev 5 lacked.
- `repository.py` at its HEAD blob, which INCLUDES `3fc99be70f`. **TO-AR-y-21 AMENDMENT 9 deliberately dropped that commit** (IB-pr-386 and AR-t-12's
  svc-commentary admission). This revision carries it. That is the widening this half names and accepts: the one-tree rule (CTO msg 3856) outranks
  the member-level exclusion.
- `served.py` at its HEAD blob (`1cb1c965f3`, IB-pr-405): adds `analysis-request-read` to svc-custody-statement's operations.
- `interactive_access.py` (`c101699a71`): closes the `profile_reader` split on the internal-caller CREATE path.
- `resident_installed.py` (three commits), `owned_report.py` (three), `entry.py`, `durable_job.py`, `loaders.py`, `ids.py`,
  `data/custodian_key_seam.json`: each named with its commits in the packet's section 3.

**Widens:** irpt-status reads the Opal research family under its registered revision (the purpose of revisions 4 and 5); svc-commentary is admitted
on the retained path (`3fc99be70f`); svc-custody-statement may call `analysis-request-read` (IB-pr-405).
**Does not move:** any route (the `/original` route stays exactly 1), IAM, any environment variable, any layer, any schedule, any table, any other
function under this pair. That irpt-status's routes do not reach the changed `put` paths is INFERRED from its route table, not measured.

## 5. After-reads (the applier's, in order)

- **R0:** live at start == `t6OJTCcm`. The per-member diff of the UPLOADED zip against LIVE (read via `get_function`, never the S3 key the upload
  overwrote) is EXACTLY the 13 members of section 3, otherwise STOP. SHARED-ROOT STOP: `irpt-performance-adapter`'s first apply
  (`2.0.0_SA_COO~P2`) is ahead of this one; if another seat holds an open ledger or plan on `investor-reporting/ops`, STOP and report.
- **R1:** on the UPLOADED zip, downloaded back by version: symbol closure missing=0, and the three signature limbs each 0 mismatches
  (`signature_closure.py`, `signature_closure_attr.py`, `method_call_limb_416.py`).
- **R2:** live == `6idtFvAm`, re-plan 0, the `/original` route count is 1.
- **R3 (live-call arm; the ledger does NOT close before it):** one GET `/api/scoped/investor-reporting/status` for a non-49F caller within a minute of
  the promote. Then irpt-status 5xx and `TypeError` counts both 0, counted from the promote UNTIL `2.0.0_SA_COO~G2`'s reads have finished, with START
  lines printed PER TENANT (49financial and cottonwood) as the denominators. A window that closes before ~G2's reads, or a denominator holding one
  tenant, is not R3. Rev 5 passed a 5-minute, one-tenant R3 and failed 8 minutes later on the other tenant.
- **R4 (`2.0.0_SA_COO~G2`, sr1 window):** `REQ-5e4149d2`'s owner read (status-job and analysis-report) answers with no `RetentionRefused` and no
  `TypeError`.
- **R5 (`2.0.0_SA_COO~G2`, same window):** one GET `.../analysis/requests/{id}/original` answers, and the object count stays 1 (the read does not write).
- Release 1's deferred reads 5 and 6 (the ticket-bound READY and `REQ-5e4149d2` served) are graded on this revision.

## 6. Both branches

- **Branch A (holds):** R0-R5 all met. Live stays `6idtFvAm`; the ledger closes; TO-APPLY-Y1's reads 5-6 are graded.
- **Branch B (rolled back):** R2 failing, OR any 5xx or any `TypeError` in the function's log group at any time inside the R3 window (an HTTP 200
  beside a logged `TypeError` is still Branch B), OR R5's count moving. Act: re-promote rev 3's object version through the same Terraform path
  (`safe-apply`; never `update-function-code`), then read live == `t6OJTCcm` and probe BOTH tenants.
- **Recorded, no rollback:** R4 answering a typed refusal that is not a `TypeError` and not a 5xx. It is recorded with its code and routed to this seat.
- This half does not predict which branch holds. The producer's rule that decides is the function's own log group and ~G2's two reads.

## 7. Owed before the apply

- The CTO half on irpt-status (this pair, or the irpt-status section of the IB-pr-416 half the CTO has been asked for).
- The source-map landing commit, on origin (`2.0.0_SA_COO~P2`, row `IRPT_BCKEND-D2-W278-S2`), which fixes the pin.
- `irpt-performance-adapter`'s apply closed on the shared `investor-reporting/ops` root, or its ledger not open.
- `2.0.0_SA_COO~G2`'s sr1 window, and the applier seated (asked of `0.0.0_AB_MSTR~DELL2` when AMENDMENT 8 is cut).
