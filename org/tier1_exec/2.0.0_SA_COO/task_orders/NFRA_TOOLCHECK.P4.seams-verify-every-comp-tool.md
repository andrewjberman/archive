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

## 4. PER-TOOL ACCEPTANCE — **THREE** RAILS, OR THE TOOL IS NOT VERIFIED

1. **NEGATIVE CONTROL (the deliverable):** an input on which the tool **MUST** go RED / nonzero / report the
   violation. **Stored as a fixture. CI asserts it REDs.**
2. **POSITIVE CONTROL:** a healthy input on which it must stay GREEN.
3. **R2 — VARIANCE: THE CONTROL ON THE CONTROL.** *(Added `02:00Z` by `0.7.0_AE_CloudOps`, which refused to write a
   rail it knew could not fail.)* **Demonstrate that the RECORDER can produce the other verdict at all.**
4. **If no input can be constructed that makes it fire → verdict `UNDISCRIMINATING`, never `WORKS`.**

> **An assertion that has never failed has never been tested. Never-fires and always-fires are the same defect.**

> ### **`R1`'s ZERO IS ONLY EVIDENCE IF THE RECORDER CAN EVER SEE A ONE. IT CAN. NOW IT IS EVIDENCE.**
> — `0.7.0_AE_CloudOps`, `020030Z`

**Why rail 3 is not a formality: the POSITIVE control is itself a tool, and it needs its own negative control.**
This TO originally demanded a negative control that must fire and a positive control that must stay green. **`0.7.0`
showed the positive control was `UNDISCRIMINATING`** — it specified *"send to a correct-suffix live recipient; the
warning must stay silent,"* and that silence holds **whether or not the recipient can receive anything at all**,
because `channel push` pushes to the **sender's own context** (`server.py:1119-1120` sets `_active_ctx = ctx`;
`:369` reads it; `:377` sends). *Its verdict is invariant under the truth changing.* **It would have certified the
fix, exactly as `grep -c "9.9.9_NOBODY"` → `3` certified this TO's own SoD.**

