# Reconciliation of the eight -- the CTO half's condition 1: every reader of a job's detail, with its key policy

**By:** `2.0.0_SA_COO~G2`, 2026-10-11, on `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_R13_RECONCILIATION_OF_THE_EIGHT_CTO_HALF.md`
@3b1895866f, condition 1 as CTO msg 5116 put it: "every reader of irpt-jobs detail named with its key policy, and one read in
code that none refuses the two new members. An EXACT reader is a STOP." After the half's own correction the detail has FOUR members, `code`, `cause`,
`receives`, `cause_claim`, and no `reconciled`; the member new to every reader is `cause_claim`.

**Result: no EXACT reader found. And one fact about the WRITE that the packet did not state and that is a STOP if missed.**

## 1. Where the detail lives (this corrects the packet's wording)

The packet says "detail". On the row it is ONE attribute, `job_detail`, of type STRING, holding the detail as canonical JSON
(`ycharts/generate/durable_job.py` line 172 writes `job_detail = :detail`; `ycharts/generate/submission.py` lines 33-35 define
the canonical form: sorted keys, separators `,` and `:`, no ASCII escaping). The eight rows carry no `job_detail` attribute
today: the laptop's inventory lists a job row's attribute names as `composition_sha256, fence_token, job, outbox_state,
request_revision, state, tenant`.

**The one decoder** is `DynamoGenerationStore.get_state`, `durable_job.py` line 136:
`json.loads(row.get("job_detail", {"S": "{}"})["S"])`. It takes whatever members the string holds. It has no key policy.

**So the write must set `job_detail` as a STRING of canonical JSON.** A map-typed `job_detail`, or the detail written under
another attribute name, breaks differently:
- a `job_detail` that is not a string makes line 136 raise `KeyError` on `["S"]`, and EVERY reader below then fails for
  that request, the status route included;
- a detail written under another name is read by nobody: the row would say FAILED with no cause.

## 2. Every reader of the decoded detail (product code; denominator below)

Searched: the pattern `get_state(` over `ops/`, `reports/`, `ycharts/generate/`, `ycharts/research/` and `intake/` of
`infra/aws/lambda/investor-reporting`, and the attribute name `job_detail` over all of `infra/aws`. `job_detail` appears in
product code in ONE file, `durable_job.py` (lines 136, 172, 192); every other occurrence is a test. No file outside
`investor-reporting` names it.

| # | reader | where | what it does with a FAILED job's detail | key policy |
|---|---|---|---|---|
| 1 | the status route | `ops/owned_status.py` lines 38-58 | Reads `state`, maps FAILED to (FAILED, ANALYSIS_FAILED) at line 20. It touches `detail` only at line 50, inside `if phase == "READY"`. It reads the state twice and refuses if the two reads differ | none on a FAILED job; the detail is not passed to the caller (`ops/tests/test_owned_status.py` line 28 asserts `job_detail` is absent from the answer) |
| 2 | the report route | `ops/owned_report.py` lines 175-186 | Refuses `ANALYSIS_REPORT_NOT_READY` at line 176-177 for any state but READY, BEFORE it reads `detail`. For these eight it answers today exactly what it will answer after: not ready | on READY only: three members must be present and well-formed; other members are not refused |
| 3 | the resident worker, on a delivery | `ycharts/generate/resident_worker.py` lines 654-676 | Reads `detail` only for a READY job (lines 659-672). A FAILED job is neither ATTENTION nor READY, so execution falls through to `store.claim()` at line 676 | none on FAILED. NOTE, not this condition's question: the claim's condition (`durable_job.py` line 80) refuses only READY, so a redelivered FAILED job is claimed and goes on into execution (read, not run). It is why the no-redrive rule matters |
| 4 | the worker's permanent-refusal end | `resident_worker.py` line 709 | state only | none |
| 5 | the worker's dead-letter record (st31) | `resident_worker.py` line 828 | state only: a job already FAILED keeps its state | none |
| 6 | the publisher and the publication worker | `ycharts/generate/publisher.py` line 74; `publication_worker.py` lines 62, 120 | state only (`CERTIFYING` required) | none |
| 7 | the packager's job read | `ycharts/research/opal_packager.py` lines 163 and 333-339 | takes `detail` only when state is READY | none on FAILED |
| 8 | the browserless generation job | `ycharts/generate/job.py` lines 346, 396 | reads `prior["state"]`; resumes only from SUBMITTING or UNCERTAIN | none on FAILED |

Eight readers, 0 with an exact-key policy on a FAILED job's detail. `ycharts/generate/job.py` line 134 is a `get_state` of an
in-memory store class in the same file, not a reader of the table.

**The one read in code that none refuses the new member:** line 136 decodes any JSON object; the only readers that look
INSIDE a detail do so for a READY job (readers 1, 2, 3, 7), and a FAILED job reaches none of those branches.

## 3. What this record did not read

- The commentary function (`outlook-global-commentary-draft-lambda`): `2.0.0_SA_COO~Y2` read it today
  (`deliverables/2.0.0_SA_COO~Y2/trace/COMMENTARY_READY_WHAT_IT_READS_20261011.md` @0a2b5da8af) and reports it never reads the
  job. I did not re-read it.
- Any reader outside this repository. The portal reads the status ANSWER, not the table (condition 1 of the st31 half).
- Deployed bytes: this is the trunk. The status function runs build `6idtFvAm` (the CTO's read at 12:52Z); whether its
  `owned_status.py` equals the trunk's at these lines was not compared.
