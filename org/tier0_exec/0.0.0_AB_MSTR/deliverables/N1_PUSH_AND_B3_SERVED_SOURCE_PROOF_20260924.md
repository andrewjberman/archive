# N1 push receipt and the B3 served-source proof -- 2026-09-24

**Seat:** 0.0.0_AB_MSTR (laptop). **Routed by:** 1.0.0_SA_CTO msg 100773 (N1 plus B3). **Push word:** Andrew-direct
~17:5xZ "Push it" (`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260924_175xZ_PUSH_N1_APPROVED.md`).

## 1. The push

- origin/CLOUD `bb2a7a3df1..8a29069dea`, fast-forward (ls-remote read `8a29069dea`). It carries the N1 drains: ~P
  `c6d8b9b2bd`, ~Y `d8212ee82c`, ~M `14cbdd190b`.
- The pre-push gate did exactly what the approval named, and nothing else. Measured beforehand with a no-write run of
  `safe_deploy_core`'s own resolvers ("2 of 18 routed objects would change"), then read back afterwards:

| served key (opal-data-mdpf) | before (rollback VersionId) | after (VersionId) | proof |
|---|---|---|---|
| `code/scripts/assets_gold/investor_reporting/investor-reporting.tar.gz` | `Ku6.brgEK.LYO6RIqzXSNdyAM9j_NsCX` (md5 59692b17...) | `gBI4hCWQalYQZcw2IWK6sDCD_gDgPYO7` (md5 dd6eab85...) | 10 of 10 served members == the committed blob at HEAD; exactly 2 changed vs rollback: `holdings_snapshot.py`, `HoldingsSnapshot.schema.json` |
| `code/scripts/gold/taxsma_membership.py` | `GMs.xhrRBXWFpnU56ab8HEUINLxV7ab5` (md5 6375ddd4...) | `2DooKbHkaKS6WFbEVn9F5ATYpcg0O_Zn` (md5 0c6da86f...) | served md5 == the committed blob |

- 16 other routed files were SKIP-NOT-MEMBER (404), so nothing was minted for them.
- 2.0.0_SA_COO~M's CRLF precondition (msg 100806: the bundle mints from working-tree bytes) arrived about a minute
  before the push. The served content settles it: every member equals its committed blob, so no CRLF bytes shipped.
- Rollback: restore each key's "before" VersionId.

## 2. B3 -- is every served IRPT function's source in CLOUD? (measured at cc08346eb0, before this push)

Instrument: a read-only agent. Deployed zips came from `lambda get-function`, and the mapping from
`infra/aws/lambda/ci/lambda-source-map.json`. Bytes were compared by sha256, with a CRLF-normalized second pass. A
control showed the compare reports DIFFER on an older commit. Artifacts are in this seat's session scratchpad
(`b3/`: zips, rows.json, compare.py, control.py).

- **Denominators:** 9 functions deployed and 9 declared in Terraform (the yang-lambda module), with no mismatch. Every
  build-map zip hash equals the deployed CodeSha256. Every function serves `$LATEST` only.
- **334 project files compared:** 270 match at the path, 40 match after CRLF->LF, 15 match at the build map's pinned
  commit, 9 are found only in history, and 0 are absent from the repo.
- **VERDICT: NO.** Three gaps:
  1. **export-render and narrative:** the served `_authz/{enforce,loaders,served}.py` and `_scope/resolve.py` are
     byte-equal to commit `385aff4646` (09-21). The CLOUD build map pins `bc3727b3a3`, whose files differ, while still
     recording the served zip hash. A rebuild from CLOUD would change what these two functions serve.
  2. **intake-poller:** the build path `intake/firm_registry.json` does not exist in CLOUD. The served file equals
     `data/firm_registry.json` at `1f54e16dfd` after CRLF->LF.
  3. **CRLF:** 40 served files were built from a CRLF working copy.
- **Closed by this push:** 8 pinned commits (`bc3727b3a3`, `9cf6a63d6f`, `19d1c3b387`, `c76b7c7aee`, `7a8d2a4ca3`,
  `896680c2de`, `0879affa62`, `c3add4090e`) were reachable only through the held drains. They are now on origin.
- **UNMEASURED:** a byte-for-byte rebuild of the generated `bd_helpers.py` in irpt-common:5 (its manifest hash matches);
  the external performance native layer; API Gateway integration targets.
