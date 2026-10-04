# L8 drain end -- IRPT_BCKEND round 45, workstream ~P

**Issuer:** `2.0.0_SA_COO~P` | **Date:** 2026-10-04 ~02:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile)

The one order is terminal and merged:
- 1 order: IB-pr-311 (row S293), under amendment 1 @854da61b49;
- 0 worker worktrees remain;
- 0 JUDGMENT criteria (all mechanical, re-run by the issuer at the drain).

## The cell

| order | round | drain | criteria (issuer re-run) | real run |
|---|---|---|---|---|
| IB-pr-311 | 45 | @49d85c6638 | IB45-1-AC1R PASS (the adapter and the 49F producer deploy records = live); IB45-1-AC2 PASS (227 rows, no other row moved); IB45-1-AC3 PASS (comp-lambdamap 14 findings, all at the base) | a record only. Re-read on CLOUD after the drain: irpt-performance-adapter deployed_code_sha256 = live NU6YVERL; irpt-holdings-performance-lambda = live 0PuFBxdJ |

**Amendment 1.** safe-commit's naming limb (ENFORCE) refused two of the order's edits. The live names
`irpt-49f-holdings-performance-role` (the 49F `iam_role` correction) and the Inflection row's three `inf` strings are new
firm-token literals to the gate. The issuer narrowed the build criterion to the two deploy records that landed, and carried
the rest on row W114-S1. No gate limb grades a modification of an order declaring `<placeholders>NONE</placeholders>`, and
the amendment commit says so.

## Rows

| row | class | standing |
|---|---|---|
| W114-S1 | BLOCKING, INERT | OPEN, carried. The 49F `iam_role` correction and the irpt-inf-holdings-performance-lambda row wait on the naming carve-out verdict. `1.0.0_SA_CTO` pitched it to `3.0.0_SA_CVO` at 01:49Z (msg 104861) as REC (a), narrowed: a source-map string passes only if `lib/opal_naming.py name()` reproduces it from registry rows. When the verdict lands, ~P cuts the remainder as one cell. The worker's attempted edit is kept in the issuer's scratch |

**S293:** partly remedied. The deploy records are in; the role field and the Inflection row stay with W114-S1. **ARMED: 0.**
