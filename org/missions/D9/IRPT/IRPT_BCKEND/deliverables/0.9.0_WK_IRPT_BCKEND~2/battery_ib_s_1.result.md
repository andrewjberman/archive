# IB-s-1 BATTERY RESULT -- `IRPT_BCKEND.TO-IB-s-1`

**Serial:** `0.9.0_WK_IRPT_BCKEND~2` (slot ~2, RESPAWN on the same order)
**Branch:** `wk-irpt_bckend-1-2` -- worktree `/c/tmp/wk-irpt-1-2`
**Run vintage:** battery re-run in full by THIS instance at 2026-09-10T23:37:21Z, source at
`d8b063c49f`; the world acts it grades were performed by the previous instance of this slot
under commits `3654197107` (source) and `4d3d2d10dd` (deploy + ledger CLOSED) and are
WORLD-DONE -- they are READ here, never re-executed (NEVER-2).

---

## WHAT THIS INSTANCE RE-GROUNDED, AND WITH WHICH INSTRUMENT

Nothing below is carried from the previous instance's report. Each row names the instrument
this instance ran.

| claim under test | this instance's instrument | result |
|---|---|---|
| the worktree carries the ordered paths | `git rev-parse --abbrev-ref HEAD`; `test -d org && test -d .tools` | `wk-irpt_bckend-1-2`; `TREE-OK` |
| the runner/handler behave as claimed | `python -m pytest` over both test files | `34 passed in 1.08s` |
| the whole acceptance battery | `timeout 600 python .../battery_ib_s_1.py` | rc=0, `6 of 6 arms PASS`, `IBS1-DIRECTORY-SERVED` |
| the Terraform root is converged | `.tools/terraform.exe ... plan -lock=false` | rc=0, `No changes. Your infrastructure matches the configuration.` |
| the QA objects exist in the firm buckets | `s3api head-object` x 3 (inside arm f) | 3 of 3 rc=0, ContentLength 275 / 273 / 273 |
| the served function carries the built bytes | `get-function-configuration` vs the ARTIFACT's own `content-sha256` metadata + a bogus-sha negative control | equal (`7OOoRBhYUc9t8pjV48MJR7erKIifjFFdOJu3zdH4enk=`); negative control False |
| the ledger is CLOSED, not merely reported closed | read of the committed entry + `deploy_ledger.py check` | `Status: CLOSED`, `legs CLOSED: 5 of 5`, committed at `4d3d2d10dd`, `lines naming irpt-bckend-s1: 0 of 7` |
| the identity-authority quotes in the runner's docstring are real | direct read of the three cited source files (a DIFFERENT instrument from the docstring that asserts them) | all three found at source: `runners_49f/a01_dim_relationship.py:3-4`, `runners_cot/a01_dim_relationship.py:4`, `runners_inf/a00_dim_account.py:8` |
| the masked discriminator does not carry a name | census of the 3 SERVED QA objects (6,371,481 + 450,726 + 417,709 bytes fetched from the firm buckets), not of the builder | 0 of 5062 discriminators non-conforming to `****dddd[ / TYPE]`; 36 distinct type tokens |

**Worktree state repaired, not discarded:** the previous instance left an `AD`-staged re-add of
`org/critical_paths/.open_deploys/irpt-bckend-s1.json` carrying `"status": "OPEN"`. The ledger
entry is CLOSED and `deploy_ledger.py close` DELETES the sentinel as the act of closing (row
`IRPT_BCKEND-W2-S6`), so committing that blob would have published a false OPEN deploy into the
estate-wide sweep. It was UNSTAGED (`git restore --staged`); no commit was touched.

---

## S1-AC1 -- ARMS (a)-(f), VERBATIM SUMMARY

```
  ARM (a) PASS: 3 of 3 firms built; 5062 of 5062 entries validate against DirectoryEntry.schema.json
  ARM (b) PASS: 5 of 5 fixture cases resolve to the expected authorized set
  ARM (c) PASS: 49F 6155 of 6155 unique accounts preserved across 201 groups; INF unmapped 0 of 874 (live, vacuous) + positive control 3 of 3; COT 835 unique accounts of 850 rows, fan-out declared
  ARM (d) PASS: 0 of 22 imports are vendor clients; 0 of 100 keystrokes raised on a stubbed network (stub verified live)
  ARM (e) PASS: A n B = 0 of 2/1 results; revoked -> 0 results, 0 accounts; A->B direct resolve refused
  ARM (f) PASS: 3 of 3 firm QA latest.json objects head-object rc=0 with a non-zero ContentLength; CodeSha256 == built artifact content-sha256 (7OOoRBhYUc9t8pjV48MJR7erKIifjFFdOJu3zdH4enk=); ledger CLOSED with 5 of 5 legs proven, committed 4d3d2d10dd, sentinel removed by the close, no BYPASS
  6 of 6 arms PASS
IBS1-DIRECTORY-SERVED
```

**(a) per firm, with the calendar's own trail** (denominator: 3 of 5 registry firms; the two
`kind` test/demo firms are excluded BY KIND, not by name):

