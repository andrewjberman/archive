# RESULT -- IRPT_BCKEND.TO-IB-rtf-13 (the directory-search zip carries its contract, first pass)

Worker `0.9.0_WK_IRPT_BCKEND~1`. Full verbatim run: `IB-rtf-13_R70-AC1_battery_output.txt` (this
commit). Summary below; every count is re-derived by the battery on each run, never carried by
hand. **THIS IS THE FIRST PASS: arms (a)-(c) only, no apply.**

## Arm (a) -- the runtime-open census that ends the class (attempted)

47 runtime-open sites censused across the 7 serving functions' packaged Python members (frontier
+ domain files, counted PER FUNCTION they are packaged into -- a shared frontier site staged into
N functions counts N times, once per function's own resolution; tests/ and fixture-generator
scripts excluded, per their own source-map notes that they are never shipped), each classification
MECHANICALLY cross-checked against the current `lambda-source-map.json`, the committed
`irpt-common` layer `BUILD_MANIFEST.json`, and each function's own `lambda.tf`
`environment_variables` block (never a hand-typed verdict trusted alone). **All 47 classifications
confirmed clean this run (`0` MISCLASSIFIED-CHECK-FAILED).** Denominators per function (STAGED /
ENV-RESOLVED-TO-LAYER / MISSING, n = the row's own total):

| function | STAGED | ENV-RESOLVED-TO-LAYER | MISSING | n |
|---|---|---|---|---|
| irpt-directory-search | 5 | 0 | 1 | 6 |
| irpt-performance-adapter | 4 | 3 | 1 | 8 |
| irpt-narrative | 5 | 2 | 1 | 8 |
| irpt-intake-poller | 3 | 0 | 0 | 3 |
| irpt-export-render | 2 | 4 | 3 | 9 |
| irpt-holdings | 3 | 2 | 1 | 6 |
| irpt-status | 4 | 0 | 3 | 7 |

Total: 47 of 47 sites classified, 10 MISSING. Plus one site excluded from the three-way count
(`_keys/keys.py:verify_against_layout`, no static target -- row `S36`).

`irpt-ycharts-generate` is BARRED (row S102, recorded not fixed) and carries no row from this
census. `irpt-directory-refresh` is not one of the 7 serving functions (a schedule target).

**Note on sequencing:** this battery's arm (a) reads the CURRENT manifest, and arm (b)'s edit
(below) was made before the battery's first run, so `directory/entry.py:74-83`'s
`DirectoryEntry.schema.json` site classifies **STAGED** in the table above, not MISSING -- it is
row `S103`, POST-FIX, confirmed resolved rather than re-discovered as still open. The **10 MISSING**
counted are ALL NEW findings (none is S103); three of them are further instances of its own class,
filed this pass because the wider census this order asked for surfaced them and they are not the
ycharts exception:

  * **`IRPT_BCKEND-W1-S34`** -- `_scope/resolve.py`'s `_server_only_properties()` (staged flat
    into 5 of the 7 functions) and its identical construct in `holdings/resolve.py` (own tracked
    copy) resolve `ResolvedScope.schema.json` at a checkout-only path with NO env override and no
    layer copy -- MISSING on **6 of 7** functions (every one but intake). Degrades UNSAFELY
    (`except (OSError, ValueError): return []`, i.e. fewer fields stripped, not more). The same
    construct-shape recurs in `ops/status.py` (`StatusEnvelope.schema.json`, degrades SAFELY) and
    `ops/manifests.py` (`PATH_MANIFEST.json`, reachability from the live route not confirmed this
    pass) -- the S96/S98/S103 class, a fourth/fifth/sixth time, OUTSIDE this order's `<paths>`.
  * **`IRPT_BCKEND-W1-S35`** -- `export/package.py`'s `candidate_checkouts()` hardcodes Andrew's
    own device-specific absolute paths as fallback candidates; on the deployed `irpt-export-render`
    zip every candidate is absent and `package.locate()` unconditionally raises. Also a live
    instance of CLAUDE.md's device-specific-logic hazard (LD-0405: "surface, don't chase").
  * **`IRPT_BCKEND-W1-S36`** -- `_keys/keys.py:verify_against_layout()` is a runtime-open call
    site present in every packaged copy of `keys.py` (flat or via the `irpt-common` layer) with NO
    static target (a caller-supplied path) and 0 call sites anywhere in the shipped or test tree
    this census's Grep sweep found. Recorded so the "35 sites" denominator is explained, not a
    defect.

None of the three new rows is fixed by this order (BOUNDS restrict the deploy to
`irpt-directory-search` and forbid a `_scope/`/`_ids/`/`directory/` source edit); they are filed
and left for the issuer's disposition, per row text.

## Arm (b) -- the member and the env

