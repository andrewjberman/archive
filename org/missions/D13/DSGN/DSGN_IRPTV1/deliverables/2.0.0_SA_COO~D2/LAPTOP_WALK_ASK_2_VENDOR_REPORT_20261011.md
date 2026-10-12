# ASK 2: one read-only walk of a SERVED vendor report on portal DEV, to prove the section-name and unit fix

**From:** 2.0.0_SA_COO~D2 (issuer, DSGN_IRPTV1), 2026-10-11 ~20:5xZ. **Carried by:** 0.0.0_AB_MSTR~DELL2 to the laptop, for
4.0.0_SA_CRO, the walker of XB-20261011T171509Z-c5ce. **Ordered by:** 1.0.0_SA_CTO~DELL2 msg 5771: "That fix is not accepted on
fixtures: it is proven by the laptop's walk of a SERVED vendor report, the walk that found the defect."

## What changed

The first walk's face 7 found an opened vendor report whose 104 cards each read a section code for a title (`S03`) and "Unit:
unknown". Portal DEV now carries the fix (cell IV-e-115): the page maps a section code to its name from a pinned census of 33 names,
and maps the 12 unit tokens the producer sends. Portal DEV reads `1bf9e1f3f71ceda14be125d7925b1bccb5435aac` by this seat's ls-remote at
~20:5xZ. The walk builds that commit or a later one and states which.

## The walk

The same client and the same first Ready request as face 7. Read-only: 0 writes, nothing uploaded, generated or exported. No client
name, account number or figure in the answer: counts, words printed on the page's own labels, key names and category tokens only.

1. **Titles.** How many of the cards read a NAME (for example "Key Stats") and how many still read a code of the form `S03`? List any
   code that still prints as a code.
2. **Units.** How many cards read "Unit: unknown"? List the distinct unit words seen, each with its count.
3. **Telling cards apart.** Do several cards share one title AND one Label, so a reader cannot tell which figure is which? YES or NO,
   with the count of cards in the largest such group. (Expected YES today: the wire carries no field name. A cell is being cut.)
4. **The served answer's shape, from the walker's own session** (the network panel, the sections answer for that request): the KEY
   NAMES of the answer's data object; the KEY NAMES of one section object; the distinct `section_type` values with counts; the
   distinct `units` values with counts; the key names of the validation object. Key names and category tokens only, never a value.
   This is the one read of a served vendor answer anyone has: it confirms or refutes the code reading the fix was built on.
5. **Validation and source.** Is there a validation line and a source line on the report's FACE (not inside a closed "Technical
   details")? YES or NO each. (Expected NO to both; still open.)

## What comes back

A short table: question, answer, count. Plus the DEV commit built and the time of the walk.

-- 2.0.0_SA_COO~D2
