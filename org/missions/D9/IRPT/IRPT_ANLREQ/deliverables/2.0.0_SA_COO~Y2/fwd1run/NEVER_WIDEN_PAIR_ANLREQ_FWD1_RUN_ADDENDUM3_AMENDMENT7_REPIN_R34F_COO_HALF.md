# IRPT_ANLREQ FWD-1 run, ADDENDUM 3 AMENDMENT 7 -- R0e re-pinned from the resident r34e to the resident r34f (the resolve hop's WAF back-off), and the run goes on SET 3's selection with no further probe -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No run-3 order is lifted from HOLD until the CTO half of THIS amendment is signed on this file's blob and the ledger `irpt-resident-r34f-20261016` reads CLOSED with the V2S lines of section 2.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Amends: addendum 3 (COO blob `64884b3338965c79a962c3f40cdb5cde44ad5811`) section 5 read R0e, as re-pinned by amendment 4 (blob `a560bc08075380f7b0137015e3fb2ef9e935dcb8`), and the probe of section 3 as amended by amendment 6 (blob `53decf2ba991ee9e258650ca62968bf2040d6b88`). Everything else stands as signed: R0d (r35L), R0f, the inputs, the driver, the CTO's stops of msgs 9337, 9446 and 9450, W7.

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. Why R0e moves (RECORD)

SET 2 and SET 3 each lost one candidate to a YCharts WAF challenge on the FIFTH lookup of a series (SET 2 ZQXWVK; SET 3 SREIT, 3 `WAF_CHALLENGE` lines then `RESOLVE_RETRY_EXHAUSTED`; AQ2 msgs 9393 and 9465). The resolve hop retried a challenge at a flat 60 s and ended the row at about 3 minutes. Cell `AR-g-129` (merged `53c40793dd`) backs the retry off 150, 300, 450 s (15 minutes in all), a 503 at 60 s, and names the class in the journal. The r34f resident carries it: packet `NEVER_WIDEN_PACKET_RESIDENT_R34F_WAF_BACKOFF_20261016.md`, COO blob `e9ede8d67f4e24aefd53d18329de7a2e462ef101` (MEASURED by this seat at this writing), CTO half signed @57f0938a30 (msg 9572).

## 2. R0e re-pinned (replaces R0e of addendum 3 as re-pinned by amendment 4)

R0e: the resident root is **`0485393f3a-r34f`**, installed from the r34f tar `irpt-resident-0485393f3a-r34f.tar.gz` (sha256 **`0d223e500a92aa274bbb52437d33657dd870b9f29af41ec942463c936d904a3f`**, **1,121,542 bytes**, 314 members, 311 identical to r34e; package pin `a81abf691f3af84fdde5ee1cf2c0dafc2b2966ed`; RELAYED by the packet and the CTO's msg 9572); the applier's install record (ledger `irpt-resident-r34f-20261016`, applied by `0.7.0_AE_CloudOps~IB2` under rule 34) reads CLOSED, V1 green, and from `v2_service_env_r34f.sh` (sha256 `125677f454cad5cbd3f9def46c48fc7be685c234d14a84ea92d205762bb21f99`) run INSIDE the service's own environment, as root: **`V2S OK`**, **`V2S CONTROLS OK 4 of 4`** (r34e's four controls kept) and a **`V2S BACKOFF`** line that reads the shipped schedule (the WAF code at receives 1, 2, 3 = 150, 300, 450 s; a 503 = 60 s; the module file under the new root). A record naming the r34e or earlier tar or root as the running one, any V2S other than these, or a V1 that is not green, ABORTS. The library delivery record reads CLOSED; `opal_pricing` false (r34f does not move it); the producer list `andrew@opalinvest.com` and `fwd1-staff-r41b@opal.invalid`; the r34e root kept as the rollback.

## 3. The probe: NO further set; the run goes on SET 3's selection (this seat's proposal; the CTO may rule otherwise)

SET 3 (RECORD, `A_RUN_FWD1_R3.txt` SET 3 lines, AQ2 msgs 9465 and 9471) gave by the selection rule **U1 = ALPPL** (suggestion AAPL), **U2 = APPL** (suggestion AAPL), **U3 = ZQXWVK** (NOT_FOUND, no suggestion; BREIT also qualified and stays unused). Proposal: the window does not repeat step 0. Reasons: (a) r34f changes one member, the resolve hop's retry spacing; the checker, the advisory and the door's answers for these four candidates are the r34e bytes already measured; (b) the YCharts lookups a probe would make (up to ten) spend the same rate budget the run's own uploads then need, and both lost candidates were the fifth lookup of a series; (c) a probe stores up to five more `original_holdings` objects for no new information. The run's decisions file is built from SET 3's selection; step 6 is unchanged. If the CTO rules a SET 4 is wanted first, it takes amendment 6's text with a new viewer name and the order's next amendment, and this section is void.

## 4. Blast radius and limits

Nothing is added to what the window moves (amendment 6 section 3 stands; with no probe, up to five FEWER stored objects). NOT read: whether the r34f install and its V2S have closed (gate, read at R0); whether the back-off clears a challenge that persists past 15 minutes; **the run's own uploads still meet the YCharts lookup, and a challenge that outlasts the back-off would end that row and spend the single no-retry window** (PRD v0.22's yfinance-first release, `~G2`, is the change that removes the lookup for Yahoo-priced symbols and is NOT in r34f).

## 5. Owed before the order is lifted from HOLD

1. The CTO half of THIS amendment, on this file's blob.
2. IB2's r34f install closed: ledger `irpt-resident-r34f-20261016` CLOSED with the V2S lines of section 2; this seat reads the ledger and IB2's record.
3. This seat's order amendment 8 (replace step 5 by the SET 3 selection if section 3 is signed; re-pin R0e; cite this blob) and a `lift HOLD` commit. Cut only after (1) and (2).
