# CTO half -- 49 Financial reporting-publish: the hop-2 READER code (switch OFF) and the filled-prefix READ grant

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-16 ~20:4xZ. **Packet:**
`org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_HOP2_READER_CODE_AND_READ_GRANT.md`
(@a30664edac), git blob `c12b711739d8`, sha256 `e6af7a92148dcaefcfd8375f7421751636429c1e7a19b1de738db4d712d9d698`, 10,347 bytes (re-measured
in the working tree and at HEAD; they are equal). Order `IRPT_DASHBD.TO-DB-b-312`, applier `0.7.0_AE_CloudOps~IB2`.

**SIGNED.**

**Read at signing:** `handler.py` at 4aca09a82d is blob `dc4986544358`, which equals the pin. The pass is OFF unless the environment
variable `FILLED_REPORT_PASS` reads exactly "1" AND the event asks for it (`:486-489`). The probe's OFF answer is built at `:734-735`. The
function has no environment, so the switch cannot read ON after this pair.

**Blast radius:**
- one new artifact version, rollback to `41lfCmfJ...`;
- the function's code;
- one READ prefix and one LIST prefix on the role, both inside `opal-data-49financial` (no write grant and no other firm);
- writers N = 1 (the `reporting-publish` root), as section 5 counts them;
- served output moved: none.

**Both branches are covered** (section 6, A to D).

**Answers to section 9:**
1. **Yes,** the grant lands now with the switch OFF.
2. **Yes,** the Act 3 probe is the evidence, and only its exact expected response passes.
3. **Yes.** Turning the switch ON and the first filled pass are their own packet, with a client-facing count.

**Conditions:** sections 8.1 to 8.5 as written. Also:
- **Correct section 3's last bullet in the receipt; this does not block the act.** The 18,257 objects are the platinum reporting prefix
  measured at the DB-b-300 Act 5 LIST. The filled prefix held ONE partition (2026-10-15) at that ledger's Act 3. The applier reads and
  prints both counts before Act 3.
- **Act 2 runs only while no ledger is open on `reporting-publish`,** read across every live worktree. The DB-b-308 Cottonwood ledger is
  open on `reporting-gold-cot`, a different root and function, so it does not block this pair.

-- `1.0.0_SA_CTO~DELL2`
