# AMGT_RESAPP round 62 -- `AMGT-al-1` act (B) never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~11:3xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at the build commit the GO names (the al-2 commit, or a descendant whose CONTENT-DIFF
equals the list below). Build and upload ONE artifact, then ONE code-only `safe-apply`; `memory_size` stays 10240. Executor
`0.7.0_AE_CloudOps~A`; order `task-orders/AMGT_RESAPP.TO-AMGT-al-1.the-memory-raise.md` section 6 (AMENDMENT 1); decomposition s.70f;
CTO ruling 5a @e041af6102. **Freeze:** deployed AND graded by 12:30Z, or it waits for Andrew's read.

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `E+FAZF0f63S5LxRWs4l3mCfOZgKc3erezTkjxCoVcBY=` (ak-2, 07:45:38Z) |
| function MemorySize | 10240 (al-1 act (A), 10:55Z) |
| artifact S3 VersionId | `YSqlUTOWHwV6H7LePjd1pr9DKomiDo5U` (LastModified 2026-10-02T07:40:52Z, 41,117,744 B) |

## WRITERS OF THE PROPERTY: 2 seats, 1 path

`build-and-upload-scoped-amgt.sh` plus a code-only `safe-apply`. The seats are AMGT_RESAPP (this act) and AMGT_HARVST, which has no
redeploy of this function in flight at signing; the CTO ruling holds every other deploy to this function from 12:30Z.

## THE FILE LIST (`--build-only` at the al-2 tree, rc=0: VERIFY missing [], isolated runtime 3 of 3 arms)

`CONTENT-DIFF SUMMARY: files 350, IDENTICAL 349, CHANGED 1, ADDED 0, REMOVED 0` against `E+FAZF0f...`:

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | al-2 | `/security/{key}/timeline/day/{date}` only. The silver headline read is bounded at 18 s from handler start. On the deadline every mention is served with `headline` null, and the body gains ONE top-level `headline_reason` (a plain sentence); status 200. A read inside the deadline serves the same bytes as today. A read FAILURE is classified exactly as before. No other route changes. |

Any other changed file at build time is a STOP.

## READERS

The Security Analysis timeline's day dissection (DEV and PROD): it lists the articles, with headlines when the read finishes inside 18 s.
The page must tolerate a null headline (`ARTICLE_FIELDS` already allows it: `headline` comes from a join that can miss). The new
top-level `headline_reason` is ignored by a page that does not read it.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId above |
| code-only `safe-apply` | the function's code (source hash) only; `memory_size` stays 10240 | a code-only `safe-apply` with `YSqlUTOWHwV6H7LePjd1pr9DKomiDo5U`, restoring `E+FAZF0f...` |

## EXPECTED OUTCOME -- both branches, read from the code's own rule

- **The silver read finishes inside 18 s** (warm, or a fast cold day): the body is byte-equal to today's. The two controls (BA 2026-09-30,
  2026-10-01, graded on the warm second call) read `6c25fff80da9be93` and `69ecb7a884a83585`.
- **The read runs past 18 s** (a cold BA 2026-09-08 sandbox; cold runs at 10240 took 16.6-19.1 s, so some will): 200 at about 18 s,
  headlines null, `headline_reason` present. The read keeps running on its one worker and fills the process cache, so the next call on
  that sandbox serves headlines.
- **Failure branch:** a non-200 on any of the 3 cold BA runs, or a control whose bytes moved -> ROLLBACK per the table.

## WHAT THIS HALF DOES NOT COVER

No memory change, no store write, no S3 delete, no vendor call, no IAM, route or gateway change: any of these in the plan is a STOP.
