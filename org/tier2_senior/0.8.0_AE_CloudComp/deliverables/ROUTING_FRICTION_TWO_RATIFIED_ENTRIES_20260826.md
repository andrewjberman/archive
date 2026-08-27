# The two CTO-ratified routing-friction entries: one is already closed, the other cannot be closed by a rule edit

**Seat:** `0.8.0_AE_CloudComp~F`  **When:** 2026-08-26 ~15:0x-15:2xZ
**Dispatch:** `2.0.0_SA_COO` 72225 (/drive tick 2) -- the two entries in
`org/modules/graph/comp-learns-backlog.md` marked *BUILD RATIFIED, APPROVED-PENDING-BUILDER*
(CTO msg 20260714T032105Z), open 43 days awaiting 0.8.0-class capacity.
**I flipped NO resolution line.** The backlog's own header reserves closure for a human act with a
citation, and I did not build either tool.

---

## ENTRY 2 -- `routing: marker firm constant` (value 128.0) -- ALREADY CLOSED, NOT BY ME

The entry's premise is that the router "repeatedly hedged this intent." **It does not hedge today.**
Exercised at this seat on the entry's own verbatim demand term:

```
comp-which "Marker/firm constant drift (FIRM_ID, thresholds) vs the canonical config"
  -> 1. score 2.00  comp-constants check [--lane bd|inf|cot|multifirm]
       "marker/firm-CONSTANT drift vs canonical config (rep_id sweeps, FIRM_ID, AUA bounds...)"
```
Score 2.00, **no "NO CURATED RULE MATCHED" banner** -- a curated rule fired and the route is
confident. The tool description is a near-verbatim restatement of the demand term.

**DISPOSITION -- RECOMMENDED, NOT TAKEN:** close as resolved by `comp-constants`, which existed
before this dispatch. ⛔ **It must NOT be flipped to `BUILT` under my name.** I did not build
`comp-constants`; recording this as my build would be a false attribution of a good act, which is the
kind that survives because nobody contests credit.

>> **THE STRUCTURAL POINT: THE BACKLOG HAS NO RE-TEST STEP.** This entry was filed 2026-07-14 against
>> a live measurement and was overtaken by a tool built in the interim. **Nothing re-tested it, so it
>> sat 43 days advertising a gap that had closed.** An entry records a measurement at a vintage; the
>> estate moves; the entry does not. <<

---

## ENTRY 1 -- `routing: pre ship field` (value 130.0) -- THE RULE ALREADY EXISTS AND IT IS DEAD

The entry's disposition reads: *"a curated comp-which rule / keyword refinement ... would sharpen it
to a confident decision."* **That refinement was already made. It cannot fire.**

### The rule exists and scores far above the routing threshold

`.tools/comp-which:1130-1135` carries a curated rule for exactly this intent, added by
NFRA_INSTDRILL item 3 to end this very hedge. Scored directly against the entry's verbatim demand
term by executing `_score_rule`:

| query | score | `_STRONG_MAIN` | would route? |
|---|---|---|---|
| `Pre-ship field-threading audit of a portal adapter function` | **15** | 4 | **YES** |
| `field-threading audit` | 6 | 4 | YES |

**And the live tool prints `!! NO CURATED RULE MATCHED THIS QUESTION` on both.**

### Why: the rule points at a tool that does not exist

| artifact | state |
|---|---|
| curated routing rule (`comp-which:1130`) | **EXISTS**, scores 15 |
| pre-push gate (`.tools/portal-hooks/d1_adapter_threading_gate.py`) | **EXISTS**, fully specified |
| test (`org/modules/graph/tests/test_adapter_audit.py`) | **EXISTS**, 19,400 bytes |
| test (`.tools/portal-hooks/d1_gate_test.py`) | **EXISTS** |
| **engine (`org/modules/graph/adapter_audit_cli.py`)** | ⛔ **ABSENT** |
| **shim (`.tools/comp-adapter-audit`)** | ⛔ **ABSENT** |

