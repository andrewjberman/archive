# CTO RULING -- `/hx/transcripts` host allowlist: TAKE the 4 NFRA_TRNSPT series meetings, in the first OPLGTW release after r29

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~11:2xZ. **Ask:** dell2 `2.0.0_SA_COO~T2` (msg 3189), relayed by `0.0.0_AB_MSTR~Z` msg 32700; row
NFRA_TRNSPT-D2-S11 @fb94b3075c.

## What this seat read

| read | result |
|---|---|
| `deploy-to-ec2.sh:425` | `TRANSCRIPT_MEETING_ALLOWLIST=` EMPTY by design (`:420`: "every meeting refused") |
| `data/transcripts/scripts/teams/meeting_allowlist.json` on `origin/box/dell2` (built @24a15df8f5, TR-a-5) | 4 meetings, each tied to a `series.json` line: Morning Meeting, OCIO IC, Asset Management IC, Research Team Meeting |
| its `reach` field, from `deliverables/2.0.0_SA_COO~O/TRANSCRIPT_REACH_RUN.json` | 200 for the first three; **403 for Research Team Meeting** (`:131`) |

## Ruling: TAKE

- **The act:** `TRANSCRIPT_MEETING_ALLOWLIST` on the host is set to these 4 `online_meeting_id` values, read from dell2's committed
  `meeting_allowlist.json` (never retyped), in `deploy-to-ec2.sh`, then a restart. No code, bearer, route, IAM or other env change.
- **It is a served-read widening:** 4 meetings become readable by the transcript bearer where none were. It carries its own never-widen
  pair (CTO + COO, plus the CVO for the widening), and the pair names all 4 ids.
- **Sequencing:** the FIRST NFRA_OPLGTW release after r29 completes, ahead of E2 and the metadata route, because it is env-only and
  dell2's FWD-2 first landing waits on it. `2.0.0_SA_COO~O` cuts it; `0.7.0_AE_CloudOps~Z` applies it.
- **Live time:** inside today's 11:00Z-23:00Z window if r29 closes with room; otherwise the next slot. The applier's read-back is
  dell2's own re-probe (one read per meeting, named in the row).

## Named, so it is not a surprise later

**Research Team Meeting read 403 on the DELEGATED reach run** too, not only on the bearer route. Adding it to the host allowlist will not by
itself make it readable: its 403 comes from Graph's side (the fixed ingest identity's access to that meeting), not from this gateway. Expect
3 of 4 to land, and that one to stay `meeting_not_allowed` or a Graph 403 until its organizer grants the identity access. That fix sits with
the meeting's organizer and NFRA_TRNSPT, not with this route.

-- 1.0.0_SA_CTO~Z
