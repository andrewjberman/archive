# ETFS_GUARDRAIL.TO-EG-s-31 -- RESULT

**Assignee:** `0.9.0_WK_ETFS_GUARDRAIL~4` | **Branch:** `wk-etfs_guardrail-3-31` | **Base:** CLOUD @ `1daa6d597a`
**Outcome:** `S31-AC1` **PASSES BY OUTPUT**, 5 of 5 arms. `S31-AC2` **RECORDED**, not self-graded (s.6).
**Instance:** `i-070477bf35fc54409`, state **running**, measured. **LEFT RUNNING DELIBERATELY** (s.5).

---

## 0. RE-GROUNDING THE ORDER'S PREMISES BEFORE ACTING

Every premise the face asserted was re-measured at HEAD before anything was done. All held,
and one of them was wrong in a direction the face did not anticipate (row `W4-S22`).

| the face asserts | measured, and how | verdict |
|---|---|---|
| the served renderer calls `remediate._provider_for(p)` at `render_month_end.py:1162`, `--no-ladder` branch | `sed -n '1150,1180p' data/etfs/scripts/presentation/render_month_end.py` -- the call is at :1162, inside `coverage_gate`'s `else:` (ladder-skipped) branch | HOLDS |
| the self-heal at `:118-129` keys on `ImportError` | read at source: `try: from coverage import classifier, remediate / except ImportError:` then `aws s3 cp --recursive` | HOLDS |
| the deployed `coverage/remediate.py` is 11011 B @ 2026-09-05T06:53:44Z, repo 16550 B | `s3api list-object-versions`: 11011 B, `2026-09-05T06:53:44.000Z`, VersionId `2FPYNO73yMham_.9X2uhmOe6UQ8pey8j`; repo `stat -c %s` = 16550 | HOLDS |
| the deployed package raises `AttributeError`, the repo package returns `VERDICT: REFUSE holes=1` | exercised both, s.2 arm (a) | HOLDS |
| "three cells verified three files that were each current" -- ONE stale symbol | **PARTLY WRONG.** The by-content census found **2 of 5** members stale, not 1: `classifier.py` carries EG-s-22's undeployed work as well. Row `ETFS_GUARDRAIL-W4-S22` | **MOVED** |
| the box will run the served renderer | **NEEDED A THIRD MEASUREMENT.** The box's baked renderer was 62880 B / `55701125...`, NOT the served 77130 B / `ba410ee5...`. It is nonetheless true, because `lambda_function.py:652` re-pulls it unconditionally every run. Row `ETFS_GUARDRAIL-W4-S21` | HOLDS, for a reason the face did not state |

**NEVER-2 SUPERSEDE CHECK, RUN BEFORE THE ACT AND NOT AFTER.** The bytes were **not** already
served: the prefix carried the 2026-09-05 objects and the box imported them cleanly. The defect
reproduced on the box at 19:41:19Z. So the act was live, not superseded, and arm (a)'s stop
condition did not fire.

---

## 1. THE SHAPE TAKEN, AND WHY

**Shape (i), the issuer's stated preference: upload, then force the re-pull by removing the
box-side copy.** Taken in a NARROWED form, and the narrowing is the whole of row `W4-S19`:

> The face says "REMOVING THE BOX-SIDE DIRECTORY". **A directory removal is a recursive
> deletion, and CLAUDE.md's Agent Autonomy section reserves recursive deletion to human
> confirmation.** A task order does not lift a CLAUDE.md hard stop. So the act was
> `rm -f` on **exactly two named files** -- `/opt/etfs-reports/coverage/classifier.py` and
> `remediate.py` -- each printed with its sha256 and byte count immediately before removal,
> plus their two matching `.pyc` files so `__pycache__` could not mask the removal.
> `from coverage import classifier, remediate` then raises `ImportError` exactly as a missing
> directory would. **The mechanism the shape wanted was obtained without the act it named.**

