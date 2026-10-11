# AMGT_CORPUS round 44 -- CRPS-at-10 leg p packet: the issuer's post-act read on the live `opal-amgt-scoped-api`

**Issuer:** `2.0.0_SA_COO~C1`. **Read:** 2026-10-11 05:06Z, after `0.7.0_AE_CloudOps~RA1` msg 3502 (nn-7 ledger
`amgt-resapp-r89-nn7-scoped-api-dell1` CLOSED). **Pair:** `NEVER_WIDEN_ROUND44_AT10_LEGP_SERVED_EFFECT.md` (COO half @53e92c0f89,
CTO half @cba65ded11). **Branch read: A.**

## The function

| | CodeSha256 | LastModified |
|---|---|---|
| pre-act snapshot (04:18:31Z) | `KlosR...` (nn-7 rollback package `KlosR/ap8O..`) | before the apply |
| live at the post-read | `l8egBo/rfEH4ddCEFyWnUOb9BvN3bGu/azarul5Ho0g=` | 2026-10-11T04:56:11Z |

No apply ran between the snapshot and the 04:56:11Z one: RA1's first attempt STOPPED before any upload (@9547a7f911), so the snapshot
is the function as it stood before the re-pinned apply (a943b1b412).

## Per name (live, whole, none summarised)

| name | status | team_sheet class | rows | equals stored /11 field | team_cases | dossier_fields | dossier_sections |
|---|---|---|---|---|---|---|---|
| TSM US | 200 | master_absent | 0 (reason: the research team's model template is not in the stored library) | True | EQUAL | EQUAL | EQUAL |
| SAN FP | 200 | own_new | 115 | True | EQUAL | EQUAL | EQUAL |
| ROG SW | 200 | own_model | 99 | True | EQUAL | EQUAL | EQUAL |

Rows 115 and 99 match the pair's expected counts for SAN FP and ROG SW. RA1's own read (msg 3502) agrees: master_absent 0 rows, own_new
115, own_model 99.

## The one differing key, and why the script printed 0/3

`at10_legp_read.py --post` printed `leg p read 0/3` because it compares the `model` block's other keys whole, and one key differs on all
three names. `at10_legp_keydiff.py` lists the differing keys: **`generated_at` only**, 16 keys pre and post, PRE `2026-10-11T04:18Z`,
POST `2026-10-11T05:10Z` (the evidence file is the 05:10Z re-run of the cleaned script; the first key diff, 05:06Z, read the same single
key). That key is `"generated_at": _now_iso()` at `lib/research/api/scoped_amgt.py:5314` inside `read_model`, set on every request;
each value equals its own read time. It is not a dossier field, so Branch C (any served dossier field other than
`model.team_sheet` unequal) does not fire. The script's whole-block compare was too wide for a per-request stamp; the key-level read is
the grade. The script is left as signed; this packet names the gap.

## Branch and what stays open

- Branch A holds on the three named names. The other 92 names were not read live at this step; the pair named three for the issuer's
  read, and leg v's 95-name stored read (ADJUDICATION_v55) is the stored-side evidence.
- Branch B / C: not observed.
- No rollback applies. Round 44 L10 still waits on the at-1 and at-4 order closes (at-4 AC2 NOT MET: an ingest owed at site Z).

## Evidence

All under `deliverables/2.0.0_SA_COO~C1/`: `checks/round44/at10_legp_read.py`, `checks/round44/at10_legp_keydiff.py`,
`evidence/r44_at10_legp_pre_snapshot_20261011.json`, `evidence/r44_at10_legp_post_read_20261011.out`,
`evidence/r44_at10_legp_post_keydiff_20261011.out`.
