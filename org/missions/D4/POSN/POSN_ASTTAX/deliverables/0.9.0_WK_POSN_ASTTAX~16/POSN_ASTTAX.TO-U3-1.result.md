# POSN_ASTTAX.TO-U3-1 -- RESULT (cell `AT4-s-3`, FWD-5 / FWD-1)

**Worker:** `0.9.0_WK_POSN_ASTTAX~16` - **Branch:** `wk-posn_asttax-4-3` -
**Worktree:** `C:/tmp/wk-posn-u3` (sparse cone) - **HEAD at execution:** `72f2417499`

---

## HEADLINE, IN ONE PARAGRAPH

**U3-AC1 is answered and the premise HOLDS.** On a scratch copy, with the live tables never
opened, `seed_canonical_securities.py` reverts a ratified five-class `asset_class` on one
re-seed: **`VXX` `'Structured'` -> `'equity'`**, and the same for the three other retag-set
members it carries. Row `W14-S3`'s "4 of 11" figure was **re-measured, not inherited, and
reproduces exactly** (4 present, 7 absent).

**U3-AC2, U3-AC3 and U3-AC4 are BLOCKED and the order stays open.** The `<paths>` grant names
`infra/aws/lambda/v2_portal/yang_pipeline/seed_canonical_securities.py`, which **has never
existed on any ref**; the file the cell is about is
`data/black_diamond/scripts/classification/seed_canonical_securities.py`, which is **outside
the grant**. Separately, the commit gate **cannot run in this worktree at all**, so no `.py`
can be committed from here regardless -- and, per `-S3`, **no commit of ANY kind can be
made from this worktree**, so this deliverable is VALID and UNCOMMITTED. Rows
`POSN_ASTTAX-Z-W16-S1`, `-S2`, `-S3`.

---

## U3-AC1 -- THE BEFORE MEASUREMENT  (PASS-by-output)

### The scratch target, named explicitly

The live tables were never opened. `boto3` is replaced in `sys.modules` **before** the
seeder's real bytes are executed; `boto3.client` raises `AssertionError`;
`boto3.resource('dynamodb').Table(name)` returns an in-process dict and **prints which name it
intercepted**. Both interceptions are in the recorded output:

```
  SCRATCH TARGET: boto3 Table('bd-securities') INTERCEPTED -> in-process dict (no network client exists in this process)
  SCRATCH TARGET: boto3 Table('etf-classifications') INTERCEPTED -> in-process dict (no network client exists in this process)
```

After the run, the control asserts `sys.modules["boto3"].__IS_FAKE__ is True` -- if anything had
displaced the fake mid-run, the arm would have raised rather than reported.

### The subject is REAL BYTES, not a re-implementation

The file is outside this worktree's sparse cone, so its bytes were read from the **git object
store** and the sha asserted equal to the object before the run:

```
  repo path : data/black_diamond/scripts/classification/seed_canonical_securities.py
  blob sha  : fbbc7165d33198789d3a7788a557ed3f5ce75614
  asserted == HEAD object: fbbc7165d33198789d3a7788a557ed3f5ce75614
  bytes     : 15000
```

The control executes those bytes and calls the seeder's own `seed(upload=True, sync_yang=True)`
-- the `--upload --yang` path `W14-S3` names. It does not re-implement the seeder.

### The BEFORE state, AS A VALUE

Scratch baseline = the registry as a **completed** retag would leave it: every retag member
present in the seeder carries its ratified five-class `asset_class`, plus two curator fields
the seeder does not own.

```
  TICKER BEFORE         AFTER          RATIFIED       VERDICT
  VXX    Structured     equity         Structured     CLOBBERED
  UVXY   Structured     equity         Structured     CLOBBERED
  QBER   Structured     fixed_income   Structured     CLOBBERED
  PDBC   Commodities    equity         Commodities    CLOBBERED

  CLOBBERED: 4 of 4 members present in the seeder -- ['VXX', 'UVXY', 'QBER', 'PDBC']
```

**THE BEFORE VALUE:** `VXX.asset_class` was `'Structured'` and is `'equity'` after one re-seed.
`UVXY` `'Structured'`->`'equity'`; `QBER` `'Structured'`->`'fixed_income'`;
`PDBC` `'Commodities'`->`'equity'`.

### The MINT control fired, so the verdict is meaningful

```
MINT CONTROL: 'CASH_USD' was absent before the run; after the run it is PRESENT (asset_class='fixed_income')
  -> the seeder IS writing. A 'survived' verdict is therefore meaningful.

  scratch etf-classifications    update_item calls:  57   rows minted: 53
  scratch bd-securities          update_item calls:  57   rows minted: 57
```

A seeder that wrote nothing would have produced "SURVIVED" for every row and would have been
worthless. It wrote 57 rows and minted 53 on the Yang target.

### "4 of 11", RE-MEASURED

Measured by `ast.literal_eval` over the seeder's own `CANONICAL_SECURITIES` (denominator
printed), against the 11-member retag set from PRD s.3 and `~14`'s `t5_bar_table.py:16-28`:

```
  MEASURED: 4 of 11 retag members carried by this seeder -- ['VXX', 'UVXY', 'QBER', 'PDBC']
  the other 7 are absent: ['DBC', 'GLD', 'GSG', 'IAU', 'SLV', 'USO', 'VIXY']
```

`W14-S3`'s figure reproduces exactly. Its vocabulary claim also reproduces:

```
  denominator: 57 rows in CANONICAL_SECURITIES
    'equity'          24 row(s)
    'fixed_income'    33 row(s)
  DISTINCT VALUES: 2 -- ['equity', 'fixed_income']
  INTERSECTION WITH THE RATIFIED FIVE CLASSES:
    ['Fixed Income / Cash', 'Equity', 'Structured', 'Commodities', 'Alternatives']
    -> <empty>  (0 of 5)
```

**0 of 5.** The seeder cannot express any ratified class, so it cannot preserve one by
accident -- it can only overwrite with one of two legacy labels. That is the mechanism.

### WHAT THE SEEDER'S DOCSTRING GETS RIGHT, and why it is not a defence

The docstring claims "attribute-preserving update_item upserts -- every field it does not own
survives". **That claim is TRUE and was verified:**

```
  VXX    management_style/sector  before=('passive', 'Broad')  after=('passive', 'Broad')  SURVIVED
```

`update_item` with `SET` only touches the named attributes. The defect is not in the fields the
seeder does **not** own -- it is precisely in the three it **does**: `asset_class`,
`sub_asset_class`, `name`. The docstring's reassurance is about a different set, and reading it
as coverage is how this writer stayed unexamined for a round.

