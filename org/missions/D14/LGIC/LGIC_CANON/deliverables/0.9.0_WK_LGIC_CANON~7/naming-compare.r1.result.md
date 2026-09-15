# naming-compare.r1.result -- 0.9.0_WK_LGIC_CANON~7 on LGIC_CANON.TO-CN-n-3 (cell CN-n-3, round 1)

Worktree `.worktrees/wk-lgic-canon-1-2` (reused directory), branch `wk-lgic-canon-1-7`, cut from CLOUD @671925aecc
(`git rev-parse HEAD` read 671925aecc77f15dfb33a1b15cfb966b0ae2c3ae before any commit). The directory's untracked
`.scratch/` from the earlier worker was neither read nor cited; this worker's scratch is `.scratch/n3/`.

## Inputs (each pinned by the last commit that carries it)

| input | commit |
|---|---|
| `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/naming-a.tsv` (worker A, `# base f95470f384`) | 69f406a696 |
| `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/naming-b.tsv` (worker B, `# base f95470f384`) | 885831971e |
| `org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/CN_NAMING_KEY.json` | 4058a56606 |
| `org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py` | 4058a56606 |
| `org/standards/NAMING_SCHEMA.json` (v1.8; refused_tokens `bd`, `mockadv`) | 2f554182b6 |
| `infra/logic/registry/scopes.json` (row `49financial`: long `49financial`, short `49f`, bucket `opal-data-49financial`) | a925c8a642 |

## The comparison (my own read, a separate method from the checker)

A python read of both answer files against the key: exact string equality to `canonical`, then each answer split
into its slots (bucket; key scope segment = second path segment; resource system = first `-` token and resource
scope = second), then the answer's tokens (split on `-/:.=`) intersected with the schema's refused tokens.
Denominator: 6 key items, 6 rows in A, 6 rows in B.

| item | slot (key) | form | A = canonical | B = canonical | slot values in both | refused hit |
|---|---|---|---|---|---|---|
| n1 | bucket | LONG | True | True | bucket `opal-data-49financial` | none |
| n2 | key scope segment | LONG | True | True | key scope `49financial` | none |
| n3 | bucket and key scope segment | LONG | True | True | bucket `opal-data-49financial`, key scope `49financial` | none |
| n4 | resource scope slot | SHORT | True | True | system `advi`, scope `49f` | none |
| n5 | resource scope slot | SHORT | True | True | system `irpt`, scope `49f` | none |
| n6 (trap) | resource system and scope slots | SHORT | True | True | system `blackdiamond`, scope `49f` | none |

Result: 6 of 6 PASS, 0 FAIL. The two answer files are identical row for row. On n3 the value compared is the KEY's
`canonical` (the `address()` output, `advisor_id=A123`), as the face says; `grade()`'s verdict on n3 (row
LGIC_CANON-W8-S1) was not consulted.

Deliverable: `org/missions/D14/LGIC/LGIC_CANON/deliverables/exercises/naming-compare.md` (6 lines `ITEM <id>: PASS`).

## Criteria (run in the worktree, bounded, after the deliverable was written)

N3-AC1 -- `cd <WS> && timeout 120 python org/missions/D14/LGIC/LGIC_CANON/deliverables/2.0.0_SA_COO~G/fixed_inputs/r1/check_canon_r1.py n3-equal`

```
ITEMS: 6  BOTH WORKERS ON THE CANONICAL VALUE: 6
VERDICT: PASS-N3-BOTH-CANONICAL
rc=0
```

N3-AC2 -- `... check_canon_r1.py n3-trap`

```
TRAP ITEMS: 1  CAUGHT BY BOTH: 1
VERDICT: PASS-N3-TRAP-CAUGHT
rc=0
```

N3-AC3 -- `... check_canon_r1.py n3-sanctioned`

```
ITEMS: 6  MARKED CORRECTLY: 6
VERDICT: PASS-N3-SANCTIONED-KEPT
rc=0
```

N3-AC4 -- `... check_canon_r1.py n3-blind`

```
BASE A: f95470f38400da6d2a40eeaa7469651e32ddb95e  BASE B: f95470f38400da6d2a40eeaa7469651e32ddb95e  LEAKS: 0 of 2
VERDICT: PASS-N3-MUTUALLY-BLIND
rc=0
```

Before the deliverable existed, N3-AC3 printed `VERDICT: FAIL-N3-SANCTIONED-ABSENT` (the file was absent) and the
other three printed the same PASS lines as above.

Surprises: none filed.
