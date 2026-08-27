# TO OPAL_MDPFCLEANUP.TO-0 — PIN + EXERCISE (pure verification, NO mutations)

<task_order id="OPAL_MDPFCLEANUP.TO-0" project="OPAL_MDPFCLEANUP">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:2xZ</issued>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project OPAL_MDPFCLEANUP, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: issued — GO (Andrew-direct "GO on OPAL_MDPFCLEANUP, dispatch to COO" @9364820b29; CTO dispatch 172234Z)</status>
<priority>P1 — first of the strict TO-0..TO-5 sequence; everything downstream keys on these pins</priority>
</task_order>

**PRD:** `docs/architecture/OPAL_MDPFCLEANUP_PRD.md` v1.1 @9f75dcb996 — §4 TO-0, copied verbatim below.
**Sequencing note (CTO 172234Z, binding):** pure verification — no mutations. Zero imports were
needed last time; if TO-0 finds one, import-before-edit applies.

## Objective (PRD §4 TO-0, verbatim spec)

(a) **Pin `wsb`/`wsd` feeder write-targets from DEPLOYED bytes** (Rule 22a: package download +
built-from diff resolved through the build input — never repo filename-match) → resolves the two K4
rows (`wsb-49f-model-aua-daily`, `wsd-49f-partner-held-etf-daily`) to KEEP or K2. ⚠ If wsb IS the
canonical `fact_model_aum_daily` producer (49F TO-4 value leg named it), it is KEEP — a kill would
sever a proof-cited input.
(b) **Exercise the `json/mdpf` consumer question** — comp-routes trace (--json, key on the outcome
enum) + CloudFront/access evidence over a live window, NOT source comments.
(c) **Publisher `R12_EXTRA_PAIRS` legacy-emission read** — does the canonical publisher still write
`json/mdpf` keys (deployed bytes, not repo).
(d) **`opal-data-mdpf` tree consumer sweep** (`mdpf/feeds/*`, `cache/`, `telemetry/`,
`bmkaud-evidence/`) — incl. IAM-floor discipline: a comp-iam operation list is a FLOOR, NEVER a
deletion warrant.
(e) **Confirm `mdpf-freshness-checker` absence** — record it, claiming nothing.
(f) **Rule-25 dormancy datings with successor checks** on every §3 row — abandoned vs key-migrated
look identical from age; census keys on BOTH spellings for the guarded set (`_` vs `-`).

## Acceptance

Per-resource claims, desired/applied/exercised, PRD §3 expected strings copied verbatim. Every K4
row exits TO-0 classified (KEEP/K1/K2/K3); no row remains UNKNOWN. Denominators printed on every
census read (auto-paginate; never `--no-paginate`).

<proof_of_spec>
<expected_criteria>wsb-wsd-write-targets-pinned-from-deployed-bytes; json-mdpf-consumer-exercised-live-window; publisher-R12-legacy-emission-read; opal-data-mdpf-consumer-sweep-with-iam-floor; freshness-checker-absence-confirmed; rule25-dormancy-datings-with-successor-checks; zero-K4-rows-remaining</expected_criteria>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_MDPFCLEANUP/proof_TO-0.json</instance_path>
</proof_of_spec>
