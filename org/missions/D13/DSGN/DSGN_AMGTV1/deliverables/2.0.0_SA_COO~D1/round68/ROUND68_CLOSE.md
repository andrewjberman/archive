# DSGN_AMGTV1 round 68 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~16:5xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round67.md` @a06920d917 section 2. Item 1 is AV-zzs-1. Item 2's producer row was already filed as `AMGT_RESAPP-D1-S14` @d30938fb2d. Item 3 is this walk. |
| issuance | @41990c51cc, fan-out 1 of 1, LF only |
| order | `TO-AV-zzs-1` -> ~142 (worker-light), in three builds. **Build 1** (portal 2be8455f, drained @8c490609cd): the subject Price/Mkt Cap/EV print the header's figure or "--", never the peer set's own value. **AMENDMENT 1** @60cdc530a2 (portal 3278da53, drained @b31bf939ab): the close walk at 16:07Z showed that 992 HK's 60.91B was the HEADER's own CURR_ENTP_VAL, served with an UNMEASURED `currency_basis`. The tile withholds it (CRPS-ao-3, FWD-20), and the row now applies the same rule. The issuer ruled this; the CTO confirmed it in msg 2816, where FWD-20 stands. **AMENDMENT 2** @42b528e904 (portal c96efe17, drained @4278570107): the withheld row cell carries the tile's own reason as its hover. There is one copy of the words, `CURRENCY_UNCONFIRMED_WORDS` in StatTile.tsx, which the tile and the row share. |
| checks on both candidates | r62 6/6, r63a 3/3, r63b 5/5, r63c 5/5, r64a 4/4, r65 4/4, r67 6/6, r68 7/7; battery29 ALL PASS (0 skipped) |
| DEV | candidate `c96efe17` = origin DEV `32835ce5` + 2be8455f + 3278da53 + c96efe17, a fast-forward (`cand/dsgn-amgtv1-r68-dev`) |
| PROD | candidate `37aa1247` = PROD `18364342` (portal-v2.1.210) + rounds 67-68 (11db6620, a97e5dff, 44d2d022, e88ced18, 37aa1247) on `cand/prod-dsgn-r68`. It changes 7 files, 0 of them outside `src/pages/SecurityAnalysis/`, and its SA tree equals the DEV candidate's (empty diff). It carries rounds 66-68; round 66 had no portal change. No PROD half is asked until the CVO grades. |
| rows | none new. Producer rows S14-S16 (round 67) stand. |

## The real run -- 16:40Z-16:44Z, `tmp/ui-walk/20261009T164047Z`, signed-in `dev:live` build of `c96efe17`

`--security 992_HK_Equity --security ASML_NA_Equity`: 62 screenshots, 0 API issues, 0 guard aborts. The walker disarmed, and its login
is refused (401). An attempt at 16:38Z was void: the dev server was down, and no page was read.

| criterion | shot | what it shows |
|---|---|---|
| FWD-27, 992 HK (the open item) | 011 | The Enterprise Value tile reads "--", and the Peers subject row's EV reads "--". Before this round it read "60.91B currency not stated". Price reads HKD 32.84 in the tile and the row, and Mkt Cap reads "HKD 421B, as of October 9th, 2026" in both. |
| FWD-27, negative arm (measured EV) | 042 | ASML's EV reads "EUR 626B" in the tile and the subject row. Price reads EUR 1,626.20 in both, and Mkt Cap reads "EUR 631B, as of October 9th, 2026" in both. |
| the same reason | r68 arm 6, real render | A screenshot cannot show hover text. On the real PeersTab render, a withheld subject EV cell carries the title "Bloomberg does not confirm this figure's currency": the tile's own words, read from the page's one copy. A shown EV cell carries none. |
| `TO-AV-zzs-1` AC3 | 011, 042 | As above. |

## Carried

- The peer price cells reading "currency not stated" are producer row S14's. They are not this round's.
- The summary rows: Price is blank on Average and "--" on Median, Min and Max. The footnote explains the Average.
- `round64/PREP.md` items 1-3.
