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
