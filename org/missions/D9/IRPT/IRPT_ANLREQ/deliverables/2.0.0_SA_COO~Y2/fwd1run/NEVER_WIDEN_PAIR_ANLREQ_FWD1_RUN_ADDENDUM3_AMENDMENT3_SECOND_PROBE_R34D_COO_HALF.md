# IRPT_ANLREQ FWD-1 run, ADDENDUM 3 AMENDMENT 3 -- a second probe set after the checker fix, the stored-object claim corrected to MEASURED, and R0e re-pinned to the resident r34d -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No run-3 order is lifted from HOLD until the CTO half of THIS amendment is signed on this file's blob, the CTO half of the r34d packet is signed, and AQ2's r34d install has closed with V2 inside the service's environment reading OK.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: addendum 3 (COO blob `64884b3338965c79a962c3f40cdb5cde44ad5811`, CTO half @bf5eb93047) section 3 (W8) and section 5 read R0e, as amended by amendment 1 (blob `7a4e8735155f871b8f8573d0d4d0f3cc63704bec`) and amendment 2 (blob `e9347582e07326f15f4dc0c099add09f198f78e9`). Nothing else changes: W7 (the driver, sha256 `455f6609...`, 67 selftest cases), the selection rule, the inputs the probe fixes, the address `fwd1-staff-r41b@opal.invalid`, the STOP conditions of the CTO's msg 9089, R0d (r35L), R0f (order amendment 1: the commentary function digest `I/6mirBTU5+JPCUUx6Xrmd1bn1vGAjvZTL75LhOm3HY=`).

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. What the first probe set showed (RECORD)

AQ2's step-0 probe (record `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/A_RUN_FWD1_R3.txt`, commit `51686af530`): ALPPL, APPL, BREIT, SREIT and ZQXWVK each answered `200 NEEDS_CORRECTION TICKER_CHECK_FAILED`, no suggestion, `REPLACE_FILE` only, two posts each; no U-row qualified; the run window stayed unspent (CTO msg 9282, order amendment 2 `d2f293eee5`).
Diagnosis (RELAYED, `2.0.0_SA_COO~G2` msg 9290; AQ2's read-only `TO-READ-CHECKFAIL`, proof VALID `4fc6914431`): a checker bug, not an environment fault: yfinance 1.2.0 raises `YFTickerMissingError` for a symbol it has no data for and the checker let it escape, so every symbol the check could not price read CHECK_FAILED. The fix (cell `AR-g-121`, merged `b535f41cb8`) maps ONLY that class and its subclasses to NOT_KEPT; every other exception stays CHECK_FAILED (the CTO's condition, msg 9291).

## 2. The claim corrected (what a person or a system meets)

