# Writer trace: the price-source label in the cot price store (CB-ah-1)

Static, repo-only. No S3 call. Class rule is in the script header (committed before the first run).

## 1. Writer
- WRITER data/black_diamond/scripts/silver/inject_scoped_overrides.py:136 (default label for every exception: `force_source` in the JSON)
- label literal at data/black_diamond/scripts/silver/inject_scoped_overrides.py:60: `# Emits source=<force_source> rows (e.g. 'bd_txn_price'), which this script`
- label literal at data/black_diamond/scripts/silver/inject_scoped_overrides.py:124: `entry's force_source (e.g. 'bd_txn_price'), NOT the generic SOURCE_TAG;`
- label literal at data/black_diamond/scripts/silver/inject_scoped_overrides.py:136: `src = exc.get("force_source", "bd_txn_price")`
- label literal at data/black_diamond/scripts/silver/scoped_price_exceptions.json:10: `"force_source": "bd_txn_price",`
- label literal at data/black_diamond/scripts/silver/scoped_price_exceptions.json:18: `"force_source": "bd_txn_price",`
- label literal at data/black_diamond/scripts/silver/scoped_price_exceptions.json:26: `"force_source": "bd_txn_price",`
- store write: data/black_diamond/scripts/silver/inject_scoped_overrides.py:253 (put_object in save(); main calls save at data/black_diamond/scripts/silver/inject_scoped_overrides.py:315)

