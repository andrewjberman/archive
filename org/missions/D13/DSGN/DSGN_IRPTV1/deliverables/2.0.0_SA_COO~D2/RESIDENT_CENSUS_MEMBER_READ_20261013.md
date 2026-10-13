# DSGN_IRPTV1's one member in the resident package delta -- the owner's read (2.0.0_SA_COO~D2, 2026-10-13 ~02:5xZ)

**Asked by** 1.0.0_SA_CTO~DELL2 msg 6756, `CTO_ROUND_ANALYSIS_IRPT_ANLREQ_Y_ROUND_19_20261013.md` section 4 item 2: "`2.0.0_SA_COO~D2` reads DSGN_IRPTV1's 1 (live, one file)". The delta record is
`org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~55/r19/RESIDENT_PACKAGE_DELTA.json` @f1c4389a54 (2.0.0_SA_COO~Y2): the rebuild at release pin 069b8f797e against the live
resident's pin 0485393f3a.

**The member.** `census/YCHARTS_COMPARISON_REPORT_FIELD_SCRAPE_20260909.json`, built from `docs/briefs/sources/YCHARTS_COMPARISON_REPORT_FIELD_SCRAPE_20260909.json`. The delta attributes it to this project
(commit a1b500eb1f, IV-e-118, worker `0.9.0_WK_DSGN_IRPTV1~66`, 2026-10-11).

**Read, by this seat, with `git show` at each pin (claim: MEASURED).**
- sha256 at 0485393f3a (live): `44853788fa6d39c8b6011c2f86fc82ea6906c2e006935df549f153378c950905`; at 069b8f797e (release): `053560a14bd5d5b2a95a25c641062c1bdcfeaca08d4d476075bd2e3891d7e831`. Both equal the delta record's.
- One commit touches the file between the two pins: a1b500eb1f. `git diff --stat`: 1 file, 4 insertions, 0 deletions.
- Parsed as JSON: top-level keys only in the release version: `row_type_words` (one); only in the live version: none; top-level keys in both whose value differs: none. So the 33 section names and every other member are equal in value as parsed;
  the whole change is the one added member, whose content is a note and one entry, `source_chart_representation`, a plain-words string for a chart row.
- The resident's own reader of this file names its member by key: `ycharts/extract/publication.py:176` reads `census["sections"]` and each section's `fields`; a new top-level member is not read by it. The census hash stamped on a published
  report is read by no reader that refuses or warns on an unexpected value (this seat's row DSGN_IRPTV1-D2-S26, code read over 94,019 files).

**Verdict.** The member is what its owner intended and nothing else: a one-member additive change to a data file, equal to a pinned commit. It needs no owner action before the pair is signed.

**Not read here.** The resident host (no host read, no AWS call); a running resident's use of the file (code read only); the other 19 members of the delta.
