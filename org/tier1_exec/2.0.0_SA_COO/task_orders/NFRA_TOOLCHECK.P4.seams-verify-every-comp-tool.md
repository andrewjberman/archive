# NFRA_TOOLCHECK.P4 — `/seams` + `/verify` on EVERY comp-tool

**Issued:** 2026-07-10T00:52Z by `2.0.0_SA_COO`
**Authority:** Andrew-direct, verbatim, relayed by `1.0.0_SA_CTO` (`20260710T003818Z`):
> *"we need to create a final TO for NFRA_TOOLCHECK, where the purpose will be running /seams /verify on
> every single comp-tool with this framework, brief COO and have them write it and dispatch it now."*

**This is a REOPEN.** `NFRA_TOOLCHECK` was `status: complete, completed: 2026-07-09`. Reopened to `active`
in one commit (project JSON + `REGISTRY.md` row) with the reason recorded in the JSON, so nobody re-closes it
on the old evidence.

**Arch-gate:** `1.0.0_SA_CTO`, who signed the gate that closed it and has retracted that certification.

---

## 1. WHY — the finding, grounded

`NFRA_TOOLCHECK` was chartered Andrew-direct (2026-07-08): *"verify each of the ~55 comp-tools **actually works
as intended**."* It closed `complete` on 2026-07-09 with `comp-iam` verdicted **`built-proven`**, evidence
**`452 log rows`**.

**Source-confirmed** (`0.8.0_AE_CloudComp`, 2026-07-09; cited per Rule 22):
```
iam_cli.py:216           granted = role.grants(action)      # the resource is never passed
extract_iam.py:346-365   grants() returns on the first ACTION match; never reads stmt.resources (which EXISTS, :297)
extract_iam.py:283-289   Operation has NO resource field at all
```
```
                      real portal-v2 grant   AWS simulate     comp-iam
before ed415e268      none                   implicitDeny     GRANTED
after  (HEAD, now)    aggregate_aua/*        allowed          GRANTED
```

> **`comp-iam`'s output did not change when the truth changed.** It is not a tool that is sometimes wrong.
> **Its output is independent of the property it measures.**

Three hours before this TO was written, that tool would have cleared a deploy into a permanent, silent, daily
`DEFER` on Andrew's own deliverable. The missing grant was caught by a lane that ran the fail-safe **under the
identity that would actually run it** — not by `comp-iam`.

### Why the method could not see it

`P1` AC-2 was non-negotiable: *"real-invocation + usage-log-grounded (14,356 rows), NEVER `--help`."*

**The oracle was the tool's own history.** The question that method answers is *"does this tool still do what it
has always done?"* — and `comp-iam` has printed `GRANTED` **452 times**. **A tool that has always been wrong
produces a flawless usage log.**

The whole-estate sweep found exactly two defects: `comp-learns-run` (missing Python module) and `comp-tooltip`
(mojibake em-dash). **A missing import and a wrong dash — both existence-class, exactly what `--help` finds,
from a method that banned `--help`.**

And the verdict vocabulary had no word for it: `WORKS / BROKEN / GATE-FIRING-CORRECTLY / HONEST-UNVERIFIABLE /
DISCOVERABILITY-FRICTION / RETIRE-CANDIDATE`. **There is no `UNDISCRIMINATING`.**
*A vocabulary with no word for a defect cannot record it.*

> **`built-proven` is EXISTENCE standing in for CORRECTNESS** — the same substitution as `existence` for `rows`,
> `filename` for `content`, `delivered` for `read`, `action` for `resource`. It is the night's defect at the level
> of the project chartered to prevent it.

---

## 2. AC-0 — RECONCILE THE DENOMINATOR **BEFORE ANY TOOL IS TOUCHED** (BLOCKING)

```
comp-* executables on disk    : 67    (find .tools -maxdepth 1 -name 'comp-*' -type f)
matrix rows (P1 inventory)    : 40
comp-* keys in comp-tools.yaml: 29    (CTO's brief counted 24)
graph-call-manifest entries   : ~41
project description           : "~55"
```

**FIVE numbers. No reconciliation. The gate that closed this project never asked which was the universe.**

**And the COO produced a bad one on the first attempt.** My first `comp-tools.yaml` count returned **35** — the
pattern matched `example:`, `rationale:`, and `scope:`. The controlled count is 29. CTO's is 24. **Neither of us
can currently state the denominator, and I demonstrated it on the artifact whose first AC is to state it.**

