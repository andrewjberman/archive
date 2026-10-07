# AMGT_RESAPP round 77 -- GROUP C draft notes (a fork of 2.0.0_SA_COO~Z, 2026-10-07 ~00:4xZ)

Drafts only. Nothing here is committed, and no existing file was edited. The issuer assembles section 85 and makes the ONE
issuance commit. Base: the shared tree at the cut; deployed function `opal-amgt-scoped-api` CodeSha256 OVpDhfwD.

## Cells

| id | title | slot | wave | class | risk | consumes |
|---|---|---|---|---|---|---|
| AMGT-ba-8 | the top band's newest news day inside 30 days (ruling 5, Z-W263-S1) | ~274 | 0 | worker | LOCAL | nothing |
| AMGT-ba-9 | the name-search resolver (Z-S228) | ~275 | 0 | worker | LOCAL | nothing (reads the crosswalk) |
| AMGT-ba-10 | the translated text on a served sentence (Z-S221) | ~276 | 0 | worker | LOCAL | nothing |
| AMGT-ba-12 | the batched repairs (Z-C-S35, Z-W7-S7, Z-S343, Z-W88-S1, Z-C-S372, Z-W19-S16) | ~278 | 0 | worker-light | LOCAL | nothing |
| AMGT-ba-11 | the adapter cell: /refresh removed, absent-axis reasons, the print text step, every hookup | ~277 | 1 | worker | LOCAL (see open question 1) | every wave-0 cell's module |
| AMGT-ba-13 | no production read of a worker folder (Z-W37-S2) | ~279 | 2 | worker | LOCAL | every other cell's drained files |

## Write sets

- ba-8: `lib/research/api/top_band.py`, `lib/research/api/tests/test_top_band_provenance.py`
- ba-9: `lib/research/api/name_search.py` (new), `lib/research/api/tests/test_name_search.py` (new)
- ba-10: `lib/research/api/translated_text.py` (new), `lib/research/api/tests/test_translated_text.py` (new)
- ba-12: `lib/research/watchlist/tests/`, `lib/research/harvest/test_am1_marker_once.py`, `test_al2_content_key.py`,
  `test_ba12_serp_single_page.py` (new, if needed), `lib/research/harvest/tests/`, `lib/research/harvest/bright_data_serp.py`,
  `lib/research/management/tests/test_ceo_search.py`
- ba-11: `lib/research/api/scoped_amgt.py`, `lib/research/print/render_pack.py` (ONLY `build_pack`'s signature and its pypdf
  text step, lines 631 and about 750-758), `lib/research/print/tests/test_ba11_skip_text_step.py` (new),
  `lib/research/api/tests/`, `infra/aws/terraform/harvest/scoped-amgt-api.tf` (the route list text)
- ba-13: twelve package directories under `lib/research/` (identity, coverage, drafting, social, freshness, metrics, peers,
  posture, provenance, price, rules, lists) and the two packaging scripts under `infra/aws/terraform/harvest/`

Every cell also has its own deliverables directory and the investigation file.

## Hookups ba-11 carries from this group

1. ba-8: `_overlay_top_band` (scoped_amgt.py about :3295) calls `top_band.news_items_newest(rows, asked)` in place of
   `prev_trading_day` + `news_items(rows, day)`.
2. ba-9: a new handler branch `GET {prefix}/resolve?q=` beside `/freshness` and `/lists` (about :6903) answering
   `name_search.resolve_query(q)`; `"GET  {0}/resolve"` in `scoped_amgt_route_table()`; and in `scoped-amgt-api.tf:548`
   `"POST /api/scoped/amgt/refresh"` becomes `"GET /api/scoped/amgt/resolve"` (the non-greedy count stays 18).
3. ba-10: merge `translated_text.served_translation(sentence)` into each served sentence dict (about :2962-2970; ba-10's
   report lists the rest).

The order's hookup section ends with the literal token HOOKUP_LIST_AT_CUT for the other groups' hookups.

## Checks, dry-run at the base

| check | base |
|---|---|
| ba-8 AC1 (r77_ba8.py) | FAIL as expected (`news_items_newest` absent) |
| ba-8 AC2 (r77_ba8.py) | PASS as expected (23 passed) |
| ba-9 AC1 (r77_ba9.py) | FAIL as expected (no module) |
| ba-9 AC2 (r77_ba9.py) | FAIL as expected (no test file) |
| ba-10 AC1 (r77_ba10.py) | FAIL as expected (no module) |
| ba-10 AC2 (r77_ba10.py) | FAIL as expected (no test file) |
| ba-11 AC1 (r77_ba11.py, local, 7 min 55 s) | FAIL as expected on C1-C5: /refresh 200 and listed; /resolve 404; 95 bare axis nulls over 95 names; 95 of 95 bands on the old rule; 0 of 210 served sentences with the keys |
| ba-11 AC2 (worker's print_equal.py) | absent at the base: FAIL as expected (not dry-runnable) |
| ba-11 AC3 (r77_ba11.py) | PASS as expected (mount test, 6 passed) |
| ba-12 AC1 (r77_ba12.py) | FAIL as expected (3 of 5 socket-blocked) |
| ba-12 AC2 (r77_ba12.py, 5 s) | FAIL as expected (10 failed, 143 passed) |
| ba-12 AC3 (r77_ba12.py) | FAIL as expected (the store is touched before any refusal); control C2 PASS |
| ba-13 AC1 (r77_ba13.py) | FAIL as expected (19 files / 44 lines under lib/; 3 packaging lines); control C3 PASS (5 files) |
| ba-13 AC2 (worker's equal_reads.py) | absent at the base: FAIL as expected (not dry-runnable) |

## Scope changes inside the group

- ba-12 item 4: the adjudication calls Z-W19-S16's rows "legacy price rows". The row's own text says they are the 10 rows of
  the CHATTER partition `TRENDING_CHATTER#2026-09-15` in `opal-harvest-security-metrics`. The face follows the row.
- ba-13: the row's "24 files" was a walk over lib/, integrations/ and infra/. At the cut: 19 under lib/, 5 under
  integrations/bloomberg/ (untouched; a control), and 2 packaging scripts (added to the cell, because a moved file must be
  packaged from its new home). Worker-folder files are COPIED, never moved, because `integrations/bloomberg/research/
  price_axis_pull.py` still reads `~4/universe.json`.
- ba-11: the route swap is carried as text in `scoped-amgt-api.tf`, because the mount test compares the adapter's table with
  that list. Applying it is the redeploy order's act.

## Open questions for the issuer

1. GATE (xii) may put a floor above LOCAL on ba-11 for its `infra/` path (and on ba-13 for its two). If it refuses, either raise
   the class or move the `.tf` line to the redeploy order and accept the mount test reading red in ba-11's tree until then.
2. The round's redeploy is NOT code-only: one gateway route is removed and one added. Its pair must name both.
3. ba-13 changes what the Lambda package reads from. It should land after this round's redeploy, or ride a later one with its
   own content-diff.
4. `render_pack.py` is shared in time, not in a wave: group D's export chart line (wave 0) and ba-11's text step (wave 1).
5. The portal client still calls `POST /refresh` (`portal/src/api/endpoints/amgt*.ts`, about line 132). Removing that call and
   its control is page work for the DSGN lane.
