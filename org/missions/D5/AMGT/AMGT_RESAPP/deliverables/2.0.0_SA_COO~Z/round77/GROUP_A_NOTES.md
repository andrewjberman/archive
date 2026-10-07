# AMGT_RESAPP round 77 -- GROUP A draft notes (ba-1..ba-4), for the issuer's section 85

Drafted 2026-10-07 ~00:5xZ from `ledger/ROUND_ANALYSIS.round76.md` @c8bbeeac10. Nothing here is committed by the drafter.

## Measured at the cut (deployed `opal-amgt-scoped-api` OVpDhfwD, one GET-shaped invoke of /freshness)

- Body 2,889,557 B decoded. Top-level: `reads` 2,758,266 B (95.5%), `rows` 130,333 B, `denominators` 573, `snapshot` 152,
  `rot` 134, `generated_at` 19.
- Inside `reads`: `seeking_alpha_bronze` 2,139,211 B, `bloomberg_bronze` 611,254 B, `packs` 6,617, `lists` 408,
  `universe` 400, `bright_data_serp` 270.
- Rows 302, covered 95. Covered rows 43,965 B; the 207 others 85,764 B. Largest row field: `rot` 42,582 B (one identical
  sentence on all 302 rows).
- The analysis says "242 keys"; the route returns 302 rows. ba-2 restates the count.
- Covered inputs: bloomberg dated 95; seekingalpha dated 3 (2026-09-11) and NEVER 92; serp NEVER 95; pack dated 95.
- The stale flag is computed by the PAGE today (`portal/src/pages/Freshness/freshnessRows.ts`), not the function. The
  function serves stamps only. So ruling 1 moves the rule to the server (ba-1) and the page renders it (ba-4).
- Lists: publishers 2 entries, 90-day interval; social_accounts 267 entries, 30-day interval; both reviewed
  2026-09-10T22:42Z, both `owner_status` UNASSIGNED. The social account list falls due 2026-10-10.
- Portal origin/DEV at the draft: 13509c52 (it moved from 6b4e89a8 during the round-76 close).

## The seam between the cells (why the default body is not cut)

r75 c59 compares the default /freshness rows to a locally computed view (302 of 302 EQUAL), and /overlay's
`input_provenance` reads the same view. So nothing is removed from, or added to, the default body. The page asks for a
SEPARATE view: `GET /freshness?view=page`.

## Hookups for the adapter cell ba-11 (in `lib/research/api/scoped_amgt.py`; no Group A cell edits that file)

At the /freshness route (`scoped_amgt.py:6905`, `return _response(200, serve_coverage_freshness())`):

```
view = serve_coverage_freshness()
if (_query(event).get("view") or "") == "page":
    from lib.research.freshness import page_body, stale_rule
    from lib.research.lists import owner_line
    today = datetime.datetime.utcnow().date()
    view = page_body.page_view(view, annotate=lambda row: stale_rule.annotate_row(row, today),
                               lists=owner_line.lists_statement(read_list_register()))
return _response(200, view)
```

- The annotation runs at SERVE time, so the flag is as of today and the stored snapshot stays the unannotated view.
- The three new modules import nothing outside the standard library, `lib/trading_calendar.py` (already packaged) and each
  other's inputs as arguments. The build's closure walk picks them up from the hookup's imports.
- ba-11 owns the deployed proof: `r77_ba1.py --crit AC2 --where deployed` and `r77_ba2.py --crit AC3 --where deployed`
  already run against the deployed function; a deployed check of `?view=page` itself is ba-11's (or the redeploy cell's) to add.

## Not in Group A

- The `/refresh` control is on the DSGN lane's page: `portal/src/pages/SecurityAnalysis/SecurityAnalysis.tsx:72`
  (`useRequestRefresh`, `hooks/useLeadPanelApi.ts:130`; client function `requestRefresh`,
  `src/api/endpoints/amgt-lead-panel.ts:131`). The server half (`POST /refresh`, `scoped_amgt.py:6208` and `:7045`) is the
  adapter cell's.
- `portal/src/api/endpoints/amgt-lead-panel.ts` is claimed by ba-4. Any other cell that types a new /overlay or route field
  in the portal client collides with it.

## Base lines (dry-run at the shared tree HEAD; ba-4 against the exported origin/DEV page files)

- ba-1 AC1 base: FAIL as expected
- ba-1 AC2 base: FAIL as expected
- ba-1 AC3 base: PASS as expected
- ba-2 AC1 base: FAIL as expected
- ba-2 AC2 base: FAIL as expected
- ba-2 AC3 base: PASS as expected
- ba-3 AC1 base: FAIL as expected (C2, the unchanged-dates bound, holds)
- ba-3 AC2 base: FAIL as expected
- ba-3 AC3 base: PASS as expected
- ba-4 AC1 base: FAIL as expected
- ba-4 AC2 base: FAIL as expected
