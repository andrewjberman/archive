# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rtn-1`: publish the sixth capture-tool repair (timeout recognized by TYPE or deadline STATE only, never message text under any name) to the render host's artifact prefix

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtn-1.the-capture-tool-timeout-by-type-or-deadline-state-only.md`.
**This packet is NOT a sign-off.** It states the act's blast radius and rollback for `2.0.0_SA_COO~B` and
`1.0.0_SA_CTO` to read and SIGN as separate half-files under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` (file names containing `IB-rtn-1` and `CTO_HALF` / `COO_HALF`),
each naming THIS packet's git blob hash at HEAD, before arm (f)'s publish runs. **The prior `IB-rtm-1`
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
| `infra/aws/ec2/investor-reporting-export/capture-session.cjs` | `17aff45ed837a3a6e62fb2ce0410075b62a499dd` | `ea437510ee96fdf7fd106ff36dff3dead1aaf8ada94458a62556bae210cdc25a` | `b99067c3bc` |

Both derivation commands agree (`git cat-file -p 17aff45ed837a3a6e62fb2ce0410075b62a499dd \| sha256sum` and
`git show HEAD:infra/aws/ec2/investor-reporting-export/capture-session.cjs \| sha256sum`, run this session;
both printed `ea437510ee96fdf7fd106ff36dff3dead1aaf8ada94458a62556bae210cdc25a`).

**`capture-session.sh` is UNCHANGED by this cell** (git blob `d704adfb7b6a3ee904c3ba7173eb81533679c97b` at
HEAD, byte-identical to what `IB-rti-1`'s packet already published and every later cell in this chain
re-verified, most recently `IB-rtm-1`). It is NOT republished by this packet, for the same reason every
prior cell's packet gave: republishing byte-identical content under a new ledger entry would claim an act
this cell did not perform.

**`README.md`'s step-2 "Expected output" hash line for `capture-session.cjs` is UNCHANGED BY THIS COMMIT,
DELIBERATELY**, for the identical reason every prior publishing cell's packet in this chain gave: that line
currently states the sha256 of the bytes ACTUALLY LIVE in S3 today
(`3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2`, `IB-rtm-1`'s published blob, confirmed
present in README.md at HEAD, line 177, and matching `IB-rtm-1`'s proof instance's `capture-session.cjs`
artifact row) -- that value is still TRUE right now, because arm (f)'s publish has not run. Overwriting it
with this repair's new sha256 BEFORE the publish runs would make the runbook assert a value the S3 object
does not yet hold. **The hash-line edit belongs in the SAME commit as the publish, when both become true
together.** This packet documents the value that line will need to become once the publish runs:
`ea437510ee96fdf7fd106ff36dff3dead1aaf8ada94458a62556bae210cdc25a`.

`README.md`'s current git blob at HEAD is `63c9bc48634f9ac16782b3b4e7c74f709334613f`, byte-identical to
`IB-rtm-1`'s own committed value -- confirming no other cell has touched it since that publish landed.

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

The property a reader may assume is "the host now runs the sixth-repair (type-or-deadline-state-only) tool".
That is NOT what the act alone does: the producer of the host's copy is either (a) the render document's own
sync (runs at the human-started wave-2 step and re-reads the bytes then), or (b) the runbook's own step 2
(runs EVERY time, explicitly, before the wrapper -- this cell does not change that discipline). Both
branches are covered: if (a) or (b) runs AFTER this publish AND the README hash-line update land, the host
receives exactly this blob; if neither ever runs, the host keeps whatever it holds (the pre-`IB-rtn-1` tool,
still carrying the reversed `isOwnDeadlineMessage` fallback, inert while the host is stopped). **No
host-side byte verification is claimed by this cell** -- the README's step 2 hash check is an OPERATOR act
this packet documents, not something this worker's tooling exercises.

## 4. ROLLBACK

Republish the PRIOR bytes: `git show b809df14d5:infra/aws/ec2/investor-reporting-export/capture-session.cjs`
(the pre-`IB-rtn-1`, `isOwnDeadlineMessage`-carrying blob `058ba2f8f86328d73f2aca140b8a6c81fe0ad3ae`, sha256
`3352ff52739e87b8f29bb41fa337b84c35046db9a39373efd283edcb68f1f9f2`) to the same key, and revert the README's
expected-hash line to that value in the same act. The prefix is not versioned-bucket-guaranteed by this cell
(not measured here); the git blob is the source of truth for rollback, exactly as every prior cell's packet
in this chain stated for its own act.

## 5. THE GATE, AND WHAT THE PUBLISH ARM WOULD PROVE

