# IB-rte-6 RESULT -- THE SERVED PATH ADMITS A PROJECTED ADVISOR GRANT

**TO:** `IRPT_BCKEND.TO-IB-rte-6` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:**
`wk-irpt_bckend-5-1b` | **base commit:** `f9e7f2849c` (HEAD of `CLOUD` at hand-off).

**Invocation:** `timeout 1800 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rte_6.py`
**Result:** `rc=1`. Transcript: `IB-rte-6_R56-AC1_battery_output.txt`.
**R56-AC1 = FAIL (arm d).** Arms (a), (b), (c) PASS; arm (d) does not, and the token
`IBR56-SERVED-PATH-ADMITS-PROJECTED-GRANT` never prints. **The order stays `pending`**, per its
own proof-of-spec contract: a FAIL row leaves the order open.

---

## What was built

**(a) THE WIRING.** `_authz/served.py`'s `Entry.id_projection` is now a FACTORY
(`firm_id -> ((kind, raw) -> id)`), called from `enforcer_for(tenant)` with the VERIFIED tenant
(never a request-controlled token). All 7 `entry.py` files that construct `_entry.Entry` now pass
`id_projection=_ids.projection_for_firm`. Census over the same 13-file population IB-rte-1
measured (every `entry.py`/`handler.py`/`dispatch.py` under `infra/aws/lambda/investor-reporting/`):
**13 of 13 wired** by an AST check (not a substring search) that verifies every real
`Entry`/`Enforcer` construction in a file carries a non-`None` `id_projection` keyword; a file
with no construction (`handler.py`/`dispatch.py`, which never build an `Entry`) is vacuously
compliant. **Mutant test**: stripping `id_projection` from `directory/entry.py`'s construction (in
memory, never on disk) makes the census fail immediately -- the discriminator the criterion asks
for.

**(b) THE PROJECTION FOR 49 FINANCIAL, MEASURED.** REC (a) as literally named in the task order
(join custodian keys through `dim_identity_crosswalk`) was built and measured FIRST: it resolves
**0 of 22,646** live ownership-map account slots (0 of 43 for abby_horton), because
`dim_identity_crosswalk` (SmartX GUIDs + Schwab digits, measured live) shares no column with the
ownership map's raw keys (Black Diamond "z"+10-digit ids, measured live) -- a divergence the
ownership-map PRODUCER's own docstring declares
(`data/assets/scripts/gold/runners_49f/d08_firm_ownership_map.py:13-19`). Filed
`IRPT_BCKEND-W1-S25`.

