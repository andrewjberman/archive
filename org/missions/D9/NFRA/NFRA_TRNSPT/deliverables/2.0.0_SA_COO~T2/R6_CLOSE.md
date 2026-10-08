# NFRA_TRNSPT round 6 -- close record (2.0.0_SA_COO~T2, dell2, 2026-10-08)

Issuance `66d4819a61` (decomposition `decompositions/NFRA_TRNSPT_DECOMP_R6.md`, CTO round-5 analysis @a8931c9d12). TR-f6 merged
`18b1a709ec` (AC1 `R6-F6-BUILD-OK rows=12 causes=5 series=4`, AC2 `R6-F6-TEST-OK passed=10`; drain re-run on the merged tree: 10 passed).

## E1 (TR-e-6, issuer) -- D2-S2 decided: listed, then not admitted; a RULE gap

Record `org/tier1_exec/2.0.0_SA_COO/deliverables/NFRA_TRNSPT_T2/R6_E1_RECLASSIFY_20260811.json` (flags, dates, types, sizes and file
extensions only; 0 `@` characters). The run record could not answer it (totals only; row NFRA_TRNSPT-D2-S3), so the issuer re-listed
2026-08-10..12 for the pull's own sender table through the gateway and ran `criterion.classify` exactly as the pull does.
- Listed: 6 messages over the 3 days, all `sender#2`; **2 on 2026-08-11**. Each: `sender_ok` TRUE, `ycharts_pdf` FALSE,
  `client_recipient` FALSE, `trade_update_excluded` FALSE -> `near_miss`, not admitted, not in bronze.
- Deciding test: `ycharts_pdf` (admission is `sender_ok AND ycharts_pdf AND NOT trade`, `criterion.py:173`). Each 08-11 message carries ONE
  non-inline attachment of ~13.5 MB, `contentType: application/octet-stream`, extension `.asc` (an ASCII-armored encrypted payload).
  The rule (`criterion.py:153-157`) accepts only `application/pdf` of >= 300,000 bytes, or body words.
- **Verdict: a RULE gap, not a data gap.** The author table admits the sender; the detection rule has no branch for an encrypted
  attachment. Whether such a message should be admitted (its payload is unreadable by silver) is a decision for the CTO, not a fix here.
- Gateway reads: three GET-only listings of the span (the classification, the attachment facts, the extensions), each in-process.

## E2 (TR-f-6) -- FWD-4's completeness record, live

Inputs `R6_COMPLETENESS_INPUTS_20261008.json`, record `R6_COMPLETENESS_RECORD_20261008.json` (this folder). As of 2026-10-08, 120 days.

| series | occurrences | here | not_allowlisted | never_recorded | refused | expired |
|---|---|---|---|---|---|---|
| monday_meeting | 17 | 12 | 1 | 4 | 0 | 0 |
| ocio_ic | 8 | 7 | 1 | 0 | 0 | 0 |
| asset_management_ic | 8 | 7 | 0 | 1 | 0 | 0 |
| research_meeting | unknown | -- | -- | -- | series refused | -- |

Criterion (1): 33 rows, each exactly one cause; counts per series sum to 33. Criterion (2), one occurrence per cause present, traced:
- `here`: asset_management_ic 2026-07-07 -> `s3://opal-data-transcripts/teams/transcripts/bronze/asset_management_ic/date=2026-07-07/...ICA-20260707-0958.vtt`.
- `not_allowlisted`: monday_meeting 2026-10-05 -> Microsoft lists a transcript created 2026-10-05T12:58:22Z (list_meeting_transcripts);
  not in bronze; the running gateway's allowlist is empty (row Z-W15-S30).
- `never_recorded`: asset_management_ic 2026-06-23 -> a calendar occurrence (calendarView chunk 2026-06-10+30d) with no transcript
  listed and none in bronze.
- `refused`: research_meeting at series level -> Graph 403 3003 on its transcript listing 2026-10-08; it is not on Andrew's calendar,
  so its occurrences are unknown and no per-date row exists. Stated in the record's `series_notes`.
- `expired`: none graded -- no dated evidence of an earlier listing is held (decomposition ruling 3; no retention figure guessed).

**Caveat for the analysis:** 2 of the 5 `never_recorded` Monday rows (2026-07-20, 2026-09-07) have a transcript of the same series dated
the NEXT day (2026-07-21, 2026-09-08; 09-07 is Labor Day), so they are likely shifted meetings, not missing ones. The builder matches
exact dates. A one-day tolerance, or matching on the calendar instance's own id, is a builder change for a later round.

## Inputs read this round (issuer session)

- Calendar: `list_calendar` in three chunks (28, 32, 44 events; none with a nextLink). An earlier exploratory call in this session
  printed one 10-day calendar page in full into the session; nothing of it entered any file.
- `list_meeting_transcripts` for the four series ids (20, 8, 7 rows; research refused).
- Bronze listing: 1,937 keys, 30 (series, date) transcript pairs.
