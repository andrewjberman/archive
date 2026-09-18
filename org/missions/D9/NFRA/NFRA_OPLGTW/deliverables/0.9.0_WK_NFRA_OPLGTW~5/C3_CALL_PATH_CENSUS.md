# C3 call-path census -- NFRA_OPLGTW.TO-OG-q-5, HALF TWO (OGQ5-AC5)

Population: every rule PRD `org/missions/D9/NFRA/NFRA_OPLGTW/prd/NFRA_OPLGTW_PRD.md` v0.9 @`e09219470f`
section "C3 - sources, closure and date semantics" states (lines 153-163 at that pin), built **by
subtraction from the printed denominator of C3's own sentences** -- never from a forward list of
rules this worker happened to remember (CLAUDE.md Rule 24(i)).

## Method (the point of this cell)

1. C3 is 6 blank-line-separated paragraphs at the pin (the heading + 5 body paragraphs); measured directly:
   `re.split('\n\n', ...)` over lines 153-164 of the pinned text returns exactly 6 non-empty blocks.
2. Each body paragraph was split into sentences on `(?<=[.])\s+` (a deterministic, mechanical split, not a
   judgment call about where a "rule" starts). **DENOMINATOR: 34 sentences** across the 5 body paragraphs
   (7 + 7 + 7 + 8 + 5 = 34; script and per-sentence printout run at this cell's cut, reproducible from the
   pinned text alone).
3. A sentence is EXCLUDED from the rule count only when it is (a) purely descriptive of upstream/external
   state with no independent operative constraint on the Gateway (2 sentences, P2.S1-S2), or (b) a pure
   logical CONSEQUENCE ("Thus...") of sentences already counted as their own rows, adding no new testable
   constraint (1 sentence, P3.S7). **3 sentences excluded, 0 rows.**
4. Three sentences (P5.S2, S3, S4) describe ONE mechanism (the CUSIP restriction, its non-join shape, and
   its budget accounting) and are folded into ONE row rather than three, because they state a single
   constraint the codebase implements (or fails to implement) as a single unit -- confirmed by reading
   `semantics.py`'s `qualify_asset_plan()`, which itself implements exactly these three clauses in one
   function. **2 sentences folded, 1 row (not 3).**
