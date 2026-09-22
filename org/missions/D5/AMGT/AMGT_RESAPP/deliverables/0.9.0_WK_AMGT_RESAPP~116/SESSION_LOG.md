# SESSION LOG -- 0.9.0_WK_AMGT_RESAPP~116 -- AMGT_RESAPP.TO-AMGT-rk-116 (this session)

Worktree: C:/tmp/wk-amgt-30-116b, branch wk-amgt-30-116b, base carries BOTH signed never-widen pair halves
(the CTO half was absent in this cell's FIRST worktree, wk-amgt-30-116, and that predecessor session STOPPED
correctly at AC0 with BLOCKING row AMGT_RESAPP-Z-W116-S1; it also filed AMGT_RESAPP-Z-W116-S2 on
bbg_credentials.py's username-in-cleartext defect. Both rows are already merged to SITEZ; this session
continues from S3).

## What this order was

AMGT-rk-116 (L-MB) -- the Bloomberg model-block PULL + DERIVE for Lenovo `992 HK Equity`: 5 Bloomberg
requests (1 refdata, 1 histdata, 3 bestdata) plus the READ_HERE/dapi_check login probe = 6 total, 60
security-field points, 1 unique security, under a signed never-widen pair naming Lenovo's served keys as
the entire blast radius. Lands the FIRST bestdata object ever for Lenovo and one new served
`derived/model_block/992_HK_Equity/<stamp>/model_block.json` carrying rk-109's `fiscal_year_join`
(31 March FYE, non-December path) and rk-112's currency labels.

## What was done

1. Printed `git rev-parse --abbrev-ref HEAD` (wk-amgt-30-116b) and `test -d org && test -d .tools`: TREE-OK.
   Confirmed `integrations/bloomberg/research/model_block_pull.py`, `integrations/bloomberg/READ_HERE.md`
   and `integrations/bloomberg/auth/dapi_check.py` all present.
