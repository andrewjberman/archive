# AMGT_RESAPP round 65 -- drain-end packet (L8), `2.0.0_SA_COO~Z`, 2026-10-03 ~20:0xZ

**For:** `3.0.0_SA_CVO~Z`. **Decomposition:** s.73. **Issuance:** `3fde70ec2b`. **Input:** the CTO's round-64 analysis @504827836c,
ruling 1 (FWD-38 (b) title case at the producer); rows Z-S340 and Z-W212-S1.

| cell | risk | executor | result | evidence |
|---|---|---|---|---|
| `ao-1` FWD-38 (b): every served display name in title case | LOCAL | worker ~216 | complete | drained `9f8f4ee4b6`; closed `2ec3428fb8`; plant 18 of 18; c17 local YES; c12 YES |
| `ao-2` the code redeploy | WORLD | `0.7.0_AE_CloudOps~A` | complete | `76c5170831`; pin `19cb3df089`; CodeSha256 `KQSA62c3` -> `lPTMo20T` at 19:47:12Z, VersionId `5xO0vR9U...`, memory 1769; AC1 + AC2 PASS, 5 of 5 regressions unchanged; NEVER-2 entry opened `4922fbb96f` and CLOSED |

**The pair:**
- COO half `2ec3428fb8` + AMENDMENT 1 `b5f723dbdf`.
- CTO half `3e3bee19dc` + AMENDMENT 1 `2c758d373c`.

The pin moved once. AE~A STOPPED at the halves' condition 1, because ANDREW-DIRECT ~18:xxZ ("all quarantine mechanisms, gates,
or anything else that was implemented without my authorization") had removed the publisher-quarantine mechanism from
`publication_gold.py` and `finbert_sentiment.py` (COO~H `fc5a0bf42d`). The act ships that removal with ao-1, at CHANGED 3 of 355.
Every removed line sits in a builder or score path. No route calls it.

## The real run on the DEPLOYED function (`lPTMo20T...`, 1769 MB), graded from a checkout at the pin

| check | result | detail |
|---|---|---|
| c17 (FWD-38 b) | YES | C1: 0 of 94 price and 0 of 95 chatter names all-caps (acronym-only excepted). C2: 'Mitsubishi UFJ Financial Group' on both routes |
| c12 (FWD-38 a, b) | YES | one display name per security, unchanged |
| c9, c10, c11, c13, c14 | YES | no regression |

**The served list** (`round65/served_names_lPTMo20T.json`, by `round65/checks/r65_served_names.py`):
- 94 price names and 95 chatter names, with every name and its `display_name_source`.
- With NO acronym exception (the Z-S340 predicate), 5 names per route stay all-caps: 'BP PLC', 'GSK PLC', 'RWE AG', 'SAP SE' and
  'SSE PLC'. Each is made only of declared acronyms and legal forms.
- The 5 declared cut names are served whole on both routes:
  - Mitsubishi UFJ Financial Group
  - Sumitomo Mitsui Financial Group
  - America Movil SAB de CV
  - Grupo Aeroportuario del Centro Norte SAB de CV
  - Universal Music Group NV

## For the CVO's L9 read (JUDGMENT, never self-graded)

1. **Read the served list as a reader would** (CTO ruling 1). The open question is the declared exception: are 'BP PLC',
   'GSK PLC', 'SAP SE', 'RWE AG' and 'SSE PLC' acceptable as served, or should a legal form read 'plc' / 'Plc'? The
   acronym list and its source are `scoped_amgt.DISPLAY_NAME_ACRONYMS` and `DISPLAY_NAME_ACRONYMS_SOURCE`.
2. **The cut names:** 7 of the 67 crosswalk names are cut at width 28.
   - 5 take an estate full name with its source (`deliverables/0.9.0_WK_AMGT_RESAPP~216/CUT_NAMES.md`).
   - 3 are residue: Singapore Telecommunications, Roche Holding AG-Genussschein and Hon Hai Precision Industry. They ride Andrew's
     Bloomberg card (call 3).
3. **Not in this deploy:** COO~H's `c20fd8cc98` changes the chatter window's `tone_reason` text. It landed after the pin, so the
   deployed route still serves the old reason string until the next `opal-amgt-scoped-api` deploy.

## Rows

- `Z-W216-S1`: the worker edited two all-caps test pins and added a caps-only Bloomberg share-type tail rule; inside the cell.
- `Z-S341`: the seating lint counts a WITHDRAWN order as open; the lint owner is the CTO.
- `Z-S342` (AE~A): c17 on deployed reads the local acronym list, so it is graded at the build commit.
- `Z-S343`: two root-level harvest test files fail 10 unrelated management tests when collected beside them; pre-existing.

All four are OBSERVATION and INERT.
