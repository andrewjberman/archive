# The Variant 1 round: the cut plan (2.0.0_SA_COO~D1, 2026-10-14 ~20:5xZ, written for the 21:00Z re-seat; nothing is cut yet)

**Gate:** PRD v2.21 reads ADMITTED (`prd-signoff.py status`: ratified-text SIGNED by the CVO, current; brief auto-admitted). The CTO's msgs 5868, 5873 and 5877 say cut now; the 21:00Z dell1 restart is minutes away, so no worker or fork is started: they would die mid-task.
**Inputs read:** the CRO spec `org/tier1_exec/4.0.0_SA_CRO/deliverables/MDPF_CANON_GLOBAL_AUA_TREND_FULL_HISTORY_SPEC_20261014.md` @686f769e63 in full (Variant 1, amendment 1, the rule table, the amended oracle), the CRO record @ab28358b88, CTO msgs 5868, 5873, 5877. **NOT yet read:** the PRD addendum text v2.19 to v2.21 (@02852d9d16, @038b2173f3, @3826492d9c, @183aa32f6b): the cut reads it first.

## The rectangle (my reading of the CTO's msgs; the PRD addendum is the authority and may differ)

| cell | what | risk | depends on |
|---|---|---|---|
| `CN-p-1` producer (`mdpf_gold_consolidator`, `data/mdpf/scripts/gold/`) | Global series fields the Trend groups need: Client Supervised by difference, ETF and ALT, `carried` rows for the 9 no-total dates; the SMArtX `fact_model_aum_daily` read for the pre-05-18 SMA legs; the category tree drops "Muni SMA" from ALT (Muni is a custom model). NO pre-05-15 per-model emit (v2.20: dropped; the portal stitches it) | WORLD (a served change, a gold-package deploy by CloudOps under a never-widen pair, CTO half owed) | the SMArtX key's naming-gate and registry answer (a refusal is a registry row) |
| `CN-p-2` portal (`ModelPortfolios.tsx`, `trendGrouping.ts`) | the stitch of the single-firm lines (49F before 2026-05-15, Inflection's Custom 2026-05-15 to 07-19) for INTERNAL sessions only; every other session draws Variant 2 with exception (ii); Client Supervised, ETF, ALT from the served series; Other AUA retired; carried points drawn with their class. The approved edits ride it (lime, the Other Models "as of", 49F, Inflection and Cottonwood as built): ONE client-facing row, ONE smoke (CTO msg 5877) | LOCAL; client-facing at the landing | CN-p-1's served fields for the pre-05-18 legs; builds against the spec's amended oracle meanwhile |

Fan-out: 2 of 2 chains, cap 8; one data edge (CN-p-2's real run waits on CN-p-1's deploy). CN-i-3 is WITHDRAWN (msg 5877). The base for the portal worker is the current PROD plus the three feature commits (`scratch/canon-i3-base`, patch-ids equal to `fd5433a3`) or whatever the cut re-derives from the then-current PROD.

## Open before the cut (mine to read, or the CTO's to rule)

1. **How the portal knows a session is internal.** The stitch is "internal sessions only"; I have not found the signal the page can read. Read `portal/src` for the user type field the other internal-only pages use before writing CN-p-2.
2. **The history leaf (CN-j-1, deployed) is probably unused by this Trend.** The spec takes Client Supervised per date from the Global difference, "replacing `clientChipAt`", so the Trend no longer reads `category-views-history`. That makes CN-j-2 (surface a history-row error, a condition of the promote under the CTO's earlier ruling) possibly moot. Put to the CTO: withdraw CN-j-2, or keep it for another reader.
3. **The never-widen pair for CN-p-1:** count the writers of each moved Global leaf (N printed), both branches, a rollback per key; the spec says every Global leaf is read before and after and the headline sums must be byte-equal.
4. **Tooling:** the pixel comparison and the `--hover-after-press` option exist; the smoke is on 5174 and the CRO wants one line (branch and head hash) when it is ready.
5. **My own two flaws to not repeat:** a recipe for conditional edits must fit statement-level sites (name two constants, select by one flag), and a check that compares source lines must tolerate a rewrapped expression (see `HANDOFF_CN_I_3_20261014.md`).
