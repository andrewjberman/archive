# FIND_INSURE.002b — Slugify shared util + extract_source_list refactor

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.3 §3 (slugify-util shared discipline); ws CTO `0719c576f` v0.3 absorption of ws CVO arch-brief `8fb6f7d94`
**Pod:** 0.1.0_DS_MarketIntelligence
**Lane:** DS base (sub-deliverable of FIND_INSURE.002; same lane)
**Author:** 2.0.0_SA_COO 2026-05-27T~16:30Z
**Status:** pending — GO active in parallel; non-blocking on .001/.002 AC5/.003 (timing-flex per CVO brief)
**Sizing:** ~30-45min wall

<status>pending</status>

---

## Objective

Author a shared slugify utility at `data/find/imo/scripts/_util/slugify.py` mirroring the canonical pattern in `data/demo/scripts/transform/fake_identities.py`. This becomes the single source of slug-truth for all FIND_INSURE pipeline stages (Phase 1 `crawl-web` per-IMO path determination + Phase 2 `crawl-linkedin/crawl-jobs` reuse + Phase 3 `serving-build` consolidation joins).

Refactor `extract_source_list.py` (already shipped `9aaa1459d` + path-relocated `333413bcf`) to import from the shared util instead of carrying its own inline slugifier.

Per PRD v0.3 §3 + CVO arch-brief: prevents slug-divergence across pipeline stages by centralizing definition at `_util/` Phase 0.

## Acceptance criteria

- **AC1.** `data/find/imo/scripts/_util/slugify.py` authored with single exported function (e.g., `slugify(company_name: str) -> str`) implementing: lowercase + ASCII-only (Unicode-normalize NFKD + strip diacritics) + `-`-separated + collapse-consecutive-dashes + strip-leading/trailing-dash + handle `&` → `and` per fake_identities precedent.
- **AC2.** Module-level docstring cites canonical source (`data/demo/scripts/transform/fake_identities.py`) + PRD v0.3 §3 reference + immutability discipline (slug-stability is load-bearing for Phase 1 path-determination on re-runs).
- **AC3.** Unit-test-class assertions (inline `if __name__ == "__main__"` or docstring doctests acceptable; pytest not required at Phase 0 single-util scope): 5+ representative cases including the 4 sentinel-class from .002 AC7 spot-check + edge cases (Unicode diacritic; `&`-token; consecutive whitespace; leading/trailing whitespace).
- **AC4.** Refactor `data/find/imo/scripts/_meta/extract_source_list.py` to `from _util.slugify import slugify` (or equivalent relative import). Remove inline slugifier; keep CLI flags + extraction logic unchanged.
- **AC5.** Empirical anti-regression: re-run extractor against the 99-IMO universe and confirm slug output **identical pre-vs-post-refactor** for all 99 entries. Diff at AC evidence. Zero slug-drift.
- **AC6.** Standard DS discipline per CLAUDE.md: `from __future__ import annotations` first import; `.tools/ds-commit-gate.sh` clean; `.tools/ds-precommit-check.py` clean; ruff `--target-version py39` clean.

## Dependencies

- **Path:** `data/find/imo/scripts/_util/` subdir per v0.3 ratification — confirm exists via `git ls-tree` (ws CTO `0719c576f` should have shipped the medallion skeleton including `_util/`). If missing, create with `.gitkeep` + flag CTO via [SYNC] for v0.3 skeleton-completeness audit.
- **No upstream dependency:** decoupled from FIND_INSURE.001 bucket (no S3 write at this TO scope); decoupled from FIND_INSURE.002 AC5 (which is the deferred S3 write); decoupled from FIND_INSURE.003 (which doesn't touch script content).

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.002b — slugify-util` to ws COO with: slugify.py commit hash, refactor commit hash, AC5 empirical-identity diff (99/99 slugs identical), per-AC evidence block. CC ws CTO (PRD architect) + AE 0.7 (informational — _util/ may surface in their .003 comp-graph register-and-recognize step).

## Notes

- Non-blocking on .002 AC5 closure — slugify-util-via-import refactor + AC5 S3 write can land in either order. AC5 closure can use the v0.1-inline slugifier (already empirically-verified deterministic) OR the v0.2-imported one (if .002b lands first).
- Non-blocking on .001/.003 (different lane).
- Phase 1 dispatch (when authored) will assume slugify-via-import — .002b ships pre-Phase-1 to ensure clean import availability.
- CVO brief flagged this as "non-blocking on .002 RAVC2; can land as follow-on" — concurring as separate atomic TO sub-deliverable rather than addendum-to-.002.
- comp-pipescript io once code lands; no IAM scope (pure util module).

— ws COO /drive #169 follow-on 2026-05-27T16:30Z