`infra/aws/lambda/ci/lambda-source-map.json`'s `irpt-directory-search` entry gains ONE
`staged_from` object (`docs/contracts/investor-reporting/v1/DirectoryEntry.schema.json`, pin
`6e764ef0aa48a01f922931d66413477a2eff05a4`, `packaged_as: contracts/DirectoryEntry.schema.json`,
sha256 `7ed220ff87a787c6b596bcc66bc90a8a5a69fe2ec7da88e145207297011aab24` -- re-derived this run via
`git show <pin>:<path> | sha256`, matches the declared value) and the matching `files[]` entry.
`infra/aws/terraform/investor-reporting/directory/lambda.tf` gains ONE environment line,
`IRPT_CONTRACTS_DIR = "/var/task/contracts"`, the same value class the other four
`IRPT_CONTRACTS_DIR`-carrying roots use (pointed at this root's OWN zip, since this function
attaches no layer), citing `holdings/lambda.tf:85`'s precedent. **Structural parse-diff** (parsed
JSON, HEAD vs current, not a raw line-diff -- a raw diff shows a trailing-comma line touched by the
array insertion that carries no semantic change): exactly one function changed
(`irpt-directory-search`), exactly one `files[]` addition, exactly one `staged_from` addition, zero
removals, zero other scalar fields hand-touched. `artifact_sha256` is untouched BY THIS EDIT (S89)
-- it later moves when the BUILD (arm c) legitimately writes it; that is the build's own field,
not this arm's.

## Arm (c) -- the packet

`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-13.md` committed (this commit), `blob` printed in the WORKER
REPORT. **K-CODE**: `irpt-directory-search` rebuilt via `build-and-upload.sh investor-reporting
irpt-directory-search` from worktree HEAD `19ccf82226` (at/after the manifest commit). Prior LIVE
`CodeSha256` read live before the build: `PUjH3OjDe8Yj3RwdIO0KT3GXsYGfvUCmzG/aHsi6e1c=` (matches
the face's own citation verbatim). Build-store rollback source: S3 object version
`elK9Z3qtolvKrVJhSuMrmlFJZT.77_Dk` (read before the build ran). Built `artifact_sha256`:
`76LeVyYNfhdyDnQNXR3LzrqSv7k7Vr3POSjpcBzww6E=`. **VERIFIED AT REST**: the downloaded zip's own
sha256 matches the declared value; 13 of 13 members byte-equal to their declared blob (pinned
commit, or HEAD for a directly-tracked member) -- never the working file. Served-byte delta vs the
prior 12-member set: exactly `['contracts/DirectoryEntry.schema.json']` (`m=1` of 1). **K-ENV**:
`IRPT_CONTRACTS_DIR` on the directory root. **Terraform plan, directory root** (vendored binary,
`0 to destroy`): `Plan: 0 to add, 1 to change, 0 to destroy` on `irpt_directory_search`
(`before.source_code_hash` == the prior live value, `after.source_code_hash` == the built value);
the SAME root's `irpt_directory_refresh` resource plans `no-op` (untouched). **The other six roots
re-taken**: `export`/`holdings`/`intake`/`narrative`/`ops`/`performance` each read `No changes.`

**THE HALVES, READ AT HEAD:** `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` and
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` carry NO file naming `rtf-13` -- **0 of 2 halves
present.** Per this order's own text, this is the EXPECTED first-pass outcome (the halves cannot
exist before the packet does). **STOP HERE**: arm (d) does not run this pass. `R70-AC1` FAILS
TRUTHFULLY at (c) in a VALID instance. The order stays open, pending the issuer's and the CTO's
sign-off against this packet's `blob <hash>`.

## R70-AC2 (judgment, for the CVO)

Stated in the proof-of-spec instance, not graded here. In short: the build-time check that would
make every runtime open a staging member BY CONSTRUCTION belongs in `build-and-upload.sh`'s
existing `ADHC_DRIFTD.002` parity gate, generalised from "every `.py` on disk is declared" to
"every module-level path-join/env-candidate this census's pattern set finds resolves to a
declared `files[]`/`staged_from` member or a named layer member, or the build refuses" -- keyed on
the OPENS (this census's own method), never a filename list, because a filename list is exactly
what let `entry.py`'s `_CONTRACT`/`IRPT_CONTRACTS_DIR` pair (and now `resolve.py`'s
`ResolvedScope.schema.json`) ship for months with a perfectly clean file-presence parity check.
Three passes (S96, S98/S99, S103) were needed because each pass's own `<paths>` grant bounded its
census to ONE function or ONE module family; this pass's wider census (7 functions, both frontier
and domain files) is the first to surface the SAME construct recurring in 6 of 7 functions at
once (row S34) -- suggesting the remedy belongs in the shared BUILDER, not a per-cell manifest
patch, or the pattern will need a fourth, fifth and sixth pass to reach the functions this one's
`<paths>` did not.
