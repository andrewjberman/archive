# IB-rte-4 RESULT -- the served Lambda members declared from their true sources

**Cell:** `IB-rte-4` (decomposition v0.5 s.R5). **Order:**
`IRPT_BCKEND.TO-IB-rte-4.the-served-lambda-members-declared-from-their-true-sources.md`.
**Worker:** `0.9.0_WK_IRPT_BCKEND~4`. Remedy commit: `2796e3ffe3c062be7e7a9d934ec7fb21dd577df9`
(LOCAL, branch `wk-irpt_bckend-5-4`). Battery: `battery_ib_rte_4.py`; output:
`IB-rte-4_R54-AC1_battery_output.txt`.

---

## (a) THE CENSUS -- 9 of 9 investor-reporting functions, 147 declared+served members

Population (`N of N`): the SAME filter `build-and-upload.sh`'s own `TMPJS_LIST` applies
(`tf_file` contains `investor-reporting`, `package_type != Image`, `build_type != nodejs`) --
`irpt-directory-refresh`, `irpt-directory-search`, `irpt-export-render`, `irpt-holdings`,
`irpt-intake-poller`, `irpt-narrative`, `irpt-performance-adapter`, `irpt-status`,
`irpt-ycharts-generate`. Every function's `files[]` set equals its SERVED zip's member set
(9 of 9, `SET-MATCH=True`) -- the served zip really does carry every declared member and nothing
undeclared.

| function | members | TRACKED-AT-PATH | TRACKED-ELSEWHERE (staged, hash-verified) | CONTENT-DIFFERS (CRLF artifact, row S38) | UNRESOLVED (rows S34/S35) |
|---|---|---|---|---|---|
| irpt-directory-refresh | 5 | 3 | 2 | 0 | 0 |
| irpt-directory-search | 9 | 2 | 7 | 0 | 0 |
| irpt-export-render | 17 | 11 | 6 | 0 | 0 |
| irpt-holdings | 12 | 7 | 2 | 3 | 0 |
| irpt-intake-poller | 28 | 4 | 3 | 20 | 1 |
| irpt-narrative | 15 | 5 | 5 | 5 | 0 |
| irpt-performance-adapter | 19 | 8 | 5 | 6 | 0 |
| irpt-status | 12 | 3 | 9 | 0 | 0 |
| irpt-ycharts-generate | 30 | 4 | 9 | 15 | 2 |
| **TOTAL (147 of 147)** | 147 | **47** | **48** | **49** | **3** |

**Yes, this is the same instance of the `memory/feedback_structural_over_cultural_pattern.md`
item-6 class the round-4 analysis and rows W1-S20/W2-S59 already named** -- generalised far wider
than the four originally-named members: **48 of 147** declared+served members across **7 of the
9** functions are undeclared copies with no vintage at their own `source_dir`, resolving cleanly to
one of the estate's existing shared frontiers (`_authz/`, `_scope/`, `_keys/`, `_ids/`, `_gate/`,
`directory/handler.py`, `intake/checkpoint.py`, `lib/trading_calendar.py`, the terraform-core
`firm_destination_policy.json`). The `memory/` file itself could not be read from this worktree
(row `IRPT_BCKEND-W4-S36`, INERT) -- this census answers the same question directly rather than
relying on its characterization.

**3 of 147 members (2 distinct: `firm_registry.json` on `irpt-intake-poller` +
`irpt-ycharts-generate`, `settings.json` on `irpt-ycharts-generate`) could NOT be resolved at
all** -- a content-addressed search of the ENTIRE git object graph (`git hash-object --no-filters`
then `git cat-file -e` / `git rev-list --objects --all` on the resulting blob id, not a path
guess) found these exact served bytes committed nowhere, ever. Rows `IRPT_BCKEND-W4-S34`/`W4-S35`
(ARMED). No content is invented to close them; `irpt-intake-poller` and `irpt-ycharts-generate`
still fail to build with the real, unmodified manifest on these two members alone.

