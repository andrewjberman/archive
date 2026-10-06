# OG-ga-1 PHASE A preflight (0.9.0_WK_NFRA_OPLGTW~28, 2026-10-06)

- Before-record: `GA1_BEFORE.json` -- 1 in-force active dim_asset grant, 0 carrying `download_filtered`; revision 2, operations `describe, list, query`; 0 other principals in force.
- Operator identity: `sts assume-role` on `opal-gateway-access-admin` succeeded; `get-caller-identity` names `assumed-role/opal-gateway-access-admin/wk28-ga1`. Credentials held in the child process environment only.
- Candidate/rollback: written to the off-repo directory X only (`candidate.json`, `rollback.json`; they carry tid/oid/email).
- Scope diff (in-process `prepare()` under the operator role, nothing written): 8 lines, saved in X (`diff.txt`; it names the granted account ids as dict keys, so it stays off-repo).
  Changed-key list: `operations` only -- `{'added': ['download_filtered'], 'removed': []}`. Every other dimension (masters, datasets, accounts, columns, dates, portal_channels) added=[] removed=[].
  The stored grant scope equals the re-shaped current scope (round-trip check: True).
- Pre-write download probe (SSM `4a44eb6d-be2e-43e8-96f6-075aa94303a4`, status Success, host i-07dccb1615503ac99, real holder read from the store through `app/data_entitlement`, HybridStore: POLICY# reads real, everything else in memory):

  `dim_asset_download: REFUSED ENTITLEMENT_DENIED entitlement_denied`

  Full output: `GA1_PROBE_BEFORE.out`. Probe `synthetic_principal false`, `grant_source store`, `grants_written 0`.
