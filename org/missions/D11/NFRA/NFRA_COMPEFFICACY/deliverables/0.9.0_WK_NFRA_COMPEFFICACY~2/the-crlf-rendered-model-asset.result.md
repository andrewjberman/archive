# CE-e-1 -- THE CRLF-RENDERED MODEL ASSET: what was measured, what was fixed, what still fails

**TO:** `NFRA_COMPEFFICACY.TO-CE-E-1` | **assignee:** `0.9.0_WK_NFRA_COMPEFFICACY~2` |
**branch:** `wk-nfra_compefficacy-8-1`, cut from CLOUD@`e8f74b6717` | **fix commit:** `d9be5ef2c0`
| **worktree:** `C:/tmp/wk-compeff-8-1` | **date:** 2026-09-09/10

**HEADLINE.** The fix is real and measured: a fresh linked worktree cut from the fixed branch renders
**2 of 2** tracked members of `org/modules/graph/potion/model/` byte-identical to the MAIN tree and to
`MANIFEST.json`, `comp-which` there emits **0 bytes** on stderr instead of the potion ALARM, and the
same 78 candidates come back ordered differently at **76 of 78** positions from the lexical fallback.
**E1-AC2 PASSES by output. E1-AC1 FAILS by output on arm (e) only -- 9 of 11 arms PASS** -- and it
fails for a reason no fix inside this order's grant can remove: the baseline arm (e) compares against
was itself captured under the lexical fallback, so arm (e) contradicts arms (b) and (c) of the same
criterion. Row `NFRA_COMPEFFICACY-W2-S2` (BLOCKING, ARMED) carries it. **TO-CE-E-1 STAYS OPEN; the
`<status>` was NOT flipped to `complete`.**

---

## 1. THE FIX SHAPE TAKEN, AND WHAT THE OTHER WOULD HAVE COST

**Taken: (i), the `.gitattributes` entry -- one line, `org/modules/graph/potion/model/** binary`,**
plus a block of comment stating the measurement, the domain and the cost. `d9be5ef2c0`, 1 file
changed, 27 insertions.

**Why (i) and not (ii).** The order's own refusal clause decides it: *"A fix that makes the ALARM
disappear WITHOUT making the fresh worktree's bytes equal the manifest is the wrong fix and this
order refuses it."* Only (i) makes the bytes equal. And (ii) was not merely more expensive here, it
was **BLOCKING**: `potion_embed.py:57-63` hashes RAW bytes (`_sha256(p)` over the file as it sits on
disk), so a manifest carrying an LF-NORMALISED digest would mismatch **in the MAIN tree**, where the
raw bytes ARE the LF bytes -- it would move the false alarm from the worker slots to the main tree
rather than remove it. Making (ii) work therefore requires the VERIFIER to normalise before hashing,
and `potion_embed.py` is outside this order's `<paths>` and explicitly out of grant. It is also the
shape this repository has already refused once, in `.gitattributes`' own audit-log block: *"DO NOT fix
this by normalizing line endings inside the comparator: that blinds a tamper detector to a real
whole-file rewrite in order to silence a checkout artifact."* A hash pin normalised at both ends stops
being a pin on the bytes the loader loads.

**Why `binary` (= `-text -diff -merge`) and not `-text` alone.** `-text` stops the eol conversion,
which is the entire measured defect. It leaves the default TEXT MERGE armed on `tokenizer.json`, and a
clean auto-merge of a hash-pinned asset produces bytes matching neither parent and breaks the pin
**with no conflict** -- silent-wrong, on an asset whose whole design is to fail loud. `-merge` turns
that case into a conflict. **COST, stated:** `git diff` renders these two members as
`Binary files ... differ` instead of a text diff; accepted, because any change to a pinned member must
be re-declared in `MANIFEST.json`'s hash anyway, so the manifest and not the diff is this directory's
review instrument. **NON-APPLICATION:** `MANIFEST.json` and `potion_embed.py` are deliberately NOT
covered and stay ordinary reviewable repo text.

**Why `/**` over the directory and not a per-file line** -- see section 3.

---

## 2. THE BASELINE WITH ITS ENVIRONMENT (ruling R-8)

Measured at this seat, 2026-09-09 ~22:0xZ, re-derived rather than taken from the face:

