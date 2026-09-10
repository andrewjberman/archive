# ETFS_GUARDRAIL.TO-EG-s-20 -- THE SEND PATH MADE CORRECT AND TEST-SAFE

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` (L7 worker subagent of `2.0.0_SA_COO`, round 3, cell `EG-s-20`)
**Worktree:** `/c/tmp/wk-etfs-3-4` on `wk-etfs_guardrail-3-4`, cut from CLOUD at `ea47e92a72`
**Window:** 2026-09-10 ~03:2xZ -> ~04:0xZ
**Commits (LOCAL, never pushed):** `6b79c79663` (the fix + tests + the OPEN ledger entry, BEFORE the apply), `670269d25b` (the CLOSED entry + the preserved plan transcript + the AC2 battery, BEFORE the grading reads)

> **NO SEND AND NO INVOCATION OF `etfs-reports-orchestrator` WAS FIRED BY THIS ORDER.** Every AWS
> call made here is a READ (`lambda:GetFunctionConfiguration`, `lambda:GetFunction`, an HTTPS GET of
> the presigned code location, three `s3:GetObject`) plus the one Terraform apply the face mandates.
> The imported deployed module's boto3 clients are stubs that RAISE on any call.

---

## 1. THE DEFECT, RE-DERIVED AT THIS SEAT BEFORE TOUCHING ANYTHING

The face handed me the measurement; I re-took it rather than inheriting it.

| what | value | instrument |
|---|---|---|
| deployed zip member `lambda_function.py` | 28,504 B, sha256 `dc05ea90c94dc41e21a92b63a69a3bc3f278dbc878c11324e35b56a295241fd8` | presigned `Code.Location` fetched and hashed |
| worktree file at `ea47e92a72` | 28,504 B, same sha256 -- **EQUAL** | local hash |
| `:435` (deployed) | `unresolved_days = (unresolved_doc or {}).get("unresolved") or []` | `sed -n '435p'` on the zip member |
| `:516` (deployed) | `msg = _build_terminal_email(month, unresolved_doc.get("unresolved") or [], artifacts["ask"])` | `sed -n '516p'` on the zip member |
| served `coverage_unresolved.json` (2026-09) | 1,414 B, sha256 `8edeb9e77d962431...`, top-level keys `['49financial', 'cottonwood']`, `'unresolved' in doc` = **False** | `s3api get-object` |

Worktree == deployed, so the line numbers are the same in both and this is not a skew.

**THE PRODUCER, read rather than assumed.** `render_month_end.coverage_gate` builds
`any_unresolved[partner] = ladder_result["unresolved"]` (`:961`) into `{"unresolved": any_unresolved}`
(`:971`), and `main()` uploads `verdict["unresolved"]` verbatim to `coverage_unresolved.json`
(`:1066-1069`). The document is keyed by PARTNER by construction. I exercised that function
hermetically (series supplied, probe stubbed, `ladder=False`, zero AWS) and got exactly the served
shape back.

---

## 2. WHAT I CHANGED, AND WHY THAT SHAPE

### 2.1 ONE normalizer at BOTH sites

`_normalize_unresolved(doc)` returns a flat row list, injecting each row's `partner` from the key the
producer put it under. Both former defect sites now call it -- **the same function**, so the live
guard and its own rehearsal can no longer disagree. That is the point: the CVO's row `S11` named the
real fault as *a guard sharing a failure mode with the thing it guards*, and two independently
correct call sites would leave that fault standing.

Post-fix, in the DEPLOYED bytes (727 lines):

```
:602              unresolved_days = _normalize_unresolved(unresolved_doc)
:713          unresolved_days = _normalize_unresolved(artifacts["unresolved"])
```

`terminal_qa` additionally returns `unresolved_count` and `unresolved_dates`. **That is what makes
the rehearsal able to FAIL.** Before, a QA run over a month with two unresolved dates returned
`ok:true` with a subject and a body head and nothing that could distinguish "no unresolved dates"
from "two unresolved dates the reader is keyed wrong for".

I did NOT keep a literal `.get("unresolved")` compatibility branch. It is unnecessary: the legacy
`{"month": ..., "unresolved": [...]}` shape flattens correctly through the partner branch anyway
(`"month"`'s value is a string and is skipped; `"unresolved"`'s value is a list whose rows carry
their own partner), which is why the round-1 fixture still passes. Tolerance for free, and the
census over the deployed source reads a literal zero.

One cosmetic correction in the same function, disclosed: the producer writes no `provider` into
`coverage_unresolved.json` (only `coverage_egress_ask.json` carries it), so `u.get('provider')` put
the literal string `None` into an URGENT email. It now renders `(not stated)`.

### 2.2 THE RECIPIENT SHAPE I CHOSE, AND WHY

Andrew, ~02:5xZ, verbatim: *"make sure no test run hits aj's email, that is not appropriate."*

The constraint is unsatisfiable by any invoker as the code stood, because the recipient set is the
PRODUCER's: `EMAIL_RECIPIENT` is a Lambda environment variable and reads
`aj@opalinvest.com,andrew@opalinvest.com`. So the fix has to move the decision to something the
invocation can carry.

**THE SHAPE: a marker on the event, an override, and an unconditional forbidden-filter that runs LAST.**

```
TEST_MARKER              = "test_run"
TEST_FORBIDDEN_RECIPIENTS = frozenset({"aj@opalinvest.com"})
TEST_DEFAULT_RECIPIENTS   = ("andrew@opalinvest.com",)

