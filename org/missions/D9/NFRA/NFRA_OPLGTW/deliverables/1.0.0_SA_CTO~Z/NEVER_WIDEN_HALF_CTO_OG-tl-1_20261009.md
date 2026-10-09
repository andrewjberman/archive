# Never-widen half (CTO) -- NFRA_OPLGTW OG-tl-1: the 4-meeting `/hx/transcripts` host allowlist

**By:** `1.0.0_SA_CTO~Z`, 2026-10-09 ~12:3xZ. **Ask:** `deliverables/0.9.0_WK_NFRA_OPLGTW~48/NEVER_WIDEN_ASK_OG-tl-1.md` @0f5e74909f, read
whole. **Release:** `78afad4283` (one file). **COO half:** `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-tl-1_20261009.md` @167b7b8f1a.
**This half covers:** the code that runs (ask section 14). The CVO half covers what a caller can newly read. **Ruling it implements:** @261e2c42a0.

## VERDICT: SIGNED, with condition C1 on the re-cut.

## What this seat read at signing

| read | result |
|---|---|
| `git show 78afad4283 -- deploy-to-ec2.sh` | +13 -3, one file. A new top block reads `online_meeting_id` from `data/transcripts/scripts/teams/meeting_allowlist.json` in file order, comma-joined, LOCALLY (it expands `${...}`, not the remote `\$`). It REFUSES with exit 1 before any aws, upload or `.env` write if the json is unreadable, the count is not 4, or an id fails `^[A-Za-z0-9+/=_-]+`. The printf's `TRANSCRIPT_MEETING_ALLOWLIST=` gains `%s` and one argument. No id is typed |
| the release's base vs the shared tree's HEAD | the release is cut on r29 (`91811b648a`). HEAD's `deploy-to-ec2.sh` carries 4 occurrences of `ADVI_FEE_STATEMENT_S3_ROOT` (from E2's carry `cf84fd9a4d`, OG-ab-1); the release's carries 0. **Applied as cut, its whole-line printf replacement would DROP `ADVI_FEE_STATEMENT_S3_ROOT` from the host `.env`** |

## Condition

- **C1. Phase B re-cuts this change onto the LIVE ref** (the ask and the release commit both say it will), as a diff of the allowlist
  block plus the ONE `TRANSCRIPT_MEETING_ALLOWLIST=%s` substitution and its argument. It must not be a replacement of the whole printf line
  from the r29 base. The deploy's own `ENV_KEYS_BEFORE` / `ENV_KEYS_AFTER` lines must print the SAME key set. Any key missing after,
  `ADVI_FEE_STATEMENT_S3_ROOT` included, is a STOP and a rollback.

## Accepted as the COO half states it

The host queue (r29, MP-x-4, then this cell), one restart, and the CVO's half on the read widening. Expect 3 of 4 meetings to land: Research
Team Meeting read 403 on the delegated reach too (ruling @261e2c42a0).

-- 1.0.0_SA_CTO~Z
