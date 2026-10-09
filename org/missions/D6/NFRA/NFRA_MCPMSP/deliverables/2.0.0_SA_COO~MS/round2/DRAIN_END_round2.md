# NFRA_MCPMSP round 2 -- drain-end packet (L8 input)

**Issuer:** 2.0.0_SA_COO~MS, 2026-10-09 ~05:5xZ, site Z. Re-seated by 0.0.0_AB_MSTR~Z on 1.0.0_SA_CTO~Z msg 32397
(Andrew ~04:4xZ: "yes also make sure that all COOs are running /canonical-drive on their attached projects.").

## Orders (round 2, read by `python .tools/round-close-check.py --project NFRA_MCPMSP --round 2`)

| read | value |
|---|---|
| orders in round 2 | 14 |
| complete, proof structurally OK | 11 of 11 (`proof_ok=11 proof_bad=0`) |
| cancelled | 3: MS-sv-1, MS-rn-1, MS-rx-1 (Amendment A-CANCEL in each order) |
| judgment criteria | 1: MS-dn-1 AC5, UNGRADED -- the round's only open L9 item |
| verdict | REFUSED, on AC5 alone |

Cancelled: the three cells needed G-MSPID (an MSP calling identity; holder Andrew). Andrew 2026-10-01 ~17:4xZ: "doesnt
matter right now"; "we just want to have the infrastructure to do so even if not fully proven"
(`org/tier1_exec/4.0.0_SA_CRO~O/deliverables/ANDREW_DIRECT_20261001_174xZ_OPEN_CALLS_8194_YES_MSPID_DEFER_MCPINDEX_PRIORITY.md`).
Their FWDs stay ungraded and go to the round-2 analysis; re-cut in the first round after G-MSPID is answered.

## Owed to the CVO at L9

**MS-dn-1 AC5** (judgment; the gateway firm Deny changes no served answer). Material:
- `org/missions/D6/NFRA/NFRA_MCPMSP/deliverables/0.9.0_WK_NFRA_MCPMSP~5/AC5_BEFORE_MS-dn-1.json`
- `org/missions/D6/NFRA/NFRA_MCPMSP/deliverables/0.9.0_WK_NFRA_MCPMSP~5/AC5_AFTER_MS-dn-1.json`
- Issuer read at completion (08772a9c10): sha256 before/after equal on 10 of 10 keys (9 firm + 1 global). The order
  named 3.0.0_SA_CVO~O as grader; the reviewer on this box now is 3.0.0_SA_CVO~Z.

## Channel (`comp-surprise --project NFRA_MCPMSP --json`)

| read | value |
|---|---|
| investigation rows | 31 (`INVESTIGATION_v1.Z.md`) |
| adjudication rows | 2 |
| remediation rows | 7 |
| open | 12 (Z-W1-S9, -S10; Z-W3-S3..S6; Z-W4-S3; Z-W5-S1..S4; Z-W7-S1), plus new Z-S4 |
| armed | 0 |
| CVO watermark | `REMEDIATION_v1.Z.md` (round 1) -- round-2 rows are uncompiled |
| armed rows whose owner could not be seated | none |

New row **Z-S4** (this seat): `round-close-check.py` matches proof `to_id` exactly while `proof-of-spec-check.py`
matches slug-tolerantly, so 11 valid proofs read PROOF-BAD until `<to_id>` was declared on the 14 round-2 orders
(repair done in this commit). Disarm owner 1.0.0_SA_CTO~Z.

## Round state

Every round-2 order is terminal. L8 (channel compile + AC5 at L9) is the CVO's; then the slug to the CTO.
