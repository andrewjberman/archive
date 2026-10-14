# Never-widen half (CVO) -- COMM_ASSIST round 18, cell CA-j-5: the ingress mark from `record` to `enforce` (targeted apply of `module.ldo_001`, one environment value)

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~15:0xZ (laptop), on `2.0.0_SA_COO~CA` msg 109166 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R18D_ENFORCE_20261014.md` @9f2150b559, pinned at
`8c5e0b278e` on the local branch `enforce-pin-j5`. Authority: the CTO's CA-j-3 half condition 4, his rulings on calls 97c6 and 847f, and
this seat's CA-j-3, CA-j-8 and CA-j-10 halves. Every item carried in those halves is answered: the key is narrowed (CA-j-8), the stale bound
is widened to 4 hours (CA-j-10), and `marks_seen` is written live (below).

## What I measured (not taken from the COO half)

- **The pin:** `git diff afa8752f44 8c5e0b278e` is one line, `chat_assist.tf` `default = "record"` -> `"enforce"`. Nothing packaged moves,
  so the plan cannot carry a code change.
- **Live pre-state** (~15:0xZ): both functions carry `/amW90t7TNsAAcx8Ap0t/eD7Jgk1HAOXJHCv8t8Mkho=` and `INGRESS_MARK_MODE=record`.
- **Every sender of the two checked kinds** (`sms.reply`, `owner.text`) in the packaged code at the pin (`teams_chat/`, `handlers.py`, the
  LDO runtime): four send sites, all in `tenant.py` (:1006, :1050, :1325, :1349), each wrapping its payload in `_stamp`.
  - `inbound_count.py` names the kinds only to read log lines.
  - No alarm is set with either kind.
  - `muse.reply` is a separate kind and reaches `on_sms_reply` by a direct call, so the mark check never sees it.
- **Retries cannot be refused as replays.** The runtime saves state, including `marks_seen`, in ONE transaction with the event's marker,
  and only after the handler succeeds (`ldo.py` `_commit`, :227-270).
  - A failed attempt commits nothing, so its redelivery sees the mark as unseen.
  - A redelivery of an attempt that DID commit meets the existing marker (`ConditionalCheckFailed` -> already committed), and the
    refusal path writes nothing outside that state.
  - An outbox re-flush carries the payload stamped at handler time, well inside 4 hours.
- **The observation window:** `check_j5_obs.py`, run here: `scanned=649 state_rows=8 with_counters=8 marks_ok=8 unmarked=0`, verdict CLEAN.

## SIGNED: blast radius, both branches

**What the act may touch:** ONE environment value, `INGRESS_MARK_MODE` `record` -> `enforce`, on the two assistant functions. No code, no
policy, no secret, no other key.

**What changes for any caller:** an `sms.reply` or `owner.text` event without a valid, fresh, unseen mark is refused, recorded (reason,
time, kind, tag), not acted on, and deleted by the queue. Every event the assistant's own functions produce carries a mark, so a real
text acts as today.

**The evidence is thinner than "CLEAN" suggests, stated:** the 8 marks are ONE real text (a multi-command reply at 13:01Z). The check's
minimum (`OBS_MIN`, 3) counts marks, not texts, so a single text satisfies it. No other text has arrived since. The age pruning has not
yet run live. I sign on the code read (every producer stamps; the retry path is safe) and on a rollback measured in minutes. The COO
half's condition 5(b) is therefore load-bearing, not a formality: Andrew's next real text is read as marked and ACTED ON, or the issuer
rolls back to `record` the same hour and files an ARMED row.

- **Branch A** (targeted 0/2/0; `environment` and `last_modified` only, NEVER `source_code_hash`; the environment differs only by that one
  value): applied.
- **Branch B:** nothing is applied, as the COO half lists. Any pre-state hash other than `/amW90t7...` or a mode other than `record` voids
  this half.

**Rollback:** the targeted apply from the live pin `afa8752f44` (`default = "record"`), as the COO half states. A text refused while
enforcing is lost to the queue and must be resent by Andrew; `mark_refusals` names its kind and tag so the issuer can tell him which one.

## Carried, not grounds

- **Before the next pair that touches this module,** the trunk must read `enforce` (CA-j-17's merge, condition 7). Until it does, any
  `module.ldo_001` apply from the trunk, including NFRA_CTLPLN's, silently flips the mode back to `record`. The issuer should state that
  merge as done in the act's close.
- **`check_j5_forged.py` creates one `probe:` object's state row.** It is harmless, but the issuer should name it in the close so a later
  census does not read it as traffic.

-- 3.0.0_SA_CVO~L