Per the face's own alternative ("or through the projection's existing read path -- name which,
cite `file:line@commit`"), this cell built the shipped projection from
`blackdiamond/49f/silver/dim_account_xref` instead -- the SAME reconciliation table
`data/assets/scripts/gold/investor_reporting/directory_runner.py:326-332 @de4e176cc3` already
reads on the host session (no new grant), which carries `bd_account_id` (the ownership map's own
key shape) mapped to `schwab_account_id` (the SAME target space `raw_keys.json` names). Bundled as
`infra/aws/lambda/investor-reporting/_ids/data/custodian_key_seam.json` (a DECLARED, dated
snapshot -- the serving lambdas' execution roles hold no grant on either gold-dimension bucket the
identity tables live in, per this order's own `comp-iam: DECLARED-NOT-APPLICABLE`). Measured:
**17,895 of 22,646** slots resolve (**21 of 43** for abby_horton). Which firm needs this seam is
DECLARED in `_ids/raw_keys.json`'s new `account.projection_seam` field, never a hand-typed firm
literal in `_ids.py` (the LGIC naming gate refused the first draft on exactly that; the dispatch
is now data-driven off the registry-declared field).

A raw key the seam cannot resolve is returned RAW, never minted from an unresolved custodian
key -- minting it would produce a well-shaped `acc_`+24hex id indistinguishable from a genuinely
issued one, which `_scope.unmatched_reasons` would then misclassify NOT-IN-DIRECTORY instead of
the true UNPROJECTED-ID (exactly the mislabelling `_scope/resolve.py`'s own history warns
against).

Inflection and cottonwood measured (R56-AC2, no fix): both firms' live ownership maps are EMPTY
at this cell's cut -- cottonwood's object exists with 0 advisors, inflection's object does not
exist at all (`loaders.load_ownership`'s own rule: absent == empty). `0 of 0` for both, VACUOUS.

**(c) DEPLOY.** `7 of 7` functions (`irpt-directory-search`, `irpt-export-render`,
`irpt-holdings`, `irpt-narrative`, `irpt-status`, `irpt-performance-adapter`,
`irpt-ycharts-generate`) rebuilt with `_ids.projection_for_firm`, the new seam data file, and (for
4 of 7 that did not already declare it) `ids.py` added to `lambda-source-map.json`'s `files[]`.
Packaged with a SHARED_ROOTS resolver adapted from the sibling `~2` slot's `rt6_package.py`
(`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/rte6_package_deploy.py`),
since `build-and-upload.sh`'s generic packer cannot resolve a file absent from a function's own
`source_dir`. Two MORE untracked-production-source-file gaps surfaced while packaging
(`irpt-status`'s `handler.py`/`checkpoint.py`; `irpt-ycharts-generate`'s `gate.py`/
`firm_destination_policy.json`/`firm_registry.json`/`settings.json`) -- extracted UNCHANGED from
the currently-deployed zips for the build only, never committed. Filed `IRPT_BCKEND-W1-S26`.
Every zip verified importable in a flat, fresh-interpreter layout (the `irpt-common` layer's
`/opt/python` added as a fallback for the 4 functions that attach it) before upload. Uploaded to
`s3://opal-313476888478-lambda-artifacts/investor-reporting/<function>.zip` with the
`content-sha256` metadata the `yang-lambda` module's data source reads; `terraform plan`/`apply`
run TARGETED at each function's own `aws_lambda_function.this` resource across the 7 separate
Terraform roots (`0 to add, 1 to change, 0 to destroy` each -- re-plan `No changes` after every
apply). Ledger `irpt-bckend-rte6-id-projection-wiring`, OPENED before any apply, CLOSED with all 8
legs proven (`org/critical_paths/change_management/20260919T0006Z_irpt-bckend-rte6-id-projection-wiring_deploy_completion.md`).
Served `CodeSha256` per function, verified against the built artifact, `7 of 7` MATCH:

| function | served == built CodeSha256 |
|---|---|
| irpt-directory-search | `v0MMA3yUxIPNdCMXhE/2pSD9lU+5LgI945JqkuULH8U=` |
| irpt-export-render | `WJ8Nk/Zr2g1/cafjnJvF1glFiMdPiFc7Bt8hktqsxuo=` |
| irpt-holdings | `R2+ff33uJO3jrCOuMII9y6SvEhvG43wfeXrGbn0pJGk=` |
| irpt-narrative | `XUJ68NaABwFNW9ItzMBO5l0Jvb2pG5t+ot833bkLY5g=` |
| irpt-status | `twhh/jwDdSwzQ6/BtFdkl52jXYuO19AfVviu/+FlD5A=` |
| irpt-performance-adapter | `xI2iPO5/5WTf2a6rqgdL6kXJZ3ODiDZI22pz51jGMuQ=` |
| irpt-ycharts-generate | `4TF3bfgPezMaZvx7tZdwJHOF6S7GyRq0ayI6s5ryV3s=` |

**(d) LIVE ROUTE -- FAILS.** The SAME real request IB-rte-1 measured (advisor `abby_horton` /
`49financial`), run against the deployed bytes with the real directory and ownership map through
the SAME construction `served.Entry.enforcer_for` now performs, still reads **code=UNPROJECTED_GRANT**,
`k=0` served. Cause: `_authz/enforce.py`'s own, UNEDITED refusal policy
(`resolve_now`, `if unprojected: return None, Refusal("UNPROJECTED_GRANT", ...)`) refuses the
**WHOLE** grant if **ANY** ownership id fails to project -- and it runs BEFORE the empty-permitted-set
check, so the 21 accounts that DID resolve never reach `permitted_account_set`. Abby Horton's
grant is 21 of 43 resolved (79% firm-wide); 22 remain genuinely unresolved. This is the estate's
own documented safety direction ("the viewer HAS a grant this system cannot see; refusing rather
than serving the empty result"), unedited by this order (bound: entry points + `_ids/` only) and
correct on its own terms -- it is simply incompatible with a 79%-complete bridge. The cross-firm
swap (a fabricated advisor id) is still correctly REFUSED (`EMPTY_GRANT`). The pre-fix bytes
negative control (the SAME construction with `id_projection` omitted, exactly as every entry point
built it before this order) reads `UNPROJECTED_GRANT` as expected. Filed `IRPT_BCKEND-W1-S27`,
BLOCKING, disarm owner `1.0.0_SA_CTO`.

**What would close arm (d):** either (i) the ownership-map PRODUCER re-keyed to the canonical
Schwab spine it already declares as its own eventual cutover (`d08_firm_ownership_map.py`'s "V8
class" divergence note) -- out of this order's bound ("no ownership-map write ... a producer
outside this project") -- or (ii) a CTO ruling on `enforce.py`'s all-or-nothing refusal policy
itself, which this order's bound also does not authorize touching. Both are named, neither is
this cell's to do.

## Rows filed

- `IRPT_BCKEND-W1-S25` (OBSERVATION, ARMED, disarm owner `1.0.0_SA_CTO`) -- REC (a) as literally
  named resolves 0%; this cell substituted the face's own alternative read path.
- `IRPT_BCKEND-W1-S26` (OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~B`) -- two more
  untracked-production-source-file gaps (`irpt-status`, `irpt-ycharts-generate`), same class as
  row W1-S20.
- `IRPT_BCKEND-W1-S27` (BLOCKING, ARMED, disarm owner `1.0.0_SA_CTO`) -- R56-AC1 arm (d) fails:
  the served path is still not reachable for abby_horton because of enforce.py's all-or-nothing
  policy at 79% seam coverage.

## Bounds observed

The ONLY code touched: `_authz/served.py` (the `id_projection` factory contract), the 7 `entry.py`
files (the `id_projection=` keyword), `_ids/ids.py` and `_ids/raw_keys.json` (the seam
declaration/dispatch), `_ids/data/custodian_key_seam.json` (new, bundled), and tests
(`_authz/tests/fixtures.py`'s id shapes, `_ids/tests/test_ids.py`). `_authz/enforce.py` was READ,
never edited (arm (d)'s cause lives there, out of bound). No ownership-map write, no directory
write, no IAM, no env change, no principal created. Every `.py` edit passed
`.tools/commit-gate.sh`; the LGIC naming gate (ENFORCE mode, live -- CLAUDE.md Rule 30 said "WARN
today" and the live gate refused on first attempt, a discrepancy noted here rather than filed
separately since it cost one restructure, not a defect worth its own row) drove the
data-declared-seam design rather than a hand-typed firm literal.
