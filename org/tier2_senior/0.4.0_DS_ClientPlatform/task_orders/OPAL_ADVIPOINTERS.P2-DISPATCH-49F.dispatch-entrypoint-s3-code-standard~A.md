# TO OPAL_ADVIPOINTERS.P2-DISPATCH-49F — the dispatch entrypoint for the canonical 49F runner chain under the S3-code standard (push plan §3 row 2, DS~A half)

<task_order id="OPAL_ADVIPOINTERS.P2-DISPATCH-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DS_ClientPlatform~A (runner lane)</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-19 build (with AE's TF half, same window); unattended cycles 08-20/21/22 prove it.</dated>
<status>pending -- GO received 160631Z; sequenced behind P1-CLOSE deliverables at this seat</status>
<priority>P1 — the runner chain has no production trigger today (fails production-bar criterion (i)); this closes it</priority>
<authority>Push plan @a2f27c8d0a §3 row 2 + the CTO HOST RULING quoted verbatim in-row: "the runner executes under the S3-code standard as its OWN scheduled stage -- NOT appended to the legacy chain's stage list (different outputs, one producer per key holds)" — revisable on AE's read only with new evidence. P2 spec ratified @9b5896793f (CRO P2_UNIFIED_MORNING_SCHEDULE_TIMING_MAP_SPEC_20260811.md).</authority>
</task_order>

## Objective
Author the dispatch ENTRYPOINT that runs a00..a07 -> b00..b03 -> c00..c04 as ONE scheduled stage under
the S3-code standard (Rule 12: local -> S3 -> compute pulls -> execute; never code written on a VM,
never inline python in SSM). AE owns the TF (EventBridge floor + event accelerator) in
OPAL_ADVIPOINTERS.P2-FLOOR-49F; your entrypoint is what their schedule invokes. The D fleet is NOT in
this stage — publishers run on their own schedule after it (P4).

## Context
`runner_common.py` OUT_ROOT = `portal/gold/advi/49financial` (P3 re-point already landed); SCOPE =
`schwab/08335338`. Silver lands daily ~12:18Z. The entrypoint must resolve ALL inputs from S3 at run
time — a session-local input anywhere fails production-bar (i). Existing stage runners
(a00_runner/c0x_runner) are the composition units; do not rewrite stage logic under this TO.

## Compiler tools (three-phase)
Phase 1: `comp-pipescript io <script> --pipeline bd` for each runner the entrypoint composes — expect
0 COLUMN GAPS; `comp-pipescript postdeps <script> --firm bd` before any QA run. Phase 2: commit-gate.
Phase 3: `comp-pipescript deployed` shows MATCH after S3 upload (this IS criterion P2D-2).

## Cross-domain coordination
- shared_resource: the entrypoint script + its S3 code key — also_in_to: OPAL_ADVIPOINTERS.P2-FLOOR-49F
  (AE's TF references it as the invocation target). AE is last_write_owner on TF; you are on the
  script. MCP AE the exact S3 code key + invocation contract (args, env) BEFORE AE plans; AE MCPs you
  the schedule expression before apply.
- shared_resource: `opal-data-assets/portal/gold/advi/49financial/**` (write) — also in P1-CLOSE
  (read), P4-EMIT (DS~B read). Writes only via the chain's own emitters.

## Acceptance criteria
- P2D-1 ENTRYPOINT: script committed (repo home per the S3-membership guard rules) composing the full
  a->b->c chain, fail-loud per stage (a stage rc!=0 aborts the chain and the abort is VISIBLE in the
  run log — never swallowed), zero session-local inputs (every input an S3 read; enumerate the input
  set in the header docstring with bucket/key patterns).
- P2D-2 DEPLOYED: `comp-pipescript deployed <entrypoint>` = MATCH after `aws s3 cp` (safe-deploy lane
  discipline — DS owns the gold-script deploy cycle per Rule 13).
- P2D-3 QA EXERCISE (ad-hoc, run-and-read): one ad-hoc invocation via the S3-code path (not local)
  writes `{table}/date={D}/data.parquet` + manifest for a QA date; partitions listed with counts
  (denominator = table count in the chain) — artifacts are QA evidence, never production evidence.
- P2D-4 CONTRACT TO AE: the invocation contract (S3 code key, entry args, expected duration from
  known timings, failure signature) delivered to AE in writing before AE's apply.
- P2D-5 proof instance VALID rc=0 positional: ids P2D-1,P2D-2,P2D-3,P2D-4,P2D-5.

<proof_of_spec>
  <expected_criteria>P2D-1,P2D-2,P2D-3,P2D-4,P2D-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/OPAL_ADVIPOINTERS.P2-DISPATCH-49F_PROOF_OF_SPEC~A.json</instance_path>
</proof_of_spec>

## Do not
- Do not append the runner to the legacy chain's stage list (host ruling — own stage).
- Do not create the schedule/TF yourself (AE's half; Terraform is the only deploy mechanism there).
- No alerting/monitoring machinery (moratorium, Andrew 07-28). The schedule floor IS the control.

## Reporting
COO (cc CTO, AE, MSTR) at entrypoint-deployed and after the first unattended cycle. Surprise channel:
one banked line to COO. Session log with Compiler Tools section = explicit deliverable.
