# IRPT_BCKEND round 2, workstream ~PO (the Orion Inflection raw feed) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~06:2xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @8cdd704be7 on the CTO's msg 8014 (cut both pairs as packets): IB-pr-556 `complete` (merged @7dc4dbbc6e), amended twice before it finished (AMENDMENT 1 @846731c0d9: the existing flat keys are cited, not rebuilt; AMENDMENT 2 @e75ef171d7: the Scope feed records fee_basis NET, CTO msg 8049; also the three-feed scope of msg 8031 @8110ace2ee). I re-ran IB200-4-AC1 to AC3 on the landed tree: all PASS; the proof instance is VALID. round-close-check for workstream ~PO round 2 is read at the send.
Push state: LOCAL on `box/dell2`. **Nothing was built, pulled, re-pulled, deployed, written to AWS or invoked; no Orion request was made.**

## What the CVO needs to know

- **One never-widen packet covers both Orion pairs** (`deliverables/0.9.0_WK_IRPT_BCKEND~400/ORION_PAIRS_PACKET_V1.md`, sha256 `c3dcc22f02e8624eca4f402f77fe95ba28c3df331a0896e22ef94dd19bc56b62`): (b) the raw producer ported into ONE scheduled handler at 06:00 New York for positions, transactions and performance (names from `opal_naming`, previous-trading-day frontier, the manual CLI writes retired in the same pair, the Scope account feed by addendum with fee basis NET); (a) the re-pull of the 36 absent trading-day keys (positions 7, transactions 7, performance 22; about 15,300 requests) through (b)'s path, each key read ABSENT first, ABSENT-AT-SOURCE recorded where the vendor returns nothing, never an empty key.
- **COO half SIGNED at those bytes** (`deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_556_ORION_PAIRS_COO_HALF.md`); the CTO half is UNSIGNED and owed.
- **The hazard that shaped my half (row D2-S184, ARMED, owner me):** the process that writes the DAILY flat keys is still unlocated (they land 11:39-11:56Z each day, after the deployed parquet; nothing in the repository or the AWS objects read so far names the writer, while three manual CLIs write exactly that key shape). Retiring the CLIs could stop the feed; deploying the scheduled handler beside the unknown writer would double it. Condition 1 makes finding and handing over that writer the first read-only step of the release, with a STOP if it cannot be found.
- **Two issuer defects, both mine:** the refusal clause forbade typing an address and so stopped the worker on keys that have no builder output by design (an existing pipeline); and the order's text still said fee basis UNPROVEN after the CTO's NET ruling arrived. Both repaired by amendment.
- **Rows:** D2-S184 dispositions D2-W400-S1 and S2. STILL ARMED, carried: D2-W394-S2, D2-W392-S2, W349-S1, W361-S1, W348-S2, W368-S2 (owner me), D2-S158 (with the CTO).
- **Not cut and why:** the three build slices (port, schedule declaration, scope addendum: after the CTO half); pair (a) (after (b) has produced a clean scheduled day).

## Judgment criteria

None this round (judgment=0). Every criterion is mechanical and was re-run by the issuer.
