# IRPT_ANLREQ release 1 REVISION 5 -- the rev 4 re-cut, shipped whole -- never-widen pair

**Deployer:** `2.0.0_SA_COO~Y2`. **Applier:** `0.7.0_AE_CloudOps~DELL2` (or the CTO's named substitute). **Live-call actor:** `2.0.0_SA_COO~G2` (CTO msg 3749).
Supersedes revision 4 (`NEVER_WIDEN_PAIR_ANLREQ_RELEASE1_REV4_IRPT_STATUS.md`), which went live at 15:43Z and crashed every call. It was rolled back to rev 3 at
16:43Z (rows `IRPT_ANLREQ-D2-S16`, `IRPT_BCKEND-D2-S60`).

**COO half: SIGNED by this file, 2026-10-09 ~17:2xZ.** CTO half: owed.

## 1. Why revision 4 failed, and what is different now

- `status_installed.py:137` passes `additional_policy_revisions=` to `composition.build_retained_repositories`. Rev 4 packaged `composition.py` at
  `80a79a7462`, which predates that keyword, so every call raised TypeError.
- **New gates at this pin:** `checks/r2/signature_closure.py` on the built zip (CTO msg 3731, now fleet-wide) and a live-call arm (section 4, R3).

## 2. Pin and artifact

- **Pin:** box/dell2 `54ed3aa8f6` (AR-y-21 AMENDMENTS 8-9). It must be on origin before the apply.
- **Built** (BUILD_ONLY at the pin, detached worktree, this seat): `DZOdwUOG/+EQe4mxW65GoDSoa4fckLXDXQDfExm3fTk=`.
- **Live now / ROLLBACK:** rev 3 `t6OJTCcmOnWGVl8iglcvfGoYb3PbPJqJYqsSgJBpGdI=`. Its current object version is `1dX90t6JdYfffHVpKsy7MHlQdfdFvp2V`, re-uploaded by
  Branch B leg B1. The applier records the version it replaces at step 0.

## 3. Gates at the pin

| gate | reading |
|---|---|
| per-member diff of the BUILT zip vs live rev 3 (both 49 members) | **3 changed**, 0 added, 0 removed: `status_installed.py` (59853db310e6 -> 326fed4f54b4), `composition.py` (6d2c3696d030 -> 5b896004af77), `repository.py` (f255335beb26 -> f01fcf549e8e) |
| symbol closure on the built zip | PASS |
| signature closure on the built zip | 121 calls checked, 1 mismatch: `served:1006 InteractiveAccess(profile_reader=)`. It is ALSO in live rev 3, is owned by `2.0.0_SA_COO~P2` (row S60), and is tolerated by name. The rev 4 mismatch `status_installed:137` is gone |
| `_authz` census + `test_status_installed_revisions.py` + `test_status_installed.py` | 19 passed |

## 4. Blast radius (what moves on irpt-status, and what does not)

Three commits ride the two re-pins. Each is already served by `irpt-export-render`, which stages both files at `2aa217ec58`.
- `f60e6f1d2a` (YCDGEN, YCD-l-6): retention resolves the policy from the reference. `build_retained_repositories` gains `additional_policy_revisions`.
- `b13bab7495` (IB-pr-336): one line, custody naming (the `CUSTODY_REPORT` kind).
- `2aa217ec58` (IB-pr-369): `ReportRepository` / `ArtifactRepository` take `revisions=`. Each family is retained under its own policy revision, and a
  write of a family under another revision refuses (`ReportRefused`).

**Widens:** irpt-status may READ the Opal research family under its registered revision (the purpose of rev 4). **Does not move:** any route (the
`/original` route stays exactly 1), IAM, any env var, any layer, `resident_installed.py` (stays `80a79a7462`), any other function. irpt-status is a
reader; that the `put` path changes are not reached by its routes is INFERRED from its route table, not measured. `IB-pr-386` and AR-t-12's svc-commentary admission (`3fc99be70f`) are
deliberately NOT carried (AMENDMENT 9).

## 5. After-reads

- R0: live at start == `t6OJTCcm`. The per-member diff of the UPLOADED zip against LIVE (read via `get_function`, never the S3 key) is EXACTLY the three
  members above, otherwise STOP. The shared-root STOP applies.
- R1: symbol closure missing=0 and signature closure exactly the tolerated mismatch, on the UPLOADED zip.
- R2: live == `DZOdwUOG`, re-plan 0, the `/original` route count is 1.
- **R3 (live-call arm, before the ledger closes):** zero `TypeError` events in irpt-status logs for 5 minutes with traffic shown (START lines), plus ONE
  authorized owner GET answering 200 in `2.0.0_SA_COO~G2`'s sr1 window (codes and section names only).
- R4: `2.0.0_SA_COO~G2`'s owner read of `REQ-5e4149d2` (status-job and analysis-report) answers, with no `RetentionRefused`.
- **Branch B:** any TypeError in R3, or R2 failing, re-promotes rev 3's object version. R4 failing alone does NOT roll back: it is recorded with its
  code and routed to the issuer.

## 6. Owed before the apply

- The CTO half.
- Pin `54ed3aa8f6` on origin.
