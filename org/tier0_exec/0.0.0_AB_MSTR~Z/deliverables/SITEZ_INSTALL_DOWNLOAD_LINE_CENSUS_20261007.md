# Site Z: install and download lines in tracked build and deploy scripts -- read-only census, 2026-10-07

By `0.0.0_AB_MSTR~Z`, asked by `1.0.0_SA_CTO~Z` msg 31229. Nothing was run and nothing was fetched.

## Denominator

- Scope: git-tracked files under infra, .tools, data, integrations, lib ending in .sh .ps1 .cmd .bat .py .tf .yml .yaml .mjs .js: **7270 files** read (0 unreadable). The `portal` submodule is NOT in scope.
- PACKAGE-INSTALL pattern (bun install/add/x, bunx, npm install/ci, npx, yarn, pnpm, pip install/download, uv pip, choco, winget, docker pull): **172 lines in 107 files**.
- NETWORK-FETCH pattern (curl, wget, Invoke-WebRequest, Invoke-RestMethod, Start-BitsTransfer, iwr): **106 lines in 61 files**. Counted only: most call an Opal or AWS endpoint and are not a package fetch, and they were not read one by one.

## What this census is not

- The class of a file is assigned from its PATH, not from reading it. Class A is the list to read first.
- A match is a line of text. A comment, an echo or a refusal message that names `pip install` matches too.
- A script that fetches through a different verb (a Python `urllib` call, `git clone`, an SDK download) is not matched.
- Untracked and gitignored scripts are not in scope.

## Package-install lines, by class

### A. build / deploy / run scripts (by path, a seat may run these ON this box) -- 79 lines in 54 files

