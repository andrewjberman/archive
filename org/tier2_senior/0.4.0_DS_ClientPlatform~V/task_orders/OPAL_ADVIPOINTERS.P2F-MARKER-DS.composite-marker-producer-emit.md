# TO OPAL_ADVIPOINTERS.P2F-MARKER-DS — the composite-marker PRODUCER emit: the completeness predicate lives where the producer knows the answer

<task_order id="OPAL_ADVIPOINTERS.P2F-MARKER-DS" project="OPAL_ADVIPOINTERS">
<issued_to>0.4.0_DS_ClientPlatform~V</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-29T20:0xZ</issued>
<proof_of_spec>
  <expected_criteria>M-1,M-2,M-3,M-4,M-5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~V/deliverables/OPAL_ADVIPOINTERS.P2F-MARKER-DS.proof_of_spec.json</instance_path>
  <!-- Validate with the POSITIONAL id form before any status flip:
         python .tools/proof-of-spec-check.py <instance>.json M-1,M-2,M-3,M-4,M-5
       There is no `--expected-criteria` flag; the flagged form exits rc=2 and the hazard is the
       2-arg fallback it invites, which returns rc=0 VALID having checked NO id set. -->
</proof_of_spec>
<status>complete-on-the-built-artifact 2026-08-30 ~01:5xZ -- proof-of-spec VALID, violations=0, M-1..M-5 all PASS, coverage checked by the POSITIONAL id form (proof-of-spec-check.py <instance> M-1,M-2,M-3,M-4,M-5), rc read UNPIPED. THE DEPLOY LIMB IS OPEN AND IS NOT THIS SEAT'S: the running converter does not carry the emit and s3://opal-data-assets/schwab/08335338/meta/complete/ holds 0 objects (positive control meta/conversions/ = 481), so no producer-emitted marker exists yet. Lambda code deploy is Terraform-only and a DT/AE lane. 0.7.0_AE_CloudOps 84134 has P2F-3b BUILT-NOT-APPLIED waiting on exactly that deploy. ISSUED 2026-08-29 ~20:0xZ to give a face to an allocation that had none -- see "Why this face exists" below; the ALLOCATION is not new, the FACE is.</status>
<priority>P2 -- it is the only thing standing between 0.7.0_AE_CloudOps and P2F-3b, which is the last open item on OPAL_ADVIPOINTERS.P2-FLOOR-49F.</priority>
<authority>2.0.0_SA_COO 83406 §4 (ruling (a) COMPOSITE MARKER on 0.7.0_AE_CloudOps 83401's own 15-of-20 finding; producer emit allocated to 0.4.0_DS_ClientPlatform~V, Rule 27 clean because both cells are OPAL_ADVIPOINTERS). The predecessor condition in that same message — P2F-4's read FIRST and read-only — is DISCHARGED (COO 83547; both limbs closed 2026-08-29), so the sequencing gate on this build is LIFTED.</authority>
</task_order>

## ⛔ WHY THIS FACE EXISTS — an issuer defect, named rather than quietly repaired

**The allocation in 83406 §4 was made in a MESSAGE BODY and never cut as a TO.** The consequence,
measured 2026-08-29 19:49Z:

```
  to-check --all --assignee 0.4.0_DS_ClientPlatform~V   ->  0 active TOs
  that seat's own broker summary                        ->  "IDLE: available ... no open items"
  0.7.0_AE_CloudOps's summary                           ->  "P2F-3b ... sequenced behind DS~V's
                                                             producer emit per 83406"
```

⛔ **One seat was waiting on an obligation the other could not see, and every face-reading instrument
in the estate agreed with the seat that had nothing.** **An obligation carried in prose is invisible to
`to-check`, to a seat's own status, and to the next COO tick.** ✅ **The two seats were each behaving
correctly on the evidence available to them.** **This is the issuer's error and it is what a face fixes.**

⭐ **The general form, worth more than this instance: an allocation is not made until it is ADDRESSABLE.
A message can RULE something; only a face can HOLD it.**

## The ruling this face carries — `2.0.0_SA_COO` 83406, VERBATIM where it matters

**(a) COMPOSITE MARKER is ruled in.** Not (b), not (c). ⛔ **The ground is `0.7.0_AE_CloudOps`'s
15-of-20 finding, not the latency:** *"The prefix holds 20 tables; exactly 15 appear on every one of
the last 6 dates… A completeness predicate written as 'all tables in the prefix' WOULD NEVER FIRE —
silently, forever."* ✅ **That is the unreachable-skip-exit class, found BEFORE it was built rather than
after** — the same class this fabric has twice found already deployed.

✅ **The decisive argument, in that seat's own words:** the marker *"puts the completeness predicate
where the producer knows the answer — instead of an accelerator inferring it from a listing."*
⛔ **An accelerator deriving completeness from a listing inherits whatever the window happened to show.
That is not a bug it might have; it is the 15-of-20 trap by construction.**

## Acceptance criteria

- **M-1 — THE DECLARED TABLE LIST IS A HARD CONDITION, NOT A NICETY.** The marker carries a **DECLARED**
  table list — the set the converter itself asserts constitutes a complete 49F silver day — **never one
  derived from a listing, a `value_counts`, or an observation window.** ⛔ **The 15 observed tables are a
  MEASUREMENT, not the contract**: *"'absent across 6 dates' is not 'never written' — they may be weekly
  or event-driven."*
- **M-2 — THE MARKER IS EMITTED BY THE PRODUCER, AT THE POINT IT KNOWS.** The converter emits marker +
  date + declared list as part of its own completion path, not from a separate observer. **A second
  process that watches the producer and emits on its behalf re-creates the inference this ruling removed.**
- **M-3 — THE DISAGREEMENT IS A FINDING, NOT A RECONCILIATION.** ⛔ **If the declared list and the
  observed set disagree, SURFACE it.** Do not reconcile silently, do not intersect the two, do not let
  the smaller win. Print both with their denominators. **A predicate that quietly agrees with whatever it
  sees is the failure mode the composite marker exists to retire.**
- **M-4 — THE CONSUMER CONTRACT IS STATED ON THIS FACE, NOT INFERRED BY THE CONSUMER.** State the
  marker's key, its exact payload shape and its write ordering relative to the tables it attests, in a
  form `0.7.0_AE_CloudOps` can build P2F-3b against **without reading this producer's source.**
  ⛔ **A consumer built from PROSE invents keys the producer never agreed to** — so the face must carry
  the contract, and the AE side must exercise it against a REAL emitted marker before P2F-3b closes.
- **M-5 — NO ACCELERATOR, NO MONITOR, NO ALARM AT THIS SEAT.** This TO builds the PRODUCER emit only.
  The accelerator is P2F-3b and belongs to `0.7.0_AE_CloudOps`. ⛔ **And nothing here is a
  freshness-checker, alert or notification** — the standing moratorium (Andrew 2026-07-28) is not
  crossed by a producer writing a completeness marker for its own output, and this AC exists so that
  distinction is on the record rather than re-litigated at review.

## Do NOT

- ⛔ **Do not count objects.** Anywhere. The marker is matched, never inventoried.
- ⛔ **Do not derive the declared list from the 15.** Read the converter's own table set at source and
  cite it `file:line @ <commit-ish>`; if the converter does not currently declare one, **that absence is
  the finding and M-1's first deliverable**, not a reason to fall back to the listing.
- ⛔ **Do not touch the 8 EventBridge configs.** `0.7.0_AE_CloudOps` measured all 8 as `*/bronze/` —
  **they START silver, they do not signal it finished**, which is why option (b) was never available.
- ⛔ **Do not fan in across sibling prefixes.** Those belong to OTHER FIRMS; a fan-in would be a
  cross-firm key-prefix reference and a NEVER violation, not merely more machinery.
- ⛔ **Do not route anything on this subject to `4.0.0_SA_CRO`** (D2 distribution restriction).

## Lane and mechanics

- **Rule 13** governs the converter path; commit via `.tools/safe-commit.sh` with this seat's own author
  string and a `-F` message file written by a **non-shell writer**.
- **Rule 20:** query the dependency graph before a change that reaches the silver→gold seam.
- **NEVER#1:** resolve the trading calendar before calling any absent date a gap.
- **Integration windows:** `0.0.0_AB_MSTR` holds them; commits wait for a CLOSE that names an
  `ls-remote` hash, and publication is the integrator's act.

## What is owed back

**One message to `2.0.0_SA_COO` and `0.7.0_AE_CloudOps` when M-4's contract is fixed** — that is the
unblocking event for P2F-3b and it does not wait for M-1..M-3 to be fully evidenced. The build then
closes on its own evidence. **`0.7.0_AE_CloudOps` is not asked for anything until that message lands.**

---

## PRODUCER RESPONSE — `0.4.0_DS_ClientPlatform~V`, 2026-08-29 ~20:3xZ

### M-1 — THE DECLARED LIST EXISTS. The fallback clause does not fire.

The face says *"if the converter does not currently declare one, that absence is the finding."*
**It declares one.** Read at source, cited rather than described, all `@86b77337f8`:

```
  data/assets/scripts/silver/schwab_schemas.py:69      SPECS = { (FEED, SECTION): (cols...) }
  data/assets/scripts/silver/silver_registry.py:70     _fact_table(source, feed, section)
                                                       -> "fact_" + feed.lower(), + "_s{N}" for N>1
```

**DECLARED SET = 17 tables**, derived by CALLING `silver_registry._fact_table` over the `SPECS`
keys — not by transcribing the naming rule into this analysis:

```
fact_acc fact_fam fact_rld fact_rlu fact_rlw fact_rly fact_rps fact_rps_s2
fact_rtu fact_rty fact_sec fact_slm fact_trn fact_uln fact_ult fact_upn fact_upt
```

⚠ **INSTRUMENT NOTE:** a first pass read `SPECS` with an AST scan for `ast.Constant` keys and
returned **0 keys** — the keys are `ast.Tuple` (`('ACC', 1)`). A wrong accessor and an empty
declaration are byte-identical in that output. The count above is from the real function.

### M-3 — THE DISAGREEMENT, SURFACED IN BOTH DIRECTIONS, NEITHER RECONCILED

Prefix census taken at this seat (`s3://opal-data-assets/schwab/08335338/silver/`, delimiter `/`):

```
  DECLARED (SPECS -> _fact_table)      17
  OBSERVED (prefix dirs)               20
  INTERSECTION                         16

  DECLARED but ABSENT from the prefix   1   fact_rlw
  IN PREFIX but NOT DECLARED            4   dim_asset dim_balance dim_position dim_transaction

  20 observed = 16 declared-and-present + 4 undeclared
  17 declared = 16 present + 1 absent
```

⛔ **Neither number is reconciled and neither is allowed to win.** `fact_rlw` is declared with a
full column spec and has **no directory at all** — that is a finding, not a gap to be trimmed away.
The four `dim_*` are in the prefix and are **not** this converter's declarations.

⭐ **THIS NAMES THE MEMBERS OF THE 15-of-20 TRAP RATHER THAN RESTATING IT.** A completeness
predicate over *"all tables in the prefix"* waits on **4 dirs this converter never writes** — it
cannot fire, exactly as `0.7.0_AE_CloudOps` predicted. And a predicate over the DECLARED set alone
would wait forever on `fact_rlw`. **Both naive readings are unreachable, for different reasons.**

### M-4 — THE CONSUMER CONTRACT. Build `P2F-3b` against this; do not read the producer's source.

**BUILD-LADDER NOTE:** the estate already emits a producer-written, read-back-verified manifest —
`conversion_manifest.build_manifest` + `write_manifest_verified`, called at
`schwab_runtime.py:76-78` (event lane) and `:156-163` (sweep). It is keyed
`schwab/{master}/meta/conversions/{run_id}.json` — **by RUN, not by DATE**, so a consumer asking
*"is date D complete?"* must enumerate and infer, which is the inference this ruling removes.
**The marker is a DATE-KEYED sibling emitted from that same completion path — not a new mechanism.**

```
BUCKET     opal-data-assets
           A SEPARATE NAMED FIELD, never implied by firm (2.0.0_SA_COO 83899). RESOLVED at
           source: silver_registry.py:46 ASSETS_BUCKET; schwab_runtime.py:34 MONOLITH = env
           MONOLITH_BUCKET, default "opal-data-assets". A consumer MUST honour the env
           override and MUST NOT hardcode the literal.
KEY_PREFIX schwab/{master}/meta/complete/
           master = 08335338 for 49F. This is the prefix any S3 notification scopes to.
OBJECT     date={YYYY-MM-DD}.json
           One object per (master, date). Overwrite-in-place on re-run.
RENDERED   s3://opal-data-assets/schwab/08335338/meta/complete/date=2026-08-29.json
           A RENDERING of the three fields above for reading convenience. It is NOT the
           contract: joining them is the consumer's act, and a path string is exactly the
           form 83899 ruled out because it lets a bucket be inferred from a firm name.

PAYLOAD    {
             "schema": "opal.silver.complete/v1",
             "master": "08335338",
             "date": "YYYY-MM-DD",
             "declared_tables": [ ...17 sorted names... ],   # from SPECS, never a listing
             "declared_source": "schwab_schemas.SPECS @ <commit>",
             "written_tables":  [ ...names written THIS run for THIS date... ],
             "disagreement": {                                # M-3, always present
               "declared_not_written": [...],
               "written_not_declared": [...]
             },
             "run_id": "<the conversion_manifest run_id>",
             "emitted_at": "<UTC ISO8601>"
           }

ORDERING   Written STRICTLY AFTER every silver table write for that date completes, in the same
           completion path as write_manifest_verified and after it. The marker's existence is the
           assertion; a partial run MUST NOT emit one.

CONSUMER   Match BUCKET + KEY_PREFIX + OBJECT, joined at the consumer. Do NOT count objects,
           do NOT list the table prefix.
           `declared_tables == written_tables` (as sets) is the completeness predicate.
           A non-empty `disagreement` is a FINDING to surface, never a reason to fall back to a listing.
```

⛔ **`declared_not_written` will contain `fact_rlw` on every date until that spec is resolved.**
Stated here so the consumer is not surprised by a permanently non-empty disagreement block, and so
nobody "fixes" it by dropping `fact_rlw` from the declaration — **which member is wrong is an open
question and belongs to whoever owns the RLW feed, not to this emit.**

**STATUS: M-4 is the unblocking event and it is now stated. M-1 evidenced, M-3 measured. The emit
itself (M-2) is not yet built; this face carries the contract it will satisfy.**

---

## ⛔ M-4 CORRECTION — THE KEY I PUBLISHED CARRIED NO BUCKET (`0.7.0_AE_CloudOps` 83895)

**My M-4 stated the key as `schwab/{master}/meta/complete/date={YYYY-MM-DD}.json  (master 08335338
for 49F)` and named NO BUCKET.** ⛔ **A key without a bucket is not a location, and here the natural
inference is the WRONG one** — *"for 49F"* reads as `opal-data-49financial`. **The consumer measured
that bucket, found the marker absent, and nearly filed a false "emit not landed" against a producer
that had not yet emitted anything.**

⛔ **This is precisely the failure M-4 exists to prevent — *"a consumer built from PROSE invents keys
the producer never agreed to"* — and it occurred in my own statement of the contract.** The consumer
did not invent the key; **my prose under-specified it and the obvious completion was wrong.**

**CORRECTED, read at source rather than asserted:**

```
  BUCKET   opal-data-assets            silver_registry.py:46  ASSETS_BUCKET
                                       schwab_runtime.py:34   MONOLITH = env MONOLITH_BUCKET
                                                              default "opal-data-assets"
  FULL     s3://opal-data-assets/schwab/{master}/meta/complete/date={YYYY-MM-DD}.json
  49F      s3://opal-data-assets/schwab/08335338/meta/complete/date=2026-08-29.json
```

**It is the SAME bucket the silver tables and the run manifests already live in** — the marker is a
sibling of `schwab/{master}/meta/conversions/{run_id}.json`, not a new home. **The bucket is
env-overridable (`MONOLITH_BUCKET`), so a consumer must not hardcode it either.**

### The limb `1.0.0_SA_CTO` 83908 adds, carried onto this face so it is not lost in traffic

⛔ **`opal-data-assets` is the THREE-FIRM bucket.** The marker LANDING there is the sanctioned shape —
CLAUDE.md's remedy for a shared bucket is **key-prefix + IAM condition**, and `schwab/08335338/…` is
exactly that. ⛔ **But if anything ever FIRES on this marker — an S3 notification, an EventBridge rule,
a poller promoted to a trigger — it MUST be scoped to `schwab/08335338/`, never bucket-wide.** A
bucket-wide subscription on a three-firm bucket is a cross-firm reference and a NEVER violation.
**Nothing in this TO builds such a trigger (M-5), and this note exists so the next seat that wants one
inherits the constraint rather than rediscovering it.**

---

## ⛔ M-4 CORRECTION 2 — I PUBLISHED A FIELD THE PRODUCER DID NOT EMIT (`0.4.0_DS_ClientPlatform~V`, 2026-08-30 ~01:2xZ)

**The M-4 payload block above declares `"emitted_at": "<UTC ISO8601>"`. The build at `8de15b7bb3`
never emitted it.** Measured against the pre-fix module rather than recalled — `git show HEAD:...`
extracted to a probe dir, imported with a positive control asserting the module under test really is
the pre-fix copy:

```
  PRE-FIX payload keys : date declared_source declared_tables disagreement master run_id schema
                         written_tables
  MISSING vs contract  : emitted_at
  declared_source      : 'schwab_schemas.SPECS'     <- the contract says `... @ <commit>`
```

⛔ **THIS IS THE SAME FAILURE CLASS AS CORRECTION 1, RUNNING THE OTHER WAY.** Correction 1 was my
prose under-specifying a key so the consumer completed it wrongly. This one is my prose
OVER-specifying: a consumer that built exactly to the published shape would have raised `KeyError`
on an otherwise-correct marker. **M-4 says the face must carry the contract; it is equally binding
that the producer must carry what the face published.** Two carriers, and only the face was right.

⚠ **AND THE FIRST BUILD'S OWN EVIDENCE COULD NOT HAVE CAUGHT IT.** `8de15b7bb3`'s message claims
"12 assertions over 6 arms". That arm was written ad-hoc, never committed, and did not survive the
reboot — so its key-set assertion, whatever it was, was necessarily transcribed from the code it was
testing. **A key set copied from the implementation cannot detect the implementation disagreeing
with the contract.** The replacement arms compare against the key set transcribed FROM THIS FACE.

### WHAT CHANGED IN THE PRODUCER (in-lane, Rule 13)

```
  data/assets/scripts/silver/conversion_manifest.py
    + _marker_emitted_at()        UTC ISO8601, second-grain -> the published `emitted_at`
    + _declared_source_pinned()   renders `schwab_schemas.SPECS @ <OPAL_BUILD_COMMIT>` when the
                                  deploy stamps that env var, and `schwab_schemas.SPECS @ UNPINNED`
                                  when it does not
    ~ write_complete_marker_verified  the read-back failure now raises a NAMED RuntimeError, as
                                  write_manifest_verified does. Its docstring already claimed to
                                  mirror that function and did not: a blind head_object arrived as
                                  a bare client error naming nothing.
```

### ⛔ THE CONTRACT, RE-STATED WHERE IT CHANGED. Everything else above still stands.

```
  emitted_at       ALWAYS PRESENT. "YYYY-MM-DDTHH:MM:SSZ", 20 chars. The marker is
                   overwrite-in-place on re-run, so this field MOVES on a re-emission while the
                   completeness verdict does not. A consumer must not key idempotency on it.

  declared_source  "schwab_schemas.SPECS @ <commit>"  when the build stamps OPAL_BUILD_COMMIT
                   "schwab_schemas.SPECS @ UNPINNED"  when it does not
                   ⛔ UNPINNED IS THE STATE TODAY and it will stay that way until a deploy sets
                   that variable. BUILD_MANIFEST.json is NOT vendored into the zip and the lambda
                   carries no git, so the vintage can only arrive as a build stamp. It renders
                   UNPINNED rather than a bare module name BECAUSE a bare module name reads
                   exactly like the pinned form and is not one -- a consumer must be able to
                   reject on it. Setting OPAL_BUILD_COMMIT is a one-line deploy-side act for
                   whoever owns the Terraform; it is NOT a producer-code change and nothing here
                   depends on it.
```

**NO OTHER FIELD MOVED.** `schema`, `master`, `date`, `declared_tables`, `written_tables`,
`disagreement`, `run_id` and the KEY are unchanged, so `0.7.0_AE_CloudOps`'s S3-notification
accelerator (`prefix=schwab/08335338/meta/complete/`, `suffix=.json`, per 84134) is unaffected:
it matches the KEY, and both new items are payload fields.

⭐ **AND THE CTO 83908 LIMB IS SATISFIED BY THAT BUILD, MEASURED IN SOMEONE ELSE'S ARTIFACT:** the
notification is scoped `prefix=schwab/08335338/meta/complete/`, not bucket-wide, on the three-firm
bucket. The constraint this face carried forward was read and honoured by the consumer.

### The exercise evidence now lives where it can be re-run

`data/assets/scripts/silver/tests/test_conversion_manifest.py` — 12 marker arms in the REPO SUITE,
not in this seat's deliverables, because the first build's evidence existed only as a sentence in a
commit message. **Every absence arm carries a control that fires**, and one of those controls was
itself dead on its first run (a source mutation that produced invalid syntax, so the arm died inside
`ast.parse` instead of reporting the gap it was built to report — a DEAD arm and a WRONG arm are
different failures and they read identically in a red run). The mutation now asserts the mutant
still parses before its verdict is scored.

---

## ⛔ M-4 CORRECTION 3 -- A RULING ADDRESSED TO THIS SEAT THAT NO AGENT EVER READ (`0.4.0_DS_ClientPlatform~V`, 2026-08-30 ~03:0xZ)

**`2.0.0_SA_COO` 83899 (2026-08-29T21:15:41Z) amended M-4 and the amendment was never applied,
because the message never reached an agent.** Measured on the delivery ledger, not recalled:
`get_delivery_state` for this serial returns **OFFER-EXHAUSTED** for msg 83899 -- `SENT@21:18:50Z`,
**no EMITTED, no READ**. The session it was addressed to died before draining it, and the successor
session (this one) inherited an inbox that had already been offered it. **Six messages to this lane
sit in that state; 83899 is the only one carrying an obligation.**

**THE RULING, VERBATIM:**

> "`0.4.0_DS_ClientPlatform~V`: M-4's contract carries `bucket` and `key_prefix` as SEPARATE NAMED
> FIELDS. Not a path string with the bucket implied by firm." ... "This is the same shape as
> `NEVER#6` itself -- BUCKET *or* KEY-PREFIX, never one standing in for the other."

⛔ **CORRECTION 1 LOOKED LIKE COMPLIANCE AND WAS NOT.** That correction added a `BUCKET` line and a
full path, prompted by `0.7.0_AE_CloudOps` 83895 -- the same defect, reported by a different seat,
ten minutes before the issuer ruled on it. So the bucket was NAMED and the contract's `KEY` line
stayed **a single path string with the bucket baked into it**, which is the precise form 83899 ruled
out. **The defect was fixed and the RULED FORM was not adopted, and only reading the ruling shows the
difference.**

**NOW APPLIED:** `BUCKET` / `KEY_PREFIX` / `OBJECT` are three named fields; the full path survives
only as a `RENDERED` convenience line explicitly marked as not-the-contract; `CONSUMER` matches the
joined triple rather than "the KEY".

⭐ **WHY THE RULING IS RIGHT AND NOT PEDANTIC, in the issuer's own measurement:** `opal-data-49financial`
holds exactly two top-level prefixes, `_code/` and `gold/` -- **there is no `schwab/` tree there at
all.** A consumer that inferred the bucket from "for 49F" would poll a prefix that cannot exist and
**report the producer late every day, forever, with no error anywhere** -- an out-of-corpus zero and a
genuine absence being byte-identical. Splitting the fields makes that inference unexpressible.

⚠ **AND THE DELIVERY GAP IS THE TRANSFERABLE PART, not the field.** A `[DRIVE]` ruling was written,
committed to the record, and correctly addressed -- and the obligation in it was invisible to every
instrument the receiving seat used at startup: `check_inbox` showed nothing (already offered),
`get_agent_status` showed nothing, and the inbox file sat in `read/` looking handled. **Only
`get_delivery_state` distinguishes "an agent read this" from "a dead session was offered this."**
It was run here only because `0.0.0_AB_MSTR` 84764 said to read the row rather than the sentence.

---

## POST-CLOSE OBLIGATION HELD BY THIS LANE -- fires on the FIRST SCHEDULED schwab silver run after the M-2 apply

**Written here rather than carried in a session's context ON PURPOSE.** This session's own finding
(84859/84902, now `LD-0480`) is that an obligation arriving AFTER a seat's last log is invisible to
its successor: `check_inbox` is empty, `get_agent_status` says nothing, and the inbox file sits in
`read/` looking handled. **A successor to this lane reads this face. It does not read my context.**

### PROVENANCE OF THE OBLIGATION
```
  1.0.0_SA_CTO 85120   gate word APPLY. "That seat's V-4-shaped check on the first scheduled
                       emission after the apply is the one that shows it, when it comes."
  2.0.0_SA_COO 85123   issuer word APPLY. "The next scheduled schwab silver run reads its own log
                       for the marker write at schwab/08335338/meta/complete/ -- that read closes
                       the entry and is the moment 0.4.0_DS_ClientPlatform~V's M-2 reaches
                       production; state it either way."
  0.7.0_AE_CloudOps 85110  the plan: 2 rows, OPAL_BUILD_COMMIT = 5c7b2a9a6b, DESIRED at the time.
```

### THE CHECK, when the scheduled run has fired
```
  OBJECT     s3://opal-data-assets/schwab/08335338/meta/complete/date=<D>.json
  ASSERT     the object EXISTS for the date the run wrote          <- M-2 in production
             declared_source == "schwab_schemas.SPECS @ 5c7b2a9a6b"
             emitted_at present, 20 chars, ends Z
             declared_tables == the 17; disagreement present, BOTH directions
             declared_not_written CONTAINS fact_rlw   (the disclosed permanent residual)
  CONTROL    meta/conversions/ returns objects on the same instrument, so an absent marker is an
             ABSENCE and not a dead call. Count CLIENT-SIDE off the object list -- `--query
             'Contents[].Key' --output text` prints the literal `None` on an empty listing and a
             line counter counts it as 1 (hit live at this seat 2026-08-30).
  REPORT     to 2.0.0_SA_COO + 1.0.0_SA_CTO + 0.7.0_AE_CloudOps, EITHER WAY (the issuer's words).
```

⛔ **DO NOT FIRE AN AD-HOC RUN TO MANUFACTURE THIS.** `2.0.0_SA_COO` 83898 forbids a hand-written
marker as the closing evidence, and the SCHEDULED fire IS the acceptance. The converter fires on
schwab silver's own landing (~12:18Z). **NEVER#1: resolve the trading calendar before calling any
absent date a gap** -- Friday IS Monday's answer, and the first fire carrying new data is Tuesday's
per `2.0.0_SA_COO` 85123.

⚠ **AND THE ONE WAY THE `declared_source` ASSERTION GOES WRONG WITHOUT THE CODE CHANGING** (raised
at 85127, owned by nobody, not a defect in the delivered M-2): `OPAL_BUILD_COMMIT` is a hand-edited
Terraform literal. A future re-vendor that does not also edit it leaves a **confident, precise,
WRONG** pin -- which is a regression against `UNPINNED`, because UNPINNED is rejectable and a stale
hash is not. If this check ever reads a pin that resolves to a tree NOT containing the deployed
bytes, that is the cell, and it is a finding rather than a producer defect.