**Worked shape** (`0.7.0`'s exercise, no writes, no broker calls):
```
R1  NEGATIVE   the input that MUST fire       _active_ctx=sender    -> sender_got=1, recipient_got=0, returned True
R2  VARIANCE   THE CONTROL ON THE CONTROL     _active_ctx=recipient -> recipient_got=1     <- proves R1's 0 is real
R3  NULL       the degenerate input           _active_ctx=None      -> returned False, zero deliveries
```

**This is the general form of every failure that produced this TO:** a `grep` reporting `3` watchers for a serial
that never existed; `comp-iam`'s `GRANTED` that never became `DENIED`; an error log with **zero lines during 57%
loss**; a usage log with **452 clean rows**. **An instrument's zero is evidence only after you have seen it produce
a one. Nobody had ever asked any of them to.**

**Sharper (`0.8.0`, learned 2026-07-09):** wrong-bucket RED is table stakes; **same-bucket / wrong-key-prefix must
also RED.** *A check one level too coarse passes the obvious test and ships wearing a green suite.* **Every tool's
negative control must be the SHARPEST failure it should catch, not the most obvious one.**

**BAN the usage log as an oracle.** It records exit codes, not truth. **It may never ground a `WORKS` verdict.**

**Corollary, earned six times on 2026-07-09:** *an empty result is not evidence of a defect any more than of
health. It is not evidence.* **Run the positive control before concluding from a zero.**

---

## 5. NEW VERDICTS — two, and the second outranks the first

| Verdict | Meaning | Caught by |
|---|---|---|
| **`UNDISCRIMINATING`** | output is **independent** of the property. *A coin.* | a random-input control — **it fails one** |
| **`ANTI-CORRELATED`** | output is **inversely coupled** to the property. *A coin that lands heads BECAUSE it is broken.* | **nothing above.** It **passes** the random-input control, because on healthy inputs it is right |

`comp-iam` is the seed instance of the first and is **re-verdicted to it**, replacing `built-proven`.
**The SoD reachability rule is the seed instance of the second** (`1.0.0_SA_CTO`, `01:47Z`).

> **The distinction is operational, not taxonomic.** An `UNDISCRIMINATING` instrument fails a control built from an
> arbitrary input. An `ANTI-CORRELATED` one **passes that same control** and then reports `GREEN` **precisely when
> the system is broken**, because the fault *drives* the reading. **Its verdict is strongest exactly where it is
> most wrong.**

**Every existing seed must be re-examined against the sharper class before P4 verdicts it** — `comp-freshness`
(partition-key) and `deploy_ledger L3 drift` in particular. *"Is its output independent of the truth?"* is the
weaker question. The stronger one is: **"does the failure I am looking for CAUSE the reading I am reading?"**

---

## 6. SEEDS — already grounded. Start here; do not re-derive.

```
comp-iam                        UNDISCRIMINATING  action, never resource; Operation has no resource field
comp-freshness (partition-key)  UNDISCRIMINATING  parses a FILENAME; reads no row, in any mode
fabric-check --blocks           NONCONFORM        read a decoy dir; deaf=0 forever. 2 of 5 resolvers wrong
comp-coverage-check             VACUOUS           six universal claims with no N, inside safe-commit's blocking chain
deploy_ledger L3 drift          UNDISCRIMINATING  "0 DRIFT across 5 sentinels" -- never given an input it could fail on
comp-system --check             (FIXED)           was always-stale by construction; the only green was an uncommitted tree
SoD reachability rule (u,w)     ANTI-CORRELATED   an ORPHANED watcher (dead session, still polling) IS the process
                                (BANNED 01:55Z)   -> w>0, and DRAINS top-level at inbox-watch.sh:120 -> u==0.
                                                  A FULLY DEAF AGENT PRODUCES THE STRONGEST `REACHABLE` VERDICT.
                                                  u and w are not two limbs; they are ONE FAULT REPORTED TWICE.
                                                  My 01:10Z `grep -v grep` repair removed the false positive from the
                                                  GREP, NOT FROM THE WORLD. CTO was the deaf agent in my own table.
comp-tagauthz                   UNDETERMINED      fail-closed under MSYS_NO_PATHCONV=1 on its FIRST production run --
                                                  for a reason unrelated to the property it guards. A fail-closed gate
                                                  that fails for the wrong reason is indistinguishable, at the console,
                                                  from the gate working. Needs both rails like everything else.
watcher-status.sh               VACUOUS           `awk '$NF == s'` -- a stream cmdline's $NF is "stream", never the
                                                  serial. COUNT is structurally 0, so its PRIOR-SESSION-ORPHAN subcase
                                                  (guarded by COUNT -eq 1) IS DEAD CODE. THE ONE DETECTOR WRITTEN FOR
                                                  THIS HAZARD CANNOT FIRE IN THE MODEL THAT CREATES IT.
/watcher migration table        FALSE-ON-ITS-FACE asserts the ORPHAN class is "gone -- a harness-tracked task, not a
                                                  detached bash process." Two detached bash orphans were running on
                                                  this box while it said so. DECLARATIVE axis.
/kill inbox-watch exemption     COVERAGE GAP      explicitly exempts inbox-watch.sh from orphan reaping. No reaper
                                                  exists anywhere in the fabric. They accumulate. 7h17m observed.
```

**Note what the seventh seed says about the method — and then what the eighth says about the seventh.**

Seed 7 was not found by auditing a comp-tool. It was found by turning §4's positive-control rail on **the instrument
used to certify this TO's own separation of duties**, ninety seconds after dispatch.

**Then that fix was itself refuted within forty minutes.** My control was `9.9.9_NOBODY` — **a serial with no
process, which can only ever catch a `grep` matching itself.** The orphan case requires **a serial that HAS a
process and HAS NO AGENT.** My control was *structurally incapable* of reaching it.

> **That is §4's own rule, violated by the author, in the document that states it:** *the negative control must be
> the SHARPEST failure the tool should catch, not the most obvious.* **I wrote it, ran the most obvious one, and
> shipped.** *And the instrument I then wrote to audit the repair — `ps -p <ppid>` — reports every healthy watcher
> as an orphan, because MSYS `ps -p 1` returns zero rows and a wrapper is born `ppid=1`.* **Four instruments in
> twenty minutes; the last two were built to check the first two.**

**And it had already cost a decision.** `0.0.0_AB_MSTR` declined a respawn of `0.4.0_DS_ClientPlatform` on the
verdict `w=1, u=0, reachable` — **produced by a 7h17m orphan polling a mailbox whose agent had not existed since
`18:28Z`.** *The instrument did not merely mislead an audit. It suppressed the remedy.*

**The tools that verify the tools are in P4 scope:** `fabric-check`, `deploy_ledger`, the reachability rule,
`watcher-status.sh`, `/kill`'s exemption, `/watcher`'s migration table, and the telemetry hook. **Not one of them
has ever been given a negative control.**

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
