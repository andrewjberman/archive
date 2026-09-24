# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rtl-1`: publish the write-boundary-guarded, taxonomy-closed capture tool to the render host's artifact prefix

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtl-1.the-capture-tool-invariant-guard-at-the-write-boundary.md`.
**This packet is NOT a sign-off.** It states the act's blast radius and rollback for `2.0.0_SA_COO~B` and
`1.0.0_SA_CTO` to read and SIGN as separate half-files under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` (file names containing `IB-rtl-1` and `CTO_HALF` / `COO_HALF`),
each naming THIS packet's git blob hash at HEAD, before arm (f)'s publish runs. **The prior `IB-rtk-1`
packet and its signed halves do NOT cover this repair -- this is a NEW blob and needs NEW halves.**

## 1. THE ACT AND ITS EXACT BLAST RADIUS

Copy exactly ONE object, from the git-blob bytes at the commit that carries the repair, to the artifacts
prefix `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`, overwriting the one key
of the same name, with the operator identity only. Every hash below is git-OBJECT-derived
(`git cat-file -p <blob> | sha256sum`, cross-checked with `git show <commit>:<path> | sha256sum`), NEVER a
raw working-tree read -- row `IRPT_BCKEND-W13-S3` documents that a raw read on this box's CRLF checkout
produces a DIFFERENT, WRONG value, and this was re-verified live this session (raw read
`b6f266432e9c94002980316a6e97256d43b8ce11117281ade99e53b6bce232e0` vs git-object
`b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c` for the SAME working-tree file, same
instant):

| file | git blob (`git rev-parse HEAD:<path>`) | sha256 of the blob bytes | changed at |
|---|---|---|---|
| `infra/aws/ec2/investor-reporting-export/capture-session.cjs` | `82abe68499ab1d5422f6f73979c3f5b72ed4c583` | `b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c` | `cb6429dc9e` |

Both derivation commands agree (`git cat-file -p <blob> \| sha256sum` and
`git show cb6429dc9e:infra/aws/ec2/investor-reporting-export/capture-session.cjs \| sha256sum`, run this
session; both printed the same value above).

**`capture-session.sh` is UNCHANGED by this cell** (git blob `d704adfb7b6a3ee904c3ba7173eb81533679c97b` at
HEAD, sha256 `17ae44f0d6ee0a2f30225a99446f74c33fb82ce893026bb9852d211581ef89e0`, byte-identical to what
`IB-rti-1`'s packet already published and every later cell in this chain re-verified, most recently
`IB-rtk-1`). It is NOT republished by this packet, for the same reason `IB-rtj-1`'s and `IB-rtk-1`'s packets
gave: republishing byte-identical content under a new ledger entry would claim an act this cell did not
perform.

