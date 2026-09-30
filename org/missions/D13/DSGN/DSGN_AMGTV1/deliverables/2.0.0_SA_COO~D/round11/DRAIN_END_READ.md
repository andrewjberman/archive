# DSGN_AMGTV1 -- ROUND 11 DRAIN-END READ (the COO's one message of the round)

**From:** `2.0.0_SA_COO~D` (site Z) **to** `1.0.0_SA_CTO~Z`.
**Round:** 11, the round-10 analysis's enrichment list with rulings 1, 3 and 4 and cell 4.
**Decomposition:** v11, issuance @eacffcbd94, 6 cells in 5 chains (n-5 -> n-6 on ~44).
**Close record:** `ROUND11_CLOSE_WALK.md`.

## 1. Orders -- 6 of 6 terminal, every instance VALID

| order | slot | portal -> DEV | CLOUD merge | mechanical criteria (my re-run) |
|---|---|---|---|---|
| AV-n-1 the qualifier leads an unresolved figure | ~40 | 3ad73a54 -> 5437b4fb | a18ba3453d | unitlead 3/3; Q1 3/3; bytes 3/3 |
| AV-n-2 evidence wording names the filing evidence | ~41 | 52081c8a -> 3ce95031 | d902994339 | evidence 3/3; Q2 4/4; bytes 3/3 |
| AV-n-3 a not-searched day says how its articles were found | ~42 | f57796d1 -> f3827581 | b7b1c16c65 | denied 3/3; Q3 4/4; bytes 3/3 |
| AV-n-4 the walker waits for the load state | ~43 | (walker only) | 5f1750bfa6 | loadstate 3/3; walkerbound 3/3; walkvoid YES |
| AV-n-5 versions and what moved | ~44 | 7ed3ddcf -> 846ecc6c | ec95fde52a | versions 3/3; Q5 4/4; bytes 3/3 |
| AV-n-6 where each input came from | ~44 | 63bcc1eb -> 846ecc6c | ec95fde52a | ledger 3/3; Q6 4/4; bytes 3/3; versions still 3/3 |

- **Portal:** site-Z DEV (local, unpushed) went 2bb60cc3 -> 846ecc6c, with `tsc -b` rc=0 after every portal merge.
- **Merges:** every merge read "dropped 0, foreign 0".
- **Harness grants:** n-5 and n-6 each used exactly the two granted stub lines; there were no other re-anchors.
- **Check fix:** a check defect, a 0x08 byte in census.cjs present since round 6, was fixed in the round-11 copy at the cut.

## 2. The one real run -- walk K

- **Build:** 5174 @4e4307be (contains DEV 846ecc6c, 0-line diff). The signed-out control read YES first.
- **Walk K was VALID:** 432 shots, disarm proven, 0 guard aborts, 0 API issues.
- **Load states:** 54 of 54 read `loaded`, the longest wait 3,609 ms. 6501 JP opened fully for the first time.
- **Every order is visible on the running page** (details in the close record):
  - TSM's EV reads "unit not resolved -- raw figure ... (TWD)";
  - IMB's Posture reads "Filing evidence, each side";
  - BA 09-08 reads "not searched for this company directly -- 5 articles found in other searches";
  - 6501's Thesis reads "no research dossier for this name";
  - BA's Model tab shows the 14 versions, the 212/0/7/172 compare and the 6-class ledger.
- **n-3's planted day changed under the page:** 992 HK 2026-08-13 is now served PARTIAL. BA exercised the DENIED wording instead.
- **L8:** the six JUDGMENT criteria (n-1..n-6 AC4) go to `3.0.0_SA_CVO~Z` in the L8 packet.

## 3. The channel

- Round 11 added 0 rows.
- `comp-surprise --project DSGN_AMGTV1` reads 23 investigation rows and 13 adjudication rows.
- Its "armed 6" is each row's FILED standing. On the latest dispositions:
  - all 7 ARMED-standing rows and all 8 BLOCKING rows are GRADUATED or DISMISSED (0 undispositioned);
  - 5 rows remain UNDER_INVESTIGATION: Z-C-S12, Z-W5-S1, Z-W8-S1, Z-W11-S1 and Z-S2. All 5 are OBSERVATION and INERT, and none
    blocks the L10 slug.

## 4. Round-12 inputs (the enrichment list is yours; PRD v0.4 @03912f9462 adds FWD-12..20, FWD-20 ui-smoke first)

1. **The versions picker repeats a label when several versions land on one day.** BA shows "September 10th, 2026" x4; the
   walker's duplicate-options check hit 4 names. The served stamp carries the time.
2. **What-moved and rule lines print raw floats:**
   - "193510.78009600003 to 187187.819936";
   - "1.350954532623291";
   - "-0.8280000000000001";
   - SHORT_INT_RATIO reads "a line this page has no name for yet".
3. **FWD-11, machine words still on the face (carried):** "No chatter_daily rows exist for this security_key yet" on a
   never-collected timeline.
4. **Posture wording at zero:**
   - "a comparable the research team has not identified (comparable): ...";
   - "0 of the 0 citations can be shown ...".
5. **The publisher name map (carried):** "a publisher this page has no name for yet" on 992 HK's partial day.
6. **FWD-12's re-run** needs a served route before any page cell can build it.
7. **Carried:**
   - FWD-2 names on 7 of 22 rows and the driver series (AMGT_RESAPP r51);
   - `/timeline/day` latency (HARVST n-6);
   - Andrew-direct via COO~H msg 26928, a mention counter.

## 5. Held for Andrew

- **Worktree removal:** worker worktrees `/c/tmp/wk-dsgn-amgtv1-{18..44}` and the scratch roots
  `C:/tmp/cood-r{7,8,9,10a,10b,10c,11a,11b}-root` are all merged or scratch. Removing them is a recursive delete, and his word
  covered 9-17 only.
- **Coverage-rule ask:** routing the per-name publisher denominator to AMGT_HARVST waits for his word.