### Callers / schedulers / docs naming the writer or its JSON (all repo hits in searched trees)
- COMMENT/DOC data/black_diamond/scripts/gold/aua_overrides.json:2: `"_description": "AUA valuation overrides for 05_build_client_performance.py. RC6 ghost account exclusions only. RC1/RC2 mispriced assets are fixed at `
- CODE data/black_diamond/scripts/gold/build_canonical_prices_v2.py:22: `6b. Auto-chain       -> inject_scoped_overrides.py --upload  (enforced in code)`
- CODE data/black_diamond/scripts/gold/build_canonical_prices_v2.py:68: `Path(__file__).resolve().parent.parent / 'silver' / 'inject_scoped_overrides.py'`
- CODE data/black_diamond/scripts/gold/build_canonical_prices_v2.py:482: `def _run_inject_scoped_overrides():`
- COMMENT/DOC data/black_diamond/scripts/gold/build_canonical_prices_v2.py:494: `print(f"\nERROR: inject_scoped_overrides.py not found at {INJECT_OVERRIDES_SCRIPT}")`
- COMMENT/DOC data/black_diamond/scripts/gold/build_canonical_prices_v2.py:496: `print("ERROR: run inject_scoped_overrides.py --upload manually to repair, "`
- COMMENT/DOC data/black_diamond/scripts/gold/build_canonical_prices_v2.py:511: `print(f"\nFATAL: inject_scoped_overrides.py (PROD) exited {e.returncode}")`
- CODE data/black_diamond/scripts/gold/build_canonical_prices_v2.py:670: `_run_inject_scoped_overrides()`
- CODE data/black_diamond/scripts/gold/build_canonical_prices_v2.py:689: `help='Skip auto-chained inject_scoped_overrides.py post-step. '`
- COMMENT/DOC data/black_diamond/scripts/gold/gold_dispatch.sh:668: `# build_canonical_prices_v2.py resolves inject_scoped_overrides.py via`
- COMMENT/DOC data/black_diamond/scripts/gold/gold_dispatch.sh:669: `# Path(__file__).parent.parent / 'silver' / 'inject_scoped_overrides.py'`
- COMMENT/DOC data/black_diamond/scripts/gold/gold_pipeline_deps.yaml:11: `- script: inject_scoped_overrides.py`
- COMMENT/DOC data/black_diamond/scripts/silver/bd_price_update.py:80: `# This is the SINGLE SOURCE OF TRUTH.  inject_scoped_overrides.py reads`
- COMMENT/DOC data/black_diamond/scripts/silver/scoped_price_exceptions.json:2: `"_description": "CUSIP-keyed scoped-exceptions blocklist. Hard-overrides canonical_prices for listed CUSIPs so Yahoo can NEVER re-price them off a cro`
- COMMENT/DOC data/cot/scripts/gold/aua_overrides.json:2: `"_description": "AUA valuation overrides for 05_build_client_performance.py. RC6 ghost account exclusions only. RC1/RC2 mispriced assets are fixed at `
- CODE data/cot/scripts/gold/build_canonical_prices_v2.py:24: `a scoped-override inject step. The manual price-pin / inject_scoped_overrides`
- COMMENT/DOC data/cot/scripts/gold/gold_dispatch.sh:500: `# build_canonical_prices_v2.py resolves inject_scoped_overrides.py via`
- COMMENT/DOC data/cot/scripts/gold/gold_dispatch.sh:501: `# Path(__file__).parent.parent / 'silver' / 'inject_scoped_overrides.py'`
- COMMENT/DOC data/cot/scripts/gold/gold_pipeline_deps.yaml:10: `# build_canonical_prices_v2 -> inject_scoped_overrides post-step. The scoped`
- CODE data/inf/scripts/gold/INF_build_canonical_prices.py:59: `Path(__file__).resolve().parent.parent / 'silver' / 'inject_scoped_overrides.py'`
- CODE data/inf/scripts/gold/INF_build_canonical_prices.py:340: `def _run_inject_scoped_overrides():`
- COMMENT/DOC data/inf/scripts/gold/INF_build_canonical_prices.py:342: `log(f'WARN: inject_scoped_overrides.py not found at {INJECT_OVERRIDES_SCRIPT}')`
- COMMENT/DOC data/inf/scripts/gold/INF_build_canonical_prices.py:346: `log('=== Step 6b: inject_scoped_overrides.py (v1 stub) ===')`
- COMMENT/DOC data/inf/scripts/gold/INF_build_canonical_prices.py:351: `log(f'FATAL: inject_scoped_overrides.py exited {e.returncode}')`
- COMMENT/DOC data/inf/scripts/gold/INF_build_canonical_prices.py:486: `log('\n  NOTE: --skip-inject passed; inject_scoped_overrides.py skipped (v1 stub ok)')`
- CODE data/inf/scripts/gold/INF_build_canonical_prices.py:488: `_run_inject_scoped_overrides()`
- CODE data/inf/scripts/gold/INF_build_canonical_prices.py:507: `help='Skip inject_scoped_overrides.py post-step (default for v1 stub)')`
- CODE data/inf/scripts/silver/inject_scoped_overrides.py:3: `inject_scoped_overrides.py -- INF Price Override Injector (v1 stub)`
- CODE data/inf/scripts/silver/inject_scoped_overrides.py:9: `positions with corrupt T1 prices), implement the BD inject_scoped_overrides`
- CODE data/inf/scripts/silver/inject_scoped_overrides.py:14: `python inject_scoped_overrides.py --upload    # no-op for v1`
- CODE data/inf/scripts/silver/inject_scoped_overrides.py:15: `python inject_scoped_overrides.py             # dry run (also no-op)`
- COMMENT/DOC data/inf/scripts/silver/inject_scoped_overrides.py:24: `print("inject_scoped_overrides: v1 stub -- no overrides to apply")`
- COMMENT/DOC infra/aws/terraform/bd-pipeline/CHANGELOG.json:4052: `"message": "0.4.0_DS_ClientPlatform: build_canonical_prices_v2 auto-chains inject_scoped_overrides",`
- COMMENT/DOC infra/aws/ec2/bd-gold-layer-runner/deploy-to-ec2.sh:19: `# inject_scoped_overrides.py) remain in code/silver/ on S3 as emergency`

cot-side hits (data/cot, cot-pipeline terraform): 5; any CODE-CALL among them: False

