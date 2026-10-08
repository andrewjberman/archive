# NEVER-WIDEN -- COO HALF: ETFS_RIVALS RIV-mr-1 ALONE (the marker read-out) -- deploy the five rivalfunds Lambdas at content pin fd633ec4d2, republish 2026-10-07 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~23:53Z, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** CTO rulings msgs 31477 (ask 3) and 31480: RIV-mr-1 J1 is MET (CVO ADJUDICATION_v30 @e3cc04e7bb) and "may ship
alone", render.py only, under its own pair. RIV-rg-1 is NOT applied (its J1 is NOT MET; row ETFS_RIVALS-Z-S71) and my
half for pin acf83a5716 (@cfa71419f0) is WITHDRAWN. No vendor is called; no wheel is built; nothing is fetched.

## VERDICT: SIGNED

Conditions: the pin is the content pin fd633ec4d2; every read below holds; the act stops at the first differing read.

## THE PIN IS BUILT, NOT A POINT ON CLOUD -- resolved by content

Site-Z CLOUD HEAD carries RIV-rg-1's readers (merge 1d2241ca66), which must not be deployed. So the pin is the LIVE pin
f9f8334ef6 plus the ONE build commit of RIV-mr-1 (339ba875be) cherry-picked onto it in the deploy tree: commit
**fd633ec4d2**, kept on the local branch `rv-deploy-r25mr`. Read:
- `git diff f9f8334ef6 fd633ec4d2`: 2 files -- `data/etfs/scripts/rivalfunds/render.py` (+8 / -8) and its test (not packaged).
- `render.py` at the pin is blob bc108a9504f5, EQUAL to `render.py` at the merged mr-1 commit 4c34f7f298 (the positive
  read); the patch f9f8334ef6 -> pin over render.py hashes equal to the patch f9f8334ef6 -> 4c34f7f298 over it (1810af7f95a3).
- Negative control: none of RIV-rg-1's seven reader files differs from the live pin (the diff names two files only), so
  `g4_rows` is NOT in this pin.
- The script: 9,348 to 9,502 bytes; still one fetch, to this product's chart route.

## THE ACT, IN ORDER

1. **Open the NEVER-2 ledger entry** (slug `etfs-rivalfunds-r25-mr1`): apply; republish; served read.
2. **`safe-apply` of `C:/tmp/rv_apply25mr.tfplan`** from `C:/tmp/rv-r8` at the pin (plan text `round25/rv_apply25mr.plan.txt`):
   **0 to add, 5 to change, 0 to destroy**; `source_code_hash` and `last_modified` only. Before = the live set (daily
   3BFfLeYC, fetch mHg1VZz2, canonical vTjVc2Ym, silver 0hmlWkob, publish 8PjWCoxj); after = daily UHfCiT80, fetch OoXPTjMF,
   canonical 7KNOgjTc, silver 7SS2kS3b, publish DGtKYZj1. (The saved plan `C:/tmp/rv_apply25.tfplan` of the withdrawn
   deploy is NOT this one and is not applied.)
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-07","mode":"daily","batch_id":"rv-publish-1007r25mr","sink":"s3","refresh_a1":false}`.
   `refresh_a1` FALSE: no table's code changes.
4. Download the served objects; grade; close the ledger.

## THE WRITE SET (the same code path as rounds 23 and 24), with the rollback per key

| key under `s3://opal-data-etfs/rivalfunds/etfs/` | expected | rollback |
|---|---|---|
| five Lambda code hashes | the after-set | re-package at f9f8334ef6, plan, `safe-apply` |
| the three A1 tables | **no write** (no input newer; as at 19:18Z and 21:25Z) | -- |
| `platinum/page/date=2026-10-07/revisions/<stamp>/` | 15 copies (index, manifest, 13 charts; no audit copy: the audit page's bytes do not change) | none; they are the rollback |
| `.../index.html` | 1,693,709 B (served 1,693,555: the script's 154 bytes); 1 script; `fund_sections` 0 missing | republish from the rolled-back code, or copy back |
| `.../audit.html` | 1,255,777 B, byte-equal to the served one in the prediction | same |
| 13 `.../charts/*.json` | rewritten with identical `securities` data (13 of 13 equal to the served objects; only `generated_at` differs); 5,675,727 B, 5,894 markers | same |
| `.../manifest.json`, one state record | as rounds 23 and 24 | same |

Prediction: `round25/real_run_2026-10-07.mr1_only.json`, the real-run tool run FROM the deploy tree at the pin. Against the
served tables its tables read 0 moved rows of 6,066 and of 1,406: **no served figure moves.**

## BOTH BRANCHES

- **Fits** (rounds 23 and 24: 74 s, 558 MB): status OK, the reads above.
- **Killed or timed out:** as rounds 23 and 24 -- manifest not older than index and 13 chart objects, or one more
  republish, else roll back.
- **After this act the deployed code is NOT a commit of CLOUD's history.** The next deploy from CLOUD (RIV-rg-2 with
  rg-1) carries the same render.py, so nothing is lost; until then the ledger and STATUS name fd633ec4d2 as the live pin.

## WHAT THIS ACT DOES NOT PROVE

- One tooltip at the plot's right edge sits 0.64 px over the frame's border (seen in round 25's browser look; as round
  24 built the clamp).
- Andrew's look at the chart is the acceptance; not yet had for rounds 24 or 25.
