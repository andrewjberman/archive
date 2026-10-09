# NFRA_CTLPLN workstream INBOUND (macro COMM) -- round 7 drain-end read, and the reviewer packet for rounds 6 and 7 (2.0.0_SA_COO~R, 2026-10-08 ~23:0xZ)

Round 7 was cut on `1.0.0_SA_CTO` msg 107329 ruling (3) (decomposition `decompositions/NFRA_CTLPLN_DECOMP.inbound7.md`, issuance
`c54bf92186`, merged `537ac6650f`; AMENDMENT 1 `159dad0a43` on Andrew-direct ~21:4xZ, the Kimi token budget). Its one order is
terminal (`complete`). Round 6's drain-end is `INBOUND_ROUND6_DRAIN_END_20261008.md` (`03d37ff43f`). Push state: all on
`box/laptop`; CLOUD push state UNREAD by this seat.

## Round 7's cell, drained

| cell | what landed | merge | proof | issuer re-run |
|---|---|---|---|---|
| CT-i-13 | run-once keys unique per draft for the chat text, the chat send and the mail text (row S34; 3 of 12 `ctx.once` sites fixed, 9 audited unaffected); a refused End of Day draft restores its link line or texts the reason and keeps the open draft (row S33); quiet chat cursors pruned after 7 days; the Kimi call doubles its budget on a cut-off (cap 16000) and logs each attempt | `75420934c2` | VALID | `SILENT-PATHS ok=True arms=9/9 base_texts_second_draft=1`; `AGENT-SUITE ok=True` (127 + mail reply 9/9) |

Drain checks: `py_compile` and `ruff --target-version py39` clean on the three modules; the eight inbound scripts green.

## Deploys (both APPLIED, neither EXERCISED yet)

| round | order | live (CloudTrail) | live `CodeSha256`, read by the issuer | applier's report | halves |
|---|---|---|---|---|---|
| 6 | `NFRA_CTLPLN.TO-APPLY-19` | ingress 21:48:11Z, handler 21:48:17Z | `M67/KipojF79vIGJTxCmQnDQfVyzws1VGU4OsD+7Yt0=` | `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/teams_r6_20261008/REPORT.md` | COO `b07357fa48`, CTO `1dd8aa70e7` |
| 7 | `NFRA_CTLPLN.TO-APPLY-20` | ingress 22:31:55Z, handler 22:32:01Z | `xWURpe/nRkiZAc8Uui+arsJpSeVnUErNEHBWqtvrM5Q=` | `org/tier2_senior/0.7.0_AE_CloudOps/deliverables/teams_r7_20261008/REPORT.md` | COO `0a67682d62`, CTO `54a8846698` |

The round-6 first-hour count (CTO condition) was sent at 22:41Z: 1 chat event, 0 failed, 0 unexplained; too quiet to exercise.
The CTO set the EXERCISED read for 2026-10-09 ~22:00Z (msg 107436).

## Judgment criteria for `3.0.0_SA_CVO` (L9; none self-graded)

1. **CTi11-AC3** (round 6): `deliverables/0.9.0_WK_NFRA_CTLPLN~39/CHANNEL_READ_SCOPES_MEASURED.md`: does it name, from the code,
   the scopes requested and the scopes the three channel-read paths need, and which are missing?
2. **TO-APPLY-19 AC2**: is the round-6 deploy as both halves describe? Read the applier's report against the COO half's branch
   A and conditions 1-4.
3. **TO-APPLY-20 AC2**: the same, for round 7.

## Rows

S33 and S34 (ARMED, owner this seat) are disarmed in code by CT-i-13 and live since 22:32Z. Their EXERCISED read is the full-day
count on 2026-10-09. W41: none. Earlier: W38-S1 disarmed by W38-S3; W38-S2, W39-S1..S4 INERT.

## Still open

- The gateway's channel routes ship with NFRA_OPLGTW's release (site Z, routed by `1.0.0_SA_CTO`). Until then `channel_poll`
  reads `failed=1` a minute, as both halves accept.
- Item 5, mail into the same text path, waits on site Z's mail-domain admission. When it is cut, it is cut on clause 9 as written:
  Andrew-direct ~22:5xZ, "No it always has to say andrew in the body text somewhere, otherwise i dont care" (`c0a11edcc8`).
