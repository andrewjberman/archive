# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rtm-1`: publish the typed-classification, truthful-cleanup-reporting capture tool to the render host's artifact prefix

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtm-1.the-capture-tool-typed-error-classification-and-truthful-cleanup-report.md`.
**This packet is NOT a sign-off.** It states the act's blast radius and rollback for `2.0.0_SA_COO~B` and
`1.0.0_SA_CTO` to read and SIGN as separate half-files under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` (file names containing `IB-rtm-1` and `CTO_HALF` / `COO_HALF`),
each naming THIS packet's git blob hash at HEAD, before arm (g)'s publish runs. **The prior `IB-rtl-1`
packet and its signed halves do NOT cover this repair -- this is a NEW blob and needs NEW halves.**

## 1. THE ACT AND ITS EXACT BLAST RADIUS

Copy exactly ONE object, from the git-blob bytes at the commit that carries the repair, to the artifacts
prefix `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`, overwriting the one key
of the same name, with the operator identity only. Every hash below is git-OBJECT-derived
(`git cat-file -p <blob> | sha256sum`, cross-checked with `git show <commit>:<path> | sha256sum`), NEVER a
raw working-tree read -- row `IRPT_BCKEND-W13-S3` documents that a raw read on this box's CRLF checkout
produces a DIFFERENT, WRONG value; both derivation commands were re-run THIS session and agreed:

| file | git blob (`git rev-parse HEAD:<path>`) | sha256 of the blob bytes | changed at |
|---|---|---|---|
| `infra/aws/ec2/investor-reporting-export/capture-session.cjs` | `058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae` | `3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2` | `b809df14d5` |

Both derivation commands agree (`git cat-file -p 058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae \| sha256sum` and
`git show HEAD:infra/aws/ec2/investor-reporting-export/capture-session.cjs \| sha256sum`, run this session;
both printed `3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2`).

**`capture-session.sh` is UNCHANGED by this cell** (git blob `d704adfb7b6a3ee904c3ba7173eb81533679c97b` at
HEAD, sha256 `17ae44f0d6ee0a2f30225a99446f74c33fb82ce893026bb9852d211581ef89e0`, byte-identical to what
`IB-rti-1`'s packet already published and every later cell in this chain re-verified, most recently
`IB-rtl-1`). It is NOT republished by this packet, for the same reason every prior cell's packet gave:
republishing byte-identical content under a new ledger entry would claim an act this cell did not perform.

**`README.md`'s step-2 "Expected output" hash line for `capture-session.cjs` is UNCHANGED BY THIS COMMIT,
DELIBERATELY**, for the identical reason `IB-rtk-1`'s and `IB-rtl-1`'s packets gave: that line currently
states the sha256 of the bytes ACTUALLY LIVE in S3 today (`f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d`,
`IB-rtl-1`'s published blob) -- that value is still TRUE right now, because arm (g)'s publish has not run.
Overwriting it with this repair's new sha256 BEFORE the publish runs would make the runbook assert a value
the S3 object does not yet hold. **The hash-line edit belongs in the SAME commit as the publish, when both
become true together.** This packet documents the value that line will need to become once the publish
runs: `3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2`.

**A DIFFERENT part of `README.md` -- the new "cleanup failure" paragraph naming exit code 4 (arm (b)'s OWN
explicit instruction, "update the README to name that exact code and the required manual step", untied to
publish state) and a new sentence describing typed timeout classification -- IS already committed this
session (`1473f3ec4a`), ahead of the publish, for the same reading `IB-rtl-1`'s row `W13-S4` established:
this prose describes REPO CODE BEHAVIOR (true today, regardless of what bytes are in S3), never a claim
about published bytes -- unlike the hash line above, which literally asserts a sha256 of an S3 object.

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

The property a reader may assume is "the host now runs the C-S179/C-S180-repaired tool". That is NOT what
the act alone does: the producer of the host's copy is either (a) the render document's own sync (runs at
the human-started wave-2 step and re-reads the bytes then), or (b) the runbook's own step 2 (runs EVERY
time, explicitly, before the wrapper -- this cell does not change that discipline). Both branches are
covered: if (a) or (b) runs AFTER this publish AND the README hash-line update land, the host receives
exactly this blob; if neither ever runs, the host keeps whatever it holds (the pre-`IB-rtm-1` tool, still
exposed to C-S179/C-S180, inert while the host is stopped). **No host-side byte verification is claimed by
this cell** -- the README's step 2 hash check is an OPERATOR act this packet documents, not something this
worker's tooling exercises.

## 4. ROLLBACK

