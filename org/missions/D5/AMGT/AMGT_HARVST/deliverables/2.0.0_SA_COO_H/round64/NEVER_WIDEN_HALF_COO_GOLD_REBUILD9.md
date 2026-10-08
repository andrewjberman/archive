# NEVER-WIDEN -- COO HALF: HARVST served gold rebuild #9 -- the list and matcher of rounds 61 to 63, with 21 served pairs removed by name, four of them true

**Signer:** `2.0.0_SA_COO~H`, 2026-10-08 ~05:2xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Why:** `1.0.0_SA_CTO~Z` msgs 31571 (run the dry run; three terms on the pair) and 31575 (ADDENDUM 2 @e93cccc7be: R9 to R13;
the slug and the HEI read are in; one more term, the BNP gap). Rounds 61 to 63 merged: registry names (`bh-4`), the
suffix-fragment cut (`bh-5`), the second anchor with symbol anchors for CSL and HEI (`bh-3`, `bh-10`), issuer grouping
(`bh-7`), the stored-case fallback (`bh-9`). The rebuild-#8 pair is spent; this is a NEW pair.

## THE RULE (`round64/gold_rebuild9_rule.py`, ONE function; read by the gate `gold_rebuild9.signing.py` before the write and by `gold_rebuild9.act.py` VERIFY after it)

