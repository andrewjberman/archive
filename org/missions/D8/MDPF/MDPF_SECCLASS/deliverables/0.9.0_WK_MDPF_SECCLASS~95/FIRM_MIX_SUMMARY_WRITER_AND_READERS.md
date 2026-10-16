# FIRM_MIX_SUMMARY_WRITER_AND_READERS -- SC-e-105 (round 26)

Served object under test: `opal-data-bd/platinum/firm/mix_summary.json` (firm `49financial`), the firm Mix summary the Advisor Intelligence page reads.
Evidence pinned at worktree HEAD `d63495282e` (repo code, census via `git grep HEAD`) and at the nested portal repo HEAD (read through `git -C portal show HEAD:<path>`). No code was edited; no AWS call was made.

WRITER: data/black_diamond/scripts/gold/D_04.client_portal_summary.py:578

Why this line is the writer. Line 578 is `_write_batch([(summary, 'platinum/firm/mix_summary.json')], upload, label='firm mix summary')` inside `build_firm_mix_summary`. The module sets `FIRM_ID = '49financial'` (line 133), so the object it writes is the 49financial firm's. Its body is built by `_write_json_to_s3` (line 268), which calls `json.dumps(data, default=str, separators=(',', ':'))` (line 270) with no `sort_keys`: the served key order is the order the `summary` dict is built (`generated_at`, `data_as_of`, `firm_id`, `mix`, `mix_periods`, `concentration`, `composition`, `restated_through`). The destination bucket and key come from `platinum_destination(key)`, imported at line 84 from `lib.platinum_dest`. That module is NOT tracked at HEAD and is not on disk in the main checkout, so the bucket is not read from the writer; it is read from the readers instead: `data/assets/scripts/gold/runners_49f/d06_firm_mix_summary.py:246` reads `Bucket="opal-data-bd", Key="platinum/firm/mix_summary.json"` as the served 49financial object, and the fit harness names `opal-data-bd` as the legacy bucket (`data/assets/scripts/gold/runners_49f/fit_harness.py:41`).

Other scripts that write a similarly named object, and why none is this key.

- `data/cot/scripts/gold/D_04.client_portal_summary.py:589` writes `platinum/firm/mix_summary.json` for `FIRM_ID = 'cottonwood'` (line 132) through the module-level `BUCKET` (`from lib.config import S3_BUCKET`, line 83, untracked at HEAD). The cottonwood served bucket is `opal-data-cot`, the `BUCKET` constant of `data/cot/scripts/gold/runners_cot/d_fleet_common.py:22`. Different firm, different bucket: a different object that happens to share the key string.
- `data/inf/scripts/gold/INF_D_02d.firm_mix_summary.py:528` writes `MIX_SUMMARY_KEY` (line 66) to `S3_BUCKET = 'opal-data-inf'` (line 61). Different bucket: a different object.
- `data/cot/scripts/gold/runners_cot/d08_cot_mix_summary.py:211` is a QA emitter: `d_fleet_common.py` states "QA-ONLY emission ... NO S3 writes". It reads the cottonwood served object (`opal-data-cot`) by key name. It does not write this object.
- `data/assets/scripts/gold/runners_49f/d06_firm_mix_summary.py` declares `FAMILY = "platinum/firm/mix_summary"` (line 44) and `FIRM_ID = "49financial"` (line 45). Its only write is the `--out` QA file (line 296). It is the 49F emitter whose payload feeds the advi twin, not a writer of the legacy key.
- `data/assets/scripts/gold/runners_49f/d_publisher_port.py` writes the advi twin `platinum/advi/49financial/{leaf}` into `opal-data-portal-v2` (`SERVE_BUCKET` line 61, `SERVE_ROOT` line 62, scope assert line 467). It names `platinum/firm/mix_summary.json` only as a `legacy` label (line 106). It never writes the legacy key. The twin is a different object and is not this one.

Census. `git grep -l -I -E 'firm/mix_summary|mix_summary\.json' HEAD -- data/ infra/ lib/` plus `git -C portal grep` on `src/`, filtered by the check (code extensions only, tests excluded, the writer excluded), gives 8 census files. The reader table below carries one row for each.

