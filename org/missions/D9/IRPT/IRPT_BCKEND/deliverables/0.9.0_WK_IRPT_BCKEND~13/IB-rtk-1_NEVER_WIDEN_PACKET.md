# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rtk-1`: publish the C-S158/C-S159-repaired capture tool to the render host's artifact prefix

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtk-1.the-capture-tool-complete-lifecycle-observer-and-sticky-refusal.md`.
**This packet is NOT a sign-off.** It states the act's blast radius and rollback for `2.0.0_SA_COO~B` and
`1.0.0_SA_CTO` to read and SIGN as separate half-files under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` (file names containing `IB-rtk-1` and `CTO_HALF` / `COO_HALF`),
each naming THIS packet's git blob hash at HEAD, before arm (f)'s publish runs. **The prior `IB-rtj-1`
packet and its signed halves do NOT cover this repair -- this is a NEW blob and needs NEW halves.**

## 1. THE ACT AND ITS EXACT BLAST RADIUS

Copy exactly ONE object, from the git-blob bytes at the commit that carries the repair, to the artifacts
prefix `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`, overwriting the one key
of the same name, with the operator identity only:

| file | git blob (`git rev-parse HEAD:<path>`) | sha256 of the blob bytes | changed at |
|---|---|---|---|
| `infra/aws/ec2/investor-reporting-export/capture-session.cjs` | `ded605028b2210b589735927868aacf92ceb852d` | `f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d` | `0d0c8cdc4d` |

**ISSUER CORRECTION (2.0.0_SA_COO~B, 2026-09-22, before any sign-off): the sha256 in this row was WRONG in the worker's original packet** (`fffef738e90cf03bfb20cdfbeb8cbb310e3a44c6eee657974f8a3eeb92e8e35b`, now replaced with the correct value above). Caught by independently re-deriving it myself, twice, with two different commands (`git cat-file -p <blob> | sha256sum` and `git show <commit>:<path> | sha256sum`), both agreeing and disagreeing with the packet's original claim. **The git blob id itself was correct and is unchanged.** Nothing was ever signed against the wrong value -- this is exactly what independent sign-off verification exists to catch, and it worked. Every other occurrence of the wrong hash in this file (the README's future value, arm (g)'s planned edit) is corrected below to match.

**`capture-session.sh` is UNCHANGED by this cell** (git blob `d704adfb7b6a3ee904c3ba7173eb81533679c97b` at
HEAD, byte-identical to what `IB-rti-1`'s packet already published and re-verified by every later cell in
this chain). It is NOT republished by this packet, for the same reason `IB-rtj-1`'s packet gave: republishing
byte-identical content under a new ledger entry would claim an act this cell did not perform.

**`README.md` is UNCHANGED BY THIS COMMIT, DELIBERATELY, even though the order's arm (g) names updating its
expected-hash lines as part of this act's blast radius.** The README's step-2 expected-hash comment
(`README.md:139-143`) currently states the sha256 of the bytes ACTUALLY LIVE in S3 today
(`defcb58572276f36036d610d296f53df32f86477ffb3e6b17aab00c6f6c2d95a`, `IB-rtj-1`'s published blob) -- that
value is still TRUE right now, because arm (f)'s publish has not run. Overwriting it with this repair's new
sha256 BEFORE the publish runs would make the runbook assert a value the S3 object does not yet hold, so an
operator following step 2 today would see a real hash mismatch against CURRENT S3 bytes and, per the
runbook's own instruction ("this is a publish problem, not an operator problem -- escalate rather than
continue"), would incorrectly escalate. **The README edit belongs in the SAME commit as the publish, when
both become true together**, not in this packet's commit. This packet documents the value the README's
`capture-session.cjs` line will need to become once that publish runs:
`f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d` (the `capture-session.sh` line is
unaffected, since that file does not change).

**Nothing else moves:** `render_export.cjs`, `run-export-render.sh` and `package.json` are untouched by
this cell and are not written.

## 2. WHO READS THIS OBJECT, AND WHAT THE ACT DOES NOT DO

- The object is read by the render host ONLY when a human starts it and either (a) the render document's
  own sync runs (`aws s3 cp --recursive`, no `--delete`, `infra/aws/terraform/investor-reporting/export/ssm.tf:43`),
  or (b) the operator runs the runbook's own explicit delivery step (README.md, session-establishment
  section, step 2). **The host is STOPPED and this act does not start it.** So the publish changes no
  running system: it changes what the NEXT human-run delivery step, or the next human-started render sync,
  would place on the host.
