# AMGT_RESAPP round 77 -- `AMGT-ba-20` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-07 ~04:0xZ

**The act** for `opal-amgt-scoped-api`, under ONE NEVER-2 entry. Executor `0.7.0_AE_CloudOps~A`. Order:
`task-orders/AMGT_RESAPP.TO-AMGT-ba-20.the-code-redeploy.md`. Two legs, in this order:

1. **Code and route leg.** ONE artifact built from a DETACHED worktree at EXACTLY `14a36147bd` (the ba-18 drain; every round-77
   build cell's drain is its ancestor). It is never built "at or after" that commit. Then ONE `safe-apply` on
   `infra/aws/terraform/harvest/`, the plan graded UNTARGETED. It may move exactly:
   - the function's code (its artifact object and hash);
   - ONE gateway route swap: `POST /api/scoped/amgt/refresh` removed and `GET /api/scoped/amgt/resolve` added (the route list in
     `scoped-amgt-api.tf`, edited as text by ba-11 @8c0c6de8c5; the non-greedy route count stays 18).
   Any other resource is a STOP. `memory_size` stays 1769. Then `round71/checks/leadpanel_cold_warm.py --label after` and the cold
   invokes' `AMGT_PHASE` lines, reported and not graded.
2. **Snapshot event.** ONE direct invoke with exactly `{"amgt_scheduled_action": "refresh_freshness_snapshot"}`. Read its stamp.

No grant, no schedule change, no IAM, no memory change, no store write beyond the snapshot the function already writes daily.

## THE BASE, read live at signing (~03:5xZ) -- the rollback per key

| object | value | rollback |
|---|---|---|
| function CodeSha256 | `OVpDhfwDG3BzKE++wDxMlFA6JrwpTnH3FiHC+NrzsrE=` (round 76 az-5, built at `de48559928`), MemorySize 1769, LastModified 2026-10-06T20:10:29Z | the prior artifact through the module, one `safe-apply` |
| the gateway route list | carries `POST /api/scoped/amgt/refresh`; no `/resolve` | the same `safe-apply` at the prior commit restores the list: the route text and the code roll back TOGETHER, never one without the other |
| the /freshness snapshot object | `amgt/harvest/state/freshness_snapshot/current/snapshot.json`, 2,889,391 B, 2026-10-06T20:18:24Z, VersionId `JG_6dEHiqJz..PozaZFTXiUFGezcwPky` | copy-object from that VersionId; NEVER an S3 delete |
| open NEVER-2 entries on this function | none on the shared tree (az-5's closed @cad400c0b3); the executor reads every live worktree | -- |

## THE CONTENT-DIFF, measured by the issuer at signing

A detached worktree at `14a36147bd`, `build-and-upload-scoped-amgt.sh --build-only`, then `content_diff.py --zip` against deployed
`OVpDhfwD`: files 380, IDENTICAL 364, CHANGED 8, ADDED 8, REMOVED 0. Every file is a round-77 cell's; there is no rider from
another project this round.

| class | file | cell |
|---|---|---|
| CHANGED | `lib/research/api/scoped_amgt.py` | ba-11 (the adapter: /refresh out, /resolve in, absent-axis reasons, every hookup) |
| CHANGED | `lib/research/print/render_pack.py` | ba-11 (the text step skipped for the route) and ba-18 (no chart line on an undrafted thesis) |
| CHANGED | `lib/research/api/top_band.py` | ba-8 |
| ADDED | `lib/research/api/name_search.py`, `lib/research/api/translated_text.py` | ba-9, ba-10 |
| ADDED | `lib/research/filings/__init__.py`, `section_coverage.py`, `table_class.py` | ba-7, ba-6 (the filings package enters the artifact for the first time) |
| ADDED | `lib/research/freshness/stale_rule.py`, `page_body.py` | ba-1, ba-2 |
| ADDED | `lib/research/lists/owner_line.py` | ba-3 |
| CHANGED | `lib/research/lists/data/publishers.json`, `social_accounts.json` | ba-3 (owner Andrew, ASSIGNED; two fields each) |
| CHANGED | `lib/research/scores/divergence.py`, `lib/research/scores/peers_v.py` | ba-14, ba-16 (the adapter reads five names from them; the stored score records are not rewritten by this act) |
| CHANGED | `lib/research/harvest/bloomberg.py` | ba-25 (one tuple entry, the `segments` bronze request; no route calls it) |

- **Size:** 255,401,153 B against 262,144,000 B (97.4%, 6,742,847 B spare).
- **VERIFY-SCOPE:** cold-start FATAL [] and request-time break []; 98 of 98 required modules packaged; 18 of 18 data members.
- **Any file outside this table is a STOP.**

## WRITERS OF WHAT MOVES (NEVER-1)

- **The function's code: N = 1 writer,** this act.
- **The gateway route list: N = 1 writer,** this module's route resource, fed by the one list in `scoped-amgt-api.tf`.
- **The snapshot object: N = 1 writer,** `refresh_freshness_snapshot()` in this function, reached by the daily schedule (12:30
  UTC) and this act's one event. The stored snapshot stays the UNANNOTATED view: the stale rule and the lists statement are applied
  at serve time on `?view=page` only (ba-11 hookup 4), so the object's shape does not change.
- **Served bodies, read from the producer's own rule:**
  - `GET /freshness` (no query): unchanged, 302 rows with `reads` (r75 c59 compares it).
  - `GET /freshness?view=page`: NEW. 95 covered rows, each with `stale`, `stale_inputs` and `keyed_date`; no `reads`; the lists
    statement. Local: 66,350 B, 3 stale and 92 not stale.
  - `/overlay`: ADDED `chatter_absent_reason`, `price_absent_reason`, `breakout_price_absent_reason`; `top_band` now shows the
    name's newest news day inside 30 days (local: 57 names with items, 38 with "No news in the last 30 days"; 69 items against 3).
  - `/thesis`: ADDED `passage_coverage`; translation keys on every served sentence (210 of 210 local) and three translated keys on
    the chart; the driver chart and the segment breakdown are REFUSED for a share-capital or one-label table (local: the chart
    served 2 -> 1, ASML NA refused; segment rows served on 12 -> 10 names, ASML NA and PBR refused). This is the one place an
    existing served value changes, and it is the ruled change (CTO ruling 7).
  - `/print`: the body is EQUAL on 3 names (ba-11 AC2); the export prints no chart line on an undrafted thesis (ba-18).
  - `POST /refresh`: 404. `GET /resolve?q=`: 200 with `exact`, `candidates` or `none`; 500 with a plain reason when the name list
    cannot be read.

## EXPECTED OUTCOMES (both branches)

| check | before (OVpDhfwD) | expected after | if not |
|---|---|---|---|
| `r77_deployed.py` (3 lines in `r77_deployed_cells.txt`): `r77_ba11.py --crit AC1 --where deployed` | NO on all five clauses (measured on 5 names) | YES: /refresh 404, /resolve answers, 0 bare axis nulls, every band on the 30-day rule, every served sentence with the translation keys | rollback of the leg |
| ... `r77_served_shape.py --where deployed` | NO (C1, C2, C3, C5, C6 fail; C4, the control, passes) | YES: the page view 95 rows under 150,000 B with one or more rows not stale; the owner line names Andrew; ASML NA refused and BA kept; `passage_coverage` served | rollback of the leg. C3 (the owner line) is the ONE clause never exercised before the deploy: it reads the PACKAGED list files. The issuer exercised the same code against those files placed as the build places them: "Andrew owns the publisher list and the social account list." |
| ... `r77_ba2.py --crit AC3 --where deployed` | YES (a bound) | YES: the default body unchanged | rollback of the leg |
| r76 c62 (the top band) | YES, 3 items | YES, with MORE items: local at `14a36147bd` reads YES with 69 items. ba-8 changed which day the band shows, not the clauses c62 grades | a NO is a rollback trigger |
| r76 c63, r75 c59 (40-wide burst), r75 c57 / c58 / c61, r74 c53 / c55 / c56, r71 c38 | YES each | YES each (no regression). c61 grades segment headings over 95 names: a refused breakdown serves no rows and so no heading | rollback of the leg; a c59 that reads UNMEASURED (exit 2) is reported, not a rollback |
| new CodeSha256 | `OVpDhfwD...` | differs AND equals the artifact built at `14a36147bd` | an unchanged hash is a 0-diff deploy: STOP |
| the plan | -- | exactly: the function's code, one route removed, one route added | any other resource: STOP before the apply |
| cold chatter read (leadpanel `after`) | cold Duration 2,580-3,137 ms | reported; ba-11 and the round's cells do not touch the chatter phases | not a rollback |

**Measured locally on the merged tree before signing** (the handler in-process, the same code the artifact carries): r76 c62 YES
(69 items) and c63 YES; r75 c57, c58 and c61 YES; `r77_ba11` AC1 YES on five of five clauses over 95 names; `r77_served_shape`
YES with its owner clause skipped; the api, print, identity, filings, freshness and lists suites 1,294 passed. r75 c59, r74
c53/c55/c56 and r71 c38 have no local arm that predicts the deployed read and were not run.

**Not proven by this act, stated so it is not assumed:** the gateway route itself. Every check above invokes the function
DIRECTLY, so `/resolve` through the gateway (the edge, the authorizer) is first exercised by the page or by the walk (ba-24).

## SIGNED

`2.0.0_SA_COO~Z`, 2026-10-07 ~04:0xZ. The CTO half is owed by `1.0.0_SA_CTO~Z`.
