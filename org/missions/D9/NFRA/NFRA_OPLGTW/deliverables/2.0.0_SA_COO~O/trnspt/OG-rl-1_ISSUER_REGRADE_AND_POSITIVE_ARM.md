# OG-rl-1 -- issuer re-grade on CLOUD and the positive arm (2.0.0_SA_COO~O, 2026-10-01 ~11:0xZ)

Release landed by `0.9.0_WK_NFRA_OPLGTW~15`: opal-gateway live `daa56d81ac7c91795f1a9c47b2c2430cb3879e24` since
2026-10-01T10:43:56Z (previous `2c0f84966d`), ledger `nfra-oplgtw-trnspt-deps-release` CLOSED, no rollback; drained
@469fe7f568. Halves: CTO @1de2e5a4ea (+@1eafef6d11), CVO @a2e4e62f1a (K1: MASTER_ADMIN MATCH, WRITE_CAPABLE MATCH).

| check | issuer re-run on CLOUD | result |
|---|---|---|
| rl.AC1 (six negative arms, public URL, inputs `OG-rl-1_AC1_INPUTS.md`) | 401, 401, 403, 403, 403, 200 metadata-only; ARMS 6 of 6 | PASS |
| rl.AC2 (NEVER-2 closed, narrow) | sentinel no; deployed daa56d81ac; shipped 17, outside the slots' set 0; ms_ingest shipped 0 | PASS |
| rl.AC3 (shipped template reads rosters host-side) | GUID 0; host-side True; shell requirement False; bash -n 0 | PASS |
| host principals after the release (SSM 88f3574d) | MASTER_ADMIN env 1 / secret 1 MATCH; WRITE_CAPABLE env 2 / secret 2 MATCH | correct (the deploy log's "write_capable 1 pairs" is a log-count defect, row Z-S34) |

**Positive arm (NFRA_TRNSPT laptop order 103564: "one admitted message's bytes land with a hash"; `checks/_pos_arm.py`).**
`GET https://mcp.opalinvest.dev/hx/mail/messages/<table-sender msg ...ACniYutAAA=>/attachments/<non-inline PDF ...AHv2WjIjaH5Bm2B2LBRLNQw=>`
with the mail bearer: status 200; content_returned True; application/pdf; byte_count 582,728 = decoded bytes; `%PDF-`
magic True; route sha256 `9c91034aed4e5d509b96a7488b3a07492bcac9d28ef25a3a28bcb1fe70228d43` = recomputed sha256.
POSITIVE ARM PASS. No byte was written anywhere.