```
  FIRM 49financial: bucket=opal-data-bd entries=4509 valid=4509 of 4509 as_of=2026-09-09 source_completion=2026-09-09 calendar_business_date=2026-09-09
    TRAIL: expected_last_trading_day(2026-09-10) = 2026-09-10 [calendar NYSE/pandas_market_calendars]
    TRAIL: 2026-09-10: source set INCOMPLETE -> prev_trading_day
    TRAIL: business date SELECTED 2026-09-09 (source set complete)
  FIRM inflection: bucket=opal-data-inf entries=293 valid=293 of 293 as_of=2026-09-10 source_completion=2026-09-10 calendar_business_date=2026-09-10
  FIRM cottonwood: bucket=opal-data-cot entries=260 valid=260 of 260 as_of=2026-09-09 source_completion=2026-09-09 calendar_business_date=2026-09-09
```

**(c)** `49F portfolio groups: 201 groups, 29907 membership rows, unique accounts BEFORE
grouping 6155 == AFTER grouping 6155`. The INF live unmapped population is EMPTY (0 of 874),
which is a VACUOUS pass and says so out loud; a constructed positive control grades the reason
machinery at 3 of 3 (row `IRPT_BCKEND-W2-S3`: the face names 79 unmapped, the live vintage
carries 0).

**(f)** is a read of a world the previous instance already changed. The comparison sits on TWO
DIFFERENT OBJECTS -- the SERVED function's `CodeSha256` against the STORED artifact's own
`content-sha256` metadata -- so neither side is the producer's self-report, and a bogus-sha
negative control proves the comparison can disagree.

---

## S1-AC2 -- THE ROOT IS CONVERGED

```
No changes. Your infrastructure matches the configuration.
```
rc=0, run AFTER the apply and AFTER the ledger closed, with `-lock=false` per the criterion's
own invocation. Four resources refreshed and none drifted: `aws_iam_role.irpt_directory`,
`aws_iam_role_policy.irpt_directory`, `module.irpt_directory_search.aws_lambda_function.this`,
`module.irpt_directory_search.aws_cloudwatch_log_group.lambda`.

---

## S1-AC3 -- THE JUDGMENT, RECORDED AND NOT SELF-GRADED

Addressed to `3.0.0_SA_CVO` at L9. No verdict is claimed here.

### 1. Which identity inputs were treated as AUTHORITATIVE, with the line read for each

AUTHORITATIVE = the custodian or the vendor STATES the fact and this runner carries it forward
unchanged. Every line below was re-read from source BY THIS INSTANCE, not taken from the
runner's own docstring:

- **49F relationship grouping** -- `data/assets/scripts/gold/runners_49f/a01_dim_relationship.py:3-4`:
  *"the CUSTODIAN-DELIVERED family grouping (fact_fam) SUPERSEDES this file's prior"* inferred
  union-find. Inference is retired exactly where the custodian states the fact, so
  `relationship_id` is carried, never re-derived.
- **49F account open/closed** -- `gold/advi/dimensions/dim_account` `account_is_open`,
  `closed_date`: the custodian's own state field, carried into `termination.indicator`.
- **INF in-universe predicate** -- `data/inf/scripts/gold/runners_inf/a00_dim_account.py:8`:
  *"an account is IN-UNIVERSE iff its rep_id appears in silver/api_dims/representatives"* on
  the same as-of frontier. The predicate is APPLIED from that module, not copied into this one.
- **INF household mapping** -- `runners_inf/a01_dim_relationship.py`'s MAPPED / SELF-FAMILY
  disposition, carried with its disposition token rather than collapsed to a boolean.
- **COT relationship grain** -- `data/cot/scripts/gold/runners_cot/a01_dim_relationship.py:4`:
  *"`Relationship ID` ships ON EVERY custody row (relationship-grain by construction)"*; `'0'`
  is the vendor's NO-RELATIONSHIP sentinel and is treated as absence, not as a group.

### 2. Which were treated as RECONCILIATION PRIOR ART -- carried as provenance, never as authority

- **49F `dim_account_xref`** `match_method` / `match_as_of` / `in_0833_universe`
  (`bd49f_dim_conversion.resolve_bridge`). A bridge row reconciles two custodial key spaces. It
  is emitted as a per-account provenance fact; `match_method='unresolved'` is reported IN BAND
  and never removes an account from the directory. **Note for the CVO:** the face attributes
  these three fields to `a06_dim_identity_crosswalk`; they live on `dim_account_xref`. Filed as
  row `IRPT_BCKEND-W2-S4`, worked to the fields' real home.
- **49F `dim_identity_crosswalk` (a06)** -- SmartX allocation ids. A crosswalk is a join aid.
- **49F `dim_portfolio_group` / `bridge_group_account`** -- the 201 groups OVERLAP by design.
  Membership is read for the overlap census (6155 == 6155) and NEVER for a scope.
- **Fuzzy name matching** (`build_schwab_bd_account_xref.py`) is **not used here at all**. A
  name never authorizes; `search` matches display text only to ORDER and DISAMBIGUATE
  candidates that the `ResolvedScope` has ALREADY admitted.

### 3. Can the masked discriminator leak a name?

