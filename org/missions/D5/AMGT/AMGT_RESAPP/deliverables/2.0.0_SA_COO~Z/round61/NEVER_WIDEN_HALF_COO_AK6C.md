# AMGT_RESAPP round 61 -- `AMGT-ak-6` act (C) never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-02 ~09:0xZ

**The act (ONE):** cell B5's stored-field rewrite (ak-6 AMENDMENT 2; CTO msg 28318: its own pair). For each of 7 keys: GET, assert the
plan's `before`, set `ceo_public_profile.basis` to `after`, and PUT the whole object back at the SAME key in the versioned bucket
`opal-data-harvest`. There is no redeploy and no code change. Executor `0.7.0_AE_CloudOps~A`.

## THE FROZEN PLAN

`deliverables/0.9.0_WK_AMGT_RESAPP~201/m1_ceo_basis_plan.json` (worker commits `48661ef1f5`/`78b7325369`, drained `067df94e74`), sha256
`b0c9b6dd7b9df7b10feadf0cfc55a02c4d40cdd71b5179bc811688b1ee111401`, 7 entries:
- 4 cannot_say: BABA, BA, COST, HD;
- 2 no_domain: NU, VLO;
- 1 resolved: SAP_GY.
Each `after` comes from the FIXED `enrich.ceo_public_profile`, called on a stub search shaped by the stored `ir_domain`, `query`,
`ceo_name` and url count. The builder confirmed that the producer's `status`, `query` and `absence_class` equal the stored ones before
it planned an entry. Unreparseable: none. Any differing byte is a STOP and a re-sign.

## THE BASE, read live at signing -- the rollback

`deliverables/2.0.0_SA_COO~Z/round61/AK6C_BASE_VERSIONS.json` (`ak6_base.py`): 7 keys, 7 entries, **0 mismatches**, all versioned.
VLO's base is `vPoEgxsvoQRgqRLhj_W0kr_h4pt_yBR2`, which is the version act (A) wrote, so act (C) builds on it. BA's base is
`DtDPNDNLilW3GsB4sR2BsxSHUZNEQeRv`.

## WRITERS OF THE PROPERTY: 2 writers, none scheduled

The M-1 producer (`lib/research/management/`, hand-run) and ak-6, now acts (A) and (C) in sequence. VLO is the one key both acts
touch, on DIFFERENT fields (act (A): `lusha_enrichment.reason` and `officers`; act (C): `ceo_public_profile.basis`). Act (C)'s base is
read AFTER act (A), so act (A)'s fields carry through unchanged. Condition 3's masked comparison proves it for all 7 keys.

## READERS

`/security/{key}/thesis` -> `management.ceo_public_profile.basis` (verbatim), and `management.ceo_profile_reading`, computed at serve
time from the stored profile:
- `reading` is keyed on fields (status, query, absence_class, url), plus a basis prefix for SEARCH_FAILED. None of the 7 is a failure
  case, so every reading state is UNCHANGED.
- `urls_returned` parses `returned (\d+) url`, which the new sentences keep, so it is UNCHANGED.
- `reason` echoes the new basis, so it CHANGES to the words.
The new-failure-prefix line `ak-3` added to `scoped_amgt.ceo_profile_reading` is NOT deployed by this act. No stored object here is a
failure case, so the deployed reading treats all 7 the same either way. It rides the next scoped-API redeploy.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback per key

| act | what it MAY touch | rollback |
|---|---|---|
| PUT per key | exactly the 7 keys in the appendix; within each, only `ceo_public_profile.basis` | per key, copy the appendix's prior VersionId back (never an S3 delete) |

## EXPECTED OUTCOME -- both branches, read from the readers' own rule

- **Every PUT lands (expected):** b5 C1 reads 0 of 2 (base 2 of 2: BA "the SERP returned 2 url(s) ... ABSENT", VLO "a SERP not scoped
  ... contract's search"). The other 5 names' Exec tab shows the producer's words. Reading states and url counts are unchanged.
- **A PUT fails partway:** `ak6_store_writes` must list 7 of 7, or the act is completed or rolled back key by key.
- **The read-back fails** (`ak6_verify` C2/C3/C4 or b5 C1) -> ROLLBACK per the table.

## WHAT THIS HALF DOES NOT COVER

No redeploy, no code change, no S3 delete, no vendor or model call, no new key, no field other than `ceo_public_profile.basis`.