**Evidence file:** `u3_ac1_before_output.txt` (verbatim, 4916 bytes, rc 0).

---

## U3-AC2 -- THE CHANGE  (FAIL / BLOCKED -- row `POSN_ASTTAX-Z-W16-S1`)

### The invocation, run verbatim, and the discriminator that reads it correctly

```
$ timeout 180 git diff -- infra/aws/lambda/v2_portal/yang_pipeline/seed_canonical_securities.py
rc=0
--- bytes of diff output ---
0
```

An empty scoped `git diff` means **clean** OR **matched nothing**, and those print
identically. The discriminator:

```
index entries matching the GRANTED pathspec: 0
index entries matching the REAL pathspec (positive control): 1
```

It is **matched-nothing**. The positive control fires on the real path.

### The granted path has never existed

| probe | granted path | real path |
|---|---|---|
| `git log --all --oneline -- <path>` | **0 commits** | 4 commits |
| `git ls-files -- <path>` | 0 | 1 |
| exact-basename over all **33,731** index entries | -- | exactly 1 hit, `data/black_diamond/...` |

The basename census is over the **full index (33,731)**, not the readable cone. `comp-find`
was deliberately not used for it: in this cone-mode worktree its denominator certifies a
~3,270-file sweep, which is row `Z-W14-S6`'s blindness and would have returned a confident
zero.

### Where the wrong path came from

The `<paths>` grant is the **round-3 subject's directory** joined to the **round-4 subject's
filename**. `W14-S3` is explicit that these are different files: its own fourth evidence bullet
says *"AT3-s-4 / TO-T4-1's grant and its measured subject are
`infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py`"* (hyphens), while every
line cite for the second writer is against `data/black_diamond/...`. The round-4 decomp supplies
**no directory at all** -- one PROSE occurrence at `:103`, bare filename, "POSN-owned seed script".

`<paths>` IS the write grant. A path the order lacks is a blocking row, never an override, so
**no edit was made to the real file and the granted path was not created to make the order
executable.**

### What the change WOULD be -- recorded, not applied

`u3_proposed_patch.diff` in this directory is a complete, reviewable patch (+57/-2), generated
against the real bytes and **exercised on a scratch copy** (see below). It reuses the sibling's
mechanism rather than inventing a second one.

**The sibling's rule**, `seed-etf-classifications.py:72-120 merge_item()`: *"the module wins
where it knows something; the TABLE wins where the module only has a placeholder; and where
BOTH know something and they DISAGREE, nothing is decided here -- the disagreement is returned
as a conflict for the caller to refuse on"*, with `:293-294` making `--force` the only way past
a disagreement.

**How it maps here:** `seed_canonical_securities.py` never emits a placeholder -- its
vocabulary is two hardcoded values -- so `is_placeholder`'s half is inert and the **conflict
half is the whole mechanism**. The patch adds a `get_item` pre-read, treats a differing
non-blank served value on an owned field as a conflict, preserves the table's value, and
returns non-zero unless `--force`.

**WHAT THE CHANGE DOES NOT ALTER, stated explicitly:**

1. **A FIRST MINT STILL MINTS.** `_yang_conflicts` returns `[]` for an absent row, so a ticker
   the table does not yet carry is written whole. Measured: **53 rows minted under the patch**,
   the same 53 as pre-patch.
2. **The `bd-securities` write is untouched.** Not one line of the bd limb changes; this cell is
   about the Yang registry.
3. **The dry-run path is untouched.** The pre-read only runs when `upload` is true.
4. **`--force` still reverts**, by design -- the override is preserved, not removed.
5. **Non-owned attributes** (`management_style`, `sector`, `rationale`, `firm_origin`) behave
   exactly as before; they were never at risk and the patch does not touch them.

---

## U3-AC3 -- THE PROOF  (FAIL / BLOCKED -- but both required controls were measured)

AC3's named invocation is "re-run AC1's exercise against **the patched script**". There is no
patched script in the repo, because AC2 is blocked. So AC3 cannot be graded.

**What WAS measured, on the scratch copy only, as the mutant/discrimination control this
deliverable owes under `PROOF_OF_SPEC.controls.mutant`:**

```
  pre-patch  : CLOBBERED 4 of 4, minted=True
  patched    : SURVIVED  4 of 4, minted=True, rc=1
  --force    : CLOBBERED 4 of 4  (the override still overrides)

  OK: THE CONTROL DISCRIMINATES.
```

All three arms AC3 asks for are present in that reading:

- **NEGATIVE CONTROL (required):** pre-patch bytes, same input -> still reverts, 4 of 4. **FIRES.**
- **POSITIVE / MINT CONTROL (required):** the same run still mints a row that did not exist --
  `CASH_USD` minted in **both** arms, 53 rows minted under the patch. **FIRES.** A script that
  preserved everything by refusing to write at all would have minted 0.
- **The value SURVIVES:** 4 of 4 under the patch, and the run refuses loudly rather than
  silently reverting:

```
  [PRESERVED] VXX        asset_class: table serves 'Structured', seeder asserts 'equity' -- table wins, pass --force to override
  REFUSED 4 etf-classifications row(s): the table serves a value this seeder disagrees with.
```

The two arms read **differently on the same input**, so the control discriminates and AC1's
"CLOBBERED" is a property of the seeder's write rule, not of the instrument.

**This is a scratch demonstration for the issuer, and it is NOT U3-AC3.** The repo file was not
edited. AC3 stays FAIL until the grant is corrected and the patch actually lands.

**Evidence file:** `u3_mutant_control_output.txt` (verbatim, rc 0).

---

## U3-AC4 -- THE GATE  (FAIL / BLOCKED -- row `POSN_ASTTAX-Z-W16-S2`)

The gate does not fail a check here. **It cannot run**, and it fails before dispatching any file:

```
$ timeout 180 bash .tools/commit-gate.sh <the .py>
Traceback (most recent call last):
  File "C:\tmp\wk-posn-u3\.tools\commit_gate_runner.py", line 96, in <module>
    import comp_constants_cli   # noqa: E402
ModuleNotFoundError: No module named 'comp_constants_cli'
GATE_RC=1
```

**Cause, from the gate's own source:** `commit_gate_runner.py:78` sets
`GRAPH_DIR = WORKSPACE / "org" / "modules" / "graph"`, `:91-93` puts it on `sys.path`, `:96-100`
imports five modules from it. This worktree's cone is six entries -- `.tools`,
`infra/aws/lambda/v2_portal`, `org/missions`, `org/projects`, `org/ref`, `org/standards` --
and **`org/modules` is not among them.**

