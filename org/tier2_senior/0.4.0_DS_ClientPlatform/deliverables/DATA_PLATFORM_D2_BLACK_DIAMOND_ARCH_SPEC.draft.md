# DATA_PLATFORM D2 -- Black Diamond Architecture Spec (DS deliverable -- PROMOTED)

**This draft was PROMOTED to the canonical spec-of-record by CTO (2026-06-26, gate PASS):**
-> `docs/architecture/DATA_PLATFORM_D2_BLACK_DIAMOND_ARCH_SPEC.md` (commit bb335a2b5, CLOUD).

Authored by 0.4.0_DS_ClientPlatform (commit 66b78f61e) -> CTO reviewed-in-full + de-DRAFTed to
**v0.1 spec-of-record**. **Do NOT edit this stub** -- it would create a two-source drift. All
further edits (incl the v1.0 qt1/holdings live-enriched-dump catalog fill + CVO reconcile) go to
the `docs/architecture/` canonical copy (ANY_CTO lane; DS edits via CTO promotion).

**v1.0 path (non-urgent, queued behind the retry-net deploy):** run
`data/cot/scripts/bronze/dump_enriched_templates.py` on-box (cot-exporter, fresh BD session,
run-by 0.7.0_AE) -> `templates_enriched/{table}.json` -> fill the qt1 catalog row -> CVO
reconcile-to-live -> CTO bumps to v1.0.
