# RT8 ARM (g) -- THE FOUR SYNTHETIC EXPORTS, BEFORE AND AFTER

`0.9.0_WK_IRPT_BCKEND~4` on `IRPT_BCKEND.TO-IB-rt-8`, addendum arm (g).
Ledger `irpt-bckend-rt8-synthetic-delete`, entry
`org/critical_paths/change_management/20260911T1454Z_irpt-bckend-rt8-synthetic-delete_deploy_completion.md`.

**THE WORD.** `1.0.0_SA_CTO` 95968 carrying Andrew-direct 2026-09-11 ~13:48Z, VERBATIM
*"yes on synthetic exports"*; record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260911_134xZ_PUSH_CLOUD_HOLD_DEV_FETCH_LATO_DELETE_SYNTHETIC_EXPORTS.md`.
It covers EXACTLY four objects in `opal-data-ycharts` (us-east-1) under
`firms/49financial/generations/GENIBS14SYN/attempts/1/exports/` and nothing else -- no other
object, no other prefix, no other firm. This file is written in two passes: the BEFORE section is
committed with the ledger's sentinel BEFORE any delete; the AFTER section is appended when the act
is done.

---

## I. THE INVENTORY RE-READ AT THE MOMENT OF THE ACT

Read under this serial with `s3api list-objects-v2` and `s3api head-object`, not carried forward
from the round-2 inventory. **A re-read is required precisely because the earlier inventory is
hours old and a delete is unrecoverable at this grain.**

| key (under the prefix) | bytes | ETag | VersionId | metadata |
|---|---|---|---|---|
| `r1/report.pdf` | 43,848 | `7cdc641a549f69b473d4aca0970f0bc8` | `wl2x4Z9vSi31.i.TUVq__pjfcz0U4qFK` | `irpt-synthetic=true`, `export-revision=r1`, `vendor-synthetic-holdings=false` |
| `v0-11-overview/report.pdf` | 41,859 | `a9daef1f66f1bc6a2c04a1065134ba49` | `Jg9agZs3W5xchqyD8bH3UCQTCMQ8Z2HS` | `irpt-synthetic=true`, `export-revision=v0-11-overview`, `vendor-synthetic-holdings=true` |
| `v0-11-comparison/report.pdf` | 41,859 | `1997156029153927e559bb4c4efe81b2` | `NO5Dioo.m.mOZs4JjR2GsZHXKmhI6nVE` | `irpt-synthetic=true`, `export-revision=v0-11-comparison`, `vendor-synthetic-holdings=true` |
| `v0-11-multicomp/report.pdf` | 41,859 | `5a4c65fe92ad24ebb4845d5ab9d9c095` | `arZTAfWafyUSzIQRYcctzEswDuMxmOlv` | `irpt-synthetic=true`, `export-revision=v0-11-multicomp`, `vendor-synthetic-holdings=true` |

**THE GATE, WITH ITS DENOMINATORS:** 4 of 4 named keys present; `irpt-synthetic=true` on 4 of 4;
**0 unexpected objects under the prefix**; and the WIDER read -- the whole `GENIBS14SYN/` generation
-- holds 4 of 4 objects and **0 objects the word does not cover**, so there is nothing under this
generation that the act must be careful to spare. A FIFTH object would have been a STOP and a row,
never a fifth delete. Verdict printed by the reader: `PROCEED`.

The machine-readable capture is `.scratch/rt8g_before_inventory.json` in the worker's worktree; the
table above is its content, and the transcript is quoted in the ledger's L1 proof.

## II. WHAT IS NOT RE-RUN, AND WHY

The production-reader exclusion proof is **CITED, NOT RE-RUN** -- arm (e) of the RT8-AC1 battery,
transcript committed at
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/IB-rt-8_RT8-AC1_battery_output.txt`:
5 of 5 objects `EXCLUDED_BY_BOTH`, 4 of 4 readers admitting 0 of 5, with the ordinary-object control
showing `export_status` and `download` still admitting 1 of 1. Re-running it would measure the same
thing with the same instrument, and after the delete the four objects it read no longer exist.

## III. ONE FACT THE WORD DOES NOT REACH, STATED BEFORE THE ACT

**`opal-data-ycharts` HAS VERSIONING ENABLED** (`get-bucket-versioning` reads `Status: Enabled`,
read in the same pass as the inventory). A `delete-object` without a `--version-id` on a versioned
bucket does NOT destroy bytes: it writes a DELETE MARKER, after which `head-object` returns 404 and
every ordinary read stops finding the object, while the four noncurrent versions listed above
remain retrievable by their VersionId. **So "deleted" here means "removed from every ordinary
read", not "the bytes are gone."** That is the act this arm performs, and it is the conservative
one: the permanent form is `delete-object --version-id` per version, which is UNRECOVERABLE and is
a different act needing its own word. Recorded as row `IRPT_BCKEND-W4-S20` rather than decided
here.

---

## IV. THE ACT

(appended after the deletes)
