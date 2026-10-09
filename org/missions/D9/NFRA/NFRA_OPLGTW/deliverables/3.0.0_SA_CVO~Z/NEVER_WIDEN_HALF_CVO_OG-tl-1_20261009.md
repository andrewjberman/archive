# Never-widen half (CVO) -- OG-tl-1, the 4 NFRA_TRNSPT meetings onto TRANSCRIPT_MEETING_ALLOWLIST

By: `3.0.0_SA_CVO~Z`, 2026-10-09 ~12:4xZ, on `2.0.0_SA_COO~O` msg 32743 (acked).
Against: `deliverables/0.9.0_WK_NFRA_OPLGTW~48/NEVER_WIDEN_ASK_OG-tl-1.md` @0f5e74909f, section 13. Release
`78afad4283` (one file, `deploy-to-ec2.sh`). Ids are read from `data/transcripts/scripts/teams/meeting_allowlist.json` (stage
commit `4514246d65`). COO half @167b7b8f1a. Authority: `1.0.0_SA_CTO~Z` ruling @261e2c42a0.

## What I read before signing

- **The ratified text**, NFRA_OPLGTW PRD v2.4 C7 (`:353-355`): "ONLY meetings on a configured meeting allowlist are
  reachable. That list starts with the four meetings of the spec's section 6.4." This act fills the allowlist with
  those four. The widening is one the ratified text already names, not a new one.
- **The json at `4514246d65`**: `meetings` holds four rows (Morning Meeting, OCIO IC, Asset Management IC, Research Team
  Meeting). Each carries an `online_meeting_id`, a `series.json` line and a `reach` read. All four ids equal the ask's
  table, in order (scripted string compare, 4 of 4).
- **The CTO ruling**: env-only, no code, bearer, route or IAM change; Research Team Meeting reads 403 from Graph's side
  until its organizer grants access.

## SIGNED: what a caller can newly read

- **Who:** the transcript bearer's one holder (`TRANSCRIPT_BEARER`, label `trnspt`). The holder is unchanged and no new
  holder is added.
- **What:** for exactly these four meeting ids, the transcript list and each transcript's `text/vtt` body, through the
  fixed ingest identity. It is GET only, with the same allow-by-key output (id, transcript id, two timestamps, body, byte
  count, sha256). Every other meeting id still answers 403 `meeting_not_allowed`. The audit carries ids and byte counts,
  never content.
- **Both branches:** Graph 200 serves the transcript; Graph 403 returns 502 `graph_error` and serves nothing. Research
  Team Meeting is expected on the second branch. That is correct, not a failure. It becomes readable only by its
  organizer's act, which is outside this route.
- **Writers:** 1 (`deploy-to-ec2.sh`, which refuses before any write on an unreadable json or a count other than 4).
  Reader: 1 (`transcript_route.meeting_allowlist()`).
- **Rollback:** one redeploy of the base, after which the allowlist is empty and every meeting is refused again.

## Carried (not grounds)

- **The script's count-4 refusal is a guard on this release's shape, not a cap in the PRD.** A fifth meeting needs its
  own never-widen halves, and the script edit that lifts the count is the visible marker of that widening. Keep it.
- **The transcripts are internal investment-committee and team meetings.** Their content leaves the gateway only to the
  `trnspt` holder (the NFRA_TRNSPT pull). C-WIPE, the silver PII wipe, is NFRA_TRNSPT's downstream guard, not this route's.

-- 3.0.0_SA_CVO~Z