**POSITIVE CONTROL on the absence verdict:** 29 sibling `*_cli.py` engines resolve at that exact path
(`atomcheck_cli.py`, `cache_cli.py`, `comp_constants_cli.py`, ...). The path pattern is right; this
one member is missing.
**SECOND CONTROL:** `python org/modules/graph/tests/test_adapter_audit.py` terminates
`FileNotFoundError: ...adapter_audit_cli.py`. **A test for a tool that was never built.**

The suppression mechanism is already named in `comp-which`'s own comments: a RULES entry whose target
is not routable **"scores it but never surfaces -- same silent-drop class as the comp-system bug."**
The escape hatch for that case, `_CURATED_POINTER_ONLY`, is now an **empty set** (it held
`comp-surface-check` until that tool was retired 2026-08-06).

>> ⛔ **THE CAPABILITY WAS DESIGNED, ROUTED, GATED AND TESTED. ONLY THE ENGINE WAS NEVER BUILT.**
>> Four artifacts point at a fifth that does not exist, and each of the four is individually
>> well-formed. **The routing friction is not a routing defect -- it is a MISSING TOOL wearing a
>> routing defect's symptoms**, which is why 43 days of "add a curated rule" never closed it. <<

⚠ **THE GATE IS NOT WIRED.** `d1_adapter_threading_gate.py`'s docstring says *"Fires at portal
pre-push,"* but a sweep for its name across `*.sh`/`*.py`/`*.yaml` finds only its own two tests --
**no hook invokes it.** So it is not a live pre-push hazard today; it is a staged gate whose
dependency is absent. **Stated because "fires at portal pre-push" in a docstring, read alone, would
have me report a live blocking gate that does not exist** -- a description is not a state.

### DISPOSITION -- NOT MINE TO TAKE

**The entry cannot be closed as a routing refinement, and I am not self-authorizing a tool build.**
Building `adapter_audit_cli.py` is a project, not a keyword edit: the gate's own docstring specifies
S3 platinum-envelope fetch, field-by-field threading comparison, and a four-value finding taxonomy
(`SCHEMA-DRIFT` / `NESTED-SCHEMA-DRIFT` / `TYPE-ONLY` / `NOT-THREADED` / `FALLBACK-ORDER`). That is
rung 7 of the build ladder and needs an issuer.

**Three routes, for `2.0.0_SA_COO` / `1.0.0_SA_CTO` to choose between:**
1. **BUILD the engine** to the existing gate + test spec -- the tests and gate already define it, so
   the spec cost is already paid. Needs a TO.
2. **RE-POINT the rule** at an existing tool. ⚠ The rule's own text declares `comp-adapter-audit`
   **DISTINCT from `comp-transform`** (adapter/raw-input side vs component/render side), so this
   knowingly routes the intent to a tool that answers a neighbouring question.
3. **RETIRE the rule + gate + tests** and DECLINE the entry, recording that the capability was
   specified and not built.

⛔ **AND A SEPARATE FINDING, ROUTED NOT CHASED:** a curated rule pointing at a non-existent tool
**scores, is silently dropped, and produces the "no curated rule matched" banner** -- which reads to
every agent as *"the catalog does not cover this,"* when the truth is *"the catalog covers it and the
target is missing."* **Those two states are indistinguishable at the call site.**

**SWEPT, because the question was one probe and it decides whether this is a one-off or a class:**
every RULES entry whose first call names a `comp-*` target, checked against `.tools/`:

```
RULES entries with a comp-* target (DENOMINATOR) : 91
  target shim PRESENT in .tools/                 : 90
  target shim ABSENT                             :  1   <- comp-adapter-audit, and only it
```

**It is a ONE-OFF, not a class.** The curated routing surface is otherwise intact at 90 of 91, which
is worth stating positively: this finding does not impugn the rule table. ⚠ The sweep tests SHIM
PRESENCE only -- it would not catch a rule whose target exists but is non-routable for another
reason, so it is a floor, not a proof of full routability.
