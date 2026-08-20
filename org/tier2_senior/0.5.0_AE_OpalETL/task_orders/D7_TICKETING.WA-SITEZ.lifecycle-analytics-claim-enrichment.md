# TO D7_TICKETING.WA-SITEZ — Ticket Lifecycle v2 W-A: native analytics fields + claim enrichment (smallest first; unblocks C3/O6)

<task_order id="D7_TICKETING.WA-SITEZ" project="OPAL_TICKET">
<issued_to>0.5.0_AE_OpalETL~Z (build; site-Z). Laptop apply leg = EXECUTION PLACEMENT via MSTR~Z ferry (envelope law @550b20ec5b: applies stay under laptop apply-time mechanics).</issued_to>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-20T20:0xZ</issued>
<status>pending — GO rides this commit's MCP. QUEUE POSITION: behind the dep-3 registration sitting at this seat (CTO~Z @942d4d885c: "the current dep-2/dep-3 chain is UNCHANGED and remains the critical path"). W-A is first of the four W lanes (CTO sequencing: smallest first).</status>
<priority>P2 (P1 = dep-3 schedule-landed)</priority>
<authority>ANDREW-DIRECT 2026-08-20 ~19:4xZ, TICKET LIFECYCLE v2 flow, record @942d4d885c (org/tier1_exec/1.0.0_SA_CTO/deliverables/ctoZ_ANDREW_DIRECT_20260820_TICKET_LIFECYCLE_V2_FLOW.md) — his O6 verbatim: "we need to have analytics built in to the DDB... easier to manage if its baked into the DDB and process natively." CTO~Z ruling 3 (ANALYTICS NATIVE) + C3 (claimer identity visible). Rigor frame: ATOM_DECOMP discipline @9b93c39eeb. CTO~Z RULES + COO~Z DECOMPOSES (@550b20ec5b). Design-of-record = the CTO~Z deliverable above; PRD §-anchor is CTO~Z's leg (TOs re-point when it lands).</authority>
</task_order>

## Objective
The `opal-ticket-api` Lambda's transition writes gain NATIVE analytics + claim enrichment, computed
IN the Lambda at the transition write (process-native, no external analytics job), appended to
`events[]` as today:

- at CLAIM: `claimed_at`, `time_to_claim_s`, `claimed_by = {name, email, user_id}` — resolved
  SERVER-SIDE at claim time from the claimer's `opal-users-v2` directory row (display-grade
  snapshot ON the ticket row; a snapshot, not a live join).
- at COMPLETE: `completed_at`, `time_to_resolve_s`, `completed_by = {name, email, user_id}`.
- `created_at` exists; one grain = one ticket's lifecycle.