**`README.md`'s step-2 "Expected output" hash line for `capture-session.cjs` is UNCHANGED BY THIS COMMIT,
DELIBERATELY**, for the identical reason `IB-rtk-1`'s packet gave for its own round: that line currently
states the sha256 of the bytes ACTUALLY LIVE in S3 today (`f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d`,
`IB-rtk-1`'s published blob) -- that value is still TRUE right now, because arm (f)'s publish has not run.
Overwriting it with this repair's new sha256 BEFORE the publish runs would make the runbook assert a value
the S3 object does not yet hold, so an operator following step 2 today would see a real hash mismatch
against CURRENT S3 bytes and, per the runbook's own instruction, would incorrectly escalate. **The hash-line
edit belongs in the SAME commit as the publish, when both become true together.** This packet documents the
value that line will need to become once the publish runs: `b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`.

**A DIFFERENT part of `README.md` -- a new prose subsection describing the write-boundary invariant and the
closed retry taxonomy -- IS already committed this session (`6c7713e1df`), ahead of the publish.** This is
a deliberate, narrower reading of the order's arm (f) than `IB-rtk-1`'s precedent needed to make: arm (d)
("THE RETRY TAXONOMY, CLOSED -- code and documentation must agree literally... so a reader cannot derive a
wider or narrower set than the code implements") requires this prose to exist as part of the CORE repair,
independent of publish state, and `R112-AC2`'s own `<expect>` names "CODE-README-AGREE" as something this
battery must print PASS-by-output for NOW. The prose describes REPO code BEHAVIOR (true today, regardless
of what bytes are in S3), not published BYTES -- unlike the hash line above, which literally asserts a
sha256 of an S3 object and is the only thing arm (f)'s "do not update the README before the bytes it
describes actually exist in S3" clause can be describing, since prose about behavior does not describe
bytes. Both halves' signers should read this split and disposition it; it is stated here, not hidden.

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

The property a reader may assume is "the host now runs the C-S170/C-S171-repaired, taxonomy-closed tool".
That is NOT what the act alone does: the producer of the host's copy is either (a) the render document's
own sync (runs at the human-started wave-2 step and re-reads the bytes then), or (b) the runbook's own step
2 (runs EVERY time, explicitly, before the wrapper -- this cell does not change that discipline). Both
branches are covered: if (a) or (b) runs AFTER this publish AND the README hash-line update land, the host
receives exactly this blob; if neither ever runs, the host keeps whatever it holds (the pre-`IB-rtl-1` tool,
still exposed to C-S170/C-S171 and the open retry taxonomy, inert while the host is stopped). **No host-side
byte verification is claimed by this cell** -- the README's step 2 hash check is an OPERATOR act this
packet documents, not something this worker's tooling exercises.

## 4. ROLLBACK

Republish the PRIOR bytes: `git show cb6429dc9e~1:infra/aws/ec2/investor-reporting-export/capture-session.cjs`
(the pre-`IB-rtl-1`, still-C-S170/C-S171-defective, open-taxonomy blob
`ded605028b2210b589735927868aacf92ceb852d`) to the same key, and revert the README's expected-hash line to
`f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d` in the same act (the retry-taxonomy
PROSE subsection is not part of this rollback -- it describes repo code behavior at whatever commit is
checked out, and a rollback of the PUBLISHED bytes does not by itself revert the repo's own HEAD). The
prefix is not versioned-bucket-guaranteed by this cell (not measured here); the git blob is the source of
truth for rollback, exactly as `IB-rti-1`'s, `IB-rtj-1`'s and `IB-rtk-1`'s packets stated for their own acts.

## 5. THE GATE, AND WHAT THE PUBLISH ARM WOULD PROVE

Arm (f) of `IRPT_BCKEND.TO-IB-rtl-1` publishes ONLY when BOTH halves are at HEAD naming THIS packet's blob
(`82abe68499ab1d5422f6f73979c3f5b72ed4c583`, sha256 `b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`);
it would then, in one act: update the README's expected-hash line for `capture-session.cjs` to that sha256,
open a NEW deploy-ledger entry (`org/critical_paths/.open_deploys/irpt-rtl-1-capture-tool-publish.json`) and
commit its sentinel BEFORE the act, publish, read the object back from S3, compare its sha256 to the table
above, and close the entry. Verdict token (not yet reached this pass): `IBR112-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOB`.

**AS OF THIS COMMIT, NEITHER HALF EXISTS FOR THIS PACKET** (censused this session via `Glob` over
`org/tier1_exec/{1.0.0_SA_CTO,2.0.0_SA_COO~B}/deliverables/` for any filename containing `IB-rtl-1`: 0 of 0
found; separately, `git log CLOUD -3` shows the shared branch's tip is currently on an unrelated project,
`IRPT_FNTEND` round 12, confirming no cross-seat reference to this blob exists anywhere reachable from this
worktree). Per the order's own arm (f): **"STOP here unless BOTH halves (`2.0.0_SA_COO~B` and
`1.0.0_SA_CTO`) are at HEAD naming this NEW packet's blob."** This worker therefore does NOT open the ledger
entry, does NOT publish to S3, does NOT update the README's hash line, and does NOT claim host-side or
S3-side verification -- exactly as the order's DELIVERABLE section anticipates ("the ledger entry and S3
readback IF both halves land"). **The host is STOPPED and this cell does not start it -- no on-host readback
exists here.** The publish remains available to a later pass once both halves land, the same shape
`IB-rti-1`'s, `IB-rtj-1`'s and `IB-rtk-1`'s own first passes took.

## 6. WHAT THE REPAIR CHANGED (for the signers)

- **(b) C-S170**, the write-boundary invariant: `refuseIfLatched()` previously ran BEFORE
  `await context.storageState()` (old :364, before :366's capture) -- a foreign navigation during that
  specific await still resulted in a write. Now `context.storageState()` (capture-session.cjs, main(), the
  `const rawState = await context.storageState();` line) is captured to MEMORY first, the latch is checked
  immediately after, the file is written ATOMICALLY (temp file, then `fs.renameSync`), and the latch is
  checked AGAIN immediately after the rename -- if set, the just-written file is deleted
  (`fs.unlinkSync`) and the run exits non-zero. Proven by R11's own case 1 ("storage wait foreign hop then
  portal": now writes=0, was writes=1) and this worker's own `harness_ib_rtl_1.cjs` (the post-rename timing
  variant: refuses, unlinks==1).
- **(c) C-S171**, the observer's response-path filter: `createLifetimeObserver`'s `onResponse` had no
  `isNavigationRequest()` filter (unlike `onRequest`, which already had one) -- a foreign-origin SUBRESOURCE
  wrongly latched a terminal refusal. Now both paths carry the same filter. Proven by R11's case 3
  ("non-navigation foreign response": now writes=1/success=true, was writes=0/success=false/refused),
  unaffected control at case 4 (an actual foreign MAIN-FRAME navigation: still refuses).
- **(d) The retry taxonomy, closed**: `readinessRefusal` (bare string, every reason equally retryable)
  replaced by `readinessOutcome` (`{ready, retryable, cause}`), preserving every existing check and its
  order (status, password, per-hop origin/sign-in-path, final-URL origin/sign-in-path, marker) unweakened.
  Exactly three causes now retry (timeout, HTTP 5xx, marker-absent-after-load); an HTTP 4xx and a generic
  non-timeout navigation error now terminally refuse on FIRST occurrence (R11 cases 8/9:
  verificationCalls==1, storageCalls==0 -- proven never retried). README's new prose subsection states the
  same three causes verbatim (`battery_ib_rtl_1.py --arm retry`, PASS).
- S125 instance-id validation, S126 marker check, S127's origin allowlist/vendor-host refusal/scoped
  storageState, C-S153's initial-navigation hop walk, and C-S158/C-S159's sticky observer latch are all
  unweakened -- re-verified this session: the R8 diagnostic, run unmodified, is BYTE-IDENTICAL to this
  round's own pre-repair baseline; R9's externally-visible verdict (success, writes) is unchanged for all 6
  cases (one case's INTERNAL path to an unchanged refusal verdict changed, documented in
  `battery_ib_rtl_1.py`'s own module docstring as an intended strengthening consistent with BOUNDS, not a
  regression).