**Positive control, and it fires:** the gate's *in-cone* dependency loaded fine --
`:87` loads `ds-precommit-check.py` from `.tools/` via importlib without raising, and the
traceback's frame is nine lines later at `:96`. So this is an out-of-cone import, not a broken
gate, a broken python or a bad argument. An exact-basename census over all 33,731 index entries
finds `comp_constants_cli.py` at exactly one path: `org/modules/graph/comp_constants_cli.py`.

**It is fail-closed, and that was EXERCISED, not inferred:**

```
$ bash .tools/safe-commit.sh --author "..." -F <msg> -- <the .py>
  [risk-reflex] ...python.exe: can't open file 'C:\tmp\wk-posn-u3\org\modules\graph\comp_pulse.py': [Errno 2] No such file or directory
ERROR: BLOCKED -- commit-gate failed (py_compile / ruff / lint). Commit aborted; files unstaged.
  Fix the reported issue(s) and re-commit. This gate is UNIVERSAL + fail-closed on ALL .py
  (Rule 14); --force does NOT bypass a gate failure (it only overrides the contamination check).
SAFECOMMIT_RC=1
```

`git log --oneline -1` was unchanged: nothing committed. Note the second, independent
out-of-cone miss in that output -- the `risk-reflex` limb reaching for
`org/modules/graph/comp_pulse.py` -- same cone cause, different consumer.

**BOTH ASCII LIMBS, checked rather than the one that stopped me**, since clearing one teaches
nothing about the other:

- **commit-MESSAGE arm (BLOCKING):** the message file for the real commit was written by a
  non-shell writer and verified **0 non-ASCII bytes** before use. Clean.
- **staged-`.py` arm (WARN-ONLY, ships):** **UNMEASURED, and stated as unmeasured rather than
  clean.** It could not run -- the gate never reached file dispatch. Independently, every file
  in this deliverables directory was byte-scanned for `>126`: **0 non-ASCII across all
  artifacts**. That is my own scan, not the gate's verdict, and it is not a substitute for one.

**CONSEQUENCE FOR THIS DELIVERABLE -- and it is WORSE THAN THE ROW `-S2` FIRST SAID.**
`-S2` recorded "no `.py` can be committed". Measured afterwards, and filed as `-S3`
against my own row: `.tools/commit-gate.sh` is 59 lines ending in a bare
`exec python "$SCRIPT_DIR_WIN/commit_gate_runner.py" "$@"` with **no bash-side extension
filter** -- its own header says it "delegates ALL files to ONE python process" -- and the
runner raises at *import* scope. So the gate exits 1 on an `.md`-only file list **and on an
empty argument list**, both measured. `safe-commit.sh:653` is a flat `if [ "$GATE_RC" -ne 0 ]`
-> `exit 1` with no `rc=2` "gate is broken" branch, and of its four audited overrides
(SENSITIVE, LOG-SWEEP, SURPRISE-ROW, SYSTEM-CURRENT) **none covers the commit gate**.

**Therefore NOTHING can be committed from this worktree.** The real delivery commit -- a file
set of `.md`/`.json`/`.diff`/`.txt` containing **zero** `.py` -- was attempted and returned
`SAFECOMMIT_RC=1` with `HEAD` unchanged. This result document, the proof-of-spec instance
(which validates `rc=0`), the proposed patch and all three rows exist **only in this
worktree's working tree**. They are on no branch and no drain can see them.

The two control scripts live under `.scratch/` with their **full source embedded verbatim at
the end of this file** so the method survives. They were not renamed to a non-`.py` suffix --
dodging a gate by extension is not a remedy. No workaround was manufactured: the cone was not
widened, `PYTHONPATH` was not re-pointed, and no bare `git commit` was used.

---

## WHAT WAS NOT DONE, AND WHY (declared, so no gap reads as coverage)

| Not done | Reason |
|---|---|
| Edited `data/black_diamond/.../seed_canonical_securities.py` | Outside `<paths>`. The grant IS the write surface; a missing path is a blocking row, never an override. |
| Created the granted path so the order would run | That is reconstructing the tree to make an order executable. Refused. |
| Widened the sparse cone / set `PYTHONPATH` at another tree's `org/modules/graph` | Same reason; and grading THIS tree's bytes with ANOTHER tree's checks is a wrong-grain reading even when it returns clean. |
| Ran the seeder against the live `etf-classifications` or `bd-securities` | The cell's hard stop. No network client was ever constructed in any run. |
| Re-ran round 3's `AT3-s-4` | Read-dependency, not claimed. Its mechanism was read and reused; its cell was not re-executed. |
| Flipped `<status>` to `complete` | Three criteria FAIL. A VALID instance is not a met order, and a status flip is never a way to release a gate. |
| Re-derived the 11-member retag set | Cited to PRD s.3 + `~14`'s `t5_bar_table.py:16-28`, which derived it by subtraction over 285 rows. Only the 4-of-11 *intersection* was re-measured, which is what the preflight asked for. |

---

## CONTROLS SUMMARY

- **MUTANT:** FIRED-AS-EXPECTED. Patched vs pre-patch bytes on identical input read
  SURVIVED 4/4 vs CLOBBERED 4/4, mint firing in both.
- **DETERMINISM:** STABLE. Two same-input runs of the AC1 control produced byte-identical
  output (4916 bytes each, `diff -q` clean).
- **TREE STATE:** `git status --porcelain` shows exactly 2 entries -- the granted channel file
  (modified) and untracked `.scratch/`. `git diff --stat HEAD -- data/` is empty. The subject
  file is not present in this worktree and was not touched.

---

## APPENDIX A -- `u3_ac1_before_control.py` (full source, verbatim)

Lives at `.scratch/run/u3_ac1_before_control.py`; embedded because the commit gate cannot run
in this worktree and no `.py` can be committed from it.

