# DSGN_AMGTV1 -- ROUND 8 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`. **Round:** 8, the round-7 analysis's enrichment list
@0c498ee766 items 1, 4 and 5. **Decomposition:** v8 (issuance @b8e3ec6f5d). **Close record:** `ROUND8_CLOSE_WALK.md`.

## 1. Orders -- 3 of 3 terminal, every instance VALID

| order | slot | portal -> DEV | CLOUD merge | mechanical criteria (my re-run) |
|---|---|---|---|---|
| AV-q-1 the walker waits for the day state | ~29 | none | ac0fdbfc16 | daystate 3/3 (3/3); walkerbound 3/3 (3/3); signed-out control YES |
| AV-q-3 classification labels per Positioning | ~31 | 761deafa -> c151bbef | 47f7517018 | labels 3/3 (3/3); Q3 5/5; round-7 columns 3/3 |
| AV-q-2 the lead source line in the footer form | ~30 | fac7c101 -> 29c8226a | e148b35d27 | sourceline 3/3, census 18 of 18 footers (3/3); Q2 5/5 |

- **Portal:** DEV (site-Z local, unpushed) went ab7e1e49 -> 29c8226a, with `tsc -b` rc=0 after each portal merge.
- **Merges:** every merge read "dropped 0, foreign 0".
- **Order hygiene:** all 3 workers flipped their own orders. No amendment was cut and no row was filed this round.

## 2. The one real run -- the day's articles are on pixels

- **The walk:** signed-out control YES, then walk G on 5174 @fa5ba517 (which contains 29c8226a). It read "walk void: no", 0
  API issues, and a proven disarm.
- **`timeline-days.json`:** it records every opened day with its state:
  - 992 HK 2026-08-13 read `rows` after 5,309 ms;
  - the event's day 2026-02-12 read `rows` after 5,577 ms;
  - four newest days read `empty` at about 1.6-1.9 s;
  - no day hit the ceiling.
- **The shots show the articles:** two per day, under "STRONGEST FIRST".
- **L8:** the JUDGMENT criteria (q-1 AC4, q-2 AC3, q-3 AC4) go to `3.0.0_SA_CVO~Z` in the L8 packet.

## 3. The channel -- 21 rows (round 8 added none)

Carried ARMED: round 1's W2-S1 / W3-S1 / W3-S2 and W4-S1 (b) (AMGT_RESAPP's).

## 4. Round-9 inputs (the enrichment list is yours; close record "Seen on the walk")

1. **FWD-2, the label/domain split:**
   - The lead list's "Sub Asset" column now carries Positioning's heading, but its values are sector names ("Energy",
     "Information Technology").
   - Positioning's values under the same heading are sub-asset buckets ("Ultra Short Duration", "High Yield", "Large").
   - The asset-class value's case differs ("equity" against "Fixed Income").
   - This is the round-7 analysis's ruling 5 met on the header and missed on the domain.
2. **FWD-5, ordering:**
   - Both days show two rows with equal visible marks (A, in headline yes, in lead yes).
   - The rows run earliest first on 08-13 and latest first on 02-12, so "strongest first" has no visible tie-break.
3. **FWD-11, form residuals:**
   - raw ISO article times with "(instant)";
   - "Dated" as a prefix only on the lead line;
   - the lead list's system-voice line about the date;
   - the Positioning model window's footer has no source;
   - one truncated Sub Asset cell;
   - BP/ LN with no name and "--".
4. **Carried:** FWD-2 names 7 of 22 rows (AMGT_RESAPP); the /timeline/day latency (~5.5 s) was routed to 2.0.0_SA_COO~H.

## 5. Held for Andrew

Worker worktrees `/c/tmp/wk-dsgn-amgtv1-{18..31}` and the scratch portal worktrees `C:/tmp/cood-r7-root/portal` and
`C:/tmp/cood-r8-root/portal` are all merged or scratch. Removing them is a recursive delete; his word (~20:2xZ) covered 9-17
only. Every branch is kept.
