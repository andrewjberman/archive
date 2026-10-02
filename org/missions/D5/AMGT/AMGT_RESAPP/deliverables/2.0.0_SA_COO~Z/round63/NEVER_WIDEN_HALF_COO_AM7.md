# AMGT_RESAPP round 63 -- `AMGT-am-7` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~16:4xZ

**The act (ONE, four PUTs):** to the versioned bucket `opal-data-harvest`, PUT four planned objects at four NEW keys, each after
checking the local file's sha256 against its plan entry. Executor `0.7.0_AE_CloudOps~A`; order
`task-orders/AMGT_RESAPP.TO-AMGT-am-7.the-management-objects-write.md` (sections 1, 6 AMENDMENT 1 and 7 AMENDMENT 2); decomposition s.71.
**Sequence:** after am-6 leg 1 is graded, so the reader that serves these objects is the code they were graded against.

## THE KEYS, read live at signing (before-state)

| key (`s3://opal-data-harvest/...`) | source file | sha256 | before |
|---|---|---|---|
| `management/v1/6501_JP_Equity/2026-10-02.json` | `0.9.0_WK_AMGT_RESAPP~205/m1_pool/<key>` | `9398a8808ff1...` (plan) | 404; prefix holds 0 objects |
| `management/v1/2317_TT_Equity/2026-10-02.json` | `0.9.0_WK_AMGT_RESAPP~205/m1_pool/<key>` | `66b79e014a9f...` (plan) | 404; prefix holds 0 objects |
| `peers/v1/BP-SLASH-_LN_Equity/2026-10-02T1543Z.json` | `0.9.0_WK_AMGT_RESAPP~209/peers_pool/<key>` | `89b06e8bdec5...` | 404; served now: `2026-09-24T2252Z.json` |
| `peers/v1/NG-SLASH-_LN_Equity/2026-10-02T1543Z.json` | `0.9.0_WK_AMGT_RESAPP~209/peers_pool/<key>` | `3589f0d6eff9...` | 404; served now: `2026-09-24T2252Z.json` |

Plans: `m1_fwd7_plan.json` sha256 `598950e3150bae6f975a5f47c56bb38657c354418f07706842a60b3d54a3a595` (its `ASML_NA_Equity` entry is
NOT written, AMENDMENT 2); `peers_slash_plan.json` sha256 `ccb09b8ab20a7caff35bdf19970444b423da5d5b9dbe302a17002a8b969fec22`.
Positive control on the 404s: `head-object` of the existing `peers/v1/BP-SLASH-_LN_Equity/2026-09-24T2252Z.json` returns VersionId
`szq0ir8TBXw3EWuVoCqu4JDGqoi_dS3_`.

## WRITERS OF THE PROPERTY: the producers of `management/v1/` and `peers/v1/`

The management batch (`lib/research/management/batch.py`) builds only `real_filing` names, so it never writes 6501_JP (no_object) or
2317_TT (placeholder_only). The peers objects are written by the peers build; no peers build is in flight at signing. The route serves
the newest as_of per key, with no process cache, so each PUT serves on the next request.

## READERS

Security Analysis: the management panel for 6501_JP and 2317_TT, and the peers panel for BP/ LN and NG/ LN (DEV and PROD).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| key | what it MAY touch | rollback |
|---|---|---|
| the two `management/v1/` keys | one NEW key each | no prior object exists, so only a delete restores "no object", and an S3 delete needs Andrew's word. The served status is ABSENT before and after; only the reason text moves. |
| the two `peers/v1/` keys | one NEW key each | PUT the `2026-09-24T2252Z.json` bytes under a newer as_of key, which the route then serves (the halves name it at that time). |

## EXPECTED OUTCOME -- both branches, read from the route's own rule (newest as_of per key wins)

- **The PUTs land and serve:** `r63_served.py --cell c2 --where deployed` reads C2 PASS for 6501_JP ("no persisted filing for this name
  in the pool ...") and 2317_TT ("No filing could be matched to 2317 ..."), each ABSENT with its own reason instead of the "no M-1
  management object has landed" fallback; C1 (ASML_NA) FAIL, held on the vendor word (row Z-W205-S1). `--cell c6 --where deployed
  --plan <peers plan>` reads 52 of 52 (base at signing 0 of 52): BP and NG peers go from `basis` absent to derived, `members` 0 to 12,
  `subject` null to the pool block's classification (vintages 2026-09-30).
- **Failure branch:** a sha256 mismatch before a PUT is a STOP before writing; c6 under 52 of 52 after the PUTs -> the peers rollback
  above; a c2 C2 FAIL -> STOP and report (the management keys are not rolled back without Andrew's word).

## WHAT THIS HALF DOES NOT COVER

No other key, no S3 delete, no vendor call, no code or function change.
