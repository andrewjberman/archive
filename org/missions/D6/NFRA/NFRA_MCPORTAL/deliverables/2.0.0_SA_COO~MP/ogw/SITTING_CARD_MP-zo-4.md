# The /opalgateway sitting (MP-zo-4) -- card for Andrew, and the GO the issuer fills from it

Prepared 2026-10-21 ~00:0xZ by `2.0.0_SA_COO~MP` while the close run waits. Nothing here is a request yet: it is asked for when batch17 (`OG-rl-18`, not before 2026-10-22T06:00Z) has closed and the bundle at mcportal `f90f03a` is live. The open call is `sitez-20261020T212417Z-ee12`.

## What Andrew does (about ten minutes, once)

1. Name the test person: one colleague (or a test login) who can sign in and call the gateway. The issuer needs: their display name as the People page shows it, and how they call (which client). No account numbers.
2. At `https://mcp.opalinvest.dev/opalgateway`, signed in as the owner, pick that person and make six changes in this order, one click each, letting the page re-read between them:
   1. switch one channel OFF;
   2. switch it back ON;
   3. switch one tool OFF;
   4. switch it back ON;
   5. STOP the person;
   6. RESTORE the person.
3. Between the changes, the test person makes one call to a tool of that channel and one to the named tool (the issuer tells them which). Expect: refused after 1, 3 and 5; admitted after 2, 4 and 6.
4. Say, in your own words, what the page showed (a few sentences; they are quoted verbatim and graded by the CVO). Do not summarise for the record: say it to the issuer's terminal.

## What the issuer fills into the GO file after the sitting

`deliverables/2.0.0_SA_COO~MP/ogw/GO_MP-zo-4.md`, read by the worker `~44`:

- `PRINCIPAL_TID=` / `PRINCIPAL_OID=` (the test person's ids, from the People page data; written as given, never invented);
- `CALLING_IDENTITY=` (how the worker may call the gateway as that person: or the words `NO CALLING IDENTITY`, in which case every effect check records false with that reason and substitutes no one);
- `CHANNEL=` and `TOOL=` (the ones switched) and the two exact tool calls;
- `T0=` / `T1=` (ISO Z): the window of the six changes;
- `ANDREW_WORDS=` (verbatim).

The worker is spawned only after this file is committed. The worker cannot make any of the six changes; the writer verifies the owner's signed header.

## Limits stated in advance

- The unattributed arm (a store-direct write in a test tree) is proven by `MP-zo-2`'s page test and is not repeated served.
- The writer's refusal of a non-owner `master_admin`'s widening confirm is `MP-zo-3`'s fifth test; its served arm needs a real non-owner session and is not graded here.
- `Z-W3-S2`'s last limit (the configured owner key equals Andrew's oid) is proven by step 2 itself: the writer accepts his header.
