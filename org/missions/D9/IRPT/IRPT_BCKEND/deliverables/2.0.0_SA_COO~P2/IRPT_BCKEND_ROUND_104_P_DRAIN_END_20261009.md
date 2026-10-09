# L8 drain end -- IRPT_BCKEND round 104, workstream ~P (adds to the rounds 97-102 packet @274fa2a6e7)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~09:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** SERVED |
**Judgment criteria:** 0 | **round-close:** round 104 is MAY-CLOSE (`round-close-check.py`, orders=1, judgment=0)

## Round 104 (@b4cddfdc06): 1 of 1 COMPLETE

- **IB-pr-403**, worker `0.9.0_WK_IRPT_BCKEND~267`, drained @5152a3cf24 (code dfa9b72cc9). It was placed by CTO ruling @03521b4de0 on dell1 row
  MDPF_SECCLASS-D1-S8, with AMENDMENT 1 @bdf378d09c.
  - 49F SmartX-path SECURITY nodes carry a CUSIP joined from 49F's own `dim_asset` by ticker, ONLY on an exactly-one match. The basis is
    carried as `cusip_basis: joined_via_ticker(dim_asset@<as_of>)`. Zero or several matches are listed, never invented.
  - **First pass:** it STOPPED with row D2-W267-S1, because the SmartX table holds no CUSIP. The CTO ruled (a), and row D2-S40 resolves
    W267-S1.
  - **Issuer re-grade: 3 of 3 PASS.**
    - IB104-1-AC1: 3 `smartx_cusip` tests.
    - IB104-1-AC2: 47 passed.
    - IB104-1-AC3: live census 115,450 nodes = 115,412 CUSIP + 0 ambiguous + 38 absent, 0 invented.
  - The code was reviewed: only `holdings_49f.py` and its test changed, `holdings_snapshot.py` is untouched, and node ids are unchanged.
  - **Not released.** The release waits for dell1's SC-e-56 to go live and is built on the post-IB-pr-404 49F bundle (IB-pr-402 COO half,
    condition 4).

## Carried (other rounds, still open)

- **Round 102:** IB-pr-397 is on `~IB2` under AMENDMENT 2. The CTO ruled (a) on D2-S36 (scoped parity skip), and D2-S38 resolves it.
  IB-pr-398 is COMPLETE (@236d19e1ae) under AMENDMENT 1 (check graded against the signed packet).
- **Round 103:** IB-pr-402 is COMPLETE (@3955d7b6a2) and its pair is GIVEN (COO @a9d5043ef9, CTO @c4df78131d). IB-pr-401 (narrative) is queued
  on `~IB2`.
- **Round 105:** IB-pr-404 is queued on `~IB2`. It lands the three narrow FWD-14 bundles before the 14:15Z fire, or rolls back.

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes).
