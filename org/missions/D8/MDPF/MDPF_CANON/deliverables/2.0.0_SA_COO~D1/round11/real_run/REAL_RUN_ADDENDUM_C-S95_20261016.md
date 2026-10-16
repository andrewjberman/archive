# MDPF_CANON round 11 -- real-run addendum for the CVO's C-S95 (CN-s-3 AC2): the Monthly view and a carried-date tooltip (2.0.0_SA_COO~D1, 2026-10-16 ~16:2xZ)

**archetype:** VALIDATE

Answers ADJUDICATION_v20 C-S95 ("render the Monthly view and one carried-date tooltip"). The screenshots are OUTSIDE the repo (C-S96, the CVO's ruling): this file commits only their path and SHA-256. Directory (this box): `C:/dev/_real_run/MDPF_CANON_r11/`.

| file | sha256 | what it shows |
|---|---|---|
| `cn_s_3_cottonwood_monthly_view_before_amendment1.png` | `2471718797e7a6a16203a3b0c85cc56b5f4dfbb78be7b5693f0b1212d9c61318` | the Monthly view of a Cottonwood session on the candidate at `978da061`: five bars, Jun 30, Jul 31, Aug 31, Sep 30, Oct 15; the Aug 31 bar DRAWS (the base drew nothing there) with its stack at reduced opacity |
| `cn_s_3_cottonwood_monthly_aug31_tooltip_before_amendment1.png` | `ffe9e425fc3b0cfde3c88a5ff385f77bf65ae0760d07baef038575e2034d91eb` | the 2026-08-31 tooltip at `978da061`: Total $476M; only `Custom Models (carried)` and `Other AUA (carried)` carry the suffix; the five primary rows read without it (the gap this run found) |
| `cn_s_3_cottonwood_monthly_aug31_tooltip_after_amendment1.png` | `bc582ca008d96c598208f922090b4cfacd9861d7023ad35aca6daa63ed92c17d` | the same tooltip after AMENDMENT 1 (portal `7a88ca75`, rebuilt, re-rendered): all seven rows read `(carried)`: Custom Models $15M, Ultra Short-Term $18.5M, Short-Term $18.4M, Intermediate-Term $80.3M, Long-Term $59.5M, Ultra Long-Term $1.07M, Other AUA $284M; Total $476M |

The 2026-08-31 values equal the CRO spec's month-end oracle row (18.5, 18.4, 80.3, 59.5, 1.1, 15.0, 283.7, 476.5, $M). Method: `bun run build` then `node scripts/ui-smoke.mjs portfolios <png> --dist dist --firm cottonwood --fixtures <served 2026-10-15 Cottonwood object> --click Trend --pick monthly --hoversel ".recharts-bar-rectangle#32"` (the Other AUA segment of the third bar), headless Edge, auth stubbed.

**What the run found, and the repair:** the first tooltip marked two of the seven rows. `carriedTooltipLabel(entry.name, carried_keys)` marks a row only when its display name is in the carried-key list, and CN-s-3's list held the canonical stack labels for the five primary lines. The order was reopened (AMENDMENT 1, `fe07e26ec5`; same bytes on the worker branch `dec17c26cc`), the worker added the display names (portal `7a88ca75`, one file), the instance is VALID, merged `265af9105f`. The worker also filed row `MDPF_CANON-D1-W31-S1` (OBSERVATION, INERT): the Global Trend's carried keys are raw stack labels too, so its five primary rows cannot read `(carried)` on a carried date; read from code, NOT rendered, outside this order. It is the CVO's to place.

The candidate rendered here: portal DEV `39dab87f3b` + `1e39adc9` (CN-s-4) + `978da061` (CN-s-3) + `7a88ca75` (the repair), on the nested branch `wk-31-r11-candidate`. Instruments after the repair, on this candidate: `r11_cn_s_3.py pure` 7 of 7; `bun run typecheck` rc 0 (the negative control was run at the first candidate and stands).
