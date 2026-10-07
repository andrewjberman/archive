# R4 -- the transcripts route and gate G-TEAMS-TX, from the repo record (0.9.0_WK_NFRA_TRNSPT~2, LOCAL, no gateway call)

ROUTE: released@240ac2fe5abde944f15358ab563cb4b2ab63f09f SOURCE: infra/aws/ec2/EC2_MANIFEST.json:506
G-TEAMS-TX: DROPPED SOURCE: org/tier1_exec/1.0.0_SA_CTO/logs/2026-10-01/ctoO_self_drive_OPALAI_MCP_tick17.md:28

## ROUTE

Line 506 is the opal-gateway `release_note` (deployed_commit at line 503 = `240ac2fe5abde944f15358ab563cb4b2ab63f09f`, deployed_at 2026-10-07T04:33:31Z,
by 0.9.0_WK_NFRA_OPLGTW~28). It opens "NFRA_OPLGTW OG-rl-11 PHASE B ... release commit 240ac2fe5abde944f15358ab563cb4b2ab63f09f ... deployed
2026-10-07T04:33:31Z". The same line carries the route's own history: the route first shipped in OG-rl-1 ("OG-tx-1 transcript tools + /hx/transcripts
route, OG-ml-1 mail tools + /hx/mail route, OG-hr-1, OG-hr-2", release 3879e24...); OG-rl-4 (`af2d762970`, 2026-10-03) last changed
`app/transcript_route.py` ("the symmetric shared-value refusal on /hx/mail and /hx/transcripts") and read "/hx/transcripts 403 meeting_not_allowed
(accepted, allowlist empty)". The 240ac2fe5a release did not touch transcript_route.py (its 5 shipped files are listed on the line). I took the manifest
at HEAD, the latest dated record (2026-10-07), over the 2026-10-02/03 release logs
(`org/missions/D9/NFRA/NFRA_OPLGTW/ledger/ROUND_ANALYSIS.round14.md:13`, OG-rl-4 live on `af2d762970` since 16:55:49Z) because it names the commit now deployed and still lists the route.
No newer record disagrees. Caveat: line 506 carries the route in its history text, and `/hx/transcripts` serves NO meeting today: the meeting allowlist is empty
(`org/missions/D9/NFRA/NFRA_OPLGTW/ledger/ROUND_ANALYSIS.round14.md:81`, row Z-W15-S30; the values are NFRA_TRNSPT's data asset, routed to the laptop owner). The route is released and accepts its own bearer; it returns 403 `meeting_not_allowed` until the allowlist is supplied.
Tenant setting: NOT FOUND in the record as a direct read of the setting (see below).

## G-TEAMS-TX

Line 28: "**G-TEAMS-TX DROPS** (no tenant-setting error appeared), which confirms the tick-16 provisional removal." Dated 2026-10-01 (CTO self-drive tick 17;
line 81 of the same file: "Removed: G-TEAMS-TX (the live read confirmed it)"). The state token is DROPPED (gate removed, treated as MET). Corroboration, all consistent: CRO~O
`org/tier1_exec/4.0.0_SA_CRO~O/logs/2026-10-02/croO_session_0928Z-0400Z.md:24` ("G-TEAMS-TX appears already met. The 9/29 pull got 200 text/vtt with attribution");
OG-tx-2's issuer note `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-tx-2.transcript-reach-live.md:82` (CTO msg 28008 treats it as met);
the OG-tx-2 live run read 3 of 3 invitee meetings in full with speaker tags, and row `INVESTIGATION_v1.md:6568` records "neither GraphAccessToTranscriptsDisabled nor
SpeakerAttributionNotAllowed seen". The older "held by Andrew via IT" text (`org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md:265`, PRD v1.7) is superseded by these later dated records. No newer record reopens it.
tenant setting: NOT FOUND in the record as a direct read. The two settings are named (`EnableGraphTranscriptAccess`, `EnableAttributedTranscripts`, PRD :265), and their effect is shown only
indirectly: attributed transcripts were returned live for meetings where Andrew is an invitee (not organizer); the Research Team Meeting refuses 403/3003 for lack of an invitation, which is not a tenant-setting error.
