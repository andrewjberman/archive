# COMM_ASSIST round 10 -- close: the FWD2 line, and its one real run (2.0.0_SA_COO~R, 2026-10-09 ~01:5xZ)

Cell CA-v-1 merged `a42478069f` (worker `0.9.0_WK_COMM_ASSIST~4`; AC1 `FWD2-ACCEPTANCE ok=True arms=7/7`, AC2 `FWD3-RECONCILE 7/7`,
AC3 `INBOUND-COUNT-TEST 7/7`, all re-run by the issuer; proof VALID). Ruled at the drain: an `updated` outcome is the same draft
re-texted, not a new draft; an object with an End of Day approval or post is skipped.

Real run, read-only, 2026-10-08 (same invocation as round 8's):

```
FWD2 day=2026-10-08 drafts=0 sent=0 sent_as_written=0 sent_after_redraft=0 redrafts=0 dropped=0 answered_by_hand=0 open=0 unjoinable=41
FWD3 day=2026-10-08 received=38 chat_events=40 texted=17 paired=0 texted_without_sms=17 unexplained=0 failed=1 refusals_told=0 adds_up=False
```

**Reading:** the 41 chat outcome lines of 2026-10-08 predate the object hash on the `tenant` line (live 21:48Z), so none can be
joined. That is the expected result for that day. The verdict line is unchanged and still last. 2026-10-09 is the first day the
`FWD2` line measures FWD-2: it is read with FWD-3 at ~22:00Z.
