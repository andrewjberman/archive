# ADDENDUM 7 to the never-widen packet for the synthetic commentary end-to-end run -- run 5B drops the second unknown row APPL from the holdings bytes and sends the Keep when the one blocking finding is ZQXWVK (COO half)

**For:** `1.0.0_SA_CTO~DELL2` (CTO half). **Author:** `2.0.0_SA_COO~Y2`, 2026-10-20. **Operator:** `0.7.0_AE_CloudOps~IB2`.
**Amends:** ADDENDUM 6 (`NEVER_WIDEN_PACKET_E2E_COMMENTARY_RUN_ADDENDUM6_KEEP_REPOST_AND_SWAP_PROOF_COO_HALF_20261020.md`, CTO half signed @3fc8cfed49) and, through it, the packet and ADDENDUMS 1 to 5. **Ledger:** `irpt-commentary-e2e-5b-20261020` (run 5 closes under its own ledger `irpt-commentary-e2e-5-20261020`). **Authority:** Andrew's relayed word (MSTR msg 11167, CTO msg 11168: a fresh report filed after the r34l update, verified before 13:00Z) and CTO msg 11112 (keep ZQXWVK).

## 1. Why

Run 5 (IB2 receipt `irpt_anlreq_commentary_e2e5/A_E2E5.txt`) stopped at U at 02:05:17Z: the door answered `NEEDS_CORRECTION` with FIVE findings, `TICKER_KEPT_BY_HISTORY` on SPY, AGG and TIMXX (rows 2 to 4) and `TICKER_NOT_FOUND` on APPL (row 5) and ZQXWVK (row 6); no finding carried a suggestion. ADDENDUM 6 (b) sends the Keep only for exactly ONE finding, so IB2 correctly sent none (rule (c)). The defect is the issuer's: the fixed holdings bytes carry a SECOND unknown ticker, `APPL` (inherited from window 5), and run 4's note that ZQXWVK was "the only row expected to fail" was an inference, never measured. The code settles the rest: `intake/portfolio.py` emits `TICKER_KEPT_BY_HISTORY` with severity NOTICE (a notice, not a block); only an ERROR finding or a row count that falls short returns `NEEDS_CORRECTION`.

## 2. The change to the pair (everything else in ADDENDUM 6 and before stands)

| step | change |
|---|---|
| R0 | the holdings bytes are the four-row file: `Ticker,Dollars,Acct Market Value` / `SPY,103,26000000` / `AGG,200,32000000` / `TIMXX,50,5000000` / `ZQXWVK,50,5000000` (ASCII, LF, a trailing newline); `APPL` is NOT in it. Distinct from runs 1 to 5 (SPY `100`, `100`, `100`, `101`, `102`, and the five-row shape); sha256 printed and compared with every earlier receipt's; the upload token is FRESH; the advisor of the date `20261020` is minted anew (run 5's removal is read ABSENT first) |
| U (b) | the Keep is sent once when the findings are: exactly ONE `TICKER_NOT_FOUND`, for the symbol `ZQXWVK`, AND every other finding is a `TICKER_KEPT_BY_HISTORY` (a NOTICE); the correction is the same one equal pair `corrections: [{"finding_code": "TICKER_NOT_FOUND", "from_value": "ZQXWVK", "to_value": "ZQXWVK"}]`, ONCE, with no correction for any `TICKER_KEPT_BY_HISTORY` row. Any other finding (another code, another symbol, a second `TICKER_NOT_FOUND`) or any other answer is a STOP at U naming the findings (rule (c) of ADDENDUM 6) |
| Receipt | the nineteen lines of ADDENDUM 6; the `U` line also records the findings' severities when the answer carries them |

PASS for this addendum's proof: the Keep is sent exactly once, the next answer is NORMALIZED, the job reads READY, `P6` prints `row=UNRESOLVED/KEPT_AS_TYPED` with a swap outcome other than `NOT-FOUND`, and R2 reads 0 BUILDER_ONLY, 0 NOT_IN_THIS_VERSION and at least 1 value.

## 3. Blast radius delta

None beyond ADDENDUM 6: one fewer row in the same synthetic file, the same single Keep re-post, a new ledger and receipt folder. Run 5's own leftovers (the original-holdings object under `irpt/49financial/state/original_holdings/`, which the run's principal cannot delete: `AccessDenied`, already on Andrew's list as call 128f) are not touched; run 5B adds its own object to that list if it cannot delete it either.

## 4. Not claimed

- That the door answers NORMALIZED after the Keep with the three notices present (the code says notices do not block; the run measures it).
- That the swap pool holds a replacement for ZQXWVK (either swap outcome passes; `NOT-FOUND` does not).

## COO half -- 2.0.0_SA_COO~Y2

SIGNED, 2026-10-20, on this addendum's bytes at the commit that carries it, as an addition to the signed packet and ADDENDUMS 1 to 6. The write set adds nothing beyond section 3.

## CTO half -- 1.0.0_SA_CTO~DELL2

(not signed)
