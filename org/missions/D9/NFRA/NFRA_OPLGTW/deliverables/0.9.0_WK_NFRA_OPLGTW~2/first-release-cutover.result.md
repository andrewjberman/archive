# NFRA_OPLGTW.TO-OG-r-1 -- first release cutover -- RESULT (final, post R-53 amendment)

**Assignee:** 0.9.0_WK_NFRA_OPLGTW~2 | **Worktree:** C:/tmp/wk-oplgtw-2a, branch wk-nfra_oplgtw-2a
**Proof instance:** `NFRA_OPLGTW.TO-OG-r-1.first-release-cutover.proof_of_spec.json` -- schema-valid;
`py -3.12 .tools/proof-of-spec-check.py <instance> OGR1-AC1..AC18` -> **VALID (rc=0)**.

## Outcome, in one line

**The release deployed for real.** Round 1: the deploy (OGR1-AC2) failed closed on a halt-gate identity
defect this worker found and filed (`NFRA_OPLGTW-W2-S5`); the coordinator GRANTED the row and, on ruling
R-53, corrected this worker's own proposed one-line fix (which was wrong two files away) into the actual
edit: `HALT_GATE_REPO_ROOT` now resolves to the CALLING worktree while `HALT_GATE_CONTEXT_FILE` /
`HALT_GATE_AUDIT_LOG` stay explicitly pinned to the main tree. This worker implemented that corrected edit
(the order's `<paths>` grant was widened for the identity-resolution lines only), verified it four ways
(AC15-AC18), and the deploy then ran clean: `opal-gateway` active, `/health` `{"ok":true}`, `/mcp` unauth 401,
on-box md5s captured. The deploy-completion ledger opened before the deploy (AC1) and closed with all three
legs truthfully proven after it (AC8).

**15 of 18 criteria PASS by output: OGR1-AC1, AC2, AC3, AC5, AC6, AC7, AC8, AC11, AC12, AC13, AC14, AC15,
AC16, AC17, AC18.**
**3 of 18 FAIL, each a real, disclosed, surprise-filed finding, not a probe defect:**
- **AC4** -- 9 of 68 deployed files carry CRLF line endings differing byte-for-byte from their LF git blobs.
  This deploying worktree has `core.autocrlf=true` and only `*.py` carries an `eol=lf` `.gitattributes`
  override; `deploy-to-ec2.sh` tars the live checkout rather than a normalized archive. NEW to this deploy
  (OG-p-1's prior baseline shows these same paths matched cleanly before). No functional break found on
  inspection. Surprise row `NFRA_OPLGTW-W2-S8`.
- **AC9** -- OG-p-1's `BASELINE.json` records no error-count metric under any key; there is no baseline value
  to compare a post-deploy error count against, independent of the deploy's success.
- **AC10** -- the recorded previous-release artifact (the commit live before this release) has no
  `app/data_entitlement.py` at all, so it fails the runbook's own s.7.2 rollback restorability precondition.
  The R-40 content-hash mechanism itself is correct and verified (recorded == read-back). Surprise row
  `NFRA_OPLGTW-W2-S7`.

`<status>` stays `pending`: per this order's own proof_of_spec block, `complete` flips "only when every
MECHANICAL criterion PASSES by output," and three do not.

## The halt-gate fix (R-53), what changed and how it was verified

`infra/aws/ec2/safe-ec2-deploy.sh`'s identity-resolution block (granted to this order's `<paths>` for these
lines only):
1. `HALT_GATE_REPO_ROOT` = `git rev-parse --show-toplevel` from the CALLING worktree (was: collapsed onto the
   shared main tree unconditionally).
2. `HALT_GATE_CONTEXT_FILE` and `HALT_GATE_AUDIT_LOG` pinned EXPLICITLY to the main tree (they have no
   fallback inside `halt-gate-check.sh` and would otherwise have moved into a worktree deleted at drain).
3. The stale justifying comment rewritten to state why the old collapse was wrong and dated.

Verified, all live/pinned-commit reads, no assumption:
- **AC15** -- from this worktree, the fixed script resolves `HALT_GATE_REPO_ROOT` to this worktree and the
  gate resolves this worker's own serial, `0.9.0_WK_NFRA_OPLGTW~2`.
- **AC16** -- the SAME fixed script, invoked as-if from the main tree, resolves `HALT_GATE_REPO_ROOT` to the
  main tree, byte-identical to the PRE-edit text pinned at `cbfa646e3292e81b8fb1e199ad352274c29016dd` (the
  parent of this worker's own R-53 commit) -- a fix that only helps workers would have failed this.
- **AC17** -- the pre-R-53 text restored in a scratch copy (never touching the tracked file) FAILS AC15's own
  check (this worker's serial does not resolve) while AC16's own check still PASSES against it -- the
  mutant discriminates exactly the defect this fix closes.
- **AC18** -- from this worktree, both `HALT_GATE_CONTEXT_FILE` and `HALT_GATE_AUDIT_LOG` still resolve under
  the main tree, not this worktree -- the override audit trail was never relocated.

Two probe bugs found and fixed while grading the real deploy (both committed, both re-verified): AC5/AC6's
HTTP header lookup was case-SENSITIVE against a server that sends lowercase `www-authenticate` (fixed by
keeping the raw `http.client.HTTPMessage` instead of `dict()`-ing it); AC6 asserted an equality RFC 8414's
authorization-server metadata never carries (`resource`) and was corrected; AC16/AC17 originally compared
against `git show HEAD:...`, which silently started reading the POST-edit text the moment this worker's own
fix commit landed -- re-pinned to the immutable pre-fix commit hash.

## What actually happened, in order (superseding the pre-amendment result)

1. **OGR1-AC1** -- opened the ledger, committed the sentinel + entry (`7752ea3bdb`) before any deploy attempt;
   recorded the previous-release snapshot for AC10 at the same moment.
2. **OGR1-AC11** -- local, pre-deploy, moto-emulated authority difference test: PASS (5/5 denied ungranted, 1/1
   allowed granted).
3. **First AC2 attempt** -- failed closed at the halt gate (IDENTITY UNRESOLVED); root-caused and filed as
   `NFRA_OPLGTW-W2-S5`.
4. **R-53 amendment received** -- merged `CLOUD` (`git merge CLOUD`, no fast-forward possible), re-read the
   amended order, implemented the corrected fix to `safe-ec2-deploy.sh`'s identity-resolution lines, added and
   verified OGR1-AC15-AC18, committed (`1764e54a16`).
5. **Second AC2 attempt** -- Step 1 passed; the halt gate now resolved this worker's serial and surfaced 18
   ROUTINE (non-STOP) pending messages on the issuer's inbox, none addressed to this deploy or to
   NFRA_OPLGTW/opal-gateway; reviewed (printed in full in this criterion's own output) and acknowledged via
   the gate's own documented `HALT_ACK=1` route (never `HALT_OVERRIDE`, which was never needed -- the gate
   itself never returned its STOP-class rc=2). The deploy then ran to completion: artifact built, uploaded,
   installed via SSM, systemd restarted, `/health` and `/mcp` verified on-box, `EC2_MANIFEST.json` updated and
   committed by the wrapper itself. PASS.
6. **OGR1-AC3, AC5, AC6, AC7, AC12, AC13** -- all live, all PASS (see the outcome summary above for the two
   probe bugs found and fixed for AC5/AC6, and the exact live role-assume evidence for AC13).
7. **OGR1-AC4** -- FAIL, a genuine CRLF byte-parity gap (see above), surprise row `NFRA_OPLGTW-W2-S8`.
8. **OGR1-AC8** -- all three ledger legs closed with real proof (the AC4 digest run, the AC3/AC5/AC6/AC7/AC9/
   AC12/AC13 verify run, the EC2_MANIFEST.json commit) and the entry committed CLOSED before this grading
   read. PASS.
9. **OGR1-AC9, AC10** -- FAIL, unchanged from the pre-amendment round (independent of the deploy's success);
   see surprise rows `NFRA_OPLGTW-W2-S7` (AC10) and this row's own text (AC9, no separate row filed since it
   blocks no other criterion).
10. **OGR1-AC14** -- re-verified PASS (mutant control for AC13, unaffected by the amendment).

## Surprise rows filed this order (all committed, `org/missions/D9/NFRA/NFRA_OPLGTW/surprise-channel/investigations/INVESTIGATION_v1.md`)

- **NFRA_OPLGTW-W2-S5** -- BLOCKING (now resolved by the R-53 fix this worker implemented), disarm owner
  `2.0.0_SA_COO~O`.
- **NFRA_OPLGTW-W2-S6** -- OBSERVATION, INERT. Leftover test fixtures in the live access-state table.
- **NFRA_OPLGTW-W2-S7** -- OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~O`. Previous-release rollback
  restorability gap.
- **NFRA_OPLGTW-W2-S8** -- OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~O`. The CRLF deploy-parity gap.

## Not attempted / declared exclusions

- Setting `SCHWAB_ACCOUNT_REF_SECRET_ID` in the release configuration (WORKER FACE narrative, not a graded
  criterion): still outside this order's `<paths>` grant (widened only for `safe-ec2-deploy.sh`'s
  identity-resolution lines, not `deploy-to-ec2.sh`'s env block). No AC1-AC18 criterion tests it.

## Validation

- `jsonschema.validate` against `org/standards/PROOF_OF_SPEC.schema.json`: SCHEMA VALID.
- `bash .tools/commit-gate.sh` on every touched `.py`/`.sh`: clean.
- `bash -n infra/aws/ec2/safe-ec2-deploy.sh`: SYNTAX_OK, before and after the R-53 edit.
- `py -3.12 .tools/proof-of-spec-check.py <instance> OGR1-AC1..AC18`: **VALID (rc=0)**.
