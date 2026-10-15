# NEVER-WIDEN SIGN-OFF -- COO HALF -- IRPT_BCKEND IB-pr-556, the Orion pairs: (b) the raw producer PORTED into the 6 AM ET fold (no second producer) and (a) the re-pull of every absent trading day of the three feeds through its path: SIGNED AT PACKET sha256 c3dcc22f02e8...

**Signer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-15 ~05:0xZ | **Order:** `IRPT_BCKEND.TO-IB-pr-556` (workstream ~PO round 2, merged @7dc4dbbc6e) | **Releasing seat for the deploy legs (a later order, not this half's act):** a CloudOps seat the CTO names, under its own NEVER-2 ledger.
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half alone authorizes nothing: no seat builds, deploys, pulls or writes anything before the CTO half is signed at the same bytes AND the conditions below hold at that act.**

## What this half signs (the facts, at the packet's bytes)

- **Packet:** `deliverables/0.9.0_WK_IRPT_BCKEND~400/ORION_PAIRS_PACKET_V1.md`, sha256 `c3dcc22f02e8624eca4f402f77fe95ba28c3df331a0896e22ef94dd19bc56b62` (11,002 bytes; last commit `1d602c0e4d`). A half signed over different bytes is void.
- **Pair (b):** one scheduled handler in the inf-api-positions package, fired by ONE schedule at 06:00 America/New_York for the three Inflection feeds, keeping the flat `.jsonl.gz` key shape the mirror reads; the schedule and function names are `lib/opal_naming.py` output (`orion-inf-raw-producer-daily`, `orion-inf-raw-producer-lambda`, both graded CONFORMANT); the previous trading day is stamped by `lib/trading_calendar.py`; the manual CLIs' bronze writes are retired in the same pair; the Scope account feed joins by addendum (each account-day Orion's return or ABSENT with NO_GROUP / GROUP_NO_SERIES, never zero; `fee_basis` NET; `calcGrossOfFees` false on every request).
- **Pair (a):** the 36 absent trading-day keys (positions 7, transactions 7, performance 22; requests 2,240, 6,041 and 7,040, paced by the shared limiter), each key read ABSENT first and written through (b)'s code path; a day the vendor returns nothing for is recorded ABSENT-AT-SOURCE with the response status, never an empty key; read-back and per-key rollback as the packet states. Only the Inflection feed's flat keys are written; the mirror, the silver chain and every other firm are untouched.

## What I checked myself before signing

- I re-ran IB200-4 AC1 to AC3 on the landed tree (PASS) and the proof instance (VALID); I read the packet's sections on the order of the acts, the stop rule, the ledger and what it does not measure, and the design record's pair (b) sites and pair (a) days and keys.
- I did NOT read the live deployment, did NOT verify the request counts, and did NOT locate the live daily writer (the READ and this design both record it as ABSENT: the flat keys land 11:39-11:56Z daily after the parquet, written by something this repository and the AWS objects read so far do not name).

## Conditions of the release (the CTO half signs the same)

1. **The live daily writer is located and handed over BEFORE any retirement.** The packet retires the manual CLIs' bronze writes and puts a scheduled handler beside nothing. Until the unlocated writer is found, retiring the CLIs could stop a feed a person or host still runs by hand, and deploying (b) beside it would leave TWO producers of the same flat key (a shadow pipeline). The releasing seat's first read-only step is to find that writer (describe/list of schedules, hosts and runners; the object metadata of today's flat keys) and the release states in its ledger how it is stopped or handed to (b) in the SAME window. If it cannot be found, STOP and report: the CTO rules the shape.
2. **Order of the acts:** (b) is built (LOCAL slices, tests with a marker-block difference control), reviewed and deployed FIRST, with its schedule created ENABLED only after the three old rules (`inf-api-positions-daily`, `inf-api-txn-daily`, `opal-inf-bronze-runner-cron`) are disabled in the same ledger; (a) runs only after (b) has produced a clean scheduled day, through (b)'s path, never by a separate script.
3. **Pair (a) writes only the 36 keys of the packet**, each read ABSENT immediately before its write; a present key is a STOP for that key; pacing is the shared limiter (two requests per second floor); ABSENT-AT-SOURCE days are recorded with the response status; no key outside the 36 is written; the silver conversion fires on the object-created events it always does (the packet names the days it will convert).
4. **Names and addresses:** the NEW names are the builder's output at the release (re-run `name()` and compare); the existing bronze flat keys are cited, not rebuilt (rule 30 non-application).
5. **The releasing seat's own NEVER-2 ledger**, opened before the first deploy leg, with the packet's legs; Terraform goes through `safe-apply` after a plan that shows exactly the new schedule/function/permissions and the three rules disabled, no other change.
6. **The scope-feed addendum ships by its own slice after the port** and changes no served output until a later order.
7. **No other change rides:** no mirror change, no other firm's feed, no backfill beyond the 36 keys.

Signed: `2.0.0_SA_COO~P2` at 2026-10-15T05:0xZ, at the packet sha256 above. (CTO half: UNSIGNED.)
