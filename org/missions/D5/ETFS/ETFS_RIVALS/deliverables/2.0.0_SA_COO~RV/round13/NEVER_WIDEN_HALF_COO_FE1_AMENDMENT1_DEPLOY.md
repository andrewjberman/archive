# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 13 RIV-fe-1 AMENDMENT 1 -- deploy the five rivalfunds Lambdas at CLOUD 42b4e258d1, republish 2026-10-06 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-06 ~21:1xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** the CTO half @2f44b42430 ("The 2 Alphabet mentions") asked this seat to read which case holds. Measured: case 1 -- WCMG's
stored account says "Alphabet Inc" and cites `WCMG|R30|GOOGL_US_Equity`; WCMG holds GOOGL; the served page linked GOOG reading
"Alphabet Inc-Cl C". Cause: `render._collect_aliases` let an alias from another listing's casing variant outrank the held key's
page name. RIV-fe-1 was REOPENED with criterion AC3 (amend 986ea1ddfc; base FAIL 2), fixed by its worker, drained @a61a83ec16
(AC1, AC2, AC3 PASS, issuer re-run). Package suite on CLOUD: 777 passed, 2 skipped, 0 failed.

## VERDICT: SIGNED

Conditions: the pin is CLOUD 42b4e258d1; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (291bb5bb4b, deployed 20:41Z, ledger etfs-rivalfunds-fe1 CLOSED)

Measured: `git diff 291bb5bb4b 42b4e258d1` over what `rivalfunds_package.py` stages -- ONE file: `render.py` (+37 / -4): inside a
fund's panel an alias that can mean several page names resolves to the name whose key the fund holds or traded (a cited key
breaks a tie); a single-meaning alias behaves as before. RIV-lk-1 is NOT in this pin (held on its branch for the gateway route).

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-fe1-a1`).
2. **`safe-apply` of `C:/tmp/rv_apply13c.tfplan`** from `C:/tmp/rv-r8` detached at 42b4e258d1 after `rivalfunds_package.py`
   (plan text `rv_plan13c.txt` beside this half): **0 to add, 5 to change, 0 to destroy**, `source_code_hash` + `last_modified`
   only. Before = the fe-1 set (daily HiLwg//x, fetch M4tzZ1Hh, canonical hJQP/r1t, silver b5uodcYR, publish KwIQm/7I), live;
   after = daily r6Ecbq6f, fetch MsbSvBMk, canonical VNE9jlG0, silver L7L0vmOP, publish 9yxo7f6w.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-06","mode":"daily","batch_id":"rv-publish-1006r13b","sink":"s3","refresh_a1":false}`.

## EXPECTED OUTCOME -- MEASURED, NOT PREDICTED

`round12/real_run.py` on the pin's code (live inputs read-only, writes local only), `round13/real_run_2026-10-06.fe1a1.json`:
- `index.html` 1,317,781 B (32.4% headroom; live 1,318,591 B), dialogs ON, 2,076 buttons, 423 dialogs (live 424), 0 dead; 13 of 13;
- **`fund_sections`: 2,076 buttons, 2,076 with their fund's section, 0 missing** (this seat's own walk of the rendered page
  agrees: no member). So NO `FAIL: fund sections missing` line prints.
  - The 2 Alphabet mentions in WCMG now link GOOGL_US_Equity reading "Alphabet Inc" (WCMG panel: 3 GOOGL buttons, 0 GOOG).
  - The 8 Nebius mentions in WCMG ALSO close tonight, before any parsekey: the same rule links the name to the key WCMG holds
    (NBIS_US_Equity; read on the rendered page: WCMG's panel carries 11 Nebius buttons, all to NBIS_US_Equity). This was not
    predicted in the fe-1 half, which expected them to wait for 2026-10-07; it is measured here.
- The one-fewer dialog is N97284108's (read: the page's Nebius dialogs are now [NBIS_US_Equity] only). Only WCMG's mis-linked
  mentions referenced it; GQGU's panel carries no Nebius button on the main page. S43 itself (GQGU's Nebius still keyed
  N97284108 in the A1 tables) stays open until G4 carries parsekeys -- the 10-07 census, unchanged.
- Producer rule, both branches (publish_page.produce_a1, `refresh_a1: false`): SKIP when the A1 objects of 2026-10-06 have no
  newer input (the measured branch); REBUILD with the pin's code otherwise (no parsekeys in G4 tonight: today's keys) -- read at P1v.
**Branch NOT applied:** stop, close the entry red; the served page stays rv-publish-1006r13.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the 291bb5bb4b set (live) | the 42b4e258d1 set | a saved plan from a detached worktree at 291bb5bb4b after `rivalfunds_package.py`, `safe-apply` |
| platinum/page/date=2026-10-06/index.html | 1,318,591 B (20:43:24Z), fund_sections missing 10 | ~1,317,781 B, missing 0; prior kept under revisions/<ts>/ | republish after the code rollback |
| platinum/page/date=2026-10-06/audit.html, manifest.json | batch rv-publish-1006r13 | batch rv-publish-1006r13b | as above |
| state/publish_page/date=2026-10-06/ | present | +1 marker | none needed |

The morning read (10-07, with the pk-1/al-1 census, ledger etfs-rivalfunds-pk1-al1 leg C1) now expects `fund_sections` missing 0.
