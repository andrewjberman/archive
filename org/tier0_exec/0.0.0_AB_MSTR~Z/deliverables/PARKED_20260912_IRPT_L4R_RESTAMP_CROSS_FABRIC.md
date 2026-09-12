# PARKED -- re-stamp the four IRPT L4-R sign-off records to hash-bound (cross-fabric)

**archetype:** PARK
**owner:** `0.0.0_AB_MSTR~Z` as cross-fabric carrier
**opened:** 2026-09-12 ~01:1xZ, site Z
**urgency:** LOW, and the low urgency is MEASURED, not assumed (see EVIDENCE)

## THE ITEM

Re-stamp four L4-R sign-off records so each binds to a PRD half HASH instead of falling back to a
version string:

```
org/missions/D9/IRPT/IRPT_BCKEND/prd/signoff/3.0.0_SA_CVO.json    signer 3.0.0_SA_CVO   (BASE)
org/missions/D9/IRPT/IRPT_BCKEND/prd/signoff/4.0.0_SA_CRO.json    signer 4.0.0_SA_CRO   (BASE)
org/missions/D9/IRPT/IRPT_FNTEND/prd/signoff/3.0.0_SA_CVO.json    signer 3.0.0_SA_CVO   (BASE)
org/missions/D9/IRPT/IRPT_FNTEND/prd/signoff/4.0.0_SA_CRO.json    signer 4.0.0_SA_CRO   (BASE)
```

## WHY IT IS PARKED RATHER THAN DONE

Three independent reasons, any one of which is sufficient:

1. **D9/IRPT is the LAPTOP fabric's**, and that device is in managed winddown.
2. **Andrew's site-Z session scope is explicit and narrow** -- relayed as msg 21430, VERBATIM:
   *"AMGT_RESAPP and POSN_ASTTAX only."* IRPT is outside it.
3. **All four signers are BASE serials with no base session live here.** CLAUDE.md: *"a BASE serial
   with no base session is a silent hole -- mail to a base while only LANES are live gets no bounce,
   no ack and no staleness signal, and reads as delivered."* Assigning this to those serials tonight
   would create exactly that hole, which is why it is parked with a named owner instead.

⛔ **AND A RE-STAMP IS NOT A CLERICAL ACT.** The current tool writes a hash-bound record, so whoever
runs it is giving a REAL SIGNATURE on an IRPT PRD's bytes as they stand -- not converting a file
format. It belongs to a seat that has actually read those PRDs. `4.0.0_SA_CRO~Z` could technically
stamp two of them and declined on exactly this ground; that refusal is correct and is recorded here
so nobody re-derives it.

## WHAT UN-PARKS IT

Either of:
- the laptop fabric's `3.0.0_SA_CVO` and `4.0.0_SA_CRO` sessions being live (route to them), or
- Andrew widening the site-Z session scope past AMGT_RESAPP + POSN_ASTTAX.

## THE UNDERLYING DEFECT (context, not the item)

`prd_signoff_lib.py:198` -- `current = (half_hash == hashes[half]) if doc.get("half_hash") else
(prd_version == version)`. A record with NO half_hash is graded on the VERSION STRING.
Census by `1.0.0_SA_CTO~Z`, denominator printed: **14 L4-R records across 5 projects; 6 carry
half_hash, 8 do not** (AMGT_RESAPP x2, POSN_ASTTAX x2, IRPT_BCKEND x2, IRPT_FNTEND x2). On the two
IRPT projects the version strings currently MATCH, so the fallback is the deciding branch there. On
AMGT and POSN the stale strings fail the compare, so those are inert -- by luck, not design.

Row `AMGT_RESAPP-Z-S6` is `1.0.0_SA_CTO~Z`'s and stays ARMED; this park does not touch it.

## EVIDENCE THAT THE URGENCY IS LOW

`4.0.0_SA_CRO~Z` measured both IRPT PRDs with the gate's OWN hash function
(`prd_signoff_lib.half_hashes`), each record at its own `prd_pin` versus HEAD:

```
IRPT_BCKEND (pin e6ba5d9878, v0.13)  brief 49684def3276 -> 49684def3276  MOVED=False
                                     ratified-text 4609cfe4b540 -> 4609cfe4b540  MOVED=False
IRPT_FNTEND (pin d1479bc5f0, v0.6)   brief a7e0e561a78a -> a7e0e561a78a  MOVED=False
                                     ratified-text 4d5f428c9bea -> 4d5f428c9bea  MOVED=False
```

Controls, both directions: POSN's brief half (known moved) returned MOVED=True at two pins and False
at the pin where nothing moved; POSN's ratified-text half (unchanged all night) returned False at
both. So the instrument discriminates and the four Falses are worth something.

>> **Z-S6 ON IRPT IS A LIVE EXPOSURE, NOT A LIVE LIE.** No IRPT signature is certifying unread bytes
   today. The fallback is returning the right answer for the wrong reason -- which is why it still
   gets fixed, and why it does not get fixed at 01:00 on a fabric in winddown. <<

⛔ **COVERAGE LIMIT THAT SITE Z CANNOT CLOSE:** that measurement was taken against this checkout at
HEAD `b9aec29d31`, equal to `origin/SITEZ` by ls-remote read. **If the laptop holds UNPUSHED commits
touching either PRD, no read from here can see them.** Whoever picks this up on that device re-runs
the comparison against its local HEAD before treating "no drift" as covering that fabric.

## WHAT THIS SEAT ALREADY DID (so it is not re-done)

The fix that stops the class GROWING is landed and on origin: `prd-signoff.py --expect-half-hash`
(`7204d31156`, pushed in `b9aec29d31`), exercised in-path by `4.0.0_SA_CRO~Z` on a real sign at
00:59:46Z -- negative arm REFUSED rc=3 and was measured a true no-op, positive arm STAMPED rc=0.
Every NEW stamp from here is hash-bound.

Cross-fabric awareness carried to the laptop over the agent bus, two messages:
`1d755918-a761-4c57-9544-733e21653786` (the notice) and `26ea021a-c3dc-42b8-a7ef-86e8b7f44476` (the
follow-up carrying the no-drift measurement that closed the notice's one open question).
⚠ Both are SENT, not delivered -- the bus queue holds 14 days and no laptop seat has acked. That is
expected during a winddown and is stated rather than read as delivery.

Sources: `1.0.0_SA_CTO~Z` msg 21899; `4.0.0_SA_CRO~Z` msgs 21883, 21888, 21898, 21905, 21909.
