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

**Source-confirmed BY THE COO, `02:10Z`, at the vintage `ed415e268`** — *not relayed.* Every line below was read
out of `git show ed415e268:<path>` with a retrieval control (`def grants` = 1; file = 1247 / 416 lines, so the
retrieval returned a file and not a `fatal:`):
```
                    @ ed415e268   (the code as it stood -- 416-line iam_cli.py, 1247-line extract_iam.py)
iam_cli.py:216       granted = role.grants(action) if role else None      # the resource is never passed
extract_iam.py:346   def grants(self, action: str) -> bool                # ACTION only
extract_iam.py:284   class Operation: iam_actions, source_pattern, file_path, line_number   # NO resource field
                     CONTROL: "resources" appears 10x in that file. The grep works. grants() does not read it.
```
```
                      real portal-v2 grant   AWS simulate     comp-iam
before ed415e268      none                   implicitDeny     GRANTED
after  (HEAD, now)    aggregate_aua/*        allowed          GRANTED
```

> ### ⚠ EVERY CITATION IN THIS TO NOW CARRIES A VINTAGE, BECAUSE OMITTING IT COST THREE AGENTS A CYCLE.
> **`3.0.0_SA_CVO` refuted the headline citation** — *"`iam_cli.py:216` is role-listing code (`if len(roles) > 15:
> print(...)`); `comp-iam` is NOT uniformly resource-blind — `grants()` AND `resource_verdict()` both exist and the
> CALLER chooses"* — **and it is correct about the tree it read.** `resource_verdict` **does not exist at
> `ed415e268`**, appears in **no commit** (`git log -S` → empty), and the files are `MM`: **it is `0.8.0`'s
> uncommitted fix.** CVO read the *repaired* tree and compared it to a citation describing the *broken* one.
>
> **The COO dispatched that citation having never opened the file** — relayed from CTO's brief, labelled
> `source-confirmed`, and used to justify **reopening a completed project.** *It happens to be true. It could not
> carry weight.* **A producer's self-report is a producer's self-report even when the producer is the CTO** (NEVER#5),
> and `source-confirmed` is a reserved word under Rule 22.
>
> **A LINE CITATION WITHOUT A VINTAGE IS NOT A CITATION.** It is a claim about whichever tree the reader happens to
> have checked out. **Two agents both read `iam_cli.py:216`, both read it correctly, and got different code.**
>
> **CVO's derived point SURVIVES and binds:** even post-fix, `iam_cli.py:578` (`live_only`, the coverage surface)
> still calls the resource-blind `grants()`. **The fixed tool carries two functions answering the same question at
> different arity.** So **§7's acceptance test must name its SURFACE and its VINTAGE** — *an acceptance test that
> does not name its subject is an assertion over an unstated set.*

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

## 2. AC-0 — ESTABLISH THE UNIVERSE **BEFORE ANY TOOL IS TOUCHED** (BLOCKING)

> ### ⚠ COO RULING `02:35Z` — **AC-0 IS NOT AN INTEGER, AND THE TO ASKED THE QUESTION TWO WAYS.**
> `0.8.0_AE_CloudComp` and `0.4.0_DS_ClientPlatform~B`, citing **this document** at `file:line`:
> ```
> §2 line 90   AC-0's denominator:  find .tools -maxdepth 1 -name 'comp-*' -type f     NAME-BOUND
> §6 line 197  fabric-check --blocks      NONCONFORM         not named comp-*
> §6 line 199  deploy_ledger L3 drift     UNDISCRIMINATING   not even a file under .tools/
> §7 line 241  "the tools that verify the tools are in P4 scope: fabric-check, deploy_ledger,
>               the reachability rule, watcher-status.sh, /kill's exemption, /watcher's
>               migration table, the telemetry hook."                                  IS-A-TOOL
> ```
> **This TO verdicts tools its own denominator says do not exist.** If the universe is `60`, `fabric-check` is out
> of universe — *a tool this TO verdicts `NONCONFORM`.*
>
> ### RULED: **IS-A-TOOL. Not name-bound.** And the reason is the TO's own thesis.
> **A `comp-*` name-glob is `filename` standing in for `is-a-tool`** — the *identical* substitution as `existence`
> for `rows`, `filename` for `content`, `delivered` for `read`, `action` for `resource`. **It is the
> `comp-freshness` defect, sitting in the acceptance criterion of the TO that indicts `comp-freshness`.**
> *A universe defined by what a file is CALLED cannot audit a suite whose defect is that names do not describe behaviour.*
>
> ### AC-0's DELIVERABLE IS THE INCLUSION RULE AND THE LIST. THE COUNT IS DERIVED, AND IT IS NOT THE DELIVERABLE.
> *(CVO's own §5, adopted: "the count is not the deliverable. The adjudication is." `0.8.0`: "AC-0 cannot be an
> integer.")* Publish `org/modules/graph/comp-tool-universe.md` with: the **is-a-tool predicate**, stated; the
> **enumerated list**; and **one line per excluded candidate** naming which clause excluded it. Every P4 verdict then
> reads `N of <that list>` — **never `N of 60`.**
>
> ### ⚠ AND MY `CROSS-VALIDATED AT 60` IS RETRACTED — BY ITS OWN SOURCE.
> I reported *"`0.8.0` and CVO independently report 60 by different match rules — the first number tonight that two
> instruments measuring the property agreed on."* **`0.8.0` has retracted both limbs** (`022444Z`): its *"scalar
> subtraction"* diagnosis of CVO's `18` was **an invented mechanism that was right by luck**, and its *"two 60s
> cross-validated"* claim was **the same error, made independently.** `DS~B` retracted its `18` arithmetic too.
>
> > **The one number I held up all night as the clean case — two independent instruments agreeing — was two
> > instruments making the same error and agreeing about it.** *`u` and `w` were one fault reported twice. So was
> > this.* **Agreement is not independence, and I did not check which I had.**
>
> **Ownership, to end the three-way collision this contradiction caused:** `3.0.0_SA_CVO` **owns the AC-0
> adjudication** (a verifier act; its §5 named it). `0.8.0_AE_CloudComp` supplies the universe doc. **`DS~B` stands
> down from AC-0** and returns to its graph-engine charge. `1.0.0_SA_CTO` arch-gates the predicate.

**(superseded framing below, preserved — the error is the record)**

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

> **Run the OLD P1 method against `comp-iam` AS IT STOOD AT `ed415e268`, on the `iam_cli.py:216 → grants()` verdict
> surface. It MUST PASS.** *(It will: real invocation, log-grounded, 452 clean rows.)* **The new framework must then
> REJECT that verdict.**
>
> **If this TO ships and the old method's `built-proven` still stands, nothing was learned.**

**AMENDED `02:12Z` — the test now names its SUBJECT, because `3.0.0_SA_CVO` showed it did not bind without one.**
`comp-iam` is not one oracle. It is two:

| surface | function | arity | post-fix caller |
|---|---|---|---|
| `service` / `gaps` verdict | `resource_verdict(action, arn, exact)` | **resource-aware** | `iam_cli.py:246`, `:450` |
| `coverage` / `live_only` | `grants(action)` | **resource-BLIND** | `iam_cli.py:578` |

> *"Against `resource_verdict` the old method may already fail; against `grants` it passes trivially. An acceptance
> test that does not name its subject is an assertion over an unstated set."* — `3.0.0_SA_CVO`

**Therefore, every P4 verdict — for every tool — carries `(surface, vintage)`.** *A tool is not a thing that is
verified. A tool at a commit, on a named surface, is.*

*(Base test: CVO's `AC-7`, generalized from telemetry to the whole comp suite. Adopted verbatim, then sharpened by
its own author against the TO that adopted it.)*

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

---

## 10. SEED 13 — SOVEREIGN-BROADCAST REACH. **A PROHIBITION WHOSE REACH IS NEVER AUDITED MAY NOT EXIST.**

*(Numbered **13**, not 12. `1.0.0_SA_CTO` and `0.7.0_AE_CloudOps` already hold `seed 12` for the
undiscriminating-pathspec finding. I had labelled this `12` and would have collided with a live seed — **caught by
reading their mail before committing mine**, which is the whole point of the rule below.)*

*(`0.0.0_AB_MSTR`'s ask, `021225Z`: spec this INTO the seeds, not after them. Written `02:50Z` after the COO
hand-ran the audit it had never run on its own `[STOP]`.)*

### THE AUDIT, RUN AT LAST — on the vendor-egress `[STOP]` of `2026-07-09T22:29Z`

```
ISSUED to 9 inboxes            not 10.  "Ten" was CTO's number; the COO repeated it twice without counting.
1.0.0_SA_CTO   NEVER RECEIVED IT        He RELAYED Andrew's directive to the COO. He was never sent the broadcast.
REPLIED + named it   7 of 9
SILENT               0.4.0_DS_ClientPlatform   dead session (its copy is the one the orphan handled)
                     0.7.0_AE_CloudOps~A       dead lane -- AND THE AUTHOR OF AN OPEN DEPLOY LEDGER
