# CN-j-2 (candidate for the round-7 recut) -- an error in a history-leaf row must surface where the run's consumers look -- design note, 2.0.0_SA_COO~D1, 2026-10-14 ~16:3xZ

Draft only. Nothing here is issued. It exists because the CTO's publisher CTO half (item 4, `ledger/NEVER_WIDEN_R7_J1_PUBLISHER_CTO_HALF.md` @9a492909b7) accepted the quiet leaf failure "for now" and made its
surfacing a condition of the portal promote (CTO msg 5648: "the promote waits on it, not on the hold alone").

## The defect, as built and as the CTO half states it

`lambda_function.py` (CN-j-1, merged `1c8ebf3e5d`) reports the four history leaves in `history_rows` of the run manifest and the pointer, OUTSIDE `results`, `expected`, `failed` and `all_present`. A leaf whose assembly
or write fails therefore leaves `all_present` true; the failure is visible only to a reader who opens `history_rows`. Today nothing reads the leaf, so the quiet failure is harmless. From the moment the AUA Trend
(CN-i-1, candidate `34cd12d2`, NOT landed) reads `category-views-history`, a stale or missing leaf would draw a wrong Client chip history with no signal.

## What the CTO asked for

"An `error` history row must surface where the run's consumers look (`all_present` or a manifest flag the readback grades)." No alarm is to be built (the moratorium): the surfacing is a field in the run
manifest and the pointer that a readback grades, never a notification.

## Shape of the cell (one publisher file, WORLD)

- Owned files: `infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py` and its tests (`tests/test_history_leaf.py`, `tests/test_completeness.py`), the same surface as CN-j-1.
- Behaviour to decide with the CTO (two options, REC the first): (a) `all_present` turns false when any `history_rows` row carries `error` or `verify_absent`, so every existing consumer of that flag sees it; (b) a new manifest
  key `history_ok` (and the pointer's copy) that the readback grades, leaving `all_present` as it is. REC (a): the consumers already look there, and an extra key is one more thing nobody reads. Cost of (a): a history-leaf
  failure now marks the whole run not-all-present, which the existing pointer logic may treat as a failed run; the cell must read what `all_present` false does downstream before choosing.
- Criteria shape (at most three mechanical): (1) a unit arm planting a failing leaf and reading the flag; (2) the seam against the pointer writer; (3) the existing CN-j-1 arms unchanged. Base: (1) and (2) fail.
- Deploy: a second publisher deploy under its own pair (CTO half owed), after CN-j-1's deploy has read clean; two acts never share a window.
- Not in the cell: the portal code (CN-i-1 and CN-l-2 are not landed); any alarm; any change to the 18 existing leaves.

## Where it goes

Round 7's issuance is closed (one issuer per round, spec and decomposition frozen mid-round), so this enters the round-7 L10 enrichment list as a round-8 cell, `CN-j-2`, ahead of the portal promote. The promote's
own pair (CN-i-1) carries the condition that the surfacing is deployed and read before the PROD push.

## The downstream read of `all_present`, as the CTO's gate requires (the issuer's PRE-READ, 2026-10-14 ~17:3xZ; the cell's first criterion re-runs it at its own base)

Instrument: `comp-find all_present` over corpus `all`: 263 hits across 93,374 files scanned (12,280 ephemeral-floor files, 7,690 binary and 2 unreadable files NOT searched), bands SURFACED 68, CONFIG 37, TEST 28, DOC 130. Read, not guessed, in the SURFACED and
TEST bands; the CONFIG and DOC bands (37 and 130 hits) were counted and NOT read line by line, and the archive logs under `org/audit/` are rail logs of an old query, not consumers.
- **The publisher itself** (`lambda_function.py`): `all_present` is computed at :651 AFTER every pair and every history leaf has been written (the publish loops precede it), and is then (1) written into the immutable run manifest (:689), (2) logged in the SUMMARY line
  (:730), and (3) returned in the invocation payload (:731). The manifest and the mutable pointer (`latest.json`, whose rows are keyed by each pair's own `status`, never by `all_present`) are written UNCONDITIONALLY after it.
- **No other first-party code reads it:** no portal file, no other lambda, no Terraform, no `.tools` script. The only code readers outside the publisher are the issuer's own checks (`r7_cn_j_1.py` :271, :307, :319; `r7_history_readback.py` :342). Hits in `data/etfs/.../test_coverage_gate.py`, the
  `bd-` and `cot-` ownership tests and `bundle_contract.js` are local variable or test names, not this flag.
- **The publisher's own tests** assert it (READ at the assertions, not inferred): `tests/test_completeness.py` (about ten assertions, all about the 18 gold-projected pairs, none about a history row) and `tests/test_history_leaf.py`: :140 is a HEALTHY run (True, stays); :220 is a scope without
  category-views gold, so the PAIR is missing (False through `missing_pairs`, stays); :190 plants a malformed dated object that the leaf OMITS and NAMES, row status still `published`, and asserts True. Whether :190 stays True depends on a decision the cell must take and state: does an
  omitted date count as a history-row error? REC: NO. An omission is a defined, visible outcome of the leaf (`omitted` names it); only a row with `status` `error` or `verify_absent` (the CTO's wording is "an `error` history row") turns the flag. Under that rule :190 stays True, the :8 docstring ("all_present
  is unaffected" for H4) is reworded, and the cell ADDS a test that plants a real `error` row and reads the flag. If the CTO wants omissions to count, :190 flips and the cell says so as its second criterion.
- **Consequence for the CTO's fork:** no consumer in the repository takes an action on a false `all_present`; a false cannot stop the 18 good leaves from being served, because they are written before the flag exists and the pointer does not read it. The fallback (a separate manifest key) is therefore NOT forced. The
  residual unknown is OUTSIDE the repository: whatever reads the invocation payload of the daily schedule (an asynchronous EventBridge Scheduler invoke, whose return value the scheduler does not consume, INFERRED, not read) and any human tooling over the manifests. The cell re-reads the
  schedule's target and its retry/DLQ settings at the base before the code.
