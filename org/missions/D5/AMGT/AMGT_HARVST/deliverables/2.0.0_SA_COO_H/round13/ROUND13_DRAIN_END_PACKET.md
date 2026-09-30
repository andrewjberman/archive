# AMGT_HARVST ROUND 13 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~06:4xZ

**Issuance:** `8dbea345c9` (two orders over `ROUND_ANALYSIS.round12.md` @`094cc1f110`; decomp section 25).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Close run:** `round13/CLOSE_RUN_ROUND13_TRACE.txt` (deployed plane, OK).

## 1. TWO ORDERS, TWO TERMINAL, TWO VALID

| order | seat | class | merges | result |
|---|---|---|---|---|
| `b-1` an event is one story | `~39` | LOCAL | `89674edbe5`, REOPENED `debe403b24`, `6a91a6efb1` | calendar words never link; per-story qualification; story-carrying ids; STOP limb 6/6; AC4 (added by AMENDMENT 1) 7 of 7 kept leads unchanged |
| `b-2` the served rebuild | `~39` | SERVED | `99e40301df` | ONE put `date=2026-09-29/part-20260929T062617Z` (ETag `391cfd4b...`); 8 -> 7 events; 5 prior parts intact (issuer re-read) |

## 2. THE OUTCOME, ON THE DEPLOYED PLANE

The deployed timeline (function `CtIvirv...`) now serves the one-story part: Boeing shows ONE event (09-08, led by
"Boeing Delivers 51 Jets in August, Lowest in Four Months", 2 articles); BA 08-26 is gone (two unrelated one-article
stories, neither qualifying); Lenovo's three events and NVDA 06-01 are unchanged in span and lead. Every `event_id` moved,
as the addendum requires.

## 3. THE REOPEN -- a served regression caught before it shipped (row `Z-S40`)

`b-1` passed AC1-AC3 and drained. **Before signing `b-2`'s pair, the issuer rebuilt in memory at the merged rule and
compared every lead to the served one**: BA 09-08 would have reverted to the runway headline -- the lead the round-12 L9
graded wrong -- because the runway headline over-merged into the deliveries story on "jet". The STOP limb guarded six
events' membership, not the leads the last round graded; **that criterion gap was the issuer's.** `b-1` was reopened with
AC4 (no kept lead regresses), the worker fixed the over-merge, and the served rebuild proves it: 7 of 7 kept leads
unchanged on the deployed plane.

## 4. JUDGMENT FOR L9 (presented, not graded)

`b-2` AC4: every served event with its lead, tier-A publishers and every headline; every prior event's articles traced
(5 kept whole, 2 kept with articles left, BA 08-26 with both left). **The question: is each served event ONE story about
its own company, and does its lead name it?**

**Read beside it -- the rule is FITTED, and both halves say so:** three generations of tuning against the same 8 events
(round 12's link threshold; round 13's token floor, earnings-word table and name-detection day floor; AMENDMENT 1's
tight-cluster refusal, 6-character stems and a class exemption added so HD 08-18 survives). No instrument this round can
say how the rule behaves on a security it has never seen. **The CTO adopted a held-out read as owed at the round-13
analysis** (CTO half @`78d6115535`).

## 5. ROWS -- the gate's own fold: 91 ids, GRADUATED 55, DISMISSED_WITH_REASON 25, UNDER_INVESTIGATION 11 (25 files)

Remedy EXERCISED this round: `Z-S40` (the lead regression; AC4 + the served rebuild). Disarmed by specification:
`Z-W39-S1` (the unwired event route recomputes the old 3-argument id; it must key by the stored `event_id` before any cell
wires it -- COO half s.6.3). Open with a named owner: `Z-S37` (the `safe-merge` staging window; round 13 added a SECOND
instance on the one-shot path -- the CTO's tick16 log swept into `6a91a6efb1` between the grade and the commit; tool fix
proposed to the script's authoring lane), `Z-W37-S4` (the Seeking Alpha 402; the account holder). INERT or informational:
`Z-W34-S1`, `Z-W35-S2`, `Z-W36-S1`, `Z-W37-S1`, `-S2`, `-S5`, `Z-W39-S2`. **Armed rows with an owner this seat could not
seat: NONE.**

## 6. WHAT I GOT WRONG THIS ROUND

1. **The STOP limb's population.** I guarded membership of the six events L9 graded as one company event, and did not
   guard the LEADS L9 graded right. The regression was caught by my own pre-signing read, not by a criterion.
2. **I blocked the shared index for ~20 minutes** (04:53-05:12Z): the row gate refused my reopen commit on a typed-in
   timestamp (`04:5xZ`), the order file stayed staged, and my retry loop waited on an index it was itself dirtying.
   `2.0.0_SA_COO~D` flagged it; unstaged; every later commit loop unstages its own paths on any refusal.
3. **My first `b-1` drain attempt left its files dirty in the working tree**, which then refused the next merge; all 9
   were byte-identical to the branch and were restored to HEAD before re-merging.

## 7. FOR THE ROUND-14 CUT (the CTO decides)

1. The held-out read of the story rule (adopted as owed).
2. The event route, if wanted: key by the stored `event_id` (`Z-W39-S1`).
3. Unchanged from round 12: the portal panel's DEV push (Andrew's hold); the Seeking Alpha 402 (the account holder);
   bbg (one further diagnostic call needs its own word).

## 8. WHAT THIS PACKET DOES NOT DO

It grades no judgment, claims no FWD REALIZED, pushes nothing (every commit is LOCAL), and cuts no round-14 cell.