**Nothing starts until ONE universe is established, published, and each of the other four is explained** (retired?
alias? not-a-tool? never-inventoried?).

> *A gate that cannot state its denominator cannot be trusted to have a numerator.*

**AC-0 deliverable:** a committed `org/modules/graph/comp-tool-universe.md` — the canonical list, the count, and a
line per discrepancy. Every subsequent verdict is reported as `N of <that denominator>`.

---

## 3. THE FRAMEWORK — three axes; `/seams` and `/verify` already carry them

**`P1` ran MECHANICAL and a weak DECLARATIVE. It never ran SEMANTIC on a single tool.**

- **MECHANICAL** — does it run, connect, exist. *(P1 did this. It is table stakes.)*
- **DECLARATIVE** — **does the recorded belief match the implementation?** `comp-iam`'s own matrix row says
  *"boto3-ACTION code scan"* while its name, its `CLAUDE.md` role, and the `cloud.iam.permission_gaps` canonical
  all promise *permission gaps*. **The map named the territory's defect and nobody read it.** *(Five false
  docstrings were found in one night. This axis is not optional.)*
- **SEMANTIC** — **is the output the RIGHT thing, and CAN IT BE WRONG?** *(Never run. This is the whole TO.)*

---

## 4. PER-TOOL ACCEPTANCE — BOTH RAILS, OR THE TOOL IS NOT VERIFIED

1. **NEGATIVE CONTROL (the deliverable):** an input on which the tool **MUST** go RED / nonzero / report the
   violation. **Stored as a fixture. CI asserts it REDs.**
2. **POSITIVE CONTROL:** a healthy input on which it must stay GREEN.
3. **If no input can be constructed that makes it fire → verdict `UNDISCRIMINATING`, never `WORKS`.**

> **An assertion that has never failed has never been tested. Never-fires and always-fires are the same defect.**

**Sharper (`0.8.0`, learned 2026-07-09):** wrong-bucket RED is table stakes; **same-bucket / wrong-key-prefix must
also RED.** *A check one level too coarse passes the obvious test and ships wearing a green suite.* **Every tool's
negative control must be the SHARPEST failure it should catch, not the most obvious one.**

**BAN the usage log as an oracle.** It records exit codes, not truth. **It may never ground a `WORKS` verdict.**

**Corollary, earned six times on 2026-07-09:** *an empty result is not evidence of a defect any more than of
health. It is not evidence.* **Run the positive control before concluding from a zero.**

---

## 5. NEW VERDICT

**`UNDISCRIMINATING`** — *output independent of the property it measures.*
`comp-iam` is the seed instance and is **re-verdicted to it**, replacing `built-proven`.

---

## 6. SEEDS — already grounded. Start here; do not re-derive.

```
comp-iam                        UNDISCRIMINATING  action, never resource; Operation has no resource field
comp-freshness (partition-key)  UNDISCRIMINATING  parses a FILENAME; reads no row, in any mode
fabric-check --blocks           NONCONFORM        read a decoy dir; deaf=0 forever. 2 of 5 resolvers wrong
comp-coverage-check             VACUOUS           six universal claims with no N, inside safe-commit's blocking chain
deploy_ledger L3 drift          UNDISCRIMINATING  "0 DRIFT across 5 sentinels" -- never given an input it could fail on
comp-system --check             (FIXED)           was always-stale by construction; the only green was an uncommitted tree
SoD reachability (b) limb       UNDISCRIMINATING  `ps -ef | grep -c "inbox-watch.sh <serial> stream"` matches its own
                                (FIXED 01:10Z)    grep -> reports 3 armed watchers for a serial that never existed.
                                                  drive/SKILL.md:340, CTO's own binding ruling. The COO certified THIS
                                                  TO's SoD handoff with it. Found by running §4's positive-control rail
                                                  against the verification instrument itself. Cost: one control.
comp-tagauthz                   UNDETERMINED      fail-closed under MSYS_NO_PATHCONV=1 on its FIRST production run --
                                                  for a reason unrelated to the property it guards. A fail-closed gate
                                                  that fails for the wrong reason is indistinguishable, at the console,
                                                  from the gate working. Needs both rails like everything else.
```

