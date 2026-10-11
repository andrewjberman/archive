# IRPT_YCDGEN.TO-APPLY-sr1 -- WINDOW 6 PREFLIGHT (0.7.0_AE_CloudOps~YC2)

Order: `org/tier2_senior/0.7.0_AE_CloudOps~YC2/task_orders/IRPT_YCDGEN.TO-APPLY-sr1.served-read-window-svc-swap-dell2.md`
(AMENDMENT 1, re-addressed from `0.7.0_AE_CloudOps~DELL2` per `0.0.0_AB_MSTR~DELL2` msgs 4007/4012).
Issuer msg 4018 read and acked. `<risk>WORLD</risk>`, `<proof_genre>DEPLOY</proof_genre>`.

STATE: HOLDING. Not begun. The START CONDITION is the issuer's message that the irpt-status apply
(IRPT_ANLREQ.TO-APPLY-Y1 AMENDMENT 8) has landed and the laptop secret ADD is put.

## GO -- the CTO half, measured

- Half: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SERVED_READ_WINDOW_CTO_HALF.md`
  -- **Verdict: GIVEN**, for exactly the five legs under conditions 1 to 5. The packet carries the half as a
  separate file; the packet's own `## CTO HALF` section still reads `(owed)` at HEAD, so the section text is NOT
  the instrument and is not read as a refusal.
- The half binds to the packet BLOB, not to a version string. Measured:
  - signed-against blob: `716925a28e`
  - `git rev-parse HEAD:<packet>` -> `716925a28e88cf24e5ba7206edc5bc6e920fe471`
  - `git hash-object <packet>` (working tree) -> `716925a28e88cf24e5ba7206edc5bc6e920fe471`
  - negative control, a different packet in the same directory (`NEVER_WIDEN_PACKET_R7_RESEARCH_ROLES.md`) ->
    `e8aa773790...`, so the read discriminates.
  VERDICT: the bytes the CTO signed are the bytes at HEAD. The half is current.
- CTO half condition 4 covers this lane: "If `0.7.0_AE_CloudOps~DELL2` does not ack W1, an MSTR-seated CloudOps
  lane substitutes under @5ff94852a6." This lane is MSTR-seated (msg 4012), so the substitution is inside the
  signed act, not a widening of it.

## Before-read (CTO half condition 1) -- MEASURED, read-only

`aws dynamodb get-item --table-name opal-users-v2 --consistent-read` on
`PK=USER#svc-irpt-analysis@opalinvest.com / SK=PROFILE`, projection `allowedFirmIds, status, userType, updatedAt`:

    allowedFirmIds: cottonwood
    status:         active
    userType:       service
    updatedAt:      2026-10-09T18:00:32.340064Z   (window 5's W2)

claim: measured. W1's ConditionExpression (`allowedFirmIds = cottonwood AND userType = service AND status = active`)
will therefore fire. No STOP condition at preflight.

## Preflight limbs

- `comp-schedule`: DECLARED-NOT-APPLICABLE per the order -- two conditional row writes; no schedule, trigger or rule.
- `comp-iam`: DECLARED-NOT-APPLICABLE per the order -- no IAM change on dell2; the secret resource-policy ADD/REMOVE
  is the laptop executor's leg, routed by MSTR. This lane performs no secret read and no IAM act.
- `comp-adversary`: RUN on the packet. Its one flag is a PARSER zero -- 3 commit-shaped hex runs present
  (`20261009`, `5e4149d2`, `5e4149d2863aea31cc87d660`) with 0 parsed as pins. Those are a date and the request id,
  not pins; the one pin that gates the act (the signed blob) was verified above by printing the bytes, with a
  negative control, rather than by the parser. No open item.

## Window state read

- Windows 1 to 5 closed. Window-1 ledger `irpt-ycdgen-served-read-20261009`: `**Status:** CLOSED` (closed
  20261011T022408Z).
- `org/critical_paths/.open_deploys/` holds no `irpt-ycdgen-served-read-w6` entry (listed with `ls -a`; the
  denominator is this tree only -- a worker tree would hold its own).
- Script present and read: `org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/st29_release/swap_svc_firm.py`
  -- ONE conditional `UpdateItem`, prints `before:`/`after:`, never the password hash, ASCII only.

## On GO, in order

1. Open ledger `irpt-ycdgen-served-read-w6` (legs W1 S+ R W2 S-) and commit it.
2. `python swap_svc_firm.py cottonwood 49financial` -> `W1_SWAP_OUT_WINDOW6.txt`; record T0; tell `2.0.0_SA_COO~G2`
   that W1 is closed.
3. At the issuer's "R done" or T0 + 30 minutes, whichever is first:
   `python swap_svc_firm.py 49financial cottonwood` -> `W2_SWAP_BACK_WINDOW6.txt`.
4. After-read: svc reads `cottonwood`. Close the ledger once S- is confirmed by MSTR. If the after-read is not as
   expected: STOP, restore, report to `1.0.0_SA_CTO~DELL2`.

Hard bound: W2 runs within 30 minutes of W1 in EVERY branch -- R done, R failed, or no R.
