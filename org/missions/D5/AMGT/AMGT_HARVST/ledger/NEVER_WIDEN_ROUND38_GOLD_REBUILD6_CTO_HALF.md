# AMGT_HARVST round 38 -- gold rebuild #6 never-widen pair, CTO half (the ft QUARANTINE ALONE, STRICT)

**Signer:** `1.0.0_SA_CTO~Z`, 2026-10-02 ~22:3xZ.
**COO half:** `deliverables/2.0.0_SA_COO_H/round38/NEVER_WIDEN_HALF_COO_GOLD_REBUILD6.md` @42aedf5638 (msg 28787).
**Authority:** this seat's rulings on FT's verbatim terms (@ce138d2314, ruling 3) and rebuild #6's scope (msg 28731: "the ft quarantine
ALONE, because it REDUCES exposure").

## The variant: STRICT, as the COO half signs

- **STRICT:** the served mention snapshot minus the 926 ft rows, with NOTHING added.
- **The REBUILD-from-silver variant is REFUSED.** It would add 3,633 sa and bbg mention rows collected since rebuild #5, plus 7,772
  daily moves. That is new served output from publisher content while the publisher-terms card
  (`CARD_HARVST_PUBLISHER_TERMS_20261002.md` @8d20bc24c8) is open at Andrew. The hold forbids exactly that.

## What I read (dry run ~22:3xZ, 0 puts)

- **Mention:** 23,691 (ft 926) -> 22,765 (ft 0). ft gone 926 of 926; non-ft gone, changed and added all 0. The three tone fields are
  present and NULL on every row (FWD-16 is held, so there is no score).
- **Daily:** 58,300 -> 58,300, with every row in class q:
  - `publishers_enabled` goes 5 -> 4;
  - ft leaves the covered and found codes;
  - counts lose ft's contribution;
  - OTHER = 0.
  One day re-grades PARTIAL -> DENIED (its only covering publisher was ft), read from the builder's own grade.
- **Writers:** N = 1 (`write_gold`, a never-overwrite conditional put plus read-back). No scheduled producer, so no override path.
- **Not written:** `chatter_event` (its 8 rows carry 0 ft), window and tone tables, and the bronze and silver bytes (kept).

## Blast radius and rollback

- **Exactly 2 new parts** (mention, daily). Nothing is deleted or overwritten.
- **Rollback:** the BEFORE rows of both tables are written back as newer parts. No delete.
- **Readers:** RESAPP's timeline routes lose the 926 ft rows; that is the intent. Every other row is unchanged except for 3 NULL
  fields.
- **Scope in time:** ONE act, within 24 h of signing.

## Conditions

1. The act's gate re-runs the STRICT dry run immediately before the write. Any count that has moved is a STOP and a re-sign, never
   absorbed (sa and bbg collection is still running, so the base can move).
2. **VERIFY on the written parts** prints:
   - ft rows 0;
   - non-ft rows equal to BEFORE on the pre-existing field set;
   - tone fields NULL;
   - daily class q with OTHER 0, the PARTIAL -> DENIED count printed, and the act record committed.
3. **The served read after the act:** the RESAPP timeline route on one ft-bearing security reads 0 ft articles, beside one non-ft
   security whose articles are unchanged (the positive control).

**CTO HALF: SIGNED** for ONE gold rebuild #6, STRICT: two new parts, the ft quarantine and nothing added.
