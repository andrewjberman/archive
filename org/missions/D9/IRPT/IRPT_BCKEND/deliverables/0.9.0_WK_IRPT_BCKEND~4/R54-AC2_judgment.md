# R54-AC2 -- JUDGMENT, RECORDED AND NOT SELF-GRADED

For `3.0.0_SA_CVO`. No verdict is stated here. Every line citation carries `@<commit-ish>`; the
remedy commit is `2796e3ffe3c062be7e7a9d934ec7fb21dd577df9` on branch `wk-irpt_bckend-5-4`
(LOCAL -- not on `CLOUD` until this order's worktree drains).

## 1. Does the family have other undeclared-copy members beyond the four named on the face?

Yes -- the census (`the-served-members-declared.result.md` part (a), re-derived by
`battery_ib_rte_4.py` every run) found **48 declared+served members across all 7 of the family's
9 functions** carrying the same class as `IRPT_BCKEND-W1-S20`/`W2-S59` (declared in `files[]`,
genuinely served, but never tracked at the path the build reads): `served.py`, `loaders.py`,
`enforce.py`, `errors.py`, `resolve.py`, `keys.py`, `ids.py`, `gate.py`, `handler.py` (on
`irpt-status` only -- every other function that ships `handler.py` has its own tracked, committed
copy), `checkpoint.py` (on `irpt-status` only), `trading_calendar.py`, and
`firm_destination_policy.json`. Every one of those 48 resolved to a TRUE SOURCE that already
exists in the repository (`infra/aws/lambda/ci/lambda-source-map.json` `staged_from` per function
@`2796e3ffe3`) -- so the four named on the face were the ONLY ones the round-4 analysis and rows
W1-S20/W2-S59 had already found; the wider set was new to this cell's own census.

**Two members on two functions could NOT be resolved at all**, a DIFFERENT and WORSE case than
"undeclared copy": `firm_registry.json` (declared+served on `irpt-intake-poller` AND
`irpt-ycharts-generate`, byte-identical between the two) and `settings.json` (declared+served on
`irpt-ycharts-generate` only) have no true source anywhere in this repository's reachable git
object graph -- verified by content-addressed search (`git hash-object --no-filters` then
`git cat-file -e` / `git rev-list --objects --all` on the resulting blob id), not a path guess.
Rows `IRPT_BCKEND-W4-S34`/`W4-S35` (ARMED, `disarm_owner: 2.0.0_SA_COO~B`),
`org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md`. These two
functions build 7-of-9-clean everywhere else and fail ONLY on these two members; no content is
invented to close them.

## 2. Should `_authz/` (and `_scope/`, `_keys/`, `_ids/`, `_gate/`) be a shared package rather than copied into each function?

A shape question for L4, stated rather than decided here. The census shows the CURRENT shape is
already "one frontier, staged per function" (not "copied into each function" in the sense of a
hand-maintained duplicate) -- `infra/aws/lambda/investor-reporting/_authz/`, `_scope/`, `_keys/`,
`_ids/`, `_gate/` are each a SINGLE tracked definition, and every function's zip gets its member
flat-packaged at build time from that one definition, hash-verified
(`infra/aws/lambda/ci/build-and-upload.sh:160-201` @`2796e3ffe3`, the `TMPJS_STAGE` script). The
open shape question is narrower than "shared package vs copy": it is LAYER vs STAGED-FLAT-COPY.
`irpt-narrative` and `irpt-export-render` already attach the `irpt-common` LAYER for
`jsonschema`/the IRPT contract schemas (`lambda-source-map.json` functions entries, `"layers":
["irpt-common"]`), while `_authz`/`_scope`/`_keys`/`_ids`/`_gate` are staged flat into EVERY
function instead of riding that same layer. `holdings/stage.py`'s own header (`:17-21`
@`ebf5eae0c895a173a303b40b96139e363ff226c9`, cited already in row W1-S20) gives the reason a flat
copy exists at all -- "a zip is closed over its own directory" -- which is equally true of a layer
(`/opt/python` is available to every attached function without copying anything). Moving
`_authz`/`_scope`/`_keys`/`_ids`/`_gate` into `irpt-common` would remove **43 of the 48**
`staged_from` declarations (the remaining 5 -- `directory/handler.py` and `intake/checkpoint.py`
on `irpt-status`, `lib/trading_calendar.py` on `irpt-directory-refresh`, and
`firm_destination_policy.json` on `irpt-intake-poller` AND `irpt-ycharts-generate` -- are DIFFERENT
frontiers, not part of this specific shape question) and 9 functions' worth of duplicated bytes in
their zips, at the cost of coupling every one of those 9 functions to one layer's deploy cadence.
This order does not choose between them -- it only makes the CURRENT (staged-flat) shape provable
and correct.