```python
#!/usr/bin/env python3
"""POSN_ASTTAX.TO-U3-1 / cell AT4-s-3 / U3-AC1 -- the BEFORE measurement.

WHAT THIS MEASURES, AND WHAT IT DELIBERATELY DOES NOT TOUCH
-----------------------------------------------------------
Row W14-S3 ASSERTS that seed_canonical_securities.py reverts a five-class
asset_class on re-seed. This control TESTS that assertion; it does not confirm
it. If the value survives, this script says so and that is the answer.

THE SCRATCH TARGET IS NAMED EXPLICITLY AND THERE IS NO NETWORK CLIENT:
  boto3 is replaced in sys.modules BEFORE the seeder's real bytes are executed.
  boto3.client raises AssertionError. boto3.resource('dynamodb').Table(name)
  returns an in-process dict-backed ScratchTable and PRINTS which name it
  intercepted. The live DynamoDB tables 'etf-classifications' and
  'bd-securities' are never opened, read or written by this process.

THE SEEDER IS REAL BYTES, NOT A RE-IMPLEMENTATION. A control that
re-implements the producer proves nothing about the producer. The bytes come
from the git object store (the file is outside this worktree's sparse cone)
and their sha is asserted against the object before the run.

UPDATE_ITEM FIDELITY: the scratch table implements DynamoDB SET semantics --
comma-separated 'path = :value' assignments, '#alias' resolved through
ExpressionAttributeNames, ':token' through ExpressionAttributeValues, and an
absent key UPSERTS (creates the item). That upsert is what makes the mint
probe meaningful.
"""
import ast
import io
import os
import subprocess
import sys
import types
from contextlib import redirect_stdout

ROOT = os.getcwd()
SEEDER_PATH_IN_REPO = "data/black_diamond/scripts/classification/seed_canonical_securities.py"
SEEDER_BYTES = os.path.join(ROOT, ".scratch", "head", "seed_canonical_securities.py")

YANG_TABLE = "etf-classifications"
BD_TABLE = "bd-securities"

# The 11-member retag set with its RATIFIED five-class target, from PRD s.3 and
# 0.9.0_WK_POSN_ASTTAX~14's t5_bar_table.py:16-28 (derived there by subtraction
# over all 285 registry rows). Not re-derived here; cited.
RETAG = [
    ("DBC", "Commodities"), ("GLD", "Commodities"), ("GSG", "Commodities"),
    ("IAU", "Commodities"), ("SLV", "Commodities"), ("USO", "Commodities"),
    ("VIXY", "Structured"), ("VXX", "Structured"), ("UVXY", "Structured"),
    ("QBER", "Structured"), ("PDBC", "Commodities"),
]
FIVE_CLASSES = ["Fixed Income / Cash", "Equity", "Structured",
                "Commodities", "Alternatives"]


class ScratchTable(object):
    """In-process stand-in for a DynamoDB table. A dict. Never the network."""

    def __init__(self, name):
        self.name = name
        self.store = {}
        self.updates = 0
        self.minted = []

    def update_item(self, Key=None, UpdateExpression=None,
                    ExpressionAttributeValues=None,
                    ExpressionAttributeNames=None, **_):
        names = ExpressionAttributeNames or {}
        values = ExpressionAttributeValues or {}
        key = Key["ticker"]
        existed = key in self.store
        item = self.store.setdefault(key, dict(Key))
        if not existed:
            self.minted.append(key)
        expr = (UpdateExpression or "").strip()
        assert expr.upper().startswith("SET "), "only SET is modelled: %r" % expr
        for clause in expr[4:].split(","):
            lhs, rhs = clause.split("=", 1)
            lhs, rhs = lhs.strip(), rhs.strip()
            attr = names.get(lhs, lhs)
            item[attr] = values[rhs]
        self.updates += 1


def make_fake_boto3(tables):
    mod = types.ModuleType("boto3")
    mod.__IS_FAKE__ = True

    class _Resource(object):
        def Table(self, name):
            print("  SCRATCH TARGET: boto3 Table(%r) INTERCEPTED -> in-process dict "
                  "(no network client exists in this process)" % name)
            return tables.setdefault(name, ScratchTable(name))

    def resource(name, **kwargs):
        assert name == "dynamodb", name
        return _Resource()

    def client(*a, **k):
        raise AssertionError("the control must never construct a real client")

    mod.resource = resource
    mod.client = client
    return mod


def seeder_source():
    with open(SEEDER_BYTES, "rb") as fh:
        raw = fh.read()
    sha = subprocess.check_output(
        ["git", "hash-object", SEEDER_BYTES]).decode().strip()
    obj = subprocess.check_output(
        ["git", "rev-parse", "HEAD:" + SEEDER_PATH_IN_REPO]).decode().strip()
    assert sha == obj, "scratch bytes %s != object %s" % (sha, obj)
    return raw.decode("utf-8"), sha, obj


def canonical_securities(src):
    """The seeder's own list, by ast.literal_eval over its real source."""
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "CANONICAL_SECURITIES":
                    return ast.literal_eval(node.value)
    raise AssertionError("CANONICAL_SECURITIES not found in the seeder source")


def baseline(members_in_script, mint_probe):
    """The scratch registry as a COMPLETED retag would leave the live one.

    Every member carries its RATIFIED five-class asset_class, plus two curator
    fields the seeder does not own (management_style, sector) so the run also
    reports whether a non-owned attribute survives.
    """
    store = {}
    for ticker, five_class in RETAG:
        if ticker not in members_in_script:
            continue
        store[ticker] = {
            "ticker": ticker,
            "asset_class": five_class,
            "sub_asset_class": ("Volatility" if five_class == "Structured"
                                else "Commodities"),
            "management_style": "passive",
            "sector": "Broad",
            "name": ticker,
            "last_updated": "2026-09-12T00:00:00Z",
            "updated_by": "posn-asttax-retag",
        }
    assert mint_probe not in store, "the mint probe must start ABSENT"
    return store


def run_seeder(src, tables):
    saved = sys.modules.get("boto3")
    sys.modules["boto3"] = make_fake_boto3(tables)
    buf = io.StringIO()
    err = None
    try:
        mod = types.ModuleType("seeder_under_test")
        mod.__file__ = os.path.join(ROOT, SEEDER_PATH_IN_REPO)
        mod.__name__ = "seeder_under_test"   # so its __main__ guard does NOT fire
        with redirect_stdout(buf):
            exec(compile(src, SEEDER_PATH_IN_REPO, "exec"), mod.__dict__)
            mod.seed(upload=True, sync_yang=True)
    except Exception as exc:
        err = "%s: %s" % (type(exc).__name__, exc)
    finally:
        assert sys.modules["boto3"].__IS_FAKE__ is True, "the fake boto3 was displaced"
        if saved is None:
            sys.modules.pop("boto3", None)
        else:
            sys.modules["boto3"] = saved
    return buf.getvalue(), err


def main():
    src, sha, obj = seeder_source()
    secs = canonical_securities(src)
    by_ticker = {s["ticker"]: s for s in secs}

    print("=" * 100)
    print("U3-AC1 -- BEFORE MEASUREMENT. THE LIVE TABLES ARE NEVER OPENED.")
    print("=" * 100)
    print("SUBJECT (real bytes, from the git object store -- the file is outside")
    print("         this worktree's sparse cone):")
    print("  repo path : %s" % SEEDER_PATH_IN_REPO)
    print("  blob sha  : %s" % sha)
    print("  asserted == HEAD object: %s" % obj)
    print("  bytes     : %d" % len(src.encode("utf-8")))
    print("")

    # ---- the seeder's own vocabulary, with its denominator ------------------
    vocab = {}
    for sec in secs:
        vocab[sec["asset_class"]] = vocab.get(sec["asset_class"], 0) + 1
    print("THE SEEDER'S asset_class VOCABULARY, enumerated over its own list:")
    print("  denominator: %d rows in CANONICAL_SECURITIES" % len(secs))
    for value in sorted(vocab):
        print("    %-16s %3d row(s)" % (repr(value), vocab[value]))
    print("  DISTINCT VALUES: %d -- %s" % (len(vocab), sorted(vocab)))
    overlap = sorted(set(vocab) & set(FIVE_CLASSES))
    print("  INTERSECTION WITH THE RATIFIED FIVE CLASSES:")
    print("    %s" % FIVE_CLASSES)
    print("    -> %s  (%d of 5)" % (overlap if overlap else "<empty>", len(overlap)))

    # ---- re-measure the row's "4 of 11" -------------------------------------
    present = [t for t, _ in RETAG if t in by_ticker]
    absent = [t for t, _ in RETAG if t not in by_ticker]
    print("")
    print("RETAG-SET MEMBERSHIP, RE-MEASURED (W14-S3 says 4 of 11; not inherited):")
    print("  denominator: %d retag members against %d seeder rows"
          % (len(RETAG), len(secs)))
    for ticker, five_class in RETAG:
        if ticker in by_ticker:
            print("    %-6s PRESENT  seeder asserts asset_class=%-16s ratified=%s"
                  % (ticker, repr(by_ticker[ticker]["asset_class"]), five_class))
        else:
            print("    %-6s absent from the seeder's list" % ticker)
    print("  MEASURED: %d of %d retag members carried by this seeder -- %s"
          % (len(present), len(RETAG), present))
    print("  the other %d are absent: %s" % (len(absent), absent))

    # ---- the mint probe -----------------------------------------------------
    retag_names = dict(RETAG)
    mint_probe = next(s["ticker"] for s in secs if s["ticker"] not in retag_names)
    print("")
    print("MINT PROBE: %r -- written by the seeder, seeded ABSENT from the scratch"
          % mint_probe)
    print("  store. If the run does not create it, the seeder is not writing at all")
    print("  and any 'survived' verdict below would be worthless.")

    # ---- the exercise -------------------------------------------------------
    yang = ScratchTable(YANG_TABLE)
    bd = ScratchTable(BD_TABLE)
    yang.store = baseline(by_ticker, mint_probe)
    tables = {YANG_TABLE: yang, BD_TABLE: bd}
    before = {t: yang.store[t]["asset_class"] for t in present}
    before_curated = {t: (yang.store[t].get("management_style"),
                          yang.store[t].get("sector")) for t in present}

    print("")
    print("-" * 100)
    print("RUNNING THE REAL SEEDER BYTES: seed(upload=True, sync_yang=True)")
    print("-" * 100)
    out, err = run_seeder(src, tables)
    tail = [ln for ln in out.splitlines() if ln.strip()]
    for line in tail[:3]:
        print("  " + line)
    print("  ... %d line(s) of seeder stdout suppressed ..." % max(0, len(tail) - 6))
    for line in tail[-3:]:
        print("  " + line)
    if err:
        print("  SEEDER RAISED: %s" % err)
    print("")
    print("  scratch %-22s update_item calls: %3d   rows minted: %d"
          % (YANG_TABLE, yang.updates, len(yang.minted)))
    print("  scratch %-22s update_item calls: %3d   rows minted: %d"
          % (BD_TABLE, bd.updates, len(bd.minted)))

    # ---- read the value back ------------------------------------------------
    print("")
    print("=" * 100)
    print("THE READ-BACK -- asset_class, stated AS A VALUE")
    print("=" * 100)
    print("  %-6s %-14s %-14s %-14s %s"
          % ("TICKER", "BEFORE", "AFTER", "RATIFIED", "VERDICT"))
    reverted = []
    for ticker in present:
        after = yang.store[ticker]["asset_class"]
        verdict = "SURVIVED" if after == before[ticker] else "CLOBBERED"
        if after != before[ticker]:
            reverted.append(ticker)
        print("  %-6s %-14s %-14s %-14s %s"
              % (ticker, before[ticker], after, retag_names[ticker], verdict))
    print("")
    print("  CLOBBERED: %d of %d members present in the seeder -- %s"
          % (len(reverted), len(present), reverted))

    # ---- the non-owned attributes -------------------------------------------
    print("")
    print("NON-OWNED ATTRIBUTES (the seeder's docstring claims these survive):")
    for ticker in present:
        now = (yang.store[ticker].get("management_style"),
               yang.store[ticker].get("sector"))
        print("  %-6s management_style/sector  before=%s  after=%s  %s"
              % (ticker, before_curated[ticker], now,
                 "SURVIVED" if now == before_curated[ticker] else "LOST"))

    # ---- the mint control ---------------------------------------------------
    minted_ok = mint_probe in yang.store
    if minted_ok:
        state = "PRESENT (asset_class=%r)" % yang.store[mint_probe]["asset_class"]
    else:
        state = "STILL ABSENT"
    print("")
    print("MINT CONTROL: %r was absent before the run; after the run it is %s"
          % (mint_probe, state))
    print("  -> the seeder %s writing. A 'survived' verdict is therefore %s."
          % ("IS" if minted_ok else "is NOT",
             "meaningful" if minted_ok else "WORTHLESS"))

    print("")
    print("=" * 100)
    if not minted_ok:
        print("BEFORE RESULT: INDETERMINATE -- the seeder minted nothing, so this")
        print("control cannot distinguish preservation from inaction.")
        return 1
    if reverted:
        print("BEFORE RESULT: THE PREMISE HOLDS. %d of %d retag members present in"
              % (len(reverted), len(present)))
        print("this seeder had a ratified five-class asset_class CLOBBERED by one")
        print("re-seed. The BEFORE state, as values:")
        for ticker in reverted:
            print("  %-6s %r  ->  %r"
                  % (ticker, before[ticker], yang.store[ticker]["asset_class"]))
    else:
        print("BEFORE RESULT: THE PREMISE IS FALSE. Every five-class value SURVIVED")
        print("the re-seed. W14-S3's assertion does not reproduce.")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## APPENDIX B -- `u3_mutant_control.py` (full source, verbatim)

Lives at `.scratch/run/u3_mutant_control.py`. It generates the patched bytes under
`.scratch/` ONLY, writes `u3_proposed_patch.diff`, and runs the three arms. It never
writes to the repo file.

```python
#!/usr/bin/env python3
"""POSN_ASTTAX.TO-U3-1 -- THE MUTANT / DISCRIMINATION CONTROL. SCRATCH ONLY.

WHAT THIS IS NOT
----------------
This is NOT U3-AC2 and NOT U3-AC3. Those criteria require changing
data/black_diamond/scripts/classification/seed_canonical_securities.py, which is
OUTSIDE this worker's <paths> grant (row POSN_ASTTAX-Z-W16-S1). NOTHING here is
written to that file, to the repo, or to any live table. The patched variant
exists only as bytes under .scratch/ and as a .diff recorded for the issuer.

WHY IT EXISTS
-------------
PROOF_OF_SPEC requires a mutant control: "a passing assertion never mutated has
never been tested". The AC1 control has so far only ever printed CLOBBERED. A
control that ALWAYS prints CLOBBERED would read identically. This script mutates
the ONE thing the verdict should depend on -- the seeder's write rule -- and
shows the verdict flips to SURVIVED while the MINT control keeps firing.

THE MUTATION REUSES THE SIBLING'S MECHANISM, it does not invent a second one.
infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-classifications.py:72-120
merge_item(): "the module wins where it knows something; the TABLE wins where
the module only has a placeholder; and where BOTH know something and they
DISAGREE, nothing is decided here -- the disagreement is returned as a conflict
for the caller to refuse on", with :293-294 making --force the only way past a
disagreement. seed_canonical_securities.py never emits a placeholder (its
vocabulary is two hardcoded values), so the operative half is the CONFLICT half.
"""
import difflib
import importlib.util
import io
import os
import subprocess
import sys
import types
from contextlib import redirect_stdout

