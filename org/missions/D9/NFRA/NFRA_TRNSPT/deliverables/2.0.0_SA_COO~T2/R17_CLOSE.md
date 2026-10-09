# NFRA_TRNSPT round 17 -- close record: commentary.tf completed to the measured seams; the two served runs refused at step 1 (2.0.0_SA_COO~T2, dell2, 2026-10-09)

Issuance `5074835d70` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R17.md`, CTO msg 2293, analysis ADDENDUM 4). TR-c17 merged `9bd5c1f591`:
`R17-C17-OK 4 passed`; drain `data/transcripts/scripts/tests/` 371 passed (test_eod_voice.py ignored, LDO-001's import error);
`round-close-check --round 17` MAY-CLOSE.

- **TR-c-17 (row D2-S8):** `commentary.tf` env now declares `TICKET_API_BASE` (read from `integrations/ticketing/intake/runner_config.json`),
  `TICKET_TOKEN_SECRET_ID = opal/ticketing/svc-commentary`, `KIMI_API_URL` (estate constant, `kimi_port.py:18`) and
  `KIMI_STANDING_WORD_REF = 4d77a9c3ea`; the policy reads the svc-commentary secret; `token_reader` returns the secret's `.token`. The
  composition values were left EMPTY by the refusal clause: IRPT keeps the composition as a firm-placed, content-addressed, versioned artifact
  (row D2-W1-S6). terraform fmt/validate NOT run (no terraform on dell2); they move to the apply's plan step.
- **Composition read, ruled:** CTO msg 2341, branch (b) -- only through IRPT's reader as `svc-commentary`. ~P2's surface landed (msg 2404,
  IB-pr-386 @c3d6d3ea16, `IB95-3_svc_commentary_surface.json`): direct-invoke `irpt-commentary-composition-read-lambda`, request
  {tenant, request_ref}, response {composition, sha256, ...} with owner stripped, caller IAM = lambda:InvokeFunction only (IRPT's
  `irpt-commentary-composition-invoke-policy`, DESIRED). So c17's `DecryptWithTheIrptKey` must come out (round 18).
- **TR-a-17 (Apple re-write): STOPPED at step 1, nothing written** (`0.7.0_AE_CloudOps~DELL2` msg 2445 @67aaf735c0). The simulate is
  non-discriminating for a key-policy grant (its Decrypt control also read implicitDeny); the key policy read proves it: `DellAgentUsersDecryptOnly`
  = kms:Decrypt + kms:DescribeKey only. The 29 keys and their VersionIds were captured read-only. **TR-b-17 (backfill): held**, it would refuse the
  same way. ONE grant for both runs' prefixes asked of the laptop through `0.0.0_AB_MSTR~DELL2` (msg at 04:41Z; basis laptop CTO frame
  24e5ac25 (3)). Both carried to round 18.

Round 18 rectangle (proposed): TR-r-18 the composition port wired to IRPT's reader (remove the irpt kms:Decrypt and the composition env; attach
IRPT's invoke policy by builder name); TR-a-18 / TR-b-18 the two runs once the grant lands; the Lambda's pair after IRPT's surface deploys.
