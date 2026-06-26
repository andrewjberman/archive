# PFMG_TAXSMA Leg-1 (step-1 rename + stateful flag) — design note for the CTO arch-gate

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-06-26 | **Project:** PFMG_TAXSMA (dir predates the ADVI->PFMG rename)
**Gate:** CTO step-1 runtime arch-gate (4 checks, pre-position 201746Z; hybrid GO + leg decomposition 201918Z). RAVC → [1.0.0_SA_CTO]; CC [2.0.0_SA_COO] + [3.0.0_SA_CVO].
**Scope:** DESIGN ONLY (design->arch-gate->build, the GATE-0 pattern). No rename code until CTO accepts. Grounds Yang's spec + S0.3 + S0.1, does not invent the runtime/flag-store.

---

## 0. Grounded inputs (cited)

- Yang step-1 (verbatim): two daily "Short Sale Avail File" emails (FIS/`SmartLoan9990@fisglobal.com`) → download both attachments to the **Short Sale** folder, FIRST renamed ` YYYYMMDD PRELIM`, SECOND ` YYYYMMDD`. (`tools/tax_sma/YANG_TAXSMA_AUTOMATION_SPEC.md` §step-1)
- BASE = `…\Opal Capital\Shared - Documents\TAX` (Yang's machine; OneDrive-shared → HYBRID-hostable). (`PFMG_TAXSMA_S0.2_converter_scripts_assessment.md`)
- S0.3 rule: sort the date's FIS emails by `receivedDateTime` asc → first=PRELIM, second=final; single-email-day = **option (a) stateful flag** (hold, no cutoff, Andrew-direct). (`deliverables/ADVI_TAXSMA/S0.3_email_disambiguation_rule.md`, `210217bd9`)
- S0.1: step-2 lot cost-basis is a LOCAL/fresh-pull leg, not an AWS lookup. (CVO `5322c8672`)
- CTO arch-gate: HYBRID GO = local-runner + status surface (not a hosted Lambda day-one). (`201918Z`)

## 1. CHECK 1 — the STATEFUL FLAG STORE (load-bearing)

**Granularity (confirm):** the FIS "Short Sale Avail File" is a SINGLE firm-wide SmartLoan file (two sends/day), NOT per-account. So the flag is keyed by **business-date**, one record per date. (The CTO "first email per client/date" phrasing resolves to per-date for this firm-wide file — flag if a finer grain is intended.)

**WHERE it lives:** a small JSON ledger owned by the local runner at `BASE\Short Sale\.state\short_sale_flags.json` (one writer, daily volume — no DB needed; inspectable; under BASE so the eventual Alyssa UI reads it from the shared drive). SQLite is a drop-in if concurrency ever warrants; day-one JSON.

**Record + lifecycle (open→closed state machine):**
```
{ "date": "YYYYMMDD",
  "state": "OPEN_PRELIM_PENDING" | "CLOSED_FINAL",
  "prelim": {"received_at": ISO, "saved_as": " YYYYMMDD PRELIM", "msg_id": ...},
  "final":  {"received_at": ISO, "saved_as": " YYYYMMDD",        "msg_id": ...} | null }
```
- **OPEN** on the FIRST FIS email for date D: save attachment as ` D PRELIM`, write state=`OPEN_PRELIM_PENDING` (+ prelim block).
- **CLOSE** only on the SECOND email for date D: save as ` D` (final), state=`CLOSED_FINAL` (+ final block). The open→closed **transition trigger** is strictly the arrival of the second email — **no cutoff, no auto-promote** (option a).
- A lone PRELIM stays `OPEN_PRELIM_PENDING` indefinitely until the second arrives.
- **Idempotency:** keyed by `(date, msg_id)` so a re-run / re-poll never double-saves or double-transitions.

**QUERYABLE / not-silent (Andrew-direct):** the status surface (Check 2) projects every `OPEN_PRELIM_PENDING` date as a visible "PRELIM-only, final not yet arrived" row — a lone-email date is in a KNOWN pending state, never silently dropped or silently treated as final. Query = `state == OPEN_PRELIM_PENDING`.

## 2. CHECK 2 — HYBRID runtime shape (local-runner + status surface)

- **Local-runner:** a Python runner on the machine with BASE (OneDrive-shared) mounted. Reads FIS emails via the **M365 gateway** (mail-read + attachment-fetch, READ-ONLY — the same gateway SCTY/NFRA_MSGRAPH hardens); writes renamed attachments to `BASE\Short Sale\` and the flag ledger. No hosted Lambda day-one (S0.1 = local leg).
- **Trigger:** daily-AM scheduled (emails land ~5AM + ~7AM). Local scheduler (Windows Task Scheduler) fires it; it is also safely re-runnable on demand (idempotent).
- **Status surface (observable):** the runner writes a `BASE\Short Sale\.state\status.json` after each run — last-run time, per-date flag states (OPEN/CLOSED), what it saved, any OPEN_PRELIM_PENDING dates, errors. This is what the eventual Alyssa UI reads (UI is a later leg; day-one the status file IS the surface). The rename is thus **driven** (scheduled runner) and **observable** (status.json + the flag ledger).
- **Destructive-surface note (SCTY):** step-1 WRITES attachments to one named folder (`BASE\Short Sale\`) only — bounded, non-destructive (new files, never overwrites a CLOSED final), read-only on mail. Aligns with the PRD's bounded-write posture.

## 3. CHECK 3 — STEP-2 data source

- **Day-one = fresh-pull (local):** Yang's manual Schwab Cost-Basis-tab "Export only lot level detail" → TCF lot files under `Tax Lot/YYYYMMDD` (per Yang step-2 + `SCHWAB_SDD_DELIVERY_BRIEF.md` §9). No AWS-native lot data exists (S0.1).
- **Go-forward (Leg-2a, Nixon only):** extend the CRS ingest to Nixon (bd+schwab, SmartX master `0008242234`) + revive cadence → converts step-2 to an AWS-native lookup (ULN schema is already 1:1 to `convert_cost_basis` IN). **Feasibility to confirm BEFORE committing the CRS path:** Chiles+Bump have NO Schwab ACC (Leg-2b, → DS mini-discovery, NOT mine); only Nixon is CRS-ingestable. Fresh-pull is the day-one leg regardless.
- **Schwab-ULN cadence note:** before any "revive," I confirm HALT-vs-batch-cadence (Schwab CRS is ad-hoc ~monthly; last ULN 05-08 is likely no-new-delivery, not a break) — low-pri, post-L6, no false-chase (COO+CVO discipline).

## 4. CHECK 4 — STEP-3 (and STEP-5) unchanged

- `convert_cost_basis.py` (Leg-3) + `convert_optimization.py` (Leg-5, now committed `bfa81d9da`): Yang **VERBATIM**, a `{BASE}+{date}` **parameterize-only** shim — no logic edits (S0.2: located, HYBRID-hostable, BASE=OneDrive-shared). The shim only injects BASE + the YYYYMMDD date so the same scripts run under the hybrid runner. Ground each against `YANG_TAXSMA_AUTOMATION_SPEC.md` for the I/O contract before wiring.

## 5. Build order (on CTO accept) + what stays gated

1. Leg-1 rename + flag ledger + status.json (this design) — the runner core.
2. Leg-3 + Leg-5 parameterize-only shims (verbatim converters).
3. Leg-2a Nixon fresh-pull wiring (+ CRS-extend feasibility confirm).
- GATED, not mine: Leg-2b (Chiles+Bump bd cost-basis → DS mini-discovery). NOT invented here.

## 6. Open question for the CTO

1. **Flag granularity** — confirm per-business-date (firm-wide FIS file) vs a finer per-account grain. My read: per-date.
2. **Flag-store location** — `BASE\Short Sale\.state\` (under the shared drive, UI-readable) vs a runner-local state dir surfaced via status.json. My lean: under BASE so the UI reads it natively; confirm that mixing a `.state\` dir into the shared TAX folder is acceptable.

**Net:** step-1 is a hybrid local-runner that intakes the two FIS emails via the M365 gateway, applies the S0.3 order rule, renames into `BASE\Short Sale\`, and maintains a per-date open/closed flag ledger (option-a, queryable via status.json) — no cutoff, never a silent skip. Design-only; RAVC CTO for the arch-gate, then I build the runner.