ROOT = os.getcwd()
SCRATCH = os.path.join(ROOT, ".scratch", "run")
HEAD_BYTES = os.path.join(ROOT, ".scratch", "head", "seed_canonical_securities.py")
PATCHED_BYTES = os.path.join(SCRATCH, "patched_seed_canonical_securities.py")
DIFF_OUT = os.path.join(SCRATCH, "u3_proposed_patch.diff")
REPO_PATH = "data/black_diamond/scripts/classification/seed_canonical_securities.py"

# Reuse the AC1 control's machinery verbatim -- same scratch table, same fake boto3.
_spec = importlib.util.spec_from_file_location(
    "ac1", os.path.join(SCRATCH, "u3_ac1_before_control.py"))
ac1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ac1)


# --------------------------------------------------------------------------
# THE PATCH, expressed as anchored replacements on the real bytes.
# --------------------------------------------------------------------------
ANCHOR_SIG = "def seed(upload: bool = False, sync_yang: bool = False) -> None:"
NEW_SIG = (
    "# The fields this seeder OWNS on the Yang table. A value the table already\n"
    "# serves for one of these, that DISAGREES with the seeder's, is a CONFLICT --\n"
    "# the same rule seed-etf-classifications.py:72-120 merge_item() applies.\n"
    "YANG_OWNED_FIELDS = ('asset_class', 'sub_asset_class', 'name')\n"
    "\n"
    "\n"
    "def _yang_conflicts(yang_table, sec):\n"
    "    \"\"\"Fields the table already serves with a DIFFERENT non-blank value.\n"
    "\n"
    "    Returns [(field, live_value, seeder_value), ...]. An absent row returns []\n"
    "    -- a FIRST MINT is never a conflict and must still mint.\n"
    "    \"\"\"\n"
    "    got = yang_table.get_item(Key={'ticker': sec['ticker']})\n"
    "    live = got.get('Item') or {}\n"
    "    if not live:\n"
    "        return []\n"
    "    out = []\n"
    "    for field in YANG_OWNED_FIELDS:\n"
    "        live_value = live.get(field)\n"
    "        if live_value is None or str(live_value).strip() == '':\n"
    "            continue\n"
    "        seeder_value = sec['name'] if field == 'name' else sec[field]\n"
    "        if str(live_value) != str(seeder_value):\n"
    "            out.append((field, live_value, seeder_value))\n"
    "    return out\n"
    "\n"
    "\n"
    "def seed(upload: bool = False, sync_yang: bool = False,\n"
    "         force: bool = False) -> int:"
)

