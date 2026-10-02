# DSGN_AMGTV1 -- ROUND 27 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-02 ~14:5xZ)

**Input:** `1.0.0_SA_CTO~Z`'s `ledger/COMPLETION_GRADES.round26.json` @0c4c6d6368, FWD-2 NOT_REALIZED (a page cell). Decomposition v27
and the issuance are @0b418007f9.

## 1. ORDER (1 of 1 terminal, drained)

| order | cell | worker | portal | instance | outer drain |
|---|---|---|---|---|---|
| `AV-ze-1` | every bar and bubble carries its served identity one hover away (FWD-2) | ~78 | f0683e8f | VALID (AC1 3/3; AC2 battery ALL PASS) | b53982a04b |

Blobs are LF with no 0x08. The bars' hover title carries the name, ticker, asset class, sub-asset class, sector (null said in words),
the 30-day figure and places moved (in words, or the served reason). The bubbles' SVG `<title>` carries the served display name, the
month's count, and whatever identity the chatter row serves, with the rest said "not served". The producer half (chatter rows serving
ticker, classification and places_moved) is RESAPP round 63 cell 3 (CTO msg 28528).

## 2. THE CANDIDATE -- portal `df019dba` (worktree 70, branch `dsgn-r27-onto-dev`, LOCAL)

It is remote DEV 415f50db (fetched ~14:4xZ) plus AV-ze-1, a fast-forward over 415f50db; DEV 415f50db contains PROD f76b02acb6.
**Battery on df019dba:** identity.cjs 3 of 3; `round26/checks/battery.sh` BATTERY: ALL PASS (12 checks 3/3, 14 of 14 harnesses, tsc 0).

## 3. THE REAL RUN -- walk `tmp/ui-walk/20261002T144632Z` (5174 = df019dba; ARM / DISARMED 14:51:21Z; site Z only)

104 shots, walk void no, 0 API issues. The price face (shot 004) renders 94 bars, every bar named, with the layout unchanged.
**Blind spot, named:** walk.mjs never hovers, so it cannot read the native hover titles. They are graded by identity.cjs on the
live-shape fixtures. A person hovering three bars and three bubbles on the served page is the FWD-2 DONE WHEN read.

## 4. OPEN

- The CTO's review of df019dba (a product file). The DEV push and the PROD promote of df019dba need Andrew's word (his earlier
  "yes to all" covered 0ab75973 only).
- The CTO's instrument items (msg 28537: fwd15 / fwd16, an ABSENT fixture row for FWD-15, the list.png chatter fixture) are
  round 28. Round 27's issuance stands, and to-pipeline-gate refuses a second issuance into a round.