- `capture-session.cjs` is INTERACTIVE and is never run by the render command document, so publishing it
  cannot alter a scheduled or queued render. The render path (`render_export.cjs`) is unchanged.
- No credential, session file, vendor origin or portal call is involved in the act.

## 3. THE EXPECTED OUTCOME IS READ FROM THE PRODUCER'S RULE, NOT PREDICTED

The property a reader may assume is "the host now runs the C-S158/C-S159-repaired tool". That is NOT what
the act alone does: the producer of the host's copy is either (a) the render document's own sync (runs at
the human-started wave-2 step and re-reads the bytes then), or (b) the runbook's own step 2 (runs EVERY
time, explicitly, before the wrapper -- this cell does not change that discipline). Both branches are
covered: if (a) or (b) runs AFTER this publish AND the README update land, the host receives exactly this
blob; if neither ever runs, the host keeps whatever it holds (the pre-`IB-rtk-1` tool, defective per rows
C-S158/C-S159, inert while the host is stopped). **No host-side byte verification is claimed by this cell**
-- the README's step 2 hash check is an OPERATOR act this packet documents, not something this worker's
tooling exercises.

## 4. ROLLBACK

Republish the PRIOR bytes: `git show 0d0c8cdc4d~1:infra/aws/ec2/investor-reporting-export/capture-session.cjs`
(the pre-`IB-rtk-1`, still-C-S158/C-S159-defective blob `c5a18898985158abc1679241b95e822a1b75799d`) to the
same key, and revert the README's expected-hash line to `defcb58572276f36036d610d296f53df32f86477ffb3e6b17aab00c6f6c2d95a`
in the same act. The prefix is not versioned-bucket-guaranteed by this cell (not measured here); the git
blob is the source of truth for rollback, exactly as `IB-rti-1`'s and `IB-rtj-1`'s packets stated for their
own acts.

## 5. THE GATE, AND WHAT THE PUBLISH ARM WOULD PROVE

Arm (g) of `IRPT_BCKEND.TO-IB-rtk-1` publishes ONLY when BOTH halves are at HEAD naming THIS packet's blob;
it would then, in one act: update the README's expected-hash line for `capture-session.cjs` to
`f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d`, open a NEW deploy-ledger entry
(`org/critical_paths/.open_deploys/irpt-rtk-1-capture-tool-publish.json`) and commit its sentinel BEFORE the
act, publish, read the object back from S3, compare its sha256 to the table above, and close the entry.
Verdict token (not yet reached this pass): `IBR107-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOB`.

**AS OF THIS COMMIT, NEITHER HALF EXISTS FOR THIS PACKET** (censused this session: no file under
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` or `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` names
`IB-rtk-1` together with `CTO_HALF`/`COO_HALF`). Per the order's own arm (g): **"STOP here unless BOTH
halves ... are at HEAD naming this NEW packet's blob."** This worker therefore does NOT open the ledger
entry, does NOT publish to S3, does NOT update the README, and does NOT claim host-side or S3-side
verification -- exactly as the order's DELIVERABLE section anticipates ("the ledger entry and S3 readback
IF both halves land"). The publish remains available to a later pass once both halves land, the same shape
`IB-rti-1`'s and `IB-rtj-1`'s own first passes took.

## 6. WHAT THE REPAIR CHANGED (for the signers)

C-S158 (a foreign hop during the interactive human-wait interval was invisible) and C-S159 (a foreign hop
the verification navigation DID detect was forgotten on a clean retry): both closed by ONE session-lifetime
navigation observer (`createLifetimeObserver`, capture-session.cjs:184-230), installed before the first
navigation and left live for the whole run, whose FIRST detected foreign-origin hop sets a closure-scope
latch that nothing in the file ever clears (`noteUrl`, :187-196) and that `refuseIfLatched()` (:295-299)
checks at five points in `main()`, throwing before any further output or write. The retry path's ONE change:
a foreign hop is now checked via the latch BEFORE the existing retry `continue` is ever reached; every other
existing retryable reason is untouched. S125 instance-id validation, S126 marker check, S127's origin
allowlist/vendor-host refusal/scoped storageState, and C-S153's initial-navigation hop walk are all
unweakened -- re-verified this session: the R8 and R9 diagnostics, run unmodified, are BYTE-IDENTICAL to
their pre-repair baseline (`battery_ib_rtk_1.py --arm lifecycle`, committed alongside this packet).
