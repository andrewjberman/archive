# gate-rename-and-running-name -- round 23 EN-ac-1 (FWD-8) result, 0.9.0_WK_LGIC_ENFORCE~1

Worktree /c/dev/wk-lgic-enforce-23-1, branch wk-LGIC_ENFORCE-1. Gate commits: 810f245ca9 (both limbs, first cut) and 75bd033fa7 (the live lookup matches the declared node type; ruff E731 fix was a blocked attempt, not a commit). The four criteria were run against the committed HEAD 75bd033fa7 (LOCAL, not pushed).

## AC1R23-AC1 -- invocation: timeout 1500 python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~L1/fixed_inputs/r23/check_en_r23.py rename
```
rename: rc=0 WARN 1 graded | ['NAMING OUT-OF-PATTERN infra/aws/terraform/zz-r23-probe/zz_probe.tf:2 bd-zz-r23-probe-role -> {system}-49f-zz-r23-probe-role']
copy:   rc=1 REFUSE | ['NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_probe_copy.tf:2 bd-zz-r23-probe-role -> {system}-49f-zz-r23-probe-role']
PASS-R23-RENAME
rc=0
```

## AC1R23-AC2 -- invocation: timeout 1500 python .../fixed_inputs/r23/check_en_r23.py adopt
```
live pick: bd-49f-auto-login (IAM_POLICY); vintage 2026-10-11 02:14:17 UTC
adopt:  rc=0 WARN 1 graded | ["NAMING OUT-OF-PATTERN infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-49f-auto-login -> blackdiamond-49f-auto-login-policy |   why: EXISTING, touched, and OUT-OF-PATTERN as IAM_POLICY: WARN; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial'); RUNNING-LIVE IAM_POLICY 'bd-49f-auto-login' read from the live plane, Built from the estate as of 2026-10-11 02:14:17 UTC. Stitch source: stitch-codebuild built 2026-10-10T03:01:04Z.  manifest: b348aea09b23: EXISTING, not minted by this diff"]
absent: rc=1 | ["NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-zz-r23-notrunning-policy -> {system}-49f-zz-r23-notrunning-policy |   why: NEW and OUT-OF-PATTERN as IAM_POLICY: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial')"]
PASS-R23-ADOPT
rc=0
```

## AC1R23-AC3 -- invocation: timeout 1500 python .../fixed_inputs/r23/check_en_r23.py closed
```
undated: rc=1 | ["NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-49f-auto-login -> blackdiamond-49f-auto-login-policy |   why: NEW and OUT-OF-PATTERN as IAM_POLICY: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial'); LIVE-READ-FAILED: CensusError: the live pull printed no vintage or no denominator"]
unreadable: rc=1 | ["NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-49f-auto-login -> blackdiamond-49f-auto-login-policy |   why: NEW and OUT-OF-PATTERN as IAM_POLICY: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial'); LIVE-READ-FAILED: CensusError: the live pull did not scan every node type (rc=3):"]
PASS-R23-CLOSED
rc=0
```

## AC1R23-AC4 -- invocation: timeout 900 python .../fixed_inputs/r23/check_en_r23.py selftest
```
self-test: rc=0 arms=39 rename=2 adopt=5
PASS-R23-SELFTEST
rc=0
```

