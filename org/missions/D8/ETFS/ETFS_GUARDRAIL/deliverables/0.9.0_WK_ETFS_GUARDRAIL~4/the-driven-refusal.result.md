# ETFS_GUARDRAIL.TO-EG-s-21 -- THE DRIVEN REFUSAL: EVERYTHING IS READY AND ONE CLAUSE IS UNREACHABLE IN EVERY MONTH

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` (L7 of `2.0.0_SA_COO`) · **Branch:** `wk-etfs_guardrail-3-21` (LOCAL)
**Worktree:** `C:/tmp/wk-etfs-3-21` · **Base:** `1d62717c65` · **Battery runs:** 16:30:40Z, 16:34:49Z, **16:45:42Z** (3 of 3 identical)
**Outcome:** `S21-AC1` **FAIL** (arm (e) of the battery = arm (d) of the criterion). `<status>` NOT flipped.
**THE SINGLE PERMITTED DRIVEN RUN IS UNSPENT.** No invoke, no send, no S3 write, no S3 delete.
**Rows filed:** `ETFS_GUARDRAIL-W4-S8` (BLOCKING/ARMED), `-W4-S9` (OBSERVATION/ARMED), `-W4-S10` (INERT),
`-W4-S11` (INERT), `-W4-S12` (OBSERVATION/ARMED -- a false-blocking commit gate).

---

## 0. THE CONCLUSION FIRST, BECAUSE IT IS NOT THE ONE THE LAST THREE REFUSALS GAVE

**The two cells cut to unblock this order WORKED. Both are on the served bytes and I measured both
myself.** The forcing now reaches the verdict; the egress ask is now recorded on the ladder-skipped
branch with its provenance and its provider. Five of the battery's six arms HOLD, and the run that
would have been fired is fully specified below down to the byte counts it would write.

**It is blocked by a clause nobody has looked at yet, one grain ABOVE the criterion, in the PRD's own
accept.** `S21-AC1` arm (d) -- and `FWD-9`'s ACCEPT at `ETFS_GUARDRAIL_PRD.md:566-567` (restated at
`:187`) -- require of the driven run's month that **"the publish keys for that month STAY ABSENT (a 404
beside the refused 200)"**. There is no such month, and there cannot be one without an S3 delete, which
this order forbids absolutely:

> a forced class C requires a slice the fixture can **REMOVE** (`_apply_fixture_remove` drops dates from an
> already-loaded series; `classifier.py:191-194 @8471f83a18` needs *no slice* **plus** a probe answering
> partition-present and priced>0) -- so the candidate months are exactly the months in which some partner
> **has** a daily slice. **Measured: 275 slices across 3 partners, months = {2026-05 .. 2026-09}, 0 slices
> outside that range. And 5 of those 5 months already serve `etf_ownership.pdf` AND `.html`. 404-able: 0 of 5.**

That set is written as a **subtraction from a printed denominator**, not as a forward list, precisely
because a forward list is how the last five of these got missed (CLAUDE.md rule 24).

**I did not fire.** Firing would have spent a non-renewable act on a run I had already measured to fail
arm (d) -- which is the waste this face's own `<status>` line names, on different grounds. The remedy is
one ruling, not one round: arm (d)'s `404` names **one world-state** of the property *"this run did not
publish"*, exactly as the pre-`R-EG-8` clause named **one writer** of the egress-ask property. Re-cut to
the property -- *the publish keys are byte-identical across the run (ETag + VersionId + LastModified read
on both sides), or absent* -- and **the run is satisfiable today, on 2026-07, with no code, no deploy and
no data change.** That is `W4-S8`, disarm owner `1.0.0_SA_CTO`.

---

## 1. WHAT I RE-GROUNDED BEFORE ANYTHING ELSE

| premise the face carries | world at 2026-09-10 ~16:3xZ | verdict |
|---|---|---|
| `EG-s-20` terminal | `<status>complete`, drained `5d292ff11f` | HOLDS |
| `EG-s-27` terminal, `--no-ladder` threaded | `<status>complete`; measured in the FORCED command on served bytes | HOLDS |
| `EG-s-29` terminal, rung-3-equivalent ask | `<status>complete`; served renderer sha256 `ba410ee5c9c4263e8fe37ade171aa4d61f834df246d0f57f30299dbba03a031a`, 77,130 B, VersionId `lvBC1IFEk3Fpfry_ysQfCNf5PIA8f00E`, LastModified 2026-09-10T14:09:53Z -- **matches the issuer's own verified read exactly** | HOLDS |
| the face's `<status>` "DO NOT FIRE ... rung 3 never fires" | that reason is **FALSE** at this commit (arm (d) re-cut; the equivalent writes the ask) -- but the *instruction* is still right for a different reason | `W4-S11` |
| `2026-08` has 6 keys, ask deleted by the issuer | confirmed: 6 keys, `coverage_egress_ask_ladder_skipped.json` absent | HOLDS |
| the new cross-fabric gates (`1d62717c65`) | exercised at commit; output read, not exit codes | see s.7 |

**GRAIN NOTE.** The repo's `data/etfs/scripts/presentation/render_month_end.py` at `903c5cba50` is
**byte-identical** to the served artifact (both 77,130 B / `ba410ee5...`), so a `file:line` citation into
the repo file resolves to the bytes the box actually pulls. That is a content resolution, not a
`merge-base` claim (rule 22a).

---

## 2. THE MECHANISM I CHOSE, AND WHAT I REJECTED

**CHOSEN: `--fixture-remove cottonwood:2026-07-15` + `--no-ladder`, on month `2026-07`, via a
`test_run` invocation of `etfs-reports-orchestrator`.** Nothing on S3 is touched to create the
condition -- the fixture drops one date from the series **in memory** -- so the cell's bound
(*no served artifact of a real month is altered to create the condition*) is satisfied structurally
rather than by care.

**WHY `2026-07` AND NOT `2026-08`.** This is the choice the issuer's seating message assumed the other
way, so it is stated with its evidence:

| | 2026-07 | 2026-08 |
|---|---|---|
| unforced verdict (needed for the undo arm) | PUBLISH, 0 gaps, 22 of 22 trading days x 3 partners | PUBLISH, 0 gaps, 21 of 21 x 3 |
| `coverage_verdict.json` served today | **ABSENT** -- the run creates it | **PRESENT, 1,225 B, 2026-09-10T00:24:44Z -- the run OVERWRITES the record of August's real publish** |
| keys the refusal run would alter | **0** (all 7 writes are new keys) | 1 (the verdict of a real published month) |
| publish keys 404-able | no | no |

August is strictly worse on the only axis where they differ, and identical on the blocking one. On
2026-07 **the run alters nothing at all**; it only adds.

**REJECTED, with reasons:**

- **A month with no served publish keys** (the cell's own preference). *Does not exist* -- s.0. The three
  months without cottonwood coverage (2026-05, -06) also have no provable PUBLISH baseline, so the undo
  arm could not discriminate there even if the 404 were free.
- **A future/empty month (2026-10+, 2026-04).** `classifier._month_dates` returns `[]` for a wholly
  future month, and a month with no slice cannot carry a *forced* class C at all -- the fixture would
  remove nothing (`removed_slice_count: 0`) and any REFUSE would be organic, which destroys the undo arm.
- **Editing a real month's daily slices to create the hole.** Never considered seriously: it alters served
  data and the fixture already reaches the same code path without touching S3.
- **Re-pointing `REPORTS_PREFIX`/`--s3-out` at a scratch prefix.** `_render_command` builds `--s3-out`
  from the function's own environment; changing it is a configuration change on a Terraform-managed
  deployed producer, outside this order's `<paths>` and outside its NO-CODE-CHANGE bound, and it would
  leave a new reachable state on the scheduled path.
- **Deleting or moving 2026-07's publish keys to manufacture the 404.** Forbidden absolutely
  (NEVER-AUTO-DELETE; *no S3 delete under this order at all*), and it would destroy a served report.

---

## 3. WHAT THE RUN WOULD HAVE DONE -- MEASURED, NOT PREDICTED

The battery loads the **served** renderer in-process with `s3` replaced by a facade that reads through and
**captures** `put_object` instead of sending it, and drives `coverage_gate` twice with the real S3 series.

```
REAL PROBE (read-only) cot-etf-ownership-daily <- {"date": '2026-07-15', "probe": true}:
  {"status": "probe", "date": "2026-07-15", "partition": true, "priced": 10791, "output_exists": true}
  write-free control on daily/cottonwood/2026-07-15.json:
  ETag "46a75c130740bc32e39cc6877eed4827" -> "46a75c130740bc32e39cc6877eed4827"  UNCHANGED=True

  forcing DISENGAGED ladder=False -> VERDICT=PUBLISH  holes=0 C per partner={'cottonwood': 0, ...}
  forcing ENGAGED    ladder=False -> VERDICT=REFUSE   holes=1 C per partner={'cottonwood': 1, ...}
