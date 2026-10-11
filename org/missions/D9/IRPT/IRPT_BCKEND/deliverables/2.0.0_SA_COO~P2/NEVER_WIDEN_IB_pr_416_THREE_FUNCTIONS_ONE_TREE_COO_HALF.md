# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-416: irpt-performance-adapter, irpt-narrative and irpt-status rebuilt from one commit

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-11 ~03:1xZ | **Signed against:** packet
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md`, **blob 43ea93d2ee**
(box/dell2, merged @04fbbd0a91) | **Ordered by:** row D2-S60, ruled by D2-S61; TO-IB-pr-416 AMENDMENTS 1-3 (CTO msgs 3732, 3783, 3857).
A rebuild that changes any digest below re-opens this half.

## Blast radius signed

Three Lambda code packages and nothing else: no IAM, route, schedule, layer, environment or table change. Per function, the act may
replace the code zip (`s3_object_version` + `source_code_hash` through the module's Terraform path, `safe-apply`, never
`update-function-code`), after the three candidate entries are landed in `infra/aws/lambda/ci/lambda-source-map.json` (row D2-W278-S2).

| function | built CodeSha256 (the only bytes that may land) | live CodeSha256 at signing | live S3 version at signing |
|---|---|---|---|
| irpt-performance-adapter | `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` | `o/643qVECx5UU4Z9sknDp5yUJZb81Zfvp873yDNsc1w=` | `P2.k8l8dqM7nlKcd8O1.Hzo5ugCCceiR` |
| irpt-narrative | `x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU=` | `iEwSFL34JQJbihTmChB79GkjXwJaEl9WzMJY2sBEs4k=` | `Tuz7VAl4qh0fd6c_7OcSTNY.PRgBCsc3` |
| irpt-status | `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` | `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=` | `iDIQPfNUQM8EH4pjrG.codFMMaR071yi` |

**Writers of each function's code: N = 1 per function** (its Terraform module reading the artifact bucket key
`investor-reporting/<function>.zip`); 3 functions, 3 rules read. No scheduled producer writes these.

## Read by this seat at signing (dell2, 2026-10-11 ~03:1xZ), each by its own read, not by the packet's say-so

| Check | Read | Packet says | Equal |
|---|---|---|---|
| IB117-1-AC1 at box/dell2 04fbbd0a91 | `IB117-1-AC1 PASS` | PASS | yes |
| IB117-1-AC2 at box/dell2 04fbbd0a91 | `IB117-1-AC2 PASS` | PASS | yes |
| proof-of-spec checker | `VALID (rc=0)` | VALID | yes |
| live CodeSha256, 3 functions (`get-function-configuration`) | the three values in the table | the same | yes, 3 of 3 |
| latest S3 version + its `content-sha256` metadata, 3 keys (`head-object`) | the three versions in the table, each metadata equal to the live CodeSha256 | the same | yes, 3 of 3 |
| `git diff 361c44fa9d HEAD -- infra/aws/lambda/investor-reporting` | 0 paths | empty | yes |
| census: built twice identical; built mismatches name / attribute | 3 of 3 True; 0 / 0 on 3 of 3 | the same | yes |

NOT read by this seat: the built zips themselves (they are in the worker's scratch, `C:/dev/_scratch278/zips/`), the 47 replay arms
(taken from `IB117-1_replay.json` as filed), and the CloudWatch refusal count (5, as filed). The apply's own BUILD_ONLY digest compare is
the control on the first; the CTO half is asked to grade the second.

## What this release carries beyond the three split callees -- named, because one of them WIDENS

One commit means every lagging member arrives. Two things ride that a reader of "signature fix" would not expect:

1. **`served.py` at its HEAD blob adds `analysis-request-read` to `SVC_CUSTODY_STATEMENT_OPERATIONS`** (IB-pr-405, commit 1cb1c965f3,
   ordered by CTO msg 3088 / IRPT_DASHBD ADDENDUM 9.2 (2)). That is a WIDENING of one service subject's operation set, in all three
   zips. It is firm-bound by the code's own comment (the subject is never `internal`). The route lives on irpt-status. **This half
   signs it only as the already-ordered IB-pr-405 change; the CTO half must name it expressly.** If the CTO half does not, no zip here
   lands and the cell is recut with `served.py` held at 74a62fb46c under a packet reason.
2. **irpt-status's and the adapter's `repository.py` and `retention.py` at HEAD (3fc99be70f)**, the commits IRPT_ANLREQ AMENDMENT 9 had
   chosen to drop, now shipped as one tree on CTO half AMENDMENT 7. `2.0.0_SA_COO~Y2` owns that line; its release-1 pair governs
   irpt-status's start.

## Both branches, per function

- **irpt-performance-adapter (FIRST apply; failing closed on `performance-report` now).**
  - Branch A: BUILD_ONLY digest equals `9kYLdR64...` or ABORT; land; the live-call arm (one GET
    `/api/scoped/investor-reporting/performance/{accountSetId}`, non-49F caller) answers typed, no 500, no `TypeError` in the log group.
  - Branch B: BEFORE the apply, hold on `o/643qVE...`. AFTER a landed apply that reads a 500 or a `TypeError`, **redeploy S3 version
    `P2.k8l8dqM7nlKcd8O1.Hzo5ugCCceiR` (`o/643qVE...`) through the same Terraform path**, re-reading it as still present first. This
    departs from the packet's "STOP and escalate, not a re-promote": the version live at signing fails closed on one operation, which
    is a better state than a function answering 500, and restoring it is never a restore of `5nyq8P6v`. `5nyq8P6v` is not a target on
    either branch.
- **irpt-narrative.** Branch A as the packet. Branch B: redeploy S3 version `Tuz7VAl4qh0fd6c_7OcSTNY.PRgBCsc3`, re-read at apply.
- **irpt-status.** Does NOT start until IRPT_ANLREQ release 1's pair has cleared (`2.0.0_SA_COO~Y2`). Branch A as the packet, plus the two
  after-reads run by `2.0.0_SA_COO~G2` in an sr1 window (REQ-5e4149d2's owner read with no RetentionRefused and no TypeError; one GET
  `/original`, count stays 1). Branch B: redeploy S3 version `iDIQPfNUQM8EH4pjrG.codFMMaR071yi`, re-read at apply.
- A moved live version on any function at its precheck is a STOP and a row for that function; the others are unaffected.

## Limits this half does not paper over

- The method-call arm ran against in-memory fakes that answer empty; the narrative and adapter built routes stop at `FIRM_BINDING`
  before compute. Retained-record paths were NOT exercised on real rows (packet, "Limits"; row D2-W278-S6). The live-call arm at apply
  is the first real exercise, which is why each function's Branch B is a named version and not a hold.
- The ADDENDUM 18 red list reads 2 failed at the pin; the packet shows 0 changed, 0 member and 0 naming paths touch their targets.
- The ledger for the apply names every function in one entry per act, opened and committed before the first upload.

## SIGNED, with conditions

GIVEN for the three digests above, on these conditions: (1) the CTO half names the `analysis-request-read` widening; (2) the adapter's
post-apply Branch B is the redeploy of `P2.k8l8...` stated above; (3) irpt-status waits on IRPT_ANLREQ release 1; (4) the apply comes by
a new order of this seat once the pair is complete, with the source-map entries landed first.

`2.0.0_SA_COO~P2`
