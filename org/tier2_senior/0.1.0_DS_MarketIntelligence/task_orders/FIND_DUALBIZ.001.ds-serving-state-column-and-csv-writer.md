# FIND_DUALBIZ.001 — Serving `state` column + CSV writer

**Project:** FIND_DUALBIZ (FIND macro; design doc-of-record `docs/briefs/find-dualbiz-seed-fingerprint-and-pipeline-design-20260605.md`)
**Pod:** 0.1.0_DS_MarketIntelligence
**Lane:** DS_MarketIntelligence (find-dualbiz serving stage)
**Issued to:** 0.1.0_DS_MarketIntelligence
**Author:** 2.0.0_SA_COO 2026-06-15 (CTO week-kickoff Item 1, Andrew-direct agenda)
**Sizing:** ~45-75min wall (state-extraction step + CSV writer + empirical re-run against most-recent harvested set)
**Authority anchor:** Andrew-direct 2026-06-15 week agenda ("the first of which" = FIND_DUALBIZ State column) via 1.0.0_SA_CTO kickoff 20260615T145935Z; COO pre-auth repo check 20260615T150x Z (owner + no-canonical-CSV confirmed)

<status>staged</status>

> STAGED, GO-ready. Authorized to flip to `pending` + begin on the COO GO message (pending Andrew's spawn of this lane). Do not start before the GO.

## Objective

The most-recent FIND_DUALBIZ serving output must carry a **`state` column** = where each firm is based (US state), derived from the **already-harvested** silver page text — **NO new fetches**. Two parts (CTO scope):
- **(a)** Add a real **serving `.csv` writer** to `stage_serving` alongside the existing `.json` + `.md` (there is no CSV writer in the pipeline today — confirmed; the only `.csv` on disk is a `.runtmp/` scratch side-export, not a pipeline output).
- **(b)** Add the derived **`state`** field/column to ALL THREE serving formats (`.json`, `.md`, new `.csv`).

## Background (COO pre-authoring repo check — done, so you don't re-derive)

- `data/find/dualbiz/scripts/pipeline.py` `stage_serving()` (def ~L216) currently writes `dualbiz-targets-{date}.json` (~L267) + `.md` only. No `.csv` writer exists.
- Silver keeps full **Rule-17 passthrough** page text at `silver/<slug>/<date>/page.json` (footer/disclosure/contact address text is in there) — that is your state-extraction source. No re-fetch.
- comp-blast on `stage_serving` = not in the trace graph; find-dualbiz is a standalone discovery pipeline with no shared S3 keys / functions touched by other active TOs -> `<cross_domain_coordination>` is `<none/>` (structurally verified).

## Acceptance criteria

- **AC1.** `from __future__ import annotations` first import (Rule 15); `.tools/ds-commit-gate.sh` clean (py_compile + AST + ruff py39, pin 0.15.11) (Rule 14); no non-ASCII in code/logs.
- **AC2.** State-extraction step added in `stage_serving` (or a helper it calls): derive `state` per firm from the harvested silver Rule-17 text — match a US state from address/footer/disclosure patterns (e.g. `City, ST ZIP`, full state names, "located in <State>", principal-office disclosure lines). Two-letter canonical code in the output (e.g. `TX`).
- **AC3.** `state` field present on EVERY firm row in ALL three serving formats: `.json` (new key), `.md` (new column), `.csv` (new column). ADDITIVE — no existing field pruned/renamed (Rule 17 spirit).
- **AC4.** New serving `.csv` writer in `stage_serving`, written to the same serving dir as the `.json`/`.md`, filename `dualbiz-targets-{date}.csv`. Columns = the existing serving table columns + `state`. Stdlib `csv` (DictWriter), UTF-8, deterministic column order.
- **AC5.** Heuristic accuracy bar = default; **~80-90% coverage acceptable, blanks where not extractable** — DO NOT fabricate a state when the text doesn't support one (empty/`null` is correct for unknowns). The authoritative SEC IAPD/Form ADV principal-office-state upgrade for the RIA-registered subset is an **optional follow-on, OUT OF SCOPE** here (note it in your RAVC2 as a flagged upgrade path).
- **AC6.** Empirical re-run against the most-recent harvested serving set: report the `state` fill-rate (N filled / N firms) + a small sample table (firm -> state -> evidence-snippet) proving the derivation reads real harvested text, not a guess.
- **AC7.** `comp-pipescript io data/find/dualbiz/scripts/pipeline.py` run (likely "Unknown script" — find-dualbiz is not in the bd/inf gold graph; account the Unknown explicitly, it is tooling-coverage not correctness).

## Cross-domain coordination

`<none/>` — comp-blast `stage_serving` = not in the trace graph; standalone discovery-pipeline serving export, no shared S3 keys / functions with any active TO. Re-confirm at commit if you touch anything beyond `pipeline.py` + a serving helper.

## Compiler tools mandate

- **Before edit:** `comp-pipescript io data/find/dualbiz/scripts/pipeline.py` (expect "Unknown script" — account it, don't miscount as clean).
- **Before commit:** `.tools/ds-commit-gate.sh data/find/dualbiz/scripts/pipeline.py` (mandatory, Rule 14).
- **After:** n/a — find-dualbiz serving is a standalone export (no gold-runner deploy). If serving publishes to S3, verify the served `.csv`/`.json` carries `state` against the served object (verify-channel), not just local output.

## RAVC2 deliverable

`[RAVC2-Request] FIND_DUALBIZ.001 — serving state column + CSV writer` to ws COO (CC ws CTO). Body: commit hash + diff summary (state-extraction logic + CSV writer + field-adds) + AC6 empirical evidence (fill-rate + sample evidence-snippet table) + the flagged ADV/IAPD authoritative-upgrade follow-on + comp-pipescript / ds-commit-gate output.

## Notes

- Andrew led the 2026-06-15 week agenda with this as the first item; CTO relayed. Heuristic-from-harvested-text now; ADV authoritative is the optional v2.
- Owner was offline at TO-author time; this TO is staged GO-ready so it fires the instant the lane is spawned + GO'd.
- Per Rule 17 / [[feedback_silver_no_field_slimming]] — derive from the full Rule-17 silver passthrough; do not slim or re-fetch.

— ws COO week-kickoff decomposition 2026-06-15 (Item 1)
