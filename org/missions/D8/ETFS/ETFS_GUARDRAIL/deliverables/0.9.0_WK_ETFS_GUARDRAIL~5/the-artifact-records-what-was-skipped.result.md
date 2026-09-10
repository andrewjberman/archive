# EG-s-26 RESULT -- THE ARTIFACT RECORDS WHAT WAS *SKIPPED*

**TO:** `ETFS_GUARDRAIL.TO-EG-s-26` | **cell:** `EG-s-26` | **outcome_ref:** FWD-9
**assignee:** `0.9.0_WK_ETFS_GUARDRAIL~5` (RE-SEAT after the 2026-09-10T06:43:35Z device crash)
**branch:** `wk-etfs_guardrail-3-5` | **face vintage:** `d3a33a1189` (the CORRECTED face, merged into
this branch at `82b580243e` before any grading read)

---

## WHAT THIS RE-SEAT INHERITED, AND WHAT IT DID NOT DO

My predecessor on this slot committed the code at `5b15b09834` and put the bytes to the artifact key
at `2026-09-10T06:40:10Z`. At `06:43:35Z` an RMM agent rebooted the device and an OS upgrade followed,
killing the session. It left behind: a **world-done deploy**, an **uncommitted** NEVER-2 entry with
five open legs, and an **untracked** evidence file whose own verifier had recorded the deploy as
failed.

**THE DEPLOY WAS NOT RE-EXECUTED.** CLAUDE.md NEVER-2: an entry a device left OPEN proves only that
THIS device saw no completion; measure the ARTIFACT, and world-done closes SUPERSEDED, because a
re-execute of an overtaken promote is a REWIND. Every AWS call this re-seat made is a READ.

---

## `S26-AC1` -- PASSES BY OUTPUT

```
invocation: timeout 600 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/test_egs26_artifact_records_the_skip.py
rc:         0
deciding:   EGS26-SKIP-DISCLOSED-IN-ONE-READ
denominator: 6 of 6 arms hold, 0 failure lines
output:     org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~5/egs26_battery_output.txt
```

| arm | the deciding numbers, each beside its denominator |
|---|---|
| (a) | PREMISE on the DEPLOYED PRE object (VersionId `V1i.w8DNP2iqwsiiRYC7k40Neh90w3DH`, 66756 B): **8 of 8** skip tokens ZERO on BOTH counting methods over 1233 lines / 66756 bytes, against **5 of 5** positive controls NON-ZERO (`forced` 9, `mechanism` 2, `forcing` 6, `run_id` 27, `verdict` 26). LANDING half on POST (69879 B): **8 of 8** PRESENT. |
| (b) | Driven through the REAL `main()`, `--gate --no-ladder --fixture-remove`: rc 3, **0 of a permitted 0** producer invokes, **4** keys written to the recording stub and **0 of 4** is `coverage_egress_ask.json`. Artifact printed whole (2375 B). |
| (c) | Both branches through the SAME writer over the SAME fixture, only the flag differing: **7 of 14** `forcing` keys differ; **0** keys exist ONLY in the skipped record. |
| (d) | **7** top-level keys MINUS `forcing` = **6** others scanned for any of the **10** half-keys -> **0** leaks. Both halves in one object. |
| (e) | 2 scenarios x 2 ladder branches x 7 quantities = **28 of 28** IDENTICAL, plus **4 of 4** invoke counts. Comparator negative control: PUBLISH vs REFUSE, so it CAN report a difference. |
| (f) | Served sha256 = committed sha256 (`9b9cdd9c...`), prior (`b08a646d...`) DIFFERS. **1 of 7** artifact keys changed during the act, **0 of 7** since. **0 of 36** keys moved under `platinum/reports/`. **0** SES datapoints overlap the act window (whole-day Send total 7.0, all in other buckets). **0** invocations across **13 of 203** account functions; **0 of 11** act steps called anything but `s3api`/`cloudwatch`. |

---

## `S26-AC2` -- JUDGMENT, RECORDED, NOT SELF-GRADED

**For `3.0.0_SA_CVO` at L9. No verdict is offered here and none should be read into it.**

### (1) THE FIELD'S SHAPE, AND WHY A READER CAN TRUST IT

