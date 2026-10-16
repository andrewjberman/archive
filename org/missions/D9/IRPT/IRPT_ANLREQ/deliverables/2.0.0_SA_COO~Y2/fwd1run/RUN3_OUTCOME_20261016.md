# IRPT_ANLREQ FWD-1 run 3 (window 3): outcome, issuer 2.0.0_SA_COO~Y2, 2026-10-16 ~17:15Z

Claim words: MEASURED = a line this seat read in AQ2's records (named); INFERRED = said so; NOT READ = nothing read tells it.
Source records (AQ2, `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_fwd1_r3/`): `A_RUN_FWD1_R3.txt` (lines 45 to 73), `A_RUN_JOURNAL_R3.txt`, `A_RUN_ROWS_R3.txt`, `run/step_log.txt`, `run/run_report.json`.

## 1. Result: window 3 is SPENT; NO ticket was filed; F2 and F3 FAIL

MEASURED: one run, 16:50:47Z to 17:04:02Z, on the r34f resident, no probe, the files built from SET 3's selection (ALPPL yes, APPL no, ZQXWVK replace VNQ; SPY, AGG, TIMXX). Mint, sign-in and Submit worked (16:50:49Z, 16:50:55Z, 16:51:00Z). The driver pressed **0 of 3** planned decisions and its wait for the ticket answer timed out at 780 s (17:04:01Z); `ticket_id` null; 0 tickets created (F2 FAIL); no accepted request (F3 FAIL); no report (F9 FAIL). The run user is ABSENT by the index and a consistent read; the three probe viewers stay ABSENT (F1). F4 queues 0 0, F5 WE_DL_SENT 0, F6 packager secret unread, F10 yahoo_calls 0, **F12 waf_challenge_lines 0, resolve_retry_exhausted 0**: the WAF back-off was not needed and the upload was not blocked by the WAF. One new stored object (intake 316 to 317), none deleted.

## 2. What the door did (MEASURED, journal and rows)

The upload UP-11914a97... was resolved at 16:53:41Z (`state=READY`) and ended `NEEDS_CORRECTION TEMPLATE_FINDINGS` with 4 findings: TIMXX TICKER_DATA_NOT_ENTITLED (NOTICE, action REVIEW); ALPPL, APPL and ZQXWVK each TICKER_NOT_FOUND (ERROR), **suggestion ABSENT**, actions REPLACE_FILE, REPLACE_TICKER, FILE_UNRESOLVED. The resident made three advisory (KIMI) check calls: 15.5 s OK, **119.0 s KIMI_TIMEOUT**, 17.6 s OK.

## 3. Two causes, kept apart

1. **The plan depended on an advisory suggestion that is not stable (MEASURED across sets).** ALPPL and APPL carried suggestion AAPL (ACCEPT_SUGGESTION) in SET 2 and in SET 3 and carried NONE in the run, with two of the three advisory calls returning OK. The U1 "Yes" branch cannot be planned on a model's answer.
2. **The driver pressed nothing for 780 s although the door's rows had been final since 16:53:41Z (MEASURED), and it took no screenshot after Submit.** NOT READ: what the form showed between 16:53Z and 17:04Z. INFERRED, not measured: the decisions loop waits for the next planned prompt in order (ALPPL "Yes") and does not skip to APPL "No" or ZQXWVK "Replace" when the Yes button is absent; the same wait would explain 0 of 3 and a 780 s timeout.

## 4. What this does NOT show

The wait for a ticket never reached the downstream hops: nothing here tests the notice display for TIMXX, the swap pass, the report's per-holding disclosure, the four attachments or the commentary hop. The WAF back-off did not engage in the run (0 challenge lines), so r34f's one change is untested live.

## 5. Next (the issuer's recommendation; the CTO rules)

A fourth window needs a new addendum and a new address (the order's NO RETRY). Recommend that it: (a) plan only branches the door answers deterministically (Replace for a NOT_FOUND, No/unresolved for another, the TIMXX notice) and treat a suggestion-dependent Yes as optional; (b) run on a driver amended (own W7 pair) so each prompt round takes a screenshot and a prompt with no planned button falls through to its planned alternative instead of waiting; (c) mint the staff user with `allowedFirmIds = [the one firm]` if it falls after the combined ticket-service release (CTO msg 9670); (d) run on r34g (yfinance first, pricing ON) installed first, since this window is closed.
