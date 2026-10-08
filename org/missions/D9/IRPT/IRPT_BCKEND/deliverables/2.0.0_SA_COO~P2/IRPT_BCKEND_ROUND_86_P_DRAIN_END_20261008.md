# L8 drain end -- IRPT_BCKEND round 86, workstream ~P (round 85 was cut and NOT drained)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-08 ~22:0xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD by path
floor; code + packet, BUILD_ONLY, nothing uploaded or applied | **Drain:** @6303e36222 on box/dell2 (branch wk-IRPT_BCKEND-181) |
**Judgment criteria:** 0 | `round-close-check`: MAY-CLOSE

**Naming:** per Andrew-direct (CTO msg 1653), the "custody report" is the **Performance client statement**. Code ids are unchanged.

## Round 85 (IB-pr-372) -- cut, completed on its branch, NOT drained (CTO msg 1651)

IB-pr-372 reached the writer through a marked direct-invoke event in which the caller asserted the principal and the account set (row
D2-W180-S2). The CTO ruled: do not drain, because that would put a caller-trusting write path in HEAD, and recut. Branch
`wk-IRPT_BCKEND-180` @3528d24f92 is kept as a record. It is not an ancestor of HEAD (verified).

## Round 86 -- IB-pr-373, slot ~181: the Performance client statement writer, recut

- **Trigger:** the guarded Entry. `POST /api/scoped/investor-reporting/custody-report` is a DECLARED route row, served as operation
  `custody-report-persist` behind the CUSTOM portal authorizer. It is Opal-only. `entry.py` carries no direct-invoke path.
- **Identity:**
  - The principal comes only from the verified headers.
  - The request carries `retained_request` (by reference), `document` and an optional `provenance`. Any other key (owner,
    principal, account_ids, tenant, firm_id) is refused by name.
  - The owner and accounts come from the retained custody submission, loaded under the read's own rule and compared to the
    repository's admitted owner.
  - The accepted source refs come from that artifact (row D2-W180-S1 closed).
- **Pin P 9238309eca.** Census: five members, owned (`entry.py`, `submit_installed.py`, `custody_persist.py` added, `custody_write.py`
  added, registry at b4d98a4fe3 with `irpt-custody-x10-v1` ACTIVE).
- **BUILD_ONLY:** from a clean tree, rc 0, built `rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek=`. **Replay:** identical bytes on
  ANALYSIS and PERFORMANCE; the negative control is refused.
- **Graded by the issuer:**
  - IB86-1-AC1 PASS.
  - IB86-1-AC2 PASS (44 composed, 24 derived-owner, 11 guarded tests; 0 `irpt_custody_persist` in entry.py).
  - IB86-1-AC3 PASS. Proof VALID.
- **Halves:** COO half @cb29ea67bd (packet blob d7264acfc8). CTO half asked, with a REC on row D2-W181-S2.

## Rows

| row | status |
|---|---|
| D2-W181-S1 | Carried by D2-S9: the role lacks the requests-table write and the custody-prefix S3 write/read, so the persist fails closed. The laptop IAM leg was asked of 0.0.0_AB_MSTR~DELL2. |
| D2-W181-S2 | Carried by D2-S9 to the CTO with the pair: the document is caller-supplied, and the record names the submission's creator, not the persister. |
| D2-W181-S3 | INERT: routes.json `_denominator` was stale before this cell. |

**Push state:** LOCAL on box/dell2.
