# N3 -- the namers' comparison, round 2 (LN-e-3)

**Cell:** `LN-e-3`, round 2 · **Order:** `LGIC_NAMING.TO-LN-e-3-r2` · **Worker:** `0.9.0_WK_LGIC_NAMING~6` ·
**Branch:** `wk-lgic-naming-2-6`, cut from `CLOUD` @866f250fec · **Date:** 2026-09-14

This file compares the two answer files. It does not name anything. Where the namers differ, that difference is
evidence for outcome FWD-1, not a defect to fix.

## Inputs (read at HEAD 866f250fec)

- Namer A: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n3-namer-a.tsv`. This is cell e1. The header
  says `base 619dec559f` and `seat b100c432-0c42-4493-98e7-702644d33b1b`.
- Namer B: `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/r2/n3-namer-b.tsv`. This is cell e2. The header
  says `base 619dec559f` and `seat e01a546a-27da-4d0e-b8c7-4c8475c4efc3`.
- The two seat records, `exercises/r2/seats/e1.seat.json` and `e2.seat.json`. They show the same `prompt_sha256`
  (`84ac10b1...a0501ba100`), different `session_id`s and different `seat_dir`s. Neither seat_dir is inside the
  workspace or in a git repo.
- The ruled names: s.2 of `org/tier1_exec/1.0.0_SA_CTO/deliverables/ROUND_ANALYSIS_LGIC_NAMING_ROUND1_20260914.md`.
  The table is the one at @de52d3db04. The file was last changed @2706014705 (the SC1 correction), and that change
  says "The dry-run table below is unaffected".

## Checker output, verbatim

`E3R-AC1`: `timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py e3-identical`

```
DIFFERS: i03  A=orion-inf-ingest-daily  B=orion-inf-orion-ingest-daily
DIFFERS: i10  A=smartx-49f-platform-export-weekly  B=smartx-49f-smartx-platform-export-weekly
DIFFERS: i11  A=pathfinder-etfs-ingest-task  B=pathfinder-etfs-pathfinder-ingest-task
ITEMS: 18  IDENTICAL: 15  DIFFERENT: 3
VERDICT: FAIL-DIFFERENT
rc=0
```

`E3R-AC2`: `timeout 120 python org/missions/D14/LGIC/LGIC_NAMING/deliverables/2.0.0_SA_COO~G/fixed_inputs/r2/check_ln_r2.py e3-blind`

```
PROMPT A sha: 84ac10b1eaf8339fdc30b1bc8fcb0103eb3503ad7560c99daeb924a0501ba100  PROMPT B sha: 84ac10b1eaf8339fdc30b1bc8fcb0103eb3503ad7560c99daeb924a0501ba100  (identical input: neither seat was given anything but the briefing)
SESSION A: b100c432-0c42-4493-98e7-702644d33b1b  SESSION B: e01a546a-27da-4d0e-b8c7-4c8475c4efc3
VERDICT: PASS-NAMERS-UNCONFERRED
rc=0
```

## The DIFFERS items (3 of 18)

The "rule" column is copied from the same s.2 row. It is not this cell's judgment.

| item | namer A | namer B | ruled name (s.2) | which namer wrote the ruled name | s.2 rule column |
|---|---|---|---|---|---|
| i03 | `orion-inf-ingest-daily` | `orion-inf-orion-ingest-daily` | `orion-inf-ingest-daily` | namer A | FN1 (noun: the Orion ingest) |
| i10 | `smartx-49f-platform-export-weekly` | `smartx-49f-smartx-platform-export-weekly` | `smartx-49f-platform-export-weekly` | namer A | FN1 (noun: the SmartX platform export) |
| i11 | `pathfinder-etfs-ingest-task` | `pathfinder-etfs-pathfinder-ingest-task` | `pathfinder-etfs-ingest-task` | namer A | FN1 (noun: the Pathfinder ingest) |

- i03: A=`orion-inf-ingest-daily` B=`orion-inf-orion-ingest-daily` ruled=`orion-inf-ingest-daily`. Namer A wrote the
  ruled name.
- i10: A=`smartx-49f-platform-export-weekly` B=`smartx-49f-smartx-platform-export-weekly`
  ruled=`smartx-49f-platform-export-weekly`. Namer A wrote the ruled name.
- i11: A=`pathfinder-etfs-ingest-task` B=`pathfinder-etfs-pathfinder-ingest-task` ruled=`pathfinder-etfs-ingest-task`.
  Namer A wrote the ruled name.

**Tally.** 3 items differ. Namer A wrote the ruled name on 3 of them and namer B on 0. In all 3, B's name repeats
the system token inside the function slot. That is a description of the strings, not a grade.

## Items disclosed by row LGIC_NAMING-S15

Row `LGIC_NAMING-S15` (in `surprise-channel/investigations/INVESTIGATION_v1.md`, filed by `2.0.0_SA_COO~G`) says
the namers' briefing contains the ruled names of these two items word for word. So the namers agreeing on them can
come from copying the briefing, and is not independent evidence for FWD-1.

- **i05, DISCLOSED (S15).** Checker: IDENTICAL. Both namers wrote `opal-data-cottonwood`, which is the ruled name.
  The briefing's registry seed (`infra/logic/05_IDENTITY_SPINE.md:68`, per S15) names it.
- **i15, DISCLOSED (S15).** Checker: IDENTICAL. Both namers wrote `orion-inf-build-gold-profile`, which is the
  ruled name. It is SY1's worked example (`org/standards/NAMING_SCHEMA.json:125` v1.6 @2706014705, per S15).

## Denominator

18 items: 15 identical and 3 different. The 15 identical items include the 2 S15 items, i05 and i15.