The skip record lives **inside the existing `forcing` object** of `coverage_verdict.json`, beside
`forced`. Five structured keys plus one derived line:

| key | type | ladder RAN | ladder SKIPPED |
|---|---|---|---|
| `ladder_ran` | bool | `true` | `false` |
| `ladder_skip_mechanism` | str | `"none"` | `"--no-ladder"` |
| `rung3_stop_and_ask_reachable` | bool | `true` | `false` |
| `coverage_egress_ask_possible` | bool | `true` | `false` |
| `skip_note` | str | names the artifact, says the absence would NOT be structural | names the artifact, says ABSENT BY CONSTRUCTION |
| `run_shape` | str (DERIVED) | `"... and LADDER RAN"` | `"... and LADDER SKIPPED (--no-ladder; ...)"` |

`disclosure_version` moved `"1"` -> `"2"`, which is what that field exists for.

**FOUR REASONS A READER CAN TRUST IT, each with the failure it forecloses.**

**(i) EVERY KEY IS PRESENT ON BOTH BRANCHES.** A field that appears only when the ladder was skipped
is not a disclosure: the reader cannot distinguish *"this run ran the ladder"* from *"this run did not
say"*. That is exactly why `forced: false` had to exist in EG-s-25, and the same argument binds here.
Arm (c) checks it by SUBTRACTION rather than by assertion -- `set(skipped) - set(ran)` is empty, 0
keys -- so a future edit that reintroduces a skipped-only key fails the arm.

**(ii) THE WORDING IS DELIBERATELY WEAKER THAN THE OBVIOUS WORDING, AND THAT IS THE POINT.** The keys
say `rung3_stop_and_ask_reachable` and `coverage_egress_ask_possible`, never `ran` and `written`. On
the ladder-RAN branch rung 3 is called at `remediate.py:284` only `if unresolved and not dry_run`, and
its write at `:189` is further conditional on `(asks or pruned_own)`. So on the very branch those
stronger words would describe, they would be **FALSE**. A record that overclaims on one branch is
worse than no record, because it is trusted. Arm (c) pins this: the ran-branch `skip_note` must
contain *"may or may not have been written"*.

**(iii) THE COST IS NAMED IN PROSE, NOT LEFT AS AN INFERENCE.** `skip_note` on the skipped branch
names `coverage_egress_ask.json` by filename and says `ABSENT BY CONSTRUCTION ... not absent because
nothing needed asking`. Without that sentence, a reader would have to already know that `--no-ladder`
bypasses `remediate_month` entirely, that rung 3 is inside it, and that rung 3 is the sole writer of
that key -- three facts spread across two modules. This was the widening `0.9.0_WK_ETFS_GUARDRAIL~4`
found and the issuer's original boundary missed.

**(iv) THE RECORD IS ADDITIVE AND PROVEN NOT TO MOVE THE DECISION.** Arm (e) re-computes over the same
inputs with the DEPLOYED PRE bytes as the "before" side -- loaded from S3 by version id, not
reconstructed -- and gets 28 of 28 quantities identical on BOTH ladder branches, with a negative
control showing the comparator can report a difference. The `verdict = "REFUSE" if any_c else
"PUBLISH"` rule and the `:993-:999` ladder branch are untouched; in particular the `:999` re-classify
is untouched, that being SHAPE 2, which the CTO refused.

**THE HONEST LIMIT OF (i)-(iv):** they establish that the record is *internally* trustworthy and
*decision-neutral*. They do NOT establish that the record is TRUE of a live box run, because this cell
fired none -- see the exclusions and residual (3) below.

### (2) CONSUMER CENSUS -- MEASURED, WITH A DENOMINATOR, NOT RECALLED

```
comp-find "coverage_verdict" --all --corpus default
DENOMINATOR: 263 hit(s) across 29,741 file(s) scanned  [corpus=default]
             1 UNREADABLE not searched | 1,782 BINARY not searched
BANDS: SURFACED=54  CONFIG=29  TEST=24  DOC=156
DISTINCT FILES with a hit: 89 -- of which 30 are code (.py/.sh/.ts/.tsx/.js/.tf) and 59 are not
```

