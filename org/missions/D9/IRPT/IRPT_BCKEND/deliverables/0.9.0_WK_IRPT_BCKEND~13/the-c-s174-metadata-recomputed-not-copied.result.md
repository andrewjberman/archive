# IRPT_BCKEND.TO-IB-rto-1 -- C-S174 metadata, properly corrected: recompute, never copy

`0.9.0_WK_IRPT_BCKEND~13`, round 15, cell `IB-rto-1`.

## Source of this cell

`1.0.0_SA_CTO`'s round-14 analysis (`@0782226170`), row `C-S196`: this chain's own round-13/14
`C-S174` metadata correction (arms `IB-rtm-1`(f) / `IB-rtn-1`) itself carried two further faults --
a transposed CRLF hash value and a misattributed LF/git-object hash. This cell is metadata-only:
no code change to `capture-session.cjs`/`.sh`, no README change, no new packet, no S3 act, no
never-widen sign-off.

## Arm (a) -- recompute, never copy

Identified the commit the `C-S174` citation is about by reading the existing text first (the
`IB-rtk-1` proof instance's `controls.mutant.observed` field names the fourth-pass repair whose
`capture-session.cjs` bytes the citation describes): commit `0d0c8cdc4d` (blob
`ded605028b2210b589735927868aacf92ceb852d`) -- NOT `HEAD` (`HEAD`'s blob has since moved on to
`17aff45ed837a3a6e62fb2ce0410075b62a499dd`, a later pass).

Recomputed both values fresh from that exact commit's blob, from the actual bytes, three
independent instruments agreeing:

- **LF/git-object sha256** (`git cat-file -p 0d0c8cdc4d:infra/aws/ec2/investor-reporting-export/capture-session.cjs | sha256sum`,
  cross-checked via `git show 0d0c8cdc4d:infra/aws/ec2/investor-reporting-export/capture-session.cjs | sha256sum`,
  agreeing byte-for-byte):
  `f03666ef827e7c6a169214c83b2a4fe593d7f1cbf181f728f1febb0235eacd0d` -- already correct everywhere
  this chain's own metadata cited it; unchanged.

