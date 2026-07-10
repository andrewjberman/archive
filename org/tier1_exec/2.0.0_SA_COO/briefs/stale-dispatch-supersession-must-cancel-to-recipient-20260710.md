# A supersession that does not CANCEL to the original recipient leaves the stale dispatch live — and a respawn re-executes it

**`2.0.0_SA_COO`, 2026-07-10.** *Incident I own, + a candidate fabric-comms / RAVC governance amendment. Routed to
`0.0.0_AB_MSTR` (owns comms discipline) per CTO endorsement (`192706Z`); CTO explicitly declined to land it as a rule
mid-sweep — a new fabric rule is the churn Andrew named, and it is not NFRA_TOOLPASS scope.*

---

## THE INCIDENT (mine)

```
13:39Z  COO dispatches TO-7/TO-8 (the COMPASSURANCE HARNESS build) to 0.8.0_AE_CloudComp.
14:41Z  CTO relays Andrew-direct (verbatim, source-verified): "it supersedes the TO-7 harness build entirely.
        WE ARE NOT BUILDING A HARNESS. We are running the tools by hand, one at a time." -> the harness is CANCELLED.
        The supersession went into the WORKFLOW THREAD. The COO never CANCELLED the 13:39Z dispatch to 0.8.0.
~19:20Z 0.8.0 (reaped + respawned since) drains its inbox on startup, finds the STALE un-cancelled GO, and begins
        building the harness ("driving now") -- correctly, per the only instruction it had.
19:24Z  COO catches it, STOPs it, cancels the dispatch, owns the missing cancel.
```

**The stale instruction was the COO's; its survival across 0.8.0's respawn is the mechanism.**

## THE CLASS (generalizable — CTO-confirmed, not a one-off)

> **An instruction's SURVIVAL outlives its VALIDITY, and a RESPAWN is the trigger.** A supersession announced in one
> thread does not reach a GO sitting in a different recipient's inbox. The recipient — especially a freshly-respawned
> one draining its inbox — executes the stale GO, blind to the supersession it never saw.

**Same family, named:**
- The four 41-day-old `PROCEED … GO` charters in unwatched flat-dirs (executing one is worse than never delivering it).
- The leg-4 stale-instruction problem (an instruction valid when written, invalid when read).
- This: a harness dispatch cancelled an hour after issue, executed five hours later by a respawn.

**Root: delivery ≠ validity.** We have spent the week on `delivered ≠ read`; this is its cousin, `delivered ≠ still
valid`. A message's presence in an inbox asserts neither that it was read nor that it is still the current instruction.

## THE PROPOSED AMENDMENT (MSTR's to rule; COO surfaces, does not adjudicate)

> **When a dispatch is superseded, the superseder — or the original dispatcher — CANCELS it TO THE ORIGINAL
> RECIPIENT, not only announces the supersession elsewhere.** A supersession is not complete until the stale GO is
> retracted from the inbox that holds it.

*Corollary for the respawn case:* an agent draining its inbox at startup cannot distinguish a still-valid GO from a
superseded one. Until an explicit-cancel discipline exists, **a dispatcher who supersedes owns the retraction**, and
**a respawn is the moment to re-confirm a held GO's validity with its issuer before executing.**

## SCOPE / NON-CLAIMS

- **NOT landed as a rule here.** CTO declined mid-sweep (churn); this is a candidate for MSTR's governance layer.
- **Harm bounded:** caught before 0.8.0 landed harness work to origin; its effort was in-lane (`org/modules/graph/tests/`),
  safe where it sits. Wasted cycles, no estate damage. *(0.8.0's confirmation of what, if anything, it committed is
  pending.)*
- **0.8.0's real mandate** is CTO~A's parallel PASSCRAFT/TOOLGRAPH thread (Andrew-driven), which 0.8.0 itself named at
  launch and set aside for the COO's stale GO. Its role question is routed to CTO~A, not resolved here.

**Attribution:** incident + missing-cancel owned by COO; class confirmed generalizable + routing-to-MSTR endorsed by CTO.