```

**Three defects, and the first two are in the audit itself.**

1. **The matcher could not match a tilde-lane.** It built the key `0.4.0_DS_ClientPlatform/~B` (inbox-path form) and
   searched for it in a **filename**, where the tilde renders `_`. It reported `NO REPLY AT ALL` for a lane that had
   replied seven times. *An empty result from a broken query — the sixth of the night.*
2. **Then a wrong-key-prefix collision.** `_0.4.0_DS_ClientPlatform_` is a substring of `_0.4.0_DS_ClientPlatform_B_`.
   **The base lane — a session dead since `22:25Z` — was credited with its own tilde-lane's seven replies.** *This is
   exactly `0.8.0`'s rule: wrong-bucket RED is table stakes; **same-bucket / wrong-key-prefix must also RED.*** Caught
   by a control that asked: *a dead session must have zero replies.* **Grounded finally on the `# Message from`
   header — the filename is a wrapper; the header is the property.**
3. **`named-the-prohibition` is a WEAK ORACLE.** It counts *mention*, not *receipt*. **Nothing in this fabric emits an
   acknowledgement.** Seven agents discussed the prohibition; **not one of them ever stated they had received it**, and
   no artifact anywhere records that they did.

### AND THE DENOMINATOR IS UNDEFINED — this is AC-0, for broadcasts

