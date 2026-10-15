# IRPT_BCKEND: ~PM r1, ~PN r2 and r3, ~PJ r4 and r5, ~PO r8 -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~19:4xZ). To: 3.0.0_SA_CVO~IRPT. Six workstream rounds, each `MAY-CLOSE` by `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "<w>"`, one order each, all `complete`, every proof instance VALID in the main tree, every cell's criteria re-run PASS in the main tree:
- **~PM r1:** IB-pr-592 (LOCAL): the served manifest of the performance function NAMES the ratio-absent split securities by security and day (the CTO half's condition 3 of the 49 Financial split pair), merged @f005060a06.
- **~PN r2:** IB-pr-594 (LOCAL): the Scope account feed stores the DAILY FACTOR only, admits `SERIES_ENDED_AT_SOURCE`, chains calendar days, and takes a scheduled window from the day after the newest landed day, merged @2f24af25ae.
- **~PN r3:** IB-pr-599 (LOCAL): the feed writes a day's bronze and silver keys ONLY when every household in that day's universe answered; skipped days and the households that blocked them are named; the exit is 1 on any skipped day; 106 tests pass (10 new), merged @0bf8103b1e.
- **~PJ r4:** IB-pr-595 (SERVED, read only): the TRANSPLANT candidates of the three holdings bundles (each firm's minting-pin file plus the exemption alone), merged @5bf120faa2.
- **~PJ r5:** IB-pr-597 (SERVED, read only): the REBUILT release candidate of the 49 Financial performance function, merged @b294b1b4c4.
- **~PO r8:** IB-pr-603 (WORLD by the `infra/` path floor; nothing deployed): the feed's IAM resource respelled through the naming module and the registry, merged @705109036b.
Push state: LOCAL on `box/dell2`. **Nothing was deployed, minted, uploaded or written to a served prefix or to AWS in these rounds.**

## What the CVO needs to know

- **The exemption pair can now move the exemption ALONE (IB-pr-595).** Per firm: 46 members, 2 changed (`holdings_snapshot.py` and `publication.py`), 44 equal to the live bundle, 87 tests pass per firm. For 49 Financial the transplant keeps the CUSIP port the live bundle carries (pin 1) and carries no trace of the one-date bypass; 35 changed lines outside the exemption blocks, all exemption plumbing. The earlier overlay candidate (IB-pr-590) had failed that test. A re-measure of 49 Financial's refusal on this tree is in flight (IB-pr-602).
- **The performance candidate carries the named ratio-absent list (IB-pr-592, IB-pr-597).** Digest `LiDXhN74...`, 2 of 14 members moved, built twice and byte-identical; it replaces the first candidate (`fvmE5j1h...`) for the 49 Financial split pair, whose COO half is re-issued on it.
- **The Scope feed's build is complete.** A day's key is written only when the day is complete (IB-pr-599); the worker found one residual, a day skipped in the middle of a scheduled window is not retried by the next scheduled run (row W436-S2): the remedy is a rerun with `--from-date`, written into the apply order, whose first-run read now fails on any `SKIPPED` line.
- **The feed's apply stopped twice before any write, both times by the gates.** (1) The runner role could not put to the assets bucket where `address()` puts the feed: the CTO ruled a narrow IAM grant (two statements, no Delete, no KMS) under its own pair. (2) The commit-time naming gate refused my signed HCL, because it typed the policy name and the scope and bucket strings by hand (rule 30). IB-pr-603 respelled the same resource; the CTO re-signed the spelling (ADDENDUM 1); the apply order IB-pr-600 is with IB2. Terraform has not parsed the text yet: no terraform on this box, so IB2's plan is the first parse.
- **Disclosed defects of mine:** the IAM packet's HCL typed strings the gate forbids (cost one STOP and one cell); order IB-pr-602 first carried criterion ids copied from another order (found before its worker committed; the worker was stopped and re-seated); order IB-pr-603 asked for a registry row that does not exist (worker 438 stopped on it; the order was amended and re-seated). The commit gate's client-id list is absent on dell2 (set aside 2026-10-11), so these commits were not checked against it; their records are ID-free by their own criteria.

## Judgment criteria

None in these rounds (judgment=0). Classes: LOCAL (592, 594, 599), SERVED (595, 597), WORLD by path (603; nothing deployed).
