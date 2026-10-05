# AMGT_RESAPP round 71 -- `AMGT-au-7` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-05 ~18:2xZ

**The act (ONE leg, code only):** for `opal-amgt-scoped-api`, ONE artifact at build commit `a53eaf74c5` (or a descendant whose
CONTENT-DIFF against the DEPLOYED build equals the list below), then ONE code-only `safe-apply`. `memory_size` stays 1769.

- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-au-7.the-code-redeploy.md`, with AMENDMENT 1 (the gold leg leaves this act).
- It carries:
  - au-4 @18931420f3, `/freshness` covering every name;
  - au-1 @40dcc8b342, `score_unit`;
  - au-6 @066bbc25d2, the Lead Panel per-container memos;
  - au-3 @69c017d520, the feed `url` / `url_reason` route and the gold producer's `url` column. The producer code is packaged but
    never called by this function.

## THE BASE, read live at signing (18:16:47Z) -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `GS//XHnVd4+bBIg1VU++r1fp9v495pi6jKFat9KbEYE=` (round 70 at-6) |
| function MemorySize | 1769 |
| LastModified | 2026-10-05T08:23:19Z |
| open NEVER-2 entries on this function | none (`org/critical_paths/.open_deploys/` read 18:16Z) |

**Rollback:** the prior artifact version (the one at-6 uploaded, which the executor reads from the artifact object's version list
before the upload) through ONE code-only `safe-apply`. Then a re-read of CodeSha256 equal to `GS//XHnV...`.

## THE CONTENT-DIFF, measured by the issuer at signing

The build is a detached worktree at `a53eaf74c5`, run as `build-and-upload-scoped-amgt.sh --build-only`, then `content_diff.py --zip`
against the deployed `GS//XHnV`.

| class | files |
|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py`, `lib/research/harvest/publication_gold.py` |
| ADDED | `lib/research/api/served_cache.py` |
| REMOVED | none |
| IDENTICAL | 361 of 364 |

- **Size:** package 132,180,078 B over 364 entries, plus layer `opal-amgt-print-deps:1` at 121,743,633 B, totals 253,923,711 B
  against the 262,144,000 B ceiling (96.9%, 8,220,289 B spare). Zipped 41,214,968 B.
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break []. The isolated runtime is OK.
- **Any other changed, added or removed file is a STOP.**

## NEW S3 READ PATHS (CTO round-67 ruling 4)

**None.**
- au-1 adds a constant field.
- au-4 reads `covered_security_keys()`, which is already read by the deployed function.
- au-6 reads the same tables and prefixes; worker report: "NEW S3 READ PATH: none".
- au-3's route reads `url` from the gold mention rows it already reads.

The gold producer's `write_gold` is not on any request path of this function. No simulate arm is owed. The executor confirms the
role policy is unchanged in the plan; any IAM change in the plan is a STOP.

## WRITERS OF WHAT MOVES (NEVER-1: N writers = N rules)

- **The function's code: N = 1 writer**, this act. Two projects deploy this function (AMGT_RESAPP, DSGN via RESAPP); none is open.
- **The gold mention table (`article_security_mention`): N = 1 writer, AMGT_HARVST's hand-run gold build** from CLOUD HEAD under
  its own signing pair (COO~H msgs 29674, 29747). It is NOT moved by this act; AMENDMENT 1 takes the gold leg out of au-7.

## EXPECTED OUTCOMES, read from the producers' own rules

| check | before (deployed `GS//XHnV`) | expected after |
|---|---|---|
| r71 c34, score_unit | 572 of 572 failing | 0 failing |
| r71 c36, /freshness | 42 of 95 covered missing | 0 missing; a no-read name has dates null + reason |
| r71 c38, Lead Panel, warm, deployed | 9 of 9 over 2,000 ms (chatter 9.4-11.0 s, price 3.7-4.9 s) | under 2,000 ms warm on all 9 |
| r71 c35, feed url | 600 of 600 without a url or reason | **NOT graded at this act.** ft and wsj items already serve `url_reason` (route rule); bbg/barrons/sa urls appear only after HARVST's next gold build. Graded at the issuer's close read after that build. |

**BOTH BRANCHES of c38.**
- **Warm reads under 2,000 ms:** LANDED.
- **Any read over the bar:** NOT a rollback trigger by itself. au-6 changes no value (EQUAL 9 of 9), so a slow-but-correct
  function is no worse than the base. The executor reports the per-read times. The issuer files the gap as the round-72 producer
  item (row Z-W236-S1).

**Rollback triggers:** AC1 (c34/c36) or the AC3 regression set failing; a CodeSha256 other than the build's.

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-05 ~18:2xZ. The CTO half is owed at `ledger/NEVER_WIDEN_ROUND71_AU7_CTO_HALF.md`.
