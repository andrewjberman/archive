<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-06-firm-parameterized-spine</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~Z</issued_to>
    <date>2026-08-06</date>
    <status>staged</status>
    <project_code>MDPF_CANRTE</project_code>
  </metadata>

  <objective>
    Refactor the MDPF gold computation into ONE firm-parameterized path with config-only firm bindings —
    **together with the Cottonwood producer family, in one atomic unit** — producing all 14 canonical
    artifacts plus the dated `_aggregate_aua`, with genuine per-scope independence, conditional immutable
    writes, and one canonical trading calendar.
  </objective>

  <context>
    ### ⛔ THIS TO AND THE COTTONWOOD PRODUCERS ARE ONE ATOMIC UNIT (CTO~Z ruled)

    `build_cottonwood_mdpf_pair.py:64-65` imports **`_distribution_stats`** — a PRIVATE symbol — plus
    `calc_metric` and `quarter_ends` OUT of the mdpf tree by bare module name via a `sys.path` hop.
    **A refactor of `dim_mdpf_account_distribution` BREAKS COTTONWOOD WITH NO SIGNAL IN THE MDPF TREE**: a
    leading underscore declares that nobody outside may depend on it, so nothing warns you that someone does.
    **THEY MOVE IN ONE WAVE. THE SEQUENCING IS THE CONTROL** — naming the shared resource is not sufficient.
    Internal order: **backfill → slice → spine** (the backfill's output is an input to the slice).
    The coupling is not preserved; "one firm-parameterized path" dissolves it — `_distribution_stats`,
    `calc_metric`, `quarter_ends` become internal functions of the one Lambda.

    ### WHAT YOU ESTABLISHED THAT THE PACK DID NOT KNOW (do not re-derive)

    - **"Firm-parameterized" is FALSE in the incumbent — THREE shapes, not one.** 49f bespoke; inflection
      bespoke with a DIFFERENT signature and **coupled to 49f's `dates` as its axis**; cottonwood NOT built
      here at all (`load_cottonwood_slice` emits bytes verbatim from an external producer); global a fold.
    - **Cottonwood's real L2 producer is a FAMILY OF THREE in a DIFFERENT TREE** —
      `build_cottonwood_mdpf_slice.py` (956), `build_cottonwood_mdpf_pair.py` (510),
      `build_cottonwood_interpolated_backfill.py` (748), under `data/assets/scripts/gold/`, a Rule-13
      SHARED repo home with its own S3-membership deploy guard (key-exists=update enforced, 404=loud skip,
      first-mints explicit). **The port crosses a deploy-story boundary, not just a directory one.**
    - **CHANNEL INDEPENDENCE DOES NOT HOLD TODAY.** A raise inside `build_49f_artifact` aborts everything;
      an ABSENT 49f makes `axis = arts.get(...).get("dates") -> None` so **inflection SILENTLY builds on a
      different axis**; `build_global_artifact(arts["49financial"], ...)` is a direct subscript → KeyError.
      **Per-scope exceptions are work to ADD, not preserve** — so the equivalence-vs-incumbent battery and
      the channel-independence battery MEASURE OPPOSITE THINGS and cannot be the same suite.
    - **NAMING TRAP:** `build_mdpf_spine.py` is a 145-line DRIVER. The spine is
      `dim_mdpf_aggregate_aua_timeseries.py` (2587), imported as `spine`. Port "the spine" by filename and
      you port the wrapper.
    - Real closure: **14 modules / 9,442 lines across three directories and two trees** — 53% larger than
      the pack's implicit scope, including a SILVER-tier module (`rebalancer_schemas`) imported into gold.

    ### PACKAGING — DECIDED BY YOU, AND THE CAVEAT IS YOURS TOO

    **FLAT vendoring, both gold trees flattened into ONE namespace, roster at `/var/task/partner_roster.json`.**
    One namespace is **FORCED, not preferred**: the cross-tree private-symbol import means the two trees are
    already one runtime namespace. Collision check 45 files / 0 duplicate basenames, positive-controlled.

    **TWO resolving sites, not four.** `__file__` resolves through the FUNCTION'S OWN module globals, so
    inside `_load_partner_roster` it is always the spine's file regardless of caller — you EXERCISED that
    with a two-directory fixture rather than assuming it. Real sites: `_load_partner_roster`
    (`dim_mdpf_aggregate_aua_timeseries.py:1728`) and `_cot_window` (`build_cottonwood_mdpf_slice.py:870`).
    ⚠ A THIRD is real but out of scope: `build_portal_gold_accrual.py:125` — the 09:40 accrual bridge,
    dispositioned RETIRE. **IF THE BRIDGE RETIREMENT SLIPS IT RETURNS AS A THIRD ADJACENCY REQUIREMENT**
    (P4 ledger carries the dependency between "bridge retired" and "layout is sufficient").

    ### ⛔ AND THE PART THAT CUTS AGAINST THE LAYOUT DECISION — YOURS, AND IT GOVERNS CRITERION 4

    > **FLAT MAKES `_cot_window()`'s HARDCODED `return 3` UNREACHABLE. IT DOES NOT FIX IT.
    > THE LAYOUT MASKS THE DEFECT.**

    Under flat its candidate 1 hits, so the bare `except Exception: pass` + literal never fires. **If anyone
    later moves a module into a subpackage — AN ORDINARY TIDY-UP — the mdpf resolver keeps working,
    `_cot_window` silently returns a constant, Cottonwood's carry window stops following the roster, and the
    fail-closed guard PASSES BECAUSE IT IS THE OTHER READER.**
    **"We chose flat, therefore the roster is fine" MUST NOT BECOME THE RECORD.** The property has to assert
    itself, because the thing protecting it right now is a layout choice a future refactor is entitled to change.

    ### RULINGS THAT BIND THIS TO

    - **ROSTER (CTO~Z 213508Z):** build-generated hash-tied copy via the existing resolver, **NO S3
      GetObject leg.** 230319Z's target is DUPLICATE AUTHORITY — a second thing that can answer
      *what is expected-ness* and can disagree. **Measured cost:** the deployed roster diverged from the
      committed authority for NINE DAYS on `per_partner_max_lag_trading_days` with nothing detecting it.
    - **CALENDAR (CTO~Z):** bind `lib/trading_calendar` via the WS-1 layer; **retire the shim and both
      inlined privates** at `:154,164`. Tie-out discharged (n=1096, 0 disagreements, falsifier fired;
      **2027 shows 10 disagreements — every 2027 NYSE holiday**). The `<5` PMC pin ports WITH its full
      rationale. **The fallback-vs-fallback comparison stays PINNED with `_USE_PMC=False` forced** — once
      PMC is in the layer the naive test passes everywhere and the 2027 divergence goes invisible again.
      SCOPE BOUND: `bd-served-vintage-alarm`, `inf-etf-ownership-daily`, `opal-assets-absence-check` are
      OTHER PIPELINES and are NOT touched.
    - **PLATINUM DATED PREFIX IS GONE** (@4a2651063, Andrew-direct): 444 objects archived. **Treat
      `platinum/mdpf/aggregate_aua/` as GONE, not as a contract to preserve.** The real contract is
      `gold/mdpf_revamp/_aggregate_aua` — already the trigger's deployed env; the leading UNDERSCORE is
      load-bearing (a bare `aggregate_aua/` was rejected); `opal-assets-daily-emitter` reads it
      (deployed-confirmed via `AGGREGATE_PREFIX`).
    - ✅ **PER-SCOPE PLATINUM — RULED BY ANDREW 2026-08-06 ~2205Z. NO LONGER PENDING.** VERBATIM:
      *"Yeah obviously we need the three files for each scope. that means aggregate-aua-timeseries.json,
      aum-metrics.json, and account-distribution.json for Global, for 49 Financial, for Inflection, and for
      Cottonwood. 3 files times 4 scopes means that this pipeline needs to generate 12 platinum files into
      the relevant scope path buckets in opal-data-portal-v2/platinum/mdpf/{scope} every single day, is that
      abundantly clear?"*

      **THE CONTRACT:** `opal-data-portal-v2/platinum/mdpf/{scope}/` for
      `{global, 49financial, inflection, cottonwood}` × `{aggregate-aua-timeseries.json, aum-metrics.json,
      account-distribution.json}` = **12 PLATINUM FILES, EVERY SINGLE DAY.**

      **THIS SETTLES THE DESIGN, NOT JUST THE PATH. PER-SCOPE PATHING MAKES CHANNEL INDEPENDENCE PHYSICALLY
      ENFORCEABLE** rather than a property the builder must remember to honour: one partner's failure cannot
      silently remove another partner from a document **because they are no longer in the same document** —
      absence becomes a MISSING OR STALE FILE rather than a quietly shorter payload. **A single
      multi-partner document cannot be channel-independent by construction, whatever the builder intends.**
      The multi-partner single document is the mechanism this REMOVES, not a shape to preserve.

      ⚠ **"EVERY SINGLE DAY" IS PART OF THE RULING, NOT DECORATION.** It binds the scheduled production path
      and makes **12 a DAILY COMPLETENESS DENOMINATOR — a cycle emitting fewer than 12 is INCOMPLETE, not
      merely quiet.**

    - ✅ **12-vs-14 RESOLVED, Andrew-direct ~2215Z — A THIRD WAY NEITHER READING OFFERED.**
      **EXACTLY 12 FILES, and the two extras' INFORMATION FOLDS INTO the canonical 12** rather than
      continuing standalone or being dropped:
        `account-units` count → **INTO `account-distribution.json`** (his reason: that is the file feeding
          the bell curve, which is the component that serves the count)
        non-model assets → **INTO BOTH `aum-metrics.json` AND `aggregate-aua-timeseries.json`** (both portal
          components feature non-model)

      ⛔ **SHAPE LAW — the 12 are IDENTICAL IN SHAPE ACROSS SCOPES at platinum.** The folded fields are
      canonical for EVERY scope. **A scope without data carries the field with HONEST ABSENCE** (existing
      null-not-zero guards) — **NEVER a scope-specific schema.** So `account_units` exists on all four
      account-distribution files, not only cottonwood's; non-model fields exist on all four of each type,
      not only global's.

      ⛔ **LAYER LAW — VENDOR DIVERGENCE IS LEGITIMATE IN BRONZE/SILVER AND DIES IN GOLD.** Cross-vendor
      normalization is explicitly GOLD's job; **platinum projects an already-canonical gold and NEVER
      patches shape.** His framing: canonical serve shape first, then work back layer by layer. If a vendor
      difference reaches platinum, the defect is in gold — do not fix it downstream.

      ⇒ **THE P1 SPEC NOW CARRIES A CANONICAL OUTPUT SCHEMA PER ARTIFACT TYPE — one schema, four scopes,
      folded fields included.** That composes with doc 02's "AUM metrics soft-fail not acceptable" row:
      **per-scope STATUS varies in the manifest; SHAPE does not.**

      ⚠ **H6 IS DISCHARGED THROUGH THIS, NOT VIOLATED BY IT.** H6 pins served schema against silent
      cleanup in an infrastructure cutover. This fold is **exactly the "separately tested schema migration"
      doc 04 anticipates** — deliberate, in-scope, and tested. **The cutover still does not SILENTLY rename
      anything; the convergence is its own explicit act.** Do not cite H6 to refuse the fold, and do not
      cite the fold as licence for any other schema change.

      ⚠ **ORDERING (mechanism, not gate): THE TWO STANDALONE EXTRAS RETIRE ONLY AFTER THEIR INFORMATION IS
      FOLDED AND VERIFIED IN THE CANONICAL 12.** They were written by this morning's live cycle — they are
      CURRENT output, not residue. **Nothing stops before its replacement is proven.** Same shape as the
      DEPLOY-BEFORE-ENV lesson: the order is correctness, not preference.

      ⚠ Portal component re-points (the bell curve reading the folded count; non-model components dropping
      their standalone fetch) are **DT/portal-lane work — SURFACED, NOT STARTED**, and not this project's
      scope under the standing frontend guard.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before writing:
      <run>comp-pipescript io &lt;each gold script touched&gt; --pipeline mdpf</run>
      <expect>COLUMN GAPS + portal consumers per script. `--pipeline` REQUIRED — flagless is rc=2 REFUSED.</expect>
      <if_mismatch>Any COLUMN GAP is fixed or recorded BEFORE code changes — silent column omissions have
      produced zero-valued served output before.</if_mismatch>

      <run>comp-blast dim_mdpf_account_distribution</run>
      <expect>Radius WITH DENOMINATOR. The cross-tree Cottonwood consumer MUST appear; if it does not, that
      absence is itself the finding — a private-symbol import across trees is exactly what an extractor
      misses.</expect>
      <if_mismatch>A ZERO is a LOWER BOUND — measured false zero on mdpf_aggregate_aua @c801ec9d5.</if_mismatch>

    Phase 2 — before committing:
      <run>comp-validate &lt;each script&gt; --artifact /tmp/&lt;artifact&gt;.json</run>
      <expect>exits 0; PASS or WAIVED.</expect>
      <if_mismatch>`NO_CONFIG` or `ZERO_CHECKS` means UNVALIDATED — NEVER signal SAFE on it.</if_mismatch>

    Phase 3 — after committing:
      <run>comp-pipescript deployed &lt;each script&gt;</run>
      <expect>MATCH after upload.</expect>
      <if_mismatch>STALE or MISSING is a blocker; report to COO~Z.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <shared_resource>`dim_mdpf_account_distribution._distribution_stats` (PRIVATE), `calc_metric`,
    `quarter_ends` — imported cross-tree by `build_cottonwood_mdpf_pair.py:64-65`</shared_resource>
    <also_in_to>THE COTTONWOOD FAMILY IS INSIDE THIS TO — that is the control</also_in_to>
    <last_write_owner>0.4.0_DS_ClientPlatform~Z (both trees, Rule 13)</last_write_owner>
    <required_action>Move them together. Do NOT land a mdpf-tree refactor and follow with a cottonwood
    commit — the window between them is the breakage, and nothing in the mdpf tree signals it.</required_action>

    <shared_resource>The Lambda package layout + BUILD_MANIFEST (AE~Z's P1-2 / P2-1)</shared_resource>
    <also_in_to>P1-2 · P2-1</also_in_to>
    <required_action>You supply module PATHS + a COMMIT; AE~Z computes hashes from the repo file at build —
    a hash supplied by hand and a hash computed from the artifact are different claims and only the second
    is a control. Runtime is **python3.11, NOT 3.12** (hard ABI pin; the live 3.12 MDPF Lambdas are thin
    JSON handlers touching no columnar stack and are NOT a counterexample), x86_64, FLAT at zip root, repo
    files are source of truth, NEVER edit a zip.</required_action>

    <shared_resource>`gold/mdpf_revamp/_aggregate_aua/{date}.json` and `opal-assets-daily-emitter`</shared_resource>
    <also_in_to>P4-1 · P6-3 (W-1a L7/L8/L9 close against it)</also_in_to>
    <required_action>MID-CUTOVER, NOT SETTLED. Preserve the exact key or atomically re-point the emitter
    with equivalence proved. **DEPLOY BEFORE ENV** — env-first would make the emitter read copied history,
    log a valid key, report 11 cohorts and read GREEN while the live partition landed elsewhere unwatched.
    **The rollback mitigation is what would have made that failure silent.**</required_action>
  </cross_domain_coordination>

  <acceptance_criteria>
    1. ONE CODE PATH WITH CONFIG-ONLY FIRM BINDINGS. 49financial / inflection / cottonwood build through the
       same function driven by config rows; global is a FOLD, not a fourth builder, and is invoked EXACTLY
       ONCE after the available firm outputs.
       FORBIDDEN SHORTCUT, NAMED: a dispatch dict mapping firm → bespoke builder is THREE SHAPES WITH A
       LOOKUP IN FRONT. The incumbent's inflection builder takes a different signature and consumes 49f's
       `dates`; if that cross-firm axis dependency survives in any form, this criterion is not met.

    2. CHANNEL INDEPENDENCE IS EXERCISED, NOT ASSERTED. In a fixture make EACH firm fail in turn and confirm
       the other two still succeed. Confirm global carries only eligible features, LABELS each carry with
       its source data-as-of, and becomes HONEST ABSENCE after its window. Confirm no firm reads a sibling's
       frontier or gates on a sibling completion marker.
       FORBIDDEN SHORTCUT, NAMED: **an ABSENT firm must FAIL, not silently re-axis.** The incumbent's
       `arts.get(...).get("dates") -> None` path is the defect, and a test that only raises inside a builder
       never reaches it. Exercise BOTH the raise and the absence.
       THIRD STATE: a failed firm is `skipped` with honest absence — not zero, not omitted.

    3. `count_as_of` SURVIVES ON GLOBAL. `global/aggregate-aua-timeseries.json` carries `count_as_of`; its
       TWELVE SIBLINGS DO NOT.
       FORBIDDEN SHORTCUT, NAMED: **DO NOT VERIFY BY SAMPLING ONE KEY PER ARTIFACT FAMILY.** A uniform build
       path drops this field from exactly one served key — the most visible one — and any spot-check that
       sampled a firm key would have passed. Assert PER KEY against the P0-1 schema baseline. H6 binds: seven
       as-of families are FACTS TO PRESERVE, and `as_of_date` (2 of 23 objects) is NOT a convention to align to.

    4. BOTH ROSTER READERS FAIL CLOSED, PROVEN BY TEST FROM THE BUILT ARTIFACT.
       (a) SOURCE FIX: `_cot_window()` loses the bare `except Exception: pass` and the `return 3`, and fails
       closed like its sibling. `return 3` IS a private copy of a roster value — the sect-III-e defect
       230319Z names, in a line that cites 230319Z.
       (b) TEST: assert **EACH** reader raises when no candidate exists. **ONE TEST PER READER.**
       FORBIDDEN SHORTCUT, NAMED: a test written against `_load_partner_roster` alone **PASSES TODAY** while
       the real defect sits in the other tree — the control-that-cannot-fail shape inside the control built
       against it. And **FLAT LAYOUT IS NOT THE FIX**: it makes `return 3` unreachable, and a later
       subpackage tidy-up re-arms it silently while the fail-closed sibling still passes.
       ⚠ This CHANGES Cottonwood's failure behaviour from silent-degrade to refuse-the-build. That is
       correct and intended; record it as a behavioural change, not a cleanup.

    5. ONE CANONICAL CALENDAR, ASSERTED NOT ASSUMED. `lib/trading_calendar` via the WS-1 layer; shim and
       both inlined privates RETIRED. Every calendar-touching artifact asserts
       `calendar_source() == "NYSE/pandas_market_calendars"` at build time AND in acceptance.
       FORBIDDEN SHORTCUT, NAMED: doc 02's "import-health invocation" is FAIL-GREEN BY CONSTRUCTION — the
       PMC import sits in try/except, so it **passes in exactly the state it exists to detect.** That is an
       ANTI-control: it reports healthy BECAUSE the fallback engaged. The `calendar_source` assertion
       REPLACES it. This is an assertion inside existing scope — **NOT an alarm or monitor.**

    6. CONDITIONAL IMMUTABLE WRITES. Build in memory or `/tmp` and VALIDATE BEFORE ANY S3 MUTATION. Identical
       bytes → `unchanged`. Same-date different-bytes → `conflict`, recorded in the manifest, **NEVER a
       silent overwrite.** A duplicate invocation is a no-op.

    7. `_aggregate_aua` EQUIVALENCE PROVEN WITH A MUTANT. Compare against the incumbent on identical inputs
       after stripping only explicitly volatile process fields, then MUTATE one load-bearing source value and
       prove the comparison FAILS AND LOCALIZES the affected firm/global feature.
       ⚠ `trading_day_calendar` IS ON AN EXPLICIT NEVER-STRIP LIST. Doc 02 says strip "process/provenance"
       fields, and that field IS provenance by name and shape — **so doc 02's own instruction points at
       deleting the one signal that discriminates the two runtimes.** Named in the spec, not remembered.
       ⚠ Install `pandas_market_calendars<5` in ANY environment producing a QA-comparison artifact: pmc is
       NOT importable on site Z, so a fallback build validates a configuration that will never ship.

    8. COTTONWOOD BUILDS BEFORE GLOBAL, and the declared L1 preparation runs before the Cottonwood spine.
       Assert global is invoked EXACTLY ONCE. Order within the family: backfill → slice → spine.

    9. **PER-SCOPE OUTPUT, AND THE ACCEPTANCE ASSERTS THE 12 OBJECTS — NEVER THAT THE BUILDER RAN.**
       Andrew-ruled: `platinum/mdpf/{scope}/` × `{aggregate-aua-timeseries, aum-metrics,
       account-distribution}.json` for all four scopes = **12 FILES EVERY SINGLE DAY.** The gold path this TO
       builds must produce, per scope, the inputs that make those 12 emittable.
       **12 IS A DAILY COMPLETENESS DENOMINATOR** — a cycle producing fewer is INCOMPLETE, not quiet.
       FORBIDDEN SHORTCUT, NAMED: this is the governing outcome-not-intervention criterion applied to the
       daily contract. **Acceptance asserts THE OBJECTS EXIST FOR THE DAY. It does NOT assert "the builder
       ran," "no exception was raised," or "12 writes were attempted."** A build that runs cleanly and emits
       11 has failed this criterion; a report of "12 written" whose sources are all unchanged from yesterday
       has not satisfied it either (see criterion 6's conditional-write semantics).
    9a. **CANONICAL SHAPE ACROSS SCOPES, VERIFIED PER FIELD — NOT PER SCOPE.** Each artifact type has ONE
       schema; all four scopes emit it, folded fields included, with honest absence where a scope has no
       data.
       FORBIDDEN SHORTCUT, NAMED: **DO NOT EMIT `account_units` ONLY ON COTTONWOOD OR NON-MODEL FIELDS ONLY
       ON GLOBAL.** That reproduces the scope-specific schema the ruling removes, and it would pass any
       check written as "cottonwood carries its count." Assert THE FIELD IS PRESENT ON ALL FOUR, and that a
       data-less scope carries honest absence — **NEVER zero, never omitted.**
       ⚠ **AND DO NOT PATCH SHAPE ANYWHERE DOWNSTREAM.** Vendor divergence dies in GOLD. If a shape
       difference survives into platinum, the defect is in this TO's output — fix it here.

    9b. **THE EXTRAS RETIRE ONLY AFTER THE FOLD IS VERIFIED.** `cottonwood/account-units.json` and
       `global/non-model-assets.json` were written by this morning's live publisher cycle — **they are
       CURRENT output, not residue.**
       FORBIDDEN SHORTCUT, NAMED: do not retire them in the same act that introduces the folded fields.
       **NOTHING STOPS BEFORE ITS REPLACEMENT IS PROVEN** — the folded count and non-model fields must be
       demonstrably correct in the canonical 12 first. Same shape as DEPLOY-BEFORE-ENV: the ordering is
       correctness, not preference, and the version that feels tidier is the one that loses data silently.

    10. STANDARD DS CRITERIA: `comp-validate <script> --artifact /tmp/<artifact>.json` exits 0;
        `comp-pipescript deployed <script>` shows MATCH after upload.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="modify">data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py</file>
      <file action="modify">data/mdpf/scripts/gold/dim_mdpf_account_distribution.py</file>
      <file action="modify">data/mdpf/scripts/gold/dim_mdpf_aum_metrics.py</file>
      <file action="modify">data/mdpf/scripts/gold/dim_mdpf_non_model_assets.py</file>
      <file action="modify">data/mdpf/scripts/gold/mdpf_aggregate_aua.py</file>
      <file action="modify">data/mdpf/scripts/gold/build_mdpf_spine.py</file>
      <file action="modify">data/assets/scripts/gold/build_cottonwood_mdpf_slice.py</file>
      <file action="modify">data/assets/scripts/gold/build_cottonwood_mdpf_pair.py</file>
      <file action="modify">data/assets/scripts/gold/build_cottonwood_interpolated_backfill.py</file>
      <file action="delete">data/mdpf/scripts/gold/_trading_day_calendar.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">One firm-parameterized path; global a fold invoked exactly once.</requirement>
    <requirement id="2">Per-scope exceptions ADDED; both the raise and the absence exercised.</requirement>
    <requirement id="3">Both roster readers fail closed, proven by one test each from the built artifact.</requirement>
    <requirement id="4">Bind lib/trading_calendar; retire the shim and both inlined privates.</requirement>
    <requirement id="5">Cottonwood family moves in the SAME atomic unit — never a following commit.</requirement>
    <requirement id="6">Validate before any S3 mutation; conditional writes; conflict never overwrites.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">The atomic refactor across both trees, committed to your lane on SITEZ (push is MSTR~Z's, :55-:00)</deliverable>
    <deliverable type="document">Equivalence + channel-independence + calendar tie-out results, each with denominators</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <rule>DO NOT LAND THE MDPF REFACTOR AND FOLLOW WITH A COTTONWOOD COMMIT. The window between them is the
    breakage and nothing in the mdpf tree signals it.</rule>
    <rule>DO NOT ADD A GRACEFUL FALLBACK TO EITHER ROSTER READER. It would read as an IMPROVEMENT in review
    — a hardening change and a silent-degradation change look identical in a diff.</rule>
    <rule>DO NOT TREAT FLAT LAYOUT AS THE ROSTER FIX. It masks `return 3`; it does not remove it.</rule>
    <rule>DO NOT STRIP `trading_day_calendar` in the equivalence comparison. Doc 02's instruction points at
    deleting the discriminating field.</rule>
    <rule>DO NOT ACCEPT AN IMPORT-HEALTH PASS as evidence PMC is present — the import is in try/except.</rule>
    <rule>DO NOT touch the vendored calendar copies in bd-served-vintage-alarm, inf-etf-ownership-daily, or
    opal-assets-absence-check. Other pipelines.</rule>
    <rule>DO NOT PRESERVE `platinum/mdpf/aggregate_aua/` as a contract — 444 objects archived @4a2651063.</rule>
    <rule>DO NOT RE-PATH the multi-partner document unilaterally. Pending Andrew.</rule>
    <rule>DO NOT MOVE, RENAME, OR CLEAN UP SERVED FIELDS. Seven as-of families are facts (H6). The
    hyphenated `account-distribution.json` bell is untouchable.</rule>
    <rule>NO NEW GATES. NO SHADOWS — no parallel producer, no shadow prefix, no standing comparator; finite
    QA only. NO ALARMS, SNS TOPICS, SES SENDS, FRESHNESS CHECKERS, OR MONITORS.</rule>
    <rule>NEVER call a feed stale without resolving the TRADING CALENDAR first, in TRADING DAYS. Per-feed
    cadence is NOT one shared date. Schwab account `08242234`, EIGHT digits, never `08335338`.</rule>
    <rule>DO NOT use the shared dirty checkout as build input. Never rebase on SITEZ. Commit to your lane;
    push is MSTR~Z's at :55-:00. Working files in the scratchpad.</rule>
  </do_not>
</task_order>