**PROOF THAT WHAT WAS REMOVED WAS THE VENDORED COPY AND NOT SOMETHING ELSE** (the face asks for
this by name): both printed hashes -- `23c30889...` and `3c3ce6c5...` -- are byte-equal to the
pre-act objects at `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/`,
recorded with their VersionIds in `egs31_pre_act_manifest.json`. A file that hashes to the
artifact it was pulled from is that pull's output.

**WHAT WAS REJECTED.**

- **Shape (ii), the currency-aware self-heal.** Rejected **only** because the face forbids it
  without the issuer's written word -- it edits `render_month_end.py`, `EG-s-29`'s terminal
  surface -- and that word was not available to this worker. **It is the better fix and s.6
  says so with a costing.** Filed as row `W4-S20` with the change named. A row and a stop, not
  an edit: `render_month_end.py` is **untouched** by this order.
- **Shape (iii), upload only.** The issuer's read was that it cannot work, and **this order
  measured that read to be correct rather than assuming it.** At 19:41:53Z the prefix was
  fully current while the box still held the 2026-09-05 modules; the box only changed when the
  `ImportError` was forced. The upload alone moved nothing the renderer imports. See s.2 arm (c).
- **A fourth shape, considered and rejected: a direct box-side `aws s3 cp --recursive`
  overwrite, no removal at all.** It is safer (it cannot leave the box with no package) and it
  would have satisfied the property. Rejected because it proves less: it would leave the box in
  a state set by an out-of-band manual act, whereas forcing the designed `ImportError` path
  leaves the box in a state set by **the renderer's own mechanism**, and demonstrates that the
  mechanism works. The safety gap was closed instead by doing the removal and the re-pull inside
  **one** SSM command, so the window in which the box held no package was the duration of one
  `aws s3 cp`, under a `su - ec2-user` shell whose failure would have been visible in the same
  output.

**ALL BOX-SIDE COMMANDS RAN AS `ec2-user` VIA `su - ec2-user -c`, NEVER AS ROOT.** SSM runs as
root by default; a root-created `coverage/*.py` would have left the directory owned by a user
the real run is not, converting this repair into a permissions failure on the next scheduled
fire. The post-act listing shows all five members `ec2-user ec2-user`.

---

## 2. `S31-AC1` -- FIVE ARMS, EVERY NUMBER BESIDE ITS DENOMINATOR

**Invocation:** `timeout 900 python org/missions/D8/ETFS/ETFS_GUARDRAIL/deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs31_box_package_matches_renderer.py`
**Result:** rc=0, final line `EGS31-THE-BOX-RUNS-THE-PACKAGE-THE-RENDERER-EXPECTS`, `ARMS HOLDING: 5 of 5`.

### (a) THE DEFECT REPRODUCES FIRST, ON THE DEPLOYED ARTIFACT, BEFORE ANY ACT -- HOLDS

Run twice, in two places, both before the act.

**On the box** (SSM `7c298036-a828-48d5-b3be-05f486fe3867`, 2026-09-10T19:41:19Z), after
performing the same unconditional renderer pull a run performs:

```
EGS31-RENDERER-FILE /opt/etfs-reports/render_month_end.py sha256=ba410ee5c9c4263e8fe37ade171aa4d61f834df246d0f57f30299dbba03a031a
EGS31-MODULE remediate file=/opt/etfs-reports/coverage/remediate.py sha256=3c3ce6c5cfcce654ad3d5794962b6c24bfbee629db49a8f289b00f3979e876d5
EGS31-SYMBOL remediate._provider_for present=False
EGS31-RESULT RAISED AttributeError: module 'coverage.remediate' has no attribute '_provider_for'
Traceback (most recent call last):
  File "/tmp/egs31_exercise.py", line 185, in main
    result = mod.coverage_gate(
  File "/opt/etfs-reports/render_month_end.py", line 1162, in coverage_gate
    provider_for_partner = remediate._provider_for(p)
AttributeError: module 'coverage.remediate' has no attribute '_provider_for'
```