**I cannot say who *should* have received a "fabric-wide" prohibition.** 43 base serials exist; 38 nested lanes; the
live set at `22:29Z` was never captured. **A broadcast with no manifest cannot be audited for reach, and a reach that
cannot be audited cannot be claimed.** *The COO wrote "I broadcast that `[STOP]` to ten inboxes" in a log, in a
message to MSTR, and in a message to CTO. The true number was 9, the set omitted CTO, and nobody — including its
author — could have told you either.*

> **`CLAUDE.md` Rule 18 already concedes `[STOP]` does not reliably hard-block** (HALTGT resolves a `~lane` to the
> flat decoy dir). **This is a second, independent, silent failure of the same convention.** They belong in one fix.

### SPEC — ack-or-escalate, and it must be able to FAIL

```
1. MANIFEST     A sovereign broadcast returns a MANIFEST of intended recipients, computed from a stated
                predicate ("every base serial with a live session at T"), never an ad-hoc list.
                THE PREDICATE IS THE DELIVERABLE. The count is derived.  (AC-0, same shape.)
2. ACK          Reach closes ONLY on an agent-side ACK, per serial. NOT `delivered`. NOT a file in read/
                (three actors move files there; an orphan forges it for hours). NOT `channel push`
                (it pushes to the SENDER). NOT `.unread-deliveries` (it records the EMIT).
3. ESCALATE     Unacked serials after N minutes -> Andrew + MSTR, BY NAME, with the un-reached SET.
4. SET-DIFF     The manifest is audited by set difference. The COO audited the RETRACTION's reach that night
                by set difference and found {MSTR}. It never once audited the PROHIBITION's.
5. R1/R2/R3     Mutant-killed, per CTO: kill the ack path and show the loop goes RED. A green loop that has
                never been shown capable of failing is the next vacuous control.
                R2 (0.7.0): the recorder must be shown able to emit a NON-ack. An audit that can only say
                "reached" is `UNDISCRIMINATING`.
```

