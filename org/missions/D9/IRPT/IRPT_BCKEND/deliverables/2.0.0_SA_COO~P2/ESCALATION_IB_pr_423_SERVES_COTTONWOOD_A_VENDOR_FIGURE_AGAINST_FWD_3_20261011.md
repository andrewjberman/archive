# ESCALATION -- the vendor performance release (IB-pr-421, 422, 423) serves Cottonwood a VENDOR-calculated return, against ratified FWD-3

**From:** `2.0.0_SA_COO~P2` (dell2) | **To:** `1.0.0_SA_CTO~DELL2`; Andrew, at this seat's terminal | **Date:** 2026-10-11 ~09:5xZ |
**State:** the release is LIVE. IB-pr-424 (the reopen cell, CTO msg 4616) is NOT cut.

## What I got wrong

I placed `performance/authorization.py:90` as a stale per-use-word gate, recommended retiring it, and signed the COO half. I read the
egress law and did not read the ENDPOINT. The refusal was also the designed state of the product. I found this only now, reading
`retained.py` for the reopen cell.

## The three texts, each read at the line

1. **ENDPOINT FWD-3** (`org/missions/D9/IRPT/IRPT_BCKEND/prd/IRPT_BCKEND_PRD.md`): "An advisor reads, for any account at Inflection or
   Cottonwood, a performance figure computed by Opal from that account's own end-of-day holdings, and exports the same figure".
2. **ADDENDUM v0.19** (same file; ENDPOINT changed, on Andrew-direct 2026-09-28 ~22:2xZ and ~22:4xZ): "FWD-3's vendor-calculation rule
   is RETIRED; a vendor figure is now only a comparison point (FWD-13)." Its ruling 12: "No shadow path. The 49F engine read and the
   per-use Black Diamond plan retire from the adapter per firm, in the same window FWD-3 turns REALIZED for that firm".
3. **`infra/aws/lambda/investor-reporting/performance/retained.py:53-62`**, the docstring of `RetainedVendorFigureRefused`, citing
   `1.0.0_SA_CTO` rulings batch 66 item 2 (row IRPT_BCKEND-S247, 2026-10-01): "FWD-3 leaves no firm on a vendor's calculated return, a
   FRESH request for a vendor-path firm is already refused (VendorEgressRefused), and the retained copy was the one way the old figure
   still reached the page."

## What the release did

- Only Cottonwood reaches the vendor branch: `retained.py:304-315` ("Only Cottonwood reaches this branch now"). Inflection and 49
  Financial run on the holdings-basis gold or on IRPT_DASHBD's path.
- Before IB-pr-423 a Cottonwood user's fresh performance request answered UNAVAILABLE (OBJECT_NOT_COVERED): no figure.
- Since 09:19:10Z it answers with a Black Diamond-calculated return. Measured from `/aws/lambda/irpt-performance-adapter`: three
  requests at 09:45:40-42Z took the `fresh` path and ended `served`. The firm is INFERRED from the code path (the log lines read
  carry no firm); the caller is inferred to be the laptop's re-walk.
- The 2026-10-09 egress law (vendor APIs other than Bloomberg need no per-use word) permits the CALL. It says nothing about WHICH
  figure FWD-3 serves. I treated the first as settling the second.

## What I have not done

- I have NOT rolled anything back. A rollback moves served output and is not mine to take alone; the pair's Branch B names a 500, a
  `TypeError` and an `AccessDenied`, not this.
- I have NOT cut IB-pr-424. Returning a retained vendor figure on reopen would deepen the same departure.

## The ruling asked, and my recommendation

Either (a) Branch B now: the adapter zip back to S3 version `7IkeCAOa8F8IzqgaW1_WCLczFhmtzaLn` (digest
`9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=`), the source-map entry re-pinned back, then the two session-read policies removed by
the targeted destroy; or (b) a word that makes a vendor-calculated figure Cottonwood's served Performance answer until its
holdings-basis gold is served. (b) changes the ENDPOINT and rests on Andrew's 2026-09-28 word, so it is his.

**My recommendation is (a).** It restores the state the ENDPOINT describes; it is the signed rollback of both steps; and the walk's
Performance hop for Cottonwood is then honestly UNAVAILABLE until the holdings gold serves it (rows S250 and S252 name what that
waits on). The three figures already served cannot be unserved; the record should say they were shown.

## Also owed if (a) is taken

The round 119-121 L8 packet (@a3cb79cdb6) and the COO half (@468df7baa4) describe the release as a fix. Both need a correcting record;
I write it on the ruling.

`2.0.0_SA_COO~P2`
