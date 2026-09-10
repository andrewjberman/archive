# ETFS_GUARDRAIL.TO-EG-s-21 -- THE DRIVEN REFUSAL: result

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` · **Branch:** `wk-etfs_guardrail-3-21` · **Base/HEAD at work:** `a6e2031ff8`
**Task order vintage:** `org/missions/D8/ETFS/ETFS_GUARDRAIL/task-orders/ETFS_GUARDRAIL.TO-EG-s-21.the-driven-refusal.md`@`a6e2031ff8`
**Decomp:** `org/missions/D8/ETFS/ETFS_GUARDRAIL/decompositions/ETFS_GUARDRAIL_DECOMP.md`@`9c74724d7d`, cell `EG-s-21`
**Worked:** 2026-09-10 ~18:2xZ - ~19:0xZ

---

## CONCLUSION, FIRST

**THE DRIVEN RUN WAS NOT FIRED. THE ROUND'S SINGLE PERMITTED DRIVEN RUN IS STILL UNSPENT.**

`S21-AC1` is **FAIL** -- the battery ran, arm (a) PASSED, and arms (b)-(g) are `NOT-RUN-BLOCKED`. The
token `EGS21-REFUSAL-DRIVEN-AND-SENT` was not printed, rc=1.

The reason is not the recipient bound and it is not the forcing design. Both of those are clean and both
are recorded below. The reason is that **the path this order drives cannot reach a REFUSE verdict on the
bytes the reporter box will execute.** The served renderer calls `remediate._provider_for(p)` at
`data/etfs/scripts/presentation/render_month_end.py:1162` on the `--no-ladder` branch -- which R-EG-6
shape 1 makes the ONLY branch that yields a driven REFUSE -- and the `coverage` package the box holds
does not define that symbol. Exercised: `AttributeError`, raised inside `coverage_gate` **before any
verdict object exists**. Firing would have spent the irreplaceable run on an SSM `Failed` that writes no
`coverage_verdict.json`, no refusal artifacts and fires no terminal send.

**Row `ETFS_GUARDRAIL-W4-S17`** -- BLOCKING / ARMED, `disarm_owner` `2.0.0_SA_COO`.

**Nothing was written to S3. Nothing was deleted. No SES message was sent. No code was changed.
No NEVER-2 change-management entry was opened** -- an entry names an act's blast radius, and there was no
act; an entry opened and never closed is itself the hazard CLAUDE.md NEVER-2 names.

---

## 1. THE BOUND WITH NO OVERRIDE: `aj@opalinvest.com` -- CLEAN, AND MEASURED FIRST

Taken **before** any invocation, on the bytes deployed **at this run's time**, and re-read after (the
battery re-takes it end to end on every run; the last run is the record).

**GRAIN.** `aws lambda get-function` -> `Code.Location` -> the zip downloaded and hashed:

```
deployed zip sha256=9e3becb33921248e1df978fd48e996672e10d0d018290bc74ef06095b7768b95
base64 njvsszkhJI4d+Xj9SOmWZy4Q0NAYKQvHTvBglbd2i5U= == CodeSha256, LastModified=2026-09-10T17:44:50.000+0000
```

The digest of the bytes I read equals the `CodeSha256` the service reports, so the object I read IS the
object that runs. Its single member `lambda_function.py` is **byte-identical** to
`infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py`@`a6e2031ff8` LF-normalized (both
`sha256 9337c58c31a04e0b845d72b583c1a7f6250a3ae03455576275ff037d9bacfd4f`). These are EG-s-30's bytes,
exactly as the face said; that is not re-derived here, it is confirmed as the grain of everything below.

**TWO INSTRUMENTS, ON DIFFERENT SUBSTRATES, EACH WITH A LIVE NEGATIVE CONTROL.**

*Instrument 1 -- offline, the deployed artifact executed with the live `EMAIL_RECIPIENT`
(`'aj@opalinvest.com,andrew@opalinvest.com'`).* Four adversarial test events x two call sites
(`report` base = `EMAIL_RECIPIENT`, `terminal` base = `TERMINAL_RECIPIENT`), including
`test_recipients: ["aj@opalinvest.com"]`, mixed case `"AJ@OpalInvest.COM"`, and a joined RFC 5322 string:

```
offline instrument on deployed bytes: aj@ hits 0 of 8 adversarial TEST resolutions
negative control LIVE: scheduled report envelope=['aj@opalinvest.com', 'andrew@opalinvest.com'] (carries aj@),
                       scheduled header='aj@opalinvest.com,andrew@opalinvest.com'