| Reader (repo path:line) | Order-dependent | Why |
|---|---|---|
| data/assets/scripts/gold/runners_49f/d06_firm_mix_summary.py:246 | ORDER-DEPENDENT: no | served_convention_compare reads the served object by key name and walks `composition.mix` as an array (array order, not object key order); the emitter writes only its --out QA file |
| data/assets/scripts/gold/runners_49f/d_publisher_port.py:106 | ORDER-DEPENDENT: no | writes only the advi twin `platinum/advi/49financial/*` (scope assert line 467); the legacy key appears as a label and this file never reads its bytes or ETag |
| data/assets/scripts/gold/runners_49f/fit_harness.py:322 | ORDER-DEPENDENT: no | diff_surface walks `sorted(set(legacy) | set(new))` (line 191), so the output is invariant to key order; lists compare by index, which is array order |
| data/cot/scripts/gold/D_04.client_portal_summary.py:589 | ORDER-DEPENDENT: no | writer of the cottonwood object in its own bucket; it reads nothing back from the 49financial key |
| data/cot/scripts/gold/runners_cot/d08_cot_mix_summary.py:211 | ORDER-DEPENDENT: no | reads the cottonwood served object in opal-data-cot by key name through fc.emit_and_verify; schema_of sorts keys and takes only array element 0; the 49financial object is not read |
| data/inf/scripts/gold/INF_D_02d.firm_mix_summary.py:528 | ORDER-DEPENDENT: no | writer of the inf object in opal-data-inf; no read-back of this key or of the 49financial object |
| portal/src/api/endpoints/adviKeyRepoint.ts:215 | ORDER-DEPENDENT: no | the mix_summary entry is state 'held' (legacy only); its shape gate hasAnyKey('mix','composition','views') tests key presence by name, never position |
| portal/src/api/endpoints/advisor-intelligence.ts:559 | ORDER-DEPENDENT: no | getPlatinumFirmMixSummary fetches the object through adviRead and returns it typed; no iteration, indexing or hashing of the body in this file |

Census readers the regex or the census rule does not carry (found by a bare-token search, `\bmix_summary\b` and quoted `mix_summary` over `data/ infra/ lib/` at HEAD, and by reading each consumer of `getPlatinumFirmMixSummary` in `portal/src`). These cannot take a row: the check refuses any row whose file is outside its census as `extra`, so they are recorded here in prose and their verdicts are stated.

- `portal/src/pages/AdvisorIntelligence/_shared/tabs/ClientsTab.tsx:203-205,343-359` is the only consumer of the hook. It passes `mix.composition` to `normalizeMixTo4Class` (`portal/src/pages/AdvisorIntelligence/_shared/lib/composition.ts:98`), which walks `resp.mix` as an array and a fixed class list. No key-order dependence. Verdict: no.
- `portal/src/contexts/AuthContext.tsx:68` prefetches the object and discards the data. Verdict: no.
- `data/assets/scripts/gold/runners_49f/d00_served_shape_census.py` reads served families by listing and `_schema_of` (sorted keys, first array element), and its census_version is over `json.dumps(..., sort_keys=True)`. The family is reached through `data/assets/scripts/gold/runners_49f/d00_fe_routes_input.json:15,18` (template `platinum/firm/mix_summary.json`), which the census never sees because the extension filter excludes .json. Verdict: no.
- `data/assets/scripts/gold/runners_49f/pins/pin_d06_mix_summary.json` records the served sha256 (`d60f83dd...`) of this object as a static record. No file in the tree reads it by name. Verdict: no reader; it is not code.
- `infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml:15553` names the advi twin through the brace template `platinum/advi/49financial/{mix_summary,...}.json`. The regex does not match braces. The key is the advi twin, not this object. Verdict: not a reader of this object.
- `infra/aws/lambda-edge/_shared/firm-config.mjs:46` mentions the advi twin in a comment. The census excludes .mjs. The file reads no object. Verdict: no.

DECISION-FIRM-MIX-SUMMARY: NO-ORDER-DEPENDENT-READER

Closing sentence. No reader of `opal-data-bd/platinum/firm/mix_summary.json` depends on the key order of its body: every reader in the census and every consumer found outside it reads by key name, walks arrays by position, or sorts keys before it compares, so this question closes without an order change to `D_04.client_portal_summary.py`. No served object's bytes move under this decision, and none is sorted.
