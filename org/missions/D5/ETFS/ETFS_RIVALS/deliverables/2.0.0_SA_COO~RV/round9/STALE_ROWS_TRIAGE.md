# ETFS_RIVALS -- triage of the 8 stale OPEN remediation rows (round-8 analysis item 8)

**Author:** `2.0.0_SA_COO~RV`, 2026-10-05 ~17:0xZ. **Instrument:** `.tools/comp-surprise.py --project ETFS_RIVALS --json` at CLOUD
HEAD: 35 remediation rows, 13 with `closed: false`; 5 are round-8 rows carried by round 9 (Z-S24, Z-S25, Z-S29, Z-C-S35, Z-C-S36);
the other 8 are triaged here, each against the world at HEAD (not against its own text).

| row | remedy (short) | measured at HEAD | triage |
|---|---|---|---|
| Z-W3-S11 | DVD_CRNCY in the pull-enrichment request; G5 drops the suffix heuristic | `enrichment_bloomberg.py:80` `CCY_FIELD = "DVD_CRNCY"` requested beside DVD_HIST_ALL (plan fields `:11`); `gold_trade_schedule.py:170` takes the G3 `currency` first, labelled "g3" | **REMEDIATED in code** -- close candidate for the CVO (the record cites the two lines) |
| Z-S14 | G4 history lands px_close / total_return_index; rankings use g4 first | served 10-05 holding_contribution (rv-publish-1005r8b): g4_tri 973, mixed 2,023, holding_implied 320, missing 46 security rows (was 0 g4 rows at 10-01); G4 holds 3 dates (09-29, 10-01, 10-02) | **PARTIAL** -- the rankings now price from G4 where it exists; the history depth rides round 9's `RIV-cb-1` capacity budget and the G4 history pull it allows. Keep open, re-pointed to cb-1 |
| Z-S13 | per-fund issuer floors {BASG, GQGU} = round_down_2dp(resolved fraction - 2/n) | `guardrails_config.json` thresholds.min_resolved_fraction.value.issuer = 0.23 (a scalar; last change 3c7177004e, round 6) | **OWED** -- a config change under a never-widen pair; proposed as round 9's batched repair cell |
| Z-W3-S12 | a child-identity source for spinoff / rights / warrant actions | no failure measured on the served page since the row; G3 carries DVD_HIST_ALL types only | **PARK** -- owner 1.0.0_SA_CTO~Z; un-park condition: a spinoff, rights or warrant action on a universe security inside a page window |
| Z-W5-S3 | the gateway stack's fresh-tree plan reproducible | not an ETFS_RIVALS write surface (gateway stack) | **RE-HOME** to the gateway stack's owner channel; nothing in round 9 |
| Z-W5-S7 | the naming gate: carve-out for package-relative paths or keep the refusal | not an ETFS_RIVALS write surface (`.tools` naming gate) | **RE-HOME** to the gate owner (1.0.0_SA_CTO) |
| Z-W5-S14 | the wrapper's manifest write preserves unrelated entries byte for byte | not an ETFS_RIVALS write surface (the wrapper tool) | **RE-HOME** to the wrapper's owner |
| Z-S7 | fix the resolver in to-decomp-ref-lint.py / to-check.py before the seating limb enforces | not an ETFS_RIVALS write surface (`.tools`) | **RE-HOME** to the tool owner (1.0.0_SA_CTO) |

Net for round 9: 1 close candidate (W3-S11), 1 re-point (S14 -> cb-1), 1 repair cell (S13), 1 park with a condition (W3-S12),
4 re-homes outside the project. The disposition of each REMEDIATION row stays the CVO's; this file is the issuer's evidence.
