# EN-f-2 result -- the fence on opal-data-49financial, applied and proved

**Worker:** `0.9.0_WK_LGIC_ENFORCE~1`. **Order:** `LGIC_ENFORCE.TO-EN-f-2`. **Worktree:** `.worktrees/wk-lgic-enforce-1-1-f2`,
branch `wk-lgic-enforce-1-1-f2`, base `CLOUD` @d7d801c323. **Ledger:** `lgic-enforce-fence-49financial`, closed by the tool.

## Gate G-E and the sign-off conditions

| Condition (1.0.0_SA_CTO, message 96959) | Measured |
|---|---|
| Both SIGNOFF lines on the entry before L2 | `SIGNOFF 2.0.0_SA_COO~G 20260915T070844Z` @ccb7422e15; `SIGNOFF 1.0.0_SA_CTO 20260915T072924Z` @766b5a0cfb; L2 closed 20260915T081903Z |
| Scope is FENCE_PLAN s.1's 7 changes exactly | Re-plan compared with EN-f-1's `fence_plan.json` as parsed JSON: 7 of 7 non-no-op changes equal in address, actions, before and after; 238 resource_changes each; 0 only-in-new, 0 only-in-old. `Plan: 6 to add, 1 to change, 0 to destroy.` |
| (1) The applying identity is a 2a exempt principal, printed before the apply | `sts get-caller-identity` at 08:16:09Z (before L2) and 08:31:27Z (before L4): `arn:aws:iam::313476888478:user/Andrew_Berman` (FENCE_PLAN s.2a row 14) |
| (2) L3 runs, and L4 removes the probe roles, in one session within 1h of L2 | L2 apply 08:17:25Z; probes 08:20:07Z-08:21:11Z; removal apply 08:32:30Z. Window 15m05s |
| (3) A failing arm or an AccessDenied on a 2a principal rolls back | Not triggered: 4 of 4 arms as expected, and the exempt read by `Andrew_Berman` was ALLOWED. The rollback was staged, not run |

## The legs

| Leg | When (UTC) | Output |
|---|---|---|
| L2 apply | 08:16:13Z-08:17:25Z | safe-apply rc=0: `Apply complete! Resources: 6 added, 1 changed, 0 destroyed.` Halt gate scanned issuer 2.0.0_SA_COO~G, naming limb WARN, comp-tagauthz PASSED, tombstone CLEAN |
| L3 probes | 08:20:07Z-08:21:11Z | `FENCE_PROBES.md`: 49f ALLOWED (req C5WFQFQPTWGXTD8N); cot DENIED (req BYP7EENM7APP44CC); unscoped DENIED (req CHXCAFYPDN6KRAHR); exempt `Andrew_Berman` ALLOWED (req FKEX87SAV4D5EX39). Both DENIED reads name "an explicit deny in a resource-based policy" |
| L4 removal | 08:31:30Z-08:32:54Z | `lgic-enforce-fence-probes.tf` deleted; removal plan 0 add / 0 change / 6 destroy; safe-apply rc=0 `Apply complete! Resources: 0 added, 0 changed, 6 destroyed.`; get-role NoSuchEntity x3; re-plan `No changes.` (-detailed-exitcode 0) |
| Close | 08:37:05Z | `deploy_ledger.py close` rc 0, sentinel removed; `CLOSED 20260915T083706Z` appended to the entry |

## The criteria

| Id | Verdict line | rc |
|---|---|---|
| F2-AC1 | 08:23:20Z (sentinel present): `VERDICT: PASS-SIGNED-BEFORE-APPLY`. 08:37:06Z (after the ordered close): `VERDICT: FAIL-SIGNOFF` | 0, then 1 |
| F2-AC2 | `VERDICT: PASS-POLICY-LIVE` (08:23:22Z and 08:37:07Z) | 0 |
| F2-AC3 | `VERDICT: PASS-49F-READS` (both runs) | 0 |
| F2-AC4 | `VERDICT: PASS-COT-DENIED` (both runs) | 0 |
| F2-AC5 | `VERDICT: PASS-UNSCOPED-DENIED` (both runs) | 0 |
| F2-AC6 | `VERDICT: PASS-EXEMPT-ALLOWED` (both runs) | 0 |
| F2-AC7 | `VERDICT: PASS-PROBES-REMOVED` (08:37:18Z) | 0 |
| F2-AC8 | `SENTINEL: absent` / `VERDICT: FAIL-LEDGER-OPEN` (08:37:36Z) | 1 |

**In the first session F2-AC8 was FAIL and the order stayed open.** Row `LGIC_ENFORCE-W1-S18` (BLOCKING, ARMED, disarm owner 2.0.0_SA_COO~G):
`deploy_ledger.py close` unlinks the sentinel (`:440`), and `check_en.py` reaches the entry only through it
(`_entry_text` `:653-656`, `f2_closed` `:737-740`, `f2_signoff` `:676-683`, all @d7d801c323).

## Re-run on the fixed checker

A cold-start instance of `0.9.0_WK_LGIC_ENFORCE~1` re-ran F2-AC1 and F2-AC8 on the fixed checker: `check_en.py` @78f8820a58,
synced onto this branch @af2dbd097e. The blob is `b60e1b18dd` at both commits. It re-ran all eight invocations as written, from
this worktree at af2dbd097e, between 09:13:30Z (the sync commit) and 09:22:45Z (a `date -u` read taken after the runs). No live
act was repeated. The ledger entry, the sentinel and FENCE_PROBES.md were not touched.

| Id | Verdict line (re-run @af2dbd097e) | rc |
|---|---|---|
| F2-AC1 | `SIGNOFF LINES: {'1.0.0_SA_CTO': '20260915T072924Z', '2.0.0_SA_COO~G': '20260915T070844Z'}  APPLY (L2 closed_at): 20260915T081903Z` / `VERDICT: PASS-SIGNED-BEFORE-APPLY` | 0 |
| F2-AC2 | `VERDICT: PASS-POLICY-LIVE` | 0 |
| F2-AC3 | `VERDICT: PASS-49F-READS` | 0 |
| F2-AC4 | `VERDICT: PASS-COT-DENIED` | 0 |
| F2-AC5 | `VERDICT: PASS-UNSCOPED-DENIED` | 0 |
| F2-AC6 | `VERDICT: PASS-EXEMPT-ALLOWED` | 0 |
| F2-AC7 | `VERDICT: PASS-PROBES-REMOVED` | 0 |
| F2-AC8 | `SENTINEL: absent  ENTRY: org/critical_paths/change_management/20260915T0334Z_lgic-enforce-fence-49financial_deploy_completion.md  ENTRY CLOSED: True` / `VERDICT: PASS-LEDGER-CLOSED` | 0 |

8 of 8 mechanical criteria PASS by output. With the sentinel gone, the fixed checker finds the entry by slug and reads L2's close
time from the entry's log line. Row W1-S18 stays as filed; the issuer disarms it after the drain.

## Not claimed

- The Sign-off section is no longer in the entry file. The L2 close-leg re-rendered the entry without it, as row
  `LGIC_ENFORCE-W1-S17` predicted. Both lines remain in the file's committed history at ccb7422e15 and 766b5a0cfb.
  This run did not hand-restore them.
- The exempt arm probed one principal of 16 (`Andrew_Berman`, the applying identity). No other 2a principal was probed.
- No principal outside the census was probed. FENCE_PLAN s.2d's narrowing is taken from the plan, not measured.
- Push state: LOCAL on `wk-lgic-enforce-1-1-f2`; never pushed.
