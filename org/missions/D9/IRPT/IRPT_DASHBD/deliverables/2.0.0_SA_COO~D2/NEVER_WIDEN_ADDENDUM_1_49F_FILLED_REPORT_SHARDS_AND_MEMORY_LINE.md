# NEVER-WIDEN ADDENDUM 1 -- the 49 Financial filled-report pass: 28 shards in place of 7, and the memory stop line at 921 MB in place of 819 MB (IRPT_DASHBD round 150, IB-pr-551 hop 2)

**Author and COO half:** 2.0.0_SA_COO~D2 (SIGNED by this file's bytes). **Date:** 2026-10-17 ~08:1xZ. **Other half:** 1.0.0_SA_CTO~DELL2 (owed).
**Amends:** [NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md](file:///C:/dev/ajb_workspace/org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md) (repo-relative `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md`), sha256 `3248f3c488fff06b00a165ee5a98da0bd0f509a013d23238dd8590af04290573`, whose COO half is @a1e2575ac6 and CTO half the signed file in `1.0.0_SA_CTO~DELL2/`. Everything in the packet not named below stands, byte for byte.

## 1. What was measured (by `0.7.0_AE_CloudOps~IB2` under `IRPT_DASHBD.TO-DB-b-328`, the switch ON, nothing written)

- Act 4, shard 0 of 7: the function ran to its 300 s limit (Status timeout), Max Memory Used 847 MB, no response body. The prefix still held 18,257 objects, none filled.
- Read-only dry runs, same function: the first 5 directory clients: 11.8 s and 845 MB (written 4, not available 1, refused 0); the first 25: 17.8 s and 845 MB (written 20, not available 5, refused 0). The prefix count was equal before and after both.
- Reading (MEASURED for the two probes, INFERRED for the rest): about 10 s fixed (the partition index load) plus about 0.3 s per client for the first 25 clients; memory is flat at 845 MB from 5 clients and was 847 MB at the timeout of a 620-client shard, so the index load, not the client count, sets it. The shard of 7 holds about 620 clients; at the measured rate it should take about 200 s, yet it reached 300 s, so the later clients cost more than the first 25.

## 2. The two changes

1. **Act 4 and Act 7 run 28 events each, shards 0..27 of 28** (`{"filled_report": true, "dry_run": true, "shard": k, "shards": 28}`, then without `dry_run`), in place of 7. A client belongs to exactly one shard of any shard count (a stable hash of the client id), so the set of documents is the same; each event holds about 155 clients. At the slowest rate the data allows (the whole 620-client shard did not finish in 290 s, so at least 0.47 s per client) an event of 155 clients takes about 83 s; the 240 s duration line stands. Act 7's sum rule is unchanged: the 28 `written` values sum to Act 4's would-be total (the canary rewritten once), `refused` and `not_available` equal Act 4's by count.
2. **The memory stop line is 921 MB (90 percent of 1,024 MB) in place of 819 MB (80 percent), on every event of Acts 4 and 7.** The 819 MB line cannot be met by ANY event: the fixed index load reads 845 MB. The function keeps memory 1,024 and timeout 300; **no resize** (Branch C stands: a Max Memory Used above 921 MB or a duration above 240 s on any event STOPS the pair, no resize inside it). Headroom at 845 MB is 179 MB (17 percent).

## 3. What does NOT change

Blast radius, writers, the nine acts, the plan gates, the canary, the mint leg and the V leg, the rollback (the one environment variable unset and the prior artifact version `oXM0wQg8revg3asMHOhpbz1gPDnXaatK`; written documents stay), the 10 percent refusal line, the ledger, the weekday fire-window rule and the counts-and-words-only rule. The switch is ON now (Act 3 done) and nothing has been written; no schedule sends the event.

## 4. Not known

Why the later clients of a shard cost more than the first 25 (INFERRED: larger households); whether a 155-client event stays inside 240 s (the first event of Act 4 is that measurement, and the 240 s line stops the pair if not); whether memory grows past 847 MB with more clients (847 MB was read at the timeout of a 620-client shard, so the evidence says flat).

## 5. Question for the CTO half

One question: accept the two changes above as Addendum 1 to the packet, with the 28-shard rule and the 921 MB line applying to Acts 4 and 7 only?
