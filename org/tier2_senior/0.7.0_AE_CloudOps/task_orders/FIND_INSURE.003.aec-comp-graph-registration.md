# FIND_INSURE.003 — comp-graph registration for data/find/imo/ subtree

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.2 §6 (Compiler-tools mandate); ws CTO `bacf90484` 2026-05-27 ARCH-RULING Option (a)
**Pod:** 0.7.0_AE_CloudOps
**Lane:** AE base
**Author:** 2.0.0_SA_COO 2026-05-27T~15:50Z; v0.2 path amendment 2026-05-27T~16:10Z
**Status:** pending — GO held on .012 Fire 1 RAVC2-Accept per CVO ADDITIVE-2 timing gate
**Sizing:** ~30-60min wall

<status>pending</status>

---

## Amendment 2026-05-27T~16:10Z (path + subdir per ws CTO ARCH-RULING bacf90484)

Per ws CTO ARCH-RULING on AE 0.7 BLOCKED-ASK 16:02Z + COO ARCH-ASK 16:05Z, FIND_INSURE adopts:
- **Path:** `data/find/imo/scripts/` (NOT `data/find_insure/scripts/`)
- **Subdir convention:** medallion-by-layer (`bronze/silver/gold/serving/_meta`) with stage-name embedded in filename, matching fabric convention across orion/mdpf/black_diamond
- ws CTO v0.2 `bacf90484` ships the macro+project READMEs + medallion skeleton with `.gitkeep`s

This TO's AC1 below reflects the amended scope. Original v0.1 AC1 (8 stage-named subdirs at `data/find_insure/scripts/`) is superseded.

## Objective

Register the `data/find/imo/scripts/` medallion subtree with compiler tools (comp-graph + comp-pipescript) so that future Phase 1+ FIND_INSURE Lambda authoring exercises the standard CLAUDE.md compiler discipline (Rule 4 source map; comp-validate; comp-blast; comp-iam).

Per PRD v0.2 §6: `data/find/imo/scripts/` tree exists post-`bacf90484`; per-script registration as scripts land in later phases.

## Acceptance criteria

- **AC1.** Confirm `data/find/imo/scripts/{bronze,silver,gold,serving,_meta,_util}/` subtree exists (shipped by ws CTO `bacf90484` v0.2; `_util/` added per v0.3 `0719c576f` for slugify shared discipline per FIND_INSURE.002b) and is recognized by comp-graph. No new directory creation needed at this TO scope; per-script registration deferred to Phase 1+ as scripts land.
- **AC2.** `infra/aws/lambda/ci/lambda-source-map.json` updated to include placeholder entries for the Phase 1 Lambdas OR a structural commit that the source map will track once Phase 1 Lambdas land (whichever fits ADHC_DSFLOW pattern best).
- **AC3.** comp-graph indexing surface: confirm `comp-graph` either auto-discovers the new subtree OR document the manual step in the FIND_INSURE PRD §6 if a config-add is needed.
- **AC4.** comp-pipescript dry-run on the empty subtree exits 0 (no false-positive findings on placeholder structure).
- **AC5.** A short verification block in the AE per-tick log demonstrating each comp-* tool either recognizes or gracefully skips the new subtree.

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.003 — comp-graph registration` to ws COO with: directory tree confirmation, source-map diff (if any), comp-pipescript dry-run output, brief notes on any tool-side gaps (which may surface as ADHC_COMPIL_V5 candidates).

## Notes

- Companion to FIND_INSURE.001 bucket-IAM ship; can run in same AE 0.7 session.
- Low-touch on .012 critical path; mechanical compiler-tooling hygiene.
- Discovered tool gaps route as ADHC_COMPIL_V5 Fix-candidates per LD-0084 §2 sibling-PRD pattern; do NOT block FIND_INSURE Phase 0 close on compiler-tool-gap.

— ws COO 2026-05-27T15:50Z