| reading | value |
|---|---|
| `git config core.autocrlf` | `true` |
| `git --version` | `git version 2.55.0.windows.2` |
| python | `3.12.10` (`C:/Users/AndrewBerman/AppData/Local/Programs/Python/Python312/python.exe`) |
| MAIN tree | `C:/Users/AndrewBerman/Desktop/ajb_workspace` (DERIVED from `git worktree list --porcelain`, never hardcoded) |
| MAIN tree HEAD | `9328e15f45 [CLOUD]` |
| this worktree | `C:/tmp/wk-compeff-8-1` @ `d9be5ef2c0 [wk-nfra_compefficacy-8-1]`, base `e8f74b6717` |
| manifest | `C:/Users/AndrewBerman/Desktop/ajb_workspace/org/modules/graph/potion/MANIFEST.json` |
| ranker mode at the MAIN tree | SEMANTIC (potion loads; 0 B on stderr) |
| ranker mode in an UNFIXED linked worktree | LEXICAL FALLBACK (the ALARM line on stderr) |

```
$ git ls-files --eol -- org/modules/graph/potion/model/          # MAIN tree, pre-fix
i/-text w/-text attr/                   org/modules/graph/potion/model/model.safetensors
i/lf    w/lf    attr/                   org/modules/graph/potion/model/tokenizer.json

$ git ls-files --eol -- org/modules/graph/potion/model/          # C:/tmp/wk-compeff-8-1, pre-fix
i/-text w/-text attr/                   org/modules/graph/potion/model/model.safetensors
i/lf    w/crlf  attr/                   org/modules/graph/potion/model/tokenizer.json

$ git check-attr -a -- <both members>                            # pre-fix, either tree
(no output -- no attribute of any kind was set on either member)
```

| member | MAIN tree sha256 | bytes | MANIFEST declares | agrees |
|---|---|---|---|---|
| `model.safetensors` | `f95ffde02ad06f63ae38eb9d400038cd5ccaf8411ec3cb650c6025113f96cbb8` | 7,559,256 | same, 7,559,256 | YES |
| `tokenizer.json` | `e67e803f624fb4d67dea1c730d06e1067e1b14d830e2c2202569e3ef0f70bb50` | 683,666 | same, 683,666 | YES |

**2 of 2 tracked members, 2 of 2 pinned by the manifest, 2 of 2 agree at the MAIN tree.** In this
fresh linked worktree, pre-fix, `tokenizer.json` read `0a1168df8209a591defdc781567f11f8ea5b400c60b994350f8892e7bdfe829b`,
713,343 B -- the issuer's numbers, re-derived independently here.

---

## 3. THE POPULATION IS THE DIRECTORY, AND WHY THE SECOND MEMBER WAS ALREADY PROTECTED

**Census: 2 tracked files of 2 present on disk under `org/modules/graph/potion/model/`** (denominator
from `git ls-files -z -- org/modules/graph/potion/model/` in each tree, printed by both scripts).

- `tokenizer.json` -- **DIVERGENT** pre-fix: `i/lf` in the index, `w/lf` in the MAIN tree, `w/crlf` in
  every fresh linked worktree.
- `model.safetensors` -- **IDENTICAL in both trees, pre-fix, and it is NOT protected by any rule.**
  The instrument that answers *why* is `git ls-files --eol`, which reads `i/-text w/-text` for it:
  **git's own binary heuristic** classified it non-text, and eol conversion never applies to a file
  git considers binary. Measured cause, not inferred: `open(...,'rb').read(8000)` finds a NUL at
  **byte offset 1** (the safetensors format opens with an 8-byte little-endian u64 header length, so
  bytes 1..7 are zero for any model under 2^56 bytes); the same read over `tokenizer.json`'s first
  8000 bytes finds **no NUL at all**. Git's `buffer_is_binary` looks for a NUL in the first 8000
  bytes, so the two members fall on opposite sides of a heuristic neither of them declares.

**That is the shared-dependency answer the order asked for.** The members do not behave the same, and
the reason the second one was safe is INCIDENTAL to its first 8000 bytes -- it belongs to no rule, no
attribute and no manifest. A check scoped to `tokenizer.json` would have certified nothing about the
directory, and a check scoped to *the two current members* would have certified a directory whose
protection for one member is an accident of file format. Hence the entry is written over the
directory (`/**`), not per-file: **any future vendored member with a NUL-free head -- a second
`*.json`, a `merges.txt`, a `vocab.txt` -- would have inherited the defect unprotected.** After the
fix both members read `attr/-text`, so the second member's protection is now DECLARED rather than
borrowed from a heuristic.

