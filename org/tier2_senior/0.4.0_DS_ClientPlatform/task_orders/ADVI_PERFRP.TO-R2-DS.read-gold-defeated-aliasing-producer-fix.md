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
