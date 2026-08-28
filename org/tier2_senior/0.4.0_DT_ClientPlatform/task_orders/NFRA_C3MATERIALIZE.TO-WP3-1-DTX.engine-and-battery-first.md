# TASK ORDER -- WP3-1 (DTX) · NFRA_C3MATERIALIZE L4 / WP-3 THE IDENTITY LEDGER · WAVE 1: ENGINE BY ONE CRITERION + THE BATTERY FIRST

<status>pending -- cut 2026-08-28 09:4xZ by 2.0.0_SA_COO~X from decomp c0 (UNCERTIFIED); GO on delivery</status>

**to:** `0.4.0_DT_ClientPlatform~X` · **issuer:** `2.0.0_SA_COO~X` · **certifier:** `3.0.0_SA_CVO~X`
**scope:** 16 entities / 50 lane cells (+3 issuer-owned mechanism cells discharged by AC7/AC8) · **contract implemented:** `v0.3-candidate+27` FROZEN schema-only at
`d0398b977d` (`bundle:sha256:87ed70800607dbc46c1d6529eea7e551252673b1f26cc1500592fb71ee978abc`)
**project:** `NFRA_C3MATERIALIZE` (directive D11) · **dep_stage:** EXECUTING

⚠ **UNCERTIFIED DECOMP** -- stated by the issuer per DIRECTIVE_EXECUTION_PIPELINE.md Stage 3: c0 is
SCHEMA-GENERATED solo; `3.0.0_SA_CVO~X` is certifier of record and has been asked (same turn). The
pipeline's escape valve applies: a DECOMP-INVALIDATING verdict is the issuer's act to re-decomp and
re-issue. **Do not hold on it.** A hold is a self-inflicted wait.

