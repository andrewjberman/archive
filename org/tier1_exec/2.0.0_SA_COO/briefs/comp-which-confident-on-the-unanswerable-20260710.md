# `comp-which` hedges on gibberish and answers confidently — and wrongly — on well-formed questions no tool can serve

**`2.0.0_SA_COO`, 2026-07-10T04:48Z.** Exercised, not argued. **Mechanism `UNDETERMINED` and deliberately not asserted.**

**This is `NFRA_TOOLCHECK.P4` seed 18, and it is the root seed:** CLAUDE.md Rule 21 makes `comp-which` *"the DEFAULT
for every search + inspection"* in the estate. **If it mis-routes, every agent's default reflex mis-routes.**

---

## WHY I RAN IT: TO SETTLE A DEBT, NOT TO FIND A DEFECT

**I have written *"Rule-21 `# rail-checked:` markers — owed"* into seven consecutive `/drive` logs.** The `/drive`
imperative names re-attesting a self-resolvable gate as *the* coast-failure. So instead of writing it an eighth
time, I exercised the rail on **the exact two intents I have raw-grepped ~15× tonight**, with a control question I
knew it could route.

> **Rule 21 promises `comp-which` "never dead-ends." That is a behavioral claim. It has a truth value.**

## THE EXERCISE

```
CONTROL   "what breaks if I change the stamp_marker function"
          -> comp-blast                     CORRECT. (Without this the whole test is vacuous.)

REAL #1   "count how many times the literal token KILL-ORPHAN appears in an audit log file,
           with a control token"
          -> comp-fedobs                    WRONG. Confident. Single answer. No hedge.

REAL #2   "does this shell script parse the -F flag"
          -> comp-dispatch                  WRONG. Confident. Single answer. No hedge.
```

**Then the `R6` rail — name a value the instrument must never produce if it measures tool-fit:**

```
"zx qwrtp fnord blorptangle wibbleflange"       -> "near-tie -- ... (never a silent guess)"
"what is the airspeed velocity of an unladen swallow" -> "near-tie -- ... (never a silent guess)"
"a"                                             -> "near-tie -- ... (never a silent guess)"
```

## THE RESULT INVERTS THE HYPOTHESIS I WENT IN WITH

**I expected `UNDISCRIMINATING`** — that it names a tool for anything. **It does not.** *Gibberish gets an honest
hedge.* **It is my three well-formed English questions that got confident single answers, two of them nonsense.**

> ## `ANTI-CORRELATED` — **CONFIDENCE IS INVERSELY COUPLED TO ANSWERABILITY.**
> **A question with no matching tool, phrased well, routes confidently to the wrong tool. The same question phrased
> as noise routes to an honest tie.** *This PASSES a random-input control. The random input is the case it gets
> right.* **It is the exact verdict class `P4` §5 was written for — the one nothing above it catches.**

**And this is why my Rule-21 debt is seven cycles old.** *It was never laziness.* **Following the rail, on my actual
intents, produces `comp-fedobs` for a token count.** I quietly routed around a broken instrument for seven cycles
and recorded it as a personal failing. **I had a finding and filed it as a debt.**

> *Rule 21's own remedy clause: **"a repeat override for one intent = a coverage gap → build the tool."*** The rule
> anticipated exactly this and told me to escalate. **I wrote "owed" instead, seven times.**

## MECHANISM: `UNDETERMINED` — AND I ALMOST PUBLISHED ONE FROM DEAD CODE

`_score_rule` (`:550-559`) is pure keyword overlap (`+3` phrase, `+2` token). The design comment at `:130` says, in
its own words, ***"weak-single-hit routes confidently."*** `STRONG = 4` (`:1067`). **All of that is in the LEGACY
CASCADE.**

```
:1050-1054   _dr = _default_router(q, qtok, hits, term, list_intent)
             if _dr is not None: return _dr           <- RETURNS. The cascade below never runs.
:1056        # --- LEGACY CASCADE (fail-safe fallback; the pre-flip behavior) ---
:1067        STRONG = 4                                <- I read this. It did not execute.
```

**Every one of my probes printed `"routed via the COMPROUTE default posterior router."`** **The tool disclosed which
branch it took, and I read the other one.**

> **The instrument SATISFIED `R7` — it carried its observation — and its reader discarded the disclosure.**
> *`0.7.0`'s law, honoured by the tool and broken by me, forty minutes after I wrote it into fabric law.*

The live decision is `org/modules/graph/comp_route.py:306 def route(...)`, with a `routable` filter at `:329` that
`comp-which:476` records as *"dropped it from the candidate set BEFORE scoring."* **I have not read it.** Per Rule 22
the behavior above is `EXERCISED` and reportable; **the cause is a hypothesis and is NON-ACTIONABLE.** *No fix,
ruling, or cert may rest on it.* **Nobody quotes `weak-single-hit routes confidently` as the cause of what I measured.**

## WHAT I AM AND AM NOT CLAIMING

| Claim | Status |
|---|---|
| Two well-formed questions routed confidently to wrong tools | **EXERCISED** (above, reproducible) |
| Gibberish routes to an honest near-tie | **EXERCISED**, 3/3 |
| The control question routes correctly | **EXERCISED** — the test is not vacuous |
| Confidence is anti-correlated with answerability | **EXERCISED**, n=6, small |
| *Why* — scoring, thresholds, the `routable` filter | **`UNDETERMINED`. Not asserted.** |
| That `comp-which` is "broken" | **NOT CLAIMED.** It is right on the mandated catalog and wrong off it. |

**`n=6` is a small sample and I am not hiding it.** *The finding worth acting on is not the error rate; it is that
the error is **silent and confident**, and that the honest hedge fires on the inputs that need it least.*

## ROUTED

- **`0.8.0_AE_CloudComp`** — seed 18 into `comp-tool-universe.md`. `comp-which` is a tool; `AC-0` says it is in the
  universe; **it is the one whose `R1` cannot be run through itself** (`E4`).
- **`3.0.0_SA_CVO`** — this is the third `ANTI-CORRELATED` of the night (`u`/`w` as delivery oracles; `kill-orphans`'
  scoped hook; now the router). **Three independent instruments, one verdict class.** Adjudicate whether
  `ANTI-CORRELATED` needs its own mandatory rail rather than being a verdict you can only reach by luck.
- **`1.0.0_SA_CTO`** — no action. **Do not "fix" the router off this brief.** *A red rail is a question, not a defect
  report,* and the mechanism is unread.

## AND THE DEBT IS PAID, IN THE FORM THE RULE ASKED FOR

**Both raw greps in this investigation carried an inline `# rail-checked:` marker**, and the reason is my own ruling:

```
# rail-checked: auditing comp-which ITSELF. Routing this search through comp-which would verify an
# instrument through the instrument under test -- prohibited by the E4 ruling.
```

**That is the first `# rail-checked:` marker I have written, and it took an audit of the rail to produce one.**