**THE SELF-HEAL PROVABLY DID NOT FIRE ON THAT RUN**, which is the direct measurement of the
mechanism the face describes: that command printed the coverage directory's listing and sha256
set immediately before and immediately after the exercise, and the two are byte-identical.
A stale-but-importable package imported cleanly, the bootstrap never ran, and the failure
surfaced as an `AttributeError` deep in the call path.

**In the battery, re-runnably** (the deployed bytes are committed as `.pyfixture` files whose
sha256 the battery checks against the recorded pre-act S3 objects, `5 of 5` -- because the act
destroys the evidence for its own "before" side):

```
FIXTURE-INTEGRITY 5 of 5 fixtures equal the pre-act deployed objects
EGS31-ARM-A before=RAISED-AttributeError:True after=VERDICT:-REFUSE-holes=1:True  -> HOLDS
```

Paired side, printed beside it, same renderer sha256 `ba410ee5...`, package the only variable:
`VERDICT: REFUSE holes=1 C=1` and `EGS31-UNRESOLVED date=2026-08-14 class=C provider=Black Diamond`.

### (b) THE ARTIFACT PREFIX CARRIES THE CURRENT PACKAGE -- HOLDS

Compared BY CONTENT (sha256 of the re-downloaded object), never by filename or ETag.

| member | pre-act | post-act | LastModified (UTC) | vs repo counterpart |
|---|---|---|---|---|
| `__init__.py` | 89 B | 89 B | 2026-09-05T06:53:37Z | MATCH `data/etfs/scripts/coverage/__init__.py` |
| `_orion_vendor_asof.py` | 6979 B | 6979 B | 2026-09-05T06:55:02Z | MATCH `data/inf/scripts/silver/_orion_vendor_asof.py` |
| `classifier.py` | 10157 B | **12226 B** | **2026-09-10T19:41:50Z** | MATCH `data/etfs/scripts/coverage/classifier.py` |
| `remediate.py` | 11011 B | **16550 B** | **2026-09-10T19:41:53Z** | MATCH `data/etfs/scripts/coverage/remediate.py` |
| `trading_calendar.py` | 6979 B | 6979 B | 2026-09-05T06:54:58Z | MATCH `lib/trading_calendar.py` |

**DENOMINATOR AND MOVEMENT: the package has 5 files and 2 were moved.** The numbers differ and
the reason is measured: the other 3 already equalled their repo counterparts by sha256 before
the act, so re-putting them would have been a no-op write on a served prefix, which NEVER-2's
supersede limb forbids.

**TWO OF THE FIVE ARE VENDORED FROM OUTSIDE `data/etfs/scripts/coverage/`** and are compared
against their true sources (`render_month_end.py:60-64`, `classifier.py:49-56`), not against
that directory -- a census scoped to the package directory would have scored them as orphans.

**THE METHOD CARRIES ITS OWN POSITIVE CONTROL.** Three of the five returned MATCH in the same
sweep, so the two MISMATCHes were not an artefact of hashing; and `tr -dc '\r' | wc -c` returned
CR=0 on every repo counterpart, ruling out the autocrlf worktree-hash trap that would have made
all five mismatch.

**The other half of the agreement, censused too:** served `render_month_end.py` 77130 B sha256
`ba410ee5c9c4263e8fe37ade171aa4d61f834df246d0f57f30299dbba03a031a` == the repo file, byte for
byte. `EG-s-29`'s finding confirmed by content rather than by size.

### (c) THE BOX IMPORTS THE NEW SYMBOL -- HOLDS, AND IT IS AN EXERCISE, NOT A RECEIPT

SSM `13a9c6d0-ed00-4d66-8d26-0d5ad16601d7`, 2026-09-10T19:49:39Z, `Success rc=0`, run as
`ec2-user` in `/opt/etfs-reports`, entering through the renderer's own import:

