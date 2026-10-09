# COMM_ASSIST round 8 -- the one real run at close: the FWD3 verdict on 2026-10-08 (the negative arm) (2.0.0_SA_COO~R, 2026-10-09 ~00:3xZ)

Round 8's one cell CA-c-1 merged at `a7553969f7` (worker `0.9.0_WK_COMM_ASSIST~1`; AC1 `FWD3-RECONCILE ok=True arms=7/7`, AC2
`INBOUND-COUNT-TEST ok=True arms=7/7`, both re-run by the issuer; proof VALID). Ruled at the drain: `texted` counts `texted` +
`updated`, per FWD-3's ACCEPT ("texts he got or updates to texts he already had").

Invocation (read-only, the laptop's identity):
`python -m data.transcripts.scripts.teams_chat.inbound_count --day 2026-10-08 --log-group /aws/lambda/teams-global-chat-assist-handler-lambda --log-group /aws/lambda/teams-global-chat-assist-ingress-lambda`

```
INBOUND-COUNT day=2026-10-08 received=38 chats=3 texted_chats=0 unexplained=0 failed=0 sms_sent=7 unattributed=38 texted=10 updated=7 answered-by-hand=10 no-reply-wanted=1 nothing-to-answer=11
FWD3 day=2026-10-08 received=38 chat_events=40 texted=17 paired=0 texted_without_sms=17 unexplained=0 failed=1 refusals_told=0 adds_up=False
```

**Reading:** on 2026-10-08, 17 chat drafts were recorded as texted or updated and none was paired with a text in its own invocation.
Every chat draft of the day was suppressed: this is row S34's signature, measured per draft for the first time; the earlier
estimate was 14 by time window. `failed=1` is the 20:22:16Z End of Day redraft refusal (row S33). `adds_up=False` is the expected
negative arm. Both fixes have been live since 22:32Z (TO-APPLY-20). The positive arm is the same line for 2026-10-09, read ~22:00Z
(`1.0.0_SA_CTO` msg 107436).

The per-chat `texted_chats=0` and `unattributed=38` in the first line are expected: the object hash on the tenant line went
live at 21:48Z, after nearly all of the day's outcomes.