## 3. Is the builder change the estate's to keep?

`infra/aws/lambda/ci/build-and-upload.sh` and `infra/aws/lambda/ci/lambda-source-map.json` are
**not this project's own files** -- the source map's own `_description` line
(`lambda-source-map.json:2` @`2796e3ffe3`) reads "Single source of truth for source-to-deployment
mapping" and the file carries **216 function entries across every zip-based Lambda pipeline in the
estate** (measured this turn, `python -c "... len(d['functions'])"` on the committed file), of
which 9 are `investor-reporting`'s. The builder script's own usage banner
(`build-and-upload.sh:12-14` @`2796e3ffe3`) lists pipelines by name (`yang-pipeline`,
`news-pipeline`, `bd-pipeline`, `smartx-pipeline`, `market-overview`, `causality`, `portfolio`) --
none of them IRPT_BCKEND's. The `staged_from` mechanism and the `BAU_PARITY_SKIP`
shared-`source_dir` union fix (row `IRPT_BCKEND-W2-S58`) are both GENERAL-PURPOSE: any OTHER
pipeline with the same class of gap (a declared member whose true source lives outside its own
`source_dir`, or two functions sharing one `source_dir`) now has the same remedy available without
a further code change, by adding its own `staged_from` array. **Owner: whichever seat/lane owns
`infra/aws/lambda/ci/` estate-wide** -- this order's `<paths>` grant admits `0.9.0_WK_IRPT_BCKEND~4`
to it ONLY for the duration of this non-terminal order (`<preflight>` lane clause, this face); the
STANDING owner is not named on this face and is not this worker's to assign. `1.0.0_SA_CTO` is the
seat that authored the round-4 analysis correcting the remedy to "declare the true source... not a
third copy" (`IRPT_BCKEND_ROUND4_ANALYSIS.md` s.4 @`561d6e1cc9`) and CLAUDE.md Rule 30 names the
CTO as the one who refuses an L4 PRD that types a hand-built address/name rather than a builder's
output -- by the same logic the CTO (or whoever the CTO delegates estate-wide CI ownership to) is
the natural standing owner of a shared builder script, but this is inference, not a citation of an
explicit ownership record, and is offered as such.

## 4. Numbers, re-derived this run (not carried from a prior run's output)

Per `battery_ib_rte_4.py`'s own re-derivation (part (a)/(b)/(c)/(d), each run against the live S3
artifact bucket, the LIVE DEPLOYED Lambda code (`Code.Location`, not the build-artifact bucket this
order's own reruns overwrite), and git's own object database): **7 of 9** functions build clean and
upload byte-verified content; those same 7 also match member-for-member from a fresh
`git worktree add --detach` of this branch's own tip (the builder is deterministic); **0 of 7**
have ANY member differing from what is already live today (**0 deploys needed** -- an EARLIER
version of this check compared the OVERALL zip sha256 and misread 2 functions as content-differing
before the per-member, live-code comparison corrected it, self-caught before being reported). **2
of 9** (`irpt-intake-poller`, `irpt-ycharts-generate`) remain blocked on the two unrecoverable
members named above. See `IB-rte-4_R54-AC1_battery_output.txt` for the verbatim run this cites.