_resolve_recipients(event, base) -> (RFC 5322 header, SMTP envelope list)
    no marker  -> `base` VERBATIM and its split
    marker     -> `base` DISCARDED; event's `test_recipients` (or the defaults); then _drop_forbidden
```

**Why this and not the alternatives.**

- *Why not change `EMAIL_RECIPIENT` for the test run?* Because that is the PRODUCER's variable and
  changing it is a Terraform change that would have to be changed back -- a two-deploy dance around a
  live monthly schedule, with a window in which the 10-01 fire would deliver to the wrong set. The
  invocation is the thing that differs between a test and the schedule; the distinction belongs there.
- *Why not "no send at all on a test invocation"?* The face allowed it, and it is safer in one narrow
  sense, but it would make `EG-s-21` unprovable: FWD-10's whole content is that the terminal send
  FIRES and reaches andrew@. A test path that cannot send cannot demonstrate a send. So: send, but to
  a set that provably cannot contain aj@.
- *Why a FILTER and not just a replacement?* A replacement is a default, and a default is defeated by
  the next caller who passes an override. `_drop_forbidden` runs **after** every branch, so the
  property is structural: no event field, no environment value, no caller argument can put aj@ back.
  Measured: aj@ appears in **0 of 24** adversarial resolutions (list, joined string, mixed with a
  legal address, different case, whitespace-padded, duplicated, empty, null, truthy-non-boolean
  marker, non-`run` mode) across both recipient carriers.
- *Why does an empty envelope send NOTHING?* Because "cannot reach aj@" must not degrade into "sent
  to somebody else by accident". A test invocation whose recipients all filter away resolves to `[]`,
  and every send site prints a `SKIP:` line and returns.
- *And the other direction, which is not optional:* a payload with no marker -- which is exactly what
  `aws_scheduler_schedule.monthly_run` sends, `jsonencode({mode = "run"})` -- resolves to BOTH
  recipients, in order, identical to the module's own `EMAIL_RECIPIENTS` derivation, across 5 payload
  shapes. A fix that made the scheduled path stop delivering to aj@ would have been the wrong fix.

**Two additions that serve the next order.** A send-free `recipients_qa` mode returns both directions'
resolutions and answers an adversarial probe *from the running function*, so `EG-s-21` can re-take its
precondition against the live Lambda rather than an offline copy of its bytes. And both send sites now
print their SES `MessageId` -- row `W1-S26` measured that this function emitted **zero** application
log lines, so a send that DID fire had no oracle anywhere. `EG-s-21`'s arm (e) names that log line as
its strongest instrument; this deploy is what creates it.

---

## 3. THE TESTS, BUILT FROM THE PRODUCER'S OUTPUT

Round 1 passed because its fixture (`test_terminal_send.py:118`) was built to the DOCSTRING's shape.
So the new arms take the shape from the producer, **two independent ways** -- and the old fixture is
KEPT, relabelled in place as a legacy-tolerance arm, because deleting it would hide the history.

1. **BY RUNNING THE WRITER.** `render_month_end.coverage_gate` with `series` supplied, `probe`
   stubbed, `ladder=False`: zero AWS calls, and its `unresolved` is the shape asserted.
2. **BY LOADING SERVED BYTES.** The real 2026-09 object, committed as
   `fixtures/served_coverage_unresolved_2026-09.json` (1,414 B), asserted to carry the shape (1)
   produces -- same key discipline, row keys exactly `{date, class, reason}`.

**THE DISCRIMINATOR.** The same NEW arms run against the PRE-FIX blob (the deployed bytes swapped into
the worktree, then restored and re-hashed to `ac0484b73a26865e...`):

```
7 failed, 8 deselected in 2.61s          rc=1
FAILED test_producer_shaped_document_fires_exactly_one_terminal_send
       - AssertionError: exactly ONE terminal send on the refusal branch