Addendum 3 section 3 and amendment 2 carried "the probe stores nothing" as INFERRED. It is **MEASURED false**: the five probes grew the 49financial intake store from 301 to 306 versions, **one `original_holdings` CSV per candidate**, none deleted (AQ2's `OBJECTS_WRITTEN_FWD1_R3.txt`, `51686af530`). Those five, with the release-33 sitting's eight, are registered as Andrew's one-act delete, row `dell2-20261016T105058Z-dc59` (CTO msg 9288), after run 3 is graded and never by prefix. The sentence in addendum 3 section 3 "What the probe stores: nothing ... (INFERRED ...)" is replaced by: **each probe answer that asks for a correction stores one `original_holdings` CSV of the uploaded file; the applier lists the intake prefixes BEFORE and AFTER and every new object (or new VersionId of an existing key) by key and VersionId; none is deleted in the window.**

## 3. The change: a second probe set (W8, second set)

After the r34d install has closed with V2 in the service's environment reading OK (section 4), the window repeats step 0 ONCE with exactly the rules of addendum 3 section 3 as amended by amendment 2, with these differences only:
- **The same five candidates, in the same order:** `ALPPL`, `APPL`, `BREIT`, `SREIT`, `ZQXWVK`; the same synthetic one-row-plus-SPY CSV; the same re-post rule (one re-post of the same upload, only when the first answer is RESOLVING; at most two posts per candidate, ten in all).
- **A new probe viewer, because a name is never reused:** `irpt-r3q-iv-<YYYYMMDD>@opal.invalid`, minted exactly as the first (R28b amendment 1, COO blob `fe221dfcf1`; one RS256 token, exp at most 20 minutes, never written or logged), removed (ABSENT by the GSI and a ConsistentRead) before the run user is minted. R0b adds this address to the ABSENT reads; the first viewer `irpt-r3p-iv-20261016@opal.invalid` stays ABSENT (AQ2 removed it at 10:47:00Z).
- **The first set stays in the record as the failing set;** the second set's PROBE lines are written below it in `A_RUN_FWD1_R3.txt` marked `SET 2`. The selection rule applies to SET 2 only.
- **Objects:** the second set adds up to five more `original_holdings` objects (up to ten posts; identical content for a candidate may land as a new version of the same content-addressed key or as a new key: INFERRED, the applier lists whichever it is). The applier lists them by key and VersionId in `OBJECTS_WRITTEN_FWD1_R3.txt` under `SET 2`, and this seat updates the source record of the delete row `dc59` with them (the CTO's msg 9288).
- **What the second set should show (INFERRED, not a claim):** ZQXWVK reading `NOT_FOUND` with no suggestion and ALPPL/APPL reading `NOT_FOUND` with a Kimi suggestion where the door has one; any candidate that still reads `TICKER_CHECK_FAILED` does not qualify, and **if all five still read CHECK_FAILED the window STOPS before the run user is minted and nothing is run** (no B-only run).

## 4. R0e re-pinned to the resident r34d (replaces R0e of addendum 3 as amended by amendment 1)

R0e: the resident root is **`0485393f3a-r34d`**, installed from the r34d tar (sha256 **`9a088a5cfdeecd84173ee85b82d93ecf2b6fdfa311d3aec982e7db7134cf78ab`**, **1,120,240 bytes**, 314 members; package pin `11e0751415c1e811bffd0381d24a7c890ad1f33d`; RECORD, `NEVER_WIDEN_PACKET_RESIDENT_R34D_CHECKER_FIX_20261016.md`, COO half git blob **`60cf9b70bcf5cb159881d708db2001bd44c576a3`** at this writing, to be re-measured at the CTO's signing and equal to the CTO's re-signed binding), the applier's install record (ledger `irpt-resident-r34d-20261016`) reads V1 green AND **V2 inside the service's own environment reads OK** (`v2_service_env_r34d.sh`, sha256 `90802b18a174414353387c0595fc8beae414399d82042ec9ab973df699ab7940`; a V2 that ran in a shell does not count), the library delivery record reads CLOSED with `yfinance` importable by the resident's interpreter, `opal_pricing` false, the producer list `andrew@opalinvest.com` and `fwd1-staff-r41b@opal.invalid`, the r34c root kept on the host as the rollback. A record that names the r34c or earlier tar or root, any V2 other than OK, or a V1 that is not green, ABORTS.

## 5. Blast radius (the delta over addendum 3 section 4 and amendments 1 and 2)

1. Up to five more stored `original_holdings` objects, and ten more door posts by one more transient internal-viewer identity (a token, no password, at most 20 minutes) at the upload route only.
2. The resident changed by one member (`intake/yfinance_check.py`) against the r34c root; no new Yahoo call path (the checker already calls Yahoo for each symbol YCharts omits, bounded as r34c's packet states).
3. Nothing else: the run user, the driver's presses, the chain and the after-reads are as signed.

## 6. Limits named

NOT read: whether the r34d install and its V2-in-service have closed (gates, read at R0); whether the Kimi suggestion appears for any candidate (live, per probe); whether a repeated identical upload lands as a new version of an existing key or as a new key. The classifier is still not in the resident (CTO addendum 6).

## 7. Owed before the order is lifted from HOLD

1. The CTO half of the r34d packet (blob above) and of THIS amendment, on this file's blob.
2. AQ2's r34d install closed: ledger `irpt-resident-r34d-20261016` CLOSED with `V2S OK`.
3. This seat's amendment of the held order: lift the HOLD, add the second probe set and the new viewer, re-pin R0e, cite this blob. Cut only after (1) and (2).
