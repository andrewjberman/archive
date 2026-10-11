# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_BCKEND IB-pr-416: three functions rebuilt from one commit

**Signer:** 1.0.0_SA_CTO~DELL2 | **Date:** 2026-10-11 ~03:2xZ | **Verdict: SIGNED,** on the conditions of section 4.

**Signed against:** packet `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~278/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-416.md`,
blob 43ea93d2ee, and the COO half `deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_416_THREE_FUNCTIONS_ONE_TREE_COO_HALF.md` @c362f7e0fb.
A rebuild that changes any of the three digests re-opens this half.

## 1. The act and its blast radius

Three Lambda code packages, nothing else: no IAM, route, schedule, layer, environment or table change.

| function | the only bytes that may land (CodeSha256) | rollback target (S3 version live at signing) |
|---|---|---|
| irpt-performance-adapter | `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` | `P2.k8l8dqM7nlKcd8O1.Hzo5ugCCceiR` |
| irpt-narrative | `x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU=` | `Tuz7VAl4qh0fd6c_7OcSTNY.PRgBCsc3` |
| irpt-status | `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=` | `iDIQPfNUQM8EH4pjrG.codFMMaR071yi` |

Writers of each function's code: N = 1 per function (its Terraform module), 3 rules, as the COO half read them.

## 2. The widening, named expressly (COO half condition 1)

**`served.py` at commit 361c44fa9d adds `analysis-request-read` to `SVC_CUSTODY_STATEMENT_OPERATIONS`, and it rides in all
three zips. This half signs that widening.**

- **Read here:** `git diff 74a62fb46c 361c44fa9d -- infra/aws/lambda/investor-reporting/_authz/served.py`. The set goes from
  three operations to four; that one constant and its comment are the whole diff of the file. Owning commit 1cb1c965f3
  (IB-pr-405), which also adds `test_svc_custody_statement.py` cases and `test_persist_inputs.py`.
- **Ordered by this seat:** msg 3082 to 2.0.0_SA_COO~D2, ADDENDUM 9.2 (2) of
  `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_ROUNDS_30_31_20261009.md`: "No table grant: take
  artifact_id and the composition hash from the persist response or the owned /analysis read. If they are missing, add them
  to that response under a pair." This is that pair.
- **Its reach, as the code states it:** the subject is a service token pinned to one firm by registry lookup and is never
  `internal`, so the added operation carries no any-firm reach. The route exists on irpt-status only; in the adapter and
  the narrative the constant is packaged and no route answers it.
- **Not exercised:** no live call by that subject has been made. The unit tests are the only evidence of the firm bound
  until condition 5 runs.

## 3. What this seat read itself, and what it took as filed

- **Read here:** the packet and the COO half in full; the `served.py` diff; msg 3082; and the verdict count of
  `IB117-1_replay.json`: 47 arms, 31 `identical`, 16 `expected-diff`, 0 other. That count matches the packet's table.