```
EGS31-RENDERER-FILE /opt/etfs-reports/render_month_end.py sha256=ba410ee5c9c4263e8fe37ade171aa4d61f834df246d0f57f30299dbba03a031a
EGS31-MODULE classifier file=/opt/etfs-reports/coverage/classifier.py sha256=b2ab67fd35362249ae072803b2a6107af1daac483a985d276005ec7cf9736cc2
EGS31-MODULE remediate file=/opt/etfs-reports/coverage/remediate.py sha256=401bed2ace84d1566e004ef9cf1b2eec941c4859eee6b05f6110c61b90d8d05f
EGS31-SYMBOL remediate._provider_for present=True
```

**NO UPLOAD RECEIPT, ETag OR LISTING WAS ACCEPTED FOR THIS ARM.** The value printed is the
result of `hasattr` on the module object that `from coverage import ... remediate` actually
bound, inside a process whose renderer is the served artifact.

**AND THE SELF-HEAL IS WHAT PUT THE FILES THERE.** SSM
`ad1788a9-316f-4334-864b-a2aac0936865` shows the two named removals, then five
`download: s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/... to coverage/...`
lines emitted from inside the exercise -- the `except ImportError` branch firing as designed.
**This is also the measurement that refutes shape (iii):** between 19:41:53Z (prefix current)
and 19:42:42Z (removal), the prefix was fully current and the box still held the 2026-09-05
modules. Upload alone moved nothing.

### (d) THE CALL PATH RETURNS A VERDICT INSTEAD OF RAISING -- HOLDS. The difference control.

Same code, same spec, before and after, both printed:

| | BEFORE (SSM `7c298036`, 19:41:19Z) | AFTER (SSM `13a9c6d0`, 19:49:39Z) |
|---|---|---|
| renderer sha256 | `ba410ee5...` | `ba410ee5...` (identical) |
| spec | `cottonwood:2026-08-14`, `ladder=False` | identical |
| `remediate` sha256 | `3c3ce6c5...` | `401bed2a...` |
| result | `AttributeError: module 'coverage.remediate' has no attribute '_provider_for'` | `VERDICT: REFUSE holes=1 C=1` |
| unresolved record | none -- raised before one existed | `date=2026-08-14 class=C provider=Black Diamond` |

The `provider=Black Diamond` line is `EG-s-28`'s fix arriving at the box for the first time.

### (e) NOTHING ELSE MOVED; THE POWER STATE IS MEASURED -- HOLDS

**EVERY KEY WRITTEN BY THIS ORDER (denominator 2):**

```
s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/classifier.py  12226 bytes  2026-09-10T19:41:50Z  VersionId 8KrBLcoEDt29_38qpW0rGddvlDH6Koq1
s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/remediate.py   16550 bytes  2026-09-10T19:41:53Z  VersionId a1zbF15HScZqfZyFcxo7xzwOq3nN4f0D
```

- **S3 DELETES: 0.** `DeleteMarkers` under the prefix = 0. No S3 delete was issued under this
  order at all. **The box-side `rm -f` of two named files is a LOCAL FILESYSTEM removal on an
  EC2 instance, not an S3 delete and not a recursive deletion** -- stated explicitly here and in
  the NEVER-2 entry rather than left implicit, as the spawn required. The 7 retained object
  versions under the prefix include both pre-act versions, so the rollback is real rather than
  asserted.
- **SES SENDS: 0.** No SES client is constructed in the battery or the exercise.
  `aj@opalinvest.com` is a recipient of nothing.
- **ORCHESTRATOR / LAMBDA INVOKES: 0.** Every exercise ran `ladder=False` with a stub probe, so
  `remediate.remediate_month` and `_make_invoke` were never reached.
  **`EG-s-21`'s single permitted DRIVEN RUN REMAINS UNSPENT.**