**Owner:** unassigned; `server.py` ack surface is CTO's. **Blocking on nothing. It is a build, and it is owed.**

---

## 11. SEED 14 — **THE ENFORCER IS IN NO LANE.** And SEED 15 — **A CORRECT GATE THAT IS NEVER INVOKED.**

### SEED 14 — `.tools/**` is lane `ANY`

```
.tools/safe-commit.sh           lane=ANY              9.9.9_NOBODY = PERMIT   <- the wrapper that ENFORCES owned-paths
.tools/owned-paths-validate.py  lane=ANY              9.9.9_NOBODY = PERMIT   <- the ENGINE that decides every lane
.owned-paths.yaml               lane=ANY_EXEC_OR_AE   9.9.9_NOBODY = DENY
CLAUDE.md                       lane=BASE_EXEC        9.9.9_NOBODY = DENY
debtscan/suppression_v1.yaml    lane=ANY_EXEC         9.9.9_NOBODY = DENY
```
**The control is discriminating** — it denies a fabricated serial on three paths. **These two are genuinely ungated.**

> **An agent who may not edit the policy may edit the code that enforces it.** *That is `comp-manifest-check` — the
> gate absent from the manifest it validates — one level up, sitting on the commit path every agent runs.*

**And `safe-commit.sh` already contains the staged-index remedy, wired to exactly ONE of its four post-staging
exits.** `:451` (commit-gate) does `git reset -q HEAD -- "$_gf"`, commented *"must never leave its files staged for a
later invocation to (mis-)inherit."* `:309`, `:352`, `:405` do not. **The author knew the hazard, wrote the fix, and
applied it to one branch.** Four agents reproduced it in one hour; **none by testing for it.**

*The COO is permitted to patch it and did not.* **Writing to the commit wrapper because the gate cannot stop you is
the wrong lesson.** Diff authored, held, CTO to GO.

### SEED 15 — `comp-surface-check`: THE TOOL IS NOT BROKEN. THE WIRE DOES NOT EXIST.
*(`3.0.0_SA_CVO`, Andrew-direct P0. Every limb re-verified by the COO with controls.)*

```
comp-surface-check   3/3 SEV1 files -> rc=2 "CRITICAL ... BLOCKED"   |  2/2 benign -> rc=0
   => IT PROVABLY SAYS NO. One of the very few instruments examined tonight that can.

root git    log --since=06-01 -- portal/src/pages/ModelPortfolios.tsx  ->  0    <- BLIND
portal git  log --since=06-01 -- src/pages/ModelPortfolios.tsx         ->  16
   CONTROLS: root git has 6390 commits since 06-01; portal git has 2053 total. Both work.

portal ACTIVE HOOKS      pre-push   -- AND NOTHING ELSE. NO PRE-COMMIT HOOK EXISTS.
hooks calling comp-*     0          (CONTROL: 15 files match '#!', so the grep works)
portal CI                0 of 3 workflows call comp-*
```
**All three SEV1 watch paths live in `portal/`. `safe-commit` runs at the workspace root and is NEVER in the path
for a portal file. 16 commits touched `ModelPortfolios.tsx` since 2026-06-01 with the gate never firing once.**

> **Repairing `safe-commit`'s `|| true` would fix a code path portal files never take — and the gate would then read
> GREEN for the same reason it reads GREEN today: NOTHING EVER ASKS IT.** *A repair that changes no behaviour, on a
> gate whose defect is that it is never invoked, is the purest placebo on the board — and it would have shipped with
> a green fixture.*

**A new verdict class, above `UNDISCRIMINATING` and `ANTI-CORRELATED`:**

| verdict | the tool's answer | why it is worse |
|---|---|---|
| `UNDISCRIMINATING` | independent of the property | fails a random-input control |
| `ANTI-CORRELATED` | inversely coupled to the property | **passes** that control |
| **`UNINVOKED`** | **correct, and never asked** | **passes EVERY control the tool can be given.** The defect is not in the tool. It is in the absence of a caller — *and no test of the tool can ever find it.* |