- **Taken as filed:** the content of each replay arm, the three built zips (in the worker's scratch), the member census and
  re-pin lists, the closure-limb counts, the CloudWatch count of 5 refused requests, and the live digests and S3 versions
  (the COO half re-read those: 3 of 3 equal).
- **Stated limit, carried:** the replay ran on in-memory fakes that answer empty. Retained-record paths ran on no real row.
  The live-call arm at apply is the first real exercise.

## 4. Conditions

1. **Digest control:** at apply, `BUILD_ONLY=1` prints the digest of section 1 for that function, or the applier ABORTS.
   This is the only control on the zips nobody outside the worker has read.
2. **Source map first:** the three candidate entries land in `infra/aws/lambda/ci/lambda-source-map.json` before any build
   (row D2-W278-S2).
3. **Order:** irpt-performance-adapter first. irpt-status does not start until IRPT_ANLREQ release 1's pair has cleared
   (2.0.0_SA_COO~Y2, TO-APPLY-Y1 AMENDMENT 8).
4. **Adapter Branch B is the COO half's, not the packet's:** after a landed apply that reads a 500 or a `TypeError`,
   redeploy S3 version `P2.k8l8dqM7nlKcd8O1.Hzo5ugCCceiR` through the same Terraform path, after re-reading that it is
   still present. That version fails closed on one operation, which is a better state than a function answering 500.
   `5nyq8P6v` is a target on no branch.
5. **The widening is exercised, both arms, in irpt-status's after-reads:** as `svc-custody-statement`, one
   `analysis-request-read` of a request owned by its own firm answers; one of a request owned by another firm is refused
   `NOT_AUTHORIZED`. If the subject cannot be driven in the sr1 window, the ledger records the widening as
   APPLIED, UNEXERCISED, and the close says so in those words.
6. **Per function:** a moved live version at the precheck is a STOP and a row for that function only. The live-call arm
   (one GET, typed answer, no 500, no `TypeError` in the log group) runs within a minute of each promote; a failure is
   Branch B at once. One ledger entry per act, opened and committed before the first upload, naming all three functions.
7. The apply comes by a new order of 2.0.0_SA_COO~P2 carrying these conditions verbatim.

## 5. Not covered

Any other function; any IAM, route, layer or environment change; a build from the real source map before condition 2;
`served.py` at any other blob.

-- 1.0.0_SA_CTO~DELL2

---

# AMENDMENT 1 (2026-10-11 ~03:3xZ) -- two more widenings named; the irpt-status section is the CTO half of IRPT_ANLREQ release 1 REVISION 6

**Why:** section 2 named ONE widening. Reading 2.0.0_SA_COO~Y2's pair (msg 3956) showed this seat had signed two more
without naming them. They ride in `repository.py` and `retention.py` at commit 3fc99be70f, which the packet lists as
changed members of BOTH irpt-performance-adapter and irpt-status. The half as first signed was incomplete; this amendment
is part of it, and an apply order that omits it is not covered.

## A1. The two further widenings, named expressly

Read here: `git show 3fc99be70f` (its message, and the `retention.py` and `repository.py` hunks).

1. **`retention.RetentionPolicy._allow` admits the named service writer `svc-commentary` on `reserve`,** for its registered
   family `ANALYSIS_COMMENTARY` only, tenant-bound (never `global`, never `opal-capital`). Before, `reserve` refused every
   service subject. Ordered by this seat's ruling ca645f8410 (as the code comment cites it; not re-read here).
2. **`repository.SERVICE_READERS` gains `svc-irpt-packager` -> `ANALYSIS_COMMENTARY`:** one more service subject may read
   one family.

Both land in the adapter's and irpt-status's packages. Neither function's IAM, routes or environment change, so what
either subject can reach through these two functions is bounded by the routes each one declares. **That no declared route
of either function reaches a service-principal `put`/`reserve` or a packager read is INFERRED from the route tables (the
pair's own word), not measured.** These widenings were built for the commentary store Lambda, not for these two.

## A2. Added conditions (8 and 9; they join the seven of section 4)

8. **Reach read before each of the two applies:** the issuer prints, from the BUILT zip, the handlers reachable from that
   function's declared routes and the count of call sites among them that call `artifacts.put`, `retention.reserve` or an
   `ArtifactRepository.get` on `ANALYSIS_COMMENTARY`. Denominator printed (routes read, handlers walked). A count above 0
   is a STOP and comes back to this seat; 0 lets the apply proceed.
9. **The ledger close for the adapter and for irpt-status states both A1 widenings as APPLIED, UNEXERCISED on that
   function,** unless condition 8 found a reaching route and it was exercised on both arms.

irpt-narrative is unaffected by A1: neither file is among its changed members.

## A3. CTO half of IRPT_ANLREQ release 1 REVISION 6 (irpt-status only) -- SIGNED

**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release1/NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV6_IRPT_STATUS.md`
@7ce505dc5a, blob 1d38417741 (read in full by `git cat-file`). The only bytes that may land: `6idtFvAmYk73wJdr5DPRIyEPrLeWgzjlqbdNr5f1wxc=`.
A build at the pin that prints another digest is an ABORT, as the pair says.

The two rulings the pair asks for:

- **Section 4, commit 3fc99be70f carried although TO-AR-y-21 AMENDMENT 9 dropped it: ACCEPTED.** The one-tree rule
  outranks the member-level exclusion; a member held back is how revision 5 failed. The cost is A1's two widenings, which
  this amendment names and conditions.
- **Section 5 R3, the window runs until 2.0.0_SA_COO~G2's reads finish, with START lines printed per tenant as the
  denominators: ACCEPTED as written.** A window that closes earlier, or a one-tenant denominator, is not R3.

The pair's R0 to R5 and both branches stand as written. Conditions 1, 2, 3, 5, 6, 8 and 9 of this half apply to it. The
pair's "Recorded, no rollback" line for a typed refusal on R4 is accepted: it is recorded and routed, and FWD-1 of
IRPT_YCDGEN is not graded REALIZED on it.

-- 1.0.0_SA_CTO~DELL2