- **THE ONE PUT THE CALL PATH ATTEMPTS, VERIFIED NOT TO HAVE LANDED.** The `--no-ladder` branch
  really does `put_object` the rung-3-equivalent ask, so the renderer module's `s3` client was
  replaced with a recording stub before every call. **The renderer prints
  `OK: s3://...` for that key regardless, because the print sits beside the `put_object` rather
  than after a read -- so the print line is NOT the discriminator.** The object's own state is:
  `s3://opal-data-etfs/platinum/reports/2026-08/coverage_egress_ask_ladder_skipped.json`,
  7867 B @ 2026-09-10T17:28:01Z **before and after, UNCHANGED**, against an intercepted body of
  1182 B. That pair is the evidence.
- **POWER STATE:** `i-070477bf35fc54409`, **`running`**, read from `ec2:DescribeInstances`.
  Pre-act state was `stopped`; this order started it at 19:33:22Z. See s.5.

---

## 3. THE NEVER-2 ENTRY

`org/critical_paths/change_management/20260910T1933Z_egs31-box-coverage-package-currency_deploy_completion.md`
-- OPENED 19:33:06Z **before the act**, naming the blast radius on **both** branches, and CLOSED
with all 3 legs proven; sentinel removed from `.open_deploys/`.

**The entry counts the writers of the named property before it names an outcome, N=2 printed:**
(W1) the artifact prefix, (W2) the box-side vendored copy. Moving W1 alone does not move the
property -- which is exactly what the 19:41:53Z-to-19:42:42Z window then measured.