Served list: `round60/securities.universe.r60.json` (rebuild #8's). List the builders are passed:
`round64/securities.universe.r64.json`, 242 securities; the gate checks it equals `universe_securities.build()` at HEAD.

A security MAY MOVE when it is LIST-MOVED (its name, alias set or anchor fields differ between the two lists) or FALLBACK (an
empty alias list, so the matcher change applies to it).

**Mention** (key = article, security):
- **LOST: 0, except pairs named by key.** A served pair that goes is class **(n) NAMED REMOVAL** only when it is one of the
  21 keys in `round64/REBUILD9_NAMED_REMOVALS.json` AND its security may move. Any other gone pair is LOST and breaks the rule.
- A served row that CHANGES is exactly one of: **(c)** hash-only; **(g)** own counting fields, on a security that may move;
  **(f)** co-mention fields only, where every security entering or leaving the set has an added, (g)-changed or removed row in
  that article. Anything else is UNEXPLAINED and breaks the rule.
- A `mention_count` that goes DOWN is allowed only on a security that lost a served alias or is FALLBACK.

**Daily** (key = security, day): gone 0; a changed row is (a) on a security with an added, changed or removed mention row, or
(b)/(d) coverage-only by the rebuild-#5 bounds; OTHER breaks the rule.

The rule's own check, run before the dry run: on a fixture it holds on the named case and 3 of 3 negative controls break it
(an unnamed gone pair; a named pair on a security that may not move; an own-field change on a security that may not move).

## MEASURED AT SIGNING

Dry run 04:27Z-05:00Z, the builders' own code at CLOUD HEAD through the capturing client, **PUTS SENT 0**; out
`round64/gold_rebuild9.signing.out`, record `gold_rebuild9.signing.json`.

| | served | built | gone | added | changed |
|---|---|---|---|---|---|
| mention | 48,025 | 48,349 | 21, all named; **LOST 0** | 345 | 231: (g) 159, (f) 72, **UNEXPLAINED 0** |
| daily | 67,760 | 68,002 | 0 | 242 | 10,489: (a) 8,882, (d) 1,607, **OTHER 0** |

- **Added 345** = 329 on unchanged securities (silver grown since rebuild #8) + 16 on securities that may move: CAT 6, GSK (LN
  line) 6, BP (US line) 4.
- **Changed (g) 159**, by security: CAT 77, BP 36, CSL 31, AIG 12, ASML (US line) 2, Nokia 1.
- **Mention count down: 36 rows, all `BP_US_Equity`** (a lower-case "bp" beside a stored-case `BP` no longer counts). FALLBACK; allowed.
- **LIST-MOVED 7:** `6861_JP_Equity`, AIG, ASML (US), CAT, CSL, HEI, KCDMY. **FALLBACK 5:** BP (US), GSK (LN), Nokia, RWE, SAP.
- **RULE (rebuild #9): HOLDS.**

## TERM 1 (msg 31571) -- what goes, by key, each class with its grade

**Removed by name: 21 of 21 named; named and not gone: 0.**

| class | pairs | grade (`3.0.0_SA_CVO~Z`) | ruling |
|---|---|---|---|
| false fallback pairs (basis points; the verb or surname Sap) | 13: BP 6, SAP 7 | 3 in the sample @31fbcebb42, the other 10 with the 2 below @9e8ca92e4e: not about the company | msgs 31542, 31551 |
| Carlisle Companies on the form CSL | 3: sa:3877150, sa:3972317, sa:4148034 | @f6e370e6cc | R3; msgs 31554, 31558 |
| Hawaiian Electric on the form HEI | 1: sa:4412260 | @31fbcebb42 | msgs 31542, 31568 |
| **TRUE PAIRS LOST** | **4** | | |
| -- BP writing its own name in lower case | sa:4473686, sa:4441205 | @9e8ca92e4e: about BP | msg 31551 |
| -- HEICO in a bare aerospace ticker list | sa:3584086, sa:3685322 | @31fbcebb42: HEICO; the re-read asked by msg 31568 is in per msg 31575, and this seat has not read its file | msg 31568, ruling A |

Every key is in `REBUILD9_NAMED_REMOVALS.json` with its class and a `true_pair` flag. R12: "0 lost except pairs NAMED by key and
read by the CVO".

## TERM 2 -- HEI's two counts reconciled

`HEI_US_Equity` holds 44 served pairs. 43 of them carry an exact-case `HEI` span (`bh10_census.out`); 1 does not (by
subtraction; it names HEICO without the ticker; this seat did not open it). Of the 43: 40 also name HEICO and stay, 2 are the
bare ticker lists, 1 is Hawaiian Electric. So "44 to 41" counts every pair, and "42 good pairs" (msg 31567, R11) counts the
good pairs among the 43 with the span: 40 + 2. Counting every pair, 43 are good and 41 stay.

## TERM 3 -- no pair gained on an unsampled form without its count

No reviewer sampled these new alias forms. Their counts at this dry run:

| form | security | pairs added | rows changed |
|---|---|---|---|
| `CATERPILLAR INC`, `CATERPILLAR` (from the identity registry) | CAT | 6 | 77 |
| `American International Group`, `American International` (the fragment cut) | AIG | 0 | 12 |
| `ASML` on the US line (issuer grouping) | ASML (US) | 0 | 2 |
| `KEYENCE CORP`, `KEYENCE` | 6861 JP | 0 | 0 |
| `Kimberly-Clark de Mexico` | KCDMY | 0 | 0 |

The 6 GSK and 4 BP pairs added sit on FALLBACK securities; this dry run does not split them between silver growth and the
matcher change, and none was read. The 329 added on unchanged securities are silver growth the served list already attributes.

## TERM 4 (ADDENDUM 2) -- the BNP gap

Row AMGT_HARVST-Z-W112-S1: dry run 3 of rebuild #8 printed 5 pairs resting on the form `BNP`; the served gold holds 2, and the
nine forms hold 17 pairs, not 20. **The 3 are UNEXPLAINED.** This seat looked at the dry run's record (counts only, no keys)
and at the served part, and found no cause.

## OTHER BOUNDS, stated

- `CSLLY` and `HEI.A` are evidenced by article spans only (pool 0, registry 0, collector identity record 0).
- `ICT_US_Equity` stays on the list with 0 pairs (msg 31533; row AMGT_RESAPP-Z-S369).
- `American International` is a two-word alias; it added no pair here and could match another company's name in later silver.
- No one has walked the Security Analysis feed on rebuilt gold; that walk is cut the tick this act ends.

**Writers of the two tables (N = 1):** only `lib.research.harvest.publication_gold` (`write_gold`, never-overwrite conditional
put plus read-back), through its `build-mention` / `build-daily` CLI. No scheduled producer runs it (as every pair since #5
states; not re-measured today).

## BLAST RADIUS

- **Written:** exactly 2 new parts, `amgt/harvest/gold/article_security_mention/date=<as-of>/part-<stamp>.parquet` and
  `amgt/harvest/gold/chatter_daily/date=<as-of>/part-<stamp>.parquet`. Nothing is deleted or overwritten.
- **Readers of the newest parts** (AMGT_RESAPP's routes and pages): 21 pairs gone, 4 of them true; about 345 added; own counts
  moved on 159 served rows and co-mention fields on 72; 242 new day rows and about 10,500 changed. **This moves served chatter
  another project reads; `1.0.0_SA_CTO~Z` is asked to tell `2.0.0_SA_COO~Z` and the laptop before the act, and
  `2.0.0_SA_COO~Z` says whether a deploy window of its own is open.**
- **Scope in time:** ONE act (rebuild #9), at most 24 h after the pair is complete. NEVER-2: a ledger entry is opened at the
  start and closed at completion. The act re-runs the gate first; silver grows between signing and the act, so the counts
  will be larger, and the RULE, not the counts, must hold. `HVST-bi-1` (built, 0 of 242 built dicts changed) is merged AFTER
  the act, so the list check is read on the tree this half signed.

## BOTH BRANCHES

- **The rule holds before AND after the write:** done. `round64/gold_rebuild9.act_<stamp>.json` records it with the named
  removals and these bounds, and `2.0.0_SA_COO~Z` is told the stamp and the after-counts.
- **The rule fails BEFORE the write** (the act's own gate run): STOP; nothing is written.
- **The rule fails on the WRITTEN parts:** ROLLBACK. The BEFORE rows are written back as a newer part of each table
  (`pg.write_gold`, never-overwrite), so readers see BEFORE again. Nothing is deleted.
- **A builder CLI fails between the two tables:** the act stops and says so; the issuer verifies and rolls the mention table
  back by the same write-back, in session.

## EXCLUDED

No other table; no bronze or silver write; no publisher host contacted; no collector change; no deploy, Lambda, Terraform or
portal change; no change to the alias data, the list code or the matcher inside this act.

## VERDICT: SIGNED (COO), pending the CTO half