ANCHOR_COUNTERS = "    written_bd = 0\n    written_yang = 0\n"
NEW_COUNTERS = ("    written_bd = 0\n    written_yang = 0\n"
                "    preserved_yang = []\n")

ANCHOR_YANG = """        if sync_yang:
            if upload:
                yang_table.update_item(
"""
NEW_YANG = """        if sync_yang:
            # PRESERVE-DON'T-CLOBBER. This seeder's asset_class vocabulary is two
            # legacy values ('equity', 'fixed_income') and the served registry
            # carries the ratified five-class vocabulary, so an unconditional SET
            # here REVERTS a retag. Measured on a scratch copy 2026-09-13: 4 of 4
            # retag members present in this list were reverted by one re-seed
            # (VXX/UVXY 'Structured'->'equity', QBER 'Structured'->'fixed_income',
            # PDBC 'Commodities'->'equity').
            conflicts = _yang_conflicts(yang_table, sec) if upload else []
            if conflicts and not force:
                preserved_yang.append((ticker, conflicts))
                for field, live_value, seeder_value in conflicts:
                    print(f'  [PRESERVED] {ticker:10s} {field}: table serves '
                          f'{live_value!r}, seeder asserts {seeder_value!r} -- '
                          f'table wins, pass --force to override')
                continue
            if upload:
                yang_table.update_item(
"""

ANCHOR_TAIL = """    if not upload:
        print('DRY RUN -- no items written. Pass --upload to write.')
"""
NEW_TAIL = """    if not upload:
        print('DRY RUN -- no items written. Pass --upload to write.')
    if preserved_yang:
        print()
        print(f'REFUSED {len(preserved_yang)} etf-classifications row(s): the table '
              f'serves a value this seeder disagrees with.')
        print('Nothing was reverted. Re-run with --force to overwrite them.')
        return 1
    return 0
"""

ANCHOR_MAIN = "    seed(upload=args.upload, sync_yang=args.yang)\n"
NEW_MAIN = ("    parser.add_argument('--force', action='store_true',\n"
            "                        help='Overwrite an etf-classifications value the table '\n"
            "                             'already serves. Without this flag such a run REFUSES.')\n"
            "    raise SystemExit(seed(upload=args.upload, sync_yang=args.yang,\n"
            "                          force=args.force))\n")