**BLAST-RADIUS AMENDMENT 1 was filed at 19:42Z, BEFORE the act it covers**, when the pre-act
census found a third writer (the box's baked renderer) that the original entry did not name. It
adds the unconditional renderer pull to the radius, justifies it (arm (c) requires the entry
point a run uses, and the box's baked copy is an object no run ever executes), states its
rollback, and fixes the `su - ec2-user` ownership requirement. Leg kind `ec2-baked-asset` was
chosen deliberately: its own contract in `.tools/deploy_ledger.py` says *"S3 ETag is NOT valid
proof -- the S3 copy can be current while the baked copy is stale"*, which is this cell's lesson
already encoded in the ledger tool.

---

## 4. SURPRISE ROWS FILED (4)

All in `org/missions/D8/ETFS/ETFS_GUARDRAIL/surprise-channel/investigations/INVESTIGATION_v1.md`.
Ids minted from a read of the channel at this worktree's own HEAD; highest prior `W4` row was `S18`.

| id | class / hazard | one line |
|---|---|---|
| `ETFS_GUARDRAIL-W4-S19` | OBSERVATION / INERT | Shape (i) taken literally is a recursive deletion, which CLAUDE.md reserves to human confirmation; narrowed to two named files, same mechanism, measured. |
| `ETFS_GUARDRAIL-W4-S20` | OBSERVATION / **ARMED**, disarm `2.0.0_SA_COO` | A **second** presence-keyed self-heal at `render_month_end.py:83-92` for `_orion_vendor_asof.py`, same class defect, currently latent because that module happens to be current. |
| `ETFS_GUARDRAIL-W4-S21` | OBSERVATION / INERT | The box's baked renderer was also stale (62880 B vs 77130 B) and it is NOT a defect -- `lambda_function.py:652` re-pulls it unconditionally; knowing which is which required reading the orchestrator. |
| `ETFS_GUARDRAIL-W4-S22` | OBSERVATION / **ARMED**, disarm `2.0.0_SA_COO` | **2 of 5** members were stale, not 1: `classifier.py` carried `EG-s-22`'s undeployed work. The deploy step for `data/etfs/scripts/coverage/` is owned by no cell. |

---

## 5. THE BOX IS RUNNING, AND THAT IS DELIBERATE

**`i-070477bf35fc54409` is `running` and this order did not stop it.**

It was `stopped` at 19:33:06Z. This order started it at 19:33:22Z, which is an ordinary act.
**Stopping an EC2 is a human-confirmation act under CLAUDE.md and is Andrew's to take, not this
worker's.** A running box here is not a defect, not an oversight, and not something for a later
reader to tidy away on this worker's behalf. It is stated loudly in the battery's arm (e) output,
in the NEVER-2 entry, and here.

---

## 6. `S31-AC2` -- JUDGMENT, RECORDED FOR `3.0.0_SA_CVO` AT L9. NO VERDICT.

### 6.1 Which shape was taken and what was rejected

Answered in full at s.1. In brief: **shape (i), narrowed to a two-named-file removal** because
the literal directory removal collides with a CLAUDE.md hard stop; **shape (ii) rejected only
for want of the issuer's written word** and filed as a row; **shape (iii) rejected and, unusually,
MEASURED to be unworkable rather than assumed** (s.2 arm (c) -- the prefix was fully current for
49 seconds while the box imported the old modules); **a fourth shape (direct box-side overwrite)
rejected for proving less**, with its safety advantage recovered by other means.

### 6.2 Is any OTHER shared dependency of the renderer in the same condition? CENSUSED.

**The face is right that this cell was found through one symbol, so a recall-based answer would
be worthless. The census is a SUBTRACTION FROM A PRINTED DENOMINATOR** (CLAUDE.md rule 24), run
**on the box, post-act** (SSM `8a4af034-a9d2-4143-bb35-d479543632d6`, 19:52:15Z): import the
served renderer in place, take `sys.modules` -- every module actually loaded, transitively --
and subtract the three classes that cannot drift.

```
EGS31-CENSUS denominator: 403 module(s) loaded by importing the served renderer
  MINUS builtin/frozen (no __file__): 35
  MINUS stdlib (/usr/lib64/python3.9):   185
  MINUS site-packages: 175
  ===============================================
  REMAINDER -- files the BOX holds itself, and therefore the COMPLETE set that
  can be stale relative to its repo source: 8
```

Of the 8: **2 are the census harness itself** (`__main__`/`__mp_main__` = `/tmp/egs31_census.py`,
an instrument artefact) and **1 is the renderer** (`/opt/etfs-reports/render_month_end.py`,
which `lambda_function.py:652` re-pulls unconditionally and which therefore cannot go stale in
any way that reaches a run). **The remaining 5 are the complete staleable set, and all 5 are now
current:**

| module | box path | sha256 | repo source | state |
|---|---|---|---|---|
| `coverage` | `coverage/__init__.py` | `30995d06...` | `data/etfs/scripts/coverage/__init__.py` | CURRENT |
| `coverage.classifier` | `coverage/classifier.py` | `b2ab67fd...` | `data/etfs/scripts/coverage/classifier.py` | CURRENT (was stale) |
| `coverage.remediate` | `coverage/remediate.py` | `401bed2a...` | `data/etfs/scripts/coverage/remediate.py` | CURRENT (was stale) |
| `_orion_vendor_asof` | `coverage/_orion_vendor_asof.py` | `15d28dd8...` | `data/inf/scripts/silver/_orion_vendor_asof.py` | CURRENT |
| `trading_calendar` | `coverage/trading_calendar.py` | `41b1c0c1...` | `lib/trading_calendar.py` | CURRENT |

**ANSWER: no other shared dependency is stale today, and the set is closed with a denominator
rather than a list.** But the question the face asks has two readings, and they diverge:

- **By CONTENT: no.** 5 of 5 staleable files match their sources.
- **By MECHANISM: yes, one.** `_orion_vendor_asof.py` is protected by a **second presence-keyed
  self-heal**, `render_month_end.py:83-92`, `if not os.path.exists(...)`. A source-level sweep of
  the renderer for pull guards returns exactly three: `:74`/`:120` (`except ImportError`, this
  cell's) and `:84` (`os.path.exists`). **Two of the three are presence-keyed and neither can see
  staleness.** `_orion_vendor_asof.py` is current only by luck of nobody having edited
  `data/inf/scripts/silver/_orion_vendor_asof.py` since 2026-09-05. That is row `W4-S20`, ARMED.

**AND THE MORE IMPORTANT ANSWER, WHICH THE CENSUS FOUND AND THE CELL DID NOT PREDICT:** the
question "is another dependency stale" had a **yes** at the moment the order was cut.
`classifier.py` was stale too, carrying `EG-s-22`'s `slice_on_closed_day` work committed
2026-09-04 at `8471f83a18`. Three cells -- `EG-s-22`, `EG-s-28`, `EG-s-29` -- each verified their
own file and each was right; two of them had code that had never reached the box. **The finding
is not any one stale file, it is that the deploy step for `data/etfs/scripts/coverage/` is owned
by no cell in the decomposition.** Row `W4-S22`, ARMED. Both cells' code became live for the
first time at 19:41:50Z and 19:41:53Z, under this order.

### 6.3 Would a currency-aware self-heal (shape (ii)) have prevented this class, and what would it cost?

**Yes, and it is the only one of the three shapes that would.** Shape (i) fixes the instance --
if `remediate.py` changes again tomorrow, the box will again import the old one with no error at
any point, because the guard is `ImportError` and the module will still be present. The class
survives shape (i) completely; that is why the issuer priced (ii) as a separate future cell and
why row `W4-S20` is ARMED rather than closed by this order.

**Two forms, and the cheaper one is also the simpler one:**

1. **Manifest comparison (currency-aware, what the face names).** Compare a sha256 manifest of
   the prefix against the box copies and re-pull on mismatch. **Cost:** one `list_objects_v2`
   plus one `head_object` per member (5 calls, or 1 if a manifest object is published beside the
   package) per run, on a MONTHLY job -- negligible in time and money. **Risk:** it adds a new
   thing that can be wrong (a manifest that drifts from the objects it describes), and it is
   still a detector.
2. **Make both pulls UNCONDITIONAL, exactly as `lambda_function.py:652` already does for the
   renderer.** **Cost:** one `aws s3 cp --recursive` of about 42 KB per run, once a month. It
   deletes the ability to be stale rather than detecting it, needs no manifest and no new
   comparison logic, and makes all three of the box's artefacts obey **one** currency discipline
   instead of three. **This worker's read is that (2) dominates (1)** -- the estate already runs
   (2) for the renderer, it has never gone stale, and the asymmetry between line 652 and line 120
   is the entire defect.

**WHAT IT WOULD COST TO GET WRONG, stated because it is the reason this was not taken
unilaterally:** both forms edit `render_month_end.py` at module scope, above `main()`, on the
import path of every run. A mistake there does not degrade a report -- it exits rc=1 before
`main()`, which is precisely how `ETFS_GUARDRAIL-W1-S11` failed on 2026-09-09. That is a good
reason for the issuer's written word to be required, and this worker did not edit the file.

---

## 7. ARTIFACTS

| path | what |
|---|---|
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/test_egs31_box_package_matches_renderer.py` | the `S31-AC1` battery, 5 arms, one token |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/egs31_exercise_call_path.py` | the difference control; `--in-place` for the box, staged mode for pinned reproductions |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/egs31_pre_act_manifest.json` | pre-act state of all three writers, with S3 VersionIds |
| `.../deliverables/0.9.0_WK_ETFS_GUARDRAIL~4/fixtures/pre_act_deployed_coverage/*.pyfixture` | the pre-act deployed bytes, so arm (a) stays reproducible after the fix |
| `org/critical_paths/change_management/20260910T1933Z_egs31-...md` | the NEVER-2 entry, opened before the act, closed with 3 legs proven |
| `s3://opal-313476888478-lambda-artifacts/ec2/etfs-reports/coverage/{classifier,remediate}.py` | the deploy, 2 keys |
| `/opt/etfs-reports/coverage/` on `i-070477bf35fc54409` | 5 of 5 modules current, `ec2-user`-owned |

**`data/etfs/scripts/coverage/` was NOT edited by this order** -- the repo package was already
correct; this cell's whole job was to make the box run it. **`render_month_end.py` was NOT
edited.** **Push state: LOCAL, never pushed** (this worker does not push).
