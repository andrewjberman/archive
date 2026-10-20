# ADDENDUM 6 to the never-widen packet for the synthetic commentary end-to-end run -- run 5 keeps the unknown row ZQXWVK by the door's Keep re-post, records the door's finding, and proves the kept row reaches C-SWAP as UNRESOLVED (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** the packet `NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_20261017.md` and its ADDENDUMS 1 to 5 (ADDENDUM 5 CTO half signed @9fc392ccd5). **Ledger:** `irpt-commentary-e2e-5-20261020`. **Authority:** CTO msg 11112 ("keep the bad row ZQXWVK; the script posts the Keep re-post (the equal pair) after NEEDS_CORRECTION; it records the response body's finding code and row, so a stop is diagnosable next time; proving the row reaches C-SWAP as UNRESOLVED is part of the pass; window after 07:00Z Tue and before 11:30Z") and PRD v0.15 item 3.

## 1. Why

Run 4 stopped at U: the resident resolved the upload READY (23:10:58Z) and the door answered `NEEDS_CORRECTION` (23:11:07Z) for the deliberate unknown ticker ZQXWVK; the run kept only the state word, and sent no Keep. IB2's read (`A_NEEDS_CORRECTION.txt`, commit `d93ffcc185`) shows the door's keep-as-typed change (AR-g-68: `KEPT_AS_TYPED` in `intake/portfolio.py`, `UNRESOLVED` in `ycharts/generate/normalized_input.py`) is LIVE in `irpt-ycharts-generate` (CodeSha256 `kxOEgpbspky1...`, modified 2026-10-16T02:39Z). The first post of an unknown ticker is answered NEEDS_CORRECTION by design; only the filer's Keep (a re-post carrying the equal pair) files it as UNRESOLVED.

## 2. The change to the pair (everything else in the packet and ADDENDUMS 1 to 5 stands)

| step | change |
|---|---|
| A, A2 | the synthetic staff user is `fwd1-commentary-e2e5-20261020@opal.invalid`; the advisor is minted with `fwd1_advisor.py mint --date 20261020` (address `irpt-w5-advisor-20261020@opal.invalid`); R0 reads the advisors of the dates `20261018`, `20261019` and `20261020` ABSENT first (Monday's `20261019` is never touched) |
| R0 | the holdings bytes are the window-5 five-row file with the `Dollars` of `SPY` set to `102` (distinct from runs 1 to 4: `100`, `100`, `100`, `101`); its sha256 is printed and compared with every earlier receipt's; the upload token is FRESH (ADDENDUM 3); the resident root must read `0485393f3a-r34l` (ADDENDUM 5) |
| U | the five-post ladder of ADDENDUM 4 stands for the FIRST post. When the answer is `NEEDS_CORRECTION`: (a) RECORD, as closed words only, the answer's `state` and, for every finding, its `finding_code`, its row number and its symbol (the synthetic tickers SPY, AGG, TIMXX, APPL, ZQXWVK only) and whether a `suggestion` member is present; (b) if and only if the findings are exactly ONE, `TICKER_NOT_FOUND` for the symbol `ZQXWVK`, re-post the SAME upload (same `upload_token`, same file bytes, same `advisor_email`) with ONE added member `corrections: [{"finding_code": "TICKER_NOT_FOUND", "from_value": "ZQXWVK", "to_value": "ZQXWVK"}]` (an equal pair, the exact same characters; the portal's `correctionsFor` builds the same), ONCE, under the same backoff ladder if that post answers `RESOLVING`; (c) any other finding (another code, another symbol, a different count) or any other answer is a STOP at U naming the findings, and the Keep is NOT sent. The first `NORMALIZED` answer (after the Keep) gives the upload id and the input_id and the run goes on. No second Keep, no other correction, no new token, no new file |
| P6 (new, after P5) | read-only proof that the kept row reached C-SWAP: (a) the request's frozen holdings document: the row for `ZQXWVK` carries `resolution` `UNRESOLVED` and `method` `KEPT_AS_TYPED` (read in the request's retained input record or the job's frozen composition: names and the two closed values only, no amount); (b) the swap pass's record for this request: whether it names `ZQXWVK` as `REPLACED` (with the replacement ticker, a catalogue ticker) or as not analysed (the fixed sentence `ZQXWVK is not analysed; Opal Staff will manage the replacement.`), read from the report's retained `run.json` or the request's disclosures (names and the closed sentence only, never an amount). IB2 finds the location from the artifact index items it already reads at P3 to P5 and says where; `NOT-FOUND` is written when it cannot, with the places looked in |
| D | unchanged (ADDENDUM 4); the receipt's `D` line also lists the Keep post's UTC time |
| Receipt | the lines are those of ADDENDUM 5 plus `P6 swap <row=UNRESOLVED/KEPT_AS_TYPED swap=<REPLACED:<ticker>|NOT_ANALYSED|NOT-FOUND>|NOT-RUN <hop>>` (19 lines), and the `U` line reads `U upload <ok tries=N keep=<sent|not-needed> elapsed=Ss|REFUSED code findings=...|STOP ...>` |

PASS for this addendum's proof: the Keep is sent exactly once after exactly the one expected finding, the next answer is NORMALIZED, the job reads READY, and P6 prints `row=UNRESOLVED/KEPT_AS_TYPED` with a swap outcome other than `NOT-FOUND`.

## 3. Blast radius delta

One more post of the SAME upload (a re-post carrying the equal-pair correction; the door creates no second object: `intake/uploads.py` re-posts of one token), and one more synthetic advisor date. No new write path; reads only at P6.

## 4. Not claimed

- That the swap pool holds a replacement for ZQXWVK (either swap outcome passes; `NOT-FOUND` does not).
- That the commentary route is readable for an advisor-owned request by the staff user (ADDENDUM 1 section 4); a refused R or R2 is recorded, never a rollback trigger.

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 to 5. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