---

## 4. CRITERION-BY-CRITERION: INVOCATION, OUTPUT, rc, DENOMINATOR

### E1-AC2 -- PASS by output

```
$ timeout 300 python org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~2/cee1_fresh_worktree_probe.py
```
rc **0**, elapsed **59.4 s** of the 300 s bound. Verbatim:

```
CE-e-1 / E1-AC2 -- FRESH-WORKTREE PROBE of the vendored POTION model asset
  invoked from : C:/tmp/wk-compeff-8-1/org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~2
  repo root    : C:/tmp/wk-compeff-8-1
  ref          : wk-nfra_compefficacy-8-1  (DEFAULT = the invoking worktree's own branch; --ref overrides)
  ref sha      : d9be5ef2c0c1b8005d08a3f6d4fa63f5ed72db1b
  ref carries `org/modules/graph/potion/model/**` in .gitattributes : YES
  core.autocrlf: true

CUT: git worktree add -b cee1-probe-34200-1789006344 C:/tmp/cee1-probe-34200-1789006344 d9be5ef2c0c1b8005d08a3f6d4fa63f5ed72db1b
  rc=0  44.6s  -> C:/tmp/cee1-probe-34200-1789006344

CENSUS in the FRESH tree C:/tmp/cee1-probe-34200-1789006344
  tracked under org/modules/graph/potion/model/ : 2
  present on disk under org/modules/graph/potion/model/ : 2  (model.safetensors, tokenizer.json)
  manifest     : C:/tmp/cee1-probe-34200-1789006344/org/modules/graph/potion/MANIFEST.json
  manifest declares 2 model_files_sha256 entr(ies)
  ls-files --eol: i/-text w/-text attr/-text            	org/modules/graph/potion/model/model.safetensors
  ls-files --eol: i/lf    w/lf    attr/-text            	org/modules/graph/potion/model/tokenizer.json

COMPARE: fresh-tree bytes vs the manifest the loader reads, 2 of 2 tracked file(s)
  [MATCH] model.safetensors    fresh sha256 f95ffde02ad06f63ae38eb9d400038cd5ccaf8411ec3cb650c6025113f96cbb8  7559256 B
                               manifest     f95ffde02ad06f63ae38eb9d400038cd5ccaf8411ec3cb650c6025113f96cbb8  7559256 B
  [MATCH] tokenizer.json       fresh sha256 e67e803f624fb4d67dea1c730d06e1067e1b14d830e2c2202569e3ef0f70bb50  683666 B
                               manifest     e67e803f624fb4d67dea1c730d06e1067e1b14d830e2c2202569e3ef0f70bb50  683666 B

RESULT: 2 of 2 tracked file(s) MATCH the manifest (2 pinned by the manifest, 0 tracked-but-unpinned: none)

CLEANUP
  git worktree remove --force C:/tmp/cee1-probe-34200-1789006344  -> rc=0
  git branch -D cee1-probe-34200-1789006344  -> rc=0
  git worktree list --porcelain: 11 worktree(s); this slot still listed: NO

  elapsed 59.4s
FRESH-WORKTREE-ASSET-MATCHES-MANIFEST
```

**Denominator: 2 of 2 tracked members; 2 of 2 pinned; 0 tracked-but-unpinned.** The probe reports an
unpinned tracked member separately and never counts it as a match -- a member the manifest does not
pin is not evidence of agreement.

### E1-AC1 -- FAIL by output (9 of 11 arms PASS; arms failed: `e:main`, `e:fresh`)

```
$ timeout 900 python org/missions/D11/NFRA/NFRA_COMPEFFICACY/deliverables/0.9.0_WK_NFRA_COMPEFFICACY~2/test_cee1_model_asset_rendering.py
```
rc **1**, elapsed **105.3 s** of the 900 s bound. The summary, verbatim:

```
  [PASS] a                        the manifest's declared hash equals the MAIN tree's bytes for 2 of 2 tracked member(s), and every tracked member is pinned
  [PASS] b:before-fails           BEFORE the fix the arm FAILS as it must: 1 of 2 equal to MAIN, 1 of 2 equal to the manifest -- a detector that cannot go non-zero on the positive case is a constant
  [PASS] b:after-passes           AFTER the fix: 2 of 2 tracked member(s) equal to the MAIN tree AND 2 of 2 equal to the manifest
  [PASS] c:no-alarm               the fresh fixed tree emits NO potion ALARM (stderr 0 B)
  [PASS] c:ranks-semantically     the same 78 candidates are ordered DIFFERENTLY from the lexical fallback at 76 of 78 positions -- the ranker is not the fallback
  [PASS] d:alarm-reproduced       the negative control (no fix) reproduces the ALARM line verbatim on stderr
  [PASS] d:lexical-reproduced     the negative control's ranking is the LEXICAL one, 78 candidates, differing from the fixed tree's at 76 positions
  [FAIL] e:main                   P4-AC1's three byte-equality arms (c, f, e:real-byte-equal) PASS at the MAIN tree: c=False f=False e=False (denominator 3 of 3 arms, 5 of 5 questions)
  [FAIL] e:fresh                  P4-AC1's three byte-equality arms PASS in the FRESH worktree: c=False f=False e=False (denominator 3 of 3 arms, 5 of 5 questions)
  [PASS] e:main-equals-fresh      the FRESH worktree now reads IDENTICALLY to the MAIN tree, 5 of 5 questions -- the checkout-property RED is gone
  [PASS] f                        2 of 2 worktrees this run cut are removed and their branches deleted; 0 leak(s)

  9 of 11 arm(s) PASS   elapsed 105.3s
  arms failed: e:main, e:fresh
NOT ENFORCED -- 2 arm(s) failed. NO TOKEN.
```

The two refs the run cut, printed by the battery:

```
  AFTER  ref   : wk-nfra_compefficacy-8-1         sha d9be5ef2c0c1b8005d08a3f6d4fa63f5ed72db1b  carries `org/modules/graph/potion/model/**`: YES
  BEFORE ref   : d9be5ef2c0c1b8005d08a3f6d4fa63f5ed72db1b^ sha e8f74b6717dada37c908b2417456306d06c07b86  carries `org/modules/graph/potion/model/**`: NO
```

**Arm (c)/(d), the ranker discriminator -- printed, not asserted.** Same question
(`what produces canonical_prices.parquet?`), each tree's own spilled rank file, `comp-which` invoked
by explicit path in each tree:

```
    AFTER  (semantic) : 78 candidates ranked; top 10 ['comp-estate', 'comp-pipescript', 'comp-dataflow', 'comp-find', 'comp-icedrill', 'comp-dups', 'comp-similar', 'comp-system', 'comp-chainrun', 'comp-validate']
    BEFORE (lexical)  : 78 candidates ranked; top 10 ['comp-estate', 'comp-pipescript', 'comp-cluster', 'comp-constants', 'comp-dataflow', 'comp-ontolint', 'comp-parity', 'comp-tooltip', 'comp-adversary', 'comp-assets']
    candidate SET identical: True (78 of 78)
    ORDER differs at 76 of 78 positions
```

and the negative control's stderr, verbatim:

```
ALARM: POTION semantic embedder unavailable -> falling back to lexical relevance (ValueError: POTION hash-mismatch on tokenizer.json: manifest=e67e803f624fb4d67dea1c730d06e1067e1b14d830e2c2202569e3ef0f70bb50 vendored=0a1168df8209a591defdc781567f11f8ea5b400c60b994350f8892e7bdfe829b (FAIL-CLOSED))
```

against **0 bytes of stderr** in the fixed tree. Every `comp-which` in this cell was run as
`<python> <TREE>/.tools/comp-which "<q>"` with `cwd=<TREE>` -- **never** the `~/bin` forwarder, which
is baked to the MAIN tree and would have run the file this cell did not change (row `W1-S2`; the
forwarder is cell `CE-e-2`'s subject and is live until that cell lands).

### E1-AC3 -- judgment; RECORDED with evidence, NO VERDICT

Section 6 below. Graded by `3.0.0_SA_CVO` at L9.

---

## 5. ARM (e): WHY IT FAILS, AND WHY NO FIX IN THIS GRANT COULD MAKE IT PASS

Arm (e) requires `P4-AC1`'s three byte-equality arms (`c`, `f`, `e:real-byte-equal` -- the four C-S46
regression phrasings plus the real-subject question) to PASS at the MAIN tree AND in the fresh
worktree. They compare live ranked lists against the STORED baseline
`.../deliverables/0.9.0_WK_NFRA_COMPEFFICACY~1/cep4_before.json`.

**That baseline was captured under the LEXICAL FALLBACK.** The battery reads its environment off the
artifact itself and prints it: **7 of 7 captured questions carry the potion ALARM in their own
`terminal` block.** It carries no environment field; the ALARM inside its payload is the only tell --
exactly the R-8 defect (`a stored baseline names its environment ... a baseline without its
environment is not a baseline`), and exactly what `NFRA_COMPEFFICACY-S40` predicted.

Three trees, the same 5 questions, this seat, ranked-list diff against that baseline:

| tree | ranker | phrasing 1 | 2 | 3 | 4 | REAL_Q | verdict |
|---|---|---|---|---|---|---|---|
| `C:/tmp/wk-compeff-8-1` (UNFIXED worker slot) | lexical (ALARM) | 0 | 0 | 0 | 0 | 0 | byte-equal 5 of 5 |
| `C:/Users/AndrewBerman/Desktop/ajb_workspace` (MAIN) | semantic | 784 | 800 | 836 | 806 | 874 | 0 of 5 |
| `C:/tmp/cee1-after-<pid>` (FRESH, FIXED) | semantic | 784 | 800 | 836 | 806 | 874 | 0 of 5 |

and **MAIN vs FRESH-FIXED: 5 of 5 BYTE-EQUAL** (`check e:main-equals-fresh`, PASS).

**The clause is unsatisfiable alongside its own siblings.** Arm (b) demands the fresh tree's bytes
equal the manifest; arm (c) demands the ranker there NOT be the fallback. The only world in which arm
(e) passes is one where BOTH trees run the fallback -- which is the defect this cell exists to remove.
So the round-7 false RED is **gone** in the sense the trailing clause names ("gone rather than
moved"): the worker slot and the main tree now read identically, 5 of 5. What remains red is the
BASELINE, not the checkout, and its remedy is a re-capture of `cep4_before.json` (or a re-cut of the
clause to the cross-tree equality this battery already prints) -- an artifact under
`deliverables/0.9.0_WK_NFRA_COMPEFFICACY~1/`, which **this order's `<paths>` does not grant**.

Filed as `NFRA_COMPEFFICACY-W2-S2` (BLOCKING, ARMED, `disarm_owner` `2.0.0_SA_COO` -- the assignment
`S40` already made). **E1-AC1 is reported FAIL and the order is NOT flipped to `complete`.** A valid
instance is not a met order.

---

## 6. E1-AC3 -- THE READING FOR THE CVO (no verdict)

**(a) Which fix shape, and what the other would have cost.** Section 1. Shape (i), `binary` over the
directory; shape (ii) was BLOCKING inside this grant, not merely dearer, because the verifier hashes
raw bytes and the verifier is out of `<paths>`.

**(b) Was the directory's OTHER member affected, and what that says about scoping a check to the
member a row named.** `model.safetensors` was NOT converted -- and the reason is not a rule. It is
`i/-text` because git's binary heuristic finds a NUL at byte offset 1 (section 3). Two members of one
directory, one converted and one not, with **zero declared difference between them**: a check scoped
to the member `S40` named would have passed on a directory whose second member is protected by
accident. What the members SHARE is the directory's attribute state, and before this commit that
shared state was *nothing at all*. The measurable consequence is forward-looking rather than present:
today's population is safe (1 of 2 by rule after the fix, 1 of 2 by heuristic before it), and the next
NUL-free member added to that directory would have been the uncovered one. `/**` closes it.

**(c) What a worker seat now inherits that it did not before, against FWD-9's sentence** (*"a tool
cleared here stays cleared from any seat"*). Before: every fresh linked worktree ran `comp-which`'s
LEXICAL fallback, so a tool cleared at the main tree was measurably NOT the same tool in a worker
slot -- 78 candidates re-ordered at 76 of 78 positions, one stderr line as the only tell, and a
ranking battery reading a RED that belonged to the checkout. After: a fresh worktree cut from the
fixed branch renders 2 of 2 model members equal to the manifest, the loader does not fail closed, and
the worker slot's ranked lists are 5 of 5 byte-equal to the main tree's on the C-S46 set. **The
RANKER limb of FWD-9 now holds for a worker seat, measured, on this instrument.**

**(d) What is still NOT true of a worker seat after this cell.** Four things, each measured:
1. **The bare-name comp-tool forwarders still resolve to the MAIN tree.** `~/bin/comp-which` is baked
   to `C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/comp-which`; a worker who types
   `comp-which` in a worktree runs the file it did not change. Row `W1-S2`, cell `CE-e-2` -- the next
   order. Every reading in this cell was taken by explicit path for exactly that reason.
2. **The stored ranked-list baseline still does not name its environment** (section 5, row `W2-S2`):
   any future cell diffing comp-which rankings against `cep4_before.json` reads a RED on a correctly
   configured tree.
3. **Worktrees cut BEFORE the fix do not self-heal, and now show the asset as MODIFIED.** Census of
   the live fleet: 11 worktrees; 6 carry no copy of the file; of the 5 that do, 1 (the MAIN tree)
   holds the LF bytes and **4 hold the CRLF bytes** -- `C:/tmp/mstr-reconcile-20260904`,
   `C:/tmp/wk-cldgrph-6-2`, `C:/tmp/wk-compeff-8-1` (this seat's own) and `C:/tmp/wk-etfs-2-1`, two of
   them other live workers' slots. Row `W2-S3` (ARMED): the hazard is not the `M`, it is a broad
   `git add` there writing the 713,343 B blob into the index, which would break the pin for the whole
   estate. A path-named `safe-commit` does not stage it.
4. **This cell changed nothing about the ROUTER, the population or the manifest** -- only how git
   renders two files. A worker seat inherits a working semantic ranker, not a better one.

**Evidence with vintage:** `.gitattributes`@`d9be5ef2c0` (the entry), `org/modules/graph/potion/MANIFEST.json`@`e8f74b6717`
(unchanged by this cell), `org/modules/graph/potion/potion_embed.py`@`e8f74b6717` `:57-63` (the raise)
and `:82-94` (the ALARM), `cep4_before.json`@`e8f74b6717` (7 of 7 ALARM-bearing captures),
`NFRA_COMPEFFICACY-S40`@`e8f74b6717`.

---

## 7. CONTROLS

**MUTANT -- FIRED-AS-EXPECTED.** The fix reverted, run through the SAME detector at the SAME
invocation: `python .../cee1_fresh_worktree_probe.py --ref d9be5ef2c0^` (= `e8f74b6717`, the fix
commit's parent). Output: `ref carries ... : NO`, `ls-files --eol: i/lf w/crlf attr/`,
`[DIFFER] tokenizer.json fresh sha256 0a1168df8209a591... 713343 B` vs
`manifest e67e803f624fb4d6... 683666 B`, `RESULT: 1 of 2 tracked file(s) MATCH the manifest`,
`NO TOKEN`, elapsed 58.7 s. The detector returns non-zero on the positive case; it is not a constant.
The battery carries the same control internally as arms `b:before-fails`, `d:alarm-reproduced` and
`d:lexical-reproduced`.

**A SECOND, UNPLANNED MUTANT THIS RUN PRODUCED, AND IT IS WORTH THE RECORD.** The battery's first run
resolved its BEFORE ref with `git rev-list -S<string>`, which this git (2.55.0.windows.2) **rejects
with rc 129 and a usage block** -- `-S` is a `git log` option. The unchecked rc left the BEFORE ref
empty, `rev-parse "HEAD^{commit}"` resolved it to HEAD, i.e. **to the fix commit**, and the negative
control silently became a second copy of the positive one: arms `c:ranks-semantically`,
`d:alarm-reproduced` and `d:lexical-reproduced` all read FAIL with `0 of 78 positions` differing, and
`b:before-fails` read `2 of 2 equal` -- a control that could not fail, wearing a failure's clothes.
Fixed two ways: the pickaxe is now `git log -1 --full-history --format=%H -S<pattern>` with its rc
checked, and the battery now **REFUSES to run** if the resolved BEFORE ref carries the entry or equals
the AFTER ref. Both runs are on the record (`.scratch/battery_run1.txt`, `battery_run2.txt`; scratch,
not repo artifacts).

**DETERMINISM -- STABLE.** The probe run twice, same input, same tree: **0 of 34 output lines differ**
after normalising the two declared non-deterministic tokens (the scratch slot name, which is
pid+epoch, and the elapsed-seconds readings). Both runs rc 0 with the token.

**GRAIN.** Every hash in this record is `sha256` over the file **as it sits on disk in a named tree**,
which is the same object `potion_embed.py:_sha256` reads -- not `git hash-object`, not the index blob.
On this `core.autocrlf=true` box those are three different objects and only the first is the one the
loader pins.

---

## 8. WORKTREE HYGIENE

Every worktree this cell cut was removed and its branch deleted. Cut and removed: `ce-e1-probe-manual`
(exploratory), `cee1-probe-34200-1789006344`, `cee1-probe-33540-1789006440`, two determinism runs, and
`cee1-before-<pid>` / `cee1-after-<pid>` in each of the two battery runs. Proof, from the battery's own
arm (f) at the end of the accepted run:

```
  git worktree list --porcelain -- 11 worktree(s) now:
    C:/Users/AndrewBerman/Desktop/ajb_workspace
    C:/tmp/mstr-reconcile-20260904
    C:/tmp/staudt_layerD_T0
    C:/tmp/staudt_layerD_T1
    C:/tmp/staudt_layerD_T2
    C:/tmp/staudt_layerD_T3
    C:/tmp/wk-cldgrph-6-2
    C:/tmp/wk-compeff-8-1
    C:/tmp/wk-etfs-2-1
    C:/Users/AndrewBerman/Desktop/ajb_workspace/.claude/worktrees/agent-acc852ec7d8dbfdc5
    C:/Users/AndrewBerman/Desktop/scty-build
  git branch --list 'cee1-*' -> (none)
  [PASS] f                        2 of 2 worktrees this run cut are removed and their branches deleted; 0 leak(s)
```

The 11 listed are all pre-existing; none belongs to this cell.

---

## 9. ROWS FILED

| id | class | hazard | one-line subject |
|---|---|---|---|
| `NFRA_COMPEFFICACY-W2-S1` | OBSERVATION | INERT | the accept's fresh tree cannot be cut from the literal ref `CLOUD` while the fix is on the worker branch; both scripts default to the invoking worktree's branch (which IS `CLOUD` post-drain) and print the ref they resolved |
| `NFRA_COMPEFFICACY-W2-S2` | **BLOCKING** | ARMED | E1-AC1 arm (e) is unsatisfiable alongside arms (b)/(c) -- the baseline it compares against was captured under the lexical fallback; `disarm_owner` `2.0.0_SA_COO` |
| `NFRA_COMPEFFICACY-W2-S3` | OBSERVATION | ARMED | the attribute converts a silent conversion into a visible `M` in the 4 of 5 live worktrees holding CRLF bytes; a broad `git add` there would commit the CRLF blob and break the pin estate-wide; `disarm_owner` `2.0.0_SA_COO` |

---

## 10. WHAT WAS **NOT** DONE

- **No model bytes were rewritten.** `d9be5ef2c0` touched `.gitattributes` only, 1 file, 27
  insertions. The index blobs are unchanged: `7899ce87d35b3287211672afd2474c21ef99bc27`
  (`model.safetensors`) and `3e511f68ccf95c33b9ffd214a94c6d25bdb3034f` (`tokenizer.json`) before and
  after. This seat's own worktree copy of `tokenizer.json` still holds the CRLF bytes and is left
  untouched (bytes verified unchanged at `0a1168df8209a591...`; only its mtime moved, from the
  deliberate stat-cache invalidation in section 6(d)3) -- restoring it is a write to
  `org/modules/graph/potion/model/`, which the BOUNDS and the `<paths>` both refuse to this worker.
- **`org/modules/graph/potion/MANIFEST.json` was NOT edited**, although it is granted: shape (i) makes
  it correct as it stands. An edit inside a grant the work does not need is still an edit.
- **`potion_embed.py` was NOT touched** -- out of grant, and the order names it as the verifier this
  cell must not change.
- **`cep4_before.json` was NOT re-captured** and `deliverables/0.9.0_WK_NFRA_COMPEFFICACY~1/` was READ
  and never written -- out of grant. That is why arm (e) is a row rather than a repair.
- **The `<status>` was NOT flipped to `complete`** -- E1-AC1 FAILS by output.
- **Nothing was pushed, merged or rebased.** The issuer drains the branch.
- **No comp-tool was invoked by bare PATH name** in any measurement.
