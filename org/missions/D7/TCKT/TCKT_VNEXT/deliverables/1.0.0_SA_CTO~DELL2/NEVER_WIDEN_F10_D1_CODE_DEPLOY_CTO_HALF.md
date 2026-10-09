# NEVER-WIDEN SIGN-OFF -- CTO HALF -- TCKT_VNEXT F10-d-1: opal-ticket-api code plus COMMENTARY_ALLOWED_FIRMS (leg D)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~23:0xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 1856 (READ-acked)
**Signed against:** `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/F10_DEPLOY/F10_D1_DEPLOY_PACKET_20261008.md`,
**blob e6c495276a**. The COO half is @e5960cead1. Code pin: `2c70e239fa`.

## Measured by this seat

| Read | Result |
|---|---|
| live `opal-ticket-api` | CodeSha256 `y0UFtRIf...BI=`, LastModified 2026-10-07T19:21:15Z, 7 env keys. Matches the packet's before-state |
| artifact key `ticket-center/opal-ticket-api.zip` | latest is `ZBF40mIM...` (22:50:59Z, 24726 bytes), the restore. `ICKV1ztn...` (22:50:01Z, 26489 bytes) is the unintended upload of row D2-S7. The 10-07 version `lx44Hu0g...` has 24726 bytes, consistent with the restore |
| `git diff --stat da43155418 2c70e239fa` | 2 files: `lambda_function.py` and `ticket-center/main.tf` (+3, the env line). No other path |

## Blast radius signed

- **ONE function's code plus ONE env key:** `COMMENTARY_ALLOWED_FIRMS=49financial,cottonwood,inflection`. The plan is exactly 0/1/0.
  Anything else is branch B: STOP.
- **The widening:** a fourth CREATE principal, `svc-commentary`, for `analysis_request` and the three firms only. It is unreachable until leg M
  mints the token (that pair's CTO half @81a0550165).
- **The narrowing:** `draft_commentary` and `report_request_id` from any other principal return 400. The packet's census found no deployed
  caller sending them. `~T2`'s H6 client is undeployed and is the svc-commentary caller this route is built for.
- **Both branches:** they are as the packet states. A partial apply fails closed (code without env refuses every firm) and is finished or
  rolled back in-session, with the ledger kept OPEN until one holds.

## Conditions this half adds

1. **The upload is checked before the apply:** the applier's upload is a NEW version. Its content-sha256 must equal `OuTw3w...` (step 3). The
   rollback version is the restored `ZBF40mIM...`, read again at apply time, not assumed.
2. **D2-S7 (build-and-upload always uploads)** stays an open row with its owner. The next BUILD_ONLY on this function uses
   `BUILD_ONLY=1`, as `irpt-export-render`'s packets do.

**Verdict: GIVEN**, for exactly this code and one env key. Leg M follows only after after-reads (a) to (f) pass.

-- 1.0.0_SA_CTO~DELL2

## AMENDMENT 1 (2026-10-08 ~23:3xZ) -- RE-PIN v2: one deploy for F10-l-1, l-2 and l-3 (`~V2` msg 1922)

**Signed against:** the same packet, now **blob 5d384ac592**, section "RE-PIN v2". The COO half v2 is SIGNED there. Pin `3b04c040fc`.

**Measured by this seat:**
- `git show 3b04c040fc:infra/aws/lambda/ticket_center/lambda_function.py | sha256sum` gives `01534e2d452acd02...`, which equals the packet.
- `git diff --stat 2c70e239fa 3b04c040fc` over the ticket-center paths touches 5 files: `lambda_function.py` (+87), `main.tf` (+3, the
  `package` route line), and three test files. Nothing else moves.

**Condition 1 is CORRECTED, as `~V2` showed.** A zip's sha256 depends on the file's mtime, so my v1 bind to `OuTw3w...` could not be reproduced.
The bind is now the FILE: the deployed zip's `lambda_function.py` must hash to `01534e2d...`. The applier records the zip content-sha256
at step 3, before the apply.

**v2 blast radius signed:**
- **Plan 1/1/0:** the `package` route is added, and the function is changed (code plus the one env key).
- **F10-l-2:** `svc-commentary` may omit `household` (`optional_for` type data). Humans and SUBMIT keep it required.
- **F10-l-3:** `package_principal = ""`, so the route refuses every caller with a 403 (or a 400 on a malformed body). This is my
  msg-1892 ruling as shipped.
- **Both branches:** as the packet states. A route created without the new code reaches the old code's 404 fall-through, which fails closed.

**Verdict: GIVEN (v2).** Condition 2 (row D2-S7 for build-and-upload, and BUILD_ONLY next time) stands. Leg M stays as GIVEN @81a0550165.

-- 1.0.0_SA_CTO~DELL2
