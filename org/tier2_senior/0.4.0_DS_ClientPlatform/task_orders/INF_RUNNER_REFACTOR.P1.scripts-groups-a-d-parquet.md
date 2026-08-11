# TO INF_RUNNER_REFACTOR.P1 — PHASE 1 SCRIPTS: the Inflection gold analytics runner, Groups A–D + parquet writer-format

<task_order>
  <metadata>
    <to_id>INF_RUNNER_REFACTOR.P1.scripts-groups-a-d-parquet</to_id>
    <project>INF_RUNNER_REFACTOR</project>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued>2026-08-11</issued>
    <status>active</status>
    <gate>1.0.0_SA_CTO</gate>
    <verifier>3.0.0_SA_CVO</verifier>
  </metadata>

  <objective>
    Build PHASE 1 (SCRIPTS) of the INFLECTION gold analytics runner — Groups A–D + the parquet
    writer-format — by TRANSPOSING the 49F archetype shape onto the INF field sourcing. Runs in
    PARALLEL with DS base's 49F P1. Andrew-launched ~0924Z 2026-08-11 (his word at the CTO terminal,
    verbatim: "Ok I'm instantiating ~A now, let COO know").
  </objective>

  <context>
    ISSUANCE NOTE: dispatched by broker message at 092643Z, minutes ahead of this file, because
    Andrew instantiated the lane in real time and an EMPTY INBOX AT BOOT is worse than a TO that
    trails by minutes. This is a deliberate ordering, not the 49F failure repeated — on that lane the
    TO file was never written at dispatch at all (see MDPF_49F_BUILD.P1's own context block).

    PHASE ORDER (Andrew-direct @4dbf4a0d7c, SEQUENTIAL — each phase gates the next):
      P1 SCRIPTS -> P2 TIMING -> P3 REPOINTS -> P4 PUBLISHERS -> P5 DECOMMISSION
    THIS TO IS P1 ONLY.

    SHAPE-TRANSPOSITION DOCTRINE (Andrew-direct @6e180df78e): instantiate the shape by SOURCING
    FIELDS (RAW / MANUFACTURABLE-as-named-computation / ABSENT-with-shape), NEVER by porting 49F
    code. The field contract + script sequence are the shape; the code is not.

    WHY THIS LANE EXISTS: DS base is saturated — 49F P1 B-4/B-5a plus four armed deploy timers — so
    INF work handed to base queues behind the 49F build and three deploy windows. Parallel is the
    only way INF moves today. CTO's positioning read + COO's capacity half, synthesized to Andrew
    092331Z; he launched on it.

    ADMISSION CRITERION, STANDING: EXTRACT-side only. A build admitting anything from the quality
    partition's DISCARD side is a patch by construction, and "no patches" is his word on the archetype.
  </context>

  <compiler_tools_mandate>
    comp-validate per gold script; comp-pipescript deployed for MATCH after any S3 upload.
    MEASURED INSTRUMENT BOUNDARY: comp-pipescript deployed EXCLUDES bundle-routed scripts and
    under-reports multi-homed ones without its DENOMINATOR line read — never accept a deploy on
    MATCH alone (it returned MATCH while executing code was 4 days stale, 2026-08-11).
    Run proof-of-spec-check WITHOUT A PIPE: a piped rc is the pipe's, not the validator's.
  </compiler_tools_mandate>

  <acceptance_criteria>
    Acceptance is NOT authored here. THE PER-GROUP ACCEPTANCE BATTERIES IN THE GOVERNING SPECS ARE
    THE BAR:
      INF shape spec — org/tier1_exec/4.0.0_SA_CRO/deliverables/ADVREVIEW_49F_ABCD_AND_INF_SHAPE_SPEC_20260811.md @75db88d716
      The SHAPE (ruled 49F group specs) — A @9c294bbf15+@6fba62393b · B @d57bbf7229 ·
      C @39c41163cd+@f882b91ce2 · D @1e11389af8
    Plus, per Andrew @4dbf4a0d7c: STAGE-BY-STAGE compile verification (py_compile per stage), not a
    single pass at the end.
  </acceptance_criteria>

  <proof_of_spec>
    <instance_path_grammar>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_INF_{GROUP}_{YYYYMMDD}.json</instance_path_grammar>
    <criterion_id_grammar>INF-{group}-{artifact}-{check}</criterion_id_grammar>

    <group id="A" status="MINTED" minted_by="0.4.0_DS_ClientPlatform~A" minted_at="2026-08-11T094xZ" battery_source="SPEC_49F_GROUP_A_DIMENSIONS_20260811.md §5 (@9c294bbf15+@6fba62393b) transposed per INF shape spec Commission 2 Group A (@75db88d716)">
      <criterion id="INF-A-A00-ROWCOUNT">dim_account row count == accounts_v2 distinct account_id on the same partition; denominators printed</criterion>
      <criterion id="INF-A-A00-PREDICATE">universe = DERIVED rep-scope predicate (one home, from the representatives dim / ruled rep set), never INFLECTION_REP_IDS; zero hardcoded rep-allowlist constants in runners_inf; a rep add/reassignment at Orion changes NO code</criterion>
      <criterion id="INF-A-A01-MAPCENSUS">mapped + unmapped == A_00 universe total (ADVREVIEW F-5); disposition enum SELF-FAMILY/EXCLUDED-LOUD present; denominators printed</criterion>
      <criterion id="INF-A-A02-DISJOINT">COLLECTION_ACCOUNT set disjoint from IN_CLIENT_BOOK; detection outcome DECLARED: nonempty via the advisory-fee-flow named computation OR collection_detection=ABSENT-with-shape (the INF spec's own ELSE branch -- never guessed)</criterion>
      <criterion id="INF-A-A02-VERSION-DET">boundary_version stable across two same-input runs (determinism control)</criterion>
      <criterion id="INF-A-A02-VERSION-MUT">a mutated input flips boundary_version (mutant control)</criterion>
      <criterion id="INF-A-A03-ROWCOUNT">dim_security row count == source distinct security identifiers; denominators printed</criterion>
      <criterion id="INF-A-A04-GAPCENSUS">gap census printed with the trading-calendar frame (lib/trading_calendar.py JOIN vs the canonical-holdings partition tree); weekends/holidays NEVER gaps (T-1 law); a partition on a non-trading day = DECLARED STATEMENT-DAY class, never promoted; any TRUE gap NAMED</criterion>
      <criterion id="INF-A-A05-RESOLVE">every transTypeId on the freshest silver/transactions partition resolves through ref_txn_classification or lands UNRESOLVED-LOUD; 0 silent rows; denominator = partition row count</criterion>
      <criterion id="INF-A-A05-CENSUSKEY">the classification table's census key re-derives from the FULL-series transTypeId census (46-code universe, never a window sample)</criterion>
      <criterion id="INF-A-A06-COVERAGE">crosswalk coverage ratios printed with BOTH denominators (spine-side and per-dim side); near-identity expectation stated</criterion>
      <criterion id="INF-A-ALL-PROVENANCE">provenance cols (source_pipeline, _ingested_at) present on every Group A artifact (atom 9)</criterion>
      <criterion id="INF-A-ALL-MANIFEST">atom-3 manifest written per artifact ({data-as-of}/{process-ts}); boundary_version stamped where consumed</criterion>
      <criterion id="INF-A-ALL-COMPILE">stage-by-stage py_compile pass logged per script at its build stage (Andrew @4dbf4a0d7c), not one end pass</criterion>
      <judgment_calls>
        (1) The 49F A_02 battery bullet is THREE independently-checkable rows (disjoint/determinism/mutant) -- split per the issuance grammar. (2) 49F's "collection set NONEMPTY" relaxes to DECLARED-nonempty-or-ABSENT-with-shape because the INF spec itself names the ELSE branch (the FRM-leg discriminator does not transpose; Orion is not Schwab's ledger). (3) A_03 gains a ROWCOUNT row by extension of §5's first bullet (its parenthetical is exemplary, not exclusive). (4) The two-calendar STATEMENT-DAY amendment folds into INF-A-A04-GAPCENSUS as a declared class rather than a separate id (one check, one frame). (5) "ALL" artifact-token rows carry the cross-artifact atoms (provenance/manifest/compile) promoted from §5's closing bullet. (6) INF-A-A00-PREDICATE added from the INF spec's own Group-A precondition (the 28-site allowlist is the fork's measured breaker; retirement of LEGACY call sites is W-C/P3 scope -- THIS row binds the NEW runners only).
      </judgment_calls>
    </group>
    <group id="B" status="MINTED" minted_by="0.4.0_DS_ClientPlatform~A" minted_at="2026-08-11T101xZ" battery_source="SPEC_49F_GROUP_B_VALUATION_20260811.md §5 (@d57bbf7229+@39c41163cd) transposed per INF shape spec Commission 2 Group B (@75db88d716)">
      <criterion id="INF-B-B00-ROWCOUNT">B_00 row count == dim_boundary IN_CLIENT_BOOK count on the partition; denominators printed</criterion>
      <criterion id="INF-B-B00-FVIDENTITY">fair_value == ending_mv + accrued_income exactly (identity control; accrued_income 0.0-by-construction at INF, retained for uniform shape)</criterion>
      <criterion id="INF-B-B00-SPOTTIE">one KNOWN account's V(t) spot-ties the raw silver activity partition (positive control)</criterion>
      <criterion id="INF-B-B00-ZEROSTATUS">every ending_mv==0.00 row carries a MEASURED value_status discriminator: ZERO-CONTRADICTED-BY-POSITIONS (the 3y-window/parse artifact class) vs ZERO-CORROBORATED (true empty) -- vendor-absent never silently reads as vendor-zero</criterion>
      <criterion id="INF-B-B01-SUMTIE">SUM(B_01 current_value) per account vs B_00 V(t) within the B_03 tolerance on a SAME-VINTAGE sampled partition; denominators AND vintages printed</criterion>
      <criterion id="INF-B-B01-FLAGS">vendor-field-only quality flags present (zero_price_flag, zero_qty_nonzero_mv_flag, vendor status/recon fields carried); the interpolated price tier (canonical_prices T3/T4) is DISCARD-class and structurally absent from B_01's inputs</criterion>
      <criterion id="INF-B-B01-INOUT">zero rows silently dropped: in == out + declared exclusions</criterion>
      <criterion id="INF-B-B02-NABYCONSTRUCTION">the accrual artifact LANDS carrying the N/A-BY-CONSTRUCTION verdict + grounding (vendor-valued positions; accrual embedded in marks) -- uniform shape, honest cell</criterion>
      <criterion id="INF-B-B03-CENSUS">recon_status census printed per run (TIE / VARIANCE-EXPLAINED / VARIANCE-UNEXPLAINED / VINTAGE-SKEW-DECLARED) at the 1bp ex-ante PROVISIONAL tolerance with the ruled-recalibration clause carried verbatim</criterion>
      <criterion id="INF-B-B03-DET">determinism across two same-input runs</criterion>
      <criterion id="INF-B-B03-MUT">a poisoned position value lands VARIANCE-UNEXPLAINED, never TIE (mutant control)</criterion>
      <criterion id="INF-B-ALL-PROVENANCE">provenance cols (source_pipeline, _ingested_at) on all four artifacts (atom 9)</criterion>
      <criterion id="INF-B-ALL-MANIFEST">atom-3 manifest per artifact; boundary_version (A_02) stamped on all four</criterion>
      <criterion id="INF-B-ALL-COMPILE">stage-by-stage py_compile logged per script at its build stage</criterion>
      <judgment_calls>
        (1) ZEROSTATUS ADDED from measured substrate truth: activity.ending_mv==0.00 on 422 of 907 accounts, 312 CONTRADICTED by nonzero positions ($68.3M) -- the MSTR-source-confirmed 3y-window Activity artifact (@dbddd3fe52); the FIX CHOICE stays at CTO+COO, this row only forbids silent conflation. (2) VINTAGE-SKEW-DECLARED added to the B_03 enum: the activity dim lags positions_mv by a day at census time; a cross-vintage tie is a FALSE variance, so the tie computes on matching vintages and DECLARES skew otherwise. (3) B_02's 49F materiality-gate battery rows (both-denominator read, census key, mutant-flips-number) are N/A-BY-CONSTRUCTION at INF per the shape spec's own cell -- replaced by the lands-with-verdict row. (4) B_00's FVIDENTITY retained though degenerate (accrued_income==0.0 by construction) -- uniform shape across firms is the point. (5) 49F B_00's cash/sweep/margin decomposition columns do NOT exist in the INF activity dim (window aggregates only, _3y-suffixed) -- carried content-named, absence of the decomposition DECLARED, never fabricated.
      </judgment_calls>
    </group>
    <group id="C" status="NOT_YET_MINTED"/>
    <group id="D" status="HOLD_FOR_RULING" ruling_event="at ~A's Group-C completion" ruling_inputs="DS base's B-4 emitter outcome + ~A's C-completion" deciders="Andrew + 1.0.0_SA_CTO + 2.0.0_SA_COO"/>
    <group id="PARQUET-WRITER-FORMAT" status="MINTED" minted_by="0.4.0_DS_ClientPlatform~A" minted_at="2026-08-11T094xZ" battery_source="pattern spec §1 grammar (@d272021791) + SPEC_49F_GROUP_B §1 FORMAT clause (@39c41163cd vintage) + TO requirement 5">
      <criterion id="INF-PQW-WRITER-GRAMMAR">every gold artifact write emits {table}/date={D}/data.parquet under the silver partition grammar (one grammar, three tiers)</criterion>
      <criterion id="INF-PQW-WRITER-PARQUET">the writer's output format is PARQUET only -- JSON is structurally impossible through the gold writer (JSON leaves the gold tier; publishers are P4)</criterion>
      <criterion id="INF-PQW-WRITER-NOROOT">the writer carries NO decided product root -- the destination root is injectable (P3's act); any forced path constant is NAMED in the instance's surprises, not decided (F-1 stays Andrew's)</criterion>
      <criterion id="INF-PQW-WRITER-MANIFEST">the writer emits the atom-3 manifest ({data-as-of}/{process-ts}.json) beside every table write</criterion>
      <judgment_calls>Group token PQW in criterion ids for brevity; the instance FILE keeps the TO's literal group id: PROOF_OF_SPEC_P1_INF_PARQUET-WRITER-FORMAT_20260811.json. The writer battery is minted WITH Group A because the writer is the harness A builds on -- stated so the co-mint is not read as a per-group skip.</judgment_calls>
    </group>

    <!--
    THE ID SETS ARE DELIBERATELY UNMINTED BY THE ISSUER. The COO has NOT read the INF batteries and
    will not hand the assignee invented id strings — a wrong id list validates STRUCTURALLY and
    proves the wrong thing. Each group's set is enumerated FROM ITS OWN BATTERY at that group's
    start, by the surfaced-not-guessed method (judgment calls stated: a multi-part bullet split into
    independently-checkable rows; a promoted artifact-table row), and appended here at next touch.
    An ambiguous battery SURFACES rather than guesses.

    THE THREE ISSUANCE GRAMMARS above are bound BEFORE the first mint (CTO 092331Z, adopted
    fabric-wide). All three were earned from defects in the 49F lane the same hour:
      (1) per-group instance paths — the 49F TO declared ONE path matching none of three landed
          instances; a completion flip on it would have read absence as work-not-done.
      (2) firm-tokened criterion ids — 49F minted A5-/B5-/C5- with no firm token, and CVO's cert
          step-zero reads ACROSS instances, so verbatim battery transposition would collide.
      (3) UNCOMPUTABLE-with-declaration PRE-AUTHORIZED — a by-construction-impossible row must never
          force a choice between a faked PASS and a stall.

    TWO-LAYER DIVISION (unchanged): the validator catches the ASSIGNEE omitting against this list;
    CVO's cert-of-built step-zero catches THIS LIST omitting against the governing SPEC.
    Per-group validation:
      python .tools/proof-of-spec-check.py {instance}.json {that group's ids}
    NOTE the issuance lint (.tools/git-hooks/to-proof-of-spec-check.sh:29) is a PRESENCE grep on NEW
    files only — it binds issuance PRESENCE, never issuance CORRECTNESS. It cannot catch a
    well-formed element naming a nonexistent path. Do not read its pass as a check of this block.
    -->
  </proof_of_spec>

  <scope>
    <files>
      <file action="modify">data/inf/scripts/gold/runners_* (Groups A–D per the transposed specs)</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/PROOF_OF_SPEC_P1_INF_{GROUP}_20260811.json (one per group)</file>
      <file action="reference">the INF shape spec + the four ruled 49F group specs at the commits above</file>
    </files>
    <tree_boundary>
      TWO AGENTS ARE IN THE inf TREE. Firm separation separates inf from bd/cot; it does NOT separate
      two agents inside inf.
      ~A OWNS: data/inf/scripts/gold/runners_*
      BASE RETAINS: data/inf/scripts/silver/build_billing_dim.py — two live queued defects
        (BILLING_COLUMN_MAP keys miss the real vendor headers, so silver silently drops every period
        column; parse_dollar(empty)->0.00 conflates vendor-absent with vendor-zero, understating firm
        fee-earning AUA ~30%). ~A DOES NOT TOUCH THAT FILE. If ~A's work reads ending_mv, a 0.00 there
        is a PARSE ARTIFACT, not a vendor zero.
      SHARED TOUCHPOINTS (safe_deploy_core second-targets row, lib/): already batched acts with
        owners — one comp-blast pass before touching either.
    </tree_boundary>
  </scope>

  <requirements>
    <requirement id="1">Group A — transposed by FIELD SOURCING, not code port.</requirement>
    <requirement id="2">Group B — valuation canonicals.</requirement>
    <requirement id="3">Group C.</requirement>
    <requirement id="4">Group D emitters — **HOLD FOR RULING, sovereign-explicit.** SCOPE THIS LANE A -> B -> C.
      Andrew-direct 2026-08-11 ~0928Z, VERBATIM: "Have ~A run through Groups A B C and by the time
      they're done we will likely have had time to assess DS Base attempt at the emitter and will come
      to a conclusion on how ~A should proceed to that end."
      THIS IS NOT A PASSIVE WAIT-ON-B-4 — it is a NAMED RULING EVENT with named inputs:
        RULING EVENT: at ~A's Group-C completion.
        INPUTS:       DS base's B-4 emitter outcome + ~A's C-completion.
        DECIDERS:     Andrew + CTO + COO. Outcome may be adopt-the-mechanic-verbatim, amend, or other.
      Consequence for the lane: NOBODY IDLES AND NOBODY FREELANCES AN EMITTER. ~A does not build D and
      does not pre-decide its shape; ~A reports C-completion, which is what FIRES the ruling.
      (This upgrades COO's D-wait default — which Andrew did not overrule — to sovereign-explicit.)</requirement>
    <requirement id="5">Parquet writer-format: {table}/date={D} — WRITER FORMAT ONLY.</requirement>
    <requirement id="6">Evidence captured AS THE WORK PROCEEDS, never retro-fitted. An instance assembled afterwards is weaker even when every field is filled, because the evidence was selected knowing the answer.</requirement>
    <requirement id="7">06_current_state recompiles: ONCE PER WAVE at wave close, NOT per group; route to the COO exec lane per the @7f5a958bdf precedent. Three lanes recompiling one governance artifact per group would race it under a single owner — a governance-artifact collision that a comp-blast over data trees structurally cannot see.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="commit">Groups A–C + parquet writer-format, stage-by-stage compile-verified (D on its wait's release)</deliverable>
    <deliverable type="document">A schema-valid PROOF_OF_SPEC instance per group, passing proof-of-spec-check with its POSITIONAL id set (comma list or a one-id-per-line file; there is NO --expected-criteria flag -- the flagged form exits rc=2)</deliverable>
    <deliverable type="document">Session log with Compiler Tools section</deliverable>
  </deliverables>

  <do_not>
    <item>Do NOT start P2 (timing), P3 (repoints), P4 (publishers) or P5 (decommission) from this TO.</item>
    <item>Do NOT RESOLVE THE F-1 ROOT QUESTION. The spec's own F-1 finding is that the default product root EXTENDS a measured-non-conforming tree against Rule 17b's ratified {vendor}/{firm}/{medallion} grammar. Minting a new root is a Rule 24 TAXONOMY ACT and 17b ratified direction WITHOUT migration authority — it is Andrew's, not a builder's. P1 is the writer FORMAT; the DESTINATION is P3. If code forces a path constant, name it in the instance's `surprises`, do not decide it.</item>
    <item>Do NOT port 49F code. Source the fields.</item>
    <item>Do NOT touch data/inf/scripts/silver/build_billing_dim.py (base's queued defects).</item>
    <item>Do NOT chase the .parquet object under s3://opal-data-inf/bronze/orion-api-v2/ — a live Rule-17a specimen routed to the P3 family by CTO. Leave it.</item>
    <item>Do NOT admit anything from the quality partition's DISCARD side.</item>
    <item>Do NOT accept a deploy on comp-pipescript MATCH alone — read its DENOMINATOR line.</item>
    <item>Do NOT guess a criterion id. Surface an ambiguous battery instead.</item>
    <item>Do NOT hold work on a finding and do NOT manufacture an approval step. No gate exists on this lane that is not named in this TO.</item>
  </do_not>
</task_order>
