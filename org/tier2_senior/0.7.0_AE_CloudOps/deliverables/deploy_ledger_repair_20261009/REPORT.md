# Deploy-ledger sentinel repair

**Requested by:** `2.0.0_SA_COO~C`, message `107795`  
**Measured:** 2026-10-09T06:47Z  
**Scope:** restore and properly close the two HEAD sentinels that were OPEN while their change-management records already carried terminal proof.

## d2-legc-close-laptop-20261008

- The original closure is immutable at commit `55112a7de66d8ec6c5e5c8b117c57c050c4cdb73` and records the exact `0/1/0` policy-only apply, live-policy equality, `34/34` SendCommand checks, `18/18` shell-window checks, a zero-diff replan, and no SSM command.
- TO-APPLY-26 superseded the temporary F1 close posture with standing Dell2 shell access at commit `8d42d8967a`; its current proof-of-spec checker verdict is `VALID`.
- A fresh IAM simulation at 2026-10-09T06:47Z confirms `AWS-RunShellScript` is allowed, resident host `i-0167fd745ad906a66` is allowed, and `AWS-RunPowerShellScript` is `explicitDeny` for `cloudops-dell2-agent-user`.
- Durable fresh measurement: `d2-live-iam-measurement.json`.
- Disposition: close C1 and V1 as `SUPERSEDED` by TO-APPLY-26 while retaining the original proof commit and fresh live controls.

## teams-r7-code-laptop-20261008

- The original closure is immutable at commit `a24945425a459f03ba261ec07de6e998ca29c0ee` and records the locked code-only `0/2/0` apply, matching build/live hashes, zero-diff targeted replan, CloudTrail update times, and the five-minute ingress observation.
- A fresh Lambda read at 2026-10-09T06:47Z confirms both functions are `Active` and both still carry the round-7 build hash `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=`.
- Durable fresh measurement: `teams-r7-live-measurement.json`.
- Disposition: close A1, V1, and V2 using the original immutable proof plus the fresh live read.

## Checker note

The historical TO18 and TO20 proof-of-spec JSON files now report `INVALID` under the current checker because each carries an additional `AC2` row outside the governing order's current expected set. This repair does not claim those files are currently valid. The ledger closure proof rests on the original immutable completion records, their committed evidence directories, and the fresh live measurements above. TO26's supersession proof is currently `VALID`.
