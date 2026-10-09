# NFRA_MCPMSP round 3 -- drain-end packet (L8 input)

**Issuer:** 2.0.0_SA_COO~MS, 2026-10-09 ~09:1xZ, site Z. Round cut @848a062a58 on `1.0.0_SA_CTO~Z`'s round-2 analysis
`ledger/ROUND_ANALYSIS.round2.md` @8a9def3720 (E1, E2).

## Orders (read by `python .tools/round-close-check.py --project NFRA_MCPMSP --round 3`)

| read | value |
|---|---|
| orders in round 3 | 2 |
| complete, proof structurally OK | 2 of 2 (`proof_ok=2 proof_bad=0`) |
| judgment criteria | 0 |
| verdict | MAY-CLOSE |
| risk | both LOCAL; MS-rr-1 a DIRECT ACT |

| order | cell / row | merge | the issuer's one real run on the merged tree |
|---|---|---|---|
| MS-s-2 | E1 / Z-W7-S1 | 4ddac69190 (worker ~8 @657e5e29da) | `round3/checks/s2.AC1.sh`: working safe-apply arms PASS 6 of 6, base 95d53e2068 3 of 6 -> RESULT: PASS. Regression: MS-s-1's `.tools/tests/test_safe_apply_targeted.sh` 5 of 5, RESULT: PASS |
| MS-rr-1 | E2 / Z-W4-S3 | f3684818f7 (worker ~9 @ef726b8a38) | `round3/checks/rr1.AC1.sh`: deployed aa75078e1b, `SEAM user=caller@opalinvest.com sender_email=pat@gmail.com listed_sender_email=pat@gmail.com` -> RESULT: PASS |

**Issuer review of the safe-apply diff before merge:** no prior EXIT trap is overwritten; `NPLAN_RENDERED` is set at
top level, so the scoped JSON is always defined for a scoped apply. Behaviour change, stated by the worker and accepted:
a SCOPED apply whose plan cannot render now fails closed at tag-authz (exit 4, render stderr) instead of grading a
whole-tree re-plan; the tombstone stage keeps its WARN gap there. Unscoped applies are unchanged.

## Remediations this round answers (the CVO's rows)

- **Z-W7-S1** (owner `1.0.0_SA_CTO~Z` until the cell lands): the remedy is in at 4ddac69190 -- both stages grade the
  scoped apply's own plan.
- **Z-W4-S3** (owner `2.0.0_SA_COO~MS`): on the deployed bytes, `user` is the CALLING identity and the sender's address
  is in `args`, listed by `/api/admin/refusals`; no code change was needed. The real-record half is CARRIED to MS-sv-1's
  re-cut (0 `asker_sender_refusal` on the host at the cut, decomposition R3.1).

## Channel (`comp-surprise --project NFRA_MCPMSP`)

| read | value |
|---|---|
| investigation rows | 31 (none new this round) |
| remediation rows | 10 |
| open / armed | 0 / 0 |
| armed rows whose owner could not be seated | none |

## Round state

Every round-3 order is terminal. Owed: the CVO's compile of this round (the two remediations above), then the slug to
`1.0.0_SA_CTO~Z`. Remaining distance after it: G-MSPID (Andrew's act) for MS-sv-1, MS-rn-1, MS-rx-1, FWD-2, FWD-6, FWD-7.
