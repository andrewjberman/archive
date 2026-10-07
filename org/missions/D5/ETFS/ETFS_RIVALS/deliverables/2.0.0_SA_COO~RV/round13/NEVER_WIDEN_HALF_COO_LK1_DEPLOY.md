# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 13 RIV-lk-1 -- deploy the five rivalfunds Lambdas at CLOUD f3b3055a5e, republish 2026-10-06 ONCE (ADDENDUM 4 step 3: the audit link)

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~02:1xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** Andrew-direct 2026-10-06 ~16:4xZ: "3.) Make an audit gateway after 2.) is done". Step 2 is graded (CVO~RV 5ec39d17e2:
0 of 2,076 buttons lack their fund's section). The gateway route is released: NFRA_OPLGTW release r23, deployed_commit
7d65a28db0, live since 2026-10-07T01:30:43Z, ledger CLOSED (COO~O msg 30505). RIV-lk-1 (the main page's one link; the AI citation
lines move to the audit page -- round-11 analysis ruling 3) was held on its branch until then and is drained @1c9f7f5ec6. Package
suite on CLOUD: 780 passed, 2 skipped, 0 failed; lk-1.AC1, fe-1.AC1/AC3 PASS; au-1.AC1/AC2 arm (a) amended to "exactly one audit
link" (row Z-W2-S15) and PASS.

## THE ROUTE PROOF, AND ITS LIMIT (stated, not hidden)

- NFRA_OPLGTW's proof `deliverables/0.9.0_WK_NFRA_OPLGTW~28/RL9_ROUTE.json`: on the gateway host, with the released code and a
  synthetic signed-in identity, GET /rivalfunds/2026-10-06/audit -> 200 with 1,337,761 bytes (equal to the audit.html this seat
  published at 21:18Z); 2000-01-01 -> 404 (both read by this seat in the JSON). COO~O's message 30505 adds two arms the JSON
  does not carry: no identity -> 401, and the day page still 200 (COO~O's statement, not re-read here).
- NOT exercised by any seat: a real signed-in browser GET through the load balancer. This seat's unauthenticated probes of
  /rivalfunds/2026-10-06/audit, /rivalfunds/2026-10-06, /rivalfunds/2000-01-01/audit and /health all return 302 to Microsoft
  sign-in -- the balancer authenticates every path before the app, so the probe cannot tell a served route from an absent one.
  The balancer forwards every path to the app once signed in (the day page is the positive control of that hop). The first
  signed-in click on the link is Andrew's or a signed-in seat's to read.

## VERDICT: SIGNED

Conditions: the pin is CLOUD f3b3055a5e; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (42b4e258d1, deployed 21:16Z, ledger etfs-rivalfunds-fe1-a1 CLOSED)

Measured: `git diff 42b4e258d1 f3b3055a5e` over what `rivalfunds_package.py` stages -- ONE file: `render.py` (+44 / -12), RIV-lk-1.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-lk1`).
2. **`safe-apply` of `C:/tmp/rv_apply13d.tfplan`** from `C:/tmp/rv-r8` detached at f3b3055a5e after `rivalfunds_package.py`
   (plan text `rv_plan13d.txt` beside this half): **0 to add, 5 to change, 0 to destroy**, `source_code_hash` + `last_modified`
   only. Before = the fe-1 AMENDMENT 1 set (daily r6Ecbq6f, fetch MsbSvBMk, canonical VNE9jlG0, silver L7L0vmOP, publish
   9yxo7f6w), live; after = daily VhckkMgd, fetch gWWtaG7i, canonical 6lKYpSsD, silver oUN0tQyQ, publish LbqdRy4S.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-06","mode":"daily","batch_id":"rv-publish-1006r13c","sink":"s3","refresh_a1":false}`.

## EXPECTED OUTCOME -- MEASURED, NOT PREDICTED

`round12/real_run.py` on the pin's code (live inputs read-only, writes local only), `round13/real_run_2026-10-06.lk1.json`:
- `index.html` 1,276,544 B (34.5% headroom under DIALOG_SOFT_CAP; live 1,317,781 B): dialogs ON, 2,076 buttons, 423 dialogs, 0
  dead, `fund_sections` 2,076 / 2,076 / 0; exactly ONE `href="/rivalfunds/2026-10-06/audit"`, reading "The trades behind these
  figures, the latest holdings and the sources behind every AI figure are one step away on the audit page."; 0 "Cited rows:" lines;
- `audit.html` 1,381,244 B (live 1,337,761 B; gateway cap 2,097,152 B, 34.1% under): a `citations` section with 26 blocks
  (`data-cited-fund` x `data-ai-kind`), 26 "Cited rows:" lines; 221 buttons, 171 dialogs, 0 dead;
- 13 of 13 funds; status OK; no FAIL line.
- Producer rule, both branches (publish_page.produce_a1, `refresh_a1: false`): SKIP when the A1 objects of 2026-10-06 have no
  newer input (the measured branch); REBUILD with the pin's code otherwise -- read at P1v.
**Branch NOT applied:** stop, close the entry red; the served page stays rv-publish-1006r13b (no link).

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the 42b4e258d1 set (live) | the f3b3055a5e set | a saved plan from a detached worktree at 42b4e258d1 after `rivalfunds_package.py`, `safe-apply` |
| platinum/page/date=2026-10-06/index.html | 1,317,781 B (21:18:30Z), no audit link | ~1,276,544 B, one audit link; prior kept under revisions/<ts>/ | republish after the code rollback |
| platinum/page/date=2026-10-06/audit.html | 1,337,761 B | ~1,381,244 B (+ citations); prior kept under revisions/<ts>/ | as above |
| platinum/page/date=2026-10-06/manifest.json, state/publish_page marker | batch rv-publish-1006r13b | batch rv-publish-1006r13c | as above |
| every later day's page | no link | the link to that day's audit page (written by the same publish) | the code rollback |

A day published BEFORE round 12 has no audit.html: its page (unchanged, never republished by this act) carries no link either.
Row Z-W1-S48 (audit.html has no own size refusal; 34.1% under the cap today) stays open for the next round.
