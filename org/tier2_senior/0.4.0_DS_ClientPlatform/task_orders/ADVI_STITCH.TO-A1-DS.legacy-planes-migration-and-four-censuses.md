# TO ADVI_STITCH.TO-A1-DS — PHASE A, DS lane: re-ground · declare the migration SCOPE SET · land `bronze_legacy` / `silver_legacy` / the frozen reference series · the key plane · the FOUR CENSUSES (no classes)

<task_order id="ADVI_STITCH.TO-A1-DS" project="ADVI_STITCH">
<decomp_ref>workflows/atom_decomposition/runs/advi-stitch/20260824T222500Z/DECOMP.md @3ee0bec43b — cells STI-a-1, STI-a-2, STI-a-3, STI-a-4, STI-b-0, STI-b-1, STI-b-2, STI-b-3, STI-b-5, STI-c-1, STI-c-2, STI-d-0, STI-d-1, STI-d-2, STI-d-3, STI-d-4, STI-d-5, STI-inv-1, STI-inv-2, STI-inv-3, STI-inv-4, STI-inv-5</decomp_ref>
<decomp_context>NOT in this TO and deliberately named so the exclusion is legible: the landing IAM leg (AE lane, TO-A1-AE) · the firm/account-set separation control (CVO) · every Phase-B surface (the decomp's boundary cells, which are ABSENT BY DESIGN, not dark). Reads the certified decomp's boundary cells as constraints. *(This element exists because the gate's harvest reads every cell id inside `decomp_ref` as a cell the TO CLAIMS — an exclusion clause left there is INVERTED into a claim; issuer fix, AE~G's finding.)*</decomp_context>
<certification>**CERTIFIED DECOMP** — `3.0.0_SA_CVO` @43f9aaaeee: 32/32, both symmetric differences empty, no P1; first cert carrying check 7 (oracle viability), passed on a stated sample.</certification>
<issued_to>DS-class (data plane). **Seated: a FRESH `0.4.0_DS_ClientPlatform~<letter>` for ADVI_STITCH ONLY — MSTR assigns from the audit ∪ disk occupancy. ⛔ SEATING IS STAGED, NOT IMMEDIATE: MSTR measured 15 live seats on 8 cores at 4.0 GB free and stated the posture "hold one seat and say so rather than quietly seat it and degrade everything." This TO is CUT AND READY; it does not imply a spawn tonight.**</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>MSTR's capacity call. Nothing in this TO is on another lane's critical path — Phase A gates nothing on the live 08335338 route (PRD s.3, "ultimately").</seating_trigger>
<placement>LAPTOP (Rule 26). Every read and write on this box.</placement>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-25T00:0xZ</issued>
<status>ACTIVE (seating staged)</status>
<priority>P2 — his word is "ultimately"; it gates nothing and nothing gates it.</priority>
<scope_guard>ONE PROJECT. ⛔ **NO CLASS IS ASSIGNED IN PHASE A** — R1–R4 are Phase B (s.11 #7). If a census leaves you holding data that would obviously classify an account, that is exactly the moment the rule binds. Surprises: ONE LINE by MCP to `3.0.0_SA_CVO`, cc `2.0.0_SA_COO`; CVO files under `org/surprise_channel/ADVI_STITCH/` — executing seats do not write that tree. **Nothing to `4.0.0_SA_CRO*`.**</scope_guard>
<authority>PRD `docs/architecture/ADVI_STITCH_PRD.md` v0.2 **s.11 rulings #1–#10 (FIXED)** + run S1–S12. Andrew-direct finding 2 (~17:0xZ) + the ~18:4xZ labelling ruling, verbatim: *"it really needs to be labeled properly, e.g. bronze_legacy and silver_legacy … so it is absolutely clear."*</authority>
<proof_of_spec>
  <criterion id="STIA1DS-AC1" cell_refs="STI-d-0"/>
  <criterion id="STIA1DS-AC2" cell_refs="STI-b-0"/>
  <criterion id="STIA1DS-AC3" cell_refs="STI-a-1, STI-b-1, STI-inv-2"/>
  <criterion id="STIA1DS-AC4" cell_refs="STI-a-2, STI-b-2, STI-inv-1"/>
  <criterion id="STIA1DS-AC5" cell_refs="STI-a-3, STI-b-3, STI-inv-5"/>
  <criterion id="STIA1DS-AC6" cell_refs="STI-a-4"/>
  <criterion id="STIA1DS-AC7" cell_refs="STI-c-1, STI-inv-3"/>
  <criterion id="STIA1DS-AC8" cell_refs="STI-c-2"/>
  <criterion id="STIA1DS-AC9" cell_refs="STI-d-1, STI-d-2"/>
  <criterion id="STIA1DS-AC10" cell_refs="STI-d-3, STI-d-4"/>
  <criterion id="STIA1DS-AC11" cell_refs="STI-d-5"/>
  <criterion id="STIA1DS-AC12" cell_refs="STI-inv-4"/>
  <criterion id="STIA1DS-AC13" cell_refs="STI-b-5"/>
  <expected_criteria>STIA1DS-AC1,STIA1DS-AC2,STIA1DS-AC3,STIA1DS-AC4,STIA1DS-AC5,STIA1DS-AC6,STIA1DS-AC7,STIA1DS-AC8,STIA1DS-AC9,STIA1DS-AC10,STIA1DS-AC11,STIA1DS-AC12,STIA1DS-AC13</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ADVI_STITCH.TO-A1-DS_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>cells declared: 22; criteria: 13; every criterion carries ≥1 cell_ref; every declared cell reachable from ≥1 criterion. Unmapped 0; untraceable 0. *(The remaining 10 of the decomp's 32 are the AE leg, the CVO control, the two consumer-edge cells and the six boundary cells — none of them this TO's.)*</alignment_denominators>
</proof_of_spec>
</task_order>

## ⛔ SPEC-AT-PICKUP — YOUR FIRST ACT

⛔ **AND FOR THIS TO IT IS NOT A FORMALITY: every figure below except the prefix census was inherited from the CTO run at ITS vintage, the partitions move daily, and `STI-d-0` exists precisely to re-ground them.** A Phase-A census that opens by quoting a stale count inherits its staleness silently.

| # | Premise | Oracle |
|---|---|---|
| O-1 | `opal-data-bd` holds 30 top-level prefixes; the migration's territory is FOUR | `aws s3 ls s3://opal-data-bd/` `# rail-checked: prefix presence census, the scope-set premise` |
| O-2 | The landing home does not exist yet | `aws s3 ls s3://opal-data-assets/blackdiamond/49financial/` `# rail-checked` → EMPTY (INSURE mints into the same tree — coordinate, do not collide) |
| O-3 | `dim_account_xref` newest partition, 6,201 rows, `seed-xref` 5,375 / `unresolved` 826 | live parquet read at a PINNED `date=`, stated on every output |
| O-4 | The legacy universe is 8,259 entities; 6,107 in xref; 2,152 absent | re-derived at your vintage, not quoted from the run |
| O-5 | `gold/timeseries/account_performance.parquet` is a LIVE SERVED input | `lib/s3_layout.py:181-182` + `D_00b.portal_timeseries.py` — **read only; NEVER#3** |

## THE TWO FINDINGS THAT SHAPE YOUR WORK (decomp s.2.0 — read before sizing)

1. **"MIGRATE THE BD HISTORY" IS FOUR PREFIXES OF THIRTY.** A migration scoped to a BUCKET has no denominator and its completeness can never be checked. `STI-b-0` declares the scope set BEFORE any object moves.
2. **THE KEY IS PARTIAL AND MEASURED, NOT ABSENT.** His word says the stable key is unclarified; the run measured one covering 5,310 of 7,336. So Phase A **adjudicates RESIDUES** — it does not build a key, and it assigns no class. ⛔ **The most likely way this project goes wrong is a seat that censuses the 2,152 and then, having the data in hand, classifies them. `STI-inv-4` exists to make that inexpressible in the emitted schema.**

## Acceptance criteria

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **STIA1DS-AC1** | Every inherited figure RE-GROUNDED at a pinned vintage and printed beside the run's, differences named | STI-d-0 | LIVE STATE |
| **STIA1DS-AC2** | The migration SCOPE SET committed as a declared list BEFORE the first copy; every landed key traces to a listed source prefix, both directions, denominators printed | STI-b-0 | SOURCE |
| **STIA1DS-AC3** | Raw xlsx landed under `blackdiamond/49financial/bronze_legacy/{family}/{date}/`, original filenames preserved, RAW BYTES; census equals the source census; **sha256 source == destination** on the full set | STI-a-1, STI-b-1, STI-inv-2 | EXERCISED |
| **STIA1DS-AC4** | Legacy silver copied AS-IS to `silver_legacy/{table}/date={D}/`, never re-shaped; census equals source; **path census shows 0 keys under the LIVE `bronze/` or `silver/` tiers** and a grep of live consumers for the legacy prefixes returns 0 | STI-a-2, STI-b-2, STI-inv-1 | EXERCISED |
| **STIA1DS-AC5** | The THREE BD-calculated series frozen as `gold/advi/reference/bd_legacy_*`; a re-run is a NO-OP on existing keys and REFUSES on a content difference (mutant exercised); everything else in `opal-data-bd/gold` stays put, count printed | STI-a-3, STI-b-3, STI-inv-5 | EXERCISED (mutant) |
| **STIA1DS-AC6** | The served legacy series is READ ONLY and provably untouched (its key's ETag/LastModified unchanged across your work) | STI-a-4 | LIVE STATE |
| **STIA1DS-AC7** | Every Phase-A number states the PINNED xref partition; **no competing crosswalk producer exists** (`comp-find`, denominator printed); the landed copy's `match_method` distribution equals the source's | STI-c-1, STI-inv-3 | SOURCE + LIVE STATE |
| **STIA1DS-AC8** | The renumbering field's SEMANTICS confirmed from BD's own documentation/behaviour and printed — **or an explicit UNCONFIRMED**; no MIGRATED inference either way | STI-c-2 | LIVE STATE |
| **STIA1DS-AC9** | Census of the 2,152 ABSENT (last-seen + `closedDate` per account from the legacy planes, with the count the planes cannot answer for as its own residue) and the 826 open-unmatched labelled `UNKNOWN(elsewhere-candidate)`; **ZERO DROPPED verdicts anywhere in the output** | STI-d-1, STI-d-2 | EXERCISED |
| **STIA1DS-AC10** | The 541 renumbered enumerated with old→new pairs as EVIDENCE; the Schwab-side residue split — ~209 pre-2024 unlinked vs 1,817 opened 2024-2026 — counted SEPARATELY with `date_opened` as the discriminator | STI-d-3, STI-d-4 | EXERCISED |
| **STIA1DS-AC11** | The MECE check across all four censuses closes ON THE FACE against 8,259, with the 541 shown INSIDE the 5,310 and every residue printed — nothing silently double-counted | STI-d-5 | EXERCISED |
| **STIA1DS-AC12** | ⛔ The emitted census schema contains **NO class/rule field**, and a fixture attempting one is REFUSED AT WRITE. **The oracle is the schema, not a promise** | STI-inv-4 | EXERCISED (mutant) |
| **STIA1DS-AC13** | A dry-run object count + byte total printed BEFORE the first write (~8,800 objects / ~13 GB expected); commit-gate PASS; Rule 15; proof instance VALID rc=0 positional | STI-b-5 | SOURCE |

## Law that binds
Rule 13 (DS lane) · 14/14a (`safe-commit -F`, unique per-commit message filename, one chain, read the subject before it is immutable) · 15 · **17a: BRONZE IS RAW — and note Q-s1: the bucket's parquet-deny policy matches the `bronze` SEGMENT, so it may NOT reach `bronze_legacy`; VERIFY THE GUARD'S REACH AT LANDING (one denied-write probe + an isolated positive control) and report. If unreached, the no-parquet property rests on `inv-2` alone and says so** · Rule 25 (closed-period immutable) · NEVER#3 (the served legacy series) · **NEVER-SUM / NEVER-SUBSTITUTE across 08242234 / 08335338** · no non-ASCII on AWS.

## Status + reporting
Cell-level `<cell_status>`; proof instance + flip in ONE commit. Report per flip with hash + push state ("LOCAL @hash, rides integration"). cc CVO at AC3/AC5/AC12 (the invariant mutants) and at AC11 (the MECE close).
