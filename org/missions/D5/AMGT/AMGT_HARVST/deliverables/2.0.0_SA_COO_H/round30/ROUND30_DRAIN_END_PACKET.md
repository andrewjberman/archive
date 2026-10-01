# AMGT_HARVST ROUND 30 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-30 ~19:3xZ

**Issuance:** `92ac03f4c8`, three orders over `ROUND_ANALYSIS.round29.md` @`d0bc0a79f0` (decomp section 43).
**L8-L10 route:** `3.0.0_SA_CVO~Z`.
**Class: WORLD** (`ac-3`'s served gold, and `ac-2`'s vendor egress) **plus LOCAL code.**

## 1. THREE ORDERS, ALL TERMINAL

| order | class | pair | drained | status |
|---|---|---|---|---|
| `ac-1` the `bot_check` class (v0.10/v0.11); A1 body-less is `unclassified`; A2 no `check_auth` after a bot check; A3 the q6 test log | LOCAL | -- | `f3980a84ab` | complete, VALID |
| `ac-2` the sa probe on resolved securities, outside the Worker | WORLD | `0ee2667f36` / `e5171bf838` | `499b93b258` | complete, VALID (`097858b1c2`) |
| `ac-3` the paired `chatter_daily` rebuild | WORLD | `f406a6106b` / `1f2edc7733` (+ the positive arm `c3f2f1cd1d`) | `8d25ddbdc3` | complete, VALID (`1dc2ffb4a5`) |

- **Close run** (`round30/close_run_round30.py`, at trunk `bc464ff375`): **7 of 7 re-runs rc 0**; 0 tracked files were rewritten.
- **The collector suite on the trunk:** 335 passed, 1 skipped (317 at `d0bc0a79f0`, 0 regressed).
  - The one base test whose expected log changed is `test_q6_barrons_guard_ft_body.py`, which dropped the forbidden re-check,
    by `ac-1` A3.

## 2. WHAT THE ROUND MEASURED OR BUILT (the CTO grades)

| FWD | this round |
|---|---|
| **2 / 3** | **The 2 in-window bbg story-id articles are on the PAGE** (`ac-3`). `part-20260930T181745Z` holds 52,143 rows, 49,679 B, digest equal to the serializing dry run. Of 539 moves, 53 are on the 5 expected rows (992_HK 08-13 and 09-01; AAPL, C, MU 08-13) and 486 are rolling consequences; OTHER is 0. The series carries `bbg` in `publishers_found_codes` on all 5 rows (in-process route read), and the day route lists the article with headline and `mention_count`. |
| **1 / 9** | **Seeking Alpha works on its stored token** (`ac-2`). The account read returned 200 authorized, so **`Z-W37-S4` is CLEARED**. One LNVGY news page returned 200 with 20 hits, 20 dated, 0 pre-floor (2026-01-13..09-15). That took 2 requests, 0 sign-ins and 0 S3 writes. **sa is the one publisher with a measured working REST path since batch 1.** |
| **7 / 1** | **`C-HV-TRUST-TOKEN` v0.10/v0.11 is in code** (`ac-1`). `bot_check.py` classes a refusal by the signature of its kept body. The kept batch-1 bodies read wsj `bot_check/datadome` and ft `bot_check/ft_security_verification`, DERIVED by the rule. A bot check or a body-less refusal is never expiry and never a sign-in, and it stops the leg. The repair-failed path now keeps its body. The listing path makes no `check_auth` re-check after a bot check. |

## 3. ROWS THIS ROUND

- **Worker rows:**
  - `Z-W84-S1`: accepted as built; repaired refusals stay `request_rejected`, carrying the class.
  - `Z-W84-S2`: ruled in as `ac-1` A2.
  - `Z-W84-S3` (BLOCKING): ruled as A3, a test update.
  - `Z-W85-S1`: `bot_check.py` was absent from `ac-2`'s pin (it merged later). Moot: both requests were 200.
  - `Z-W85-S2`: `sa_rest_fetch.check()` HARD-CODES the account id `1btfwdu`, where `contracts.json` names `{user_id}`. So
    "authorized" reads that account, whoever the token belongs to. **Carried to round 31** (the token store).
  - `Z-W85-S3`: a capped probe needs one-attempt policy plus a send counter, because `PacedSession.get` retries in-call.
- **Carried:** `Z-W37-S4` is CLEARED by measurement; its graduation is the CVO's.
- **Issuer defects, named:**
  - `ac-1` was issued with the analysis's "four kept bodies" premise corrected at the cut (2 exist).
  - `ac-2` was re-cut before its pair (AMENDMENT 1): a collector `run` would have contradicted the no-sign-in condition.
  - `ac-3`'s expected diff was widened by measurement to the co-mentions (the CTO agreed).
  - `ac-1` needed two post-report amendments, A2 and A3, for rows the worker surfaced.

## 4. FOR ROUND 31 (the CTO's list; input already ruled)

- **The CTO cloud ruling**, `CTO_RULING_CLOUD_COLLECTION_DESIGN_20260930.md` section 0 @`34a61b749e`:
  - cell 1, the token store into Secrets;
  - cell 4, the residential-IP assignability read.
- **Cell 2** (the warm-up and ramp) waits on `CRO~Z`'s trial 2. **Cell 3** is WITHDRAWN (`CRO~Z` ran it).
- **`Z-W85-S2`**, the hard-coded sa account id, belongs with cell 1.
- **sa storing collection on its working path** is now measurable, if the CTO lists it.

## 5. FOR L9

- All criteria are mechanical.
- The served artifact is `chatter_daily` `part-20260930T181745Z`.
- `ac-2`'s evidence is `~85/ac2_probe.json`.
- **Disposable worktrees:** `wk-hvst-r29-81..83` and `wk-hvst-r30-84..86`. Their removal needs Andrew's word.
