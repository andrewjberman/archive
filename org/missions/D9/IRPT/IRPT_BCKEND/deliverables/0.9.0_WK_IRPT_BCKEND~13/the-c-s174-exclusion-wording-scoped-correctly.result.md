# IRPT_BCKEND.TO-IB-rtp-1 -- C-S174 exclusion wording, scoped correctly

`0.9.0_WK_IRPT_BCKEND~13`, round 16, cell `IB-rtp-1`.

## Source of this cell

`3.0.0_SA_CVO~B`'s round-15 review found one residual wording fault in the `IB-rtk-1` proof
instance that its own hash-repair verification (round 15, `IB-rto-1`) did not touch: line `:23`
(the `capture-session.cjs` artifact row's `deploy_evidence`) correctly records the S3 publish
pass's PUBLISHED state, but the `declared_exclusions` entry at lines `:269-270` still carried an
unqualified exclusion claiming "any real host/SSM/S3 action" was excluded under stubs/static
reads -- true of the historical diagnostic pass, FALSE of the publish pass, which DID act on real
S3 bytes with a verified readback. `1.0.0_SA_CTO`'s round-15 analysis (`@81338c807a`, section
"Round 16") confirms this and authorizes exactly this narrow wording fix. No hashes touched
(already correct as of `IB-rto-1`), no code, no publish, no sign-off.

## Arm (a) -- scoped the exclusion to what it is actually true of

File: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~13/IRPT_BCKEND.TO-IB-rtk-1.the-capture-tool-complete-lifecycle-observer-and-sticky-refusal.proof_of_spec.json`.

Confirmed the text had not drifted: the unqualified exclusion sits at exactly lines `:269-270` in
this instance at this worktree's `HEAD` (`declared_exclusions[1]`), matching the order's own
citation. Line `:23` (`artifacts_produced[0].deploy_evidence`, the `capture-session.cjs` row) is
the existing, already-correct citation of the S3 publish and its verified readback and was left
untouched -- only reused as the source for the corrected exclusion text.

**Before:**
```
{
  "item": "a real Playwright/Chromium run of capture-session.cjs, or any real host/SSM/S3 action",
  "reason": "BOUNDS: no host start/stop, live login, credential, MFA automation, real session file, or network call to the portal; everything under stubs, VM mocks, or static text reads"
}
```

**After (the exact corrected text now in the proof instance):**
```
{
  "item": "a real Playwright/Chromium run of capture-session.cjs; any real host action (start/stop, live login, credential, MFA automation, real session file, network call to the portal); any real SSM call",
  "reason": "BOUNDS: host i-0167fd745ad906a66 is STOPPED throughout this order and this cell never starts it; no live login, credential, MFA automation, real session file, or network call to the portal, and no SSM call -- everything under those limbs is stubs, VM mocks, or static text reads. This exclusion does NOT extend to S3: the publish pass DID execute a real S3 action -- aws s3api put-object of the git-blob bytes to s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/capture-session.cjs, with a verified get-object readback matching sha256 f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d (see the capture-session.cjs artifact row's deploy_evidence above, commits 0670ef16cd/60bab95e58, both now ancestors of CLOUD)."
}
```

The rewrite: (1) drops S3 from the "excluded" item list entirely -- the item now names only the
limbs that remain genuinely unexercised (Playwright/Chromium execution, host start/stop and every
live-credential/session/network act under it, and SSM); (2) the reason names those same limbs'
true STOPPED/never-called state; (3) the reason explicitly states the publish pass DID execute a
real S3 action with a verified readback, citing the exact evidence already present at line `:23`
of the same instance (the same sha256, the same commits) rather than re-deriving or restating it
differently.

## Arm (b) -- no hash recut

`grep`-equivalent (Grep tool) confirms every sha256/blob value in the file is byte-identical to
before this edit; the diff touches only the two string values of `declared_exclusions[1]`. No hash
was recomputed, re-derived, or second-guessed.

## Arm (c) -- no publish replay

No S3 action taken by this cell, no ledger entry opened, no new packet. `git status` at this
worktree's `HEAD` shows only the one proof-instance JSON (plus this result.md, the order's own
proof-of-spec instance, and the session-serial file) as pending changes.

## Arm (d) -- no code touched

`capture-session.cjs`, `capture-session.sh`, and `README.md` are untouched -- not read for editing,
not staged, not committed by this cell. Verified via `git status` (none of the three paths appear).

## Arm (e) -- verification

`proof-of-spec-check.py` re-run on the `IB-rtk-1` instance after the wording fix:

```
timeout 120 py -3.12 .tools/proof-of-spec-check.py org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~13/IRPT_BCKEND.TO-IB-rtk-1.the-capture-tool-complete-lifecycle-observer-and-sticky-refusal.proof_of_spec.json --governing-order org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtk-1.the-capture-tool-complete-lifecycle-observer-and-sticky-refusal.md
```

Result: `VALID (rc=0)`. `acceptance` array unchanged -- still 3 rows, R107-AC1/AC2 `PASS`,
R107-AC3 `UNVERIFIABLE-BY-INSTRUMENT` (judgment, unchanged), same `expect`/`status` values as
before this cell's edit. This cell corrected only the text describing what was and wasn't
exercised; no criterion verdict moved.

## Criteria

- `R116-AC1`: PASS -- the `IB-rtk-1` proof instance re-validates `VALID (rc=0)` after the
  exclusion-wording correction, with no criterion verdict changed. Corrected exclusion text
  printed in full above (Arm (a)) for direct verification.
