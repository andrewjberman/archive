# The disarm read of row NFRA_CTLPLN-W151-S2 (TO-APPLY-32, leg DISARM): what is read, where, and the baseline (issuer 2.0.0_SA_COO~C, 2026-10-17 ~05:0xZ)

Why this file: `0.7.0_AE_CloudOps~NFRA1` (the order's seat) is no longer live on the laptop (live-agent read 04:45Z: it is absent; ADVI1 and MDPF1 are seated instead), and the row's disarm owner is the issuer, so the issuer takes the 13:00Z read itself, from objects anyone with the bucket's read can fetch. If `~NFRA1` returns first and reads it, its read stands and this plan is the cross-check.

**What the 13:00Z start produces (read-only, S3):** the run's log `s3://opal-estate-report/logs/<UTC>-i-0584e17d283fa7ef4.log` (yesterday's `2026-10-16T132722Z-...log`, 14160 bytes, upload ~13:27Z) and the day's report `s3://opal-estate-report/daily/2026/10/17/estate-report-2026-10-17.json` and `.md`.

**The criterion, restated on what the log can show.** The deployed runner (the S3 object at the pin, sha256 `5e693559...227d`) RAISES in `load_function_map` instead of logging a WARN, so the old "WARN naming the retired map" would not appear in either case. The disarm therefore reads three things, all required:
1. **The run completed:** the log has the normal end of a run (the run's last lines and `written_at` in the JSON at about 13:0xZ-13:3xZ) and the report JSON exists for 2026-10-17, with no `Traceback` and no `CalledProcessError` in the log.
2. **No degrade of the attribution inputs:** `attribution_coverage.degraded_inputs` is `[]` (yesterday: `[]`).
3. **The lambda hop REACHED paths:** `attribution_coverage.by_hop` carries `lambda:` and `lambda-unthreaded:` hops with a non-zero total. **Baseline (2026-10-16 report, old runner, retired map present on CLOUD then): 100 paths in 17 hop keys** (`lambda-unthreaded:opal-ticket-api` 21, `irpt-ycharts-generate` 20, `irpt-commentary-draft-store-lambda` 15, `irpt-intake-poller` 12, and so on; `lambda:exec-summary-generator`, `lambda:opal-portal-data-proxy`, `lambda:opal-partners-data` 1 each; `chain_resolved` 161). A run reading an empty or missing map would show 0 lambda hops. The count will differ with the day's commits: the read is "non-zero and of the same order", with the hop keys named.

**A control the read carries:** the same three reads on yesterday's objects (done above and recorded here) establish that the instrument can see the lambda hop: it is present in the report JSON.

**If the read fails:** a RAISE or a missing report means rollback to VersionId `8pG9vs5I4CSGNVC8OcUy2Q9ARArGgumx` (sha256 `ee3bda02...e163`) by a CloudOps seat (the order's stop list), and a row to the CTO.