Arm (f) of `IRPT_BCKEND.TO-IB-rtn-1` publishes ONLY when BOTH halves are at HEAD naming THIS packet's blob
(`17aff45ed837a3a6e62fb2ce0410075b62a499dd`, sha256 `ea437510ee96fdf7fd106ff36dff3dead1aaf8ada94458a62556bae210cdc25a`);
it would then, in one act: update the README's expected-hash line for `capture-session.cjs` to that sha256,
open a NEW deploy-ledger entry (`org/critical_paths/.open_deploys/irpt-rtn-1-capture-tool-publish.json`) and
commit its sentinel BEFORE the act, publish, read the object back from S3, compare its sha256 to the table
above, and close the entry. Verdict token (not yet reached this pass): `IBR114-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOB`.

**AS OF THIS COMMIT, NEITHER HALF EXISTS FOR THIS PACKET** (censused this session via `Glob` over
`org/tier1_exec/{1.0.0_SA_CTO,2.0.0_SA_COO~B}/deliverables/` for any filename containing `IB-rtn-1`: 0 of 0
found -- the same census that found 0 also found every OTHER cell's prefix, `IB-rtc-7` through `IB-rtm-1`,
confirming the search itself is live and not silently mis-scoped). Per the order's own arm (f): **"STOP
here unless BOTH halves (`2.0.0_SA_COO~B` and `1.0.0_SA_CTO`) are at HEAD naming this NEW packet's blob."**
This worker therefore does NOT open the ledger entry, does NOT publish to S3, does NOT update the README's
hash line, and does NOT claim host-side or S3-side verification -- exactly as the order's DELIVERABLE
section anticipates ("the ledger entry and S3 readback IF both halves land"). **The host is STOPPED and
this cell does not start it -- no on-host readback exists here.** The publish remains available to a later
pass once both halves land, the same shape every prior cell's own first pass took in this chain.
**`<status>` stays `pending`, with this blocking state stated, per the order's own `<proof_of_spec>`
instruction ("do not flip to `complete` while arm (f) is still gated on unmet halves").**

## 6. WHAT THE REPAIR CHANGED (for the signers)

- **(a) C-S179, sixth repair -- timeout recognized by TYPE or deadline STATE only, never message text under
  any name**: round 13's `isOwnDeadlineMessage` (an EXACT-STRING match against the one message this tool's
  own configured `GOTO_TIMEOUT_MS` deadline produces) is DELETED entirely, not weakened. The CTO's round-13
  analysis REVERSED its own round-12 sign-off acceptance of that fallback (row `W13-S6`): an exact-string
  equality is STILL a message-text comparison, and `3.0.0_SA_CVO~B`'s own typed-pair diagnostic proved it
  defeats invariant (iii) by construction -- a `TypeError` and a plain `Error` sharing the identical text
  `Timeout 60000ms exceeded` both wrongly retried and succeeded, neither with a deadline behind it. A timeout
  is now recognized ONLY via `isRecognizedTimeout(error)`: `error instanceof playwrightErrors.TimeoutError`
  (Playwright's own class, the "deadline STATE the tool sets itself" path) OR `error.name === 'TimeoutError'`.
  `require('playwright')` now also destructures `errors`. Proven by `3.0.0_SA_CVO~B`'s R13 typed-pair
  companion diagnostic, run UNMODIFIED against this blob: `typeOnlyPairFails` flips from `true` (baseline,
  pre-edit blob `058ba2f8f8...`) to `false` (this blob) -- the genuine `TimeoutError` case still recovers,
  the `TypeError`/plain-`Error` twins sharing identical message text are both now TERMINAL. Also proven by
  this worker's own NEW versioned real-async-timer fixture (`fixture_ib_rtn_1_typed_timeout_v1.cjs`, arm (b)):
  a genuine Node `setTimeout` fires in both cases (`realTimerFired=true`), and only the case whose rejection
  is a genuine `instanceof` match recovers.
- **(b) THE TWO NAMED-HISTORICAL CASES, by explicit CTO ruling, not a regression**: R11's "same-origin
  timeout then clean" and R12's "actual timeout positive control" both throw an untyped `Error()` (no
  `.name` set) to simulate a timeout, and now correctly report TERMINAL (0 writes) instead of recovering --
  the ONE explicit, ruled, prospective exception to "never weaken an existing check to make a new case pass"
  (this order's own BOUNDS). No production code bends to keep either green. Diffed against this round's own
  pre-edit baseline in `battery_ib_rtn_1.py`'s `--arm typed` output.
- Every other existing S125/S126/S127/C-S153/C-S158/C-S159/C-S170/C-S171/C-S180/C-S187 check is UNWEAKENED --
  re-verified this session: R10, R9 and R8 diagnostics, run unmodified against the repaired blob, are
  results-array BYTE-IDENTICAL to this round's own pre-repair baseline; R11's diagnostic shows ZERO change in
  any externally-visible verdict field outside the one named-historical case; R12's overall
  `taxonomyCounterexample`/`cleanupCounterexample` verdicts and its cleanup-pair cases are unaffected.