```

`10791` priced rows and `partition: true` are what make the removed date **class C** and not class D --
read against the classifier's own boundary, quoted at `file:line` so the class is graded by the rule:

```
classifier.py:177-179  @8471f83a18   {"class": "D", "reason": "upstream partition missing (genuinely absent)"}
classifier.py:191-194  @8471f83a18   {"class": "C", "reason": "upstream present and priced > 0, no slice --
                                      producer never fired for this date"}
```

The forced per-partner class table the run would write:

```
cottonwood   {"A":9,"COVERED":21,"B":0,"C":1,"D":0,"UNKNOWN":0,"trading_days":22,"covered":21,"holes":1}  holes=['2026-07-15']
49financial  {"A":9,"COVERED":22,"B":0,"C":0,"D":0,"UNKNOWN":0,"trading_days":22,"covered":22,"holes":0}
inflection   {"A":9,"COVERED":22,"B":0,"C":0,"D":0,"UNKNOWN":0,"trading_days":22,"covered":22,"holes":0}
```

The disclosure that would ride on `coverage_verdict.json` (`EG-s-25` + `EG-s-26`, `disclosure_version 2`):

```json
{"forced": true, "mechanism": "--fixture-remove", "fixture_remove_spec": "cottonwood:2026-07-15",
 "removed_slice_count": 1, "ladder_ran": false, "ladder_skip_mechanism": "--no-ladder",
 "rung3_stop_and_ask_reachable": false, "coverage_egress_ask_possible": false,
 "run_shape": "FORCED (--fixture-remove, 1 slice(s) removed) and LADDER SKIPPED (...)",
 "run_id": "<minted by the run>", "run_id_source": "..."}
```

`EG-s-29`'s ask, captured verbatim from the bytes the run would put (1,182 B):

```
platinum/reports/2026-07/coverage_egress_ask_ladder_skipped.json
  written_by  : render_month_end.coverage_gate on the --no-ladder branch (...TO-EG-s-29) -- a
                RUNG-3-EQUIVALENT. RUNG 3 DID NOT RUN and did not write this.
  rung3_ran   : False
  asks        : [{"date": "2026-07-15", "partner": "cottonwood", "provider": "Black Diamond",
                  "class": "C", "reason": "ladder skipped (--no-ladder)"}]
```

**The full write set, enumerated (7 keys, all NEW, none overwritten, none deleted):**

```
NEW  platinum/reports/2026-07/coverage_egress_ask_ladder_skipped.json   1182 B  (coverage_gate, no-ladder branch)
NEW  platinum/reports/2026-07/coverage_verdict.json                             (main, always written)
NEW  platinum/reports/2026-07/coverage_unresolved.json                          (main, unresolved non-empty)
NEW  platinum/reports/2026-07/refused/etf_ownership.html                        (main, REFUSE branch)
NEW  platinum/reports/2026-07/refused/opaletfs_49financial_202607.csv           (main, REFUSE branch)
NEW  platinum/reports/2026-07/refused/opaletfs_cottonwood_202607.csv            (main, REFUSE branch)
NEW  platinum/reports/2026-07/refused/opaletfs_inflection_202607.csv            (main, REFUSE branch)
```

and the terminal envelope it would resolve, on the bytes deployed at 2026-09-10T12:16:53Z:
`['andrew@opalinvest.com']` -- with `aj@opalinvest.com` in **0 of 18** resolved test-invocation lists and
the scheduled path still `['aj@opalinvest.com','andrew@opalinvest.com']`.

**That is the entire act, priced. It is ready. One clause of one arm is what it cannot satisfy.**

---

## 4. THE BLOCKER, WITH ITS DENOMINATOR

```
  daily slices scanned: 275 across 3 partners -> months carrying a slice:
      ['2026-05','2026-06','2026-07','2026-08','2026-09']
  slices OUTSIDE that month range: 0
  served keys under s3://opal-data-etfs/platinum/reports/ : 36 (denominator)

  month   | pdf 200 | html 200 | 404-able | slice to force | unforced verdict
  --------+---------+----------+----------+----------------+-----------------
  2026-05 | True    | True     | False    | 49financial,in | NOT PROVEN (gaps {'cottonwood': 20, ...})
  2026-06 | True    | True     | False    | cottonwood,49f | NOT PROVEN (gaps {'cottonwood': 7, ...})
  2026-07 | True    | True     | False    | cottonwood,49f | PUBLISH (0 gaps)
  2026-08 | True    | True     | False    | cottonwood,49f | PUBLISH (0 gaps)
  2026-09 | True    | True     | False    | cottonwood,49f | NOT PROVEN (gaps {'cottonwood': 1, ...})
```

**0 of 5.** The intersection of *{months that can carry a forced class C}* and *{months serving no publish
key}* is EMPTY, and the two sets are disjoint by construction rather than by accident: a month has slices
because a report was produced for it, and a report produced for it is exactly what put the publish keys
there.

**WHAT IS NOT CLAIMED.** I am not claiming the property arm (d) reaches for is unprovable. It is provable
today, and stronger than a 404: read `etf_ownership.{pdf,html}` and the three CSVs with `s3api
head-object` **before and after** the run and show ETag + VersionId + LastModified identical, beside the
refusal artifacts' fresh 200s. That is a difference control on the actual claim (*this run did not
publish*), where a 404 on a never-published month is only an absence. **But substituting it is a re-cut of
a criterion, and a re-cut is not mine to make** -- especially not this one, whose whole history is a
sequence of seats discovering that a criterion named one instance of a property instead of the property.

---

## 5. THE CRITERIA

### `S21-AC1` -- **FAIL**

**Invocation (the face's, verbatim):**
`timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs21_driven_refusal.py`
**Expected:** `EGS21-REFUSAL-DRIVEN-AND-SENT` · **Got:** `EGS21-BLOCKED-NO-MONTH-CAN-SATISFY-FWD9-404`, **rc=2**.
**Denominator: 5 of 6 arms HOLD.** Full transcript: `EG-s-21_S21-AC1_battery_output.txt` (126 lines).

```
arms: 5 of 6 HOLD
  (a) PRECONDITION                       HOLD   aj@ in 0 of 18 resolved lists, bytes of 2026-09-10T12:16:53Z
  (b) DEPENDENCIES SERVED                HOLD   --no-ladder in the FORCED command, absent from the marker-free one;
                                                _skipped_branch_egress_ask at [1066, 1176]
  (c) FORCING REACHES THE VERDICT        HOLD   ENGAGED REFUSE (C on cottonwood) vs DISENGAGED PUBLISH, same bytes
  (d) ASK LIMB                           HOLD   ask recorded at the ladder-skipped key, rung3_ran=false, provider 1 of 1
  (e) A MONTH EXISTS THAT CAN SATISFY THE ACCEPT   BLOCKED   0 of 5
  (f) NO SIDE EFFECT                     HOLD   the one probe invoke ETag-controlled UNCHANGED=True
```

The battery has **no branch that can print the success token**: the success token requires arm (e), and
arm (e) is a census of the world, not of my code.

Mapping to the criterion's own arms, so the CVO does not have to derive it:
`(a)` -> battery (a), **HOLDS**. `(b)` forcing declared+disclosed -> the disclosure half is measured
(s.3); the **declaration** half (the entry's opened-at preceding the invoke) is **NOT DONE and
deliberately so** -- see s.6. `(c)` -> battery (c), the REFUSE and the class table are measured on served
bytes but read from a captured verdict rather than from a served `coverage_verdict.json`, because no run
was fired. `(d)` -> the ask limb HOLDS; the **404 limb is the blocker**. `(e)` terminal send, `(f)` undo
on served artifacts, `(g)` key enumeration -> **NOT REACHED**; `(f)`'s discriminating pair is nevertheless
measured hermetically (PUBLISH <-> REFUSE on the identical inputs) and `(g)`'s key list is enumerated in
advance in s.3.

### `S21-AC2` -- **RECORDED for `3.0.0_SA_CVO` at L9. NO VERDICT.**

Evidence, with vintage (all at 2026-09-10 ~16:3xZ unless stated):

- **The refusal as a person would read it.** Three surfaces, and they do not agree. (1) `coverage_verdict.json`
  -- complete and self-disclosing: month, per-partner class table, the forced hole's date, and the whole
  `forcing` record with `forced: true`, `ladder_ran: false` and the run id. (2) `coverage_egress_ask_ladder_skipped.json`
  -- names the date, partner, provider (`Black Diamond`), class and rung-3's own per-use authorization
  string, with provenance FIRST. (3) **the terminal EMAIL, which is the surface `FWD-10` actually names,
  and it is the weakest**: its header asserts *"could not resolve 1 date(s) after every rung ran (probe,
  re-run the producer, re-check)"* on a run where **zero rungs ran**, it carries **no forcing field at
  all**, and the only contradiction of its own header is the per-row `reason: ladder skipped (--no-ladder)`.
  Rows `W4-S9` and `W4-S10`. A reader of the artifact cannot mistake this run for organic; **a reader of
  the email cannot tell.**
- **Is the driven condition a faithful analogue?** On the axis `FWD-9` grades -- *the gate refuses over a
  class-C hole* -- **yes, and identically**: the gate's decision is `any_c` over the classification, and
  the forced hole classifies through `classifier.classify_month`'s ordinary path with a **real, measured**
  probe answer (`partition: true, priced: 10791`), not a stub. `R-EG-6` (iii) already fixed the boundary:
  the ladder's ORCHESTRATION is not covered. It differs on one axis a grader should see anyway: an organic
  class C would have survived rungs 1-2, and this one was never offered to them, so the artifact's
  `rungs: {probe: 0, rerun: 0, recheck: 0}` is a *skip*, not a *failure to repair* -- and the artifact says
  exactly that in four fields.
- **Is the disclosure enough?** On the artifact, yes, and it is now double-keyed: `forced: true` and
  `ladder_ran: false` in one object, plus the equivalent ask at a **different key** whose name and whose
  `written_by` both say it is not rung 3's. On the email, no -- see above.
- **What would the send's evidence actually prove?** `EG-s-20` made `_send_terminal_unresolved` print
  `MessageId=...` (`lambda_function.py:407-410` on the deployed bytes), so the strongest available oracle
  would be an **application log line naming the SES MessageId and the resolved destinations**. That is an
  **EMISSION** oracle: it proves SES accepted the message and assigned it an id. It is not delivery.
  Nothing on this account can prove delivery: per-recipient SES events need a configuration set, this
  account has one (bounce+complaint) and **no first-party sender names it**, so no delivery plane exists to
  read -- the CloudTrail limb stays `SES-PLANE-UNREAD` against its 2-trail denominator. `FWD-10`'s DONE
  WHEN (*"READ at Andrew's own inbox"*) is therefore only closable by a **gateway/inbox read by Andrew**,
  which no seat can take on demand and which no instrument in this estate substitutes for.
- **What the un-fired state costs and does not cost.** `FWD-9` and `FWD-10` remain NOT-EVALUATED. Nothing
  regressed; the mechanism is measured working end-to-end short of the invoke.

---

## 6. WHAT I DID NOT DO, AND WHY EACH ONE IS DELIBERATE

- **No orchestrator invoke, no SES send, no SSM command, no EC2 start/stop, no S3 write, no S3 delete.**
  The battery's stubs RAISE on every non-read call; the renderer's `put_object` is captured, never sent.
- **No NEVER-2 entry opened or closed.** The face requires it opened **before the act**, and there was no
  act. An entry for a run that never happened puts a false event in the change-management record --
  the same call my predecessor on this slot made, and it is still right. `org/critical_paths/` is untouched
  by this commit. The entry's *content* is nevertheless pre-written in s.3 (write set, both branches,
  rollback per key) so the next seating opens it in one act.
- **No code change**, no override of any gate, no widening of the order, and no `git push`.
- **One mutating capability was exercised and it is disclosed:** a single read-only `probe` invoke of
  `cot-etf-ownership-daily` per battery run (2 runs, 2 probes). `_probe` is documented write-free at
  `infra/aws/lambda/cot-pipeline/cot-etf-ownership-daily/lambda_function.py:285-294` (*"Never reaches
  put_object"*) and I did not take that on the docstring: the slice's ETag is read **before and after**
  each probe and is unchanged. I used it rather than assuming, because the whole point of the pre-flight
  was to know the forced date's class **before** spending a non-renewable act on it.

## 7. THE GATES, INCLUDING ONE THAT REFUSED CORRECT CODE

`1d62717c65` modified twelve `.tools/` files including `safe-commit.sh`, `to-pipeline-gate.py`,
`surprise-row-gate.py` and `proof-of-spec-check.py`, and added `prd-manifest-gate.py`, none of which had
run on this fabric. I read their **output**, not their exit codes. Nothing was overridden and no gate was
bypassed.

- `.tools/proof-of-spec-check.py` refused this instance twice on its own terms and was right both times
  (`controls` requires a `determinism` block and a `mutant.status`, and admits no sibling keys;
  `kind: "evidence"` is not in its enum). Fixed by writing what it asked for, not by trimming the record:
  the two extra controls I had written are folded into `mutant.description` with their own EXPECTED and
  OBSERVED, because a control moved out of the record to fit a shape is a control nobody reads.
- `.tools/surprise-row-gate.py` invoked bare on this worktree printed
  `OK: no surprise-channel rows in this commit (denominator: 0 dispatched path(s))` -- a **vacuous pass on
  an empty input set**, which is why the rows are graded at the commit and not by that read.
- **`.tools/ds-precommit-check.py` BLOCKED this cell's own battery on four FALSE findings, and that is row
  `W4-S12`.** It reported `undefined name 'kw'` / `'r'` against a textbook hand-rolled S3 continuation
  loop whose names are bound two lines above every use, in a script that had already run to completion
  twice. **Reproduced minimally in 12 lines with no imports: ds-precommit gives 4 findings and rc=1; ruff
  `--target-version py39` on the identical bytes gives `All checks passed!` and rc=0.** Two instruments,
  same bytes, opposite verdicts -- and the fail-closed one is the wrong one. Rule 14's gate is universal
  and `--force` does not bypass it, so the code was uncommittable in that shape. **It is NOT the merge's
  doing:** `ds-precommit-check.py` is not among the twelve `.tools/` files `1d62717c65` changed, so this
  is estate-wide and pre-existing. I complied rather than fought it **only because the replacement is
  independently better** -- `get_paginator(...).paginate(...)` auto-paginates, and a single
  `list_objects_v2` returns a PAGE whose length is not a denominator -- and I left the reason in a comment
  at the call site so the next reader does not mistake the shape for a preference. The 36-key denominator
  is identical before and after the rewrite.

## 8. FOR WHOEVER SEATS THIS NEXT

Everything except the ruling is done. When `W4-S8` is dispositioned, the next seating is: open the NEVER-2
entry with the s.3 write set; invoke
`etfs-reports-orchestrator` with `{"mode":"run","month":"2026-07","test_run":true,"force_fixture_remove":"cottonwood:2026-07-15"}`
(`--cli-read-timeout 0 --cli-connect-timeout 60`, synchronous, ~12-15 min, NOT-RETURNED at 15); read the
five publish keys' ETag/VersionId/LastModified **before and after**; close and commit the entry; then
grade. No code, no deploy, no data change is needed between here and there.