5. **RULE COUNT = 34 - 3 (excluded) - 2 (folded) = 29.**
6. Each of the 29 rows below carries: its C3 sentence(s) (quoted, with paragraph.sentence coordinates),
   whether a query-path call site enforces it (`file:line`), and one of the three verdicts. An
   `ENFORCED-ON-CALL-PATH` verdict is **measured through the app** -- either (i) a direct call to the
   shipped module against the real contract file at this HEAD (printed below, this worker's own run this
   turn), or (ii) a named OG-v-2 acceptance test that runs the real integrated Starlette app end-to-end
   (never a unit test of the same module asserting its own behaviour in isolation -- CLAUDE.md's "never a
   module's own tests" instruction).
7. **VERDICT DENOMINATOR: ENFORCED-ON-CALL-PATH 20, NOT-ENFORCED 5, NOT-A-CALL-PATH-RULE 4. 20+5+4 = 29 = the
   rule count.**

## The population, by subtraction

Paragraph 1 (7 sentences, all rows), Paragraph 2 (7 sentences, 5 rows + 2 excluded), Paragraph 3 (7
sentences, 6 rows + 1 excluded), Paragraph 4 (8 sentences, 8 rows), Paragraph 5 (5 sentences, 3 rows: S1,
S2+S3+S4 folded, S5).

---

### Paragraph 1 -- sources, prefixes, dates (7/7 rows)

**R1 [P1.S1]** "Source bucket is `opal-data-assets`; masters are 08242234 SmartX and 08335338 BlackDiamond."
**ENFORCED-ON-CALL-PATH.** `app/integrations/schwab/catalog.py` `parse_contract()` (:210-266) reads
`source_bucket`/`masters` from the contract file and refuses to construct a `CatalogContract` without them;
every S3 call in the module uses `self.contract.bucket`/`self.contract.masters` exclusively, never a
literal. Measured this turn, direct call against the real contract file at this HEAD:
`cat.parse_contract(json.load(open("org/standards/NFRA_OPLGTW_CONTRACT.json")), ...)` ->
`bucket='opal-data-assets' masters=('08242234', '08335338')`.

**R2 [P1.S2]** "Only their `silver/dim_position/`, `silver/dim_balance/` and `silver/dim_asset/` prefixes
are data-readable." **ENFORCED-ON-CALL-PATH.** `catalog.py` `parse_contract()` validates every
`data_prefix` against `<schwab/master/silver/dataset/>` (:232-237, `_parse_data_prefix` :269-274);
`head_set()` (:611-639) intersects every named object with `contract.data_prefixes` before it is HEADed or
GET; `_verify()` never reads a `ref["key"]` that did not pass that intersection. Measured this turn: the
real contract's `data_prefixes` = the 6 `schwab/<master>/silver/<dataset>/` prefixes for exactly
`dim_position`/`dim_balance`/`dim_asset`, both masters -- printed above (R1's run).

**R3 [P1.S3]** "A date is a Schwab business-date label, not object LastModified or request time."
**ENFORCED-ON-CALL-PATH.** Every date decision in `catalog.py` reads `closure.get("date")` or the
`date=<date>.json` marker key (`marker_key()` :764-772, `_is_date()` :319-321), never
`HeadObject`/`GetObject`'s `LastModified`; `_verify()` (:998-1073) never reads or branches on
`LastModified` at all (confirmed by reading the full method: it reads `VersionId`, `ContentLength`, `ETag`
only). Exercise: `tests/acceptance/test_local_acceptance.py::test_ogv2_a09` (OG-v-1's closure-variant dates,
including `stale_date`/`stale_version`, are distinguished purely by their `date=` label and closure
content, never by S3 object time).

**R4 [P1.S4]** "For each master/dataset the rolling window includes the latest qualified complete business
date and the previous 29 calendar days; do not silently fill missing dates from another master or
dataset." **ENFORCED-ON-CALL-PATH.** `catalog.py` `availability()` (:871-946) computes the window as
`latest - (window_days - 1)` where `window_days = ROLLING_WINDOW_DAYS = 30`
(`app/data_entitlement.py:66`, `ROLLING_WINDOW_DAYS = 30  # PRD C3: the latest qualified complete business
date and the previous 29 calendar days`); `_serves()` (:1141-1145) checks `f.get("dataset") == dataset`
against THIS master's own listed dates only -- no cross-master/cross-dataset fill exists anywhere in the
method. Exercise: `test_ogv2_a09` (per-dataset window/date variants) and `test_ogv2_ac01`.

**R5 [P1.S5]** "The available dates and latest qualified date are returned explicitly."
**ENFORCED-ON-CALL-PATH.** `catalog.py` `availability()` returns `available_dates`/`latest_qualified_date`
explicitly (:939-940); `app/integrations/schwab/integration.py` `get_access()`/`list_files()` copy those
fields verbatim into the tool response (integration.py is read-only cited here, not edited). Exercise:
`test_ogv2_ac01` (`say("OGV2-AC1: ... revision=...")`, asserts `capabilities`/`availability` fields present).

**R6 [P1.S6]** "A fixed-date grant is an enumerated date set." **ENFORCED-ON-CALL-PATH.** `catalog.py`
`_enumerated()` (:1161-1173) raises `CatalogRefused("a fixed_dates grant is an enumerated date set; none was
given")` when `MODE_FIXED` carries no dates. Measured this turn, direct call against the shipped module:
`Catalog._enumerated(MODE_FIXED, ())` -> `CatalogRefused: a fixed_dates grant is an enumerated date set;
none was given`. Exercise: `test_ogv2_a09` ("a FIXED-dates grant naming every variant date explicitly").

**R7 [P1.S7]** "Staleness is reported as days since the qualified business date and source observation
time, without pretending a missing business-calendar feed defines a late arrival." **ENFORCED-ON-CALL-PATH.**
`catalog.py` `_staleness()` (:1147-1159) computes `days_since_business_date` as plain calendar days and
states its own basis field verbatim: `"basis": "calendar days from the Schwab business-date label to the
Gateway clock's UTC date; no business calendar is applied, so this is not a claim about lateness"`.
Exercise: `test_ogv2_ac01`/`test_ogv2_a09` (`staleness` field present on every `availability` response,
printed in AC3's own measured payload above).

### Paragraph 2 -- producer completion metadata (5/7 rows, 2 excluded)

*[P2.S1]* "The existing producer markers ... do not by themselves prove closure." **EXCLUDED** -- states
the pre-existing problem, not an operative Gateway constraint.
*[P2.S2]* "Their declared fact tables and current-run written tables can differ and they do not pin
VersionIds." **EXCLUDED** -- same, context for R8/R9 below.

**R8 [P2.S3]** "Extend the producer's completion metadata contract ... to include a schema version,
master/date, run identity, expected source partitions, explicit non-applicable/empty dispositions, expected
table set, successful/failed outputs, counts and exact versioned silver objects." **NOT-A-CALL-PATH-RULE.**
This is a WRITE-SIDE rule on the producer (`data/assets/scripts/silver/conversion_manifest.py`, cell
OG-c-1, outside this Gateway entirely); the Gateway's own call path never extends or writes this metadata,
it only re-derives the producer's rule defensively from a record it is handed
(`catalog.py` `validate_closure()` :412-535, its own docstring: "ported from
data/assets/scripts/silver/conversion_manifest.py:509-640 @f4c7184f6d ... the Gateway cannot import the
producer, so the rule is carried"). Owned by the producer project, not this cell's call path.

**R9 [P2.S4]** "Publish qualified closure only after the complete expected set is reconciled."
**NOT-A-CALL-PATH-RULE.** WHEN the producer publishes a closure marker is entirely the producer's own
write-time decision; the Gateway only ever READS a marker that already exists (`_read_marker()` :977-996)
and validates it -- it has no code path that could publish, or refuse to publish, a completion record.

**R10 [P2.S5]** "The allowed completion object must carry sufficient sanitized closure facts itself; the
metadata role cannot follow references into meta/conversions or other prefixes." **ENFORCED-ON-CALL-PATH.**
`catalog.py` `marker_key()` (:764-772) builds the ONLY key ever read, from
`contract.completion_prefix_by_master` alone; `_read_marker()` (:977-980) raises `CatalogRefused` if the key
is not under `contract.completion_prefixes`; `validate_closure()`/`membership_findings()` (:412-535,
565-608) validate the closure as a wholly self-contained document -- there is no code anywhere in the
module that follows a key or reference elsewhere (confirmed by reading the whole file: the CATALOG role's
S3 calls are `list_objects_v2`/`get_object` against `completion_prefix_by_master` only, in `list_dates()`
and `_read_marker()`, and nowhere else). Exercise: `test_ogv2_a09` (closure fixtures never name a foreign
prefix); IAM-side confinement of the catalog credential is `comp-iam` territory, declared N/A for this cell
by the preflight and not re-measured here.

**R11 [P2.S6]** "A missing output, failed conversion, unexplained empty day, inconsistent grain, or
ambiguous inventory is incomplete." **ENFORCED-ON-CALL-PATH.** `catalog.py` `_TABLE_FINDING`/`add(...)`
calls in `validate_closure()` raise exactly `F_MISSING_OUTPUT`/`F_FAILED_CONVERSION`/
`F_UNEXPLAINED_EMPTY_DAY`(and `_OUTPUT`)/`F_INCONSISTENT_GRAIN`/`F_AMBIGUOUS_INVENTORY` (:293-300, 406-513);
none of these classes is in `UNAVAILABLE_CLASSES` (:125-126), so `_status_for()` (:663-668) always resolves
them to `STATUS_INCOMPLETE`. Exercise: `test_ogv2_a09`'s `missing`/`failed`/`partial`/`grain_mismatch`/
`foreign_object` closure variants (make_fixtures.py `VARIANT_INTENT`, lines 237-251).

*[P3.S7]* "Thus no historical date is promised accessible merely because a silver prefix exists."
**EXCLUDED** -- a stated CONSEQUENCE of R13-R18 below (P3.S1-S6), not an additional constraint of its own.

**R12 [P2.S7]** "Do not repair source data or rewrite silver values as part of this extension."
**NOT-A-CALL-PATH-RULE.** A build-discipline directive to the producer-extension project itself (never
silently repair source while extending the completion contract); the Gateway's OWN call path never writes
to any silver object at all (it is read-only by `SPEC.read_only=True`, `integration.py:80`) so there is no
Gateway code position where "repairing source" could even occur.

### Paragraph 3 -- Gateway catalog construction (6/7 rows, 1 excluded above)

**R13 [P3.S1]** "Gateway catalog construction validates the closure record and independently HEADs every
named silver object." **ENFORCED-ON-CALL-PATH.** `catalog.py` `snapshot()` (:805-869) calls
`validate_closure()` (:832) then `_verify()` (:846-848), which HEADs every ref by `_head()` (:1075-1086,
called at :1014 and :1026 -- once pinned, once live). Exercise: `test_ogv2_a09`.

**R14 [P3.S2]** "It persists an immutable catalog snapshot with the closure version, table/master/date,
object VersionIds, sizes, schema fingerprint, row counts, validation result and opaque authorized file
IDs." **ENFORCED-ON-CALL-PATH.** `_compose()` (:1099-1132) builds exactly this shape (`closure_id`,
`master`, `business_date`, `files[].version_id/size/schema_fingerprint/rows`, `validation.result`,
`files[].file_id`); `persist()` (:949-955) writes it with `acs.IF_ABSENT` -- a second write of the same key
raises `acs.ConditionFailed` and nothing is overwritten (immutability). Exercise: `test_ogv2_a09`/`ac02`
(catalog-ID listing, `public_files()`).

**R15 [P3.S3]** "GET every data object by that VersionId." **ENFORCED-ON-CALL-PATH.** `_get()` (:1088-1097)
always passes `VersionId=version_id`; `_verify()` only reaches `_get()` after `_versioned(pinned)` (:1010)
holds. Exercise: `tests/acceptance/conftest.py`'s `S3_CALLS` recorder (:104, :142-167), which every og_v2
test shares -- every recorded `GetObject` under a data prefix carries a `VersionId` by construction of this
call site.

**R16 [P3.S4]** "Reject null/unversioned identities or changed/unavailable versions." **ENFORCED-ON-CALL-PATH.**
`_verify()` (:1010-1037) raises `F_UNVERSIONED_OBJECT` (no usable pinned VersionId, or the live object
carries none), `F_VERSION_UNAVAILABLE` (pinned version absent from the bucket, or the key itself absent),
`F_VERSION_CHANGED` (bucket answers a different version, or a newer version replaced the pinned one).
Exercise: `test_ogv2_a09`'s `unversioned`/`stale_version` variants.

**R17 [P3.S5]** "Revalidate source membership and byte bounds; no marker may introduce another
bucket/master/dataset." **ENFORCED-ON-CALL-PATH.** `membership_findings()` (:565-608) checks every named
object's bucket/master/dataset against the contract BEFORE anything is read (its own docstring: "costs zero
S3 calls"); `_verify()`'s byte-bound check (:1038-1041) refuses `size` outside `(0, max_object_bytes]`.
Exercise: `test_ogv2_a09`'s `foreign_object` variant.

**R18 [P3.S6]** "Legacy markers are nonqualifying until a controlled producer replay or metadata backfill
reconciles against original inputs and exact current output versions." **ENFORCED-ON-CALL-PATH.**
`snapshot()` (:823-829): a marker whose `closure` is not a dict returns `RESULT_LEGACY`/`F_LEGACY_MARKER`
before any validation runs. Exercise: `test_ogv2_a09`'s `legacy_only` variant
(make_fixtures.py `LEGACY_SCHEMA`/`"legacy_only": ("no_closure", ())`).

### Paragraph 4 -- positions/balances semantics (8/8 rows)

**R19 [P4.S1]** "Positions/balances are snapshots at one date." **ENFORCED-ON-CALL-PATH.**
`app/integrations/schwab/query.py` `Query.business_date` is a single required scalar
(`REQUIRED_PROPERTIES` :53; `_valid_date(obj["business_date"])` :322-323); `QUERY_PROPERTIES` (:51-52) has
no list-of-dates property at all, so one `Query` is structurally bound to one date. Exercise: every schwab_
query test names exactly one `business_date`.

**R20 [P4.S2]** "Grouping never removes master/date identity and never sums snapshots across dates."
**NOT-ENFORCED.** `semantics.py` `assert_grouping_preserves_identity()` (:173-181) exists to refuse
`group_by=["business_date"]` and has **zero production callers** anywhere in `app/`
(`comp-find 'assert_grouping_preserves_identity' infra/aws/ec2/opal-gateway/app --all` -> 1 DEF, 0 SURFACED,
this turn). Measured directly against the shipped, unedited `check_against_grant()` with the real contract:
a `dim_balance` aggregate query with `group_by=["business_date"]` (a real, contract-declared field of that
dataset) is **accepted, not refused** -- `NO REFUSAL: group_by business_date accepted` (this worker's own
run, this turn). The "sum across dates" half is separately guaranteed by R19 (one Query, one date), but the
"grouping never removes date identity" half is a live, measured gap -- the same shape as the cell's own
HALF ONE (a criterion proven only where nothing calls it).

**R21 [P4.S3]** "Both-master questions use separate tool calls/results; date comparisons use separately
authorized snapshots and exact decimal deltas." **ENFORCED-ON-CALL-PATH** (the "separate calls" half; the
combining-function half is discussed under R20's sibling, `separate_master_results`, itself uncalled but
moot -- see note). `query.py` `Query.master` is a single scalar checked by `_enum(obj["master"],
rules.masters, ...)` (:320); no property or grammar shape in `QUERY_PROPERTIES` accepts more than one
master, so one tool call is structurally bound to one master (same shape as R19). `semantics.py`'s
`separate_master_results(combine=True)` (:231-237) and `snapshot_delta` (:215-225) are pure helpers for
COMBINING two already-separately-authorized calls' numbers -- that combination happens outside this
Gateway's own call path (a caller/skill, per `semantics.py`'s own docstring :34-39), so their zero
production callers do not represent a live gap the way R20's does: there is no Gateway code position that
could violate "separate tool calls" (structurally one master per call), and no Gateway tool combines two
dates at all. Exercise: `test_ogv2_a06`/`a08`/`a09` never issue a two-master query in one call.

**R22 [P4.S4]** "Vendor balance fields overlap: permit a named field's sum across approved accounts, never
construct a cash/AUA total by adding different balance fields." **NOT-ENFORCED** (the negative half; the
positive half -- summing one named field across approved accounts -- is separately enforced by the account
`PolicyFilter` mechanism, `query.py` `build_plan()` :551-553, unrelated to this gap).
`semantics.py` `assert_single_balance_metric()` (:260-270) exists precisely to refuse summing more than one
distinct `dim_balance` field in one query, and is called only from `assert_sum_allowed()` (:273-279) --
which itself has **zero production callers** (`comp-find` this turn: only its own DEF and the one internal
call inside itself). `query.py` `check_against_grant()` (:464-478) calls `sem.assert_field_summable()` and
`sem.assert_quantity_sum_grouped()` directly (OG-q-4's wiring, R-OG-13) but never `assert_sum_allowed()` or
`assert_single_balance_metric()`. Measured directly against the shipped, unedited module with the real
contract: an aggregate query summing BOTH `mkt_value_long` and `mkt_value_short` (two distinct
`dim_balance` additive fields) in one request is **accepted, not refused** -- `NO REFUSAL: summing two
different dim_balance fields in one query accepted` (this worker's own run, this turn).

**R23 [P4.S5]** "Quantity sums require grouping by CUSIP and long/short indicator; price is nonadditive."
**ENFORCED-ON-CALL-PATH.** `query.py` `check_against_grant()` (:470-475) calls
`sem.assert_field_summable(query.dataset, agg.field)` and
`sem.assert_quantity_sum_grouped(query.dataset, agg.field, query.group_by)` in the SAME loop that validates
every aggregate's field against the grant (OG-q-4, ruling R-OG-13). Measured directly this turn: `SUM` on
`quantity_settled` with no `group_by` -> `REFUSED as expected: INVALID_REQUEST quantity_sum_ungrouped`.
Price (`closing_price`) is absent from `ADDITIVE_FIELDS` everywhere (`semantics.py` :244-247's own
docstring), so `assert_field_summable` refuses summing it.

**R24 [P4.S6]** "Duplicate/conflicting source grains produce unavailable, not silent deduplication."
**NOT-ENFORCED.** `semantics.py` `assert_unique_grain()` (:285-295) exists to raise `UNAVAILABLE` on a
duplicate/conflicting grain key among result rows and has **zero production callers**
(`comp-find 'assert_unique_grain' infra/aws/ec2/opal-gateway/app --all` -> 1 DEF, 0 SURFACED, this turn).
Neither `query.py` nor `integration.py` calls it anywhere after a job returns rows; the engine's own
DuckDB execution (`engine.py` `_plan_job`) has no grain-uniqueness check of its own either (confirmed by
reading the full function :630-696: it projects, filters and runs the generated SQL, nothing else). A
`rows`-mode duplicate simply returns as two rows; an `aggregate`-mode duplicate is silently folded into the
SUM/COUNT like any other row -- the opposite of "produce unavailable".

**R25 [P4.S7]** "Dataset description records grain, field type, unit, sign and null semantics from measured
source plus independent fixtures." **NOT-ENFORCED** (partial: grain and type/unit ARE exposed; sign and
null_semantics are NOT). `semantics.py` `describe_field()`/`describe_dataset()` (:151-163) read exactly
this shape from `datasets.json` (`_FIELD_DESCRIPTION_KEYS = ("type", "unit", "sign", "grain",
"null_semantics", "source")`, :81) and have **zero production callers**
(`comp-find 'sem.describe_field|sem.describe_dataset' infra/aws/ec2/opal-gateway/app --all` -> 0 hits, this
turn). The LIVE `schwab_describe_dataset` tool (`integration.py` `describe_dataset()` :438-477) builds its
own response directly from `qry.DATASET_SCHEMAS`, never from `semantics.DATASETS`: it emits `name`/`type`
always, `precision`/`scale`/`unit`/`representation` for decimal fields only, and `grain` separately --
**`sign` and `null_semantics` are never included in the tool's response at all**, even though `datasets.json`
carries both for every field (cross-validated at import time by `semantics._validate_datasets()`, :91-135).
A caller of the registered tool cannot learn a field's sign or null semantics from the Gateway today.

**R26 [P4.S8]** "Unsupported/unverified metrics are refused." **NOT-A-CALL-PATH-RULE.**
`semantics.py` `resolve_metric()`/`VERIFIED_METRICS` (:305-319) exist to refuse a metric requested BY NAME,
and have **zero production callers** (`comp-find 'resolve_metric' infra/aws/ec2/opal-gateway/app --all` ->
1 DEF, 0 SURFACED, this turn) -- but none of the five tools (`TOOL_NAMES`, `integration.py` :68-69) accepts
a bare metric-name string anywhere: `schwab_query`'s aggregate shape requires an explicit
`function`+`field`+`alias` (`query.py` `AggregateSpec`, already validated against the contract's
`aggregate_operators` and the dataset's own schema by `parse_query`/`check_against_grant`). There is no
call-path surface where an "unsupported/unverified metric NAME" could even be submitted today; `resolve_metric`
is dead code reserved for a naming surface the five tools do not expose.

### Paragraph 5 -- the asset reference dataset (3 rows: S1, S2+S3+S4 folded, S5)

**R27 [P5.S1]** "The asset reference dataset carries only its approved security fields."
**ENFORCED-ON-CALL-PATH.** `check_against_grant()`'s `visible = contract_fields & set(granted_columns)`
gate (:450-457) applies uniformly to every dataset including `dim_asset`; an unknown or hidden `dim_asset`
field raises `ENTITLEMENT_DENIED`/`field_not_available` exactly like every other dataset. Measured directly
this turn against the shipped module with the real contract: requesting `dim_asset` column
`maturity_date` with a grant that omits it -> `REFUSED as expected: ENTITLEMENT_DENIED field_not_available`.

**R28 [P5.S2+S3+S4]** "For a partial-account grant restrict its CUSIPs to holdings of the authorized
accounts for that same master/date, using a qualified position snapshot solely for policy selection. This
internal policy filter is not a user-facing enrichment join. Its position objects count toward the same
object/byte/deadline limits; absent qualification denies the asset read."
**NOT-ENFORCED.** This is TO-OG-q-5's own HALF ONE and the row that opened this cell (`NFRA_OPLGTW-W6-S8`,
ARMED, owner `1.0.0_SA_CTO`). `semantics.py` `qualify_asset_plan()` (:330-360) is ALREADY BUILT to
implement all three clauses together (appends `eng.PolicyFilter("cusip", sorted(position_cusips))` to the
asset plan -- never a join; re-tags the position `SourceObject`s `role="policy"` so `check_sources()`
counts them toward the identical object/byte caps, per `engine.py`'s own `SOURCE_ROLES`/`SourceObject`
contract, :112, :213-218; raises `ENTITLEMENT_DENIED`/`asset_read_denied_unqualified` when
`position_cusips` is empty or no position sources are supplied) -- but it has **zero production callers**
(`comp-find 'qualify_asset_plan' infra/aws/ec2/opal-gateway --all` -> 1 DEF, 4 TEST -- its own unit tests in
`tests/test_schwab_semantics.py`, never a call from `app/integrations/schwab/integration.py`'s
`SchwabService.query()`, the one call site that could supply its `position_sources`/`position_cusips`
arguments). Measured through the registered `schwab_query` tool on OG-v-2's live-app harness THIS TURN
(`tests/test_schwab_asset_policy.py::test_ogq5_ac01/02/03`, this cell's own deliverable): a partial-account
`dim_asset` grant for account `99000002` on `(08242234, 2026-07-09)` returns all 4 fixture CUSIPs
unfiltered (`['SYN000001','SYN000002','SYN000003','SYN000009']`) instead of the 2 its account holds; a
CUSIP held only by an ungranted account (`SYN000003`, account `99000003`) is PRESENT regardless of which
of the two grants is used; and a grant whose sole account holds nothing on this master (`99000004`, a
BlackDiamond-only account) still returns all 4 CUSIPs with `is_error=False` instead of being denied. See
this worker's surprise row `NFRA_OPLGTW-W5-S13` for why the fix cannot be wired inside this order's
`<paths>` grant (the orchestration belongs in `integration.py`, not `query.py`/`catalog.py`).

**R29 [P5.S5]** "No other cross-dataset join is enabled in v1." **ENFORCED-ON-CALL-PATH.** `query.py`'s
grammar has no join concept anywhere: `QUERY_PROPERTIES` (:51-52) names eleven single-dataset properties
and no "join"/"joins"/"with" property; `Query.dataset` (:236) is a single scalar; `build_plan()` (:522-573)
builds exactly one `eng.QueryPlan` reading exactly one dataset's `DATASET_SCHEMAS[dataset]`. The only
cross-dataset mechanism anywhere in the codebase is the one R28 describes (`qualify_asset_plan`'s
`PolicyFilter`-based cusip restriction, itself unused today) -- there is no OTHER one to find, checked by
reading `query.py`, `catalog.py`, `engine.py` and `semantics.py` in full at this HEAD.

---

## Denominators (printed, per OGQ5-AC5's own requirement)

- **Sentences in PRD C3 (v0.9 @e09219470f):** 34
- **Rules (by subtraction: 34 - 3 excluded - 2 folded):** 29
- **ENFORCED-ON-CALL-PATH:** 20 (R1-R7, R10, R11, R13-R19, R21, R23, R27, R29)
- **NOT-ENFORCED:** 5 (R20, R22, R24, R25, R28)
- **NOT-A-CALL-PATH-RULE:** 4 (R8, R9, R12, R26)
- **Sum check:** 20 + 5 + 4 = 29 = rule count. ✓

## Findings beyond HALF ONE (R28), per this cell's own bound ("the census FINDS; it does not FIX")

Four additional `NOT-ENFORCED` rules were found -- R20 (grouping can remove date identity),
R22 (a query can sum two distinct `dim_balance` fields into an implicit combined total), R24 (duplicate/
conflicting source grains are never detected post-scan), and R25 (a field's sign and null semantics are
never exposed by the live `schwab_describe_dataset` tool even though `datasets.json` carries them). Each is
the SAME shape ruling R-OG-17 names: a criterion (`semantics.py`'s own AC1/AC6/AC9/AC10 functions, all
already built and unit-tested) proven only where nothing calls it. Each is filed as its own surprise row
below; the remedy is the issuer's to place (this cell repairs only R28's HALF ONE, and could not even do
that -- see `NFRA_OPLGTW-W5-S13`).
