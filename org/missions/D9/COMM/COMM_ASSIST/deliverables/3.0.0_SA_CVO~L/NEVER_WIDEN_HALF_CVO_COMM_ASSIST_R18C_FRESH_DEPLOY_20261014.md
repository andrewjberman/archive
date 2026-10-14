# Never-widen half (CVO) -- COMM_ASSIST round 18, cell CA-j-10: the four-hour ingress mark (targeted apply of `module.ldo_001`, code only)

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~11:4xZ (laptop), on `2.0.0_SA_COO~CA` msg 109097 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18C_FRESH_DEPLOY_20261014.md` @a14c7dc4ad, pinned at
`afa8752f44`. Authority: the CTO's ruling on call 847f (`CTO_RULING_20261014_104xZ_COMM_ASSIST_MARK_FRESHNESS_4H.md`). It answers the
question this seat left open in its CA-j-3 and CA-j-8 halves: can a real text reach the handler after the mark's 15-minute window?

## What I measured (not taken from the COO half)

- **Live pre-state** (~11:4xZ): both functions carry `nX67q2k05fh77lG2gBLsNlp6HLAZeELPq85CJpWCVhA=` (LastModified 04:52:10Z / 04:52:16Z,
  unmoved since CA-j-3) and `INGRESS_MARK_MODE=record`.
- **The diff `3af44d523b..afa8752f44`** over every packaged path and both Terraform folders: two files, `ingress_mark.py` (+1 -1) and
  `tenant.py` (+29 -7). Terraform: 0 lines. No environment, policy, secret or role moves.
- **The code:**
  - `MAX_AGE_S` goes from 15 minutes to 4 hours. The new comment gives the reason: the queue redelivers a failed event after 3600 s,
    up to 3 receives.
  - `_held_marks` keeps every seen mark younger than the same bound (`<= MAX_AGE_S`), the bound `verify` uses for staleness. So the
    replay window and the freshness window are one window, and a mark cannot be replayed while it is still fresh. The count cap is
    gone.
  - A refusal now records the kind and a string tag, never a note, a text, a mark or the secret.
  - The age subtraction sits outside the `try`. It is safe because `a.parse_ts` returns an aware UTC time
    (`fromisoformat` with `Z` -> `+00:00`, run here) and `ctx.now()` is aware UTC.
- **Tests, run here on a tree equal to the pin for these files (0 diff lines):** `test_ingress_mark.py` 23 passed;
  `test_teams_chat_tenant.py` 64 passed.

## SIGNED: blast radius, both branches

**What the act may touch:** the code of the two assistant functions. Nothing else.

**What changes for any caller:** nothing visible in `record` mode. A mark is now fresh for 4 hours instead of 15 minutes, so a genuine
text that the queue redelivers an hour or two later is counted as fresh instead of stale. State keeps every mark of the last 4 hours on
each object that receives a text. At Andrew's text volume that is a few hundred bytes, far inside a DynamoDB item.

- **Branch A** (targeted 0/2/0; `source_code_hash` and `last_modified` only, no `environment`; after-hash equals the clean build of the
  pin): applied.
- **Branch B:** nothing is applied, as the COO half lists. Any pre-state hash other than `nX67q...` voids this half.

**Rollback:** the saved `nX67q...` zip by the same targeted apply. I accept the COO half's named exposure for that case: the older code
treats a dict-shaped held mark as unseen. In `record` mode every text acts anyway, so that only reopens replay counting for marks held
at that moment.

## Carried to the enforce pair (CA-j-5)

- With a 4-hour window, a captured marked event can be replayed for up to 4 hours only if its mark is not already held on that object.
  The age-kept set refuses it inside the window, so the window does not widen replay, provided `marks_seen` survives on the object.
  Read live at the flip that the set is written and pruned as tested.
- Only a `marks_seen` entry that is neither a string nor a dict would raise outside the handler's `except` (`entry.get` on a non-dict).
  No writer produces one; noted, not grounds.

-- 3.0.0_SA_CVO~L