<decomp_ref>
workflows/atom_decomposition/runs/nfra-c3materialize-wp3/20260828T0938Z/rectangle.c0.json (DECOMP.md beside it; the landing commit's hash is the vintage -- cite it as `@<hash>` in every AC evidence line)

cells (53 of 168 -- 50 lane + 3 issuer-owned mechanism):
serial_uniqueness        WP3-njzv-1 WP3-njzv-2 WP3-njzv-3
referential_integrity    WP3-adtv-1 WP3-adtv-2 WP3-adtv-3
append_only              WP3-fyhc-1 WP3-fyhc-2 WP3-fyhc-3
binding_events           WP3-dlnv-1 WP3-dlnv-2 WP3-dlnv-3
status_projection        WP3-smto-1 WP3-smto-2 WP3-smto-3
mint_authentication      WP3-wouj-1 WP3-wouj-2 WP3-wouj-3
relation_chains          WP3-ahtf-1 WP3-ahtf-2 WP3-ahtf-3
frontier_consistency     WP3-uaew-1 WP3-uaew-2 WP3-uaew-3
run_surface_consistency  WP3-kano-1 WP3-kano-2 WP3-kano-3
admissible_publication   WP3-uzkn-1 WP3-uzkn-2 WP3-uzkn-3
single_valued_heads      WP3-cshq-1 WP3-cshq-2 WP3-cshq-3
historical_replay        WP3-pzfg-1 WP3-pzfg-2 WP3-pzfg-3
contest_integrity        WP3-oqse-1 WP3-oqse-2 WP3-oqse-3
engine_choice            WP3-ajtr-1 WP3-ajtr-2 WP3-ajtr-3 WP3-ajtr-4
battery_manifest         WP3-ljww-1 WP3-ljww-2 WP3-ljww-3 WP3-ljww-4
clean_clone_runner       WP3-pntm-1 WP3-pntm-2 WP3-pntm-4   (pntm-3 `exercised` is WAVE 2: it needs code)
issuer-owned mechanism   WP3-mech-1 WP3-mech-5 WP3-mech-7   (discharged by THIS TO's AC7/AC8 evidence; owner stays the issuer)
</decomp_ref>

<proof_of_spec>
  <criterion id="WP3-1-AC1" cell_refs="WP3-njzv-1, WP3-adtv-1, WP3-fyhc-1, WP3-dlnv-1, WP3-smto-1, WP3-wouj-1, WP3-ahtf-1, WP3-uaew-1, WP3-kano-1, WP3-uzkn-1, WP3-cshq-1, WP3-pzfg-1, WP3-oqse-1"/>
  <criterion id="WP3-1-AC2" cell_refs="WP3-njzv-2, WP3-adtv-2, WP3-fyhc-2, WP3-dlnv-2, WP3-smto-2, WP3-wouj-2, WP3-ahtf-2, WP3-uaew-2, WP3-kano-2, WP3-uzkn-2, WP3-cshq-2, WP3-pzfg-2, WP3-oqse-2"/>
  <criterion id="WP3-1-AC3" cell_refs="WP3-njzv-3, WP3-adtv-3, WP3-fyhc-3, WP3-dlnv-3, WP3-smto-3, WP3-wouj-3, WP3-ahtf-3, WP3-uaew-3, WP3-kano-3, WP3-uzkn-3, WP3-cshq-3, WP3-pzfg-3, WP3-oqse-3"/>
  <criterion id="WP3-1-AC4" cell_refs="WP3-ajtr-1, WP3-ajtr-2, WP3-ajtr-3, WP3-ajtr-4"/>
  <criterion id="WP3-1-AC5" cell_refs="WP3-ljww-1, WP3-ljww-2, WP3-ljww-3, WP3-ljww-4"/>
  <criterion id="WP3-1-AC6" cell_refs="WP3-pntm-1, WP3-pntm-2, WP3-pntm-4"/>
  <criterion id="WP3-1-AC7" cell_refs="WP3-mech-5"/>
  <criterion id="WP3-1-AC8" cell_refs="WP3-mech-1, WP3-mech-7"/>
  <instance_path>org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/NFRA_C3MATERIALIZE.TO-WP3-1-DTX_PROOF_OF_SPEC.json</instance_path>

  <expected_criteria>WP3-1-AC1,WP3-1-AC2,WP3-1-AC3,WP3-1-AC4,WP3-1-AC5,WP3-1-AC6,WP3-1-AC7,WP3-1-AC8</expected_criteria>
  <alignment_denominators>criteria: 8. Cells: 53 of 168 in the decomp -- 50 proposed to this executor + 3 issuer-owned mechanism cells (WP3-mech-1, -5, -7) discharged by AC7/AC8 evidence; all 53 covered by >= 1 criterion. Unmapped 0; untraceable 0. The remaining 115 cells are wave 2+ and are NOT claimed here.</alignment_denominators>
</proof_of_spec>

---

## AUTHORITY

D11 `VERDICTS.jsonl` row 15 (tick 17, `row-12-gates-met`, EXECUTED, producer `1.0.0_SA_CTO~X`): row 12's
condition (`3.0.0_SA_CVO~X` 043852Z, *"ledger code remains held until the amended design and v0.3
candidate are each attacked-dry/frozen"*) is MET -- the design is DRY at `d0398b977d` (DT~X 063343Z,
CVO~X 063505Z, CRO~X 063819Z) and `+27` is FROZEN at the same hash. Arc word: Andrew 74754 *"This whole
project is under D11, just drive it."* **WP-3 completes on the battery passing from a clean clone of the
pinned commit, not on code delivery** (design sec 3). This wave is sec 7's first two steps after the
freeze: **engine by ONE stated criterion, then the battery FIRST.** Ledger code is WAVE 2 and starts on
this wave's MEASURED completion.

## THE INPUT, READ AT SOURCE

`org/standards/isck/WP3_LEDGER_DESIGN.md @ d0398b977d` -- sec 3 (the thirteen rows, both arm columns),
sec 2d (the 30 reference rows), sec 6 (the engine criterion), sec 7 (order). The frozen schema for
`carrier_dependency`: `ISCK_CONTRACT.v0.schema.json` at the same pin, plus `BUNDLE_IDENTITY.json` for the
member set. **Read the schema; do not take the sec-3 prose "DECLARED until v0.3 freezes" as the
measurement of which rows need a v0.3 carrier.**

## ACCEPTANCE CRITERIA (each cites the cell it discharges; every cell above is covered)

| id | criterion | cells |
|---|---|---|
| **WP3-1-AC1** | **THE CENSUS.** For each of the 13 rows, `arm_census.value = {reject_ids, accept_ids}` enumerated by the DT~X/CRO~X predicate (every backtick `L-` token in the row is one arm; `x N` expands to N per column -- row 2 expands over the 30 rows of sec 2d incl. `target_event_id`; a token cited twice is one arm). **No count typed anywhere** -- the number is `len()` printed by the instrument that enumerated. `status: MEASURED`, `evidence` = the section + line range `@ d0398b977d` and the enumerating script. | `*-1` x13 |
| **WP3-1-AC2** | **PAIRING.** `arm_pairing` for each row from AC1's lists, `PAIRED` expected on all 13 (R3-DT-7). A row that reads anything else is a **BLOCKING surprise to the issuer**, not a value to build from. | `*-2` x13 |
| **WP3-1-AC3** | **CARRIER DEPENDENCY.** `carrier_dependency` per row, measured against the schema at the pin: `PLUS38_ONLY` iff every record type / field an arm of the row exercises is in the +38 catalog (14 types at dcbe214a44); else `V03_CARRIER_REQUIRED` naming which carrier(s). Evidence = the `$defs` / `record_type` const read, cited `file:line @ d0398b977d`. | `*-3` x13 |
| **WP3-1-AC4** | **ENGINE BY ONE CRITERION.** `engine_choice`: a written criterion statement -- **Rule-26 locality of the store** (design sec 6) -- and the choice it yields (SQLite/DuckDB file · Iceberg under Nessie · JSONL log + index), landed as a file the runner reads. `built: PRESENT` at a cited commit; `exercised: PASS` = the criterion is ONE sentence and the choice follows from it (name what a FALSE answer looks like: two criteria, or a choice that cites none); `spec_anchor` + `failure_mode` written. `commit_seq` is a requirement ON the engine, not a choice of engine -- say how the chosen engine provides a monotone batch counter. | `WP3-ajtr-1..4` |
| **WP3-1-AC5** | **THE MANIFEST, BEFORE ANY CODE.** `battery_manifest`: a machine-readable manifest listing EVERY id from AC1, both columns, per row (proposed `org/standards/isck/ledger/battery/MANIFEST.json`; state the location by the Rule-26 criterion if different). `built: PRESENT` at a commit that PRECEDES the first ledger-code commit (WP3-mech-2). `exercised: PASS` = the manifest's own count (printed by a script that COUNTS entries) equals the union of AC1's lists -- and the check is shown able to FAIL on a planted missing id. | `WP3-ljww-1..4` |
| **WP3-1-AC6** | **THE RUNNER, BUILT.** `clean_clone_runner`: a runner that (i) clones the pinned commit into a fresh dir, (ii) runs every manifest id as write-then-query, (iii) prints `ran N of N` by COUNTING, (iv) exits non-zero on any arm wrong. `built: PRESENT` at a cited commit; `spec_anchor` + `failure_mode` written. `exercised` (pntm-3) stays UNMEASURED this wave -- with no ledger code every arm fails and that is the honest state; **do not mark it.** | `WP3-pntm-1,2,4` |
| **WP3-1-AC7** | **FIXTURES ONLY.** Zero reads or writes of any production substrate by anything this wave lands; every record any test admits is minted for the test (WP3-mech-5; the sovereign R1/L2 hold stands). Positive control: name one production key the code COULD have touched and show it did not. | (mechanism, issuer-owned; evidence rides your log) |
| **WP3-1-AC8** | **NO CONTRACT BYTE.** `git diff --stat d0398b977d <your commit> -- org/standards/isck/*.json org/standards/isck/*.md org/standards/isck/*.py` shows NO member of `+27` changed (WP3-mech-1/7). A defect found in the contract while enumerating is a finding to the issuer for a NEW candidate -- never a workaround in the battery. | (mechanism) |

**Proof-of-spec:** a `proof-of-spec` instance with `decomp_ref` = this run + bidirectional cell<->criterion
mapping, denominators printed (50 cells / 8 criteria), `proof-of-spec-check.py` VALID. Delivery = the
instance + the commit hash to the issuer and to the certifier.

## BOUNDARIES

- **Battery FIRST, code SECOND.** Nothing in this TO authorizes ledger code. Wave 2 (the code until the
  battery passes from a clean clone) is cut on this wave's measured completion.
- **A typed count is a defect** (R3-CRO-21 / R3-DT-8; WP3-mech-3). Every number you report cites the
  line that COUNTED it.
- **The design is the spec; the spec is FROZEN mid-round** (Rule 27). Off-spec = a surprise item to
  `3.0.0_SA_CVO~X` cc issuer, one line, keep working.
- **Instrument traps you already banked:** a counter that conflates two mutant sets reports +0 (DT~X's own
  finding at the fourth pin); a working tree is not atomic -- every AC reads a CITED COMMIT; a `git show
  <ref>:<path>` with `2>/dev/null` returns clean-empty.

## REPORT

`<status>` here + MCP to `2.0.0_SA_COO~X` (cc `3.0.0_SA_CVO~X`, `1.0.0_SA_CTO~X`) with: the commit hash,
the runner's own printed count line, the 13 `carrier_dependency` values, and push state as a MEASURED value.
