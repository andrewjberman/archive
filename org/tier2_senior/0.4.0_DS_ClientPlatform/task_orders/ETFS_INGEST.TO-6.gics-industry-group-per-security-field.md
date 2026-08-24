# TO ETFS_INGEST.TO-6 — add `GICS_INDUSTRY_GROUP_NAME` to the per-security pull and carry it to the gold row (`INGEST-T5-1` data half, `INGEST-T3-6`)

<task_order id="ETFS_INGEST.TO-6" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED) — the DATA half of `INGEST-T5-1` (the finer field), and `INGEST-T3-6` (the gold row's Rule-24 act, a SECOND schema act at a DIFFERENT GRAIN from T2's).</decomp_ref>
<certification>✅ CERTIFIED, `3.0.0_SA_CVO~Z` @422bdb431b, bound to `@fcdf042972`. Reduced-cohort; premise-oracle verification a SAMPLE not a census.</certification>
<issued_to>DS-class. Seated: `0.4.0_DS_ClientPlatform~Z` — **who requested this TO rather than starting on a sovereign word that named their cell. That was right.**</issued_to>
<executor_class>DS-class</executor_class>
<seating_trigger>SEATED. ⛔ **BUT THE TOUCH IS SEQUENCED BY `1.0.0_SA_CTO~Z`, NOT BY ME — see below. DO NOT EDIT `etf_daily_pull.py` UNTIL THEY SEQUENCE IT.**</seating_trigger>
<placement>**SITE Z** (Rule 26). `data/**` and the etfs-pipeline Lambda are both yours to author (`.owned-paths.yaml:1661`, `POD4_OR_AE`); **AE deploys.**</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T21:5xZ</issued>
<status>staged — begins on GO **and** on CTO~Z's sequencing word</status>
<priority>P1 — it is the one input `ETFS_INGEST.TO-5`'s AC4 is blocked on, and AC4 is condition (ii).</priority>
<authority>**Andrew-direct ~21:47Z, VERBATIM:** *"Regarding the GICS, the way that needs to work is basically pulling all Opal ETF consitutent securities via the provider docs, then those securities get added to the ETFS bloomberg pull and we get that data from bloomberg itself. That way we dont need to do the constituent weighting process in bloomberg, we just get all the constituent data and we manage the calculations server side in our pipeline"* (record via `0.0.0_AB_MSTR~Z` msg 5199). Plus **C3 RULED** ~20:0xZ. CLAUDE.md Rule 13, Rule 24 (the gold row is a value-enum act at authoring).</authority>
</task_order>

## WHY THIS IS ADDITIVE AND NOT A NEW MECHANISM

**His 21:47Z word describes the shape `etf_daily_pull.py` ALREADY HAS:** it derives its universe from
`silver/holdings` — the **issuer** roster — then pulls per-security CHAR fields from Bloomberg for
that universe. `GICS_SECTOR_NAME` is **already in that list**. So this TO adds **one more field to a
per-security call that already runs**, and the aggregate is computed **by us, server-side, from
issuer weights × per-security GICS** — which is exactly what he said.

**Nothing architectural is being reversed.** What he ruled OUT is asking Bloomberg to enumerate or
weight constituents (the BQL path he already closed). What he ruled IN is the split we already have.

## ⛔ THE SEQUENCING IS NOT MINE AND I AM NOT SETTING IT

`etf_daily_pull.py` is **RUNNER_TREE_IS_PRODUCTION — saving the file IS the deploy**, no apply, no
review window. Three things want to touch it:

| who | what | status |
|---|---|---|
| `0.0.0_AB_MSTR~Z` | the **A5 one-expression** null-tolerance fix at `:88` | authorized, lands **after** the 22:00Z fire |
| **you, this TO** | the additive CHAR field at `:141` | **needs CTO~Z's word** |
| you, later | `INGEST-INV-3` — derive `FUNDS` from the config instead of restating it | **stays on A2's trigger** |

⛔ **TWO HANDS ON ONE PRODUCTION-ON-SAVE FILE IS THE HAZARD, NOT THE EDIT.** `1.0.0_SA_CTO~Z` holds
A2/A5 and sequences this. **Ask them before you touch the file; do not infer a slot from A5 having
landed.** MSTR~Z said the same and was right to say it is not theirs to set either.

## ⚠ A LIVE SOVEREIGN QUESTION SITS BESIDE THIS — AND IT DOES NOT BLOCK YOU

At the time of writing, Andrew is being asked (via CTO~Z) to confirm **GICS as the SERVED vocabulary
with Bloomberg's HB labels as a cross-check** — because three seats measured that the HB vocabulary
has **zero per-security members** and could only be served by taking Bloomberg's own fund-level
weighting, the thing his 21:47Z word says we do not need.

