# IRPT_ANLREQ FWD-1 run, ADDENDUM 3 AMENDMENT 6 -- one third probe set (SET 3) with a 90 s re-post wait and one candidate in flight at a time -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. The order is lifted from HOLD only after the CTO half of THIS amendment is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-16. CTO half: owed, `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
Numbered 6 to match the CTO's msg 9446 and the order's next amendment; there is no pair amendment 5.
Amends: addendum 3 (COO blob `64884b3338965c79a962c3f40cdb5cde44ad5811`) section 3 as amended by amendments 1 to 4 (the fourth: blob `a560bc08075380f7b0137015e3fb2ef9e935dcb8`, CTO half @36d8c81c95). **Only the probe set changes.** Everything else stands as signed: R0e (r34e), R0d (r35L), R0f, the selection rule, the CTO's stops of msgs 9337 and 9446, the inputs, the run, W7.

Claim words: MEASURED = this seat read it in this session; RECORD = a committed record this seat opened (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read.

## 1. What SET 2 showed (RECORD)

AQ2's `A_SET2_ROWS_R3.txt` and `A_SET2_JOURNAL_R3.txt` (commit `bd5a6618db`, read by this seat): with r34e running, ALPPL and APPL read `NEEDS_CORRECTION TICKER_NOT_FOUND` with suggestion AAPL (KIMI_CHECK_PROVIDER_VERIFIED); BREIT and SREIT read `TICKER_NOT_FOUND`, no suggestion; the resident resolved them one at a time (advisory call 60.4, 11.7, 18.5, 17.2 s). ZQXWVK, the fifth, never reached the checker: its YCharts lookup was challenged by the WAF on each of four receives (13:40:45Z to 13:43:46Z) and the row ended `RESOLVE_RETRY_EXHAUSTED`. AQ2's one cookieless, lease-free lookup for ZQXWVK at ~14:06Z read CLEAN (`WAFLOOK_READ.txt`: 200, no WAF action, body `[]`). INFERRED: the challenge is transient (`~G2`'s read, with its erratum msg 9427).

## 2. The change: SET 3 (W8, third set), once

After the HOLD is lifted by the order amendment that cites this blob, the window repeats step 0 ONCE with the rules of amendment 3 section 3 (as amended by amendment 2), with these differences only:
- **The same five candidates, ZQXWVK FIRST:** `ZQXWVK`, `ALPPL`, `APPL`, `BREIT`, `SREIT`. Reason for the order: ZQXWVK is the candidate the CTO's stop rests on; a challenged window then ends after one stored object, not five.
- **One candidate in flight at a time.** A candidate is posted only after the previous one in the order reads a final answer. Reason (MEASURED, SET 2): the resident resolves serially, so a candidate posted behind four others waits for them.
- **The re-post wait is 90 s** (SET 2's slowest resolve 60.4 s plus 50 percent, the CTO's sizing, msg 9446). A candidate whose first answer is RESOLVING is re-posted once, 90 s after its first post, and not before. At most two posts per candidate, ten in all.
- **STOPS:** `ZQXWVK` must read `NEEDS_CORRECTION TICKER_NOT_FOUND` with no suggestion, or the window STOPS before the run user is minted. A candidate still RESOLVING after its re-post ends the SET at that candidate: if it is ZQXWVK the window STOPS; if it is another candidate it does not qualify and the SET continues. If all five are unresolved the window STOPS. A WAF challenge in SET 3 (a RESOLVING ZQXWVK after its re-post, or a journal `WAF_CHALLENGE` line in the window) ends the window; it waits for the resident's bounded backoff change (the CTO, msg 9446). No B-only run.
- **A new probe viewer,** `irpt-r3r-iv-<YYYYMMDD>@opal.invalid` (a name is never reused), minted exactly as the first two (R28b amendment 1, COO blob `fe221dfcf1`; one RS256 token, exp at most 20 minutes, never written or logged), removed (ABSENT by the GSI and a ConsistentRead) before the run user is minted. R0b adds this address to the ABSENT reads; `irpt-r3p-iv-20261016@opal.invalid` and `irpt-r3q-iv-20261016@opal.invalid` stay ABSENT.
- **Records:** the SET 3 PROBE lines go below SET 2 in `A_RUN_FWD1_R3.txt` marked `SET 3`; the selection rule applies to SET 3 only. The applier lists the intake prefixes BEFORE and AFTER, and every new object or new VersionId by key and VersionId under `SET 3` in `OBJECTS_WRITTEN_FWD1_R3.txt`; none is deleted in the window (the delete is ordered after run 3 is graded; Andrew's standing word, CTO msgs 9395 and 9402).
- **If SET 3 passes** (ZQXWVK reads NOT_FOUND and the selection rule yields its rows) the window continues to the run user exactly as signed.

## 3. Blast radius (the delta over amendment 3 section 5)

Up to five more stored `original_holdings` objects and ten more door posts by one more transient internal-viewer identity (a token, no password, at most 20 minutes), upload route only. Nothing else moves.

## 4. Limits named

NOT read: whether a WAF challenge recurs in SET 3 (intermittent; the single lookup at 14:06Z read CLEAN). **The run's own uploads meet the same lookup: a challenge during the run would end that row after about three minutes and spend the single no-retry window.** This amendment does not remove that risk; only the CTO's backoff change does. The CTO signs knowing it. Whether the Kimi suggestion appears again for ALPPL and APPL (live).

## 5. Owed before the order is lifted from HOLD

1. The CTO half of THIS amendment, on this file's blob.
2. This seat's order amendment 6: the SET 3 text above and a `lift HOLD` commit citing the blob. Cut only after (1).