- `data/demo/scripts/run_demo_reclone.sh:29` -- `pip3 install --quiet psutil 2>&1 || echo "WARN: psutil install failed (telemetry -> wall-time-only)"`
- `data/inf/scripts/classification/classify_assets.py:295` -- `"openai package not installed. pip install openai. "`
- `data/seeking-alpha/scripts/backfill.sh:13` -- `echo "Then: source venv/bin/activate && pip install playwright boto3"`
- `infra/aws/ec2/astn-wsjft/deploy.sh:17` -- `echo "=== npm install (playwright) as ec2-user ==="`
- `infra/aws/ec2/astn-wsjft/deploy.sh:18` -- `su - ec2-user -c "cd $DEST && npm install --no-audit --no-fund 2>&1 | tail -4"`
- `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh:80` -- `pip3 install polars --quiet 2>&1 | tee -a "$LOG_FILE" || log "WARN: polars install failed (continuing; gold scripts using polars will error explicitly)"`
- `infra/aws/ec2/bd-gold-layer-runner/run-gold-layer.sh:85` -- `pip3 install psutil --quiet 2>&1 | tee -a "$LOG_FILE" || log "WARN: psutil install failed (continuing; gold_prof.py will fall back to wall-time-only)"`
- `infra/aws/ec2/inf-gold-layer-runner/run-gold-layer.sh:68` -- `pip3 install psutil --quiet 2>&1 | tee -a "$LOG_FILE" || log "WARN: psutil install failed (continuing; gold_prof.py falls back to wall-time-only)"`
- `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:193` -- `"$PY" -m pip install --quiet "pandas_market_calendars<5" 2>&1 \`
- `infra/aws/ec2/mdpf-daily-runner/mdpf-daily-dispatch.sh:493` -- `"$PY" -m pip install --quiet pyarrow 2>&1 | grep -v "^$" || true`
- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh:207` -- `( cd "$MCPORTAL_DIR" && bun install --frozen-lockfile && bun run build )`
- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh:303` -- `sudo -u ec2-user ${REMOTE_DIR}/.venv/bin/pip install --progress-bar off --upgrade pip`
- `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh:304` -- `sudo -u ec2-user ${REMOTE_DIR}/.venv/bin/pip install --progress-bar off -r requirements.txt`
- `infra/aws/ec2/smartx-exporter/build-and-deploy.sh:69` -- `echo "  docker pull $ECR_REPO:$IMAGE_TAG"`
- `infra/aws/ec2/smartx-exporter/run-all-portfolios.sh:120` -- `if docker pull "$IMAGE" 2>&1 | tee -a "$LOG_FILE"; then`
- `infra/aws/lambda/bd-pipeline/bd-allocation-processor/deploy.sh:37` -- `pip3 install -q --target "$TEMP_DIR" openpyxl`
- `infra/aws/lambda/daily_agenda_generator/package/urllib3/contrib/pyopenssl.py:20` -- `$ python -m pip install pyopenssl cryptography idna`
- `infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:658` -- `"npx --yes playwright install chromium || true ) && "`
- `infra/aws/lambda/historical-prices-scheduler/lambda_function.py:54` -- `pip install --quiet 'numpy<2' 'pandas<2.1' 'pyarrow<15' boto3 yfinance 2>&1 | tail -3`
- `infra/aws/lambda/layers/anthropic-sdk-deps/build-layer.ps1:34` -- `Write-Host "'n--- pip download manylinux2014_x86_64 / cp312 wheels ---"`
- `infra/aws/lambda/layers/anthropic-sdk-deps/build-layer.ps1:35` -- `python -m pip download '`
- `infra/aws/lambda/layers/anthropic-sdk-deps/build-layer.ps1:43` -- `if ($LASTEXITCODE -ne 0) { throw "pip download failed" }`
- `infra/aws/lambda/layers/find-insure-browser-deps/build-layer.sh:21` -- `# 'pip install --platform manylinux2014_x86_64 --python-version 3.9`
- `infra/aws/lambda/layers/find-insure-browser-deps/build-layer.sh:64` -- `pip install \`
- `infra/aws/lambda/layers/find-insure-deps/build-layer.sh:17` -- `# (Linux/python3.9) requires 'pip install --platform manylinux2014_x86_64`
- `infra/aws/lambda/layers/find-insure-deps/build-layer.sh:55` -- `pip install \`
- `infra/aws/lambda/layers/find-insure-parse-deps/build-layer.sh:18` -- `# Windows for Lambda (Linux/python3.9) requires 'pip install --platform`
- `infra/aws/lambda/layers/find-insure-parse-deps/build-layer.sh:53` -- `pip install \`
- `infra/aws/lambda/layers/irpt-common/build_layer.py:299` -- `raise SystemExit("ERROR: pip install failed rc=%d" % proc.returncode)`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/fsspec/implementations/smb.py:49` -- `$ pip install smbprotocol`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/fsspec/implementations/smb.py:51` -- `# pip install smbprotocol[kerberos]`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/numpy/f2py/setup.py:6` -- `pip install .`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/numpy/lib/utils.py:69` -- `" Install it by 'pip install threadpoolctl'."`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/config.py:1007` -- `Python 3.10 and older don't support exception groups natively. <=3.10, backport must be installed: 'pip install exceptiongroup'.`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/networks.py:968` -- `raise ImportError("email-validator is not installed, run 'pip install 'pydantic[email]''") from e`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/networks.py:970` -- `raise ImportError('email-validator version >= 2.0 required, run pip install -U email-validator')`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/networks.py:984` -- `pip install email-validator`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/networks.py:1029` -- `pip install email-validator`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/v1/env_settings.py:332` -- `raise ImportError('python-dotenv is not installed, run 'pip install pydantic[dotenv]'') from e`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pydantic/v1/networks.py:580` -- `raise ImportError('email-validator is not installed, run 'pip install pydantic[email]'') from e`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/avro/codecs/snappy_codec.py:65` -- `raise ImportError("Snappy support not installed, please install using 'pip install pyiceberg[snappy]'")`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/avro/codecs/snappy_codec.py:69` -- `raise ImportError("Snappy support not installed, please install using 'pip install pyiceberg[snappy]'")`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/avro/codecs/zstandard_codec.py:49` -- `raise ImportError("Zstandard support not installed, please install using 'pip install pyiceberg[zstandard]'")`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/avro/codecs/zstandard_codec.py:53` -- `raise ImportError("Zstandard support not installed, please install using 'pip install pyiceberg[zstandard]'")`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/catalog/__init__.py:132` -- `raise NotInstalledError("Apache Hive support not installed: pip install 'pyiceberg[hive]'") from exc`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/catalog/__init__.py:141` -- `raise NotInstalledError("AWS glue support not installed: pip install 'pyiceberg[glue]'") from exc`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/catalog/__init__.py:150` -- `raise NotInstalledError("AWS DynamoDB support not installed: pip install 'pyiceberg[dynamodb]'") from exc`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/catalog/__init__.py:160` -- `"SQLAlchemy support not installed: pip install 'pyiceberg[sql-postgres]' or pip install 'pyiceberg[sql-sqlite]'"`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyiceberg/io/__init__.py:372` -- `'Could not load a FileIO, please consider installing one: pip3 install "pyiceberg[pyarrow]", for more options refer to the docs.'`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/pyparsing/core.py:2570` -- `"must ''pip install pyparsing[diagrams]'' to generate parser railroad diagrams"`
- `infra/aws/lambda/layers/pyiceberg-nessie-deps/python/urllib3/contrib/pyopenssl.py:20` -- `$ python -m pip install pyopenssl cryptography idna`
- `infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:15` -- `pip install -t . into the package).`
- `infra/aws/lambda/news_ingestion_scheduler/deploy.sh:19` -- `pip install -r requirements.txt -t package/`
- `infra/aws/lambda/news_layer3_curation/deploy.sh:40` -- `pip install openai -t package/ --quiet`
- `infra/aws/lambda/news_layer3_curation/lambda_function.py:37` -- `print("WARNING:  OpenAI SDK not installed. Run: pip install openai")`
- `infra/aws/lambda/news_trending_analysis/deploy.sh:44` -- `pip install -r requirements.txt -t package/ --quiet`
- `infra/aws/lambda/portal_data_proxy/deploy.sh:26` -- `pip install openai -t _build_tmp/ --quiet --no-cache-dir`
- `infra/aws/lambda/portfolio_excel_generator/deploy.sh:9` -- `#   - 'pip install -t .' inline vendoring -- Rule 3 violation (deps go in Lambda`
- `infra/aws/lambda/seeking-alpha-analysis-scraper/deploy.sh:18` -- `pip install -r requirements.txt -t package/ --quiet`
- `infra/aws/lambda/semantic-news-layer3-curation/deploy.sh:26` -- `pip install -r requirements.txt -t package/ --quiet`
- `infra/aws/lambda/semantic-trending-topics-portal-publisher/deploy.sh:26` -- `pip install -r requirements.txt -t package/ --quiet`
- `infra/aws/lambda/trending_image_generator/deploy.sh:22` -- `pip install -r requirements.txt -t package/ --quiet`
- `infra/aws/lambda/trending_image_selector/deploy.sh:19` -- `pip install -r requirements.txt -t deps`
- `infra/aws/lambda/v2_portal/07_macroeconomics/lambdas/opal-portal-volatility-fetcher/deploy.sh:35` -- `pip install \`
- `infra/aws/lambda/v2_portal/yang_pipeline/outputs/generate-volatility/deploy.sh:10` -- `pip install -r "$FUNCTION_PATH/requirements.txt" -t "$BUILD_DIR" --quiet`
- `infra/aws/opalinvest_dev/lambda/session-analytics/deploy.sh:20` -- `npm install --production=false`
- `infra/aws/opalinvest_dev/scripts/deployment/deploy-lambda.sh:20` -- `npm install`
- `infra/aws/opalinvest_dev/scripts/deployment/deploy-portal.sh:26` -- `npx vite build`
- `infra/aws/scripts/build_smartx_lambda.sh:34` -- `pip install pandas pyarrow boto3 -t /build/`
- `infra/aws/terraform/harvest/build-and-upload-print-deps-layer.sh:26` -- `# NOTHING IS INSTALLED. 'pip download' fetches wheels into a scratch directory for a platform`
- `infra/aws/terraform/harvest/build-and-upload-print-deps-layer.sh:59` -- `python -m pip download --quiet --disable-pip-version-check --no-deps \`
- `infra/aws/terraform/harvest/build-and-upload-print-deps-layer.sh:62` -- `echo "VENDOR: pip download (cp311 manylinux2014_x86_64) -> $(ls "$WHEELS" | wc -l) wheel(s)"`
- `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh:130` -- `# Its sha256 is whatever this pip download prints; it is recorded on the NEVER-2 entry leg SHA`
- `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh:135` -- `python -m pip download --quiet --disable-pip-version-check --no-deps \`
- `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh:138` -- `echo "VENDOR: pip download $VENDOR_PINS (cp311 manylinux2014_x86_64) -> $(ls "$WHEELS" | tr '\n' ' ')"`
- `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh:560` -- `python -m pip download --quiet --disable-pip-version-check --no-deps --only-binary=:all: \`
- `infra/aws/terraform/harvest/lambda_src/build_zip.py:297` -- `"FATAL: pip download of %s failed rc=%d: %s"`
- `infra/aws/terraform/harvest/lambda_src/build_zip.py:302` -- `raise SystemExit("FATAL: pip download of %s produced no wheel" % (_VENDOR_PINS,))`
- `infra/aws/users/lambda/portal-authorizer/deploy.sh:24` -- `npm install --production`

### B. instance bootstrap (user-data, setup, Terraform text): by path, runs ON an AWS instance -- 46 lines in 30 files

- `infra/aws/ec2/bd-exporter/terraform/scripts/beast_user_data.sh:16` -- `pip3 install pandas pyarrow openpyxl`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:12` -- `#      copied to /home/ec2-user/.cache/ms-playwright (bunx needs node for`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:14` -- `#   5. /opt/bd-exporter initialized with package.json + bun install`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:47` -- `# we install them via dnf directly because 'bunx playwright install-deps'`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:62` -- `python3 -m pip install --target=/usr/lib/python3.9/site-packages/ \`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:99` -- `~/.bun/bin/bun install`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:105` -- `# Install chromium for root (bunx can run playwright's own JS install script`
- `infra/aws/ec2/bd-exporter/terraform/scripts/uploader_user_data.sh:108` -- `~/.bun/bin/bunx playwright install chromium`
- `infra/aws/ec2/bd-gold-detail-generator/user-data-snapshot-generation.sh:25` -- `python3.11 -m pip install --upgrade pip`
- `infra/aws/ec2/bd-gold-detail-generator/user-data.sh:25` -- `python3.11 -m pip install --upgrade pip`
- `infra/aws/ec2/bd-gold-layer-runner/launch-instance.sh:33` -- `pip3 install awscli boto3 pandas pyarrow python-dateutil --quiet`
- `infra/aws/ec2/bd-gold-layer-runner/setup-instance.sh:20` -- `pip3 install pandas pyarrow boto3 python-dateutil \`
- `infra/aws/ec2/bd-gold-qa-runner/setup-instance.sh:23` -- `pip3 install pandas pyarrow boto3 python-dateutil \`
- `infra/aws/ec2/canonical-schwab-runner/setup-instance.sh:21` -- `pip3 install awscli boto3 pandas pyarrow --quiet`
- `infra/aws/ec2/canonical-schwab-runner/user-data.sh:23` -- `pip3 install awscli --quiet`
- `infra/aws/ec2/canonical-schwab-si2/bootstrap.ps1:37` -- `& "$py\python.exe" -m pip install --no-warn-script-location cryptography boto3 *> "$base\pip.log"`
- `infra/aws/ec2/consolidation-gold-runner/setup-instance.sh:15` -- `pip3 install --quiet boto3 pandas pyarrow`
- `infra/aws/ec2/consolidation-gold-runner/setup-instance.sh:30` -- `# aws resolves via systemd's default PATH (pip3 installs to /usr/local/bin -- the maiden boot`
- `infra/aws/ec2/consolidation-gold-runner/user-data.sh:24` -- `pip3 install awscli --quiet`
- `infra/aws/ec2/cot-exporter/user-data.sh:22` -- `python3.11 -m pip install --upgrade pip`
- `infra/aws/ec2/cot-exporter/user-data.sh:23` -- `python3.11 -m pip install \`
- `infra/aws/ec2/github-actions-runner/user-data.sh:52` -- `su - "$RUNNER_USER" -c 'curl -fsSL https://bun.sh/install | bash' || log "WARN: bun install non-zero"`
- `infra/aws/ec2/inf-bronze-runner/user-data.sh:27` -- `# Use pip first as a fallback so 'pip3 install python-dateutil' for awscli-1 path`
- `infra/aws/ec2/inf-bronze-runner/user-data.sh:29` -- `pip3 install --quiet python-dateutil`
- `infra/aws/ec2/inf-bronze-runner/user-data.sh:34` -- `pip3 install boto3 pandas pyarrow requests --quiet`
- `infra/aws/ec2/inf-exporter/user-data.sh:20` -- `python3 -m pip install --target=/usr/lib/python3.9/site-packages/ \`
- `infra/aws/ec2/inf-exporter/user-data.sh:47` -- `~/.bun/bin/bun install`
- `infra/aws/ec2/inf-exporter/user-data.sh:50` -- `~/.bun/bin/bunx playwright install chromium`
- `infra/aws/ec2/inf-gold-layer-runner/user-data.sh:10` -- `pip3 install boto3 pandas pyarrow python-dateutil psutil --quiet`
- `infra/aws/ec2/inf-gold-qa-runner/user-data.sh:35` -- `pip3 install boto3 pandas pyarrow python-dateutil --quiet`
- `infra/aws/ec2/mdpf-daily-runner/user-data.sh:34` -- `# botocore a 'pip install' can clobber) satisfies that test and would skip the`
- `infra/aws/ec2/mdpf-daily-runner/user-data.sh:48` -- `python3 -m pip install --upgrade pip >/dev/null 2>&1 || true`
- `infra/aws/ec2/mdpf-daily-runner/user-data.sh:49` -- `python3 -m pip install boto3 pandas pyarrow requests "pandas_market_calendars<5" >/dev/null 2>&1`
- `infra/aws/terraform/astn-pipeline/instance.tf:69` -- `python3 -m pip install --upgrade boto3`
- `infra/aws/terraform/cot-pipeline/ssm.tf:347` -- `"python3.11 -m pip install -q 'pandas==2.2.3' 'numpy==1.26.4' 'pyarrow==16.1.0' polars psutil 2>&1 | tee -a $LOG_FILE || true",`
- `infra/aws/terraform/estate-report/instance.tf:122` -- `python3 -m pip install --upgrade boto3 kuzu`
- `infra/aws/terraform/etfs-reports/instance.tf:66` -- `python3 -m pip install --upgrade boto3`
- `infra/aws/terraform/fred-pipeline/lambdas.tf:76` -- `# (py3.11) -- CLAUDE.md Rule 3 (reuse a layer; no pip install -t .). boto3 is in`
- `infra/aws/terraform/globgrph/item2b.tf:119` -- `# Build (Linux wheels only — Windows pip install produces .pyd files that fail on Lambda):`
- `infra/aws/terraform/globgrph/item2b.tf:120` -- `#   pip install --platform manylinux2014_x86_64 --implementation cp --python-version 312 --only-binary=:all: -t python/ -r requirements.txt`
- `infra/aws/terraform/globgrph/stitch-produce.tf:155` -- `- 'pip install -q boto3 pyyaml || true'`
- `infra/aws/terraform/investor-reporting/export/main.tf:100` -- `# EXISTING YCharts app directory, read ONLY for its node_modules, because 'npm install' on`
- `infra/aws/terraform/investor-reporting/ycharts/ssm.tf:45` -- `"cd $APP_DIR && npm install --omit=dev",`
- `infra/aws/terraform/investor-reporting/ycharts/ssm.tf:46` -- `"cd $APP_DIR && npx playwright install chromium",`
- `infra/aws/terraform/portal-auth/session-analytics.tf:20` -- `# THE SOURCE PROVABLY IS PRODUCTION. Two clean builds (npm ci against the`
- `infra/aws/terraform/shared-infra/drift-producer.tf:200` -- `- 'pip install -q boto3 || true'`

