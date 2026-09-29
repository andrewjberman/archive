# AMGT_RESAPP round 49 -- drain-end packet (L7 -> L8/L9, `3.0.0_SA_CVO~Z`)

Issuer: `2.0.0_SA_COO~Z`. Decomposition s.57, issuance `ed65d1afec`, on the CTO's round-48 analysis `1dfd5c0970`. Four orders,
all terminal. Push state: LOCAL.

## 1. The orders

| cell | risk | holder | close | result |
|---|---|---|---|---|
| xx-1 FWD-30's one grader keys on the page's data attributes and names CASES | LOCAL | ~173 | drain `525e045932` (worker flipped, all PASS) | AC1 3 of 3 equal on attributes; AC2 the reason names the class (4 of 4 pairs); AC3 wording plant EQUAL / attribute plant DIFFER; issuer re-ran all three on the merged tree; VALID |
| xx-2 the rank-history series carry the served name | SERVED | ~174 | drain `209a6cce2f`, close `51d5709d24` | AC1 series name SERVED 2 of 2 held, unheld ABSENT; AC2 329 passed; issuer re-ran both merged; VALID |
| xx-3 officers from the proxy (DEF 14A) | LOCAL | ~175 (spawned on R-21, amendment `e2d8d8927f`) | drain `c1222c3cdf` (worker flipped, all PASS) | AC1 INTU 5 officers, DEF 14A 000089687825000057, 0 malformed; AC2 identified 96, pointer 2, gained 2 of 2 (HAL, INTU); 6 offline tests; issuer re-ran merged (EDGAR through fetch.py only); VALID |
| xx-4 the redeploy carrying the series name | WORLD | `0.7.0_AE_CloudOps~A` | flip at this commit | COO half `4603244135`, CTO half `8f7237f20f`; entry CLOSED 3 of 3 22:32:47Z; plan 0/1/0 code only; closure ONE file (scoped_amgt.py); AC1 (AMENDMENT 1 `b42686c15b`) issuer-re-measured `Um3BOJ+j...p7A=`; AC2 issuer-re-run on the served plane; AC3 no-regression; limbs 4/5/6 hold; VALID |

Worktrees `C:/tmp/r49-173`, `-174`, `-175`: branches merged, checkouts KEPT pending Andrew's go on checkout removal (post-crash edict).

## 2. THE RESULT

- **FWD-30 has one grader keyed on the page's data, not its wording** (CTO ruling 1). Issuer's real run, the full `--served --live
  --require-cases` sweep, read_at 22:21:04Z: **equal 95 of 96 identified names; unidentified 0 of 96** (round 48 close: 62 of 96 on
  wording). The sole NOT_OK is `6501_JP_Equity` (Hitachi, identified today by AMGT_CORPUS round 15): the deployed export refuses it
  for want of a model block (row Z-W173-S5). `round49/captures/fwd30_sweep_20260929T222104Z.{tsv,summary.txt}`.
- **The rank-history series serve the company name** (DSGN FWD-3 labels). Real run on the deployed function `Um3BOJ+j...`:
  BA US "The Boeing Co" SERVED (12 points), HD US "The Home Depot Inc" SERVED (11), the control ABSENT (0).
  `round49/captures/timeseries_trending_chatter_20260929T224246Z.json`. The page already labels a line with `series.name`.
- **Officers from the proxy, built not served** (DSGN FWD-7, LOCAL first cut): both names whose annual report points elsewhere gain
  a list of 5. Serving is round 50's, under a pair.

## 3. Judgment criteria

None this round. What the CVO may weigh:
- **The grade is looser on VALUES than the harness it replaced.** The page carries no attribute for a figure's value, the identity
  line, three absence reasons, a case's value or the driver chart (rows Z-W173-S1..S4), so those facts are matched on identity, not
  value. Asked of 2.0.0_SA_COO~D for DSGN_AMGTV1's next round (22:21Z), per ruling 1.
- **AC3's planted element is empty text** (worker caveat); the worker also rewrote every visible text node on ASML and BABA with the
  facts unchanged.

## 4. Rows this round (L8 input)

- **Z-W173-S1..S4** (~173, OBSERVATION/INERT): facts with no page attribute, graded on identity alone (above).
- **Z-W173-S5** (~173, OBSERVATION/INERT): Hitachi resolves now but the deployed export refuses it; FWD-30 95 of 96.
- **Z-W175-S1** (~175, OBSERVATION/INERT): the proxy serves the NAMED executive officers, a subset of the roster; the serving round
  decides the label.
- **Not a row, recorded here:** xx-4 AC1 as cut was VACUOUS at base -- my dry-run preceded AMGT_HARVST HVST-i-4's apply, which moved
  the base the check named. Caught by the executor pre-apply (msg 26747), amended `b42686c15b`, exercised both ways.
- **Correction to Z-S305** (s.57b.1): with `--served` the export side IS the deployed body; the CVO's v58 controlled run carries the
  attribution.

## 5. Carried to the CTO's round-49 analysis

1. **The page attributes FWD-30 lacks** (Z-W173-S1..S4) -- asked of DSGN_AMGTV1; until they land FWD-30 is equal-on-identity for
   figure values.
2. **Hitachi's model block** (Z-W173-S5) -- the 96th name is identified but has no landed block; the owner of the block (AMGT_CORPUS /
   the Bloomberg pull) decides.
3. **Serving xx-3's officers** under a pair, and the NEO label (Z-W175-S1).
4. **The "Historical-multiple reference" names its owner** -- carried to round 50 by the CTO (msg 26738).
5. **Deploy queueing on one function:** three projects redeployed `opal-amgt-scoped-api` within 90 minutes (ww-1, HVST-i-4, xx-4). Each
   half read the other open entries by hand; a check at the cut that the base it names is still live would have caught xx-4 AC1.
