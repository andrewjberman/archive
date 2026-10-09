# LGIC_ENFORCE EN-z-1 -- live-plane census, round 20

Report: `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NAMING_CENSUS_REPORT.r20.md` (vintage: Built from the estate as of 2026-10-09 12:52:02 UTC. Stitch source: stitch-codebuild built 2026-10-09T03:01:16Z). Run to `CENSUS: COMPLETE 3578 judged + 483 carded`. `census --all-roots` rc 0.

## Live totals beside stored-code totals

| | Live plane (`comp-find --corpus aws`) | Repo plane (names in code, `census --repo`) |
|---|---|---|
| Denominator | 2457 nodes scanned | 2016 names |
| Out of scope / not nameable | 396 of NOT-GRADED types + 16 aws-fixed = 412 | n/a |
| Nameable | 2045 | 2016 |
| Judged | 1906 | 1672 |
| Carded (not judged, R-29) | 139 | 344 |
| Judged + carded = nameable | 2045 | 2016 |

Verdicts (judged rows): live CONFORMANT 425, OUT-OF-PATTERN 1317, ALIAS 29, NO-SYSTEM-ASKED 135; repo CONFORMANT 453, OUT-OF-PATTERN 968, ALIAS 121, NO-SYSTEM-ASKED 124, NOT-GRADED 6.

Stored-code check beside it (`census --all-roots`, every Terraform root): `ALL-ROOTS ok=True roots_total=86 mapped=86 unmapped=0 completed=86 stopped=0 items=2601 right=669 fix=1618 not_asked=268 pattern=39 carded=0 refused=0 hole=7 carded_class_holes=0 source_bucket_holes=0 event_rule_holes=0 unknown_word_holes=1 other_holes=6 stale_hints=0 uncounted=1 counted_at_caller=17`

Round 13 carried 462 cards (131 live, 331 repo; its census counted 131 live and 332 repo items carded). This run carries those 462 verbatim plus 16 new cards (8 live, 8 repo), and counts 483 items carded: live 139, repo 344 (a card holds every site of its name, so items exceed cards).

## New cards by owner

| Owner | Cards | Names |
|---|---|---|
| 0.7.0_AE_CloudOps | 1 | `restricted-prefix-get-put-list` (repo) |
| 2.0.0_SA_COO (D0, system sprint) | 1 | `%s%s/` (repo) |
| 2.0.0_SA_COO (D9 IRPT) | 5 | `firms/{firm}/generations/{export_id}/receipt.json` (repo); `firms/` (repo); `calculated-group` (repo); `_status/lots_not_computed.json` (repo); `bbg/` (repo) |
| 2.0.0_SA_COO (D9 IRPT, project IRPT_YCDGEN) | 1 | `astn/kimi/api-key` (repo) |
| 4.0.0_SA_CRO | 8 | `ldo001-2c1d64dae3b4-expire` (live); `ldo001-360ca30f109a-expire` (live); `ldo001-617eec392d89-expire` (live); `ldo001-792eb59e6d0d-expire` (live); `ldo001-d77c7b300917-expire` (live); `dowjones/barrons/session` (live); `dowjones/wsj/session` (live); `ocilar/credentials` (live) |

Every new card was re-derived from a real RAISE at this run (17 RAISE sites, 16 distinct (plane, name) cards; `astn/kimi/api-key` is one card for two sites). Three of the repo names (`restricted-prefix-get-put-list`, `calculated-group`, `astn/kimi/api-key`) already have rows in `infra/logic/registry/name_rulings.json`, which `grade()` does not consult; the cards say so.