### C. tooling and lint (.tools, infra/linting) -- 18 lines in 8 files

- `.tools/commit-gate.sh:46` -- `# Ruff: install via 'pip install ruff'. Pinned version: 0.15.11 (ADHC_DSFLOW.004).`
- `.tools/directives-check.py:43` -- `print("ERROR: PyYAML missing -- directives-check needs it (pip install pyyaml)", file=sys.stderr)`
- `.tools/frontend-dev.py:48` -- `print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)`
- `.tools/orion-inspector.py:42` -- `print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)`
- `.tools/owned-paths-validate.py:259` -- `"ERROR: PyYAML is required. Install: pip install pyyaml"`
- `.tools/wk-provision.sh:36` -- `portal's bunfig.toml: bun install contacts the package registry, and no request may leave this machine.`
- `.tools/wk-provision.sh:81` -- `refuse 2 "--node-modules install runs bun install, which contacts the package registry, and no request may leave this machine; use --node-modules link (the default) or --`
- `.tools/wk-provision.sh:192` -- `( cd "$portal_dir" && bun install --frozen-lockfile ) || die 1 "bun install failed in $portal_dir"`
- `infra/linting/fixers/fix-unused-vars.js:18` -- `const output = execSync('npx eslint "${targetPath}" --format=json', {`
- `infra/linting/smart-lint.sh:98` -- `if command -v npx &> /dev/null && [[ -f "tsconfig.json" ]]; then`
- `infra/linting/smart-lint.sh:99` -- `TS_COUNT=$(npx tsc --noEmit 2>&1 | grep "error TS" | wc -l || echo "0")`
- `infra/linting/smart-lint.sh:129` -- `npx eslint "$TARGET_PATH" --fix --quiet 2>/dev/null || true`
- `infra/linting/smart-lint.sh:133` -- `if npx tsc --noEmit 2>&1 | grep -q "error TS"; then`
- `infra/linting/smart-lint.sh:142` -- `log_info "[DRY RUN] Would run: npx eslint --fix"`
- `infra/linting/smart-lint.sh:160` -- `log_info "Install: pip install black"`
- `infra/linting/smart-lint.sh:233` -- `if npx tsc --noEmit 2>&1 | grep -q "error TS"; then`
- `infra/linting/smart-lint.sh:267` -- `if npx tsc --noEmit 2>&1 | grep -q "error TS"; then`
- `infra/linting/smart-lint.sh:268` -- `METRICS[ts_errors_after]=$(npx tsc --noEmit 2>&1 | grep -c "error TS" || echo "0")`

