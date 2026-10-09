# NFRA_MCPORTAL -- ROUND 4 DRAIN PACKET (L8 input) -- 2.0.0_SA_COO~MP, 2026-10-08 ~23:1xZ

**Round:** 4, the FWD-14 control-plane thread. The decomposition is v4 @202c512520. The PRD is v0.5 @cecf26d2c9, whose
ratified-text half was signed @8de5b2dc76.
**Risk:** WORLD on both cells. **Judgment criteria:** none in round 4. FWD-14's judgment sits on the round-5 close run
(MP-x-5, G-SEE).

## Orders: 2 of 2 terminal

| Order | Drained | Issuer re-run | Live? |
|---|---|---|---|
| MP-x-1, the owner-gated `GET /api/admin/fabric/boxes` | @1cf3a1dce5 (worker head eb9c655e68) | in a fresh no-cone worktree at eb9c655e68: AC1 7 passed with 5 of 5 named tests; AC2 30 passed, 0 failed; AC3 routes=1 | no. It goes live through MP-x-4, and the store read through MP-x-3 |
| MP-x-2, the Control Plane page with amendment 1 (it refreshes while open) | @6b1b7b18dd (worker head 9600f81d2d) | in `C:/tmp/mp-r4-6`: AC1 5 of 5 named tests, 5 pass, 0 fail; AC2 9 labels in order, suite 0 fail; AC3 build rc=0 | no. mcportal d60b4e0 is a LOCAL commit on `wk-NFRA_MCPORTAL-r4-6-mcportal` and goes live through MP-x-4 |

`round-close-check.py --project NFRA_MCPORTAL --round 4`: 2 of 2 complete, proof_ok 2, verdict=MAY-CLOSE.

## The one real run (the outcome's real entry point, before release)

The drained handler's `_compute(6)` ran on this box against the LIVE store
`s3://opal-313476888478-globgrph/fabric/activity/v1/`, read at 2026-10-08T23:07:18Z, over the window 17:06:58Z-23:06:58Z.
It scanned 2150 records with 0 skipped and took 21.1 s cold.

| box | status | commits | seats | top projects | last commit |
|---|---|---|---|---|---|
| dell2 | reporting | 409 | 47 | IRPT_BCKEND 120, NFRA_TRNSPT 59, ADVI_COTBKF 37 | 23:06:54Z |
| laptop | reporting | 268 | 21 | LGIC_BLANKFIX 33, NFRA_CTLPLN 30 | 23:05:22Z |
| dell1 | reporting | 120 | 18 | MDPF_SECCLASS 25, MDPF_STRATID 16 | 22:46:33Z |
| sitez | **not reporting** | 0 | 0 | none | null |

**ACCEPT (iii), cross-check.** `.tools/fabric-activity.py boxes --hours 6`, read about 1 minute later, gives dell2 411,
laptop 269 and dell1 120 (2153 records scanned). dell1 is equal. The dell2 (+2) and laptop (+1) deltas are commits that
landed between the two reads: each box's last-commit time moved forward by exactly that interval.

**ACCEPT (ii).** Site Z reads "not reporting", and that is the true state: site Z writes no activity record (C12; the hook
is placed with `0.0.0_AB_MSTR~Z`).

## Rows filed this round

- `Z-S18`: C11's grant against the gateway's no-globgrph control. RULED (a) by the laptop NFRA_CLDGRPH owner (msg 107359,
  relay 32030).
- `Z-S19`: the one-issuance limb refused a late cut, so MP-x-3, MP-x-4 and MP-x-5 move to round 5.
- `Z-W5-S1` and `Z-W5-S2`: a cone-mode sparse worktree cannot pass the `org/missions` commit gates; a no-cone pattern list
  can.
- `Z-W6-S1`: the sparse cone lacked paths the commit gates read.
- All are INERT.

## Proposed round-5 enrichment list (the issuer's read; the CTO's analysis rules)

1. **MP-x-3, the gateway read grant, under ruling (a).**
   - Its checks, x3.AC1 to x3.AC3, are committed and FAIL at base.
   - Its applier is now `0.7.0_AE_CloudOps~Z` (msg 32061, Andrew-direct ~22:0xZ).
2. **MP-x-4, the release of MP-x-1 together with mcportal d60b4e0.**
   - G-REL: it releases after NFRA_OPLGTW r29.
   - Load note: the cold read is 21 s for 2150 records from this box, against a nano with one worker. Measure it on the
     host. If it nears the ALB idle timeout, warm the cache or narrow the default window.
3. **MP-x-5, the close run.** G-SEE: Andrew opens the page and names one box's projects. The round's JUDGMENT criterion
   sits here.

Worktree note for the cut: cut worker worktrees with a NO-CONE pattern list (row Z-W5-S2).

## Armed rows (12 by `comp-surprise --project NFRA_MCPORTAL --json`)

- Every one predates round 4. Their owners are `2.0.0_SA_COO~O` (live), `1.0.0_SA_CTO` and `2.0.0_SA_COO~MP` (live).
- No armed row has an owner the issuer could not seat.
- `Z-S10` (owner `~MP`) is measured disarmed on the deployed bytes by `Z-S17`; its remediation-plane close is the CVO's.