FAILED test_producers_own_writer_emits_a_partner_keyed_document      - AttributeError: _normalize_unresolved
FAILED test_served_artifact_has_the_shape_the_writer_produces        - AttributeError: _normalize_unresolved
FAILED test_terminal_qa_rehearsal_can_now_fail_on_a_real_month       - KeyError: 'unresolved_count'
FAILED test_terminal_send_prints_its_messageid                       - assert 'MessageId=...' in ''
FAILED test_a_test_invocation_cannot_reach_aj_under_any_branch       - AttributeError: _resolve_recipients
FAILED test_the_scheduled_invocation_is_unchanged_and_still_reaches_both - AttributeError: _resolve_recipients
```

The headline arm fails on *zero sends on the refusal branch* -- the defect itself. A test that passes
both before and after is not a test of this change.

**One harness defect fixed on the way, and it is the same class as the one being repaired.**
`test_handler_mode_table_has_no_new_sending_mode` matched `"_send_correction_email()" in body`, with
the empty parens baked in. The moment that call took an argument -- which this order gives it -- the
detector would have stopped seeing the only real sending mode and passed with `sending_modes == []`.
A harness transcribed from one call shape scores its own blind spot as a pass. It now matches the
CALL.

---

## 4. THE DEPLOY (NEVER-2, spine v3.9 ordering)

Entry: `org/critical_paths/change_management/20260910T0347Z_etfs-guardrail-eg-s-20-send-path_deploy_completion.md`

| step | UTC | evidence |
|---|---|---|
| entry OPENED (5 legs, 4.0 h window) | 03:47:51Z | before the apply, naming the served function, the live pre-state, the rollback and both never-widen halves |
| code COMMITTED | 03:48:53Z (`6b79c79663`) | **before** the apply |
| targeted plan -> SAVED PLAN FILE | 03:50:35Z -> 03:50:43Z, rc=0 | 1 resource; `Plan: 0 to add, 1 to change, 0 to destroy.`; transcript PRESERVED |
| `safe-apply` on that plan file | 03:54:09Z, rc=0 | `Apply complete! Resources: 0 added, 1 changed, 0 destroyed.` |
| entry CLOSED + COMMITTED | `670269d25b` | **before** the grading reads |
| grading reads (AC1, AC2) | after | see s.5 |

| | pre | post |
|---|---|---|
| `CodeSha256` | `M5Dopbky3W1f1j97cqAB403Kh7IofIv/p0fCtRg7W80=` | `ag4La0jgP8JEr55FCvXx+gnR5pDqw1CpvbEHZBrBTPc=` |
| `LastModified` | 2026-09-10T01:16:14Z | 2026-09-10T03:54:09Z |
| `CodeSize` | 10,193 | 13,785 |

`.tools/terraform.exe` **v1.9.8** throughout (never the PATH binary, which would re-pin the state's
`terraform_version`). Never a bare `terraform apply`; never `aws lambda update-function-code`.
Post-apply targeted re-plan at `-detailed-exitcode` -> rc=0, `No changes.`

**`HALT_ACK=1` WAS NEITHER USED NOR NEEDED.** The first `safe-apply` returned rc=3
`IDENTITY UNRESOLVED` *with `OPAL_AGENT_SERIAL` exported*, because `.tools/halt-gate-check.sh:52-118`
resolves identity ONLY from `org/mcp/sessions/<CLAUDE_CODE_SESSION_ID>.serial` or an
`*.orphan-cleaned` marker and never reads the variable. The gate's own printed one-line fix was
applied with this worker's TRUE serial into that gitignored path (`.gitignore:423`, absent in a fresh
worktree, nothing tracked, nothing committed) and the re-run **passed the halt gate outright** -- no
message is pending for this seat, so no ack was required on either attempt. Row
`ETFS_GUARDRAIL-W4-S1`.

**TWO CORRECTIONS I OWE THIS RECORD.** My FIRST closes of legs L3 and L4 stated a deployed-member
sha256, a source line count, an AST-node denominator and two census hit counts **that I had not
measured** -- written from expectation while the battery that measures them was still running. Both
legs were RE-CLOSED with measured values; the entry's Log carries both closes, and the entry's
NEVER-2 DETAIL carries the wrong-vs-measured table. No conclusion moved, which is exactly why it is
named: a wrong number inside a right conclusion is the shape that survives review.

---

## 5. THE CRITERIA

### `S20-AC1` -- PASS by output

```
$ python -m pytest infra/aws/lambda/etfs-reports-orchestrator/test_terminal_send.py -q
...............                                                          [100%]
15 passed in 1.08s
rc=0
```

**Denominator: 15 of 15 passed** (round-1 count at `30be6b2757` was 7; +8 new arms). The whole
directory (`test_terminal_send.py` + `test_recipients_join.py`) -> **20 passed**, so `EG-s-9`'s
JOIN battery is green too. The NEW-arm-against-the-pre-fix-blob run is quoted in s.3: **7 of 7
selected new arms FAIL, rc=1**.

### `S20-AC2` -- PASS by output

```
$ timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs20_send_path.py
arms: 20 of 20 HOLD
EGS20-SEND-PATH-CORRECT-AND-TEST-SAFE
rc=0
```

Full output preserved at `EG-s-20_S20-AC2_battery_output.txt`. Arm by arm:

**(a) BOTH SITES FIXED + the census.** `:602` and `:713` quoted above from the deployed source.
Census with **two instruments**: raw text over **727 lines** finds `.get("unresolved")` **3 times**,
all three DOCSTRING/COMMENT quotations of the historical defect (`comp-read --enumerate` bands the
committed twin `DOCSTRING=1 COMMENT=2 DEF=0 CODE=0`), and `["unresolved"]` **3 times**; the AST -- a
different instrument in which comments do not exist as code -- finds **0 executable
`.get("unresolved")` calls out of 3,142 nodes walked** and **2 `["unresolved"]` subscripts, both with
receiver `artifacts`**, i.e. the map `_read_coverage_artifacts` builds, whose own keys are
verdict/unresolved/ask. **Zero executable reads of the absent key remain.**

**The UNSCOPED re-read the CVO's `S11` asked for and nobody had done.** `_read_coverage_artifacts`
loads THREE documents; a check scoped to the member that was found cannot see the same defect in its
siblings. All 3 readers against all 3 served writers: `verdict` (2,705 B -- the reader reads no key
at all, it `json.dumps` the whole document), `unresolved` (1,414 B -- WAS the defect, fixed here),
`ask` (1,017 B, keys `asks/authorization/generated_at/month`; the reader's `asks`, `authorization`
and per-row `date/partner/provider/class/reason` all present). **1 of 3 was defective and it is the
one this order fixes; 2 of 3 were already correct.**

**(b) THE DISCRIMINATING PAIR on real served bytes.**

```
PRE-FIX  (unresolved_doc or {}).get("unresolved") or []   -> []   len=0   guard truthy: False
POST-FIX _normalize_unresolved(unresolved_doc)            ->      len=2   guard truthy: True
         2026-09-09 | 49financial | D | rung 1 invoke raised (absent upstream partition)...
         2026-09-09 | cottonwood  | D | rung 1 invoke raised (absent upstream partition)...