**49 of 147 members read `TRACKED-AT-PATH-CONTENT-DIFFERS`** -- every one inspected is a JSON
fixture or manifest, already correctly tracked at its declared path with a known vintage. This is
an INSTRUMENT ARTIFACT, not a provenance gap: `core.autocrlf=true` on this box checks out every
non-`.tf/.hcl/.sh/.py`-declared text file CRLF while its committed git blob is LF (measured,
`.gitattributes`' `text eol=lf` domain does not cover `*.json`), so a filter-free `git cat-file -p`
blob read and a raw-worktree-bytes zip member differ by exactly their CRLF count. Row
`IRPT_BCKEND-W4-S38` (ARMED, estate-wide, pre-existing -- not this order's to fix).

## (b) THE REMEDY -- `staged_from`, generalising `holdings/stage.py`'s own pattern into the builder

The CTO's ruling (round-4 analysis s.4 @`561d6e1cc9`): declare the true source in `files[]` (an
out-of-dir source staged at build time) or stage from a pinned blob -- never a third copy.
`infra/aws/lambda/investor-reporting/holdings/stage.py` already does exactly the second form for
`enforce.py`/`errors.py`/`resolve.py`/`handler.py`, committing its output with a pin+sha256
recorded in `STAGE_MANIFEST.json`. Widening `stage.py`'s own `MEMBERS` tuple (or writing an
equivalent script per function directory) would touch
`infra/aws/lambda/investor-reporting/**`, outside this order's BOUNDS ("the ONLY code paths
touched are `infra/aws/lambda/ci/`... and, if content differs, that function's deploy"). So the
SAME pattern is generalised into the ONE shared builder instead:

- `infra/aws/lambda/ci/lambda-source-map.json` gains a per-function `staged_from` array:
  `{repo_path, pin, packaged_as, sha256}` -- **9 of 9 functions** now carry one (`irpt-holdings` 2
  entries, `irpt-directory-refresh` 2, `irpt-directory-search` 7, `irpt-narrative` 5,
  `irpt-performance-adapter` 5, `irpt-intake-poller` 3, `irpt-ycharts-generate` 9,
  `irpt-export-render` 6, `irpt-status` 9 -- **48 total**, `2796e3ffe3`) -- exactly the census's
  own TRACKED-ELSEWHERE count in part (a) above.
- `infra/aws/lambda/ci/build-and-upload.sh` gains `TMPJS_STAGE` (`:160-201` @`2796e3ffe3`):
  materializes each declared member from `git show <pin>:<repo_path>`, verifies the blob's sha256
  against the DECLARED one, and writes it into `ABS_SOURCE` -- refusing loudly on a hash mismatch
  rather than shipping unverified or silently-drifted content. `STAGED_ABS_SOURCE`/`STAGED_NAMES`
  plus `cleanup_staged()` (`:226-238`) guarantee nothing staged from a pinned blob survives the
  script under any exit path -- called at the top of every loop iteration and from the existing
  `EXIT` trap. **No file under `infra/aws/lambda/investor-reporting/**` is ever written by this
  script; nothing is committed at the packaged path.**
