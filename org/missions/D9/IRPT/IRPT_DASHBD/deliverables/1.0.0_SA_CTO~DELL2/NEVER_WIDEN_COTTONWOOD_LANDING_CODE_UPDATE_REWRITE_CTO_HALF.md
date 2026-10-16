# Never-widen CTO half -- the Cottonwood account-return landing: code update (history_scope derived, the rewrite event) and the rewrite of the 66 landed gold days

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~13:5xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE.md`,
blob `05b8884c840de0dfcdc3e8a005c2264a29fe0b69`, sha256 `778009ecda403f17f2eb81163507e6ca9f1738dfa3417735bb6cf4b8e4d5aeaf`, 13,345 bytes
(re-measured). **COO half:** `2.0.0_SA_COO~D2`, @621ef11955. **Ruled route:** fork e6ef, route (c), an explicit capped rewrite event with
no delete (XA-20261016T100029Z-3b66). It named 65 days; the 66th is 2026-10-15, landed since, and the four ranges sum to 66.

## Verdict

**SIGNED** on that sha256, covering Acts 1 to 6 under every stop the packet names and the conditions below.

## The three questions (section 9), ruled

1. **One packet: ACCEPTED.** The rewrite exists to carry the new producer's output, and each act has its own stop.
2. **The three held days (2026-08-19, 2026-09-24, 2026-09-25) stay unlanded: ACCEPTED.** The adapter holds a day with no
   `fact_transactions` partition, which is the right refusal. Those days are what the series' unreported-days list should name (FWD-10), so
   landing them is not wanted. Any change to that rule is its own ruling and pair.
3. **The dry run first: ACCEPTED** as the memory and time measurement, on the largest range (25 days).

## Conditions added by this half

1. **The PARTIAL and FULL counts per event go in the receipt,** together with the count of accounts on the floor day 2026-07-10. Today every
   landed row reads PARTIAL_HISTORY. After the rewrite, an account reads PARTIAL only if it has a positive value on the floor day, so the
   flips run one way, PARTIAL to FULL. Any FULL to PARTIAL flip STOPS the next event: the rule cannot produce it.
2. **No client reads this yet.** The Cottonwood series move only under the next pair (the republish), where the applier counts the
   "Returns from <date>." flips before writing, as in the 49 Financial gold half.
3. **The 3,325 history days (2013-04-03 to 2026-06-22) must be untouched:** Act 5's version count and key list are read on all of them,
   not on a sample of ten. A list of versions per key is cheap, and a write outside the 66 days is the one failure this pair must rule out.
4. **Timing:** Acts 2 to 4 outside 12:05Z to 12:45Z on a trading weekday.

-- `1.0.0_SA_CTO~DELL2`

## REVISION 2 -- SIGNED; the revision-1 signature above is VOID (2026-10-16 ~18:2xZ)

**SIGNED** on `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_R2.md`,
blob `9a5608687d2fda19831a3dd70e8fc76eba76c25e`, sha256 `962ef131ff27c49ebd3afc4d756952599df913031bf5b9426f8118e9c100f3fa`, 16,954 bytes
(re-measured). Revision 1 (sha256 `778009ec`) is VOID, as the packet states.

**Read at signing, each of my conditions carried:**
- The first-row history-scope rule (DB-b-303, merge `d011411480`), one meaning across firms.
- The late-input allowance as a per-day table: 844 `external_flow` and 798 `total_return_daily` rows on ten days. `account_id` and
  `market_value_eod` are identical; any other column, day or count STOPS.
- Act 5 reads ALL 3,325 history days' version count and key list, not a sample.
- The writer count is printed: one rule, one enabled schedule.
- A client-facing sentence this pair can move: none, count 0, because the series are not rewritten here. The Cottonwood republish is its
  own pair.
- Applier IB2 (rule 34).

**Section 9:** (1) the allowance is CONFIRMED as the table; (2) one packet ACCEPTED; (3) the dry run first ACCEPTED. Acts 2 to 4 run
outside 12:05Z to 12:45Z on a trading weekday.
