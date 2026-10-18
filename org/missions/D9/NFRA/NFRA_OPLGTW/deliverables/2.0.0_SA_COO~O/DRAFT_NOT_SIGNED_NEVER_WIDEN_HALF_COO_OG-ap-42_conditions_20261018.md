# DRAFT, NOT SIGNED -- COO conditions for the `OG-ap-42` never-widen half (2.0.0_SA_COO~O, 2026-10-18 ~12:0xZ)

Written BEFORE any worker has reported and before the applier's Phase A, so that the numbers cannot shape the conditions (the precedent of `DRAFT_NOT_SIGNED_NEVER_WIDEN_HALF_COO_OG-ap-40_conditions_20261018.md`). This file signs nothing: the half is signed as a separate file bound to the ask's sha256 and the release sha, after my own run of `ap42.AC1`.

Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-ap-42.round-43-ninth-batched-release-firm-pin-and-graph-pin.md`. Checks: `deliverables/2.0.0_SA_COO~O/r43/checks/ap42.AC1.sh`, `ap42.AC2.sh`.

## Conditions I will hold the ask to (each is read from the ask, the Phase A record and my own runs, never from the applier's report)

- **C1 Base.** `base_sha` equals the live ref read on the host from `/opt/opal-gateway/.deployed_commit`, and `6575999df5` (dell1's harvest release) is its ancestor. If the host reads anything else, the half is not signed.
- **C2 Take list.** Exactly four files: `app/probe_listener.py`, `app/graph.py`, `tests/test_og_pr1.py`, `tests/test_og_sec2.py`, each byte-equal to its blob at `trunk_sha`. `server.py` is not in the diff. The diff of `probe_listener.py` against live is exactly the firm pin; the diff of `graph.py` is exactly the host pin; I read both diffs, not the summary.
- **C3 Harvest carried.** dell1's four harvest files are byte-equal between live and the release, and the ask names their blobs as read at `base_sha`.
- **C4 No arming.** `armings` is 0 in Phase A and Phase B; the lease parameter is absent before and after; the half does not cover an arming (that is `OG-ev-7`'s own half).
- **C5 The pins are exercised, not asserted.** Phase A shows the mismatched firm refused 403 `probe_firm_refused` with the tool function never entered (a recorder), a lease without `firm` refused, a matched firm answered, a forged Graph host refused with no client built, and `graph.microsoft.com` allowed.
- **C6 Audit CLEAN.** `OG-sec-3`'s record reads CLEAN with 0 controllable; if it reads STOP, there is no release.
- **C7 Standing guards.** Hard guard on every host run; the 27-tool read 27 of 27; `tools/list` equal before and after; host md5 equal on every file but the four taken; unit limits unchanged; clock and failed units read before the ledger closes; 30-minute read-back with `NRestarts` 0.
- **C8 First refusal is a STOP.** The first call refused after the deploy, or any trigger in the ask, is a STOP and a rollback to the live ref, and the CLOSED or rolled-back time goes to the CTO and `0.0.0_AB_MSTR~Z` in one message (dell1 cuts on the live ref).
- **C9 Disclosed limits.** The firm pin compares the call's `firm` argument with the lease's firm; the account reference carries no firm. The pin does not check that the firm is the account's firm beyond the Cottonwood adapter's own fence, which stays.

## What I do not know yet

Whether `OG-pr-4` keeps `ac01` to `ac10` unchanged in meaning, whether `OG-sec-3` finds a controllable JWKS target, and whether the host still reads `6575999df5` at the GO.
