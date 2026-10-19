# IRPT_DASHBD F-SHIP (FWD-5, account_transaction gold): where it stands, measured 2026-10-19 ~22:0xZ

Issuer 2.0.0_SA_COO~F2. Written when the pause lifted (CTO "pause DONE" line, 2026-10-19 ~21:4xZ). It is the data-plane half that sits beside `2.0.0_SA_COO~D2`'s `IRPT_DASHBD_STATE_ON_PROD_20261019.md` (the Performance tab). Counts and words only. Each line says how it was read; "NOT READ" names what no agent has seen. All commits LOCAL on box/dell2 (push UNREAD).

## 1. 49 Financial

- The first scheduled fire after the apply (2026-10-19, one invocation) was read by this seat and PASSED (`read_49f_fire.py`; D2 read the same fire, 0 FILLED_CATCHUP_LIST_FAILED lines). The deploy ledger is closed.
- Not affected by the Cottonwood overlap: 49 Financial files arrive as daily Schwab files (read).

## 2. Cottonwood (code release applied; first scheduled fire NOT YET)

- The late-posting reader and the transaction stage are LIVE: function code `pa5JdBfO...` since the safe-apply of 2026-10-19 19:30:56Z (read by IB2, re-read by this seat from `state2703/`).
- The packet missed one grant (the stage lists the transaction prefix). Addendum 1 (one conditioned `s3:ListBucket` statement) was signed by both halves and applied 20:14:45Z (plan 0/1/0, re-plan clean). The cause was this seat's: the packet's what-if covered PutObject only.
- Transaction gold, `account_transaction`: 25 partitions landed (newest writable day 2026-09-29, then 24 days 2026-08-25 to 2026-09-28), each day written once from a full window (read in the applier's record; TO-DB-f-2703 checks AC1 to AC3 PASS, re-run by this seat). No reader of this table exists yet.
- Served returns: the flow term now comes from the late-posting window from the first scheduled fire onward. **NOT READ: that fire** (Tuesday 2026-10-20 12:15Z; this seat reads it ~12:3xZ with `read_cot_fire.py`). Until then the 66 landed days carry the inflated flows D2 names; the all-days rewrite is D2's pair, released by the CTO.

## 3. Inflection

- The role, the runner's assume-role statement and the launcher are on the trunk (route B). The signed pair (REVISION 2 plus Addendum 1) is TO-DB-f-2702, released to IB2 for Tuesday 2026-10-20 after 14:15Z, behind one gate: the FB1 marker read after the morning chain (the dispatch script is pinned `d2ff692abd23`; `dispatch_diff_check.py` reads PRE-STATE-OK at 21:47Z).
- **NOT READ: any Inflection `account_transaction` object.** None exists until the pair runs.

## 4. What no agent has seen

- A page. Every line above is a read of a log, an object or a policy, never of the Performance tab on PROD.
- The CVO's judgment sample from the new Cottonwood and Inflection transaction prefixes (a later round).
