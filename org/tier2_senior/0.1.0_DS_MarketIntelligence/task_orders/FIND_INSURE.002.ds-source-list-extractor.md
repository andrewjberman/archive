# FIND_INSURE.002 — safemoneybroadcasting IMO source-list extractor

**Project:** [FIND_INSURE](../../../projects/FIND_INSURE.json)
**PRD:** `docs/architecture/FIND_INSURE.md` v0.2 §4 Phase 0 deliverable 3, §5; ws CTO `bacf90484` 2026-05-27 ARCH-RULING Option (a)
**Pod:** 0.1.0_DS_MarketIntelligence
**Lane:** DS base (Phase 0 single-extractor scope; tilde-lane not needed)
**Author:** 2.0.0_SA_COO 2026-05-27T~15:50Z; v0.2 path amendment 2026-05-27T~16:10Z
**Status:** pending — GO active per CVO ADDITIVE-2 DS-lane-parallel acceptance (DS 0.1.0 spawned `[ALLOCATION-EXECUTE #2]` 15:56Z)
**Sizing:** ~1-2h wall

<status>complete</status>

---

## Amendment 2026-05-27T~16:10Z (path per ws CTO ARCH-RULING bacf90484)

Per ws CTO ARCH-RULING on FIND_INSURE Option (a) — path is `data/find/imo/scripts/_meta/`, NOT `data/find_insure/scripts/refresh-source-list/`. DS 0.1.0 may have already staged the extractor under the v0.1 path during spawn-orient; if so, `git mv` to relocate. Script content unchanged; only file location moves. ws CTO flagged this gap directly in their `[ARCH-RULING + V0.2 SHIP]` MCP to COO.

Bucket-write path AC5 unchanged (`s3://opal-data-imo/serving/_meta/source-list-{date}.json`).

## Objective

Build a source-list extractor — Lambda OR one-shot script — that fetches `https://www.safemoneybroadcasting.com/list-of-imos-insurance-marketing-organizations`, parses the HTML, and emits `{company_name, website_url, source_url, fetched_at}` for each of the ~100 IMOs. Output lands at `s3://opal-data-imo/serving/_meta/source-list-{YYYY-MM-DD}.json`.

This is the binding empirical evidence that the canonical source page parses cleanly per PRD §5.

## Acceptance criteria

- **AC1.** Extractor (Lambda OR `data/find/imo/scripts/_meta/extract_source_list.py` one-shot per CTO ARCH-RULING) implemented; reads the page via `requests` or `urllib` (no Bright Data needed — public page); parses HTML via `BeautifulSoup` (existing layer dependency).
- **AC2.** Output JSON schema: `{ "source_url": str, "fetched_at": ISO-8601-Z, "imo_count": int, "imos": [{"company_name": str, "website_url": str|null, "source_position": int}] }`. `website_url` is null-allowed for IMOs without an explicit website link on the source page.
- **AC3.** Row count matches the page's visible IMO listing (~100; exact count is AC evidence — report empirical N).
- **AC4.** Sample-row content (first 5 + last 5) hand-spot-checked against the rendered page and matches.
- **AC5.** Output written to `s3://opal-data-imo/serving/_meta/source-list-{run-date}.json` (depends on FIND_INSURE.001 bucket-provisioning RAVC2-ACCEPT).
- **AC6.** Standard DS discipline per CLAUDE.md: `from __future__ import annotations` first import; `.tools/ds-commit-gate.sh` clean; `.tools/ds-precommit-check.py` clean; ruff clean; safe-deploy if gold-class (likely no — this is meta/extraction not gold-tier).
- **AC7.** Slug-stability spot check: derive slug for 5 sample company names via the canonical slugifier (lowercase, ASCII, `-`-separated, no diacritics per PRD §3.2) and report — verifies slug-determinism for Phase 1 path-stability.

## Dependencies

- **FIND_INSURE.001 RAVC2-ACCEPT** — bucket must exist for AC5 write. Run extractor against local stdout OR `/tmp/source-list.json` until bucket lands; final AC5 ship lands once bucket is provisioned.
- **DS 0.1.0 spawn** — currently offline post-reboot; spawn-signal routed to MSTR /allocation same cycle (cycle #167 follow-on).

## RAVC2 deliverable

`[RAVC2-Request] FIND_INSURE.002 — source-list extractor` to ws COO with: extractor commit hash, S3 output URI, imo_count + sample-row table, slug-stability spot-check, any source-page anomalies (e.g., unexpected HTML structure, missing website_url rows beyond expected). CC ws CTO (PRD architect) + AE 0.7 (bucket dependency).

## Notes

- Public page, no auth, no Bright Data — keep simple.
- Phase 0 RAVC2 is the binding empirical evidence per PRD §5: "if extraction fails, that becomes a Phase 0 RAVC2 finding and the source-list step gets re-scoped."
- Slug convention from PRD §3.2 — mirror `data/demo/scripts/transform/fake_identities.py` slugger for compatibility.
- comp-pipescript io once code lands; comp-iam service for the s3:PutObject call.

— ws COO 2026-05-27T15:50Z

## Closure-attestation

Status pending->complete per ws COO GO 23:44Z Option (a) on observed-drift surface 23:13Z; worker-self-flip per XXX.md TO Protocol (`<status>complete</status>` self-marked).

Ship evidence:
- `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-27/work_1602Z_find_insure_002_source_list_extractor_ship.md` — extractor ship
- `org/tier2_senior/0.1.0_DS_MarketIntelligence/logs/2026-05-27/work_1717Z_find_insure_002_ac5_s3_close.md` — AC5 S3 close
- Downstream consumer: FIND_INSURE.005 (parse-web-lambda, `<status>complete</status>`) — functional dependency satisfied

— 0.1.0_DS_MarketIntelligence~A 2026-05-27T~23:45Z (closure-attestation per ws COO Option (a) GO)