- Row `IRPT_BCKEND-W2-S58` (the shared-`source_dir` parity false-flag) is fixed by the SAME
  builder change: `TMPJS_UNION` (`:210-224`) computes the union of `.py` basenames declared across
  every function sharing a `source_dir`, and `ADHC_DRIFTD.002`'s parity check (`:349-352`) is
  rescoped to that union instead of the current function's own `files[]` alone. `entry.py`
  (`irpt-directory-search`'s own member) no longer false-flags while `irpt-directory-refresh`
  builds from the same `directory/`, verified this run (see (b) real build below -- 0 parity
  failures on either sibling, `BAU_PARITY_SKIP` never set).
- `BAU_SOURCE_MAP_OVERRIDE` (`:50`) lets a scratch mutant manifest be tested without ever touching
  the real file -- used only by this order's own control battery, part (d).

**Real build, whole pipeline, `BAU_PARITY_SKIP` never set** (`IB-rte-4_R54-AC1_battery_output.txt`
part (b)): **7 of 9 functions build clean and upload byte-verified content** --
`irpt-performance-adapter`, `irpt-directory-search`, `irpt-narrative`, `irpt-directory-refresh`,
`irpt-export-render`, `irpt-holdings`, `irpt-status`. **2 of 9 still fail**
(`irpt-intake-poller`, `irpt-ycharts-generate`), and ONLY on the two unresolved members named in
(a) -- every other declared member on both functions stages and verifies cleanly.

Before this fix, the SAME real build (baseline, this worker's first act on this cell) failed
**0 of 9** -- every function refused with `File not found` on at least one member, confirming the
gap was not confined to the two functions rows W1-S20/W2-S59 had already named.

## (c) VERIFIED, NOT INFERRED -- clean checkout (builder determinism) AND live-code comparison (deploy need)

TWO DIFFERENT questions, TWO DIFFERENT instruments, deliberately not conflated:

**Is the builder deterministic?** A fresh `git worktree add --detach` of this branch's own tip
(post-remedy commit `2796e3ffe3`), the real `build-and-upload.sh` run there (not this worker's own
working tree), `BAU_PARITY_SKIP` unset: **7 of 9 functions build in the clean checkout**
(`irpt-intake-poller`/`irpt-ycharts-generate` fail there too, identically, since the gap is in the
committed manifest, not this worktree's state). **7 of 7 clean-checkout-built functions are
member-for-member identical, by sha256, to THIS worktree's own build of the same function** -- the
builder itself is reproducible.

**Does any function genuinely need a deploy?** The FIRST version of this check compared the
OVERALL zip sha256 against `live CodeSha256` and read `irpt-directory-search` and
`irpt-export-render` as content-differing. **That check was WRONG, caught before being reported**:
a zip's CONTAINER is not guaranteed byte-reproducible across different builders even when every
member inside it is byte-identical, and the currently-live zips for these two functions were built
by an earlier worker's manual workaround, not this builder. The CORRECT check -- per-member sha256
against the LIVE DEPLOYED Lambda's own code (`aws lambda get-function --query Code.Location`, a
presigned URL to the EXACT bytes `CodeSha256` was computed over, never the S3 build-artifact bucket
this order's own reruns have overwritten) -- finds **0 of 7 functions have ANY member differing
from what is already live**: every declared member's content, for every function this remedy could
build, is byte-identical to what advisors are served today. `0` deploys are needed; none is
performed.

## (d) THE CONTROL -- mutant fails exactly as recorded; real manifest succeeds

Scratch-only mutant manifest (`BAU_SOURCE_MAP_OVERRIDE`, the real file never touched): the four
ORIGINALLY-named declarations removed (`irpt-holdings` served.py/loaders.py,
`irpt-directory-refresh` errors.py/trading_calendar.py). Both mutant builds **FAIL with the exact
`File not found` lines rows W1-S20/W2-S59 recorded**; both real-manifest builds **SUCCEED**, `0`
manual staging steps.

(This control's first run FAILED to fire correctly -- a bash env-var-scoping bug in the
battery itself, `VAR=x unset OTHER; cmd` binding the assignment to `unset`, not `cmd` -- caught by
this same battery's own re-run before being reported; the fix and the corrected run are both in
`battery_ib_rte_4.py`'s own history and the committed battery output.)

## SUMMARY

7 of 9 functions: declared, staged, verified, byte-identical clean-checkout build, `0` deploys
needed. 2 of 9 functions (`irpt-intake-poller`, `irpt-ycharts-generate`): blocked on 2 members
(`firm_registry.json`, `settings.json`) with NO recoverable true source anywhere in this
repository's history -- filed, not fabricated (rows `IRPT_BCKEND-W4-S34`/`S35`). Because of this,
**the battery's success token is WITHHELD** and `R54-AC1` is **NOT** a full PASS-by-output on the
literal "every arm holds" bar; see the proof-of-spec instance and this order's final report for the
exact denominator.
