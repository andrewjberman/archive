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
<status>pending -- ISSUED 2026-08-29 ~20:0xZ to give a face to an allocation that had none. See "Why this face exists" below; the ALLOCATION is not new, the FACE is.</status>
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
KEY        s3://opal-data-assets/schwab/{master}/meta/complete/date={YYYY-MM-DD}.json
           master = 08335338 for 49F. One object per (master, date). Overwrite-in-place on re-run.

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

CONSUMER   Match the KEY. Do NOT count objects, do NOT list the table prefix.
           `declared_tables == written_tables` (as sets) is the completeness predicate.
           A non-empty `disagreement` is a FINDING to surface, never a reason to fall back to a listing.
```

⛔ **`declared_not_written` will contain `fact_rlw` on every date until that spec is resolved.**
Stated here so the consumer is not surprised by a permanently non-empty disagreement block, and so
nobody "fixes" it by dropping `fact_rlw` from the declaration — **which member is wrong is an open
question and belongs to whoever owns the RLW feed, not to this emit.**

**STATUS: M-4 is the unblocking event and it is now stated. M-1 evidenced, M-3 measured. The emit
itself (M-2) is not yet built; this face carries the contract it will satisfy.**
