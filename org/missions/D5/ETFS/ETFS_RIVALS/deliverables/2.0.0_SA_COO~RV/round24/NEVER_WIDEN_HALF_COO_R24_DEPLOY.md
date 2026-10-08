# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 24 (RIV-cu-1, the chart UI) -- deploy the five rivalfunds Lambdas at CLOUD f9f8334ef6, republish 2026-10-07 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~21:2xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** Andrew-direct 2026-10-07 ~19:0xZ (record @f76452470f): the dialog chart's read-out "much more focal, bold, and
obvious", the buy/sell tooltip "much more dramatic", "a box around the chart element itself with clear dates on x-ticks".
CTO ruling msg 31397: deploy today, render-only route, **on RIV-cu-1 J1 MET by `3.0.0_SA_CVO~RV`; not MET, nothing ships.**
No vendor is called; no wheel is built; nothing is fetched.

## VERDICT: SIGNED, conditional on J1 MET

Conditions: J1 MET is on file from `3.0.0_SA_CVO~RV` before the apply; the pin is CLOUD f9f8334ef6; every read below
holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (6124b079f3, live since 19:1xZ, ledger `etfs-rivalfunds-r23` CLOSED)

**It is NOT render.py alone.** Between the live pin and this one, site-Z CLOUD took the origin pull-merge (f6cff376d1), and
the packager stages the naming library and its registry into every Lambda. Over every path the packager stages:

| path | change | what was read |
|---|---|---|
| `data/etfs/scripts/rivalfunds/render.py` | +47 / -20, the cell | packet `round24/DRAIN_END_PACKET.round24.md` @ac658a6410 |
| `lib/opal_naming.py` | +69 / -4 (origin merge) | every address and name the package builds: the 10 functions of `rivalfunds/homes.py` called under the live pin's library and registry and under this pin's -- **10 of 10 equal, 0 errors** (page, audit, chart, the gold tables, markers, state, the five function names, the schedule). The library's diff was not read line by line |
| `infra/logic/registry/` 7 files, `org/standards/NAMING_SCHEMA.json` | registry rows added and re-ordered (origin merge) | the same 10 of 10; and `gen_policies.py` regenerated at the pin is byte-equal to the committed inputs (no policy, name or schedule moves), which the plan confirms |
| `lib/trading_calendar.py`, `lib/research/identity`, the Lambda wrappers, the Terraform root | none | `git diff` empty |

The real run below ran on the worker branch, whose base (ad4c7c86d2) already held the origin merge: over the packaged
paths that branch equals the pin (`git diff 0e527447fe f9f8334ef6`: empty). So the run exercised this library.

**The script (C-NO-SCRIPT as amended in F.7).** The page's one inline script grew from 7,369 to 9,348 bytes. Read at the
pin: it makes ONE kind of call, `fetch("/rivalfunds/"+D+"/chart/"+encodeURIComponent(fund))`, this product's chart
route; no `XMLHttpRequest`, no `import(`, no `.src=`; its only absolute URL is the SVG namespace string. The page still
carries exactly one script and the audit page none (`render.validate`; `cu-1.AC3.py` arm g).

## THE ACT, IN ORDER

1. Read J1 MET on file. **Open the NEVER-2 ledger entry** (slug `etfs-rivalfunds-r24`): apply; republish; served read.
2. **`safe-apply` of `C:/tmp/rv_apply24.tfplan`** from `C:/tmp/rv-r8` detached at the pin after `rivalfunds_package.py`
   (plan text `round24/rv_apply24.plan.txt`): **0 to add, 5 to change, 0 to destroy**; `source_code_hash` and
   `last_modified` only; memory stays 3,008 MB. Before = the live set (daily cTM1SBuG, fetch 99BqkcrG, canonical tyGN8WS/,
   silver TLYlfz3r, publish RHlHCL0l); after = daily 3BFfLeYC, fetch mHg1VZz2, canonical vTjVc2Ym, silver 0hmlWkob, publish
   8PjWCoxj. A saved plan refuses if the state moved; then re-plan and re-read, never force.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-07","mode":"daily","batch_id":"rv-publish-1007r24","sink":"s3","refresh_a1":false}`.
   A request that drops at the client is re-fired only after the log shows no START and the page objects are unmoved.
4. Download the served objects; grade with `round22/served_grade.py` against the prediction; close the ledger.

## THE WRITE SET, READ FROM THE CODE PATH (`publish_page.py` at the pin, lines 804 and 925 to 993), with the rollback per key

Under `s3://opal-data-etfs/rivalfunds/etfs/`:

| key | when it is written | expected | rollback |
|---|---|---|---|
| five Lambda code hashes | the apply | the after-set | re-package at 6124b079f3, plan, `safe-apply` |
| the three A1 tables at `date=2026-10-07` | only when a G1 or G4 input is newer than the table's newest object | **no write** (as at 19:18Z; no ingest before 2026-10-08 11:00Z). One written is reported | none needed |
| `platinum/page/date=2026-10-07/revisions/<stamp>/` | the served index, manifest and 13 chart objects are copied first; the audit page only if its bytes change (line 951) | 15 copies; no audit copy (the audit page does not change) | none; they are the rollback |
| `.../index.html` | line 962 | 1,693,555 B (served 1,690,296); 1 script; `fund_sections` 2247 / 2247 / 0 | republish from the rolled-back code, or copy back from `revisions/` |
| `.../audit.html` | line 964 | 1,255,777 B, same size | same |
| `.../charts/<FUND>.json`, 13 | line 966 | 13 objects, 5,675,727 B: no key of the chart object changes | same |
| `.../manifest.json` | line 993 | `fund_sections.missing` 0; `ai_grounding {"earlier": 25, "served": 0}` | same |
| `state/publish_page/date=2026-10-07/rv-publish-1007r24.json` | the run's record | one object | none |

Prediction source: `round24/real_run_2026-10-07.after_cu1.json` (the real-run tool on the branch that equals the pin). It
rebuilds the tables locally first, which the Lambda will not; on both deploys today its sizes matched the served ones.

## BOTH BRANCHES

- **The run fits** (round 23's: 74.4 s, 558 MB of 3,008): status OK, the reads above.
- **Killed or timed out:** before `index.html` the page served since 19:19Z stays; after it and before the last chart
  object the new page is served with chart objects of the same data, so the charts draw. C1 as before: manifest not
  older than index and 13 chart objects, or one more republish, else roll back.
- **The new script fails in a reader's browser** (a state the checks and one browser cannot rule out): a chart frame
  would read "Chart could not load" or stay empty; the tables, the static trade lists and the month strips are static
  markup and do not depend on the script. Rollback is the code rollback above and one republish, minutes.

## WHAT THIS ACT DOES NOT PROVE

- Not Andrew's acceptance: his own look at the signed-in page is that, after it.
- Looked at before signing: ONE dialog section (GQGU, Meta) in one browser at 1400 x 1000. Not looked at by this seat: a
  sell marker, a marker near the plot's top (the tooltip then flips below it), a narrow window, a non-dollar listing.
  The CVO's J1 is the wider look.
- Not the first full daily run on the new code: legs L4 and L5 of `etfs-rivalfunds-r22` stay open for 2026-10-08.
