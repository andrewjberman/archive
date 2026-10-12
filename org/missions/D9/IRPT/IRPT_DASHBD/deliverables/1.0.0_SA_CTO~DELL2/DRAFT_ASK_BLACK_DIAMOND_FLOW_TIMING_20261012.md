# Draft for Andrew to send -- one question to Black Diamond on cash-flow timing (open call e41e)

**Drafted by:** `1.0.0_SA_CTO~DELL2`, 2026-10-12 ~21:2xZ, on laptop `1.0.0_SA_CTO` msg 108675 (relay msg 6565). **Send:** Andrew, to
his Black Diamond (Advent/SS&C) contact, as written or edited. **Holds:** no client name, account, figure or file.

---

Subject: Question on how Black Diamond times external cash flows in performance

Hi -- a quick methodology question for our performance team. When Black Diamond calculates time-weighted returns, how does it time
an external cash flow (a contribution or withdrawal) within the day it posts: is the flow treated as arriving at the start of the
day, so it earns that day's return, or at the end of the day, so it does not? And is that a firm-level setting we can see or change
for our account, or the same for every client? A one-line answer, or a pointer to the page of your methodology documentation that
states it, would be ideal. Thank you.

---

**Why it is asked:** the IRPT_DASHBD tie-out of Opal's 49 Financial returns against Black Diamond does not close under an end-of-day
convention on 51 segments, and Black Diamond's method help is behind a sign-in (round-86 analysis @976ca0db4d). The answer closes
the tie-out's flow-timing class; no cell waits on it.
