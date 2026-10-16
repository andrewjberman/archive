# IRPT_ANLREQ FWD-1 run, ADDENDUM 5 AMENDMENT 1 -- the synthetic advisor helper re-pinned (display name SYNTHETIC TEST ADVISOR) and the CTO's three signature conditions written in -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. The window-5 order is HELD until the CTO half of THIS amendment is signed on this file's blob AND the CTO hands over the 5174 server.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: addendum 5 (COO blob `4a24c2443c76ce74c3c61ae1b0e11b583db287e9`, CTO half signed @02306c830e, msg 10001) section 2.3 (the advisor helper) and section 3 (the start gate). **Only those change.** Everything else of addendum 5 stands as signed.

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; NOT READ = nothing read tells it.

## 1. The helper re-pinned (replaces the advisor helper's pin in addendum 5 section 2.3)

`fwd1_advisor.py` sha256 **`3860d6396db7b0c94c4052268a14489869a80e52cbaeeba49bbffeb6a25f45b6`** (12,140 bytes; MEASURED by this seat on the merged file, merge `bf63cc157d`; cell AR-y-381, worker 173; 19 offline tests, `ADVISOR-TESTS-OK 19`, `NAME-OK`, `MUTANT-FIRES`), path `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~172/fwd1_advisor.py`. It differs from the pin of addendum 5 (`cc8b8bd5f120f3e54bb73b9c82d97ba390207a65e95e769ddf1a2e1706906a34`) by two lines: the display name constant is now exactly **`SYNTHETIC TEST ADVISOR`**, written to the users row `name` and the partner row `advisorName` (the CTO's condition (2), msg 10001). The address `irpt-w5-advisor-<date>@opal.invalid`, the attribute sets, the conditions and the removal are unchanged (`name_check.py`: 19 of 19 other attributes equal the merged version). The old pin is void: a helper whose sha256 is not the one above ABORTS the order.

## 2. The CTO's three conditions, written into the start gate (addendum 5 section 3)

1. **One 5174 checkout** at DEV `4d4dc68cae` or past it, named by the CTO after Andrew's smoke, serves TCKT R20-RV first and then this window; the order reads the served checkout's HEAD and its ancestors as addendum 5 section 2.1 says, and never stops or restarts the server.
2. **The display name** reads `SYNTHETIC TEST ADVISOR` (section 1). **Timing:** the window runs OUTSIDE 13:00Z to 22:00Z on a weekday (the order prints the UTC clock and the weekday before the mint and STOPS inside that band), because a 49financial partner-facing list could show the partner row.
3. **The R20-RV and R20-REL ledgers are CLOSED before the first post** (the order reads both `Status` lines at R0; an open one is a STOP). NO RETRY.
4. **The YCharts door:** IB2's recipe-form read has reported (msg 10022: `YCP2 RESULT form=NONE`, last call 23:27:56Z, free from 23:34:26Z; the price tier stays unused in window 5, CTO msg 9991). No YCharts call by any seat between R0 and the run; the first post waits at least 390 s after the last YCharts call in the resident journal (read, not asked).

## 3. Blast radius and limits

No change to the blast radius of addendum 5 section 4: the advisor rows are still `@opal.invalid`, credential-free, 3 hours, removed in the window; only their display name changed. NOT read: any live mint of the renamed helper; the 5174 hand-over; the R20-RV and R20-REL ledger states at the time of the order.

## 4. Owed before the order runs

1. The CTO half of THIS amendment, on this file's blob.
2. The 5174 hand-over (the CTO names the checkout); the R20-RV and R20-REL ledgers closed; the weekday-band rule satisfied by the clock at R0.
3. The window-5 order to `0.7.0_AE_CloudOps~IB2` is cut HELD now (citing addendum 5 and this amendment's blob) and lifted by this seat's `lift HOLD` commit when (1) and (2) hold.