ANCHOR_ARGS = "    args = parser.parse_args()\n"


def build_patched(src):
    out = src
    for anchor, new in ((ANCHOR_SIG, NEW_SIG),
                        (ANCHOR_COUNTERS, NEW_COUNTERS),
                        (ANCHOR_YANG, NEW_YANG),
                        (ANCHOR_TAIL, NEW_TAIL)):
        assert out.count(anchor) == 1, "anchor not unique: %r" % anchor[:60]
        out = out.replace(anchor, new)
    # the --force flag must be added BEFORE parse_args, and the call AFTER it
    assert out.count(ANCHOR_ARGS) == 1
    assert out.count(ANCHOR_MAIN) == 1
    force_arg = NEW_MAIN.split("    raise SystemExit")[0]
    call = "    raise SystemExit" + NEW_MAIN.split("    raise SystemExit")[1]
    out = out.replace(ANCHOR_ARGS, force_arg + ANCHOR_ARGS)
    out = out.replace(ANCHOR_MAIN, call)
    return out


class ScratchTableWithGet(ac1.ScratchTable):
    """The AC1 scratch table plus get_item -- the pre-read the patch needs."""

    def __init__(self, name):
        ac1.ScratchTable.__init__(self, name)
        self.reads = 0

    def get_item(self, Key=None, **_):
        self.reads += 1
        item = self.store.get(Key["ticker"])
        return {"Item": dict(item)} if item is not None else {}


def run(src, label, force=False):
    yang = ScratchTableWithGet(ac1.YANG_TABLE)
    bd = ScratchTableWithGet(ac1.BD_TABLE)
    secs = ac1.canonical_securities(src)
    by_ticker = {s["ticker"]: s for s in secs}
    retag_names = dict(ac1.RETAG)
    mint_probe = next(s["ticker"] for s in secs if s["ticker"] not in retag_names)
    yang.store = ac1.baseline(by_ticker, mint_probe)
    present = [t for t, _ in ac1.RETAG if t in by_ticker]
    before = {t: yang.store[t]["asset_class"] for t in present}

    tables = {ac1.YANG_TABLE: yang, ac1.BD_TABLE: bd}
    saved = sys.modules.get("boto3")
    sys.modules["boto3"] = ac1.make_fake_boto3(tables)
    buf = io.StringIO()
    rc, err = None, None
    try:
        mod = types.ModuleType("seeder_%s" % label)
        mod.__file__ = os.path.join(ROOT, REPO_PATH)
        mod.__name__ = "seeder_%s" % label
        with redirect_stdout(buf):
            exec(compile(src, REPO_PATH, "exec"), mod.__dict__)
            if force:
                rc = mod.seed(upload=True, sync_yang=True, force=True)
            else:
                try:
                    rc = mod.seed(upload=True, sync_yang=True)
                except TypeError:
                    rc = mod.seed(upload=True, sync_yang=True)
    except Exception as exc:
        err = "%s: %s" % (type(exc).__name__, exc)
    finally:
        assert sys.modules["boto3"].__IS_FAKE__ is True
        if saved is None:
            sys.modules.pop("boto3", None)
        else:
            sys.modules["boto3"] = saved

    after = {t: yang.store[t]["asset_class"] for t in present}
    survived = [t for t in present if after[t] == before[t]]
    return {
        "label": label, "rc": rc, "err": err, "out": buf.getvalue(),
        "present": present, "before": before, "after": after,
        "survived": survived,
        "clobbered": [t for t in present if after[t] != before[t]],
        "minted": mint_probe in yang.store, "mint_probe": mint_probe,
        "yang_writes": yang.updates, "yang_reads": yang.reads,
        "yang_minted": len(yang.minted), "ratified": retag_names,
    }


def show(r):
    print("")
    print("=" * 100)
    print("ARM: %s" % r["label"])
    print("=" * 100)
    print("  %-6s %-14s %-14s %-14s %s"
          % ("TICKER", "BEFORE", "AFTER", "RATIFIED", "VERDICT"))
    for t in r["present"]:
        print("  %-6s %-14s %-14s %-14s %s"
              % (t, r["before"][t], r["after"][t], r["ratified"][t],
                 "SURVIVED" if r["after"][t] == r["before"][t] else "CLOBBERED"))
    print("  SURVIVED %d of %d | CLOBBERED %d | rc=%r%s"
          % (len(r["survived"]), len(r["present"]), len(r["clobbered"]), r["rc"],
             "  RAISED: %s" % r["err"] if r["err"] else ""))
    print("  MINT CONTROL: %r %s   (yang update_item=%d, get_item=%d, minted=%d)"
          % (r["mint_probe"],
             "MINTED -- the seeder is writing" if r["minted"]
             else "NOT MINTED -- the seeder wrote nothing, verdict WORTHLESS",
             r["yang_writes"], r["yang_reads"], r["yang_minted"]))
    pres = [ln for ln in r["out"].splitlines() if "[PRESERVED]" in ln
            or "REFUSED" in ln]
    for ln in pres[:8]:
        print("  " + ln.strip())


