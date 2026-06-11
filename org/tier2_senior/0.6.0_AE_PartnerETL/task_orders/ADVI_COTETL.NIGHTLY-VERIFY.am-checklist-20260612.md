# AM Verify Checklist — ADVI_COTETL.NIGHTLY-VERIFY (execute 2026-06-12 AM)

Pre-staged 2026-06-11 per COO 195951Z item-2. Tonight's chain: 02:00Z
`cot-bd-session-daily` (cron) → session-fetch SSM on cot runner →
`cot-session-complete` (CHAIN-FIX v0.4.1 entry trigger) → bronze-run →
`cot-bronze-complete` → silver → `cot-silver-complete` → gold.
All 4 EB rules pre-verified ENABLED 2026-06-11 ~19:35Z.

**Tooling note: comp-pipescript deployed is BLIND to opal-data-cot** (bd-only).
Use direct S3 checks + Lambda/SSM logs for the cot leg. (Rule 20: read-only
verification — no graph-gated change involved; comp-kuzu available for any
dependency question that comes up.)

## 1. Chain fired (mechanism)
```bash
# session-fetch SSM command ~02:00-02:05Z success
aws ssm list-commands --filters key=DocumentName,value=AWS-RunShellScript --max-items 20 \
  --query 'Commands[?starts_with(RequestedDateTime,`2026-06-12`)].[CommandId,Status,RequestedDateTime]'
# trigger Lambda fired bronze-run shortly after (CloudWatch)
aws logs filter-log-events --log-group-name /aws/lambda/cot-bd-daily-trigger \
  --start-time $(date -d '2026-06-12T01:55' +%s)000 --filter-pattern bronze-run --max-items 10
```
PASS = session SSM Success ~02:00Z AND bronze-run dispatched seconds-to-minutes
after (NOT a 30-min gap — that was the TTL bug). FAIL+no-fire = check
cot-session-complete rule matched (detail-type per memory: `EC2 Command Status-change
Notification`, field `document-name` hyphenated; verify via `aws events test-event-pattern`).

## 2. Artifacts fresh (the actual bar — EXISTS/FRESH/SCALED/NOT-FROZEN)
```bash
for p in bronze silver gold; do aws s3 ls s3://opal-data-cot/$p/ --recursive \
  | sort -k1,2 | tail -3; done
```
PASS = all 3 tiers carry 2026-06-12 ~02:0xZ+ objects; gold ADVANCES past the
06-09 22:26Z stale point. All 5 bronze templates present (allocations/holdings/
realized/transactions/unrealized) — a 401 night produces 0-template bronze.
Sanity: object sizes same order of magnitude as last good run (06-09).

## 3. D_04 ownership_map (PRTORG sibling dep)
```bash
aws s3api head-object --bucket opal-data-cot --key <platinum cottonwood ownership_map key>
```
(Resolve exact key from the cot gold script tree / last good run listing first.)
PASS = LastModified 2026-06-12 + nonzero size. → unblocks ADVI_PRTORG.AC-CLOSEOUT
AC1/AC4/AC7.

## 4. Validation
comp-validate: check a cot gold validate config exists; NO_CONFIG = UNVALIDATED
(NOT a pass, fail-closed per COMP_VALIDATE_PROTOCOL §10.1) — if NO_CONFIG, note
explicitly in the RAVC2, do not claim validated.

## 5. Close
- PASS → RAVC2-COMPLETE → COO + CTO (chain evidence + artifact LastModified
  table) → flip ADVI_COTETL.NIGHTLY-VERIFY `<status>complete</status>`.
- Then execute ADVI_PRTORG.AC-CLOSEOUT AC1/AC4/AC7 against fresh ownership_map.
- FAIL → root-cause from chain logs (cot runner SSM output + trigger Lambda),
  classify (session/template/trigger), RAVC2 finding → COO+CTO. Do NOT manually
  re-dispatch without checking the gate semantics (a Lambda re-invoke may DEFER
  on the sentinel date — see MDPF recovery precedent work_1337Z 06-10).

## Also due same AM (GLDINC workstream)
- gold/_parity/fee_rate_history/2026-06-12/scorecard.json — night-1 A_02 nightly
  shadow (dispatcher hook f78977825). identical=true expected; counts toward
  clean-night cutover evidence.
- gold/_parity/load_flows/ scorecard — first POST-FIX night for DS's c560e4ca9
  (1440 gap should close; clean_night_counter 0→1 if cache-read engages). DS-led.
