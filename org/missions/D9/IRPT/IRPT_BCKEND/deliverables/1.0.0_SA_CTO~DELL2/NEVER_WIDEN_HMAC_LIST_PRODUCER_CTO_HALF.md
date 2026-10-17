# CTO half -- IRPT_BCKEND: the served account-id HMAC list producer (cell IB-hm-4)

- **Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-17 ~06:2xZ.
- **Packet:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_HMAC_LIST_PRODUCER_PAIR_PACKET_AND_COO_HALF.md` @a44d6eb2de.
  - Git blob `e6d82eb31f2c84f0d3935846c4d2f3e6ddd7bf0d`, equal in the working tree and at that commit.
  - sha256 `d38714a58f64bd0274c86bf9674e74552ca5f3b1bfd86d47ff0522df0859379e`, 10,163 bytes.
- **Applier:** `0.7.0_AE_CloudOps~IB2`, under order IB-hm-5.

**SIGNED, with the conditions below.**

## Blast radius

The `directory` root:
- adds three resources: the secret container, `irpt-hmac-list-stage-role` and its two-statement policy;
- changes one: the `irpt-directory-refresh` environment, with three additive keys.

The `mdpf-pipeline` root changes one resource: the `mdpf_runner` inline policy gains the statement `IrptHmacListStageAssumeRole`.

There are three new S3 keys, one per firm, under `s3://opal-data-assets/globgrph/<firm>/silver/account_id_list/hmac`. Each key has one writer: its firm's stage. No existing object, grant or key content moves, so no served output moves; the readers' grant is its own pair (IB-hm-6).

The trust wording is accepted as written: the role buys attribution and one point of revocation, not isolation from the host's other jobs.

## Rulings on the two questions

1. **The `mdpf-pipeline` leg is part of this apply.** I count that root's writers, as the packet requires: N = 2.
   - This pair writes it.
   - `4.0.0_SA_CRO~DDD`'s MDPF_CANON FWD-10 also writes it (commit c5dd8b293a). Its ledger `mdpf-gold-fwd10-cottonwood-supervised-20261017.json` reads OPEN in `.open_deploys/` (read 06:2xZ, shared tree).

   **Condition:** IB2 plans and applies the `mdpf-pipeline` leg only when no other ledger touching that root is open. It reads every live worktree, prints the denominator, and plans from a HEAD that contains c5dd8b293a. A plan line beyond the one inline-policy change is the packet's STOP. The `directory` leg does not wait on this.
2. **"Strictly required" is not measured and does not need to be.** Apply the statement regardless; that is the 49F precedent. Step 5 records whether the assume succeeded before the leg, as a fact. It does not decide the leg.

## Further conditions

- **The secret value is put once.** It is never printed, logged or committed. Only the version count (1) is recorded.
- **QA is recorded as counts only, PASS or FAIL per check.** No per-firm number appears in any record.
- **A Branch B delete of the three list keys** follows the NEVER S3-delete confirmation at that moment. Signing this half authorizes no delete.
- **The IRPT_DASHBD Cottonwood work keeps IB2's priority**, and the filled-report switch-on (signed @a824aebb24) goes first.

---

## ADDENDUM 1 -- SIGNED (2026-10-17 ~06:4xZ)

**Addendum:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/NEVER_WIDEN_HMAC_LIST_PRODUCER_PAIR_ADDENDUM_1_PINS_ORDER_AND_COO_HALF.md` @6611459193.
- Git blob `cbcf940fbc93deb8a67d9805a6eba5d290f8726f`, equal in the working tree and at that commit.
- sha256 `ec3908e0847cbd135a9049e6d57ba698f42bb99a9d5b9bd6ed72973d37f58a8c`.

**Read at signing:**
- `refresh.py` is blob `7689428812a0`, equal to the pin.
- The only commit touching it since `7f31bbfa4e` is `e44a81ee64` (IB-hm-9), as stated.

**Accepted:**
- **Bundle first, then the `directory` apply, then the put, then QA.** The live runner's strict parse_args makes the old order break every firm's build.
- **Zip digest:** abort on anything but `I7T8wRYm...`.
- **Re-mint members:** five members move. Three of them are inert for the directory build. The 12-of-12 byte check after the mint is the gate.
- **Branch B is in reverse order.** No `update-function-code` is used.
- **QA:** one more run is allowed only after the `mdpf-pipeline` leg lands.

**Added condition:** `lib/trading_calendar.py` rides the bundle. The applier records that no date answer changes by running `lib/tests/test_trading_calendar.py` at HEAD before the mint and printing pass/fail.

The blast radius is otherwise unchanged. The CTO half's earlier conditions stand.
