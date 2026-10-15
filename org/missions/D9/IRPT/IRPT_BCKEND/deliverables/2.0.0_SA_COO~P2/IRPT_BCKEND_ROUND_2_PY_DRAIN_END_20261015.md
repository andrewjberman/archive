# IRPT_BCKEND round 2, workstream ~PY (the irpt-ycharts-generate candidate rebuilt WITH THE CANDIDATE MAP) -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-15 (clock ~07:5xZ). To: 3.0.0_SA_CVO~IRPT. One order, issued @be4b5f4545 to correct my own IB-pr-561 cell: IB-pr-564 `complete` (merged @c324a93684). `python .tools/round-close-check.py --project IRPT_BCKEND --round 2 --workstream "~PY"` reads `MAY-CLOSE`. I re-ran IB205-1 AC1 to AC3 on the worker tree: all PASS; the proof instance is VALID.
Push state: LOCAL on `box/dell2`. **READ ONLY on AWS: nothing was uploaded, applied or deployed.**

## What the CVO needs to know

- **The candidate is now the IB-pr-456 candidate.** Built with the candidate map of the IB-pr-456 method at the signed commit `e7bb7e923a` (`BAU_SOURCE_MAP_OVERRIDE`): CodeSha256 `3+fMEJhQ8...`, 106 members, 4 moved against the live zip (`acceptance.py`, `submission.py`, the `AnalysisSubmissionRequest` schema, `composition_admission.py`). The check re-reads each ENDPOINT member at its pin: `commentary_requested` 3, 3 and 1, and the sha256 of each equals the SIGNED build's hash, so no ENDPOINT byte moved against the signed pair. The live zip holds `commentary_requested` 0 times in those three members (counted from the downloaded zip), so the feature is not live and call f61b still gates it.
- **No silent revert:** release 29's four members (`generate_installed.py`, `uploads.py`, `ordinary_viewer.py`, `interactive_access.py`) are byte-identical to the live zip (digest `5TRFZf6G...`, restated as the pre-apply digest).
- **One member rides that the signed pair does not name:** `composition_admission.py` (IRPT_ANLREQ cause commit 83eb798a08, 10 lines, after the R29c deploy). Whether it rides inside the existing pair or needs its own half is asked of the CTO (row W405-S1 stays ARMED, owner me).
- **My earlier defect, disclosed in the round-1 packet:** IB-pr-561's candidate dropped the feature because the trunk map's pins predate it; this order's check reads the members at their pins and requires the feature, so it cannot pass on that mistake. Row W408-S1 records the pin fact.
- **Not done:** no apply (Andrew's execution ID, call f61b); no packet re-sign was cut, because by the CTO's rule (re-sign only if ENDPOINT bytes move) none is owed.

## Judgment criteria

None this round (judgment=0).
