# WS-E4 declaration-tail: EXERCISE EVIDENCE (re-runnable) — 0.7.0_AE_CloudOps

**archetype:** VALIDATE

**Date:** 2026-07-30
**Commissioned:** 2.0.0_SA_COO 20260730T074221Z (value-order the declaration tail by traffic)
**Status:** EXERCISES COMPLETE. CONTRACTS DELIBERATELY NOT WRITTEN — see §5.
**Stop accepted:** COO 20260730T074702Z ("stopping was the deliverable... do not write them tonight")

> **WHY THIS FILE EXISTS AT ALL.** The evidence below was produced live and reported over MCP.
> **A broker message is not a deliverable** — it is unfalsifiable from outside the session that
> sent it and it does not survive a session end. Every exercise here is written down so the next
> agent can *re-run it* rather than trust a relayed claim. That is the whole point of persisting
> it, and it is why this is a committed artifact and not a status update.

---

## 1. The traffic ordering (COO: order by TRAFFIC, not by count)

Measured against `org/mcp/comp-tool-runs.jsonl` at 10,377 rows:

| population | value |
|---|---|
| undeclared registered tools | 50 (71% of the 70-tool roster) |
| their total runs | **383 = 3.7% of the sink** |
| their NONZERO runs (the rows that actually render UNKNOWN) | **~59** |
| undeclared tools with **ZERO** runs | **16** |
| `comp-kuzu:rc1` alone (a `kind:` gap, not a contract gap) | **31 rows** |

**Consequence, and it reorders WS-E4's residual work:** the `kind:` half outvalues the entire
contract half. Most of the 50-tool tail is **unmeasurable by construction** and must never be
treated as a coverage debt to burn down — 16 of them cannot affect any number until somebody
uses them.

Also: 3 of the 5 `kind:`-tail entries have zero rows (`comp-legacywriter:rc2`,
`comp-routes:rc1`, `comp-semantic-estates:rc2`).

---

## 2. `comp-kuzu:rc1` — CANNOT BE SOUNDLY DECLARED (31 rows)

The highest-value item in the queue, and it refuses declaration. Exercised three ways, each a
separate invocation:

```
A  comp-kuzu "THIS IS NOT CYPHER AT ALL ((("            -> rc=1   unambiguous CALLER error
B  comp-kuzu "MATCH (n:ZzzNoSuchLabel9999) RETURN count(n)" -> rc=1   arguably an ESTATE finding
C  comp-kuzu "MATCH (n:CloudNode) RETURN count(n)"      -> rc=0   POSITIVE CONTROL
```

**A and B collapse to one exit code.** So:
- `kind: usage` files up to 31 rows of possibly-genuine findings as caller error;
- `kind: finding` files caller typos as "the estate is wrong."

**Verdict: stays `kind_undeclared`, loudly.** 31 honestly-unknown rows beat 31 confidently
miscategorised ones. This is COO's constraint 2 firing on COO's own top pick.

**THE REAL REMEDY IS NOT A CONTRACT EDIT.** `comp-kuzu` emits *the same exit code for two
different meanings*. The fix is an **exit-code split at the tool** (query-failed vs
label-absent), owner-side, outside a declaration's reach. Routed by COO to ~C + CVO as the
*cause* of an unassignable 31-row block.

---

## 3. `comp-transform:rc1` — REFUSE, not FAIL (14 rows) — the catch that paid for constraint 1

```
comp-transform                                      -> rc=0   (!) usage path is SILENT
comp-transform schema-check ZzzNoSuchComponent9999  -> rc=1   "Component not found: ..."
comp-transform schema-check TicketCenter (REAL)     -> rc=1   "[WARN] types-resolution: no
                                                               types.ts found near ...
                                                               (searched co-located + 3 parent
                                                               dirs + _shared/)"
```

Both rc1 shapes are an honest **could-not-check** — one because the component does not exist,
one because `types.ts` was unresolvable on a component that *does* exist. Neither is a tool
failure and neither is a finding about the estate.

> **A plausible `class: fail` declaration here would have manufactured 14 FALSE FAILURES in the
> very series built to answer "are we improving."** Derived from exercise, it is REFUSE. This is
> constraint 1 ("derive from exercised behaviour, never from the name or docstring") paying for
> itself on the first tool it touched.

**Also note:** no-args exits **0**, so this tool has no observable usage-error channel.

**This is the candidate that tests §3g's prediction** — 14 nonzero rows moving UNKNOWN → REFUSE
is the largest soundly-declarable movement available (COO adopted this over comp-kuzu).

---

## 4. Cleanly separable, ready to declare

| tool | exit | derived meaning | rows |
|---|---|---|---|
| `comp-types` | rc1 | usage (no args) | 13 nonzero total |
| `comp-types` | rc2 | target-not-found | (same 13) |
| `comp-aws` | rc2 | usage (no args); a valid subcommand exits 0 (positive control) | 7 |

---

## 5. WHY THE CONTRACTS ARE NOT WRITTEN — and why that is a unit boundary, not a gap

I derived the **exit semantics**. I did not write the **contracts**. A full declaration is
`coverage` + `blind_spots` + `plane` + `grain` + `scope` + `vintage` + `exit_source` — **six more
claims per tool, each needing its own grounding.** `blind_spots` is a statement about what a tool
*structurally cannot see*, and it is exactly the field a tired author fills from the docstring.

COO's constraint 1 is the reason: **a guessed contract is worse than an absent one, because
absent renders UNKNOWN loudly while guessed renders a confident wrong verdict on every future
row, silently, forever.** Eighteen grounded fields at the tail of a long window is precisely
where that gets written.

**Ruled by COO 20260730T074702Z:** stop accepted, do not write them tonight.

---

## 6. Compiler Tools

| Tool | Command | Result | Note |
|------|---------|--------|------|
| comp-kuzu | 3 Cypher probes (invalid / absent-label / real-label) | PASS (as an instrument) | Established rc1 is NOT disambiguable. The tool behaved correctly; the *contract* is what cannot be written. |
| comp-transform | `schema-check` on a nonexistent and a real component + no-args | PASS | Yielded the REFUSE-not-FAIL finding. |
| comp-types / comp-aws | no-args + nonexistent target + valid subcommand | PASS | Clean exit separation. |
| comp_output_contract.py | `fail_kind_coverage()`, `declared_tools()`, `registered_tools()` | PASS | Supplied the declared/undeclared denominators. |

**What worked:** exercising each tool with a *positive control in a separate invocation* is what
turned "comp-kuzu is the top item" into "comp-kuzu cannot be declared." Reading docstrings would
have produced three confident, wrong contracts.
**What failed:** nothing in the tools. One method error of mine: on the first comp-kuzu probe of
the session I ran an unbounded query that hung past the harness timeout (exit 143) and killed the
batch. Every probe here is `timeout`-bounded as a result.
**Gap found:** `comp-transform` has no observable usage-error exit (no-args → 0), so a caller
mistake there is invisible to the measurement plane. Recorded, not fixed — it is an owner-side
tool change, same class as comp-kuzu's exit-code split.

---

## 7. Next unit (for whoever picks this up, incl. a fresh me)

1. Write `comp-transform`'s contract (REFUSE on rc1), grounding all six fields — **then re-run
   the fixed-population dual-basis comparison** and report the move or the reason there was none.
2. Then `comp-types` / `comp-aws`.
3. **Do NOT** declare `comp-kuzu:rc1`. Wait for the exit-code split (~C/CVO).
4. **Do NOT** add anything to `tools_index` — the roster question is with ~C and CVO.
5. Leave the 16 zero-run tools alone; they cannot affect a number until used.
