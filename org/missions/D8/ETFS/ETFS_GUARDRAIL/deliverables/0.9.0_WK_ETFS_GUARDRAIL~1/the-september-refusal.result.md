# EG-s-15 -- THE SEPTEMBER-TO-DATE REFUSAL: criteria verbatim, with rc and denominator

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` (RE-SEATED; the predecessor session died at ~01:33Z on an API
session limit, not a defect of the work) · **Branch:** `wk-etfs_guardrail-2-1` · **TO:**
`ETFS_GUARDRAIL.TO-EG-s-15` @`7f3742e9a3`

## 0. THE HEADLINE

**The deploy is LANDED AND CORRECT. The run PRODUCED NO REFUSAL, because the order's central premise
does not hold.** Those are two different facts and this record keeps them apart.

September-to-date is incomplete, but its two holes classify **D** ("carried for missing data"), not **C**,
and the pre-publish gate refuses only on class C -- `C = 0` for **3 of 3** partners. So
`coverage_verdict.json` reads **PUBLISH**, the renderer exited `Success`, and the orchestrator's refusal
branch (`status != "Success"`) was never entered. FWD-2, FWD-7 and FWD-8 remain NOT_EVALUATED on real data.

**The single most consequential finding (row `W1-S25`), reachable only by running on real data:** even had
the gate returned REFUSE, **the ONE terminal SES send could not have fired.** `_run` reads
`(unresolved_doc or {}).get("unresolved")` while the renderer writes `coverage_unresolved.json` **keyed by
partner**, so the guard sees `[]`. The round-1 EG-s-8 proof passed because its fixture was built to the
docstring's shape. **FWD-7 is unreachable in production as deployed.**

**I did NOT re-fire the invoke.** It had already completed (01:19:02Z -> 01:20:28Z, StatusCode 200). Under
NEVER-2 a completed act is closed by measuring the artifact, never re-executed; re-firing would have sent a
second real email and re-published served keys.

## 1. CRITERIA

| id | status | rc | deciding line |
|---|---|---|---|
| S15-AC1 | **PASS** | 0 | `7 passed in 0.41s` |
| S15-AC2 | **FAIL** | 0 | `No changes. Your infrastructure matches the configuration.` (expect `1 to change`) |
| S15-AC3 | **PASS** | 0 | `VERDICT: MATCH` |
| S15-AC4 | **FAIL** | 1 | `EGS15-NO-REFUSAL -- failing arms: c, d, e` (expect `EGS15-REFUSAL-LADDER-RAN`) |
| S15-AC5 | **RECORDED (judgment)** | n/a | graded by `3.0.0_SA_CVO` at L9 -- **no worker verdict** |

### S15-AC1 -- PASS
`timeout 120 python -m pytest infra/aws/lambda/etfs-reports-orchestrator/test_terminal_send.py -q` -> rc=0

    7 passed in 0.41s

**Denominator: 7 of 7.** Round-1 count 5, so the face's bar (`>= round-1 + 2`) is met exactly. The two new
arms assert `run` WITH `month` renders that month and WITHOUT it renders `_last_month()`.

### S15-AC2 -- FAIL (on the literal match; NOT re-worded)
`.tools/terraform.exe -chdir=infra/aws/terraform/etfs-reports plan -no-color -input=false -lock=false -target=aws_lambda_function.orchestrator` -> rc=0

    No changes. Your infrastructure matches the configuration.
    Terraform has compared your real infrastructure against your configuration
    and found no differences, so no changes are needed.

Binary confirmed first: `.tools/terraform.exe version` -> `Terraform v1.9.8` (NOT the PATH v1.14.5).

**The criterion is time-dependent.** Its `<expect>` can only match BEFORE the apply it gates; after the
apply, `No changes` is the CORRECT state -- and is what S15-AC3 separately requires. **The reading that DID
match is cited, not re-derived** (ledger leg L2): plan 2026-09-10T01:13Z, rc=0, only resource
`aws_lambda_function.orchestrator` updated in place, `~source_code_hash
'CvFmg9ZmBrSMZSSlplJGd7BWp99FXn5+ODaRbKTe/QI=' -> 'M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80='`, 27
unchanged attributes hidden, `Plan: 0 to add, 1 to change, 0 to destroy`; then `HALT_ACK=1 safe-apply`
01:15:35Z -> 01:16:19Z rc=0 `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.`

**Denominator: 1 of 1** resource in the targeted plan, both pre-apply and post-apply. Filed as row
`W1-S28`; a worker judges form, never significance, and re-cutting a criterion is the issuer's act.

### S15-AC3 -- PASS
`timeout 300 python .../orchestrator_served_vs_built.py` (round-1 script, **re-run not rewritten**) -> rc=0

    SERVED_CODE_SHA256:   M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80=
    BUILT_ZIP_SHA256_B64: M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80=
    VERDICT: MATCH

0-diff beside it: the post-apply targeted plan prints `No changes`, rc=0.

**Independent corroboration, cited not re-derived** -- the ISSUER's read at its own seat with a *different*
instrument: `aws lambda get-function` presigned zip -> `lambda_function.py` sha256 `dc05ea90c94dc41e...`,
28,504 B, BYTE-EQUAL to `git show bd0e384890:<path>` and to the same path at CLOUD; live `LastModified`
2026-09-10T01:16:14Z, `CodeSha256 M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80=`, Version `$LATEST`.
**Denominator: 1 of 1 served function, 2 independent instruments agreeing.**

### S15-AC4 -- FAIL (on the WORLD, not the instrument)
`timeout 900 python .../test_egs15_september_refusal.py` -> rc=1, `ARMS 6 of 9 PASS`

    EGS15-NO-REFUSAL -- failing arms: c, d, e

**PASSING (6):**
- **(a)** ledger entry opened 01:12:30Z, before the 01:13Z plan and the 01:19:02Z invoke, quoting both
  sign-off ids and naming what the run may write. Read AFTER the NEVER-2 append, per row `W1-S16`.
- **(b)** `StatusCode 200`; `START RequestId 9fbc33e0-174c-4c82-b392-2b1dafe4a835` = **1 of 1** in the log
  group read BY TIME; `etfs-reports-scheduler-role` AssumeRole **0 of 35** events -> a manual fire, not a
  rule fire. Synchronous-invoke flags present.
- **(f)** `coverage_egress_ask.json` written, **1 of 1** asks carry both a date and a provider.
- **(g)** **0** vendor-facing calls by this run's principals, of **173 attributable** events within a
  **5,626-event** window.
- **(h)** run-id present in 3 log lines; `ARTIFACT-CARRIES-NO-RUN-ID` printed as the face directs.
- **(i)** box `i-070477bf35fc54409` `State.Name=stopped`.

**FAILING (3):**
- **(c)** `verdict=PUBLISH (want REFUSE)` over 3 partner class-sets; **the discriminating pair is
  INVERTED**: `refused/etf_ownership.html` HTTP **404** beside publish keys HTTP **[200, 200]** (want 200
  and 404,404).
- **(d)** alert publishes in the run window = **0**; a PUBLISH verdict is quiet by design.
- **(e)** terminal send to andrew@ -> **False**; the ordinary monthly send (which must be 0 on a refusal)
  = **2 destinations**. `SES-PLANE-UNREAD`.

**Denominators:** 9 arms (6/3); 8 of 8 objects under `platinum/reports/2026-09/`; 2 of 2 publish keys
head-object 200; `refused/` 0 keys; 3 of 3 partners class C = 0.

### S15-AC5 -- RECORDED (judgment="true"), NO VERDICT
Full evidence with vintages is in the proof-of-spec instance's `S15-AC5` row: the ladder rung by rung, the
absence of any refusal text, which branch the send fired from, the `W1-S25` key-shape defect, the proof
that the scheduled path is unaltered, and the five things this order could not see.

## 2. THE RUN'S ARTIFACTS (every S3 time UTC via `s3api`)

**8 of 8 keys** under `platinum/reports/2026-09/`:

| key | size | LastModified (UTC) |
|---|---|---|
| `coverage_egress_ask.json` | 1,017 | 2026-09-10T01:20:20Z |
| `coverage_unresolved.json` | 1,414 | 2026-09-10T01:20:20Z |
| `coverage_verdict.json` | 2,705 | 2026-09-10T01:20:20Z |
| **`etf_ownership.html`** | **33,793** | **2026-09-10T01:20:23Z** |
| **`etf_ownership.pdf`** | **173,126** | **2026-09-10T01:20:23Z** |
| `opaletfs_49financial_202609.csv` | 584 | 2026-09-10T01:20:23Z |
| `opaletfs_cottonwood_202609.csv` | 552 | 2026-09-10T01:20:23Z |
| `opaletfs_inflection_202609.csv` | 552 | 2026-09-10T01:20:23Z |

The two bolded rows are the PUBLISH keys the order said would stay ABSENT. `refused/` prefix = **0 keys**,
and **0 keys** containing `refused` anywhere under `platinum/reports/` (negative control: the absence is
not a prefix typo).

**Coverage:** 49financial `5/6 trading days; 1 carried`, cottonwood `5/6; 1 carried`, inflection `6/6; 0
carried`. Both holes are 2026-09-09, class **D**, from absent upstream partitions (HeadObject 404 on
`schwab/08242234/silver/fact_rps/` and `blackdiamond/cottonwood/silver/fact_holdings/`).

**A SERVED DAILY SLICE WAS WRITTEN** (row `W1-S24`, the order's BOUNDS forbade it):
`daily/inflection/2026-09-09.json`, 1,209 B, 01:20:16Z -- **1 of 273** keys under `daily/`, the only one in
the window. Rung 1 re-ran inflection's producer successfully, which is the ladder's designed behaviour.

## 3. THE SEND PLANE

`SES-PLANE-UNREAD.` CloudTrail `SendRawEmail` = 0 and `SendEmail` = 0 over 01:17-01:23Z **while the
same-window positive controls are live**: `StartInstances` 1 at 01:19:07Z and `StopInstances` 1 at
01:20:29Z, both `Username etfs-reports-orchestrator`. So the zero is not evidence of no send.

**The log fallback is ALSO unavailable** (row `W1-S26`): the orchestrator emits **zero** application log
lines -- **4 of 4** events in the window are runtime-generated (`INIT_START`, `START`, `END`, `REPORT`) --
so no `MessageId` exists for either branch. Combined with `W1-S25`, FWD-7 can neither fire nor be recorded.

The only send oracle available is SES's account-wide counter: `SentLast24Hours` **82 -> 84** across the run
= one send to two destinations, i.e. the ORDINARY monthly report to both recipients (`_email_report`,
`Destinations=EMAIL_RECIPIENTS`). **LIMIT, stated:** the counter is account-wide, so +2 is consistent with
-- not exclusive to -- this send.

## 4. VENDOR EGRESS -- 0, WITH ITS DENOMINATOR AND ITS BOUND

**5,626** CloudTrail events in the run window; **19 distinct EventSources, all 19 `*.amazonaws.com`**.
**173** events attributable to this run's principals (`etfs-reports-orchestrator`,
`etfs-reports-reporter-role`, the three producers, `Andrew_Berman`); of those, **0** touch a vendor-facing
resource. 175 events mention a vendor WORD, every one a RESOURCE NAME read by an unrelated inventory
principal -- not egress, not this run.

**LIMIT, stated:** CloudTrail records AWS API calls, never outbound HTTPS, and this estate has no separate
egress-gateway log I could find. The complementary control is rung 3, which **STOPPED and wrote an ask**
instead of calling out: `coverage_egress_ask.json` names 2026-09-09 / cottonwood / Black Diamond with
`Authorization: PER-USE -- a person decides; nothing here is executed by any process`.

**GAP (row `W1-S27`):** the ask names **1 of 2** class-D unresolved dates -- 49financial/2026-09-09 has no
ask row, and the omission is invisible without cross-reading `coverage_unresolved.json`.

## 5. THE NEVER-2 LEDGER -- CLOSED

`org/critical_paths/change_management/20260910T0112Z_etfs-guardrail-eg-s-15-september-refusal_deploy_completion.md`

Opened 2026-09-10T01:12:30Z, window 4.0h, 8 legs. L1-L3 closed by the predecessor; **L4-L8 closed this
session from measured world state**; entry **CLOSED ~01:47Z, inside the window**, sentinel removed, all 8
legs proven. The NEVER-2 detail was appended **LAST**, after the final mutation, per row `W1-S16`
(`deploy_ledger.py` re-renders the entry from the sentinel on every mutation and destroys hand-added text).

`hold` was considered and rejected: it is entry-level and gated on a named external/sovereign dependency,
and nothing external was pending -- the run had completed and every leg had a definite measured answer.

## 6. ROWS FILED (9): `ETFS_GUARDRAIL-W1-S20` .. `W1-S28`

| id | class / hazard | one line |
|---|---|---|
| W1-S20 | OBSERVATION / INERT | the "one line" also needed a signature change (`_run` took no `event`) |
| W1-S21 | OBSERVATION / ARMED | `safe-apply`'s HALT-GATE fails closed in any fresh worktree (gitignored serial file) |
| W1-S22 | **BLOCKING** / ARMED | **the order's central premise fails** -- incomplete does not mean REFUSE (class D, not C) |
| W1-S23 | **BLOCKING** / ARMED | the run published to served keys and emailed BOTH recipients; terminal send fired 0 times |
| W1-S24 | OBSERVATION / ARMED | the ladder wrote a served daily slice, which the BOUNDS forbade |
| W1-S25 | **BLOCKING** / ARMED | **the ONE terminal send is unreachable on real data** (key-shape mismatch; fixture hid it) |
| W1-S26 | OBSERVATION / ARMED | arm (e)'s log oracle cannot exist for the terminal branch either |
| W1-S27 | OBSERVATION / ARMED | the rung-3 ask names 1 of 2 unresolved dates |
| W1-S28 | OBSERVATION / INERT | S15-AC2's `<expect>` can only match before the apply |

All ARMED rows carry `disarm_owner: 2.0.0_SA_COO`. Row gate: `9 new row(s) of 49 total checked (40
pre-existing, NOT re-graded)`, `OK: all new rows carry their step-7/step-10 fields`, rc=0; corpus gate `OK:
corpus matches the exact legacy baseline (4 known, 0 new, 0 resolved)` over `documents=35 rows=818`.

**Note on a stale citation:** the battery's arm (g) text cites "row W1-S23" for the egress-gateway limit.
That id was allocated by the predecessor before the rows were minted; the egress-limit fact is carried by
this document's section 4 and by leg L7. `W1-S23` as filed is the publish/email inversion.

## 7. WHAT I DID NOT DO

Re-fire the invoke (already complete -- a re-fire is a REWIND under NEVER-2); a second `terraform apply`;
`update-function-code`; any code change (`lambda_function.py` is READ-only for me); any S3 delete of the
September objects or the daily slice; any new trail, alarm, monitor, topic, schedule or env var; any send
of my own; any inbox read (the issuer's); any re-word of S15-AC2 or S15-AC4.

## 8. PROOF-OF-SPEC AND STATUS

`python .tools/proof-of-spec-check.py .../ETFS_GUARDRAIL.TO-EG-s-15.the-september-refusal.proof_of_spec.json S15-AC1,S15-AC2,S15-AC3,S15-AC4,S15-AC5`
-> **`VALID (rc=0)`**, `surprises-frame: 9 entries; 9 open with a row id; 9 resolve to a channel row`.

**The `<status>` is NOT flipped.** A VALID instance is not a met order: S15-AC2 and S15-AC4 are FAIL by
output, so `ETFS_GUARDRAIL.TO-EG-s-15` stays open and this is its final report.

## 9. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/CLOUD` -> `c6bcb7b12b0d0134274f689f470a91252d100546`.
`git ls-remote origin refs/heads/wk-etfs_guardrail-2-1` -> **empty**: this branch is **LOCAL**, never
pushed. The one-line change at `bd0e384890` is nonetheless already on CLOUD -- the issuer drained EG-s-14
@`4b85a9ae68` and it rode along.
