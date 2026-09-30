# Model-block reader census, round 18 (CRPS-t-3)

Worker 0.9.0_WK_AMGT_CORPUS~3. Read-only. Bucket `opal-data-harvest`, prefix `derived/model_block/`. Names exercised: `BP/_LN_Equity`, `NG/_LN_Equity`.

Writer key form: raw slash (`model_block_pull.py:1319`). Live: 6 objects under each raw-slash key, 0 under `BP-SLASH-_LN_Equity` / `NG-SLASH-_LN_Equity`.

## Denominator

Searched by `git grep` over tracked files in lib/, integrations/, infra/ (portal/ excluded): **9210 files**. `model_block` hits **81 files / 673 lines** (41 files non-test). The store-prefix token (`derived/model_block/`, `MODEL_BLOCK_POOL_PREFIX`, `MODEL_BLOCK_PREFIX`) is in **15 files** (11 non-test). Non-readers among those: s3.tf and scoped-amgt-api.tf (IAM grants), model_block_pull.py (the writer; it reads only bronze), crosswalk.py (provenance text), robustness.py (a message string).

**Reader rows: 20.** OK 18, ABSENT 1, NOT_APPLICABLE 1.

## Table

| # | reader | key_form | reads_bp |
|---|--------|----------|----------|
| 1 | `lib/research/api/scoped_amgt.py:1106` | raw_slash | OK |
| 2 | `lib/research/api/scoped_amgt.py:1085` | raw_slash | OK |
| 3 | `lib/research/api/scoped_amgt.py:2011` | raw_slash | OK |
| 4 | `lib/research/api/scoped_amgt.py:2180` | raw_slash | OK |
| 5 | `lib/research/api/scoped_amgt.py:3229` | raw_slash | OK |
| 6 | `lib/research/api/scoped_amgt.py:3314` | raw_slash | OK |
| 7 | `lib/research/api/scoped_amgt.py:3979` | raw_slash | OK |
| 8 | `lib/research/api/scoped_amgt.py:4042` | raw_slash | OK |
| 9 | `lib/research/api/scoped_amgt.py:4480` | raw_slash | OK |
| 10 | `lib/research/corpus/dossier.py:927` | raw_slash | OK |
| 11 | `lib/research/corpus/dossier.py:966` | raw_slash | OK |
| 12 | `lib/research/corpus/base_census.py:152` | raw_slash | OK |
| 13 | `lib/research/peers/universe.py:312` | raw_slash | OK |
| 14 | `lib/research/peers/universe.py:331` | raw_slash | OK |
| 15 | `lib/research/peers/engine.py:163` | raw_slash | OK |
| 16 | `lib/research/scores/run_scores.py:106` | raw_slash | OK |
| 17 | `lib/research/scores/run_scores.py:223` | raw_slash | OK |
| 18 | `infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py:233` | raw_slash | OK |
| 19 | `lib/research/print/render_pack.py:1043` | other:filesystem_safe_display_form_space-to-underscore_slash-to-hyphen | ABSENT |
| 20 | `lib/research/posture/packs.py:64` | other:local_directory_file_model_block_KEY.json | NOT_APPLICABLE |

Per-row evidence (the key builder's code and the live read-only exercise) is in `MODEL_BLOCK_READERS_ROUND18.json`.

## ABSENT and its served surface

One row: `lib/research/print/render_pack.py:1043`, the `main()` command-line entry. It passes `render_pack.security_key(name)` (a local-filesystem form: space to `_`, slash to `-`) to `read_model_block`, so BP and NG read `derived/model_block/BP-_LN_Equity/` and `NG-_LN_Equity/` (neither exists) and the CLI prints `BLOCKED: no landed model block`. Non-slash names are unaffected because the two forms coincide.

**Served surface: none.** No code in lib/, integrations/ or infra/ calls `render_pack.main`, and the served print route (`scoped_amgt.py:4480`) reads with the resolved raw key. Served routes for BP and NG measured live: `/security/BP%2F_LN_Equity/versions` and `/thesis` return 200 with 6 versions / model_status SERVED (NG likewise).

## Answer to the ruling question

Every served reader (scoped_amgt, dossier, base_census, peers, scores, seed-etf-constituents) uses the same raw-slash form as the writer and reads BP and NG as present. `resolve_identity` returns the raw form (`BP/ LN` -> `BP/_LN_Equity`) and the crosswalk carries 0 slash-safe keys. The only reader that builds a different key is the unwired render_pack CLI. The census is code plus read-only live reads; the print route was not rendered.
