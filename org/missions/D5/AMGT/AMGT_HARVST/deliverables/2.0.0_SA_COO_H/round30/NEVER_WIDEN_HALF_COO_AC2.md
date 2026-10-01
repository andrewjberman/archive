# NEVER-WIDEN -- COO HALF: the Seeking Alpha probe -- an account read on the stored token, then one listing page, OUTSIDE the Worker (`HVST-ac-2`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~18:0xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rulings served:**
- `ROUND_ANALYSIS.round29.md` @`d0bc0a79f0` ruling 3, section 4 item 2;
- `ac-2` AMENDMENT 1: the probe runs outside the Worker, so no sign-in path exists.

**Vendor authority:** R-21 @`b390c36444`, on the mechanism of the collector's own client code.
**Code pin:** CLOUD at the dispatch commit, carrying `ab-1` (token-first sessions) and `ab-3` A0. The act prints
`git diff --stat <pin> HEAD -- lib/opal_data_harvest` and STOPs on any line.

## ROUND-25 RULING 1

| # | step | requests | puts |
|---|---|---|---|
| 0 | `python org/.../round30/checks/ac-2.AC1.py --before` must print `ACT-START GATE: OK` (it writes the S3 before-state) | 0 | 0 |
| 1 | `~85/scripts/ac2_probe.py`: `TokenFirstSessions.get("sa")` (the stored token, the NEWEST of `seeking-alpha/session` and `sa.dpapi`; never `refresh`), then `Publisher("sa", ...)` and `check_auth()` | **1** (`GET /api/v3/account/{user_id}/info`) | **0** |
| 2 | Only on an authorized 200: `Publisher.seeking_alpha(<Lenovo LNVGY>, limit)`, live mode, page 1 | **1** (`GET /api/v3/symbols/LNVGY/news?...`) plus its account pre-check (the client checks before a live page) | **0** |
| 3 | Write `~85/ac2_probe.json`; run AC1 and AC2 | 0 | 0 |

- **Egress:** at most 3 Seeking Alpha requests, through the collector's paced transport (15-25 s).
- **No S3 write:** no `run`, no upload, no run record.
- **Local writes:** the probe JSON, plus a kept refusal body if one occurs.

## VERDICT: SIGNED

- **Blast radius:** at most 3 requests to Seeking Alpha; 0 S3 objects.
- **Excluded:** NO sign-in and NO `refresh` (no Worker is constructed), NO other publisher.
- **Rollback:** none needed; nothing is written.

## 1. BEFORE -- measured at signing

- The sa root holds 106 objects, and the run-record root 14.
- AC1 FAILS if either changes.

## 2. EXPECTED OUTCOME, BOTH BRANCHES

**Branch A (account 200, authorized):**
- `Z-W37-S4` becomes CLEARED: the stored token reads the account.
- The listing page records its status, hits, dated hits and pre-floor hits. It is the first sa listing measured on the new code.

**Branch B (402, 401, a bot check, or an unauthorized 200):**
- The probe stops. The class is recorded, and the body is kept where the transport keeps one.
- A 402 means `Z-W37-S4` "402 PERSISTS", which is a finding. There is no sign-in; the session route is round 31's cloud
  collection.

Both branches pass AC2 when fully recorded.

## 3. ROLLBACK

Nothing to roll back: the act writes nothing to S3.