Republish the PRIOR bytes: `git show cb6429dc9e:infra/aws/ec2/investor-reporting-export/capture-session.cjs`
(the pre-`IB-rtm-1`, still-C-S179/C-S180-defective blob `82abe68499ab1d5422f6f73979c3f5b72ed4c583`, sha256
`b6f75a20150c170687ef2c1974b0a219a4ba56fc11a457b03b1fa688c68f353c`) to the same key, and revert the README's
expected-hash line to that value in the same act (the cleanup-exit-code and typed-classification prose
subsections are not part of this rollback -- they describe repo code behavior at whatever commit is checked
out, and a rollback of the PUBLISHED bytes does not by itself revert the repo's own HEAD). The prefix is not
versioned-bucket-guaranteed by this cell (not measured here); the git blob is the source of truth for
rollback, exactly as every prior cell's packet in this chain stated for its own act.

## 5. THE GATE, AND WHAT THE PUBLISH ARM WOULD PROVE

Arm (g) of `IRPT_BCKEND.TO-IB-rtm-1` publishes ONLY when BOTH halves are at HEAD naming THIS packet's blob
(`058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae`, sha256 `3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2`);
it would then, in one act: update the README's expected-hash line for `capture-session.cjs` to that sha256,
open a NEW deploy-ledger entry (`org/critical_paths/.open_deploys/irpt-rtm-1-capture-tool-publish.json`) and
commit its sentinel BEFORE the act, publish, read the object back from S3, compare its sha256 to the table
above, and close the entry. Verdict token (not yet reached this pass): `IBR113-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOB`.

**AS OF THIS COMMIT, NEITHER HALF EXISTS FOR THIS PACKET** (censused this session via `Glob` over
`org/tier1_exec/{1.0.0_SA_CTO,2.0.0_SA_COO~B}/deliverables/` for any filename containing `IB-rtm-1`: 0 of 0
found). Per the order's own arm (g): **"STOP here unless BOTH halves (`2.0.0_SA_COO~B` and `1.0.0_SA_CTO`)
are at HEAD naming this NEW packet's blob."** This worker therefore does NOT open the ledger entry, does NOT
publish to S3, does NOT update the README's hash line, and does NOT claim host-side or S3-side verification
-- exactly as the order's DELIVERABLE section anticipates ("the ledger entry and S3 readback IF both halves
land"). **The host is STOPPED and this cell does not start it -- no on-host readback exists here.** The
publish remains available to a later pass once both halves land, the same shape every prior cell's own first
pass took in this chain. **`<status>` stays `pending`, with this blocking state stated, per the order's own
`<proof_of_spec>` instruction ("do not flip to `complete` while arm (g) is still gated on unmet halves").**

## 6. WHAT THE REPAIR CHANGED (for the signers)

- **(a) C-S179, typed classification**: the verification `page.goto()` catch block previously matched
  `/timeout/i` against the error's MESSAGE TEXT anywhere -- a non-timeout error whose message merely
  contained "timeout" (e.g. a certificate failure on a URL carrying `?timeout=1`) was wrongly retried. Now
  classified ONLY by `error.name === 'TimeoutError'` (Playwright's own error class) OR an EXACT match
  against the one deterministic message this tool's own configured `GOTO_TIMEOUT_MS` deadline produces
  (`isOwnDeadlineMessage`) -- never a keyword search over free text. Proven by R12's own counterexample case
  (now terminal, was wrongly retried) and this worker's own `harness_ib_rtm_1.cjs` pair (i). The second path
  (exact-match against the tool's own configured deadline) was added after measuring that a `.name`-only
  reading regresses two long-standing reference diagnostics' own genuine-timeout positive controls (every
  upstream mock throws a plain `Error()` for a simulated timeout, never setting `.name`) -- filed as row
  `IRPT_BCKEND-W13-S6`, left to `3.0.0_SA_CVO~B`'s adjudication.
- **(b) C-S180, truthful cleanup reporting**: the post-rename latch recheck previously swallowed an
  `unlinkSync` throw (`catch (e) { /* best-effort */ }`) and always printed the same "was deleted" message
  regardless of whether deletion actually succeeded. Now the deletion outcome is tracked: a genuine
  `unlinkSync` failure prints `ERROR: session file could NOT be removed: <path> (<errno>) -- delete it
  manually before any use`, exits the new distinct `CLEANUP_FAILURE_EXIT_CODE` (4), and the file REMAINS on
  disk. Proven by R12's own EPERM counterexample case (now truthful, was untruthful) and this worker's own
  `harness_ib_rtm_1.cjs` pair (ii).
- Every existing S125/S126/S127/C-S153/C-S158/C-S159/C-S170/C-S171 check is unweakened -- re-verified this
  session: R10, R9 and R8 diagnostics, run unmodified against the repaired blob, are results-array
  BYTE-IDENTICAL to this round's own pre-repair baseline; R11's diagnostic shows ZERO change in any
  externally-visible verdict field (success/writes/exitCode/verificationCalls/prompts/storageCalls) across
  all 11 cases -- the one byte-level difference is a cosmetic addition to an already-terminal case's error
  message text, not a behavioral change.