**Not on any bytes this cell has produced, and the residual is structural rather than
theoretical.** `masked_discriminator()` (`directory_runner.py:130-140`) is built from two
inputs only: the account number reduced to its last four DIGITS (`[^0-9]` stripped first, so no
letter can survive that limb at all) and the custodian's account-TYPE string, punctuation
stripped, upper-cased, truncated to 24 characters. No name-derived value is passed to it.

Measured on the SERVED artifacts rather than on the builder: all three QA `directory.json`
objects were fetched back out of `opal-data-bd` / `opal-data-inf` / `opal-data-cot` and
censused -- **0 of 5062 discriminators fail the `****dddd[ / TYPE]` shape**, and the 36 distinct
type tokens are account-type vocabulary throughout (`IRA` 2843, `S1` 1705,
`INDIVIDUAL RETIREMENT AC` 119, `JOINT` 68, `BROKERAGE` 62, ... `KEOGH` 1).

**The residual, stated rather than argued away:** the type limb is an UNCONSTRAINED custodian
string, not an enumeration this cell validates. Twelve of the 36 tokens (`TRUST`, `LLC`,
`ESTATE`, `PARTNERSHIP`, `BANK`, ...) also occur as words inside entity display names -- that is
shared English, not leakage, since the token is read from the type column and never from the
name. But a custodian that one day writes a REGISTRATION TITLE into its account-type column
(`SMITH FAMILY TRUST U/A`) would have the first 24 characters of it flow into the
discriminator, and nothing in this cell would refuse it. Closing that would mean binding the
type limb to a ratified enum -- a schema act on `DirectoryEntry` (IB-s-18's surface), which this
order does not authorize me to touch. **This is the CVO's call, not mine.**

### 4. What an advisor could still be shown that the entitlement half (IB-s-2) must refuse

Five items, in descending order of what I would want IB-s-2 to answer first:

1. **THE SCOPE IS AN INPUT, NOT A PROOF.** `handler.py` consumes `ResolvedScope` from the
   caller. Any principal that can invoke `irpt-directory-search` can hand it a scope it wrote
   itself and receive that scope's projection. This cell deployed the function **UNWIRED** -- no
   route, no schedule, no event source -- so the only invokers today are AWS IAM principals;
   but IB-s-2/IB-s-15 must mint the scope SERVER-SIDE from a verified session and must never
   accept one off the request body.
2. **THE CROSS-FIRM FILTER IS CONDITIONAL ON A FIELD THE CALLER SUPPLIES.**
   `project()` (`handler.py:135`) reads
   `if firm and ids.get("firm_id") and ids["firm_id"] != firm: continue` -- so a scope that
   simply OMITS `verified_request_firm_id` disables the firm filter entirely and leaves only
   the account-set intersection standing. IB-s-2 must make that field MANDATORY and must refuse
   a scope without it, rather than relying on the account set as a second line.
3. **A CARDINALITY DISCLOSURE ON PARTLY-PERMITTED ENTRIES.** Search results carry
   `scope_completeness: PARTIAL` and `withheld_account_count` -- deliberately, because a
   silently narrowed answer looks exactly like a complete one (Andrew: unsupported positions are
   never silently removed). But that count tells an advisor HOW MANY sibling accounts exist
   inside a household it only partly serves. It is a real disclosure derived from custodian
   grouping, not from entitlement, and IB-s-2 owns the ruling on whether the count survives or
   collapses to a boolean.
4. **TERMINATION DATES TRAVEL WITH VISIBILITY.** A terminated client STAYS VISIBLE by Andrew's
   fixed constraint, and the search result carries `termination.effective_date` with it. That is
   a date about a former client returned to whoever holds the account today.
5. **THE PROJECTION IS IN-PROCESS, THE OBJECT IS FIRM-WIDE.** One `directory.json` per firm
   holds every entry for that firm; `irpt-directory-role` can `GetObject` it in all three firm
   buckets and the scoping happens in memory afterwards. Nothing today returns the unprojected
   set -- `search()` builds each result from an explicit field whitelist and `resolve()`
   intersects -- but the blast radius of ANY future code path in this function that forgets to
   call `project()` is the whole firm. IB-s-2's entitlement plane is the only thing that will
   ever stand between a caller and that object.

---

## DECLARED LIMITS OF THIS RESULT

- The **runner's production code deploy** is not in this cell's world: `safe-deploy.sh` accepted
  this serial, found the shared-home prefix carries 0 members, printed `SKIP-NOT-MEMBER` and
  `NOTHING WAS DEPLOYED`, and exited rc=0 under an `OK:` headline -- a third outcome the face
  does not contemplate, filed ARMED as row `IRPT_BCKEND-W2-S5`. The runner's schedule is
  IB-s-4's; the QA run this cell is authorized to make is ad hoc and landed.
- The `ResolvedScope` used throughout arms (b) and (e) is a **FIXTURE**. IB-s-2 supplies the
  real resolver. Nothing in this cell proves an entitlement decision is correct -- only that the
  handler never widens the one it is given.
- Arm (c)'s INF limb is **vacuous on the live population** and says so; its non-vacuous evidence
  is the constructed positive control (3 of 3).
