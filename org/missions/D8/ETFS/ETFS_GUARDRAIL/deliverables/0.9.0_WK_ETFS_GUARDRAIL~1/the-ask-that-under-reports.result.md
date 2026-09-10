# EG-s-23 -- THE STOP WORKED AND THE ASK UNDER-REPORTS

**Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Branch:** `wk-etfs_guardrail-2-1` · **Face:**
`ETFS_GUARDRAIL.TO-EG-s-23` @`5aeb940bd0` · **outcome_ref:** FWD-8

## 0. THE HEADLINE

**S23-AC1 PASSES BY OUTPUT — 7 of 7 arms, `EGS23-ASK-NAMES-EVERY-PARTNER`, rc=0.**

**The defect reproduced first, on the code as it stood** (arm (a)). Against `remediate.py` pinned at
`c6bcb7b12b`, two partners' ladder runs produced **2 of 2 `put_object` calls on 1 distinct key**, and the
stored body carried **only the second partner**:

    FIRST body  asks: [('49financial', '2026-09-09')]
    STORED body asks: [('cottonwood',  '2026-09-08')]
    top-level keys of the stored body: ['asks', 'authorization', 'generated_at', 'month']

49financial's outstanding day is absent, and **nothing in the document names a partner it does not
cover.** Premise held, so the cell proceeded.

## 1. CRITERIA

| id | status | rc | deciding line |
|---|---|---|---|
| S23-AC1 | **PASS by output** | 0 | `ARMS 7 of 7 PASS` → `EGS23-ASK-NAMES-EVERY-PARTNER` |
| S23-AC2 | **RECORDED (judgment)** | n/a | graded at L9 by `3.0.0_SA_CVO` — **not self-graded** |

`timeout 300 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~1/test_egs23_ask_completeness.py`

- **(a) PASS** — overwrite reproduced on the pre-change module loaded from git.
- **(b) PASS** — **3 of 3** partners reachable in the one document a reader opens.
- **(c) PASS** — partial `['cottonwood','inflection']` vs complete `['49financial','cottonwood','inflection']`,
  textually different.
- **(d) PASS** — suite **before rc=0 8 passed 0 failed → after rc=0 12 passed 0 failed**; `authorization`
  verbatim; `dry_run` fires no rung 3 (0 writes); class B stops with 0 re-runs.
- **(e) PASS** — **`DEPLOYED != BUILT`** (expected; this cell deploys nothing).
- **(f) PASS** — 0 SES clients, 0 Lambda invokes, 0 boto3 clients, 2 AWS CLI calls both `s3api`.
- **(g) PASS** — **4 of 4** new arms FAIL pre-change, PASS post-change.

## 2. THE SHAPE, AND WHY — one merged month document

Not per-partner keys, not a manifest. **The axis is who reads this and what they see.** The reader is a
person opening *one* file to decide whether Opal goes outside for data, so "which partners does this
cover" must be a property **of the stored document**.

Per-partner keys are the more obvious fix and are **worse on that axis**: each file becomes correct while
a partner that never wrote stays **invisible** to anyone who does not already know the partner set — the
same failure, moved from an overwrite to an absence. A manifest has the identical defect one level up.

So the document now carries `partners_covered` (derived from its own merged content) and `ask_scope`.

**And the merge's own failure mode is declared, not hidden.** A merge has exactly one input: the read of
what is already at the key. If that read is unavailable, a naive merge **silently degrades to the original
overwrite**. So `_read_prior_asks` separates an absent *capability* from an absent *object*:

- no `get_object` → `readable=False` → `ask_scope: "partner-only (prior asks UNREADABLE -- this file may
  omit other partners)"`
- `get_object` raises → the ordinary first-partner absence → stays month-complete

A reader is never handed a file that looks complete and is not.

## 3. WHAT THE SERVED ARTIFACT OMITS — the file a person would have authorised on

`s3://opal-data-etfs/platinum/reports/2026-09/coverage_egress_ask.json`, **1,017 B**, LastModified
**2026-09-10T01:20:20Z**, written by EG-s-15's real September run.