**A FALSE ZERO CAUGHT ON THE WAY, and it is worth stating because the number above would otherwise be
unearned:** my first census ran `comp-find "coverage_verdict" --all --scope all` and returned
`0 hit(s) across 0 file(s)`. `--scope` is not a comp-find flag; it was eaten as a PATHSPEC. The
discriminator is not the hit count -- it is the **SCANNED** count. `0 hits across 0 files` is
out-of-corpus, never absence.

**NARROWING THE 30 CODE FILES BY SUBTRACTION, never by a forward list of what I remembered:**

| bucket | n | which |
|---|---|---|
| `.scratch/` copies of the renderer or of my own tooling | 18 | not consumers; several ARE the renderer's own bytes under other names |
| the WRITER | 1 | `data/etfs/scripts/presentation/render_month_end.py:1179` |
| test batteries (mine and siblings') that assert on the object | 9 | `tests/test_coverage_gate.py`, `test_egs15/16/20/21/22/23/25/26_*.py` |
| the orchestrator and its own test | 2 | `infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`, `test_terminal_send.py` |
| **30 MINUS 18 MINUS 1 MINUS 9 = 2** | **2** | and only ONE of those is a production consumer |

**THE ONE PRODUCTION CONSUMER, READ AT SOURCE.**
`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:327-343` (`_read_coverage_artifacts`)
does `json.loads(body)` into `out["verdict"]`, wrapped in a bare `except Exception` that returns
`None`, because *"absence of any object is the ORDINARY case"*. The parsed document is then used at
exactly two sites, `:685-689` and `:805`:

```python
if artifacts["verdict"] is not None:
    message += f"\n\nCoverage verdict: {json.dumps(artifacts['verdict'])}"
```

**IT NEVER INDEXES INTO THE VERDICT DOCUMENT.** There is no `["forcing"]`, no `.get("verdict")` on the
parsed body, no schema check, no key allow-list. The whole document is re-serialised into an alert
message body. **So a new key cannot break this consumer**: there is no key it reads that a new sibling
key could shadow, and no strict parse that an unknown key could fail.

**BUT IT IS NOT WITHOUT EFFECT, AND THIS IS THE PART A "cannot be broken" ANSWER WOULD HIDE.** Because
the consumer prints the document WHOLE, every key I added lands verbatim in the render-FAILED alert
body. `skip_note` and `run_shape` are long prose strings; the artifact grew from 1,225-2,705 B class
to 2,375 B on the arm (b) run with five keys added. The alert gets longer and more verbose on every
REFUSE. I make no judgement about whether that is good or bad -- it is a consequence of the shape the
CTO's condition (i) requires (one field family, one read), and the CVO should see it stated rather
than discover it in an inbox.

**AND NOTE THE CONTRAST WITH THE SIBLING DOCUMENT, which is the reason this census is not academic:**
`coverage_unresolved.json` IS indexed by this same consumer, and EG-s-20 rows `W1-S25`/`W1-S29`/`S11`
record that both sites read a key `"unresolved"` the producer never writes -- the served document is
keyed by PARTNER -- so the guard was falsy against real bytes and the ONE terminal send was skipped on
a genuine REFUSE. That is precisely the failure mode a key-indexing consumer has and a
whole-document-printing consumer does not. The verdict document's consumer is safe **for a structural
reason**, not by luck, and I checked which it was.

### (3) WHAT A READER STILL CANNOT TELL FROM THE ARTIFACT AFTER THIS CHANGE

**Six residuals, named rather than implied.**

**(R1) WHETHER RUNG 3 ACTUALLY RAN ON A LADDER-RAN RUN.** The record says `reachable`, and reachable
is not ran -- deliberately (see (1)(ii)). A reader who wants that fact must look for the presence of
`coverage_egress_ask.json` beside the verdict, and the artifact does not tell them the answer, only
that the question is meaningful on that branch. On the SKIPPED branch there is no residual: absence is
structural and the artifact says so.

**(R2) WHETHER RUNGS 1 AND 2 DID ANYTHING ON A LADDER-RAN RUN.** `ladder_ran: true` says the ladder
was invoked, not what it achieved. Rung counts live in `ladder_result` inside the gate and are not
surfaced in `forcing`; `unresolved` carries what remained, not what was repaired. A run that fixed
four days and a run that fixed none both read `ladder_ran: true`.

**(R3) WHY THE LADDER WAS SKIPPED, AS OPPOSED TO HOW.** `ladder_skip_mechanism` records the FLAG.
Nothing records the human reason -- QA rehearsal, a driven demonstration, an operator's caution. Two
runs with identical artifacts can have been fired for opposite reasons.

**(R4) WHETHER THIS PARTICULAR RECORD IS TRUE OF A LIVE BOX RUN.** Every artifact in this battery was
produced hermetically through the real `main()` with S3 and Lambda stubbed, because the order's BOUNDS
forbid a box run and reserve the one driven run for `EG-s-21`. The bytes that produce these records
ARE the served bytes (arm (f), sha256 both sides), and the writer path exercised IS `main()`'s own --
but **DEPLOYED-VERIFIED is not EXERCISED-IN-PRODUCTION**, and no reader should upgrade it. `EG-s-27`
is the cell that carries the forced run on which this record rides.

**(R5) THE THIRD WAY A DRIVEN RUN CAN DIFFER FROM AN ORGANIC ONE.** This cell closed FORCED INPUT
(EG-s-25) and SKIPPED PROCESSING (EG-s-26). A driven run can also differ in its **recipients** and in
its **schedule provenance** -- whether it fired from cron or from a manual invoke, and to whom the
terminal message went. Nothing in `forcing` records either. `run_id`/`run_id_source` join the artifact
to a run's stdout, which is where that would be recovered, if the log survived. I name this because a
two-member enumeration of "how a driven run differs" is exactly the shape Rule 24 says to hunt by
subtraction, and I could not subtract from a printed denominator here -- there is no census of ways a
run can diverge, only the two the rulings have found so far. **That absence of a denominator is
itself the residual**, and I would rather say so than present two as if it were all.

**(R6) THE RECORD IS SELF-REPORTED BY THE RUN IT DESCRIBES.** `forcing` is written by the same process
whose configuration it discloses. A run that was patched to lie, or a stale renderer on the box, would
produce a confidently wrong record; nothing in the artifact cross-checks it against an independent
observer. `disclosure_version` and the NEVER-2 deploy evidence are the only things that let a reader
date the writer, and arm (f)'s sha256 equality is what ties this record to bytes anyone can re-hash.

---

## BOUNDS OBSERVED

- **No send, no orchestrator invoke, no box run, no write under `platinum/reports/`** -- proven, not
  asserted: arm (f) measures 0 of 36 keys moved under `platinum/reports/` across the act AND the crash
  window, 0 SES datapoints overlapping the act window on a whole-day enumeration, 0 invocations across
  13 of 203 account functions, and 0 of 11 act steps calling anything but `s3api`/`cloudwatch`.
- **`infra/aws/lambda/etfs-reports-orchestrator/` NOT TOUCHED** -- `EG-s-27`'s surface. It is READ in
  this document (the consumer census) and not modified.
- **The verdict logic and the ladder are NOT changed** -- arm (e), 28 of 28 quantities identical on
  both branches. The `:999` re-classify is untouched; that is SHAPE 2 and it is REFUSED.
- **aj@opalinvest.com is not a recipient of any driven run** -- this cell fires none.

## ROWS FILED

| id | class / hazard | one line |
|---|---|---|
| `ETFS_GUARDRAIL-W5-S8` | OBSERVATION / ARMED (disarmed this turn for the instance) | the deploy verifier hashed the PREVIOUS cell's download, rc=0 throughout, and wrote `served_equals_committed: false` about an object it never read |
| `ETFS_GUARDRAIL-W5-S9` | OBSERVATION / INERT | arm (a)'s "as currently served" stopped naming the object carrying the absence, because this cell's own deploy replaced it before the battery existed |
| `ETFS_GUARDRAIL-W5-S10` | OBSERVATION / INERT | the NEVER-2 entry could not be "closed BEFORE the grading reads": the device died between the act and its record, 5h21m past a 4h window, with the act world-done throughout |