## 2. Inputs
- s3://opal-data-bd/silver/prices/canonical_prices.parquet (data/black_diamond/scripts/silver/inject_scoped_overrides.py:179; bucket data/black_diamond/scripts/silver/inject_scoped_overrides.py:54, key data/black_diamond/scripts/silver/inject_scoped_overrides.py:55) -> firm other:opal-data-bd
- repo file data/black_diamond/scripts/silver/scoped_price_exceptions.json (data/black_diamond/scripts/silver/inject_scoped_overrides.py:62) -> firm 49financial
- repo module data/black_diamond/scripts/silver/bd_price_update.py _SCOPED_PRICE_OVERRIDES (data/black_diamond/scripts/silver/inject_scoped_overrides.py:80) -> firm 49financial

Firm map (read from .tools/ds-precommit-check.py): {"_CROSS_FIRM_FOREIGN_BUCKETS": {"data/black_diamond/": ["opal-data-cot", "opal-data-cottonwood"], "data/cot/": ["opal-data-bd", "opal-data-inf", "opal-data-49financial", "opal-data-inflection"]}, "_CROSS_FIRM_FOREIGN_KEY_PREFIXES": {"data/black_diamond/": ["blackdiamond/cottonwood/"], "data/cot/": ["blackdiamond/49f/", "blackdiamond/49financial/"]}}

Runtime env note (cot runs set BD_S3_BUCKET to the cot bucket; the code default is the bd bucket):
- infra/aws/terraform/cot-pipeline/ssm.tf:233: "export BD_S3_BUCKET=opal-data-cot",
- infra/aws/terraform/cot-pipeline/ssm.tf:293: # Runs with BD_S3_BUCKET=opal-data-cot.
- infra/aws/terraform/cot-pipeline/ssm.tf:310: description   = "COT gold chain — syncs scripts from opal-data-cot/code/gold/ (cot's own git-versioned gold tree; NEVER 
- infra/aws/terraform/cot-pipeline/ssm.tf:331: "export BD_S3_BUCKET=opal-data-cot",
- data/cot/scripts/gold/gold_dispatch.sh:62: BD_S3_BUCKET="${BD_S3_BUCKET:-opal-data-cot}"

## 3. Outputs
- s3://opal-data-bd/silver/prices/canonical_prices.parquet by default (put_object data/black_diamond/scripts/silver/inject_scoped_overrides.py:253; --output-key data/black_diamond/scripts/silver/inject_scoped_overrides.py:266) -> writes cot bucket by default: False

## 4. Account ids covered by the exceptions
- account-id keys in JSON: none; lines matching account id/no/num: none
- the exceptions are keyed by CUSIP and asset_name only: [('05613L3H2', ['BNP PARIBAS SA']), ('95000U2D4', ['WELLS FARGO & CO 4.15% 01/24/2029']), ('651639AX4', ['NEWMONT CORP 2.8% 10/01/2029'])]
- no account id is present in the repo file, so no firm can be assigned to one from the repo.

## 5. Class
- class=cross_firm: input(s) not cot: s3://opal-data-bd/silver/prices/canonical_prices.parquet (data/black_diamond/scripts/silver/inject_scoped_overrides.py:179; bucket data/black_diamond/scripts/silver/inject_scoped_overrides.py:54, key data/black_diamond/scripts/silver/inject_scoped_overrides.py:55) (other:opal-data-bd); repo file data/black_diamond/scripts/silver/scoped_price_exceptions.json (data/black_diamond/scripts/silver/inject_scoped_overrides.py:62) (49financial); repo module data/black_diamond/scripts/silver/bd_price_update.py _SCOPED_PRICE_OVERRIDES (data/black_diamond/scripts/silver/inject_scoped_overrides.py:80) (49financial)

BD-TXN-TRACE writer=data/black_diamond/scripts/silver/inject_scoped_overrides.py:136 inputs=3 outputs=1 class=cross_firm
