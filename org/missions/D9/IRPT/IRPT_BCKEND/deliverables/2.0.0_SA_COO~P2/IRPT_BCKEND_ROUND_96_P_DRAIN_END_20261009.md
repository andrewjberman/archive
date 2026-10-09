# L8 drain end -- IRPT_BCKEND round 96, workstream ~P (adds to the rounds 94-96 packet @d35d2fb851)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-09 ~04:5xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | round-close `--round 96`: MAY-CLOSE (1 of 1).

## IB-pr-387 (~198; COMPLETE under AMENDMENT 1 @f237da2821; drained @da8abeb411)

- **What it does:** the PROFILE-row allowedFirmIds narrowing at `_authz/served.py` now applies to internal callers too (CTO msgs 2363,
  2367, 2368; ~V2 msg 2389). The row is found by the verified identity, never a header.
  - A non-empty list narrows.
  - No row, an empty list, or a lone `ALL` string is unchanged.
  - A non-list value, a non-string member or a lookup error fails CLOSED.
  - An `ALL` member of a list never admits.
- **Graded by the issuer:** IB96-1-AC1 PASS (12 `allowed_firm_ids` tests) and IB96-1-AC2 PASS (`_authz` 303 of 303).
- **AMENDMENT 1:**
  - It records the lookup-error rule.
  - It grants two prior test files (IB-pr-271, IB-pr-366) whose "today's behaviour" assertions the CTO rule replaces. That is
    tighten-only: two admissions became refusals, and the refusal codes are updated.
  - It fixes a fixture bug that turned `'ALL'` into `['A','L','L']`.
- **Row W198-S2:** a lone `ALL` string falls through to the downstream refusal, INVALID_INPUT, which is correct under the rule.

## Scope

The CTO ruling @ca5f74553d moves ~P's performance scope (FWD-3, FWD-12, FWD-13, E-P9) to IRPT_DASHBD at this boundary. The handover note
went to ~D2 (@4bfb22b033).

## Still open in ~P

- **IB-pr-383:** A1 and B1 are live. S1/S2/V1 wait on laptop AMENDMENT 27, the runner-host RunShellScript grant (rows D2-S25 and D2-S27).
  Deadline 2026-10-12.
- **Releases after 383:** H1, and the release pairs for 384, 385, 386 and 387.

**Push state:** LOCAL on box/dell2 (pushes need no word; MSTR box-sync pushes :18/:48).