## python .tools/naming-gate.py --self-test (whole output, at 75bd033fa7)
```
SELF-TEST arm s3-access IAM_POLICY -> NO-SYSTEM-ASKED PASS: ok
SELF-TEST arm pipeline-chain IAM_POLICY -> REFUSE REFUSE: ok
SELF-TEST arm built tf-module-literal -> CONFORMANT irpt-cot-reporting-gold-scheduler-role: ok
SELF-TEST arm built py-call-literal -> CONFORMANT irpt-cot-reporting-gold-scheduler-role: ok
SELF-TEST arm built py-call-keywords -> CONFORMANT irpt-cot-reporting-gold-scheduler-role: ok
SELF-TEST arm built tf-module-var -> BUILT-NOT-GRADED (why printed): ok
SELF-TEST arm built tf-registry-reader -> no row: ok
SELF-TEST arm built py-call-var -> BUILT-NOT-GRADED (why printed): ok
SELF-TEST arm built py-call-refused -> BUILT-NOT-GRADED (why printed): ok
SELF-TEST arm built py-hand-typed-control -> typed literal graded REFUSE: ok
SELF-TEST arm pattern pattern-line: ok
SELF-TEST arm pattern not-a-ruling-key: ok
SELF-TEST arm pattern other-kind-warns: ok
SELF-TEST arm pattern summary-counts-it: ok
SELF-TEST place arm FIX in a mapped root, switch present -> REFUSE, PLACE-REFUSE, names the form: ok
SELF-TEST place arm the same, switch absent -> same text, counts WARN (verdict unchanged): ok
SELF-TEST place arm HOLE, switch present -> REFUSE naming the owner and the row owed: ok
SELF-TEST place arm RIGHT -> the row is untouched: ok
SELF-TEST place arm unmapped root, a name the matrix already refuses -> text added, counts REFUSE kept, switch absent: ok
SELF-TEST place arm unmapped root, a well-formed name -> untouched even with the switch present: ok
SELF-TEST place arm exit: PLACE-REFUSE exits 1 without the older switch; a would-refuse WARN row and an old REFUSE row exit 0 without it: ok
SELF-TEST place arm ratchet row: grown count -> REFUSE, PLACE-REFUSE present / WARN absent, names the new HOLE line and its owner: ok
SELF-TEST place arm switch: absent file -> off, present file -> on, an environment value of 0 does not turn it off: ok
SELF-TEST override arm an audited id: the row it names is OVERRIDDEN, exits 0 and is not refused; the row it does not name stays refused: ok
SELF-TEST override arm the same rows with no names (the difference control): both stay PLACE-REFUSE and exit 1: ok
SELF-TEST override arm a variable set by hand (no audit row for its id) passes nothing: ok
SELF-TEST override arm an audit row with an empty reason passes nothing: ok
SELF-TEST override arm a FORGED row (valid-looking, the hash of another message, a different time) passes nothing: ok
SELF-TEST override arm a row with an empty hash, and a row with the right hash whose message has no override line, pass nothing: ok
SELF-TEST override arm no message handed to the gate passes nothing, though the row is otherwise good: ok
SELF-TEST override arm an empty variable and a missing audit log pass nothing: ok
SELF-TEST override arm the index-read arm: a row on disk and not staged passes nothing; once staged it passes; a later disk edit does not change what the index holds: ok
SELF-TEST arm rename admitted: a staged rename graded against its source's HEAD bytes -> OUT-OF-PATTERN WARN: ok
SELF-TEST arm rename copy control: the same bytes staged as a copy (no R row) -> REFUSE REFUSE: ok
SELF-TEST arm adopt held: the plane holds pipeline-chain as IAM_POLICY -> OUT-OF-PATTERN WARN: ok
SELF-TEST arm adopt absent control: a name the plane does not hold -> REFUSE REFUSE: ok
SELF-TEST arm adopt read-failed control: the read raises -> REFUSE REFUSE: ok
SELF-TEST arm adopt vintage-unreadable control: the read prints UNREAD -> REFUSE REFUSE: ok
SELF-TEST arm adopt wrong-type control: the plane holds the name only as EC2_INSTANCE -> REFUSE REFUSE: ok
NAMING-GATE-SELF-TEST: PASS
rc=0
```

## Standing bar
- python .tools/naming-gate.py --self-test: NAMING-GATE-SELF-TEST: PASS and rc=0 before the change (the existing arms, none failing) and after it (rc=0; 39 SELF-TEST lines, of which rename 2 and adopt 5, all ok, per the check's count).
- python -m pytest lib/tests/test_opal_naming_fourth_verdict.py -q -p no:cacheprovider: collects 0 tests (rc=5, 'no tests ran'). The file is a mode-script with no test_ functions; it cannot newly fail under pytest. Recorded as surprise LGIC_ENFORCE-D1-W1-S5.