def main():
    src, sha, obj = ac1.seeder_source()
    patched = build_patched(src)
    with open(PATCHED_BYTES, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(patched)
    diff = list(difflib.unified_diff(
        src.splitlines(True), patched.splitlines(True),
        fromfile="a/" + REPO_PATH, tofile="b/" + REPO_PATH, n=3))
    with open(DIFF_OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.writelines(diff)

    print("=" * 100)
    print("MUTANT / DISCRIMINATION CONTROL -- SCRATCH ONLY, NOTHING IN THE REPO IS TOUCHED")
    print("=" * 100)
    print("  original bytes : %s (sha %s, == HEAD object %s)"
          % (HEAD_BYTES, sha[:12], obj[:12]))
    print("  patched bytes  : %s  (SCRATCH ONLY -- not the repo file)" % PATCHED_BYTES)
    print("  proposed diff  : %s  (%d diff lines, +%d/-%d)"
          % (DIFF_OUT, len(diff),
             len([x for x in diff if x.startswith("+") and not x.startswith("+++")]),
             len([x for x in diff if x.startswith("-") and not x.startswith("---")])))
    print("  repo file at %s is UNTOUCHED -- it is outside this worker's <paths> grant"
          % REPO_PATH)

    neg = run(src, "NEGATIVE CONTROL -- pre-patch bytes, same input (must still revert)")
    pos = run(patched, "MUTANT -- patched bytes, same input (the verdict must flip)")
    forced = run(patched, "OVERRIDE -- patched bytes with --force (must revert again)",
                 force=True)
    show(neg)
    show(pos)
    show(forced)

    print("")
    print("=" * 100)
    print("DISCRIMINATION VERDICT")
    print("=" * 100)
    discriminates = (len(neg["clobbered"]) == len(neg["present"])
                     and len(pos["survived"]) == len(pos["present"])
                     and neg["minted"] and pos["minted"]
                     and len(forced["clobbered"]) == len(forced["present"]))
    print("  pre-patch  : CLOBBERED %d of %d, minted=%s"
          % (len(neg["clobbered"]), len(neg["present"]), neg["minted"]))
    print("  patched    : SURVIVED  %d of %d, minted=%s, rc=%r"
          % (len(pos["survived"]), len(pos["present"]), pos["minted"], pos["rc"]))
    print("  --force    : CLOBBERED %d of %d  (the override still overrides)"
          % (len(forced["clobbered"]), len(forced["present"])))
    print("")
    if discriminates:
        print("  OK: THE CONTROL DISCRIMINATES. The two arms read DIFFERENTLY on the same")
        print("  input, the mint control fires in BOTH, and --force still overrides -- so")
        print("  'CLOBBERED' in AC1 is a property of the seeder's write rule, not of this")
        print("  instrument. A first mint still mints: %d row(s) minted under the patch."
              % pos["yang_minted"])
    else:
        print("  ERROR: THE CONTROL DOES NOT DISCRIMINATE -- both arms read the same, or a")
        print("  mint control did not fire. Report this rather than the result.")
    print("")
    print("  RESTATED: this is a SCRATCH demonstration for the issuer. U3-AC2 and U3-AC3")
    print("  remain BLOCKED -- the repo file is outside the <paths> grant (W16-S1) and no")
    print("  edit to it was made.")
    return 0 if discriminates else 1


if __name__ == "__main__":
    sys.exit(main())
```

---

*Recorded by `0.9.0_WK_POSN_ASTTAX~16` on branch `wk-posn_asttax-4-3`. Rows filed: `POSN_ASTTAX-Z-W16-S1`, `-S2`, `-S3`, all BLOCKING/ARMED, disarm owner `2.0.0_SA_COO~Z`. Order left at `staged` -- three of four criteria FAIL, and a status flip is never a way to release a gate.*


---

# RE-GRADE ADDENDUM -- against the RE-CUT order @`8e67653049`

**Added by the same worker, `0.9.0_WK_POSN_ASTTAX~16`, in a later session.**
**Everything above this line is the first-cut record and is unchanged.** It was
written when the order still demanded an EDIT, and its blocked verdicts were
correct for the clauses as then written. Read it as history; read this section
for the standing verdict.

## WHY THERE IS A SECOND VERDICT

The issuer re-cut the order after this worker refused to proceed, for two
defects it confirmed at source:

1. the `<paths>` grant named
   `infra/aws/lambda/v2_portal/yang_pipeline/seed_canonical_securities.py`,
   which has **never existed** -- 0 of 33,731 index entries, 0 commits on any
   ref;
2. the real file,
   `data/black_diamond/scripts/classification/seed_canonical_securities.py`,
   is lane **POD4** (`.owned-paths.yaml:1712`), so POSN may not write it.

So `AT4-s-3` became **DISCLOSE-AND-HAND-OFF, not an edit**. A second,
unrelated defect -- `org/modules` and `org/surprise_channel` missing from this
worktree's sparse cone, which made `commit-gate.sh` raise at import scope and
blocked *every* commit -- was fixed by the issuer between sessions. **Both were
re-measured this session rather than taken on report.**

## THE STANDING VERDICT

| Criterion | First cut | Now | What decided it |
|---|---|---|---|
| `U3-AC1` | PASS | **PASS (not re-run)** | Preserved by the re-cut; evidence stands. |
| `U3-AC2` | FAIL (blocked) | **PASS** | The patch RECORDED as a deliverable, verified a true delta of the real bytes, owning lane named, hand-off stated. |
| `U3-AC3` | FAIL (blocked) | **PASS** | The same scratch arms now answer the clause: survives 4 of 4, mint control fires, pre-patch arm still reverts. |
| `U3-AC4` | FAIL (blocked) | **PASS** | The gate runs and is clean on the produced bytes; a broken `.py` is still refused. |

**Nothing measured was discarded and nothing was re-measured to a better
answer.** The same diff, generated against the same bytes, and the same
three-arm control now CARRY the clauses instead of blocking on them. The only
thing that changed is the act the order asks for.

## WHAT THIS WORKER DID NOT DO

- **No edit to the POD4 surface.** `git status --porcelain -- data/black_diamond/`
  = 0 lines, against `git ls-files -- data/black_diamond/` = 176, so the empty
  status is CLEAN and not MATCHED-NOTHING. The blob at HEAD is still
  `fbbc7165d331`.
- **No live table opened.** Every arm replaces `boto3` in `sys.modules` before
  the seeder bytes execute and asserts `__IS_FAKE__`.
- **No status flip, and the order file is absent from both commits on this
  branch.** This worktree's copy of the order predates the re-cut, so
  committing it to flip a status would silently revert the issuer's correction
  on drain. The flip belongs to the issuer at HEAD.

## TWO NEW ROWS

- **`POSN_ASTTAX-Z-W16-S4`** -- the gate's non-ASCII limb is scoped to `infra/`
  and `.tools/` (`commit_gate_runner.py:427-429`), so it can never fire on
  `data/black_diamond/**`; a probe carrying 5 non-ASCII bytes passed with zero
  WARN lines. **A non-run prints identically to a clean pass.**
  OBSERVATION / INERT.
- **`POSN_ASTTAX-Z-W16-S5`** -- the re-cut retired `U3-AC2`'s edit but left
  `U3-AC4` naming its output ("the changed `.py`"), and this cell now changes no
  `.py` in the repo. The clause was graded against the bytes the hand-off
  delivers, and that scoping is disclosed so L9 can reject it rather than
  inherit it. OBSERVATION / INERT.

`W16-S1`, `-S2` and `-S3` are left exactly as filed: the channel is
append-only, and their disarm is the issuer's to record.

## WHAT IS OWED TO WHOM

**POD4 (DS)** holds the only remaining act: apply `u3_proposed_patch.diff` to
`data/black_diamond/scripts/classification/seed_canonical_securities.py` under
its own lane and gate. `u3_ac2_handoff.md` is the hand-off packet -- the
mechanism, the measurement, both controls, and the one line the patch does not
change. **POSN measured this and POSN does not own the fix.**

*Re-graded by `0.9.0_WK_POSN_ASTTAX~16` on branch `wk-posn_asttax-4-3`.*