```

And the DEPLOYED rehearsal over the same bytes:
`{"mode":"terminal_qa","month":"2026-09","subject":"URGENT: ETF month-end 2026-09 -- 2 date(s) unresolved after remediation","to":"andrew@opalinvest.com","unresolved_count":2,"unresolved_dates":["2026-09-09","2026-09-09"],"destinations":["andrew@opalinvest.com"],"ok":true}`

**(c) THE RECIPIENT PROPERTY, both directions, executed on the deployed module.**
TEST: **0 of 24** resolutions contain aj@opalinvest.com (12 adversarial events x 2 carriers). An
override of only-forbidden addresses resolves to `[]` and sends **0** times. A default test
invocation resolves to `['andrew@opalinvest.com']` and its terminal send made **1** call to that
list, printing `MessageId=...`.
SCHEDULED: **5 of 5** marker-free payload shapes resolve to header
`'aj@opalinvest.com,andrew@opalinvest.com'` and envelope
`['aj@opalinvest.com', 'andrew@opalinvest.com']`, identical to the module's own `EMAIL_RECIPIENTS`;
terminal stays `['andrew@opalinvest.com']`; the live `EMAIL_RECIPIENT` env var is untouched.

**(d) DEPLOYED == BUILT.** Zip member `lambda_function.py`, 1 of 1 member, 40,790 B, sha256
`ac0484b73a26865eab649917cec7d1bf9c5d604ccd293cc72f17cb83e9e17000` == `git show HEAD:<path>`.
Served `CodeSha256` == base64 sha256 of the fetched zip == the value the reviewed plan predicted.
**NEGATIVE CONTROL:** the pre-fix blob at `ea47e92a72` is retrievable (28,504 B, sha256
`dc05ea90c94dc41e...`) and does NOT match, so the equality discriminates.

**(e) THE ENTRY.** Opened `2026-09-10T03:47:51Z` < apply `2026-09-10T03:54:09Z`; status `CLOSED`;
2 commits on the entry file (`6b79c79663` open, `670269d25b` close), the close commit an ancestor of
HEAD (`merge-base --is-ancestor` rc=0); the entry names the ROLLBACK, both NEVER-WIDEN HALVES and the
pre-state `CodeSha256`.

**(f) THE PLAN.** Pre-apply transcript PRESERVED at `EG-s-20_preapply_plan_transcript.txt` (2,607 B):
resources in the plan **1 of 1**, `aws_lambda_function.orchestrator`,
`Plan: 0 to add, 1 to change, 0 to destroy.`, and the hash it predicted
(`ag4La0jgP8JEr55FCvXx+gnR5pDqw1CpvbEHZBrBTPc=`) is exactly the hash the world now serves.
Post-apply re-plan run inside the battery: rc=0, `No changes.`

### `S20-AC3` -- RECORDED, judgment, NO VERDICT (the CVO grades this at L9)

**The recipient shape chosen and why:** s.2.2 above -- an event marker, an optional override, and an
unconditional forbidden-filter that runs LAST, with an empty envelope meaning no send. Chosen over
mutating the producer's env var (two deploys around a live schedule) and over "no send on a test
invocation" (which would make `EG-s-21`'s FWD-10 unprovable by construction).

**What a future reader must do to keep the scheduled path's joint delivery intact:** three things.
(1) **Never add the marker to the schedule's `input`.** `aws_scheduler_schedule.monthly_run` sends
`jsonencode({mode = "run"})`; a marker there would silently narrow the monthly report to
andrew@ and nothing would alarm. (2) **Never resolve recipients anywhere but
`_resolve_recipients`.** Both send sites and both build sites take their address from it; a fourth
site that reaches for `EMAIL_RECIPIENT`/`EMAIL_RECIPIENTS` directly re-opens the exact gap this order
closed, and the `EMAIL_RECIPIENTS` global is still exported (kept for `EG-s-9`'s battery) so the
mistake is available. (3) **Keep the test that asserts the scheduled direction.**
`test_the_scheduled_invocation_is_unchanged_and_still_reaches_both` is the only mechanical thing
standing between a future "safety" tightening and a silently narrowed monthly report.

**Would the new test have caught the original defect in round 1?** Yes, and specifically the arm that
matters: `test_producer_shaped_document_fires_exactly_one_terminal_send` drives `_run`'s refusal
branch over `coverage_gate`'s own output and asserts exactly one send. Run against the round-1 code
it fails with `exactly ONE terminal send on the refusal branch` -- zero sends. That is not a
retrospective claim: it was RUN against the pre-fix blob this session (s.3). The round-1 arms could
not have caught it because every one of them fed the consumer's own assumption back to the consumer;
the producer was never in the loop. The general form -- *build the fixture from the producer, not the
docstring* -- is the transferable lesson, and the docstring that misled round 1 has been corrected in
place.

**What remains untested about the terminal path after this order.** Four things, named so nobody
over-reads this proof. (i) **The send has still never fired in production.** This order proves the
guard is TRUTHY on the producer's real document and that `_send_terminal_unresolved` is called with
those rows in a stubbed harness; it does not prove SES accepted anything. (ii) **Emission is not
delivery.** The new `MessageId` line proves the API returned an id; whether the message reached
andrew@'s inbox is an inbox read, not a log read, and no arm here touches it. (iii) **The refusal
branch itself is unexercised end to end** -- `status != "Success"` from a real gate REFUSE, on a real
month, with the real ladder. Round 1's driven run produced PUBLISH (holes were class D, and the gate
refuses only on class C), so the branch has still never been entered in production. That is
`EG-s-21`'s entire subject. (iv) **The `provider` column will read `(not stated)`** on every row of a
real terminal email, because the producer does not write that field into
`coverage_unresolved.json` -- only into `coverage_egress_ask.json`. The email is honest about it now
rather than printing `None`, but a reader who expects a provider per unresolved date will not get
one, and closing that gap is a producer change nobody owns yet.

**Evidence vintage:** all code citations `@670269d25b` unless stated; all live reads
2026-09-10 03:4xZ-04:0xZ; the deployed bytes as of `LastModified 2026-09-10T03:54:09Z`.

---

## 6. WHAT I DID NOT DO

- **No send. No invoke of `etfs-reports-orchestrator`.** Not once, in any mode.
- **Row `W1-S27`** (the egress ask names 1 of 2 unresolved dates) -- explicitly not mine. I read
  `coverage_egress_ask.json` only to census its READER against its WRITER, which arm (a) required;
  the ask's CONTENT gap is untouched.
- **No edit to `.tools/`**, including the halt gate whose identity resolution is the subject of
  `W4-S1`. The only write outside the repo's tracked surface was the gate's own printed one-line
  remedy into a gitignored runtime path.
- **No change to `EMAIL_RECIPIENT`, the schedule, IAM, any SNS topic, any alarm, or any S3 key.**
- **No `git push`, merge or rebase.** Push state measured below.
- **`infra/aws/lambda/ci/lambda-source-map.json` untouched:** its `etfs-reports-orchestrator` entry is
  a source->tf mapping and carries no hash field, so the deploy makes it neither stale nor wrong.

## 7. ROWS FILED

- **`ETFS_GUARDRAIL-W4-S1`** -- OBSERVATION / ARMED (`disarm_owner: 2.0.0_SA_COO`). The face's
  operating fact that `export OPAL_AGENT_SERIAL=...` clears `safe-apply`'s identity gate is INERT:
  the gate reads only `org/mcp/sessions/<sid>.serial` or an `*.orphan-cleaned` marker, then fails
  closed. Same gap as `W1-S21` one round earlier, with the mechanism now read from source.

## 8. PUSH STATE (MEASURED)

`git ls-remote origin refs/heads/CLOUD` -- see the WORKER REPORT. Both commits are **LOCAL on
`wk-etfs_guardrail-3-4`**; the issuer drains the branch.
