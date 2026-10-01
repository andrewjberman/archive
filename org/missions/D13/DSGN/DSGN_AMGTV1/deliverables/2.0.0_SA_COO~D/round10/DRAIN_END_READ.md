# DSGN_AMGTV1 -- ROUND 10 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`. **Round:** 10, the round-9 analysis's enrichment list @d229d699f3
items 1-4 with rulings 1-3. **Decomposition:** v10 (issuance @35704a8693) + AMENDMENT 1 (@c13bb7407f). **Close record:**
`ROUND10_CLOSE_WALK.md`.

## 1. Orders -- 4 of 4 terminal, every instance VALID

| order | slot | portal -> DEV | CLOUD merge | mechanical criteria (my re-run) |
|---|---|---|---|---|
| AV-o-4 never scale an unresolved unit | ~38 | fb107b9a -> 7950eadd | df292d6c3f | units 3/3 (3/3); Q4 3/3 |
| AV-o-3 the team's cases, Opal's rule cases labelled | ~37 | cb14d218 -> aada32c8 | 1034ca3252 | cases 3/3 (3/3); Q3 3/3 |
| AV-o-2 the dossier on the page | ~36 | 5a2f0cbc -> 0373aa18 | 747bb50ab7 | dossier 4/4 (4/4); Q2 8/8 |
| AV-o-1 one house date form (QUEUED behind the three) | ~39 | 9f261553 -> 5810586a | a43730e29f | dates 3/3, 0 visible ISO over 45 surfaces (3/3); Q1 16/16 |
| AV-o-3 AMENDMENT 1 (byte repair) | ~37 | d11747a7 -> 2bb60cc3 | 4813813e75 | bytes 3/3 (3/3); cases 3/3; Q3 3/3 (two re-runs) |

- **Portal:** DEV (site-Z local, unpushed) went b6634ba0 -> 2bb60cc3, with `tsc -b` rc=0 after every portal merge.
- **Merges:** every merge read "dropped 0, foreign 0".
- **o-1's queued base:** re-dry-run on 0373aa18 before its slot was provisioned (dates 1/3 FAIL as expected; Q1 16/16).
- **o-1's grants:** the six granted harness changes were used as named, with no other re-anchor.

## 2. The one real run -- walks I and J

- **Walk I** (DEV 5810586a) was VALID. It found three literal 0x08 bytes where regexes meant `\b` (row Z-S5):
  - AZN's rule label read "Opal's opal's";
  - no description source has named Bloomberg since round 1.
- **The repair:** a new order file was refused by to-pipeline-gate LIMB 6, so AV-o-3 was re-opened as AMENDMENT 1 with AC4
  `bytes.cjs`. It drained, and row Z-S6 resolves Z-S5.
- **Walk J** (DEV 2bb60cc3) was VALID with a proven disarm, 0 guard aborts, and 1 API 500 on another page's route. It shows:
  - long-form dates across the page;
  - IMB's pillars, fund of record and last stated position, and TSM's "No fund of record is stated";
  - AZN's team Base / Upside / Downside with "Opal's ..." rule lines, once each;
  - TSM's EV "TWD 71,993,494.73 (unit not resolved)" beside AZN's measured "USD 281B".
- **6501 never opened on walk I** (only `/peers` was requested), so TSM stood in as the planted name on walk J.
- **L8:** the JUDGMENT criteria (4: o-1 AC3, o-2 AC3, o-3 AC3, o-4 AC3) go to `3.0.0_SA_CVO~Z` in the L8 packet.

## 3. The channel -- 23 rows (round 10 added 2)

- **Z-S5** (BLOCKING, ARMED; the 0x08 bytes) is resolved by the issuer's **Z-S6**.
- A check blind spot is named: cases.cjs arm 2 asked only that a line START with "Opal's". `bytes.cjs` stays in round 10's checks.

## 4. Round-11 inputs (the enrichment list is yours)

1. **FWD-11, machine words still on the face:**
   - the Posture tab: "no pack for IMB_LN_Equity is carried in packs on this object";
   - the timeline's never-collected state: "No chatter_daily rows exist for this security_key yet";
   - two currencies on one header (TSM: Price USD, EV TWD, as served).
2. **Andrew-direct (COO~H msg 26928):** "a mentions counter wherever articles are displayed so that its clear at quick glance".
   The day list shows "named N times" since round 9; a quick-glance counter (a badge) is a candidate cell. Andrew picks up with
   this seat directly.
3. **The timeline's "searched" rule:**
   - Andrew asked how a day counts as searched. It needs all 5 enabled publishers' listing spans to reach it, so 992 HK reads 271
     of 272 days "not searched".
   - This seat offered to route a per-name publisher denominator to AMGT_HARVST, held for Andrew's word.
   - The page's publisher name map covers only Seeking Alpha and WSJ, not Barron's, Bloomberg or FT: a page cell.
4. **6501 JP never opened on the walk** (search pick or ticker resolution, unproven).
5. **Carried:** FWD-2 names on 7 of 22 rows and the driver series (AMGT_RESAPP r51); the `/timeline/day` latency (HARVST n-6).

## 5. Held for Andrew

Worker worktrees `/c/tmp/wk-dsgn-amgtv1-{18..39}` and the scratch roots `C:/tmp/cood-r{7,8,9,10a,10b,10c}-root` are all merged or
scratch. Removing them is a recursive delete; his word (~20:2xZ) covered 9-17 only. Every branch is kept.
