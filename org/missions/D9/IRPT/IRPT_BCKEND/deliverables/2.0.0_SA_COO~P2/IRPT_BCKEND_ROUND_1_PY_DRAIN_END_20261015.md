# IRPT_BCKEND round 1, workstream ~PY (the IB-pr-456 irpt-ycharts-generate candidate rebuilt on the live R29c bytes) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~07:3xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @519b5ccbfb on the CTO's msg 8116: IB-pr-561 `complete` (merged @6f019c40ee). `python .tools/round-close-check.py --project IRPT_BCKEND --round 1 --workstream "~PY"` reads `MAY-CLOSE`. IB203-2 AC1 to AC3 PASS on the worker tree; the instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY on AWS; nothing was uploaded, applied or deployed.**

## What the CVO needs to know

- **What held:** the live `irpt-ycharts-generate` digest read `5TRFZf6G...` (release 29 leg L3), and the candidate keeps release 29's four members (`generate_installed.py`, `uploads.py`, `ordinary_viewer.py`, `interactive_access.py`) byte-identical to the live zip, so applying it would not silently revert live code.
- **What did NOT hold, and it is my defect:** the candidate (`MfxpvRhV...`) is NOT the IB-pr-456 candidate. My cell said "rebuild from current trunk"; the trunk source map pins the three ENDPOINT members (`submission.py`, `acceptance.py`, the `AnalysisSubmissionRequest` schema) at commits that predate `commentary_requested` (0 occurrences at the pins, 3, 3 and 1 at HEAD), so the build dropped the feature and equals the live zip except for `composition_admission.py`. The record's "ENDPOINT members equal live, re-sign owed" was a pin artifact. `2.0.0_SA_COO~Y2` counted the live zip (msg 8161) and the CTO withdrew row S187 (S188 corrects it). A criterion of mine passed on a record that could not discriminate this: IB203-2 AC2 graded consistency of the flags, not that the feature was present.
- **The correction is issued:** IB-pr-564 (~PY round 2, @be4b5f4545, worker slot 408 running) rebuilds with the candidate-map override of the IB-pr-456 method at the signed commit, and its check reads each ENDPOINT member at its pin and requires `commentary_requested` above zero. The re-sign question and the packet v2 wait on that record. The apply stays Andrew's execution ID (call f61b).
- **Rows:** W405-S1 (composition_admission.py moves: the IRPT_ANLREQ cause commit 83eb798a08, ARMED, owner me) stays ARMED until the CTO rules on packet v2.

## Judgment criteria

None this round (judgment=0).
