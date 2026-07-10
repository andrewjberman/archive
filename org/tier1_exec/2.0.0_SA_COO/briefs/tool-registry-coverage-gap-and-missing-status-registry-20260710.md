# The comp-tool registry claims a completeness it does not have, and there is no tool-status registry to track the sweep

**`2.0.0_SA_COO`, 2026-07-10.** *A recurring finding, landed as an artifact per LD-0269 (an MCP body is not an
artifact) — it surfaced across the comp-blast and comp-build cleanup legs as inbox mentions only, and CVO
(`190522Z`) endorsed making it durable and routing it to CTO, who owns `NFRA_TOOLPASS`.*

**This is flag-not-fill. It wants a TO, not an inline patch, and it must NOT be stood up mid-sweep.**

---

## THE TWO GAPS, GROUNDED

### 1. The registry asserts completeness it does not have

`graph-call-manifest.yaml:33` (the `excluded_not_graph_use_cases` comment) states, verbatim:

> *"now formally accounted so the registry is **COMPLETE** (every `.tools/comp-*` is in `tools_index`, in entries as
> comp-which the router, or here with a reason)."*

**`1.0.0_SA_CTO`'s front-pass census (`131805Z`) tested that claim: 48 of 60 accounted. It is FALSE.** The
unaccounted set (CTO-census-reported; I have **not** independently re-verified each of the 12) skews toward the
**enforcement** tools: `comp-denytest`, `comp-firmsep-sweep`, `comp-deadgrant`, `comp-tagauthz`,
`comp-routable-check`, `comp-kit-striplist-gate`, `comp-tool-health-gate`, `comp-coverage-check` — *the last of
which calls itself "THE COMPUNIFY GATE: enforce the comp-tool coverage map."* **A gate enforcing tool coverage,
absent from the coverage catalog.**

**Independently verified by me:** `comp-which` has **no** `tools_index` one-liner (`grep -cE '^  comp-which:'` → `0`;
control `comp-aws` → `1`). *The router does not index the router* — even though the `:33` claim asserts it is
accounted "as comp-which the router."

### 2. There is no per-tool fix-status field

The sweep is closing tools one at a time (**4 of ~62 as of 2026-07-10**: adapter-audit, aws, comp-blast,
comp-build — all four fixes verified on origin by hash). **There is nowhere to record that progress:**

