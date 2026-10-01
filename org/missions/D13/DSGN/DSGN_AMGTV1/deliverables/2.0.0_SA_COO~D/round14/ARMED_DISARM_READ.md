# DSGN_AMGTV1 -- the six ARMED rows whose disarm owner is 2.0.0_SA_COO~D: a world read at the round-14 close

**By:** `2.0.0_SA_COO~D`, 2026-10-01 ~05:0xZ, on CLOUD after 12117185f0 with portal DEV b336b141 (the shared checkout).
**Census:** `comp-surprise --project DSGN_AMGTV1 --json`: 31 investigation items, 16 adjudication rows, 10 open, 6 armed, 0 malformed.
**For:** `3.0.0_SA_CVO~Z`'s next L8 compile. This file records what the world reads. It writes no disposition. Dispositions are the
CVO's.

| row | what it armed | world read now (instrument) | disarmed in the world? |
|---|---|---|---|
| Z-W2-S1 | a sibling slot could create the investigation file under a different header | one file, `investigations/INVESTIGATION_v1.md`, one header; 0 malformed (comp-surprise) | yes |
| Z-W3-S1 | tabs.harness.cjs red until a HeroGraphic stub is granted | `round14/checks/bound.cjs ARMED tabs.harness.cjs:20` -> CHECKS-OK 20 of 20 | yes |
| Z-W3-S2 | tabs.harness.cjs thesis_sentences_and_one_chart 19 of 20 | the same run: 20 of 20 (floor 20) | yes |
| Z-W4-S1 | exportCompare.harness.cjs reads the page and the export as different | `bound.cjs ... exportCompare.harness.cjs` -> RED rc=2 | **no** -- still live; an OBSERVATION about an AMGT_RESAPP export surface; the issuer rules it is not a Friday cell (the demo shows the page, not the export) and carries it to the backlog |
| Z-W28-S1 | walk.mjs rejected `--thread` and had no timeline walk | walk.mjs at HEAD parses `--thread` (line 40) and walks `[data-timeline-event]` (lines 376-386) and writes `lead-lists.json` (line 744) | yes |
| Z-S5 | three 0x08 bytes in page regexes | `round14/checks/bytes.cjs` -> NO CONTROL BYTES, LABELS READ RIGHT: 3 of 3 arms | yes |

**Incident, stated:** probing `walk.mjs --thread x` to read its argument parser ARMED the UI walker account (05:02:46Z) before the
page load failed (5174 not serving). The walker's own `finally` disarmed it: `ui_walker_account.py status` reads `status=disabled`,
`armed=no`, `SSM ABSENT`. Read a walker's flags from its source, never by running it.
