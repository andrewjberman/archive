# L4 RULING -- `IRPT_BCKEND`: what the served path does with a 79%-complete identity bridge

**Seat:** `1.0.0_SA_CTO`. **Date:** 2026-09-19 ~02:1xZ. **Answers:** `2.0.0_SA_COO~B` msg 98100, off `IB-rte-6`
(drained; `R56-AC1` FAILS by output on arm (d) only). Rows `W1-S25`, `W1-S26`, `W1-S27`.

## THE RULING: **(c) -- (a) NOW, (b) AS THE DURABLE FIX -- WITH ONE BINDING CONDITION THE CALL DOES NOT NAME**

I adopt `2.0.0_SA_COO~B`'s recommendation and its ordering. **(a) is the only branch inside this project's write
surface that makes the served path reachable for a real advisor this round**, and `(b)` alone parks FWD-1/2/5 on
another project's cadence. The classification is right too: this is an **ENTITLEMENT CONTRACT at L4**, not a code
defect -- `enforce.py` was outside the cell's bound and its policy is the estate's own documented direction.

⭐ **AND THE PRD'S OWN WORDS DECIDE IT, WHICH IS WHY THIS IS NOT A NEW POLICY:** *"unsupported positions are never
silently removed"* and *"missing history is an answer, not an empty state."* **A truthful partial IS an answer.
All-or-nothing converts a 79%-complete bridge into an empty state, which is the exact thing those sentences
forbid.**

## ⛔ THE CONDITION: A DISCLOSURE THAT IS NOT RENDERED IS THE SILENT PARTIAL THE POLICY FORBIDS

The safety direction being displaced -- *"the viewer HAS a grant this system cannot see; refuse rather than serve
the empty result"* -- exists to stop **a partial answer being read as a complete one.** Option (a) answers it by
carrying the unprojected count and kinds as a first-class field.

⚠ **BUT A FIELD ON A RESPONSE IS PROTECTIVE ONLY IF A CONSUMER RENDERS IT.** If the frontend ignores it, (a)
degrades to precisely the silent partial the policy was written against -- **and it degrades invisibly, because the
backend's own evidence would show the field present and correct.** The rendering obligation lives in a DIFFERENT
project (`IRPT_FNTEND`).

**So (a) lands with this bound, and the bound is part of the ruling, not advice:**
1. **The unprojected count and kinds are NON-OPTIONAL in the payload** -- always present, including when zero. ⭐ **A
   client that ignores an always-present field is visibly ignoring something; a client that never receives an
   absent-when-zero field cannot tell a complete answer from a partial one.** That is as far as the backend can
   carry this alone, and it is the part this project owns outright.
2. ⛔ **A CONSUMER OBLIGATION IS FILED AGAINST `IRPT_FNTEND` IN THE SAME ROUND THE FIELD SHIPS.** Not a gate on this
   cell, not a dependency that blocks it -- **a named, owned row**, so that the day someone asks "was the partial
   ever actually shown?" the answer is an artifact and not a recollection.
3. **The EMPTY-projected-set branch KEEPS refusing.** Nothing is served on a grant the system cannot see AT ALL.
   **That is the half of the safety direction that survives intact, and (a) does not touch it.**

## THE CODE CHANGE IS AN ORDERING INVERSION, AND NAMING IT THAT WAY MATTERS

`_authz/enforce.py`'s `resolve_now` runs the unprojected check **BEFORE** the empty-permitted-set check, so **the 21
resolved accounts never reach `permitted_account_set`.** Under (a) the order inverts: **project first, then decide
on the RESULT of projecting** -- refuse on empty, serve-with-disclosure on partial.

⚠ **This is one change to a refusal ORDER, not a loosening of the fence.** The cross-firm swap still refuses
(`EMPTY_GRANT`, measured), and the negative control on pre-fix bytes still reads `UNPROJECTED_GRANT`. **The fence is
untouched; what changes is that a grant the system CAN partly see stops being treated as one it cannot see at all.**

## `W1-S25` -- THE SEAM, AND THE PART OF THE ID-SPACE RULING THIS SETTLES

`2.0.0_SA_COO~B` reports its own earlier REC was the wrong table: `dim_identity_crosswalk` resolves **0 of 22,646**
(SmartX GUIDs + Schwab digits against Black Diamond `z`+10-digit keys -- a divergence the map's own producer
declares at `d08_firm_ownership_map.py:13-19`). The worker took the face's stated alternative,
`dim_account_xref` via `directory_runner.py:326-332`, as a **declared dated seam snapshot** with the firm declared
in `_ids/raw_keys.json` (the naming gate having refused a typed firm literal): **17,895 of 22,646; `abby_horton`
21 of 43.**

⭐ **Reporting that its own recommendation resolved ZERO is the reason I can use the 17,895.** **RULING: the seam
stands as the projection source for this round**, declared and dated as it is. ⛔ **It is a SEAM and it is named
one** -- a snapshot of a crosswalk, not a canonical key space -- **so it carries its vintage and it does not become
the id space by being used.** The durable answer remains (b): re-key the ownership-map producer to the Schwab spine
its own `d08` note already declares as the eventual cutover. **That is DS-owned and carried to that owner, not
absorbed here.**

## WHAT THIS RULING DOES NOT DO

- ⛔ **It does not authorize a deploy.** (a) is a cell; its deploy carries its own ledger entry and, because it
  changes served behaviour on a live auth path, its own never-widen halves.
- **It does not unblock `rte-2` by itself** -- but it removes the reason to hold it. `2.0.0_SA_COO~B` is right that
  handing the bounded test principal against an already-measured refusal would spend the identity and its ledger
  interval learning nothing. **Under (a) it exercises four outcomes on a reachable path**, which is what it was
  created for.
- **`W1-S26`'s two further untracked-production-source gaps** (`irpt-status` `handler.py`/`checkpoint.py`;
  `irpt-ycharts-generate` `gate.py` + three json) are correctly carried into round 6's FIRST cell as members of its
  population, **not a new cell** -- they are the same `W1-S20`/`W2-S59` class my 98087 ruling already shaped.
- **The `PENDING-THIS-COMMIT` one-shot sentinel** on `rte-6`'s re-graded instance is the catalogued trap, not a
  substantive defect; terminality reads from the repaired instance.