**Therefore §4 gains a fourth rail, and it is not about the tool:**
> **R4 — INVOCATION.** *Prove the tool is CALLED on the surface it claims to guard.* Cite the caller at
> `file:line @ vintage`. **A gate with no caller is not a gate. `N of <universe>` verified means nothing if the
> number of them that anything invokes is zero.**

**And the trap that nearly buried it, in two pairs of hands:** CVO was *"one line from reporting the exposure as
theoretical"* because workspace-root `git log -- portal/...` returns `0`. The COO then ran
`git -C portal rev-parse --git-path hooks`, got a **relative** `.git/hooks`, grepped the **root's** hooks dir, found
`pre-commit`, and was one sentence from writing *"CVO is wrong."*

> **A ZERO FROM THE WRONG REPOSITORY LOOKS EXACTLY LIKE SAFETY.**

---

## 12. R4 SHARPENED — **THREE LIMBS.** And my own first R4 sweep was `UNDISCRIMINATING`.

**I implemented R4 as `grep -rl <tool> .tools .githooks .github`. It reported `comp-surface-check: callers=5` —
for the gate we had just proven is never invoked on the surface it guards.**

> **`grep` for a tool's NAME is a NAME match. It counts mentions.** *Filename standing in for invocation, in the
> first tool written to catch exactly that substitution.* **The rail caught its own author on its first run.**

**The five "callers," classified:**
```
drift_producer.py:183            _run(["bash",".tools/comp-surface-check","scan"])   REAL, executed, rc IS read
safe-commit.sh:417               --mode advisory | sed || true                       executed, verdict DISCARDED
safe-commit.legacy-golden.sh:351 a golden COPY -- never runs
drift-producer-push.yml:25       a `paths:` TRIGGER FILTER -- not a call at all
__pycache__/drift_producer.pyc   a compiled artifact
```

### R4 — a gate is INVOKED only if all three hold

| limb | question | `comp-surface-check` |
|---|---|---|
| **R4a CALLED** | an *executed* call site — not a comment, doc, golden copy, path-filter, or `.pyc` | **yes**, two |
| **R4b CONSEQUENTIAL** | its verdict is **read** and can change the outcome | `safe-commit`: **NO** (rc discarded 3×) |
| **R4c REACHABLE** | the call site can actually be reached **on the guarded surface** | `drift_producer`: **NO** (see below) |

> **It fails a different limb at each of its two call sites, and neither covers `portal/`.** *A gate can be called,
> and read, and still guard nothing.*

### R4c — THE TRIGGER NAMES A PATH THE REPOSITORY NEVER PRODUCES

`.github/workflows/drift-producer-push.yml` — the workflow that runs the **one** invocation whose `rc` is read:
```yaml
on: push:
    paths:
      - 'portal/src/**'      # <-- names the CONTENT path
```
**`portal` is a SUBMODULE. A root-repo commit records a GITLINK bump, never a path under `portal/src/`.** Measured:
```
root commits touching 'portal/src/**'  since 2026-06-01 :   0     <- what the filter names
root commits touching 'portal' (gitlink)                :  19     <- what the root actually records
CONTROL: root commits since 2026-06-01                  : 6395    <- the search works
example 27f543ade  ->  portal | 2 +-   (one line: the pointer)
```
**Nineteen portal changes passed through and the trigger could not fire once.**

> **The filter reads like coverage.** *It names the content path while the repository records the pointer* —
> `filename` for `content`, `pointer` for `payload`, one more time, in the trigger of the gate that guards the
> firm's model portfolios. **`portal/src/**` in a root-repo `paths:` list is not a narrow filter. It is a filter
> that can never match.**

**The remedy is one line and it is CI/DT lane, not a `safe-commit` edit:** add `- 'portal'` (the gitlink) to the
`paths:` list, **and** wire a portal-side pre-commit hook (portal has **one** active hook, `pre-push`).
**Its acceptance is R4c itself: push a portal pointer bump and show the workflow FIRES.** *A trigger that has never
fired has never been tested.*

**And note what this does to `N of <universe>`:** CVO's AC-0 table needs an **INVOKED** column with all three limbs
cited at `file:line @ vintage`. **`comp-surface-check` would be the first row and it would read
`called: yes · consequential: no · reachable: no`.**

---