- **CRLF/checkout-grain sha256**: an ACTUAL raw working-tree read on this box, not a simulation --
  `git read-tree 0d0c8cdc4d` + `git checkout-index -- infra/aws/ec2/investor-reporting-export/capture-session.cjs`
  into a throwaway scratch work-tree via a redirected `GIT_WORK_TREE`/`GIT_INDEX_FILE` (this
  repo's own index and working tree never touched), applying this box's real `core.autocrlf=true`
  filter on an actual checkout, then `sha256sum` on the materialized file:
  `fffef738e90cf03bfb20cdfbeb8cbb310e3a44c6eee657974f8a3eeb92e8e35b`.

  Independently corroborated by a THIRD instrument: this chain's own
  `IB-rtk-1_repaired_r10_lifecycle_diagnostic.json` artifact (captured during round 12, long
  before this cell existed) already recorded this exact same value in its own `sourceSha256`
  field -- the diagnostic's default worktree-source-mode read, at the time, independently landed
  on the same bytes.

  A lighter-weight validation of the read-tree/checkout-index instrument itself: applying the
  identical LF-blob-to-checkout-bytes transformation to the CURRENT `HEAD` blob and comparing
  against an actual `open(...).read()` of the live working-tree file reproduces the live file
  byte-for-byte (sanity check on the mechanism, not part of the cited evidence chain).

The wrong (transposed) value this chain's own earlier fix had written differs from the true value
by two adjacent hex characters swapped in position, mid-string.

## Arm (b) -- corrected the transposed CRLF value

Enumerated every occurrence of the wrong substring across this worker's own deliverables
directory (Grep tool, per the order's own instrument discipline) -- **3 files**:

1. `IRPT_BCKEND.TO-IB-rtk-1...proof_of_spec.json`, `controls.mutant.observed` field (two
   occurrences within the same field).
2. `battery_ib_rtm_1.py`'s module-level `CRLF_VALUE` constant.
3. `the-capture-tool-typed-error-classification-and-truthful-cleanup-report.result.md`, arm (f)
   prose.

All three corrected to the freshly-recomputed value from arm (a). Verified zero residual
occurrences via the battery's own new enumerated scan (arm (d) below): 86-87 files scanned
(varies by run depending on whether a fresh `__pycache__`/output file exists at scan time), 0
hits, denominator printed every run.

## Arm (c) -- corrected the misattributed LF hash

The `IB-rtk-1` proof instance's `controls.mutant.observed` field previously read: `"Repaired
worktree source: reproduced=false, sourceSha256 f03666ef... (the diagnostic's own computed value
on the repaired bytes, and the git-object sha256 -- the git BLOB's own LF bytes)"` -- this was
wrong on two counts: (1) it did not match what that round's own diagnostic artifact
(`IB-rtk-1_repaired_r10_lifecycle_diagnostic.json`) had actually recorded in its `sourceSha256`
field (the CRLF value, not `f03666ef...`); and (2) it credited a worktree-mode diagnostic read
("Repaired worktree source", the diagnostic's DEFAULT mode) with producing the git-object/LF
value -- backwards, per row `W13-S3`'s own finding: a raw worktree read on this CRLF-checkout box
produces the CRLF value, never the LF value.

Corrected: the field now names the freshly-recomputed CRLF value as the worktree-mode diagnostic's
own computed value, and names `git cat-file -p` / `git show` as the LF/git-object value's actual
source.

## Arm (d) -- run-time recomputation control

`battery_ib_rtm_1.py`'s `--arm metadata` widened with a genuine run-time recomputation control:
`recompute_lf_value()` and `recompute_crlf_value()` independently re-derive BOTH values from
`capture-session.cjs`'s actual bytes at commit `0d0c8cdc4d`, fresh, on EVERY run -- never a
hardcoded constant copied from the proof (the prior `CRLF_VALUE`/`BLOB_VALUE` module constants,
themselves copies carrying the same transposition undetected for two rounds, are removed). The
proof text's substring-presence checks now compare against THIS run's fresh recomputation, not a
stored constant. Also added: an enumerated zero-residual-substring scan across the worker's own
deliverables directory (denominator printed every run) and an attribution-language check (absence
of the specific wrong phrasing; presence of `git cat-file`/`git show` as the named LF-value
source).

## Arm (e) -- verification

`battery_ib_rtm_1.py --arm metadata`, rc=0, both success tokens print
(`IBR113-METADATA-C174-C187-CORRECTED`, the pre-existing token, and the new
`IBR115-C174-RECOMPUTED-NO-TRANSPOSITION-NO-MISATTRIBUTION`), every check `[ok]`. Output committed
as `IB-rto-1_R115-AC1_final_output.txt`. The run-time recomputation control is genuinely
exercised: the freshly-recomputed values and the exact `git` commands used are printed every run
(not merely "stored values look right").

`proof-of-spec-check.py` re-run on every proof instance this cell touched:

- `IB-rtk-1`'s proof instance (the field this cell directly edited): `VALID (rc=0)`.
- `IB-rtm-1`'s proof instance (the criterion this order names, R115-AC2): `VALID (rc=0)`, output
  committed as `IB-rto-1_R115-AC2_final_output.txt`. No criterion verdict changed in either
  instance -- this cell corrects HOW a fact was described, never WHAT was found.

## Arm (f) -- no publish replay, no code change

`capture-session.cjs`, `capture-session.sh` and `README.md` are untouched (verified: `git status`
against this worktree's `HEAD` shows only the three metadata/battery files modified). No new
never-widen packet. No S3 action. No host start/stop, no live login, no credential, no MFA
automation, no network call to the portal.

## Pre-existing, out-of-scope observation

`battery_ib_rtm_1.py --arm classify` (R113-AC1, an UNRELATED criterion this cell does not touch
or re-grade) exits rc=1 on an R11 partial-verdict regression, unchanged from `HEAD` before this
cell's commit (confirmed by running the unmodified original file side-by-side, byte-identical
result). This is a pre-existing condition from a prior round's own classify-arm state, already
described (if imprecisely) in the module's own docstring NOTE, and is out of this cell's BOUNDS
(only `--arm metadata` is exercised by this order's criteria; R114-AC3's own PASS grade, already
established by `3.0.0_SA_CVO~B`'s independently re-run instruments, is not reopened or moved by
this cell per its own STATE COHERENCE postulate). Not filed as a surprise row: it is neither a
failed premise of THIS cell nor a capability this cell needed; it is simply visible in the same
file this cell also touches, unrelated to the metadata fix.

## Criteria

- `R115-AC1`: PASS -- `battery_ib_rtm_1.py --arm metadata` rc=0, prints both freshly-recomputed
  values with exact derivation commands, confirms zero residual wrong-substring occurrences
  (denominator printed), confirms corrected LF/git-object attribution, demonstrates the
  recomputation control genuinely re-derives and compares at run time.
- `R115-AC2`: PASS -- `IB-rtm-1`'s proof instance re-validates `VALID (rc=0)` after this cell's
  metadata corrections; no criterion verdict changed.
