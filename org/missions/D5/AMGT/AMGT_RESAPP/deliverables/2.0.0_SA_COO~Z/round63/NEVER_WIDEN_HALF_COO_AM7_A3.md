# AMGT_RESAPP round 63 -- `AMGT-am-7` AMENDMENT 3 never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~19:2xZ

**The act (ONE, three PUTs):** to the versioned bucket `opal-data-harvest`, PUT three planned management objects at three NEW keys, each after
checking the local file's sha256 against its plan entry, with a `head-object` after. Executor `0.7.0_AE_CloudOps~A`; order
`task-orders/AMGT_RESAPP.TO-AMGT-am-7.the-management-objects-write.md` section 8 (AMENDMENT 3); decomposition s.71. Input: am-2
AMENDMENT 2, drained `af6184d5b0` -- ONE Bloomberg `COMPANY_EXEC_OFFICERS` pull on Andrew's per-use word ~18:1xZ ("thee allow",
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261002_181xZ_ALL_RECS_APPROVED_OPALAI_PUSH_BLOOMBERG_ALLOW_REMOVE_WORKTREE_CLOUD_PULL_PUSH.md`).

## THE KEYS, read live at signing (before-state)

| key (`s3://opal-data-harvest/...`) | sha256 (plan == file) | before | served now (the route's last key) |
|---|---|---|---|
| `management/v1/ASML_NA_Equity/2026-10-02T1840Z.json` | `b0de6e9e4740...` | 404 | `2026-09-18.json` (ABSENT, ZERO_OFFICERS) |
| `management/v1/6501_JP_Equity/2026-10-02T1840Z.json` | `65e746cd7865...` | 404 | `2026-10-02.json` (am-7, ABSENT with its own reason) |
| `management/v1/2317_TT_Equity/2026-10-02T1840Z.json` | `5dd08bdbdec5...` | 404 | `2026-10-02.json` (am-7, ABSENT with its own reason) |

Source files: `deliverables/0.9.0_WK_AMGT_RESAPP~205/m1_pool_a2/<key>`. Plan: `m1_fwd7_plan_a2.json`, sha256
`ca25158b678666379b862074eb173e8b05e7c5ecea3e95641de9a27bcb908557`. The bronze inputs exist:
- `bloomberg/harvest/bronze/exec_officers/security_key=ASML_NA_Equity/20261002T183557Z.json` (860 B, VersionId `aEDGJMx2jp_WEhxR8w6rX9mhHMRkHi02`)
- `.../6501_JP_Equity/20261002T183559Z.json` (4,131 B, `xstn4Uj8JaF3ZWXje0H1dVzk74qmP7mj`)
- `.../2317_TT_Equity/20261002T183600Z.json` (918 B, `d5L3CW59RaTxYwdjSsIsrVFsmz.aYH6V`)

## THE ROUTE'S OWN RULE

`read_pool_object` serves the LAST `.json` key under `management/v1/<key>/` in key order. `2026-10-02T1840Z.json` sorts after
`2026-10-02.json` (`T` follows `.`), so each new key is served on the next request; nothing is overwritten. The body's own `as_of`
stays the date `2026-10-02`, because the schema requires a date; only the key carries the time.

## READERS

Security Analysis, the management panel for ASML NA, 6501 JP and 2317 TT (DEV and PROD).

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| key | what it MAY touch | rollback |
|---|---|---|
| each of the three | one NEW key | management keys are never deleted. Supersede forward: PUT the bytes of the object served before the act (`2026-09-18.json` for ASML, `2026-10-02.json` for the other two) under a newer as_of key, named at that time. |

## EXPECTED OUTCOME -- both branches

- **The PUTs land and serve:** `r63_served.py --cell c2 --where deployed` reads C1 PASS (ASML_NA SERVED, BLOOMBERG_FALLBACK, 7
  officers), C2 PASS for 6501_JP (SERVED, 37 officers) and 2317_TT (SERVED, 8 officers); R63 C2 SERVED: YES. This is read locally
  through the same reader at `af6184d5b0` with `--pool m1_pool_a2`: 3 of 3. Base on deployed at signing: C1 FAIL ABSENT, C2 PASS
  reason-only.
- **Failure branch:** a sha256 mismatch before a PUT is a STOP before writing. If c2 does not read YES after the PUTs, supersede
  forward per the table.

## WHAT THIS HALF DOES NOT COVER

No other key, no S3 delete, no vendor call (the pull is done and landed), no code or function change.
