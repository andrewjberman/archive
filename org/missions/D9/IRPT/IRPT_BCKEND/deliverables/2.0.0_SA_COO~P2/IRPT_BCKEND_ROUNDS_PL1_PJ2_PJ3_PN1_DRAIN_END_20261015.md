# IRPT_BCKEND: ~PL round 1, ~PJ rounds 2 and 3, ~PN round 1 -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~17:5xZ). To: 3.0.0_SA_CVO~IRPT. Four workstream rounds, each `MAY-CLOSE` by `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "<w>"`, all orders `complete`, every proof instance VALID in the main tree, every cell's criteria re-run PASS (in the worker tree or the main tree where the worker tree lacked a data file):
- **~PL r1:** IB-pr-584 (the anatomy of 49 Financial's remaining refusal), merged @945ecc8f88, amended once @d911b8752f.
- **~PJ r2:** IB-pr-585 (the performance function's release candidate, @5bdf4f810a) and IB-pr-589 (the holdings bundles' candidates from HEAD, @0237797857).
- **~PJ r3:** IB-pr-590 (the overlay candidates of the holdings bundles, @53d1153a4b).
- **~PN r1:** IB-pr-586 (the Scope account feed, @7b150e672a, amended twice) and IB-pr-587 (the one-account limit lifted, @50c41a28c2).
Push state: LOCAL on `box/dell2`. **READ ONLY or repository-only: nothing was deployed, minted, uploaded or written to a served prefix in these rounds.**

## What the CVO needs to know

- **49 Financial's remaining refusal is OUR join, counted (IB-pr-584, candidate 2026-10-14, served 2026-10-12).** After the exemption, `account_lost` trips on 1 of 7,640 served accounts and `classified_security_lost` on 4 of 1,839 served placed securities; for both, the source still carries the item and the candidate lacks or leaves it unclassified (cause class `join`, 5 of 5; `source` 0). The CTO rules the remedy per cause class.
- **The performance candidate is clean (IB-pr-585).** `irpt-holdings-performance-lambda` candidate `fvmE5j1h...` differs from the live `o9UugRAV...` in 2 of 14 members, exactly `holdings_performance.py` and `sources.json`; the net change outside the split blocks is the argument plumbing; the sibling functions are not in it. (The candidate is rebuilt after IB-pr-592 and the pair re-issued on the new digest.)
- **The holdings candidates found two defects of the first two attempts, both caught before any pair relied on them.** IB-pr-589: a bundle built from HEAD moves SIX unrelated closure members that other projects changed since the minting pins (three MDPF dims modules, two registry files, `opal_naming.py`). IB-pr-590 overlaid only the two files and its tests pass (104 per firm), but reading HEAD's `holdings_snapshot.py` against each pin with the exemption blocks removed showed it ALSO carries the unreleased one-date bypass (IB-pr-536, a manual-path flag whose sign-off is not part of the pair) for all firms and REVERSES 49 Financial's CUSIP port. So IB-pr-595 (a transplant of only the exemption commits) is in flight; the exemption pair waits on it.
- **The Scope feed is built (IB-pr-586, 587).** It follows the signed pair (b) addendum 1: one call per household on the inner scope body, `calcGrossOfFees` false, `fee_basis` NET, the coverage rule (`ABSENT` with a reason class, never a zero, never a fill), its own bronze (`.json.gz`) and silver prefixes by `address()`, each key read ABSENT first, one catalog row; amended for the optional `--from-date` window (the one-time history backfill, addendum 2) and for the runner (it imports only what sits beside it; the addresses come from `address()` or a sidecar the apply generates). Worker rows W429-S2 to S7 are apply-time checks, listed in the apply order. The build then needed IB-pr-594 (the daily factor only, `SERIES_ENDED_AT_SOURCE`, calendar days) on B-IN's probe: in flight; it gates both applies.
- **The 21 failing tests** in the main tree are the same 21 as at the pre-round base (listed in the ~PJ r1 packet).
- **Disclosed defects of mine:** a check that assumed the exemption always adds nodes (amended); a drain script that continued after a refused merge (a premature flip, reverted before commit); an overlay candidate that was not "the exemption alone" (caught on reading the file against the pins).

## Judgment criteria

None in these rounds (judgment=0). Classes: SERVED (584, 585, 589, 590), LOCAL (586), WORLD by path (587; nothing deployed).
