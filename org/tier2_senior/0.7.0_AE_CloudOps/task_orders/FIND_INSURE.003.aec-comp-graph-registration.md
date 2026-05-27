# FIND_INSURE.003 — comp-graph registration for data/find_insure/ subtree

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` §6 (Compiler-tools mandate)
**Pod:** 0.7.0_AE_CloudOps
**Lane:** AE base
**Author:** 2.0.0_SA_COO 2026-05-27T~15:50Z
**Status:** pending — GO via [DRIVE] MCP this cycle
**Sizing:** ~30-60min wall

<status>pending</status>

---

## Objective

Register the new `data/find_insure/scripts/` subtree with compiler tools (comp-graph + comp-pipescript) so that future Phase 1+ FIND_INSURE Lambda authoring exercises the standard CLAUDE.md compiler discipline (Rule 4 source map; comp-validate; comp-blast; comp-iam).

Per PRD §6 explicit note: "the `data/find_insure/scripts/` tree is new — comp-graph registration is a Phase 0 sub-deliverable. The compiler tools won't fully exercise FIND_INSURE artifacts until the graph knows about them."

## Acceptance criteria

- **AC1.** `data/find_insure/scripts/` directory created with subdirs matching PRD §3.4 orchestration: `crawl-web/`, `parse-web/`, `score-web/`, `crawl-linkedin/`, `parse-linkedin/`, `score-linkedin/`, `serving-build/`, `refresh-source-list/`. Each subdir has a `.keep` marker.
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
