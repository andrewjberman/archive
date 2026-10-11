# LGIC_ENFORCE round 23 -- the one real run of FWD-8 at the drain (2.0.0_SA_COO~L1)

Run at merged HEAD `68f2bbfc8b` (the worker's merge is `8a41501ebc`, branch `wk-LGIC_ENFORCE-1` @fbf7292378; gate code @75bd033fa7).
Each arm builds a sparse practice copy of the committed HEAD, stages the change, makes the diff as `safe-commit.sh` does and runs the
practice copy's own `.tools/naming-gate.py` with its enforce switches present. Live plane vintage read in this run: `2026-10-11 03:31:33 UTC`
(the graph DB was rebuilt from 02:14:17 UTC during the round; the first adopt arm raced it, the check was amended @f6a3f12d27).

## FWD-8 arm 1 (rename) -- `check_en_r23.py rename`

```
rename: rc=0 WARN 1 graded | ['NAMING OUT-OF-PATTERN infra/aws/terraform/zz-r23-probe/zz_probe.tf:2 bd-zz-r23-probe-role -> {system}-49f-zz-r23-probe-role']
copy:   rc=1 REFUSE | ['NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_probe_copy.tf:2 bd-zz-r23-probe-role -> {system}-49f-zz-r23-probe-role']
PASS-R23-RENAME
```

## FWD-8 arms 2 and 3 (adoption, and the name running nowhere) -- `check_en_r23.py adopt`

```
live pick: bd-49f-auto-login (IAM_POLICY); vintage 2026-10-11 03:31:33 UTC
adopt:  rc=0 WARN 1 graded | ["NAMING OUT-OF-PATTERN infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-49f-auto-login -> blackdiamond-49f-auto-login-policy |   why: EXISTING, touched, and OUT-OF-PATTERN as IAM_POLICY: WARN; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial'); RUNNING-LIVE IAM_POLICY 'bd-49f-auto-login' read from the live plane, Built from the estate as of 2026-10-11 03:31:33 UTC. Stitch source: stitch-codebuild built 2026-10-11T03:01:08Z.  manifest: 011f53502d0f: EXISTING, not minted by this diff"]
vintage: before=2026-10-11 03:31:33 UTC after=2026-10-11 03:31:33 UTC printed=2026-10-11 03:31:33 UTC
absent: rc=1 | ["NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-zz-r23-notrunning-policy -> {system}-49f-zz-r23-notrunning-policy |   why: NEW and OUT-OF-PATTERN as IAM_POLICY: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial')"]
PASS-R23-ADOPT
```

## FWD-8 arm 4 (the live read unreadable, and undated) -- `check_en_r23.py closed`

```
undated: rc=1 | ["NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-49f-auto-login -> blackdiamond-49f-auto-login-policy |   why: NEW and OUT-OF-PATTERN as IAM_POLICY: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial'); LIVE-READ-FAILED: CensusError: the live pull printed no vintage or no denominator"]
unreadable: rc=1 | ["NAMING REFUSE infra/aws/terraform/zz-r23-probe/zz_adopt.tf:2 bd-49f-auto-login -> blackdiamond-49f-auto-login-policy |   why: NEW and OUT-OF-PATTERN as IAM_POLICY: REFUSE; hand-kept carrier of 'bd' outside every permitted context: read it through lookup('49financial'); LIVE-READ-FAILED: CensusError: the live pull did not scan every node type (rc=3):"]
PASS-R23-CLOSED
```

## the two --self-test arms -- `check_en_r23.py selftest`

```
self-test: rc=0 arms=39 rename=2 adopt=5
PASS-R23-SELFTEST
```

Tightened adopt arm (the node type must read `RUNNING-LIVE IAM_POLICY '<name>'`), re-run once at merged HEAD: `PASS-R23-ADOPT`,
vintage before=after=printed=2026-10-11 03:31:33 UTC.

## Drain reads

- Instance `LGIC_ENFORCE.TO-EN-ac-1...proof_of_spec.json`: `proof-of-spec-check.py` VALID rc=0, 4 of 4 invocations match the order.
- Worker rows D1-W1-S3 to S6: four OBSERVATION/INERT rows read; none ARMED, none owes a disarm.
- Hygiene once at the merge: `py_compile .tools/naming-gate.py` OK; `--self-test` NAMING-GATE-SELF-TEST: PASS (39 arms).
- `round-close-check.py --project LGIC_ENFORCE --round 23`: verdict=MAY-CLOSE (1 order, 1 complete, proof_ok=1).
- Cost, for the grade: a commit that adds a NEW out-of-pattern name pays one live pull (budget 300 s) before it is refused;
  a commit with no such literal pays nothing (the read is lazy and once per run).
- Design choice for the grade: the lookup matches the DECLARED node type (a name held only as another type does not make a
  declaration EXISTING; row D1-W1-S4). The PRD says `exact name`; the narrower reading fails closed.
