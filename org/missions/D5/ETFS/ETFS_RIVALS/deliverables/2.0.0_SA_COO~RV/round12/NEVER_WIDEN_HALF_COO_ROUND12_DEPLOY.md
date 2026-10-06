# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 12 -- deploy the five rivalfunds Lambdas at CLOUD 50a2248fe9, republish 2026-10-06 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-06 ~17:5xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** Andrew-direct 2026-10-06 ~16:3xZ (record @05c469e083): "Any mention of a security by ticker should be hyperlinked to the
modal popup for that fund's engagement with that security", re-sequenced ~16:4xZ (ADDENDUM 4 @56de423b4d): audit off the page,
then the links, then the audit route. Round 12 (issuance 6697de57c2) built RIV-au-1; drained @c34e0875e9 (AC1/AC2 PASS re-run by
the issuer on the branch; package suite on CLOUD 746 passed, 2 skipped, 0 failed). Real-run evidence @50a2248fe9.

## VERDICT: SIGNED

Conditions: the pin is CLOUD 50a2248fe9; every read below holds as stated; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (b8b47bb8e7, deployed 2026-10-05 21:58Z, ledger etfs-rivalfunds-z-s31-repair)

Measured: `git diff b8b47bb8e7 50a2248fe9` over what `rivalfunds_package.py` stages (rivalfunds/, lib/opal_naming.py,
lib/trading_calendar.py, lib/research/identity/, infra/logic/registry/, org/standards/NAMING_SCHEMA.json):
- `render.py`, `publish_page.py` -- RIV-au-1 (this round): audit trail off the main page into `audit.html`; dialogs kept; loud
  over-cap FAIL line + manifest `holding_dialogs`.
- `gold_holding_contribution.py` -- RIV-ok-1 (round 10; its standalone deploy HELD by CTO ruling (A) @982e914b1d because it is a
  no-op on live data, row Z-S43). It rides this pin unchanged from that ruling's reading.
- `gold_trade_schedule.py` -- RIV-gt-1 (round 11): G5 stamps `producer_version`; a same-input pass at a new version writes a new
  `-v<NN>` revision. Its served replay already landed (ledger etfs-rivalfunds-served-replay CLOSED @6d83ff68bb, 364 objects).
- `enrichment_bloomberg.py` -- RIV-eg-1 (round 10): already live on the vehicle (the terminal machine's working tree); the Lambdas
  do not run the market pull.
- `tools/g5_code_replay.py`, `tools/g5_drift.py` -- tools, no Lambda entry point reaches them.
- `lib/research/identity/build_universe.py` (AMGT_RESAPP av-7/aw-6) -- staged in the zip; rivalfunds imports only
  `lib.research.identity.crosswalk` (gold_canonical_shape.py:180,185), which is unchanged and does not import build_universe.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (`.tools/deploy_ledger.py open`, slug `etfs-rivalfunds-round12`).
2. **`safe-apply` of `C:/tmp/rv_apply12.tfplan`** from `C:/tmp/rv-r8` detached at 50a2248fe9 after `rivalfunds_package.py`
   (plan text `C:/tmp/rv_plan12.txt`): **0 to add, 5 to change, 0 to destroy**, `source_code_hash` + `last_modified` only
   (daily CGLr/RBRm/... -> the five hashes in the plan text). No environment change: `RIVALFUNDS_LEG_*` stay as live,
   `leg_gates.json` at the pin unchanged from b8b47bb8e7.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-06","mode":"daily","batch_id":"rv-publish-1006r12","sink":"s3","refresh_a1":false}`.

## EXPECTED OUTCOME -- MEASURED, NOT PREDICTED

`deliverables/2.0.0_SA_COO~RV/round12/real_run.py` (live inputs read-only, writes local only) with the pin's publisher code:
- base code (control): `index.html` 1,813,001 B == the served bytes, holding dialogs OFF, 0 links, audit block inline;
- au-1 code: `index.html` 1,294,421 B (33.6% headroom under DIALOG_SOFT_CAP 1,950,000; gateway cap 2,097,152), dialogs ON,
  2,073 data-sec buttons, 424 dialogs, 0 dead; `audit.html` 1,326,857 B, 221 buttons, 171 dialogs, 0 dead; manifest
  `holding_dialogs: on`, 13 of 13 funds updated; status OK.

The producer's rule, both branches (publish_page.produce_a1 with `refresh_a1: false`): an A1 table that already has an object at
date=2026-10-06 and no newer G1/G4 input SKIPS (the measured branch: the real run read the published A1 objects); a table with a
newer input REBUILDS with the pin's code (ok-1's re-keying, a no-op on live data per Z-S43) and the page is then that rebuild --
read at P1v, not assumed. The real run turned the producers off, so the rebuild branch is NOT measured.

**Residual, stated:** 5 AI-text mentions of 3 names carried by two listings stay plain spans (RIV-ln-1 rule) -- row Z-S50, a CTO
question, not this act.
**Branch NOT applied** (the apply fails or a verify differs): stop, close the entry red; the served 10-06 page stays the 13:07Z one.

## BLAST RADIUS, PER KEY

| key | before | after | rollback |
|---|---|---|---|
| five Lambdas' code | the b8b47bb8e7 set (live, 2026-10-05 21:58Z) | the 50a2248fe9 set | a saved plan from a detached worktree at b8b47bb8e7 after `rivalfunds_package.py`, `safe-apply` |
| platinum/page/date=2026-10-06/index.html | 1,813,001 B, dialogs off (13:07:38Z) | ~1,294,421 B, dialogs on; prior kept under revisions/<ts>/ | republish after the code rollback |
| platinum/page/date=2026-10-06/audit.html | absent | ~1,326,857 B (written, not linked, not served) | delete that key (human-confirmed S3 delete) or leave: nothing reads it |
| platinum/page/date=2026-10-06/manifest.json | 13:07Z batch | batch rv-publish-1006r12 (+audit_uri, holding_dialogs) | republish after rollback |
| state/publish_page/date=2026-10-06/ | present | +1 marker | none needed |
| next organic runs (2026-10-07 07:00 ET marker publish, the batch chain) | b8b47bb8e7 code | 50a2248fe9 code: audit.html daily; G5 stamps producer_version | the code rollback above |

Not in this act: the gateway audit route and the page link (ADDENDUM 4 step 3, after step 2 is graded); republishing 2026-10-05.
