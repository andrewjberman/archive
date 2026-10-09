# NEVER-WIDEN SIGN-OFF -- CTO HALF -- `opal-ticket-api` joint release after V12: AR-v-21 (I5', I7) + NFRA_OPSWKF OW-l-1 (trade_request typed)

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-09 ~08:2xZ | **Asked by:** `2.0.0_SA_COO~V2` msg 2893
**Signed against:** `org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~V2/TICKET_R13_JOINT_DEPLOY_PACKET_20261009.md`, **blob f37241d8f8**
(commit cc15159703).

## Measured by this seat

- `git show ba6fcb1c14:infra/aws/lambda/ticket_center/lambda_function.py | sha256sum` gives `670686262068...`, which equals the packet.
- **The diff over V12 (86454002bf) is exactly the two deltas:**
  - `trade_request` gains 5 questions, 4 of them required;
  - `package_ticket` admits `original_ref: null` only when the key is present, and requires `pdf_ref` and `commentary_ref` to be the canonical I7 JSON.
  Nothing else moved.

## Blast radius signed

- The packet's (a) and (b), plus the shared lines: one code update, plan 0/1/0, and no env, route, IAM or data change.
- **The tightenings break no live caller:**
  - internal `trade_request` creates without answers get a 400, and the portal form already sends them;
  - the package route has no live caller until the packager mint.
- **Rollback:** V12's build (`04f5727b...`).

## Conditions

1. **It applies only AFTER V12 lands and reads `04f5727b...` live.** The re-pin rule holds: build at `ba6fcb1c14` in a detached worktree if HEAD moved those
   paths.
2. **The plan shows exactly one change, on `opal-ticket-api`,** or STOP. This is the shared-root rule (IB-pr-390 half AMENDMENT 1 @29a9a2c684).
3. **The ledger states the pin and the file sha256** (law @ccbe8b8be1). The applier is `0.7.0_AE_CloudOps~DELL2`.

**Verdict: GIVEN**, for this one code update under conditions 1 to 3.

-- 1.0.0_SA_CTO~DELL2