### D. tests -- 5 lines in 3 files

- `.tools/tests/test_wk_provision_no_registry.py:7` -- `is never started and no bun install ever runs.`
- `infra/aws/ec2/historical-prices/test_historical_prices_scheduler.py:517` -- `"""User-data creates a virtualenv for pip install."""`
- `infra/aws/ec2/historical-prices/test_historical_prices_scheduler.py:521` -- `"""pip install does NOT use --ignore-installed (breaks system aws CLI)."""`
- `infra/aws/terraform/nfra-ctlpln-identity/tests/derive_ssm_documents.py:377` -- `"""Lines of a document's steps that fetch something at run time (s3 cp/sync, curl, wget, git clone, pip/npm install)."""`
- `infra/aws/terraform/nfra-ctlpln-identity/tests/derive_ssm_documents.py:576` -- `print("FETCHED-AT-RUN-TIME (resident and export documents; s3 cp/sync, curl, wget, git clone, pip/npm install, npx):")`

### E. vendored library text (a package's own files, not a script of ours) -- 24 lines in 12 files

- `infra/aws/lambda/infrastructure_monitor/httpcore/_async/__init__.py:15` -- `"installed. Use 'pip install httpcore[http2]'."`
- `infra/aws/lambda/infrastructure_monitor/httpcore/_async/__init__.py:27` -- `"installed. Use 'pip install httpcore[socks]'."`
- `infra/aws/lambda/infrastructure_monitor/httpcore/_sync/__init__.py:15` -- `"installed. Use 'pip install httpcore[http2]'."`
- `infra/aws/lambda/infrastructure_monitor/httpcore/_sync/__init__.py:27` -- `"installed. Use 'pip install httpcore[socks]'."`
- `infra/aws/lambda/infrastructure_monitor/httpx/__init__.py:24` -- `"everything with: pip install 'httpx[cli]'"`
- `infra/aws/lambda/infrastructure_monitor/httpx/_client.py:682` -- `"Make sure to install httpx using 'pip install httpx[http2]'."`
- `infra/aws/lambda/infrastructure_monitor/httpx/_client.py:1396` -- `"Make sure to install httpx using 'pip install httpx[http2]'."`
- `infra/aws/lambda/infrastructure_monitor/httpx/_decoders.py:112` -- `Requires 'pip install brotlipy'. See: https://brotlipy.readthedocs.io/`
- `infra/aws/lambda/infrastructure_monitor/httpx/_decoders.py:113` -- `or   'pip install brotli'. See https://github.com/google/brotli`
- `infra/aws/lambda/infrastructure_monitor/httpx/_decoders.py:123` -- `"Make sure to install httpx using 'pip install httpx[brotli]'."`
- `infra/aws/lambda/infrastructure_monitor/httpx/_decoders.py:165` -- `Requires 'pip install zstandard'.`
- `infra/aws/lambda/infrastructure_monitor/httpx/_decoders.py:166` -- `Can be installed as a dependency of httpx using 'pip install httpx[zstd]'.`
- `infra/aws/lambda/infrastructure_monitor/httpx/_decoders.py:174` -- `"Make sure to install httpx using 'pip install httpx[zstd]'."`
- `infra/aws/lambda/infrastructure_monitor/httpx/_transports/default.py:193` -- `"Make sure to install httpx using 'pip install httpx[socks]'."`
- `infra/aws/lambda/infrastructure_monitor/httpx/_transports/default.py:337` -- `"Make sure to install httpx using 'pip install httpx[socks]'."`
- `infra/aws/lambda/infrastructure_monitor/openai/_extras/_common.py:11` -- `$ pip install openai[{extra}]`
- `infra/aws/lambda/infrastructure_monitor/pydantic/config.py:1004` -- `Python 3.10 and older don't support exception groups natively. <=3.10, backport must be installed: 'pip install exceptiongroup'.`
- `infra/aws/lambda/infrastructure_monitor/pydantic/networks.py:967` -- `raise ImportError("email-validator is not installed, run 'pip install 'pydantic[email]''") from e`
- `infra/aws/lambda/infrastructure_monitor/pydantic/networks.py:969` -- `raise ImportError('email-validator version >= 2.0 required, run pip install -U email-validator')`
- `infra/aws/lambda/infrastructure_monitor/pydantic/networks.py:983` -- `pip install email-validator`
- `infra/aws/lambda/infrastructure_monitor/pydantic/networks.py:1028` -- `pip install email-validator`
- `infra/aws/lambda/infrastructure_monitor/pydantic/v1/env_settings.py:332` -- `raise ImportError('python-dotenv is not installed, run 'pip install pydantic[dotenv]'') from e`
- `infra/aws/lambda/infrastructure_monitor/pydantic/v1/networks.py:580` -- `raise ImportError('email-validator is not installed, run 'pip install pydantic[email]'') from e`
- `infra/aws/lambda/infrastructure_monitor/tqdm/contrib/slack.py:17` -- `raise ImportError("Please 'pip install slack-sdk'")`

## Package-install lines by verb

- pip: 114
- pip3: 20
- npx: 12
- npm: 10
- bun: 9
- bunx: 5
- docker: 2
