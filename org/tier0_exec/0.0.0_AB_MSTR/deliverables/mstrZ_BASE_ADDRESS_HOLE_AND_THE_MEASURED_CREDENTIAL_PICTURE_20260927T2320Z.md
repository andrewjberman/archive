# Two integrator findings, 2026-09-27 ~23:1x-23:2xZ -- a 12-day-deep address hole, and the credential exposure measured rather than relayed

**Author:** `0.0.0_AB_MSTR~Z`. Both were found while running the ordinary push cadence; neither was
being looked for.

---

## 1. MAIL ADDRESSED TO THE BASE SERIAL HAS NO CONSUMER ON THIS DEVICE

A routine push refused: `HALT-GATE: 26 pending message(s)`. All 26 were addressed **`To:
0.0.0_AB_MSTR`** -- the BASE serial, no lane. Measured per slice, at 23:1xZ:

| slice | unread (top level) |
|---|---|
| `org/mcp/inbox/0.0.0_AB_MSTR/~Z/` (what my watcher watches) | **0** |
| `org/mcp/inbox/0.0.0_AB_MSTR/` (base) | **26**, aged **3 to 12 days** |

Only the `~Z` session exists on this device and a watcher watches exactly one slice, so **the
pre-push halt gate is the only reader base-addressed mail has here.** The gate resolves my LANE
serial and scans the BASE slice -- which is what surfaced these at all. **The delivery lag therefore
equals my push cadence**, and nothing announces it in a quiet window.

**THE GATE WAS DOING A SECOND JOB NOBODY DESIGNED IT FOR.** It is a SEQUENCE control: never push
blind past a STOP addressed to you. Here it was the sole DELIVERY mechanism for an entire address.
A control that is also a channel's only reader looks healthy exactly when the channel is starving.

**WHAT WAS IN THERE** -- the mix is the argument against treating an aged queue as noise:

- **21** FYI/record relays from `4.0.0_SA_CRO~W` (2026-09-15) -- the class CLAUDE.md rule 31 now bars
  from an inbox outright ("FYIs and corroborations go to the record, not to an inbox").
- **2** from `1.0.0_SA_CTO~Z` (09-24) -- the identity-denial rulings R-71/R-72. Already known here.
- **3** from `2.0.0_SA_COO~Z` (09-18), and **one of those was a genuine integrator ASK**: *"Portal DEV
  merged locally (625a0888), needs INTEGRATOR PUSH"*. **Unread for 9 days.**

**I MEASURED THE ASK BEFORE ACTING ON IT, and it was world-done:** `625a0888` is an ancestor of
`origin/DEV` (tip `c3dd9ca9`, `ls-remote` read), with `--is-ancestor HEAD HEAD` as the positive
control. Re-executing would have been a rewind. **NEVER-2's "measure the artifact before acting on an
open entry" applies to a stale ASK, not only to a stale ledger entry** -- an unread ask and an
unfinished act are indistinguishable from the inbox alone.

**DISPOSITION:** all 26 moved to the base slice's own `read/`; the gate now passes rc=0 silently.
Reviewing them was not consuming them, and leaving them would have re-refused every future push --
which is precisely what trains a seat to bake `HALT_ACK=1` into its push command and retire the gate.

### The correction was ALMOST parked FOR NO REASON -- the broker was the wrong liveness instrument

The senders believe they delivered. The correction they need is one line: **on site Z, address the
integrator as `0.0.0_AB_MSTR~Z`, not the bare base serial.**

**I first wrote this section as a PARK.** `get_live_agents()` returned exactly **one** LIVE seat,
`0.7.0_AE_CloudOps~I` -- a Tier-2 this MSTR is barred from writing to (`mstr-no-tier2-writes`). No
permitted recipient, so I gave the item an owner and an un-parking condition: *"the first Tier-1
session to register LIVE on this device."*

⛔ **THAT CONDITION WOULD NEVER HAVE FIRED, AND THE ITEM WOULD HAVE SAT FOR HOURS ON A MEASUREMENT
ERROR OF MY OWN.** I checked the process plane before believing it:

| instrument | reading |
|---|---|
| broker `get_live_agents()` | **1** LIVE |
| `claude.exe` with a serial in argv (process plane) | **7** sessions |
| per-session MCP servers (`org/mcp/server.py`) | **2** |

**FIVE OF SEVEN LIVE SEATS CANNOT REGISTER, so the broker's live-set undercounts by 6** -- and four of
the seven are Tier-1 seats I am perfectly free to write to: `1.0.0_SA_CTO~O`, `1.0.0_SA_CTO~Z`,
`2.0.0_SA_COO~O`, `2.0.0_SA_COO~Y`, `3.0.0_SA_CVO~O`.

⭐ **THE LESSON, AND IT IS THE INVERSE OF THE ONE I ALREADY HELD.** I have banked *"a live PID is not a
consuming session"* -- do not infer reachability from a process. **The inverse is just as wrong: AN
UNREGISTERED SESSION IS NOT A DEAD ONE.** A registration is a claim the seat's MCP server makes on its
behalf; when that server is gone the seat is still there, still working, still reachable by
FILESYSTEM. **A park justified by "nobody is live" is only as good as the instrument that said so, and
parking is the failure mode that leaves no trace** -- an item parked on a condition that cannot fire
looks identical to an item correctly waiting.

**DELIVERED, not parked:** one file to each of the five Tier-1 lane inboxes at **23:49:04Z**, 1,330
bytes each, over the channel that survived the 09-26 outage. A `read/` move will prove a WATCHER
acted; it never proves the agent read it, and delivered-to-the-door is the strongest claim this
channel supports.

## 2. THE LIVE BD PASSWORD IS OUT OF THE WORKING TREE -- MEASURED HERE, NOT RELAYED

`2.0.0_SA_COO~O` escalated at 23:00Z (row `NFRA_MCPINDEX-Z-S31`) that the live BD password sat in **18
places across 16 tracked files**, and asked for tonight's history purge scope and a rotation to go to
Andrew before 02:45Z. `0.7.0_AE_CloudOps~I` then reported the redaction done, 24 sites / 22 files.

**A producer's self-report is not evidence (CLAUDE.md section 4), so I ran the producer's own
instrument myself** -- `secret_literal_census.py`, landed by that seat @`03086508a9`, which reports
every value as `len` + a sha256 prefix and never emits a secret:

```
python .../secret_literal_census.py . --fingerprint 161ff0eb3831
  DENOMINATOR: 76581 text file(s) scanned under .
  occurrences of 161ff0eb3831: 0
```

**0 occurrences across a printed denominator of 76,581 files.** The working tree at HEAD is clean.

⛔ **AND THAT NARROWS THE DECISION RATHER THAN CLOSING IT. THE TREE IS NOT THE HISTORY.** The
redaction commits exist, so by construction their pre-image blobs are still reachable in git history
-- that needs no measurement, it is what a commit IS. So:

- **Working tree:** clean, measured, 0 of 76,581.
- **History:** still carries it. Only a rewrite reaches that, which is tonight's purge.
- **Clones already taken:** **no rewrite reaches those at all** -- two full clones and ~60 worktrees on
  this device alone. **Only rotation ends that exposure**, and rotation is not a substitute for the
  purge or vice versa. They are different remedies for different populations.

**I corrected my own earlier escalation to Andrew on this point**, which had said the password "sits
in 16 tracked files" -- true when `2.0.0_SA_COO~O` measured it, false by the time I repeated it. **A
perishable state claim restated an hour later is a new claim and needs its own measurement**; I have
now paid for that twice in two days.

**WHAT I AM NOT DOING:** widening tonight's purge scope on my own judgment. The command and its blast
radius are the laptop MSTR's; the scope is Andrew's. Both decisions remain open and are stated as open.

## 3. TRUNK STATE AT WRITING

Pushed on cadence at 23:1xZ. `origin/CLOUD` = `03086508a9` (`ls-remote` READ), local `CLOUD`
identical, **0 unpushed**. The push printed `605ab459a0` as its target and **landed `03086508a9`** --
the understatement property again, so the three-commit tail beyond my pre-push guard range was graded
after the fact: 1 add, 2 modify, no deletions, no gitlink moves, banned commit absent.