```

The `test_recipients: ["aj@opalinvest.com"]` case resolves to header `''` and envelope `[]` -- the
"filters away to empty, and an empty envelope is NO SEND" property the code claims, observed.

*Instrument 2 -- the RUNNING function, live, send-free `recipients_qa` with an adversarial probe.*
Different substrate (the deployed process with its own environment, not my copy of its bytes):

```
test={"report": ["andrew@opalinvest.com"], "terminal": ["andrew@opalinvest.com"]}
scheduled={"report": ["aj@opalinvest.com", "andrew@opalinvest.com"], "terminal": ["andrew@opalinvest.com"]}
```

**Why the negative control matters more than the zero.** A resolver that returned `[]` for everything
would also produce "0 aj@ hits". The scheduled branch DOES return `aj@opalinvest.com` on both
instruments, so the instrument can express the failure and its zero on the test branch is
discriminating rather than vacuous.

`EG-s-20` terminal, its flip cited: `<status>complete -- 2026-09-10 ~04:0xZ by 0.9.0_WK_ETFS_GUARDRAIL~4 ...`,
flip commit `9e3040a75f6b882648e1b3d4f3a9946ee32e1ad5` (2026-09-10T00:22:06-04:00).

**Arm (a) PASSES.** The bound is satisfied and it is not what stopped this order.

---

## 2. WHAT STOPPED IT: A SHARED DEPENDENCY UNDER TWO CORRECTLY-VERIFIED FILES

### 2.1 The measurement

`aws s3api list-objects-v2 --bucket opal-313476888478-lambda-artifacts --prefix ec2/etfs-reports`
-- **denominator 7 objects**, printed in full by the battery:

| key | size | LastModified |
|---|---|---|
| `ec2/etfs-reports/render_month_end.py` | 77130 | **2026-09-10T14:09:53.000Z** |
| `ec2/etfs-reports/coverage/classifier.py` | 10157 | **2026-09-05T06:53:40.000Z** |
| `ec2/etfs-reports/coverage/remediate.py` | 11011 | **2026-09-05T06:53:44.000Z** |
| `ec2/etfs-reports/coverage/__init__.py` | 89 | 2026-09-05T06:53:37.000Z |
| `ec2/etfs-reports/coverage/trading_calendar.py` | 6979 | 2026-09-05T06:54:58.000Z |
| `ec2/etfs-reports/coverage/_orion_vendor_asof.py` | 6979 | 2026-09-05T06:55:02.000Z |
| `ec2/etfs-reports/probe.sh` | 2177 | 2026-06-25T23:23:06.000Z |

Byte comparison against repo HEAD `a6e2031ff8` (LF-normalized):

```
SERVED render_month_end.py sha256=ba410ee5c9c4263e8fe37ade171aa4d61f834df246d0f57f30299dbba03a031a  == repo(LF): True
coverage/classifier.py      deployed= 10157 repo= 12226 IDENTICAL=False
coverage/remediate.py       deployed= 11011 repo= 16550 IDENTICAL=False
```

Top-level defs enumerated rather than grepped:

```
DEPLOYED remediate defs: ['_slice_exists', 'rung3_stop_and_ask', 'remediate_month', '_main']
REPO     remediate defs: ['_provider_for', '_slice_exists', '_read_prior_asks', 'rung3_stop_and_ask', 'remediate_month', '_main']
```

`_provider_for` -- the symbol EG-s-29 added the call to -- is **ABSENT** from the deployed package.

### 2.2 The exercise, with a difference control

Reading is not enough for a claim this expensive, so the battery **runs** the served renderer's
`--no-ladder` gate branch twice: once over the DEPLOYED `coverage` package, once over the REPO one.
Same renderer file in both arms; the package is the only variable. Zero AWS calls (stub probe, supplied
series, module `s3` replaced by a capturing stub):

```
[DEPLOYED] remediate=coverage has _provider_for=False; 21 trading slices, 20 after forcing
[DEPLOYED] coverage_gate RAISED: AttributeError: module 'coverage.remediate' has no attribute '_provider_for'
[DEPLOYED]   at provider_for_partner = remediate._provider_for(p)
[REPO] remediate=coverage has _provider_for=True; 21 trading slices, 20 after forcing
OK: s3://opal-data-etfs/platinum/reports/2026-08/coverage_egress_ask_ladder_skipped.json (rung-3-EQUIVALENT egress ask, ...)
[REPO] VERDICT=REFUSE holes=1 C=1 puts=['platinum/reports/2026-08/coverage_egress_ask_ladder_skipped.json']
DEPLOYED-package result="AttributeError: ... no attribute '_provider_for'" ; REPO-package result='REFUSE' ;
difference control discriminates=True
```

The forcing design is **correct** -- it yields exactly the driven REFUSE the order wants, with `C=1`
and the arm-(d) egress ask written by EG-s-29's rung-3-equivalent. It is the *substrate* that cannot
run it.

### 2.3 Why the box cannot already be repaired -- by subtraction over both branches, not by assumption

1. **The box is stopped and has been since before the symbol existed.**
   `i-070477bf35fc54409 state=stopped LaunchTime=2026-09-10T01:19:07.000Z
   reason='User initiated (2026-09-10 01:20:29 GMT)'`; `ssm describe-instance-information` returns
   **0 rows**. A stopped instance's filesystem cannot be written. `_provider_for` first entered the repo
   at `7e544cb4d7`, committer date `2026-09-10T08:33:05-04:00` = **12:33:05Z** -- eleven hours after the
   box stopped. So no pre-stop copy on that box can contain it.
2. **If `/opt/etfs-reports/coverage/` is ABSENT, the self-bootstrap pulls from the same stale prefix.**
   `render_month_end.py:118-129` fires `aws s3 cp --recursive .../ec2/etfs-reports/coverage/` only on
   `ImportError` -- and that prefix is the 2026-09-05 copy measured above.

Both branches of the only unknown land on a `remediate.py` with no `_provider_for`, so **the unknown is
closed rather than assumed**. This is the one place I did not have a direct instrument (I did not boot
the box: stopping an EC2 is a human-confirmation act under CLAUDE.md, and the subtraction answers the
question without one).

**A consequence worth stating for whoever remediates:** re-uploading `coverage/*.py` to the artifact
prefix is **necessary but not sufficient**. The bootstrap fires only on `ImportError`, so an *existing*
box directory is never refreshed by a run. Two acts, not one.

### 2.4 What firing anyway would have cost -- measured, not predicted

```
POSITIVE CONTROL platinum/reports/2026-08/coverage_verdict.json
    -> PRESENT LastModified=Thu, 10 Sep 2026 00:24:44 GMT ETag="6d13a29621407b94c876b9a60677ea4b"
       VersionId=<ABSENT -- opal-data-etfs is UNVERSIONED>
TARGET           platinum/reports/2026-08/coverage_unresolved.json
    -> ABSENT-OR-ERROR (aws rc=255: An error occurred (404) when calling the HeadObject operation: Not Found)
(control PRESENT + target ABSENT => the absence is the OBJECT'S, not the CALL'S)
```

The `AttributeError` exits the renderer non-zero, so the orchestrator takes its `status != "Success"`
branch (`lambda_function.py:889`). There it reads the month's existing coverage artifacts; 2026-08's
`coverage_unresolved.json` is a measured 404, `_normalize_unresolved(None)` returns `[]` on the deployed
handler, and the ONE terminal send is gated on `if unresolved_days:`. **So FWD-10's send would not fire
either.** The run would have produced an SNS "render FAILED" alert and nothing else -- and would have
left a `refused/`-free month whose `coverage_verdict.json` still reads `PUBLISH` from 00:24:43Z, which a
later reader could easily mis-join to my run. That is the waste row `W4-S6` exists to prevent.

### 2.5 The scope of the break, stated so it is not read wider than it was measured

**The scheduled (ladder-ON) monthly fire is NOT broken by this.** `remediate_month`'s signature is
character-identical between the deployed and repo copies, and `classifier.py`'s def list is identical
(`['_month_dates','_load_series','classify_month','summarize','coverage_line','_main']` on both sides;
the size delta is EG-s-22's additive `slice_on_closed_day`). Only the `--no-ladder` branch crashes.

A second, non-blocking consequence of the same staleness: the deployed `remediate_month` predates
EG-s-28, so an **organic** refusal rendered from this box would still carry unresolved rows with no
`provider` -- the very defect EG-s-28 and EG-s-29 closed in the repo.

### 2.6 THIS IS THE SECOND EXECUTION OF THIS ORDER, AND IT CONTRADICTS THE FIRST -- HERE IS WHY BOTH ARE RIGHT

The same slot executed `EG-s-21` earlier today (`a02bc48b98`, 2026-09-10T12:48:56-04:00; drained
`f1f5eef023` with the order STILL OPEN). It also refused to fire, on a different ground -- FWD-9's
accept named a 404 no month could produce -- and `R-EG-9` then re-cut arm (d) off that 404, which is why
this face was re-dispatched. **Its deliverables at those paths are overwritten by this execution; the
prior versions stand in git at `a02bc48b98`.** My `EG-s-21_S21-AC1_battery_output.txt`,
`test_egs21_driven_refusal.py` and this file replace them.

That result states, at its s.3: *"forcing ENGAGED ladder=False -> VERDICT=REFUSE holes=1"*, and its
grounding table records the served renderer's identity exactly (`ba410ee5c9c4263e...`, 77,130 B,
LastModified 2026-09-10T14:09:53Z) with an explicit and correct GRAIN NOTE that a `file:line` citation
into the repo file resolves to the bytes the box pulls. **Every one of those statements is true.**

**The two measurements do not conflict; they are on different substrates, and mine is the one the box
executes.** That battery loaded the served renderer *in this repo checkout*, where
`render_month_end.py:115-119` puts `data/etfs/scripts/` on `sys.path` and
`from coverage import classifier, remediate` therefore resolves to the **repo** package -- the
`REPO-package` arm of my difference control, which returns `REFUSE holes=1` for me too. The box resolves
the SAME import against `/opt/etfs-reports/coverage/`, whose only supply is the 2026-09-05 artifact
prefix. The prior execution verified the served RENDERER and was right about it; it did not verify what
the renderer IMPORTS, and neither did EG-s-29 or EG-s-30. The GRAIN NOTE is exactly right about
`render_month_end.py` and silent about the package beneath it -- which is why this needed a second
instrument rather than a second reading.

### 2.7 The shape of the defect

EG-s-29 verified its own served file. EG-s-30 verified its own served file. **Both were right.** The
defect lives in what those files SHARE, and no per-file check could see it -- CLAUDE.md Rule 22's
shared-dependency clause landing exactly as written: *"A CHECK SCOPED TO THE MEMBERS CANNOT SEE A DEFECT
IN WHAT THE MEMBERS SHARE."* The face's "TWO THINGS LANDED AFTER THIS FACE WAS CUT" section correctly
told me not to re-derive that `render_month_end.py` and the orchestrator are served and current. They
are. The renderer is simply not self-contained.

---

## 3. THE FORCING DESIGN, RECORDED SO A RE-CUT NEED NOT RE-DERIVE IT

Chosen and exercised, never executed against the world.

- **Month `2026-08`.** Its served `coverage_verdict.json` (LastModified 2026-09-10T00:24:44Z, generated
  2026-09-10T00:24:43.743827+00:00) reads `verdict=PUBLISH holes=0` with **21 of 21 trading days
  `COVERED` for all three partners and zero B/C/D/UNKNOWN**. An unambiguous prior verdict is exactly
  what arm (f)'s before/after needs, and August carries no organic noise to confound the forced hole.
- **Partner `cottonwood`.** `render_month_end.py:847-850` makes only `cottonwood` and `49financial`
  probe-capable. This matters and is easy to get wrong: a non-probe-capable partner's missing day
  classifies **UNKNOWN**, and `coverage_gate` sets `any_c` only on class **C**, so forcing Inflection
  would have produced a hole and a **PUBLISH** verdict.
- **Slice `2026-08-14`, spec `cottonwood:2026-08-14`.** One trading day, one slice, in memory only.
- **REJECTED, and why:** (i) editing or deleting any served object of a real month -- forbidden outright
  by the order and by NEVER-AUTO-DELETE, and unnecessary because `--fixture-remove` reaches the
  classifier's real code path without touching S3; (ii) a month with no served publish keys -- there is
  none that also carries removable slices (the face records 404-able 0 of 5), and arm (d)'s
  unmoved-`LastModified` discriminator needs the publish keys to EXIST; (iii) 2026-09 -- in progress,
  and its 2026-09-10T01:20Z run already left `coverage_unresolved.json` and `coverage_egress_ask.json`
  in place, so a forced run's artifacts could not be told from the organic ones without extra argument.
- **The undo is structural.** `--fixture-remove` mutates only the in-process `daily` dict
  (`render_month_end.py:441-449`, *"nothing on S3 is ever touched"*) and the flag is per-invocation.
  There is no persistent state to reverse; arm (f)'s proof is the classifier re-run on the same inputs
  without the flag, which is a local read.
- **Blast radius that the NEVER-2 entry would have named** (recorded here because the entry was
  correctly not opened): on the REFUSE branch `platinum/reports/2026-08/{coverage_verdict.json,
  coverage_unresolved.json, coverage_egress_ask_ladder_skipped.json, refused/etf_ownership.html,
  refused/opaletfs_*_202608.csv}`; **on the PUBLISH branch the same `coverage_verdict.json` PLUS the
  served publish keys `etf_ownership.html`, `etf_ownership.pdf` and the three `opaletfs_*_202608.csv`
  -- overwritten with FORCED, data-removed content.** The bucket is unversioned, so that rollback is a
  re-render of 2026-08 unforced, not a version restore. That second branch is the whole reason the
  sign-off must name the radius and not the producer's decision.

**How to confirm the disarm rather than assume it:** after the coverage package is redeployed AND the
box re-pulls it, re-run this battery. Its DEPLOYED arm must print `VERDICT=REFUSE holes=1` instead of
the `AttributeError`. The difference control is already built and already discriminates.

---

## 4. CRITERIA

### `S21-AC1` -- **FAIL**

`invocation`: `timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs21_driven_refusal.py`
`expect`: `EGS21-REFUSAL-DRIVEN-AND-SENT` -- **NOT PRINTED**, rc=1.

```
ARM a    PASS             the test-invocation recipient path CANNOT reach aj@opalinvest.com on the bytes
                          deployed at this run's time; two instruments, both with a live negative control
ARM b    NOT-RUN-BLOCKED  the forcing's DISCLOSURE is read from a produced artifact; no artifact is produced
ARM c    NOT-RUN-BLOCKED  coverage_verdict.json is never written -- coverage_gate raises before it returns
ARM d    NOT-RUN-BLOCKED  no refusal artifacts and no egress ask exist to head-object
ARM e    NOT-RUN-BLOCKED  the terminal send guard is False (coverage_unresolved.json 404 -> [])
ARM f    NOT-RUN-BLOCKED  there is no forcing to undo -- the run did not happen
ARM g    NOT-RUN-BLOCKED  the run wrote no keys, so there is no write enumeration to make
ARM PRE  BLOCKING         DEPLOYED-package result="AttributeError: ... no attribute '_provider_for'" ;
                          REPO-package result='REFUSE' ; difference control discriminates=True

S21-AC1 RESULT: FAIL -- token NOT printed.
```

**Denominator: 1 of 7 arms holds (a); 6 of 7 NOT-RUN-BLOCKED.** Full transcript:
`org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/EG-s-21_S21-AC1_battery_output.txt`.

### `S21-AC2` -- RECORDED, NO VERDICT (judgment; `3.0.0_SA_CVO` grades at L9)

Evidence, with vintage, on each limb the criterion names:

- **The refusal as a person would read it.** No refusal document was produced, so there is nothing to
  read as a person. What CAN be stated with vintage is the shape it would have had: the ladder-skipped
  branch (`render_month_end.py:1148-1180`@`a6e2031ff8`) builds one unresolved row per C/D/UNKNOWN date
  carrying `date`, `class`, `provider` (single-writer via `remediate._provider_for`) and
  `reason: "ladder skipped (--no-ladder)"`. **Its `provider` field is precisely the field that cannot
  be produced on the box today** -- so the operational property R-EG-8 refused to weaken is the same
  property that blocks the run. That is a fact for the CVO, not a verdict from me.
- **Faithful analogue or not.** The driven condition removes a slice the classifier would otherwise see
  and reaches the real classification code path, but it differs from the organic case in two ways the
  artifact itself discloses (`_forcing_record`, `disclosure_version 2`,
  `render_month_end.py:889-954`): `forced: true` with the spec and removed count, and `ladder_ran: false`
  with `rung3_stop_and_ask_reachable: false` and `coverage_egress_ask_possible: false`. Whether
  "ladder skipped" is a difference that MATTERS to what FWD-9 claims is a judgment; I record that the
  divergence is explicit in the record rather than implicit.
- **Is the disclosure enough that a later reader cannot mistake this for organic?** Unexercised on a
  real artifact. The disclosure is `ALWAYS PRESENT` by construction on both branches, and the
  ladder-skipped ask is written to its own key `coverage_egress_ask_ladder_skipped.json` with a
  `written_by` provenance field inside it -- protected twice, by key name and by content. What is NOT
  yet shown by any act is that a reader meeting the served bytes actually reaches the disclosure first.
- **What the terminal send's evidence would prove about DELIVERY vs EMISSION.** Nothing was sent, so
  this is stated as a limit rather than a finding: the deployed handler prints a `MessageId` at its
  correction site (`lambda_function.py:843-845`) and `_send_terminal_unresolved` is the one terminal
  call site; a `MessageId` is an **emission** oracle (SES accepted the message), never a delivery one.
  Per the estate's own record, no Opal sender names an SES configuration set, so no delivery plane
  exists to read, and CloudTrail's SES limb would remain `SES-PLANE-UNREAD`. Any future grade of FWD-10
  should say EMITTED, not DELIVERED.

---

## 5. CONTROLS

- **Mutant / difference control -- FIRED AS EXPECTED.** The `coverage` package is swapped under an
  otherwise identical served renderer: DEPLOYED -> `AttributeError`, REPO -> `REFUSE holes=1`. The
  control is a real one (the "mutant" is the artifact actually serving), and it discriminates in the
  direction that matters -- had it returned REFUSE on both arms, my blocking claim would be false.
- **Negative control on arm (a) -- LIVE.** The scheduled branch returns `aj@opalinvest.com` on both
  instruments, so the test branch's zero is not a dead instrument.
- **Positive control on the absence -- LIVE.** `coverage_verdict.json` HEADs 200 while
  `coverage_unresolved.json` returns 404 from the same call shape, so the 404 is the object's and not
  the call's.
- **Determinism -- STABLE.** Two full battery runs, 54 lines each, **0 differing lines** excluding the
  start timestamp and the per-run presigned-URL-derived line; rc=1 both times.

## 6. DECLARED EXCLUSIONS

- **The driven run itself.** Not fired. Bound 2 permits one and it is unspent; firing it into a path
  that raises before writing a verdict would have consumed it for nothing.
- **The NEVER-2 change-management entry.** Not opened. It names an act's blast radius; there was no act.
- **Any code change, artifact upload or box repair.** Out of `<paths>` and against the NO CODE CHANGE
  bound. The remediation (redeploy `coverage/*.py` AND make the box re-pull) is the issuer's to route.
- **Booting the reporter box to read `/opt/etfs-reports/coverage/` directly.** Not done: it would have
  required stopping an EC2 afterwards (a human-confirmation act), and the subtraction in s.2.3 closes
  the question without it. Stated as a coverage limit, not hidden.
- **The pre-existing pytest red** `test_served_artifact_has_the_shape_the_writer_produces`. Owned by
  `ETFS_GUARDRAIL-W4-S14` / `ETFS_GUARDRAIL-S38`; not touched in either direction, and the fixture was
  not refreshed.
- **Probing `cot-etf-ownership-daily` for 2026-08-14 to confirm `partition/priced`.** Not done: the run
  is blocked regardless, so the check could not change the outcome.

## 7. ROWS FILED

Both appended to
`org/missions/D8/ETFS/ETFS_GUARDRAIL/surprise-channel/investigations/INVESTIGATION_v1.md`.

- **`ETFS_GUARDRAIL-W4-S17`** -- **BLOCKING / ARMED**, `disarm_owner` `2.0.0_SA_COO`,
  `disposition` `UNDER_INVESTIGATION`, `grounding.status` `GROUNDED` (10 evidence items). The stale
  `coverage` package under the current renderer.
- **`ETFS_GUARDRAIL-W4-S18`** -- **OBSERVATION / INERT**, `disposition` `UNDER_INVESTIGATION`. An
  artifact the issuer deleted has reappeared: the prior execution's grounding table records *"2026-08
  has 6 keys, ask deleted by the issuer ... confirmed: 6 keys, `coverage_egress_ask_ladder_skipped.json`
  absent"* at ~16:3xZ, and I read the same prefix at ~18:3xZ with **7 keys**, including
  `platinum/reports/2026-08/coverage_egress_ask_ladder_skipped.json`, 7867 B,
  **LastModified 2026-09-10T17:28:01.000Z**, carrying `generated_at 2026-09-10T17:28:00.106557+00:00`
  and 40 asks across `["49financial","cottonwood"]` -- for a month whose served verdict is
  `PUBLISH holes=0`. Writer unattributed by this seat (S3 alone cannot name it and I did not read
  CloudTrail). It is INERT for this order because no run happened, but it is **material to arm (d)**: the
  arm asks for *"an egress ask RECORDED FOR THE RUN"*, and on this month that key is now PRE-EXISTING, so
  presence alone no longer discriminates. A re-cut should require a before/after on the ask key
  (LastModified moved + the run's own `run_id`), exactly as arm (d) already requires for the publish keys.

## 8. PUSH STATE

**LOCAL.** Committed on `wk-etfs_guardrail-3-21` only. No `git push` was run by this seat.
