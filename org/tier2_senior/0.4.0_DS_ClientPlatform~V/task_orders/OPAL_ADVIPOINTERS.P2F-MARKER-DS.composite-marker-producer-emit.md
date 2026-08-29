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