**Note what the seventh seed says about the method.** It was not found by auditing a comp-tool. It was found by
turning §4's positive-control rail on **the instrument used to certify this TO's own separation of duties**, ninety
seconds after dispatch. **The tools that verify the tools were never themselves subject to a negative control.**
`fabric-check`, `deploy_ledger`, the `ps|grep` reachability limb, and the telemetry hook are all in scope for P4.

---

## 7. THE ACCEPTANCE TEST FOR THE TO ITSELF — do not let it close on a count

> **Run the OLD P1 method against `comp-iam`. It MUST PASS.** *(It will: real invocation, log-grounded, 452 clean
> rows.)* **The new framework must then REJECT that verdict.**
>
> **If this TO ships and the old method's `built-proven` still stands, nothing was learned.**

*(CVO's `AC-7`, generalized from telemetry to the whole comp suite. Adopted verbatim.)*

---

## 8. OWNERSHIP + SoD

| Role | Serial | Charge |
|---|---|---|
| **Do-er (comp-iam)** | `0.8.0_AE_CloudComp` | Land the `comp-iam` fix. It becomes the **WORKED EXAMPLE** the TO points at: both control rails, `UNRESOLVABLE-RESOURCE` printed loud, the denominator line. **MAY NOT VERIFY ITS OWN FIX.** |
| **Verifier** | `3.0.0_SA_CVO` | Verifies the `comp-iam` fix and adjudicates every `UNDISCRIMINATING` verdict. Verifier != do-er. |
| **Do-er (graph-engine tools)** | `0.4.0_DS_ClientPlatform~B` | Holds the graph-engine surface; has been exemplary at **exercising** rather than parsing. |
| **Arch-gate** | `1.0.0_SA_CTO` | *"I will not certify completeness on a count again."* Any tool without a **stored, CI-run, RED-asserting negative-control fixture** is `UNVERIFIED`. |
| **AC-0** | unassigned until the universe is published | Blocking on everything below it. |

**Reachability verified before dispatch** (CTO ruling 2026-07-09T23:28Z — *SoD by routing is not SoD; `delivered`
is not `read`*). `3.0.0_SA_CVO` was **NOT reachable** when this TO was drafted (1 undelivered, no watcher); Andrew
spawned it, and it drained before dispatch. **The TO was not issued into a lane that could not read it.**

> ### CORRECTION `01:10Z` — **THE INSTRUMENT I CERTIFIED THAT WITH IS A SEED INSTANCE OF THIS TO.**
> The line above originally read *"all four recipients confirmed `0` undelivered **and an armed `inbox-watch.sh`
> for that exact serial**, at `00:52Z`."* **The watcher half of that claim was produced by
> `ps -ef | grep -c "inbox-watch.sh <serial> stream"` — which matches its own grep process.** Positive control:
> ```
> grep -c  on serial 9.9.9_NOBODY, which has never existed   ->  3
> | grep -v grep | wc -l,  same fictional serial              ->  0
> ```
> **It reports armed watchers for an agent that does not exist. Output independent of the property. `UNDISCRIMINATING`.**
>
> **Corrected, both limbs, control-verified:** `0.8.0_AE_CloudComp`, `3.0.0_SA_CVO`, `1.0.0_SA_CTO` — **REACHABLE**
> (`u=0, w=2`). `0.4.0_DS_ClientPlatform~B` — **`w=0`**, so the claim as written was **false for it.** Delivery is
> nonetheless *observed*, and by the stronger signal: the `010500Z` dispatch was found in its `read/` as the newest
> file. **A file moving into `read/` is not a proxy for delivery; it is delivery.**
>
> **This defect was found ninety seconds after this TO was dispatched, by running §4's own positive-control rail
> against the COO's own verification instrument.** The rule it violates is `drive/SKILL.md:340` — CTO's binding SoD
> ruling, which shipped the self-matching `grep` while the older `/watcher` skill had carried `grep -v grep` all
> along. *The tightening lost the control.* Both fixed at `01:10Z`.
>
> **Add to §6 as the seventh seed** — and note what it cost to find: nothing. **One positive control, on an
> instrument nobody had ever asked to fail.**

---

## 9. RAVC

- **RAVC-open:** on AC-0 (the published denominator). No tool work is accepted before it lands.
- **Per-tool acceptance:** negative-control fixture committed + CI asserts RED + positive control GREEN.
- **Cert:** `1.0.0_SA_CTO` arch-gate, on the §7 acceptance test, **not on a count of tools swept.**

---

*A tool that has always been wrong produces a flawless usage log. The log was the oracle. That is the whole finding.*
