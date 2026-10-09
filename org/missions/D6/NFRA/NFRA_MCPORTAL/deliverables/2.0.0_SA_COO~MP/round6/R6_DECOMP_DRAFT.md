# NFRA_MCPORTAL -- ROUND 6 DECOMPOSITION DRAFT (FWD-15, FWD-16, FWD-17) -- 2.0.0_SA_COO~MP, 2026-10-09 ~05:1xZ

**Status: DRAFT, not a decomposition.**
- Nothing is issued from this file.
- Round 6 is cut only from the CTO's round-5 analysis, after FWD-14 grades REALIZED (ROUND_ANALYSIS.round4.md @460bc0af2f,
  section 5, "subtracted").
- This file exists so the cut is immediate when that lands. It is written while MP-x-4 waits on NFRA_OPLGTW r29
  (`/next-calls --drive`, WHILE BLOCKED).

## The constraint every FWD-15 to FWD-17 cell meets

PRD C3 serves the pages from the gateway process. The gateway host carries `app/` and the instance role. It holds no
workspace checkout, no git and no box's working tree. Its only fabric data is the S3 read granted by MP-x-3 (live):
`fabric/activity/v1/` and `fabric/open-calls/v1/`. Every source a cell needs must therefore be either IN those two prefixes
or a new published record. Three outcomes need a source the PRD names but the gateway cannot read today.

## Q1 -- FWD-15: where does "a deploy is open on this surface" come from? (C13)

C13 rates an overlap by surface kind AND "whether `org/critical_paths/.open_deploys/` on any box names that surface".
Those sentinels are repo files on each box. The activity store records the commits that touch them, but as a file list,
with no add-versus-delete. So "open now" is not readable from it as written.
- **(a) Rec:** each box publishes its open-deploy sentinel list beside its open-calls copy
  (`fabric/open-calls/v1/box=<box>/open_deploys.json`, the same writer pattern, written when `deploy_ledger.py`
  opens or closes an entry). This stays inside the granted prefix, so no IAM change.
- **(b)** Infer "open" from the activity records, as the last touch of a sentinel path being an add. It is weaker, and C14
  forbids guessing.
- **(c)** Rate on kind alone, and show the deploy column as "not recorded" (the C14 pattern) until a record exists.

## Q2 -- FWD-16: where do "pushed to its box branch" and "on the trunk" come from? (C14)

C14 reads `origin/box/*` and integration records. The gateway cannot run git.
- **(a) Rec:** each box's scheduled `.tools/box-sync.sh` writes one small state record per run into the activity store
  (`fabric/activity/v1/gitstate/box=<box>/<stamp>.json`: branch head, trunk head, pushed and merged shas, refusal count).
  It is owned by GitOps (`4.0.0_SA_CRO~A`, C14 already places push and fetch events there), and the gateway reads it under
  the existing grant.
- **(b)** The gateway reads GitHub's API for branch heads (egress is now open). That adds a token and a second source.

## Q3 -- FWD-17: how does a close from the page reach the open-calls writer? (C11)

C11: "the close ... goes through the open-calls writer and never edits the file". The writer, `.tools/open-calls.py close`,
runs on a box against that box's repo list. The gateway cannot run it.
- **(a) Rec:** the page writes a close REQUEST object
  (`fabric/open-calls/v1/box=<box>/requests/<id>.json`: id, ruling text, ruled_by=andrew, the owner-verified header claims).
  The box's 10-minute open-calls scan applies it through `open-calls.py close --ruled-by andrew` and the writer republishes.
  This needs one narrow `s3:PutObject` on `requests/` only: a never-widen grant, with a C10 ledger.
- **(b)** A small Lambda performs the close. Rejected: the list's one writer is the box, so a second writer breaks that.

## Draft cells (shape only, assuming the recommendations; re-cut against the analysis)

| Cell | FWD | Builds | Risk |
|---|---|---|---|
| MP-o-1 | 15 | `app/refs/overlap_rules.json` (C13: kinds Terraform > code > registry > tool > record, and the open-deploy uplift), `GET /api/admin/fabric/overlap`, tests with a planted Terraform overlap rated above a planted shared-log overlap (A15) | WORLD (lives through a release) |
| MP-o-2 | 15 | publisher: `deploy_ledger.py` open and close put `open_deploys.json` per box (if Q1 = a) | WORLD |
| MP-g-1 | 16 | `GET /api/admin/fabric/gitstate` over the gitstate records; "not recorded" for a box with none (A16) | WORLD |
| MP-g-2 | 16 | box-sync writes the gitstate record (if Q2 = a); GitOps-owned, so possibly a cross-project cell | WORLD |
| MP-k-1 | 17 | `GET /api/admin/fabric/calls` (every box's cloud copy, ABSENT is never empty) + `POST .../close` writing a request (if Q3 = a) | WORLD |
| MP-k-2 | 17 | the scan applies close requests through the writer; the never-widen PutObject grant on `requests/` only | WORLD |
| MP-p-2 | 15-17 | the page's three new panels under Control Plane, refreshing while open (the C12 ruling) | WORLD |
| MP-r-2 | 15-17 | one release, applier `0.7.0_AE_CloudOps~MP`, on the then-live base | WORLD |

The close run (`A15`, `A16`, `A17` on the page, with Andrew's one close as the JUDGMENT criterion) follows the release.
