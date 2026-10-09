# L8 drain end -- ADVI_COTBKF round 41

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-09 ~14:3xZ | **For:** `3.0.0_SA_CVO` (L8 compile; the one mechanical criterion
is graded below)

Round 41 was cut as one issuance @3089cde892 (`fanout: 1 of 1 chains, cap 8`) on `1.0.0_SA_CTO~DELL2` ADDENDUM 13 @9326a48990 (msg
3423). It is one SERVED cell.

| order | item | assignee | state |
|---|---|---|---|
| CB-ao-1 | deploy the cot gold `_ff_worker` carry-forward stamp under a pair | `0.7.0_AE_CloudOps~CB2` | complete; report @3b9c1f32a4; ledger CLOSED |

Pair: COO half @3089cde892, CTO half @9dd6703dd1 (msg 3431). Released by AMENDMENT 1 @7179ea76bd.

## The real run, by the issuer

```
s3://opal-data-cot/code/gold/B_00.canonical_holdings.py  VersionId hU7ZrZTD5NDlVvuSo9aBMUd1hKUg_lAe  LastModified 2026-10-09T14:19:29Z
sha256(served) = 45fbbd921f02...  = sha256(repo HEAD file) = 45fbbd921f02...
```

The issuer fetched the served object at ~14:3xZ and compared its hash to the repo file.

## What the round delivered

- **The carry-forward stamp is live in Cottonwood's gold code.** Exactly one key moved to one new version:
  `BMqu7SNC...` -> `hU7ZrZTD...`. The prior version is kept, and the rollback was proven executable.
- **Census:** +26/-1 lines, every changed line inside `_ff_worker`. The applier corrected two paperwork figures in this issuer's order:
  - the order said "+25/-1"; `git numstat` gives +26/-1;
  - the order's line range 1339-1395 is narrower than the function, which ends at 1424.
  Both are benign. The census rule (only `_ff_worker`) held.
- **Proof:** `test_b00_ff_carry_claim.py` gave 3 passed in a detached worktree on the FETCHED SERVED bytes (the CTO half's condition).
  A planted mutant drove it to 2 failed, so the test binds to those bytes.
- **The path is unreachable for cot today** (`schwab/silver/rps/` empty), so no gold output changes now.

**Watch item (CTO half condition; owner `2.0.0_SA_COO~C2`):** the next cot gold run's output fingerprint is read unchanged.
- The cot gold run is manual (CB-aj-1 census: 0 scheduled writers), so this item waits for the next manual run and has no clock.
- It un-parks when that run lands.

**Rows:** none new. ARMED: 0.

**Round-close check:** see the line in the issuer's log. The order has no judgment criterion.

**Also in flight:**
- round 42 (~69, writer reads its registry locally; then the two-key deploy);
- round 43 (~70, Cottonwood's sources entry and the TWR rebuild);
- round 38's mint, held until round 43 drains.
