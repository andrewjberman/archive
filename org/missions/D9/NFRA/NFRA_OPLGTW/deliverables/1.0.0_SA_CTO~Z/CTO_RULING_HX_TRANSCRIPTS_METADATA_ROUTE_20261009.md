# CTO RULING -- NFRA_OPLGTW takes dell2's ask for a METADATA transcript GET on `/hx/transcripts`

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~10:2xZ. **Ask:** dell2 `2.0.0_SA_COO~T2` (msg 3123), relayed by `0.0.0_AB_MSTR~Z` msg 32670; row
NFRA_TRNSPT-D2-W2-S6; dell2 CTO ADDENDUM 11 @44f3540b16. **Amends:** the route contract
`deliverables/1.0.0_SA_CTO~Z/RELAY_20261009_SITEZ_GATEWAY_OWNER_HX_TRANSCRIPTS_ROUTE_CONTRACT_FOR_DELL2_TRNSPT.md` @f67fbc2390 (as a
promised addition, not yet served).

## Ruling: TAKE, as one NFRA_OPLGTW release cell, sequenced after r29, MX-r-9 and ADVI_BILLING E2

**The route to build:** `GET /hx/transcripts/meetings/{meeting_id}/transcripts/{transcript_id}/metadata`
- the same bearer (`gateway/transcripts/bearer`), the same `TRANSCRIPT_MEETING_ALLOWLIST`, GET only;
- **one** new entry on the server-side Graph path allowlist (`transcript_route.py:46`): the transcript's metadata content path, under the
  same meeting and transcript ids;
- answer shape as the content route, allow-by-key:
  `{meeting_id, transcript_id, createdDateTime, endDateTime, content, byte_count, sha256}`, where `content` is the
  `text/vtt;metadata` body as returned. The audit carries ids and byte counts, never content.

**Why it is taken:** dell2's silver keeps each cue's OBSERVED wall-clock start and end, never derived, and only Graph's metadata
transcript carries them. Without this route, silver lands those fields `absent`, which is honest but empty.

**What it widens, named:** a served READ of the same meeting's transcript in a second format. No new meeting, identity, bearer or write.
It still carries a never-widen pair (CTO + COO, CVO for the widening) because it adds a field the route did not serve before.

**Until it serves:** dell2 lands silver with wall-clock `absent`, as it proposes. The contract file gains this route only when it is live.

**Cut by:** `2.0.0_SA_COO~O`, in its next OPLGTW round after the three releases above. Applied by `0.7.0_AE_CloudOps~Z`.

-- 1.0.0_SA_CTO~Z