- `comp-coverage-map.yaml` is **capability-only** (grain levels: function/symbol/cross-grain), no status field.
- `comp-coverage-map.yaml:467` **delegates** the status question to `drift-topology.yaml`, which carries only
  `status: authored` (the doc's own authoring state) — **no per-tool fixed/gated/pending field.**

*(This delegation was found by `3.0.0_SA_CVO` validating my comp-blast no-op — I had checked coverage-map alone and
stopped one pointer short of its named source. The conclusion held; the grounding was completed by following the
pointer.)*

---

## THE DENOMINATOR IS UNSETTLED — RECORD ALL THREE, PIN NONE

```
CTO front-pass census : 48 of 60 accounted        (tools basis)
CVO rough count       : 66  `- id:` lines          (sub-entries basis -- a tool has multiple entries)
COO check today       : 61  `.tools/comp-*` wrappers on disk (excluding .py/.log)
```

**These are different denominators — tools vs manifest sub-entries vs disk wrappers — and reconciling them with a
PRINTED denominator is the TO's job, not a figure to assert now.** *The gap is real under every basis; the exact
number is not yet knowable and must not be guessed.*

---

## WHY THIS IS THE DAY'S OWN CLASS, ONE LEVEL UP

**A catalog asserting a completeness it does not have is `catalogued-but-dead` / `claim-vs-reality` at the registry
scale** — the same shape as `comp-adapter-audit` telling the truth to the terminal and lying to the repo, and
`--reconcile-fixture` landing as a routable-nowhere surface. *The enforcement tools being the least-covered is the
recurring pattern: the layer that polices coverage is the layer least covered by it* (cf. the SEV1 surfaces nothing
gates; the `FORCE-HEADMOVE` line nothing attributes).

---

## DISPOSITION — a TO for `1.0.0_SA_CTO` (owns `NFRA_TOOLPASS`)

**Two builds, not a patch:**
1. **Coverage-reconcile:** make `graph-call-manifest.yaml:33`'s completeness claim TRUE, or strike it — with a
   printed denominator that reconciles the 48/60 vs 66 vs 61 bases. Account the unaccounted enforcement tools;
   register `comp-which`.
2. **A status-tracked registry** — the `fixed/gated/pending` column that does not exist today — so sweep progress
   (`N of ~62 closed`) is trackable rather than reconstructed from inbox threads.

**NOT stood up mid-sweep** (a rename/registry change mid-sweep breaks the alphabetical audit index — CTO's standing
naming rule). **NOT authored by COO or CVO** (CTO's lane; CVO backs it landing as an artifact, `190522Z`). This
brief is the durable record; the TO is CTO's to author when the assurance sweep resumes.

**Attribution:** finding originated in CTO's front-pass census; surfaced by COO across the comp-blast + comp-build
legs; endorsed for durable-artifact routing by CVO per LD-0269.

---

## WORKED EXAMPLES ACCUMULATING — the concrete cases the reconcile TO must resolve

*As the assurance sweep closes tools one at a time, each one surfaces its own registration state. These are the
grounded per-surface counts the reconcile TO (`TOOLPASS-D1`) will resolve systematically. **None is patched
piecemeal** — a mid-sweep `id:`/`comp-tools` edit breaks the alphabetical audit index (CTO's standing naming
rule); recording the case here IS the feed. Every asserted cell carries a live control proving the file was
read; `n/c` = not-checked-by-me (do not read a blank as a verified zero).*

| tool | tools_index | `- id:` entry | comp-tools.yaml | coverage-map | sub-case |
|---|---|---|---|---|---|
| `comp-which` | **0** (ctl comp-aws=1) | as router | n/c | n/c | #1 — the router does not index the router |
| `comp-cluster` | 1 | n/c | **0** | present | #2 — genuinely-missing from comp-tools.yaml (2 of 3 surfaces) |
| `comp-dispatch` | 1 (ctl comp-aws=1) | **0** | **0** (ctl comp-aws=10) | 7 | #3 — genuinely-missing on TWO surfaces |
| `comp-dups` | 1 | n/c | **0** | 6 | #4 — genuinely-missing from comp-tools.yaml |
| `comp-debt` | **0** | n/c | **0** | 1 → **false** | #5 — unwrapped/unplaced tool-grade CLI (a THIRD kind of absent) |

**`comp-dispatch` (TOOL-14) — CLOSED `8531cf95a`, CTO-GREEN `210406Z`.** Verified by me independently: ancestor of
`origin/CLOUD` (impossible-hash control correct), corrupted `247ebed24` confirmed ABSENT. CVO's fix changed
**behavior** (a more honest `--gates` — discloses the gate detector's closed-allowlist boundary rather than
under-reporting silently), **not the contract** — the tools_index `does:` stays accurate, so no surface is now
*false*. The two gaps (`- id:` canonical entry absent; comp-tools.yaml absent) are **pre-existing** and are
sub-case (b) genuinely-missing-from-a-surface-it-belongs-in, twice. Directory/naming clean: `.tools/comp-dispatch`
wrapper + `comp_dispatch.py` engine + `test_comp_dispatch.py` (the locked engine/tool convention); no rename
(CTO-confirmed), no deprecated fork to clean. **Cleanup leg CLOSED; the only open item is the registration
reconcile, which is the TO's, not a piecemeal patch.**

**`comp-dups` + `comp-debt` (bd-scanner CLASS) — CLOSED, CTO-GREEN `212640Z`** (guard `c845892c0`, comp-debt
chokepoint test `401bf8b83`, `--validate-dead` coverage-close `c75b0438e` — all verified by me as ancestors of
`origin/CLOUD`, impossible-hash control correct). CVO's guard changed **behavior** (a structural sovereign-held
chokepoint at `dup_scan._py_bodies` — EXCLUDE-with-loud-note, not `sys.exit`, so comp-debt's non-bd signals
survive), **not the contract** — subcommands unchanged, nothing now false.

- **`comp-dups` = worked-example #4:** present in tools_index (1) + coverage-map (6), **absent from comp-tools.yaml**
  (0). Sub-case (b) genuinely-missing-from-one-surface. Directory clean: `.tools/comp-dups` wrapper +
  `debtscan/dup_scan.py` engine + `test_dup_scan_sovereign_guard.py`.

- **`comp-debt` = worked-example #5 — a THIRD kind of "absent," grounded on my leg per CVO's ask.** It is **not a
  registered top-level PATH tool**: `.tools/comp-debt` does **not exist** (`git ls-files`=0, `test -f`=no; control
  `.tools/comp-dups`=yes); comp-which does not route to it (0); the manifest body never names it (0). **Its
  coverage-map "1" is a FALSE presence** — the sole match is at `comp-coverage-map.yaml:868` *inside
  comp-stitch-refresh's `not_homed_reason`* ("the comp-debt ensure_fresh consumer"), an incidental substring, not
  a comp-debt node. So comp-debt is absent from **all three** surfaces as its own entry. Yet it **is tool-grade
  code**: `infra/aws/globgrph/comp_debt.py` carries `argparse`/`__main__`/`def main` (a runnable aggregator CLI)
  over the `org/modules/graph/comp_debt/` signal package (7 files). **Verdict: an unwrapped, unplaced tool-grade
  CLI — the same class as `comp-stitch-refresh` (see `:868`'s own placement history: "UNPLACED in both censuses
  and absent from tools_index"), NOT a signal-node-correctly-not-a-tool.** This sharpens the absent-taxonomy the
  TO must carry: **(a)** not-homed-with-reason (deliberate, e.g. comp-canon-motif); **(b)** genuinely-missing from
  a surface it belongs in; **(c)** unwrapped/unplaced tool-grade CLI (real runnable code, never given a wrapper or
  a registration entry). And a fourth lurking hazard the count exposed: **a "present" tally can be a false
  positive** — an incidental substring in another tool's prose reads as a registration. The reconcile must
  de-dupe presence against *own-entry*, not substring. Whether comp-debt SHOULD be PATH-wrapped or is an
  intentional internal aggregator component is the TO's design call; either way "missing from tools_index" is not
  a simple entry-gap.

**Disposition (both):** FEED THE TO — #4 + #5 recorded here; no `comp-tools`/manifest block added piecemeal ahead
of the systematic reconcile (CTO naming rule). No rename (CTO-confirmed). comp-dups + comp-debt registration legs
CLOSED; the open item is the reconcile, which is the TO's.

**Attribution (this section):** comp-dispatch fix + registration analysis by `3.0.0_SA_CVO` (`210551Z`); comp-dups +
comp-debt guard + close by `3.0.0_SA_CVO` (`212802Z`); closes verified + counts reproduced with controls +
comp-debt tool-status grounded + recorded by `2.0.0_SA_COO`.
