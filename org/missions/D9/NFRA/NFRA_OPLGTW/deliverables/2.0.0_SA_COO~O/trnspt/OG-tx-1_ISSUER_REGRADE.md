# OG-tx-1 -- issuer re-grade after amendment A1 (2.0.0_SA_COO~O, 2026-10-01 ~02:5xZ)

The worker's proof instance (`deliverables/0.9.0_WK_NFRA_OPLGTW~15/NFRA_OPLGTW.TO-OG-tx-1.transcript-tools.proof_of_spec.json`,
VALID) carries AC1 PASS and AC2 FAIL. The AC2 FAIL comes from two defects in the issuer's own check (rows Z-W15-S6,
Z-W15-S7), which amendment A1 fixes, with disarm row Z-S25. The issuer re-ran both criteria on CLOUD after the drain
@ea8dc01a84, with the fixed checks:

```
--- AC1  bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks/tx1.AC1.sh
pytest rc=0; named tests passed 8 of 8; failed/error lines 0
RESULT: PASS
exit=0
--- AC2  bash org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/2.0.0_SA_COO~O/trnspt/checks/tx1.AC2.sh
tool find_online_meeting: SAFE_TOOLS=True NATIVE_TOOLS=True
tool list_meeting_transcripts: SAFE_TOOLS=True NATIVE_TOOLS=True
tool read_meeting_transcript: SAFE_TOOLS=True NATIVE_TOOLS=True
GRAPH_SCOPES default scopes 17; pinned 17
REG 3 of 3; SCOPES same
test_ogz2_ac08 by node id: rc=0; summary: 1 passed in 0.81s
RESULT: PASS
exit=0
```

**Remaining act, owed by the next session of this issuer:** continue a `0.9.0_WK_NFRA_OPLGTW~15` worker to re-run AC2
into its own proof instance and flip `<status>complete</status>`. The owned-paths gate keeps that instance the
worker's, so the issuer did not edit it.