**AMENDED ~20:09Z — ANDREW-DIRECT DAY-ONE FIELD SET (his no-retrofit word, "don't want to have to
be retroactively adding stuff", routed via CTO~Z 2777):** the cut ALSO carries, at day one:
- `schema_version: 2` (cheapest future-proofing);
- `priority` enum RESERVED (a reserved value is a schema act — it rides the Rule-24 record);
- `category` / `tags[]` free-form at claim/close;
- `reopened_count` + `reopened_at[]`;
- `first_response_at`;
- **`client_updates[]` APPEND-ONLY `{ts, author, text}` with the ORIGINAL DESCRIPTION as entry
  zero** — his rich-text store of client requests, IN the row (no second store, no join). DDB
  400KB item cap NOTED with the S3-spill key DESIGNED-NOT-BUILT (named in the schema record;
  never built in this TO).
`ticket_type`/`status`/`source`/`requester`/`events[]` are deployed and stay.

The Rule-24 schema record RIDES this change and covers the FULL field set above (grain declared,
axis intents stated, four-postulate note incl. the reserved priority enum; the outcome-array/enum
surfaces re-tested per the 08-20 Rule-24 widening).

## Acceptance criteria (D7F pattern: stable ids, mutants, both directions, positional proof)
- **WA-1** CLAIM transition, exercised on a real row: `claimed_at` + `time_to_claim_s` +
  `claimed_by{name,email,user_id}` land on the row, identity resolved server-side from
  opal-users-v2 (never from the request body).
- **WA-2** COMPLETE transition, exercised: `completed_at` + `time_to_resolve_s` + `completed_by`
  land; `time_to_resolve_s` measures create→complete on the row's own timestamps.
- **WA-3** MUTANT (D7F-4 class, both directions): a request body carrying forged
  `claimed_by`/analytics fields is ignored-or-refused (server-derived only) — the mutant
  DISCRIMINATES (forged in → not on row; legit claim → correct identity on row).
- **WA-4** REGRESSION: existing consumers unbroken — board/list/get render rows WITHOUT the new
  fields (pre-W-A rows) and WITH them; `events[]` append shape preserved; existing battery
  (authz 12/12, D7F rows) re-run green.
- **WA-5** Rule-24 schema record committed WITH the change (field set, grain, axis intent;
  opal-users-v2 snapshot semantics stated: display-grade copy, not a live join).
- **WA-6** IAM per Rule 22a: the Lambda role's read of `opal-users-v2` verified on the LIVE
  primitive — `aws iam simulate-principal-policy` with ONE `--resource-arns` (the exact table ARN)
  + a SEPARATE positive control; comp-iam treated as floor. Laptop apply: ledger opened/closed +
  tag; 0-diff.
- **WA-7** Proof instance VALID rc=0 POSITIONAL (`python .tools/proof-of-spec-check.py <instance>
  WA-1,WA-2,WA-3,WA-4,WA-5,WA-6,WA-7,WA-8`) — rc taken unpiped.
- **WA-8** DAY-ONE SET exercised (the ~20:09Z amendment): a create carries `schema_version:2` +
  `client_updates[0]` == the original description; a claim/close append lands a further
  `client_updates[]` entry APPEND-ONLY (a mutant overwrite/delete of an existing entry is
  refused/ignored — append-only discriminates); `first_response_at` set on the first responding
  transition; `reopened_count`/`reopened_at[]` behave on a reopen (or the reopen path's absence
  is stated honestly if no reopen transition exists yet — no phantom claim); the S3-spill key is
  NAMED in the schema record and verifiably NOT built.

<proof_of_spec>
  <expected_criteria>WA-1,WA-2,WA-3,WA-4,WA-5,WA-6,WA-7,WA-8</expected_criteria>
  <instance_path>org/tier2_senior/0.5.0_AE_OpalETL/deliverables/D7_TICKETING.WA_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## FREE FIXTURE — the measured pre-W-A baseline (COO~Z fold ~20:28Z, from DT~Z's surprise-channel note 2809)

The TAC-2' water-test row is a **completed lifecycle whose correct analytics values are already known
and were independently witnessed by four seats.** Use it rather than rediscovering one:

| ticket | `TCK-20260820-dcec0012` |
|---|---|
| created | 2026-08-20T20:18:09.873Z |
| claimed | 2026-08-20T20:25:52.709Z (POST /claim 200, `dt-promote-internal@opalinvest.dev`) |
| completed | 2026-08-20T20:25:53.113Z (POST /complete 200, same identity) |
| ⇒ `time_to_claim_s` | **462.836** |
| ⇒ `time_to_resolve_s` | **463.240** |

**MEASURED BASELINE:** on that completed row, top-level `claimed_by` and `completed_by` are **BOTH
NULL**, while `events[]` carries the actor correctly at every transition
(created `svc-ticket-form` → claimed → completed). Same class, same row: `requester_email` and
`firm` are null at top level while the nested `requester{}` object carries both.

**How to use it, and the honest bound:** this is the *pre-W-A baseline*, not a defect report — the
fields it shows empty are precisely the ones this TO fills. It gives WA-1/WA-2 a **regression
anchor with pinned arithmetic** (a post-W-A claim/complete cycle must populate what this row leaves
null, and the two derived seconds values above are what correct looks like). ⚠ **Whether those keys
are schema-present-but-unwritten or absent-and-rendered-null is a BUILD-TIME READ you owe at the
source — do not assume either from this table.** DT~Z surfaced and took no action, correctly.

<compiler_tools_mandate>
Before write: `comp-blast` on ticket_center lambda + `comp-iam service opal-ticket-api` (floor).
Before commit: `.tools/commit-gate.sh` (universal); `comp-pipescript` n/a (not a gold script).
After commit: live simulate-principal-policy per WA-6; `comp-validate` n/a (no gold artifact).
</compiler_tools_mandate>

<cross_domain_coordination>
`infra/aws/lambda/ticket_center/lambda_function.py` is SHARED with W-C half (b) (READ-OWN matrix)
and W-D (SUMMARIZE action). SEQUENCE: W-A lands FIRST; W-C(b)/W-D rebase on it. MCP the W-C/W-D
builder (same seat today — self-coordination note stands if reassigned). New resource:
opal-users-v2 (read) — WA-6 covers. No portal files in this TO (the client view is W-C).
</cross_domain_coordination>

## Do not
No alert/SNS/SES/monitor machinery (2026-07-28 moratorium; the nudge path is W-B and is
Andrew-asked there). No client-visible surface changes here (W-C). No matrix widening here
(READ-OWN is W-C; SUMMARIZE is W-D). Do not begin before the dep-3 registration sitting completes
unless CTO~Z re-sequences.

## Reporting
Completion report → COO~Z (validation) cc CTO~Z (acceptance gate) + MSTR~Z (laptop ferry for the
apply leg). Surprise channel: one line to COO~Z. Session log with Compiler Tools section =
deliverable.