2. Confirmed both never-widen pair halves on file: `ledger/NEVER_WIDEN_ROUND30_RK116_COO_HALF.md` (committed
   by `2.0.0_SA_COO~Z` at the round-30 issuance @bf5c280e48, its own commit hash is the signature's vintage)
   and `ledger/NEVER_WIDEN_ROUND30_RK116_CTO_HALF.md` (Status: SIGNED, `1.0.0_SA_CTO~Z`, ~19:4xZ). Read both
   in full: matching blast radius (Lenovo's keys only; 12 other non-December names named, none touched),
   matching rollback discipline (no delete, ever).
3. Ran AC0: `pair_coo True pair_cto True`; `fye_join_wired True currency_labels_wired True`; SIZED line
   re-derived from the module's own constants, matching the order's stated 6-total/60-point sizing exactly;
   credential check OK (username redacted in every recorded artifact per the spawn instruction and row S2);
   DAPI: UP. No sign-in attempted. PASS.
   - Fixed a script-mechanics issue in the order's own `.scratch/r116/ac0.py` template: running it as a
     script (not `-m`) leaves cwd off `sys.path`, so `model_block_pull.py`'s `from lib.research.harvest
     import bloomberg` raised `ModuleNotFoundError`. Added `sys.path.insert(0, os.getcwd())` to the scratch
     harness (never to producer code); output otherwise identical to the order's literal script.
4. Ran AC1: pre-counts matched the issuer's measured-at-the-cut values exactly (refdata 1, histdata 1,
   bestdata 0, pull_log 0, derived 3, ledger_entries 1); `--dry-run` printed 5 DRY-RUN PULL lines naming
   exactly `992 HK Equity`, 0 written. PASS.
   - Found (surprise row S3): the dry-run's own printed fourth write key is `amgt/harvest/state/pull_log/...`,
     not `bloomberg/harvest/state/pull_log/...` as the order's W4 and both pair halves state.
     `_state_pull_log_prefix` (model_block_pull.py:389-391) hardcodes the literal string `"amgt"` instead of
     the module's `VENDOR="bloomberg"` constant that the bronze writer uses. Re-pointed `ac1.py`/`ac3.py`'s
     pull_log reads at the real prefix so the pre/post count measures the key that actually moves (grain
     match); filed row AMGT_RESAPP-Z-W116-S3 (OBSERVATION/INERT, no blast-radius violation -- still scoped
     to opal-data-harvest and security_key=992_HK_Equity only).
5. Opened the deploy ledger (`amgt-rk116-lenovo-model-block`, 4 legs) after AC1, before the live act.
   - Found (surprise row S4): the order's literal leg-kind token for w5, `s3-key`, is not a member of
     `deploy_ledger.py`'s `LEG_KINDS` enum (`{git, s3-prefix, activation, ec2-baked-asset, verify, tf-lambda}`);
     the literal open command exits rc=1. Substituted kind `verify` for leg w5 (closest semantic fit: a
     post-deploy served-artifact read, matching what AC3's ledger read-back actually proves); all other legs
     used the order's kinds unchanged. Open succeeded, rc=0. Filed row AMGT_RESAPP-Z-W116-S4
     (BLOCKING/INERT -- blocking the literal command, not the mission; resolved by the substitution).
6. Ran AC2, THE ONE LIVE ACT: pull then derive, both naming exactly `992 HK Equity`. PULL landed raw stamp
   `20260922T201211Z` (4 keys: refdata, histdata, bestdata, pull_log). DERIVE landed derived stamp
   `20260922T201218Z` (11 FY rows, 228 figures, 58 unresolved). No Bloomberg error; never retried. PASS.
7. Ran AC3: refdata 1->2, histdata 1->2, bestdata 0->1 (Lenovo's first-ever forecast bronze), pull_log 0->1
   (real prefix), ledger_entries 1->2 with the run's own last entry. Closed legs w1 and w5. PASS.
8. Ran AC4: derived pre 3 post 4, added `20260922T201218Z`; all 3 pre-existing stamps printed with sha256
   (unchanged, still present at their same keys, no delete/overwrite); new document `security_key
   992_HK_Equity`, 228 figures, 58 unresolved. No rollback trigger. Closed leg w6. PASS.
9. Ran AC5, THE PRECONDITION READ-BACK: `fiscal_year_join` PRESENT (`{method: "fiscal-period (fye_join)",
   max_gap_days: 93}` -- rk-109's non-December path fired for Lenovo's 31 March FYE); `currencies`
   `{quote: HKD, reporting: USD, mixed: true, converted: false}` (rk-112's rule honored, nothing converted);
   228 of 228 figures carry `currency_basis`, bases drawn from `{invariant, quote (CRNCY), reporting
   (EQY_FUND_CRNCY)}`; 11 fiscal_years (2016-2026); 15 forecast figures across periods 2027/2028/2029 (from
   the new bestdata). No rollback trigger. Closed the verify leg and the ledger entry
   (`deploy_ledger.py close`: "all 4 legs proven; sentinel removed", rc=0). PASS.
10. Ran AC6: `pull_lines 1` (one stamp), `securities_named ['992 HK Equity']`, `requests_spent 5 probe 1
    total 6 sized_total 6` -- equal to AC0's SIZED line. PASS.
11. No rollback trigger fired at any point; branch taken: KEEP (the new derived stamp is now the served
    block; the 3 prior stamps are untouched and still readable).
12. Wrote the proof-of-spec instance; ran `python .tools/proof-of-spec-check.py <instance>
    AC0,AC1,AC2,AC3,AC4,AC5,AC6`.
13. Filed surprise rows AMGT_RESAPP-Z-W116-S3 and -S4 (this session, both class/hazard as above), spliced
    into the one fenced JSON array in INVESTIGATION_v1.md by textual append (never re-serialized).
14. Flipped `<status>` in the task-order RECORD FACE from `pending` to `complete` (inside this worker's
    `<paths>` grant, per section 6).

## Not done / declared exclusions

- Did not touch any of the 12 other non-December names named in the pair (6861, 9433, CSL, COST, HD, NVDA,
  INTU, IMB, NG/, SSE, ST, ICICIBC) -- both commands named exactly `992 HK Equity`; AC6 confirms.
- Did not run the READ_HERE sign-in (fill/submit) -- AC0 read DAPI UP, so none was needed, and the worker
  is forbidden from running it regardless.
- Did not print the Bloomberg terminal username value anywhere (redacted per row S2's finding).
- Did not delete, overwrite, or remove any S3 object in any branch (no rollback trigger fired, so no
  rollback branch was exercised; the pair's discipline is additive-only regardless).
- Did not read, show, diff or check out branch `wk-amgt-14-50` or `C:/tmp/wk-amgt-14-50`.

## Result

All seven criteria (AC0-AC6) PASS by output. proof-of-spec-check.py rc=0 on the final instance. Task order
status flipped to complete. Two surprise rows filed this session (AMGT_RESAPP-Z-W116-S3, -S4), both
OBSERVATION/BLOCKING-of-the-literal-command with INERT hazard standing, both self-resolved by this worker's
substitutions and named for the disarm owner (`2.0.0_SA_COO~Z`) to correct upstream.
