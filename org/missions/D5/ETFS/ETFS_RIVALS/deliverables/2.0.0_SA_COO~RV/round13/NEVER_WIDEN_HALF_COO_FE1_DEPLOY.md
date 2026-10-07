# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 13 RIV-fe-1 -- deploy the five rivalfunds Lambdas at CLOUD 291bb5bb4b, republish 2026-10-06 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-06 ~20:3xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** ROUND_ANALYSIS.round11.md @3ae96d6bc7 rulings 1, 2, 5 (C-S47 + Z-S50 + C-S36): every mention in fund F's panel opens a
modal with F's engagement, and the page counts it. RIV-fe-1 drained @1de1c1af1b (AC1 37/37 on the plant, AC2 PASS; issuer
re-run). Package suite on CLOUD: 774 passed, 2 skipped, 0 failed. RIV-lk-1 (the audit link) is NOT in this pin: it stays on its
branch until the gateway route is released, so no link can precede the route.

## VERDICT: SIGNED

Conditions: the pin is CLOUD 291bb5bb4b; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (92cf1f322b, deployed 20:02Z, ledger etfs-rivalfunds-pk1-al1 OPEN on its census leg)

Measured: `git diff 92cf1f322b 291bb5bb4b` over what `rivalfunds_package.py` stages -- three files, all RIV-fe-1:
- `render.py` (+95): a shared name resolves by the panel fund's own keys; `_sec_dialogs` writes a fund section from a trend row in
  any period; `fund_section_census`;
- `publish_page.py` (+11): manifest `fund_sections`, and a `FAIL: fund sections missing ...` line when missing > 0;
- `security_names.py` (+23): the names stage also asks the trend's ticker-named keys (runs on the vehicle from CLOUD; no Lambda
  path calls Bloomberg).
gw-1's gateway files are on CLOUD at this pin but are not in the Lambda package.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-fe1`).
2. **`safe-apply` of `C:/tmp/rv_apply13b.tfplan`** from `C:/tmp/rv-r8` detached at 291bb5bb4b after `rivalfunds_package.py`
   (plan text `rv_plan13b.txt` beside this half): **0 to add, 5 to change, 0 to destroy**, `source_code_hash` + `last_modified`
   only. Before = the pk-1/al-1 set (daily NLWa+glx, fetch pzoscnfB, canonical pX4xe2wJ, silver hJ/zqsdO, publish B5srwuWE) --
   live, read by the plan; after = daily HiLwg//x, fetch M4tzZ1Hh, canonical hJQP/r1t, silver b5uodcYR, publish KwIQm/7I.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-06","mode":"daily","batch_id":"rv-publish-1006r13","sink":"s3","refresh_a1":false}`.

## EXPECTED OUTCOME -- MEASURED, NOT PREDICTED

`round12/real_run.py` on the pin's code (live inputs read-only, writes local only), `round13/real_run_2026-10-06.fe1.json`:
- `index.html` 1,318,591 B (32.4% headroom under DIALOG_SOFT_CAP; live 1,294,421 B), dialogs ON, 2,076 buttons, 424 dialogs, 0
  dead; `audit.html` 1,337,761 B; 13 of 13 funds; status OK;
- **`fund_sections`: 2,076 buttons, 2,066 with their fund's section, 10 missing** -- so the stage prints its
  `FAIL: fund sections missing` line tonight. The 10, enumerated on the rendered page:
  - 8: "Nebius Group Nv" in WCMG's AI text links N97284108, whose modal carries GQGU only. This is S43 (two keys); it is expected to
    close when G4 carries parsekeys after the 2026-10-07 07:00 ET run (pk-1 + al-1, live) -- read then, not assumed;
  - 2: "Alphabet Inc-Cl C" in WCMG's AI text links GOOG_US_Equity, whose modal carries BASG, GQGU, PCLG, PFOE and no WCMG:
    WCMG has no contribution or trend row for GOOG. The account names a listing the fund shows no engagement with -- a question for
    the CVO/CTO (the AI account or the name map), not a renderer gap.
- The CVO's C-S47 count was 15; the pin reads 10, and names each.
- Producer rule, both branches (publish_page.produce_a1, `refresh_a1: false`): an A1 table with an object at date=2026-10-06 and no
  newer G1/G4 input SKIPS (the measured branch); a table with a newer input REBUILDS with the pin's code (pk-1/al-1 keys: no
  parsekeys in G4 tonight, so today's keys) -- read at P1v.
**Branch NOT applied:** stop, close the entry red; the served 10-06 page stays the 17:33Z one.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the 92cf1f322b set (live) | the 291bb5bb4b set | a saved plan from a detached worktree at 92cf1f322b after `rivalfunds_package.py`, `safe-apply` |
| platinum/page/date=2026-10-06/index.html | 1,294,421 B (17:33:01Z) | ~1,318,591 B; prior kept under revisions/<ts>/ | republish after the code rollback |
| platinum/page/date=2026-10-06/audit.html | 1,326,857 B | ~1,337,761 B; prior kept under revisions/<ts>/ | as above |
| platinum/page/date=2026-10-06/manifest.json | batch rv-publish-1006r12 | batch rv-publish-1006r13 (+fund_sections) | as above |
| state/publish_page/date=2026-10-06/ | present | +1 marker | none needed |

Interaction with the OPEN pk-1/al-1 entry: its census leg C1 (after the 10-07 07:00 ET run) is unchanged; this act adds the
`fund_sections` read to that same morning (missing expected 2, Nebius closed).