| | |
|---|---|
| asks it names | **1** — `cottonwood` / `2026-09-09` |
| outstanding per `coverage_unresolved.json` (same run) | **2** across `['49financial','cottonwood']` |
| **omitted** | **`('49financial','2026-09-09')`** |
| top-level keys | `['month','generated_at','asks','authorization']` |

There is **no field from which a reader could learn a second partner existed**. A person authorising on it
approved half of what was outstanding while believing they had seen all of it.

## 4. A CORRECTION TO MY OWN EARLIER ROW

`W1-S27` (mine, on EG-s-15) reported this 1-of-2 shortfall correctly but **speculated the cause was an
unmapped provider** for 49financial. **That speculation was wrong** — `_PROVIDER_BY_PARTNER` maps
`49financial -> "Schwab"` explicitly. The cause is the partner-less key plus the per-partner call. The row
hedged the cause as "likely", which is why it was a hypothesis and not a finding — but a reader chasing
the provider map would have found nothing wrong there.

## 5. CONSUMERS — censused, not recalled

`comp-find "coverage_egress_ask" --all` → **124 hits across 29,716 files**; bands SURFACED=36 CONFIG=8
TEST=33 DOC=47. Outside `remediate.py` and the tests, **exactly one** first-party consumer:
`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`. Its access sites were **read**, not
assumed: `:292 if ask and ask.get("asks")`, `:296 for a in ask["asks"]` with per-entry `.get(...)`, `:300
ask.get('authorization')`.

**Not broken by this change** — every key it touches is unchanged, the per-entry shape is unchanged, the
two new top-level keys are additive, and the only difference it sees is that `asks` is now *complete*.

**Lane:** that file is `0.9.0_WK_ETFS_GUARDRAIL~4`'s live surface for EG-s-21. **Read only — not edited,
not staged, not touched.**

## 6. WHY THE DEFECT SURVIVED A SUITE THAT LOOKED LIKE IT COVERED IT

`test_rung3_two_d_days_two_partners_ask_names_all_no_further_calls` already existed and passes against the
defect. It asserts the two **return values** and concatenates them *in the test*:

    all_asks = ask_cw["asks"] + ask_inf["asks"]

It never reads what is **stored**. The concatenation that makes it look complete happens in the test, not
in the artifact — and `_StubS3` has no `get_object`, so nothing in the suite *could* read back a write. My
four arms read the stored body and ship a `_StoreS3` that models a real key→bytes store.

## 7. DEPLOYED-vs-BUILT (arm e)

    DEPLOYED  s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/remediate.py
              11,011 B   sha256 3c3ce6c5cfcce654...
    BUILT     data/etfs/scripts/coverage/remediate.py
              15,011 B   sha256 25ff4dbed4af6545...
    DEPLOYED != BUILT          CRLF 0 in each

**Corroboration:** the deployed bytes hash **equal to the pre-change blob** — the box is running exactly
the overwriting version. Until someone deploys these bytes, **every future ladder run still overwrites one
partner's ask with the next.**

## 8. WHAT THIS DOES NOT REPAIR

The **served** artifact — the 2026-09 ask still omits 49financial's day; this cell writes no served key.
It is **not deployed**. It does not touch rungs 1–2, inflection's producer, or any egress authorization.
And it cannot make a partner that **never runs at all** appear — no per-partner function knows a set it
was never given — but such a partner is now *visibly* absent from `partners_covered` rather than
*invisibly* absent from a document with no coverage field, which is the property the bar asked for.

## 9. ROWS FILED

None. Nothing off-task surfaced; the correction in §4 is to my own prior row and is recorded here and in
the proof instance rather than as a new row, since the channel is append-only and `W1-S27` stands.

## 10. PROOF-OF-SPEC AND STATUS

`python .tools/proof-of-spec-check.py <instance> S23-AC1,S23-AC2` → **`VALID (rc=0)`**.
**`<status>` flipped to `complete`** — S23-AC1 passes by output.

## 11. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/wk-etfs_guardrail-2-1` → **empty**: LOCAL, never pushed.
