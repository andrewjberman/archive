# `OPAL_ADVIPOINTERS` dependency read -- the graph, the startable set, and the shape

**Author:** `0.4.0_DS_ClientPlatform~G` - **Commissioned by:** `2.0.0_SA_COO` 71484
**Snapshot:** 2026-08-25T21:35Z @ `07cc7456178c` - **Population:** 13 TOs (the 8 SEAT rows, plus 5 carried as graph nodes because things depend on them)

## THE HEADLINE

**It is ONE LONG SERIAL SPINE, not a set with genuine parallelism -- but the phase numbers do NOT
describe it, and they fail in BOTH directions.** A seat ask built on the phase numbers would be
wrong twice over.

| | phase-number reading | what the TOs actually say |
|---|---|---|
| the four `P4` rows | one phase, ~4 parallel siblings | **a 5-DEEP SERIAL CHAIN inside one phase number** -- PUBIAM -> EMIT -> PINS-CERT -> REPOINT -> PROMOTE. Only `P4-EDGEREAD` is a true parallel sibling |
| `R-WATCH`, `INF-ONEWRITER` | invisible -- no phase number to place them | **fully independent, zero edges in either direction.** The two most startable rows in the project are the two a phase-order read cannot see |

**This is precisely the failure `1.0.0_SA_CTO` predicted** -- *"six seats discovering each other's
dependencies at runtime."* Seating the four `P4` rows in parallel off their shared number puts four
seats in a queue behind one another.

## NOTE: THE STRUCTURAL FINDING, and it is why this pass never happened

**NOT ONE of the 13 TOs carries a machine-readable dependency element.** I checked every one for
`<seating_trigger>`, `<start_condition>`, `<dependencies>`, `<gate>`, `<cross_domain_coordination>`:

```
TOs carrying ANY dependency element:  0 of 13
```

**Every edge in the graph below lives in `<status>` and `<priority>` PROSE.** That is why no tool
has sequenced this block, and why the pass had to be done by reading: the dependency data is in
sentences, and `to-check` renders a status line, not a graph. It is the same class as the defect
that started tonight -- **decision-bearing content sitting in a field nothing queries.**

## The graph (edges quoted from the TOs; nothing inferred from a phase number)

```
  INDEPENDENT (no predecessor, referenced by nobody)
    R-WATCH ........... DS base ... "activates at respawn; GO is this TO + the respawn itself"
    INF-ONEWRITER ..... DS base + AE (joint) ... INF plane, not the 49F chain; zero cross-refs

  THE SPINE
    P1-CLOSE [CLOSE] ................ "P2 opens on P1 close (framework law)"
      |
      v
    P2-DISPATCH [CLOSE] ............. "sequenced behind P1-CLOSE deliverables at this seat"
      |
      v
    P2-FLOOR [SEAT, AE] ............. "prep now, apply after the 23:01Z fixture + P2D-4 contract
      |                                + CTO per-apply gate"
      v
    P4-PUBIAM [SEAT, AE] ............ "sequenced behind P2-FLOOR apply at this seat"
      |                               "gates the P4 EMIT: DS~B cannot write platinum/advi
      |                                without the grant"
      +-------------------------------+
      |                               |
      v                               v
    P4-EMIT [CLOSE, DS~B]        P4-EDGEREAD [SEAT, AE]  <-- the ONLY true parallel branch
      |                               "slotted after P4-PUBIAM"
      |  "every downstream row (4b pins, 4c flip) consumes your output"
      v
    P4-PINS-CERT [node, CVO] ........ "the flip (4c) is illegal without the pre-flip pin + cert"
      |
      v
    P4-REPOINT [CLOSE-PENDING-RULING, DE]
      |   status: "P4R-3 flip DECLARED-HELD on all 10 keys ... route act surfaced to COO for AE"
      v
    P4-PROMOTE [SEAT, DT] ........... "executes on DE P4R-5 handoff"
      |
      v
    P5-TEARDOWN [SEAT, AE] .......... "HELD ON THE FRAMEWORK P5 GATE (pre-existing law, not a new
                                       gate): acts begin only after the P4-verified event + CTO
                                       per-item gate"
      |
      +--> BACK EDGE: P4-PINS-CERT's census tail. 3.0.0_SA_CVO 71493, and the TO's own status:
           "GROUP CENSUS REMAINS OPEN (P5-gated)."  The one P4 row with work that runs at P5 time.

  PARALLEL PREP (not on the critical path today)
    P3-CLOSE [SEAT, DS~A] ........... "prep may start now, close evidence from the 08-20
                                       scheduled run"
```

## STARTABLE TODAY -- every predecessor satisfied

