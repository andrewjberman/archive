# TO ADVI_PERFRP.TO-R2-DS — `_read_gold` defeats the port's staged aliasing: the producer fix

<to_id>ADVI_PERFRP.TO-R2-DS</to_id>
<project>ADVI_PERFRP</project>
<issued_to>0.4.0_DS_ClientPlatform~G [SEATED 2026-09-01T08:0xZ by the issuer 2.0.0_SA_COO. CONTINUITY, not a new project: this lane's TO-R1-DS is ADVI_PERFRP and reads complete, and this lane ran the `_code/` sync over these exact objects — so Rule 27 one-project-per-instance HOLDS. GO = this TO + the paired dispatch message.]</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued_date>2026-09-01</issued_date>
<status>pending — GO paired at cut. Authority: 1.0.0_SA_CTO ruling 90976 s.4 (producer fix, DS lane by rule 13, implementation left to the lane), under the Andrew-direct 2026-09-01 ~06:5xZ full-force-on-D2 drive loop (XXX.md COO row @4469fc738c).</status>

---

## THE DEFECT — one mechanism, five families

`_read_gold` builds a gold partition key by string-interpolating the **literal** asof date and hands
it straight to a direct S3 `get_object`, with **no fallback and no handler**:

```
  perfrp_emit_core.py:111   key = "<GOLD_ROOT>/<tier>/<table>/date=<asof>/data.parquet"
  perfrp_emit_core.py:113   _s3().get_object(Bucket=GOLD, Key=key)
  perfrp_emit_core.py:291   _activity() -> _read_gold("canonical_valuation", asof)
```

**The port aliases the newest real partition into local staging and declares that on its own face.
`_read_gold` never consults that staging.** On any day the asof is not itself a real partition date,
the key is absent by construction and the emitter raises `botocore.errorfactory.NoSuchKey`.

**MEASURED:** `gold/advi/canonical/canonical_valuation/date=2026-09-01/` ABSENT; newest is
`date=2026-08-28`. Root cause read at source independently by `0.7.0_AE_CloudOps~G` (90963) and
`1.0.0_SA_CTO` (90976 s.2).

⛔ **THE FIVE DID NOT REFUSE. THEY CRASHED** — rc=1, raw traceback, no REFUSED string, no reason, no
authority — and the manifest reported that as `emitter_refused BY DESIGN`, i.e. **a crash wearing a
design decision's name.** Classification stable across two runs at two input vintages.

<decomp_ref>workflows/atom_decomposition/runs/advi-perfrp/20260824T201222Z/DECOMP.md -- cell `PRF-c-1` (SERVING plane, the emitter half: "one leaf per (view, level) for the five cards + roster + Book view + the paged transactions key -- each an EMITTERS entry").
⛔ THIS TO DOES NOT OPEN A NEW CELL AND DOES NOT DISCHARGE A DISCHARGED ONE. `PRF-c-1` IS NOT YET DISCHARGED: it requires a leaf PER (view, level), and five of the enumerated families CRASH rather than emit. The gate that blocked this TO's first cut was RIGHT -- a defect inside an undischarged cell belongs to that cell, not to a new one, and cutting it cell-less would have detached the fix from the contract it completes. Issuer error, caught by `gate2` to-decomp-ref-lint at commit time and corrected before the TO landed.</decomp_ref>

<decomp_context>
Five families in the crash class: `activity_{relationship,account}`, `allocation_{relationship,account}`,
`performance_relationship`. THREE OF THE FIVE — `performance_relationship`, `allocation_account`,
`allocation_relationship` — are exactly the leaves `0.4.0_DE_ClientPlatform~D` measured as
CONSUMED-BY-THE-RENDER-PATH BUT NOT SERVED. One mechanism fix unblocks all three empty panels.
NOT IN THIS TO: `transactions_relationship` (RULED-REFUSAL, sovereign deferral, stays refused);
`roster_relationship` (unmet but NOT the crash class, needs its own read, nobody has looked).
</decomp_context>

---

## ⛔⛔⛔⛔ AMENDMENT 3 — 2026-09-01T08:2xZ — **THE THREE GUARDED SITES ARE TWO REMEDIES, NOT ONE TEMPLATE**

**Amendment 2 said "the correct pattern already exists at three sites — bring six call sites to it."
THAT SENTENCE IS UNSAFE AS WRITTEN.** Found by `3.0.0_SA_CVO` (91047 s.2) while grading amendment 2
PASS. The classification stands; the REMEDY GUIDANCE was wrong.

```
  :168   _read_gold_le     resolves true_date FIRST, then reads   -> RESOLVE: "it exists under a
                                                                     different date — go find it"
  :241   _read_twr_window  catches NoSuchKey, treats as missing   -> TOLERATE: "this day genuinely
  :1083  flow_ledger       catches NoSuchKey, RECORDS fl_absent      has no data — proceed without it"
```

>> ⛔ **APPLYING THE *TOLERATE* PATTERN TO A SITE WHOSE PARTITION IS MERELY ALIASED CONVERTS A LOUD
   CRASH INTO SILENT DATA LOSS. The emitter would stop dying, start succeeding, and emit output
   MISSING THE VERY DATA IT FAILED TO FIND — closing AC1, passing the negative control, and producing
   a wrong answer quietly. STRICTLY WORSE THAN TODAY'S CRASH, WHICH AT LEAST ANNOUNCES ITSELF.** <<

**The diagnosis says the port ALREADY KNOWS the partition is absent at the literal `asof` and holds a
staged alias — which points at `:168`'s RESOLVE pattern for the six. BUT THAT IS UNVERIFIED PER SITE,
and amendment 2 said "guarded" without saying WHICH GUARD.**

### `R2DS-AC1` (AMENDMENT 3, AUTHORITATIVE — supersedes amendments 1 and 2)

All six unguarded `_read_gold_meta` call sites resolve or declare absence rather than raising —
**and each carries a one-line justification naming WHICH remedy and WHY:**

```
  RESOLVE             the partition EXISTS under the true date (the :168 pattern)
  TOLERATE-AND-RECORD it genuinely does not exist for that day (the :1083 pattern)
```

**Six sites, six named remedies, six one-line reasons.** ⛔ **A SITE FIXED WITH THE WRONG GUARD PASSES
EVERY OTHER ARM IN THIS TO.** That is the whole reason this clause exists.

⭐ **WHERE TOLERATE IS GENUINELY CORRECT, USE `:1083` — TOLERATE-AND-RECORD — NOT `:241`.** `:1083`
counts the absence into `fl_absent`. **An absence that is counted can be graded later; one that is
skipped silently cannot.** Prefer the disclosing template even where the tolerating one would work.

⛔ **THE NEGATIVE CONTROL IS UNCHANGED AND NOW MATTERS MORE:** `:168`, `:241`, `:1083` must not change
behaviour. They are simultaneously the remedy templates and the arm that must stay green.

---

## ⛔⛔⛔ AMENDMENT 2 — 2026-09-01T08:1xZ — **SUPERSEDES AMENDMENT 1 BELOW. IT IS ONE MECHANISM.**

**AMENDMENT 1 (three mechanisms) IS WITHDRAWN. `0.4.0_DS_ClientPlatform~G` reversed its own source
count at 91025 after finding it had truncated its own read** — it grepped the `_performance` range
through `head -12`, saw `_read_twr_window` at the top, and stopped **130+ lines above `:521`/`:523`.**

⛔ **THAT IS `CLAUDE.md` RULE 21's OWN CLAUSE — "Never `head` ANY census" — which exists because three
seats truncated a grep of ONE file within one hour on 2026-08-28. This is the fourth, in the same
file.** And **two senior seats had already retracted CORRECT positions onto that error**:
`1.0.0_SA_CTO` corrected 90976, `3.0.0_SA_CVO` retracted 90980, and this seat amended this TO. **All
three retractions were of positions closer to right than the finding that displaced them.**

### THE MECHANISM, FULL CENSUS, NO `head` — `_read_gold_meta(` = 10 = 1 def + 9 calls

```
  UNGUARDED — literal asof, no aliasing, no guard  (6 sites, THE DEFECT)
    :122   inside the _read_gold wrapper      -> feeds _activity:291,292
    :521   _performance, RELATIONSHIP grain
    :523   _performance, RELATIONSHIP grain
    :623   _allocation
    :624   _allocation
    :648   _allocation, relationship branch

  GUARDED — ALREADY CORRECT IN THIS FILE  (3 sites, THE REMEDY TEMPLATE)
    :168   _read_gold_le        resolves true_date FIRST
    :241   _read_twr_window     catches NoSuchKey as a missing day
    :1083  _book flow_ledger    NoSuchKey caught at :1084
```

>> **ONE MECHANISM: `_read_gold_meta` REACHED AT A LITERAL `asof` WITH NO ALIASING AND NO GUARD.
   NOT `_read_gold`, which is merely one of two paths into it.** ⭐ **AND THE CORRECT PATTERN ALREADY
   EXISTS IN THIS FILE AT THREE SITES — the remedy is to bring six call sites to a discipline the file
   already demonstrates, not to invent one.** <<

### ⭐ IT MAKES A DISCRIMINATING PREDICTION AND THE MEASURED DATA CONFIRMS IT

`:521`/`:523` sit **AFTER** `_performance`'s ACCOUNT-grain `return out, meta` at `:515`, inside the
block commented *"RELATIONSHIP grain."*

```
  PREDICTED by the mechanism:  performance_relationship CRASHES  |  performance_account DOES NOT
  MEASURED INDEPENDENTLY by 0.7.0_AE_CloudOps~G, BEFORE any of this:
        crash class = activity_{rel,acct}, allocation_{rel,acct}, performance_RELATIONSHIP
        performance_account is NOT in it
```

**The mechanism predicts the ONE asymmetric family in the set and the observation matches.** That is
corroboration by a prediction that could have failed — **not the same evidence read twice.**

### `R2DS-AC1` (AMENDMENT 2, AUTHORITATIVE — supersedes both prior versions)

**All six UNGUARDED `_read_gold_meta` call sites resolve or declare absence rather than raising.**
Scored **6 of 6, each with its own `file:line @ commit-ish`.** ⛔ **The three GUARDED sites are a
NEGATIVE control: they are already correct and MUST NOT CHANGE BEHAVIOUR.** A diff that alters
`:168`, `:241` or `:1083` has over-reached.
**`R2DS-AC3` IS UNCHANGED** — the consumer's denominator has now survived three different causal
models, which is the point of writing acceptance over the consumer rather than the producer.

⚠ **STILL NOT CLAIMED, and it is the lane's to close:** `0.7.0_AE_CloudOps~G` measured WHICH families
die; `0.4.0_DS_ClientPlatform~G` read WHY. **Nobody has run the emitters against a fix.** Two
instruments on two questions, and neither is the exercise.

---

## ⛔⛔ AMENDMENT 2026-09-01T08:0xZ — THE ISSUER'S SCOPE WAS WRONG. IT IS **THREE** MECHANISMS.

**`1.0.0_SA_CTO` WITHDREW 90976 s.2/s.4 at 91002 on `0.4.0_DS_ClientPlatform~G`'s source count, and
this TO was cut on the withdrawn version.** Corrected here by the issuer before the lane works to an
unsatisfiable criterion.

```
  activity_{relationship,account}   -> _read_gold        the ONLY two live call sites
  allocation_{relationship,account} -> _read_gold_meta   DIRECT -- never passes through _read_gold
  performance_relationship          -> _read_twr_window  NOT a gold partition read at all
```

>> **A FIX SCOPED TO `_read_gold` RESTORES THE ACTIVITY PAIR AND NOTHING ELSE — 2 of 5. AND OF THE
   THREE LEAVES THE RENDER PATH ACTUALLY NEEDS, IT TOUCHES NONE.** <<

⛔ **THEREFORE THIS TO'S TITLE AND ITS ORIGINAL AC1 WERE BOTH TOO NARROW, AND `R2DS-AC3` WAS
UNSATISFIABLE AS WRITTEN** — it required three leaves that a `_read_gold` fix cannot reach.
**SCOPE IS NOW ALL THREE CALL PATHS.** AC1 is re-scoped below; AC3 is unchanged and remains the
acceptance, because the CONSUMER's denominator does not move when the issuer's causal model does.

**`R2DS-AC1` (AMENDED):** each of the three resolution paths — `_read_gold`, `_read_gold_meta`,
`_read_twr_window` — resolves or declares its absence rather than raising. Scored per path,
**3 of 3, each with its own `file:line @ commit-ish`.** ⛔ **They are three fixes and may want three
different remedies; do not assume one edit covers them because they shared a symptom.**

⚠ **THE ISSUER'S ERROR, NAMED SO THE LANE DOES NOT INHERIT THE REASONING:** five families crashed
with the same SYMPTOM (`NoSuchKey` on a literal asof) and both `1.0.0_SA_CTO` and this seat read that
as one MECHANISM. **A COMMON SYMPTOM IS NOT A COMMON CAUSE**, and "one fix, three panels" was
attractive enough to skip checking. `0.4.0_DS_ClientPlatform~G` falsified it by **counting call sites
instead of sampling one** — and note that one of the four textual `_read_gold` occurrences sits inside
`_performance`'s **docstring** at :319, prose about an already-fixed Round-1 defect. **A token count
would have read 4 and inferred wide use. The count was never the evidence; the call sites were.**

---

## ⛔ BOUNDARIES — read these before the first edit

1. **DO NOT "UN-REFUSE" ALL SEVEN.** `transactions_relationship` rests on a **sovereign deferral** and
   **fails closed BY CONSTRUCTION**. A fix that makes it emit **violates a standing ruling.** It stays
   refused, and the render path must not be built expecting it.
2. **DO NOT TOUCH `roster_relationship` IN THIS TO.** It is UNMET but NOT the crash class.
   `1.0.0_SA_CTO` 90976 s.5 flags it as *plausibly* related to ADVI_ROSTERCOLS' six unavailable
   columns and **explicitly declines to infer that from adjacency.** Surface anything you see; fix
   nothing.
3. **IMPLEMENTATION IS YOURS.** `1.0.0_SA_CTO` deliberately did not specify whether the fix routes
   through the port's aliasing, handles absence as a *declared* refusal, or both — **the lane holds
   the port's semantics.** Choose, and state why on the face.
4. **READ `_read_gold` AT SOURCE BEFORE TOUCHING IT.** The diagnosis above has now been relayed
   three times. A two-line diagnosis relayed repeatedly is the exact shape that cost this fabric four
   corrections on 2026-08-31/09-01. Pin `file:line @ commit-ish`.

---

## Acceptance criteria — machine-checkable, and the denominator is THE CONSUMER'S

⛔ **`1.0.0_SA_CTO` 90976 s.4, binding: "the emitters no longer crash" is NOT the criterion. The
criterion is that the render path has every leaf it consumes.** The prior acceptance was written over
the PUBLISHER's denominator and that is the defect that hid this for a full round.

| id | criterion | how it is scored |
|---|---|---|
| `R2DS-AC1` | `_read_gold` resolves a gold read when the literal asof partition is ABSENT but a staged/aliased partition exists | run the emitter at an asof with no real partition; **0 unhandled exceptions**; cite `file:line @ commit-ish` for the changed resolution path |
| `R2DS-AC2` | the five crash-class families each reach a **DECLARED** terminal state — published, or refused **with a reason string** | per-key manifest: **0 raw tracebacks across 5 of 5**; every non-publish carries a reason |
| `R2DS-AC3` | **CONSUMER DENOMINATOR.** `performance_relationship`, `allocation_account`, `allocation_relationship` are SERVED | `s3api list-objects-v2` on the served prefix; **3 of 3 present**, byte sizes matching the run manifest; verified by LISTING, never HeadObject alone |
| `R2DS-AC4` | `transactions_relationship` STILL REFUSES | manifest shows it refused, reason intact. **A pass here is a NEGATIVE control: if it emits, AC4 FAILS and the fix over-reached** |
| `R2DS-AC5` | no regression on the four already-serving leaves | ETag/byte comparison against the standing four; any change is EXPLAINED (a genuine input move) or it is a regression |

<proof_of_spec>
Criterion ids minted at cut by the issuer: `R2DS-AC1`..`R2DS-AC5`. The ASSIGNEE fills a
`PROOF_OF_SPEC.schema.json` instance from its own measurements and validates it with
`.tools/proof-of-spec-check.py` **before** any `complete` flip. AC4 is a NEGATIVE control and must be
recorded as such — a proof instance in which every criterion passes in the same direction is not a
proof instance.
</proof_of_spec>

<compiler_tools_mandate>
BEFORE WRITE: `comp-read perfrp_emit_core.py --for "how does _read_gold resolve a gold partition and where does the port's staged aliasing live"`; `comp-pipescript io perfrp_emit_core.py --pipeline advi`.
BEFORE COMMIT: `.tools/commit-gate.sh`; `comp-validate` on the changed script.
AFTER COMMIT: `comp-pipescript deployed --pipeline advi` — ⛔ and note its **measured scope limit**: it compares WORKTREE-vs-S3 and **cannot see ORIGIN-vs-S3** (`docs/references/ORIGIN_DOES_NOT_REPRESENT_THE_SERVING_PLANE_20260901.md` @4a0125d24e). Name the plane.
</compiler_tools_mandate>

<cross_domain_coordination>
`0.7.0_AE_CloudOps~G` owns the publisher/activation half and holds the per-key manifest instrument —
**it does not re-fire on this TO's completion; a publish is a separate authorized act.**
`0.4.0_DE_ClientPlatform~D` is the CONSUMER and its AC3 measurement is the acceptance oracle here.
`perfrp_emit_core.py` is a HIGH FAN-IN file: eleven wrappers import it. **A stale shared core reading
MATCH across every wrapper is a measured incident in this estate — check the core, not the wrappers.**
</cross_domain_coordination>

**DELIVERABLE:** a session log with a populated `## Compiler Tools` section (blank/N-A not accepted),
and a report to `2.0.0_SA_COO` + `1.0.0_SA_CTO` carrying per-criterion evidence.
⛔ **NO DEPLOY AND NO PUBLISH IS AUTHORIZED BY THIS TO.** It authorizes the FIX and its QA exercise.
A serve act needs its own word and its own `change_management` ledger entry (NEVER#2).
