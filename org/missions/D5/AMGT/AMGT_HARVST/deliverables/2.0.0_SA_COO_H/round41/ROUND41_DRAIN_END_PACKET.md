# AMGT_HARVST -- ROUND 41 DRAIN-END PACKET (L8 input), `2.0.0_SA_COO~H`, 2026-10-03 ~23:2xZ

**Round:** Andrew-direct ~20:3xZ card 2, "yes to all recommendations"
(`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261003_20xxZ_YES_TO_ALL_SEVEN_OPEN_CALL_RECS.md` @9fe6e6f111):
"run FinBERT scoring over the stored articles, and the event rebuild". Decomposition section 54 (issued @740c25f399).
Three issuer direct acts, one chain. **Class: SERVED.** No collection ran (0 collectors; Scheduled Task Disabled; STOP_FT
unchanged).

## 1. The cells

| cell | result | evidence |
|---|---|---|
| `HVST-an-1` FinBERT scoring | **DONE.** 5 `article_sentiment` parts, 13,235 rows = 13,224 scored + 11 no-text markers, 0 errors. After: `already_scored` 13,224, `would_score` 0. Lambda `opal-news-ai-sentiment` only. | `round41/an-1.batch01-05.out`, `an-1.after_dryrun.out` |
| `HVST-an-2` served tone rebuild (FWD-16) | **SERVED.** Pair: COO @72f2c9be42 + CTO @8e0fed682a. Gate HOLDS, VERIFY on the written parts HOLDS. Mention 23,691 -> 31,042: gone 0, changed (pre-existing) 0, added 7,351 (sa +7,043, bbg +308, signed knowingly). All 31,042 rows carry FinBERT tone: positive 12,117, negative 10,034, neutral 8,891; join mismatch 0. Daily 58,300 -> 58,512: gone 0, OTHER 0. | `round41/gold_tone_act_20261003T220422Z.json` (parts `article_security_mention/.../part-20261003T222707Z`, `chatter_daily/.../part-20261003T224754Z`) |
| `HVST-an-3` served event rebuild (FWD-6) | **SERVED.** Pair: COO @72f2c9be42 + CTO @8e0fed682a. Gate HOLDS over the new mention (31,042 rows); VERIFY on the written part HOLDS, and its digest equals the gate's. Events 8 (6 securities) -> **507 (68 securities)**: duplicate 0, out of universe 0, orphan 0, lead rule 0, headline mismatch 0, headline null 0. | `round41/gold_event_act_20261003T225425Z.json` |

## 2. The CTO halves' post-act conditions

- **an-2 (both PASS):** RESAPP chatter serves `tone` null with a reason on all 95 rows. BA's day view on 2026-09-29 (its busiest
  day) serves 9 articles, equal to its 9 gold mention rows. Record: `round41/post_act_an-2_20261003T225305Z.json`.
- **an-3 ran only after an-2's read.**
- **an-3 (PASS):** the RESAPP timeline on BA serves 12 events with 12 coverage markers. Every marker's day opens (0 empty days).
  AMD and VLO serve 0 events, which equals gold. Their tier-A articles all come from ONE publisher (sa: AMD 45, VLO 37), and the
  rule needs 2 tier-A publishers, so 0 is the rule's answer, not a route gap. Record: `round41/post_act_an-3_20261003T231542Z.json`.
- **The 4 dropped event_ids (all RE-FORMED, none lost):** the event_id hashes (security, first_day, last_day, lead), and the
  rebuilt mention table adds members to each story (`round41/dropped_events.json`):
  - `c6406ab65afa` 992_HK 2026-02-12 -> `f4c762001c3f` (lead changed; +1 member)
  - `df65e860ac9b` 992_HK 2026-05-22 -> `fdc313bf8ec4` (lead changed; +1)
  - `db2286aabb9f` AMZN 2026-09-06..07 -> `cdf28fcf57d6` (last_day changed; +2)
  - `3edd30795cb9` HD 2026-08-17..18 -> `d19774c1e1a8` (lead changed; +6)

## 3. For the CVO

- **Judgment to grade on the served artifacts:** are 507 events a faithful set of news stories (FWD-6, "bursts of real coverage
  appear as marked events with a headline")? Is the FinBERT tone on the gold mention rows the scorer's own output (FWD-16)?
- **Not served yet, stated so it is not read as done:** RESAPP's chatter route still serves `tone` null. Its reason text is the
  pre-deletion wording until the next opal-amgt-scoped-api deploy carries c20fd8cc98. FWD-17 (window tone, `chatter_window`)
  was not built: card 2 named scoring and the event rebuild only.
- **Surprise rows this round:** none filed. One observation, carried here: a security whose tier-A coverage is single-publisher
  gets no events under the 2-publisher rule (AMD, VLO).

Push: LOCAL.
