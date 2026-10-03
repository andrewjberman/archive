# L8 drain end -- IRPT_BCKEND rounds 36 (IB-pr-301) and 37-41, workstream ~P, and IRPT_DASHBD rounds 10-11, workstream B

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-03 ~08:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

Every order of these rounds is terminal and merged:
- 8 orders: IRPT_BCKEND IB-pr-301..306 and IRPT_DASHBD DB-b-18 and DB-b-19;
- 0 worker worktrees remain;
- 0 JUDGMENT criteria (every criterion is mechanical, re-run by the issuer at the drain).

Six cells are SERVED only in P-2's window, under both never-widen halves:
- packet `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~P/NEVER_WIDEN_SIGNOFF_PACKET_P2_WINDOW_20261003.md`,
  @855fdad77c, blob f3532bf5b9;
- CTO half `CTO_HALF_IRPT_DASHBD_P2_WINDOW_20261003.md` @e67cba94ac (batch 222).

The window opens on Andrew's B2 (PROD promote) word. It is carded to `0.0.0_AB_MSTR`, inbox 20261003T084251Z. Each outcome's
real run is that window's V leg; none has run yet.

## The cells

| order | round | drain | criteria (issuer re-run) | served |
|---|---|---|---|---|
| IB-pr-301 | 36 | @26240fa401 | IB36-3-AC1/AC2 PASS: 13 PATH B tests; export suite 181; reporting + contracts 135 | window A8 (export) |
| IB-pr-302 | 37 | @7d02c6fe8b | IB37-1-AC1/AC2/AC3 PASS: 7 route-pin tests; `_authz` 207 with only the 6 base failures (S15) | window A6 + A8 |
| IB-pr-303 | 38 | @b72601ad47 | IB38-1-AC1/AC2 PASS: claim `inferred` on a missing trading day; performance 246 | **SERVED already** as round 36 D1 (adapter U+miRkw3, CTO batch 207, D1 closed under batch 214) |
| IB-pr-304 | 39 | @cc13527fa3 | IB39-1-AC1/AC2/AC3 PASS: the edge admits the reporting SERIES path only; reporting-read wired for render grants | window A6 + A7 |
| IB-pr-305 | 40 | @74d2720dec | IB40-1-AC1/AC2 PASS: the export-download response contract (`data.download_route` with url + expires_at, sha256, byte_length); `_contracts` 114/0 | window A8; ~D's Download on DEV 3ff86a54 |
| IB-pr-306 | 41 | @eb707844ba | IB41-1-AC1/AC2 PASS: COMPOSED_FIRMS = Inflection + Cottonwood; `PathARetiredForFirm`; performance 251 | window B3 (adapter NU6YVERL, which differs from the live adapter by exactly `retained.py`) |
| DB-b-18 | 10 | @65a788ebf1 | DB10-1-AC1/AC2/AC3 PASS: method contract 0.3.0, 22 columns equal the emitted row, schema_hash 73e80ef7..; the three packages rehearsed | window A1-A6 + A3 |
| DB-b-19 | 11 | @b9b2f81739 | DB11-1-AC1/AC2/AC3 PASS: 38 short DIV debits admitted by negative share quantity; `irpt_reporting` suite 22 | window A1-A2 (in gold Mex71Y5g) |

## Rows these rounds raised

**BLOCKING, all 6 dispositioned by the issuer at this drain** (rows S300-S305, `2026-10-03T08:52Z`). Each was resolved in code by a
later cell and is served in the window.

| row | resolved by | served at leg |
|---|---|---|
| W104-S1 | IB-pr-302 (enforce reporting_read) | A6 / A8 |
| W104-S2 | IB-pr-302 (GetObjectVersion) | A6 |
| W104-S3 | batch 205 (c) plus IB-pr-302's removal of the export platinum policy | A8 |
| W104-S4 | IB-pr-302 (`facts.frozen_as_of`) | A8, B1, B2 |
| W105-S1 | IB-pr-304 (the edge pattern) | A7 |
| W105-S2 | IB-pr-304 (the read wiring) | A6 |

**OBSERVATION / INERT, open, ruled or carried:**

| row | content | standing |
|---|---|---|
| W104-S5, W104-S6, W105-S3 | contract and body choices | recorded in their cells |
| W106-S1 | the absence text says "missing" while the claim reads inferred | carried |
| W107-S1 | read wired with no requests table | prospect renders have no account |
| W108-S1..S3 | the test_seam_paired grant, the revision marker, the reopen-and-flip | ruled at the IB-pr-305 drain |
| W109-S1 | the public code is OBJECT_NOT_COVERED | ruled |
| W109-S2, W109-S3 | INERT | ruled |
| IRPT_DASHBD W5-S1 | one-pin note | carried |
| IRPT_DASHBD W5-S2 | the method-row hash holds only with `--tieout` | packet leg A3 passes `--tieout 0.037` |

**ARMED from these rounds: 0.**

## What the compile can grade now, and what waits on the window

- **Now:** each drain's criteria, each merge, and the six dispositions.
- **Waits on the window:**
  - P-2: every 49 Financial account served on method_version 2;
  - P-3: the summaries;
  - P-6: print and export on PATH B, and PATH A refusing 49F, on PROD;
  - FWD-8 realized on one served pair.
  Each is read at the window's V leg, as the CTO half's section 3 orders.
- **Then:** E3 (the ONE Black Diamond population pull) is cut after A5 is read back.