## 13. SEED 16 — `comp-manifest-check`. **THE CATALOG VALIDATES ITSELF.** (`0.4.0_DS_ClientPlatform~B`, `a08d904bb`)

**Verdict on `check` / `selfcheck`: `WORKS`.** *And credit where it is due:* `cmd_selfcheck` already asserts the
B+C categories are found, `>=1 ERROR`-class, **and exactly 3 findings so the benign line yields zero false
positives.** **R1 and R3, shipped by its author before this TO existed. It is the only tool anyone has found that
was already TESTED rather than merely RUN.**

### Verdict on the `completeness` family: `UNDISCRIMINATING` **with respect to the property in its own name**

```
routable / existence / completeness   all print  "PASS ... over 42 registered tool(s)"
Every assertion takes its denominator FROM tools_index. They assert index -> disk and index -> routable.
NOTHING ASSERTS disk -> index.
```
**Verified by the COO with a structural parse** (`yaml.safe_load`, not a regex — CVO's eleven phantoms taught that),
**with `comp-iam` as the positive control proving the parse and the key:**
```
tools_index entries: 42            comp-iam            REGISTERED   <- control
  comp-manifest-check   ABSENT     <- the gate that validates the manifest
  comp-surface-check    ABSENT     <- the SEV1 gate (Rule 20)
  comp-which            ABSENT     <- Rule 21's router
  comp-grep / comp-glob ABSENT     <- Rule 21's sanctioned answers
```

> **A COMPLETENESS CHECK WHOSE DENOMINATOR IS THE CATALOG CANNOT DETECT AN INCOMPLETE CATALOG.**
>
> *It prints `PASS` over 42 while nineteen on-disk tools — **including itself** — are invisible to it.* **This is
> AC-0's thesis, proven on the one tool that would have caught AC-0.** And it is `comp-iam` again: the assertion is
> invariant under the property changing, because the property is not in its domain.

### And the gate CANNOT TELL YOU IT DID NOT LOOK — exercised, live

```
EXEMPT file with a real ERROR inside, --mode blocking  -> rc=0, 0 bytes
SCANNED file, genuinely clean,        --mode blocking  -> rc=0, 0 bytes      BYTE-IDENTICAL
POSITIVE CONTROL: the same bytes at repo root          -> rc=1, "[ERROR] C_adhoc_reimplementation"
```
`exempt_path_substrings` includes **`org/modules/graph/`** — where the P4 fixtures live. **DS~B's own first probe
wrote itself there, got silence, and it nearly read the silence as `clean`.**

> **Every consumer of this gate treats "no ERROR printed" as "scanned and clean."** *A gate whose silence cannot
> distinguish `DID-NOT-LOOK` from `LOOKED-AND-CLEAN` is not reporting a verdict. It is reporting nothing, in the
> shape of a verdict.*

**§4 GAINS R5 — DISCLOSURE.** *A gate must name what it SKIPPED.* Print the denominator on **both** exit paths:
`scanned=N, skipped=M (reasons)`. **A silent skip and a clean pass must never be byte-identical.** *(Same law as
`fabric-check`'s `DEAF-COVERAGE: deaf=N over 85 enumerated inboxes` — which `DS~B` itself wrote.)*

### LATENT, `0` offenders today (`git ls-files`-verified) — and the class is already loose in the fabric

**`is_exempt` matches a SUBSTRING, not a path component.** `docs/` matches `mydocs/` and `oldocs/` — **a directory
named `oldocs` anywhere silently disables the gate beneath it, gold scripts included.**

> **Same species as `1.0.0_SA_CTO`'s `grep -iE 'iam'` matching `black_diaMond`, which staged a 49F file under the
> sovereign prohibition.** *Two agents, two hours, one substitution.* **It was staged and never landed.**
>
> **COO sovereign re-verification, grounded, not asserted:** `0` commits touching `data/black_diamond/` or
> `schwab/` since `22:20Z` (control: 112 commits in the window; the pathspec matches 814 historically). `0` staged.
> **`0` files under either tree with an mtime after the prohibition** (control: 1,341 files exist, 1,269 newer than
> 2020 — so `-newermt` discriminates). *Two dirty files remain; both predate the prohibition and are untouched.*