**THIS TO IS SAFE UNDER EITHER ANSWER**, which is why it is cut now rather than held: the finer GICS
field is required to render the side-by-side comparison **whichever vocabulary he ultimately picks**.
⛔ **What his answer WOULD change is `INGEST-T3-6`'s gold-row vocabulary act — so if he rules before
you reach that half, use his ruling and tell me.** Do not pre-empt it.

## Acceptance criteria

| id | criterion | cell_refs | grounding |
|---|---|---|---|
| **`INGEST-TO6-AC1`** | `GICS_INDUSTRY_GROUP_NAME` added to the **per-security CHAR field list** (`etf_daily_pull.py:141`). **ONE field, nothing adjacent** — `INGEST-INV-3` stays on A2's trigger even though it is in the same file and the same hand | `INGEST-T5-1` | **SOURCE** |
| **`INGEST-TO6-AC2`** | ⛔ **CTO~Z's sequencing word is CITED in your report before the edit** — who else touched the file, in what order, and where your save sits. **Saving is deploying** | `INGEST-T5-1` | **SOURCE** |
| **`INGEST-TO6-AC3`** | ⛔ **EXERCISED ON A SCHEDULED FIRE, not an ad-hoc run.** The landed `bbg/{as-of}/characteristics.csv` gains the column, `run_manifest.json` reads `run_class: scheduled`, and the field-exception counts are legible. **Report which run you read and how you know it was the scheduled one** | `INGEST-T5-1` | **EXERCISED** |
| **`INGEST-TO6-AC4`** | The **gold holding row** carries the field, as a **Rule 24 authoring act** with its four-postulate record — ⛔ **a SECOND schema act at a DIFFERENT GRAIN from T2's row, and the two MAY NOT SHARE AN AXIS.** Include the token-hygiene census (`comp-find -i`, denominator printed) | `INGEST-T3-6` | **SOURCE** |
| **`INGEST-TO6-AC5`** | ⛔ **RE-CHECK THE OVERLAP AT THIS EDIT — this is the hand-off `ETFS_INGEST.TO-5` AC5 named you for, by serial.** `0.4.0_DE_ClientPlatform~Z` measured that `characteristics.csv` carries **`TOTAL_NUMBER_OF_HOLDINGS_IN_PORT` but NOT `FUND_PCT_TOP_TEN_HOLD`** — so the "two fast-moving fields overlap" premise is **HALF TRUE**, and the second is **SOLE-SOURCED** from the constituents leg. *(I relayed that premise into a TO without measuring it; it is one of two relay defects of mine this round.)* **State both fields' post-edit sourcing** | `INGEST-T5-1` | **DATA** |

<proof_of_spec>
  <!-- POSITIONAL invocation, no flag; CHECK THE RC not the output string; take it WITHOUT a pipe.
       The `firm` enum still has no ETFS value — enter FABRIC and DECLARE it, as you did on TO-2/TO-3.
       Routed to CTO~Z as gate owner; neither of us edits a gate. -->
  <criterion id="INGEST-TO6-AC1" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC2" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC3" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO6-AC4" cell_refs="INGEST-T3-6"/>
  <criterion id="INGEST-TO6-AC5" cell_refs="INGEST-T5-1"/>
  <expected_criteria>INGEST-TO6-AC1,INGEST-TO6-AC2,INGEST-TO6-AC3,INGEST-TO6-AC4,INGEST-TO6-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/ETFS_INGEST.TO-6_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run at pickup

| premise | the read |
|---|---|
| the field is absent today | `head -1` the landed `bbg/{as-of}/characteristics.csv` → **11 columns, no `GICS_INDUSTRY_GROUP_NAME`**; ⛔ **positive control `GICS_SECTOR_NAME` MUST be present** or your read is broken, not the field absent |
| the CHAR list is at `:141` | `grep -n "GICS_SECTOR_NAME" integrations/bloomberg/pipeline/etf_daily_pull.py` |
| A5 has landed | `grep -n "fillna(False)" integrations/bloomberg/pipeline/etf_daily_pull.py` |
| the universe derives from the issuer roster | `sed -n '78,92p' integrations/bloomberg/pipeline/etf_daily_pull.py` — this is the half of his word that already exists |

## Standing constraints

- **The file is production-on-save.** One field. Nothing adjacent. **`INV-3` waits for A2.**
- **No alarm, no monitor.** The manifest and the log are the record.
- **Commit to your lane; do NOT push.** Report per-commit push state, as you did on TO-3 — **that
  discipline caught a difference two of your three commits had.**
- **Read the number, then write the sentence.**
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), coordinate `-Z-S{n}`.
  Mid-round the spec is FROZEN — route, do not adjudicate.
- **Status moves with the act, by you, same turn.**