| row | executor | why startable | kind |
|---|---|---|---|
| `R-WATCH` | `0.4.0_DS_ClientPlatform` base | no predecessor; its GO *is* the TO + the respawn | FULLY startable |
| `INF-ONEWRITER` | `0.4.0_DS_ClientPlatform` base + `0.7.0_AE_CloudOps` joint | no predecessor, different plane (INF, not 49F); "DATED this week, owners named" | FULLY startable |
| `P3-CLOSE-49F` | `0.4.0_DS_ClientPlatform~A` | "prep MAY START NOW"; the close itself waits on a scheduled run | PREP only |
| `P2-FLOOR-49F` | `0.7.0_AE_CloudOps` | "PREP NOW"; the apply waits on the P2D-4 contract + CTO per-apply gate | PREP only |

**Everything else has an unsatisfied stated predecessor.**

## NOTE: THE SEAT ASK -- and the number depends on a ruling you have not made yet

**Of the 8 SEAT rows, FOUR are AE and all four sit on the spine in order:**
`P2-FLOOR -> P4-PUBIAM -> P4-EDGEREAD -> P5-TEARDOWN`.
**ONE AE INSTANCE CARRIES ALL FOUR SEQUENTIALLY.** Seating four AE lanes would put three of them in
a queue behind the first.

```
  executor class over the 8 SEAT rows
    0.7.0_AE_CloudOps ......... 4   (P2-FLOOR, P4-PUBIAM, P4-EDGEREAD, P5-TEARDOWN) -- ALL SERIAL -> 1 seat
    0.4.0_DS_ClientPlatform ... 3   (R-WATCH base, INF-ONEWRITER base+joint, P3-CLOSE ~A)
    0.4.0_DT_ClientPlatform ... 1   (P4-PROMOTE) -- deep in the spine, NOT startable now
```

**RECOMMENDATION (labelled as such -- you rule the order and the seating):** the defensible ask
today is **2 to 3 seats, not 6 to 8** -- one AE for the spine's AE leg, one DS for `R-WATCH`, and
one DS for `INF-ONEWRITER` (which is joint with AE and on a different plane, so it may belong with
the AE seat instead -- your call, and it is the one row I would not place without you).

NOTE: **AND THE COUNT IS COUPLED TO YOUR CLOSE RULINGS, WHICH IS THE PART I DID NOT EXPECT.**
`P1-CLOSE` and `P2-DISPATCH` are both `CLOSE` in the sweep (instances VALID rc=0, all rows PASS).
They are the first two nodes of the spine. **If you close them, `P2-FLOOR`'s stated apply gate may
already be satisfied -- and that cascades into `P4-PUBIAM`.** So the seat ask and the close
adjudication are not two independent decisions; doing the closes first may convert the AE seat from
prep-only to fully startable. I am not asserting the gate IS satisfied -- see limit 1.

## Limits, stated

1. NOTE: **A STATED GATE IS A CLAIM IN A RECORD, NOT A MEASURED FACT ABOUT THE WORLD.** Every edge
   above is as true as the TO that states it and no truer. I did not verify one gate against live
   infrastructure -- you explicitly did not ask for that, and it is a much larger job. **If a TO is
   wrong about its own precondition, this graph inherits that silently.** Carry the caveat into the
   seat ask rather than letting it firm up on the way to Andrew.
2. **The one gate I have positive reason to doubt** is `P2-FLOOR`'s -- not because it is misstated,
   but because its predecessors are `CLOSE` candidates and the status text predates that. It is
   stale-prone, not wrong.
3. **`P4-REPOINT` carries a live hold I did not adjudicate:** *"P4R-3 flip DECLARED-HELD on all 10
   keys ... the advi twins are unreachable from every portal route family ... route act surfaced to
   COO for AE."* That is a real blocker on the spine and it is already yours.
4. **`P4-PINS-CERT` included as a node only.** `3.0.0_SA_CVO` ruled it at 71493 (2 of 3 uncovered
   criteria discharged in sibling artifacts, `49F-CENSUS-READ` genuinely open and already declared
   open in the status -- the close is earned). Not re-adjudicated here.
5. **Population inherited from `to-check`**, same as the sweep -- deliberately, because the
   `project=` attribute drifts and ADVIPOINTERS is exactly where a drift would hide.
6. **Edge direction was read from prose, and prose is ambiguous in a way a field is not.** Where a
   TO says only that it is "sequenced behind" something, I recorded an edge; that phrasing can mean
   a hard gate or a seat's own ordering preference, and **the two are indistinguishable in the
   text.** Two edges rest on it (`P2-DISPATCH` behind `P1-CLOSE`, `P4-PUBIAM` behind `P2-FLOOR`).

-- `0.4.0_DS_ClientPlatform~G`
