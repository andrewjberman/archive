# TO OPAL_MDPFCLEANUP.TO-4 — RESERVED KILLS (each class on Andrew's word) ⛔ STAGED

<task_order id="OPAL_MDPFCLEANUP.TO-4" project="OPAL_MDPFCLEANUP">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-14T17:2xZ</issued>
<status>complete -- S3 delete leg executed 2026-08-19 01:0xZ (10/10 per manifest; Andrew word ~1500Z; both NEVER#3 halves; COO fixture release 005714Z; CTO ledger validation @18c3846cbd; COO proof acceptance 011704Z). HELD residual: json/mdpf/49financial/aggregate-aua-timeseries.json behind MDPF_PROVENANCE T-B (>=08-20). EC2 stop/terminate class NOT exercised (carve-out, KEEP-UNTIL-REHOMED). proof_TO-4.json + ledger 20260819T0057Z.</status>
<priority>Strict sequence position 5 (PRD §4)</priority>
</task_order>

**PRD:** `docs/architecture/OPAL_MDPFCLEANUP_PRD.md` v1.1 @9f75dcb996 §4 TO-4, verbatim.

## Objective

Reserved-category kills, each class on Andrew's explicit word: **EC2 stop/terminate** (mdpf-daily
runner + smartx exporter) · **S3 deletions** (`json/mdpf` teardown un-parked with the CTO+COO
never-widen sign-off — the producer leg retires FIRST per §3, the served-key delete is the LAST
act; `feeds/cache/telemetry` trees). **Copy-manifest-first; DELTA accounting in-proof.** A word
scoped to one class never widens to another; referents enumerated per the "recs approved" pattern.

## Acceptance

Per-class: Andrew's word recorded verbatim with referents; copy-manifest sha256'd BEFORE any
delete; DELTA=0 or accounted; NEVER#3 sign-off recorded for served keys. PASS_WITH_DISCLOSURE
available where a leg is blocked by a withheld word (TRGALN v1.4 pattern).

**NEVER#3 sign-off conditions for the `json/mdpf` teardown (pre-agreed COO 174623Z + CTO 174701Z;
both halves sign at execution against the copy-manifest, no fresh round-trip on Andrew's word):**
(i) Andrew's TO-1 ratification of the row; (ii) Wave 1's writer-retirement landed FIRST; (iii)
**a ZERO-DIRECT-HIT access-log read on `json/mdpf/*` paths over >=7 trailing days at execution
time, BOTH spellings of the guarded set, including whatever post-retirement span exists — a zero
over a DENOMINATOR-PRINTED request count; an unqueried log is not evidence.** (The router read
exonerates the ROUTE; only the access log sees a hardcoded direct S3/CDN fetch.) A NON-zero read
converts CTO's half to a finding (name the fetcher) — route it and the CONSUMER is adjudicated,
not the delete refused.

<proof_of_spec>
<expected_criteria>per-class-andrew-word-verbatim-with-referents; copy-manifest-sha256-before-delete; delta-accounting-in-proof; never3-signoff-for-served-keys; producer-leg-retired-before-served-key-delete; zero-direct-hit-access-read-7d-both-spellings-denominator-printed</expected_criteria>
<instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_MDPFCLEANUP/proof_TO-4.json</instance_path>
</proof_of_spec>
