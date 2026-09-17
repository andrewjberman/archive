# GATE_DOMAIN_BASELINE.r3.md -- EN-n-1 (round 3), 0.9.0_WK_LGIC_ENFORCE~1

Criterion N1R3-AC10 (JUDGMENT, graded by `3.0.0_SA_CVO` at L9): reproduce the pinned pre-state at
`f1ecf97da7` and print the post-state at this worker's tip, each with its denominator.

## INSTRUMENT

Same one run S41/S45 measured and pinned (`f1ecf97da7d184e7b3429bab62effdcc444374f2`, LGIC_ENFORCE-S45,
ruling R-15 @ce23346075):

```
git diff 4b825dc642cb6eb9a060e54bf8d69288fbee4904 <REV> -- 'org/missions/**/*.json' > diff.txt
python .tools/naming-gate.py --diff diff.txt
```

`4b825dc642cb6eb9a060e54bf8d69288fbee4904` is the git empty-tree object, so every string in the 955
records is presented as NEWLY ADDED -- the worst case the gate can see.

## PRE-STATE, reproduced at the pin

`<REV>` = `f1ecf97da7` (this cell's frozen commit), read via a transient detached worktree
(`.worktrees/wk-lgic-enforce-3-1-pinread`, removed after the read; the diff's pre-images are all
`/dev/null` so no repo history beyond the diff itself was needed, but the gate itself -- `lib/opal_naming.py`
and the registry -- was read AS IT STOOD AT THE PIN, not at this worktree's tip).

```
NAMING-GATE: WARN 3815 graded
```
- REFUSE lines: `grep -c '^NAMING REFUSE' <out>` = **2917**
- distinct files carrying a REFUSE: `grep '^NAMING REFUSE' <out> | sed 's/^NAMING REFUSE //; s/:[0-9]*.*//' | sort -u | wc -l` = **90**
- `git diff <empty-tree> f1ecf97da7 -- 'org/missions/**/*.json' | grep -c '^diff --git'` = 969 (the tracked
  population S41 fed in); the gate's own `parse_diff` produced **955** file entries (the 14-file gap between
  969 and 955 is S42's own finding, unrelated to this cell).

This reproduces the pinned baseline (3815 graded / 2917 REFUSE across 90 files) exactly.

## POST-STATE, at this worker's tip

Same invocation, same `diff.txt` (built from the empty tree to `f1ecf97da7`, i.e. the identical 955-record
frame S41/S45 used -- not re-derived against this tip, since the record set itself is frozen and only the
GATE changed), run against `.tools/naming-gate.py` as edited by this cell in this worktree:

```
DENOMINATOR: 955 path(s) in this diff; declaration-tree domain = 955 MINUS EXCLUDED(org/, docs/) 955 = 0 path(s)
COVERAGE: 0 path(s) in the declaration domain the gate could not see (extension outside its graded set and not .gitattributes); 0 seen
NAMING-GATE: PASS 0 graded
```

- graded: **0** (of 955 presented; all 955 fall under `org/` and are excluded by the record-tree subtraction)
- REFUSE: **0**
- rc: **0**

This is R-15's frame exactly as ruled: "the same 955-record frame grades 0 REFUSE under R-13's domain" --
and per S45, that 0 is a disclosed 0-of-0 (DENOMINATOR/EXCLUDED printed), not a silent vacuity. The
ruling's required negative control travels as SEPARATE criteria (N1R3-AC7/AC8), not folded into this
positive half: at this same tip, the identical literal (`advi-49f-fwd2-exercise-queue`, and a resolving vs.
non-resolving repo-path citation) still REFUSES when it appears as a `.tf` resource name / a non-resolving
`.py` path literal -- measured directly against the real gate under `--enforce`, not injected:

```
$ python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_en_r3.py regress-n2-tf-name-refuses
.tf resource name: rc=1; refused: True
PASS-N2R-TF-NAME-STILL-REFUSES

$ python org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/2.0.0_SA_COO~G/fixed_inputs/r3/check_en_r3.py regress-n2-nonresolving-path-refuses
non-resolving path literal: rc=1; refused: True
PASS-N2R-NONRESOLVING-PATH-REFUSES
```

## DENOMINATORS, both states

| | pre-state @f1ecf97da7 | post-state @this tip |
|---|---|---|
| files presented (parse_diff) | 955 | 955 |
| graded | 3815 | 0 |
| REFUSE | 2917 | 0 |
| files carrying a REFUSE | 90 | 0 (n/a) |
| rc (WARN mode, no `--enforce`) | 0 | 0 |

Nothing here asks Round 3 to cut early; this file only pins what N1R3-AC10 asks reproduced (LD-0521,
round 3 stays behind its three slugs).
