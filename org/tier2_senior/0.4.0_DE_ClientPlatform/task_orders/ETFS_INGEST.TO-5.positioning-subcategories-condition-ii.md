# TO ETFS_INGEST.TO-5 — condition (ii): "GICS replaced for sub-categories" on the DEV build (`INGEST-T5-1`, `INGEST-T5-2`)

<task_order id="ETFS_INGEST.TO-5" project="ETFS_INGEST">
<decomp_ref>workflows/atom_decomposition/runs/etfs-ingest/20260824T2010Z/DECOMP.md @fcdf042972 (CERTIFIED vintage) — cells `INGEST-T5-1` (condition (ii) render) and `INGEST-T5-2` (the render sites + the sub-asset-class lookup question, surprise item Z-S-G).</decomp_ref>
<certification>✅ **CERTIFIED** — `3.0.0_SA_CVO~Z` @422bdb431b, **bound to `@fcdf042972` and no other vintage.** Cut after certification. ⛔ **What the signature does NOT buy:** REDUCED-COHORT run, **one independent perspective (the author's)**; *a certifier is the second reader, not the cohort*. Premise-oracle verification was **a SAMPLE, NOT A CENSUS** (3 of 36). **In particular, no DE-class seat has read the portal plane for this decomp — the two cells below are MY reads and you are the first portal reader.**</certification>
<issued_to>DE-class (portal). Seated: `0.4.0_DE_ClientPlatform~Z`.</issued_to>
<executor_class>DE-class</executor_class>
<seating_trigger>SEATED. ⛔ **THE TWO CELLS HAVE DIFFERENT TRIGGERS — START WITH `T5-2`, WHICH IS UNBLOCKED NOW.** `T5-1` waits on a data dependency (below) that is not yours and is A2-sequenced.</seating_trigger>
<placement>**SITE Z** — ruled by `1.0.0_SA_CTO~Z` on your own first `/frontend-dev` render (*"an unprovable toolchain = the one laptop leg, SURFACED not assumed"*). I had left this OPEN in my executor-class declaration rather than assuming it; your render settled it.</placement>
<issued_by>2.0.0_SA_COO~Z</issued_by>
<issued>2026-08-24T21:0xZ</issued>
<status>staged — begins on GO</status>
<priority>P1 for `T5-2` (unblocked, and it answers a live open question) · P2 for `T5-1` (gated on the field).</priority>
<authority>Andrew-direct ~15:2xZ promote conditions, VERBATIM: *"Until data pipeline is complete with full data structure for daily bloomberg data for all ETFs, and it displays properly on DEV build with **GICS replaced for sub-categories on frontend**."* **C3 RULED ~20:0xZ** (*"all recs approved, proceed"*, CTO~Z msg 4845): sub-categories = **`GICS_INDUSTRY_GROUP_NAME`** (one level finer), **rendered on DEV BESIDE Bloomberg's `HB_INDUSTRY_SECTOR_ALLOCATION` labels for him to point at.** The Models-side segment vocabulary is **OUT**. ⛔ **THE PROMOTE WORD REMAINS HIS** — this TO serves condition (ii); it does not discharge the promote.</authority>
</task_order>

## ⛔ START HERE: `INGEST-T5-2` — A QUESTION I AM FILING, NOT A DEFECT I AM ASSERTING

**MEASURED at the COO seat (re-derive it — it is one of the 33 oracles the certificate does NOT assert):**

| map | keys | GICS sector names present | `Cash & Cash Equivalents` |
|---|---|---|---|
| `SUB_ASSET_COLORS` (`portal/src/lib/chartColors.ts:279`) | **21** | **0 of 11** | **absent** |
| `SUB_ASSET_CLASS_DISPLAY_MAP` (`HoldingsTab.tsx:136`) | **13** | **0 of 11** — all thirteen are **Models-side segments** (`US Large Cap`, `Short Duration`, …) | n/a |

Negative control `zzz_no_such_key_9999` absent; positive control — the first six keys print as real
Models values. The gold producer emits the **11 GICS sectors + `Cash & Cash Equivalents`**
(`etf_positioning_gold.py:124 SUB_ASSET_CLASS_VOCAB`), and `HoldingsTab.tsx:157` resolves
`SUB_ASSET_CLASS_DISPLAY_MAP[apiSubAssetClass] || apiSubAssetClass`, then `:127` looks the result up
in `SUB_ASSET_CLASS_COLORS`.

> **So every ETF holding's `sub_asset_class` misses BOTH lookups today and falls through to whatever
> the fallback is.** ⛔ **WHETHER THAT RENDERS WRONG IS UNMEASURED.** There may be a deliberate
> computed fallback that is entirely correct. **A map-key measurement and a render measurement are
> DIFFERENT PLANES, and no control inside the first can answer the second.**

**YOUR ORACLE IS A SCREENSHOT, NOT A GREP** — `/frontend-dev`, ETF mode, the Holdings tab and the
summary panel, read against the **silver-canvas colour law**. Report what you SEE.

⚠ **AND THIS MEASUREMENT FALSIFIED MY OWN HYPOTHESIS, which is why it is framed as a question.** I
predicted that C3's move from 11 sectors to ~24 industry groups would **break** the colour map. **It
cannot** — the map was never keyed on the ETF vocabulary at all. **C3 is cheaper than I feared on
that axis, and a pre-existing question fell out instead.** If your render shows the fallback is fine,
**say so and Z-S-G closes as a non-finding** — *the reason it is not a finding is more useful than
the finding would have been.*

## ⛔ AMENDMENT 1 (21:0xZ, BEFORE GO) — `T5-2` IS ALREADY ANSWERED, AND THE ANSWER IS A THIRD THING

`0.4.0_DE_ClientPlatform~Z` rendered it under CTO~Z's earlier direction before this TO reached them.
**`INGEST-TO5-AC1` is DISCHARGED at issuance** — evidence: their msg 5042, portal vintage `d43b88c5`,
the REAL artifact as fixture (`platinum/etfs/positioning_data.json`, 76,149 B, 2026-08-24T12:30:47Z
s3api/UTC, negative control 404).

**THE VERDICT — neither prediction, and the screenshot is why:**
- ✅ **THE LABELS ARE FINE.** Every GICS name renders in full and correctly spelled. The display-map
  miss is **harmless** because the fallback chain ends in `return apiSubAssetClass` — the raw value
  survives to the page. **Nothing is mislabelled.**
- ❌ **THE COLOUR CHANNEL IS DEAD.** `getAssetClassBgColor` (`Attribution/constants/holdings-shared.tsx:99-104`)
  returns `SUB_ASSET_CLASS_COLORS[sub]` when present, **else** `ASSET_CLASS_COLORS[assetClass]`. At
  **0 of 11** coverage all 110 equity rows fall to the same `ASSET_CLASS.equity` fill: the SUB ASSET
  column is one flat blue, and the composition treemap paints every tile identically. **In Models mode
  that colour is the DISCRIMINATING channel; in ETF mode it carries zero information.**

> **SO IT DOES NOT RENDER *WRONG*. IT RENDERS *UNDIFFERENTIATED*.** The lookup census predicted
> breakage; the fallback chain predicted harmlessness; **the page shows correct text with a dead
> colour dimension.** Neither grep could have produced that answer.

⚠ **AND THEY FOUND A THIRD TABLE MY MEASUREMENT MISSED.** I cited two maps; there are **three**, and
the one I missed is **the mechanism site**: `SUB_ASSET_CLASS_COLORS` at
`Attribution/constants/holdings-shared.tsx:71` (21 keys, 0 of 11). **My two-map figure was a FLOOR I
presented without saying so.** Colour law: PASS on the silver canvas.

⚠ **TODAY the miss is UNREACHABLE** — the route is committed-not-deployed, so ETF mode shows the
cause-agnostic "not available yet" notice and nothing renders. **A verdict taken today would have
read "harmless" and would have been harmless FOR THE WRONG REASON.** Using the live artifact as the
fixture is what made the answer real.

## ⛔ AMENDMENT 2 (21:0xZ, BEFORE GO) — `T5-1` IS **TWO ACTS**, AND MY ORIGINAL SCOPE HAD ONE

DE~Z's consequence, adopted verbatim in substance: **C3's 24 `GICS_INDUSTRY_GROUP_NAME` values will
miss the same three tables exactly as the 11 do now.**

> ⛔ **A T5-1 BUILD THAT ONLY SWAPS THE FIELD INHERITS THE DEAD COLOUR CHANNEL AT FINER GRAIN — 24
> undifferentiated values instead of 11, which is STRICTLY WORSE, because the finer the axis the more
> the colour channel was carrying.**

**So `T5-1` is scoped as two halves and `AC6` is added for the second:**
1. **the field swap** — the additive pull + the gold row carrying it (not yours; DS/vehicle lanes);
2. **a COLOUR/VOCABULARY ACT for the new values** — ⛔ **a Rule 24 AUTHORING EVENT.** Per the
   2026-08-20 widening, **PROPOSING values to an existing axis is itself an authoring act** requiring
   the four-postulate test **and** a token-hygiene census.

**DE~Z is NOT minting that vocabulary and neither am I** — they named it so this TO could scope it
deliberately instead of having it discovered mid-build. **That is the surprise channel working as
designed: an executing seat surfaced a scope gap in my spec and did not fix it off their own bat.**

## `INGEST-T5-1` — condition (ii), and its dependency is NOT YOURS

**What C3 asks for: BOTH vocabularies on the DEV build, side by side, so Andrew can point at one.**
Not a swap — a comparison surface. `HB_INDUSTRY_SECTOR_ALLOCATION` labels (e.g. `"Health Care
(Equity)"`, 10–14 per fund) are **already landing** in
`bbg/{as-of}/constituents/derived_sector_allocation.csv`.

⛔ **THE BLOCKING DEPENDENCY, MEASURED: `GICS_INDUSTRY_GROUP_NAME` IS NOT PULLED TODAY.**
`etf_daily_pull.py:141` requests `EQY_DVD_YLD_IND_NET, BETA_ADJ_OVERRIDABLE, GICS_SECTOR_NAME,
CNTRY_OF_DOMICILE, CUR_MKT_CAP` — confirmed against the landed `characteristics.csv` header. The
finer field is **additive to that file**, which is **mid-L1-2-streak** and therefore **A2-sequenced**;
the gold holding row then has to carry it (`INGEST-T3-6`, DS-class, a Rule-24 act at a second grain).
**None of that is yours. Do not wait idle on it — do `T5-2` and the fixture work below.**

### ⛔ AND THE FIELD-LIST EDIT CARRIES A HAZARD SOMEONE ELSE MEASURED — RE-CHECK IT, DO NOT INHERIT IT

`0.0.0_AB_MSTR~Z` measured that a missed L1 day is survivable partly because `characteristics`'
**fast-moving** members (`TOTAL_NUMBER_OF_HOLDINGS_IN_PORT`, `FUND_PCT_TOP_TEN_HOLD`) are
**independently captured by the constituents leg**.

> **THAT IS AN OVERLAP, NOT A MECHANISM. It can lapse silently the day either field list is edited,
> and NOTHING ENFORCES IT — and C3's ruling edits exactly that field list, this round, by us.**

So when the additive field lands, **the overlap is re-checked at that edit rather than assumed to
survive it.** Whoever makes the edit owns the re-check; you carry it here so it is not discovered
later as a gap. *(This is why it is in a TO and not in the decomp: I froze the certified run and said
I would not silently edit it — the constraint belongs where it is executable.)*

## Acceptance criteria

| id | criterion | cell_refs | grounding layer |
|---|---|---|---|
| **`INGEST-TO5-AC1`** | ⛔ **RENDER IT AND READ THE SCREENSHOT.** `/frontend-dev`, ETF mode, Holdings tab + summary panel. Report what a `sub_asset_class` cell actually shows and what colour it gets. **Answer Z-S-G: is the fallback correct, degraded, or wrong?** A grep is not an answer to this criterion | `INGEST-T5-2` | **EXERCISED (render)** |
| **`INGEST-TO5-AC2`** | **Enumerate the render + lookup sites with a printed denominator**, and state which are **ETF-mode-only** vs **SHARED WITH MODELS MODE**. ⛔ **A token census is a FLOOR — pair it with a structural pass** (the round-1 lesson: a quote-delimited pattern found 5 of 12 membership sites and read CLEAN) | `INGEST-T5-2` | **SOURCE, two instrument classes** |
| **`INGEST-TO5-AC3`** | ⛔ **MODELS MODE BYTE-IDENTICAL — the inherited sovereign constraint.** ETF and Models render through the **same components**, so any change here can move Models. Byte-diff the Models-mode payload/render pre- and post-change. **This is ETFS_POSITIONING's constraint and it binds you** | `INGEST-T5-1`, `INGEST-T5-2` | **EXERCISED** |
| **`INGEST-TO5-AC4`** | **Condition (ii): BOTH vocabularies rendered SIDE BY SIDE on the DEV build** — `GICS_INDUSTRY_GROUP_NAME` beside the Bloomberg `HB_INDUSTRY_SECTOR_ALLOCATION` labels, **for him to point at.** ⛔ **NOT a swap.** Screenshot is the deliverable. **Gated on the field landing — declare KNOWN-UNREACHABLE with one line if it has not, rather than leaving the criterion silently open** | `INGEST-T5-1` | **EXERCISED (render)** |
| **`INGEST-TO5-AC6`** | ⛔ **THE COLOUR/VOCABULARY ACT FOR THE NEW VALUES — the second half of `T5-1`.** Either (a) the ~24 `GICS_INDUSTRY_GROUP_NAME` values get colour coverage across **all THREE tables** (`holdings-shared.tsx:71`, `chartColors.ts:279`, `HoldingsTab.tsx:136`) with a **Rule 24 four-postulate record + token-hygiene census**, since proposing values to an existing axis IS an authoring act; **or** (b) you state, with the render as evidence, that the colour channel is deliberately not carried at this grain and **what replaces it as the discriminating dimension.** ⛔ **WHAT IS NOT ACCEPTABLE IS SHIPPING 24 UNDIFFERENTIATED VALUES SILENTLY** | `INGEST-T5-1`, `INGEST-T5-2` | **EXERCISED (render) + SOURCE** |
| **`INGEST-TO5-AC7`** | **Land the three screenshots somewhere durable for Andrew to point at**, not a session-scoped scratchpad. Name the path in your report. *(You asked where; this criterion is the answer — put them under your own `deliverables/` and cite them, since the DEV render IS the artifact condition (ii) is judged on.)* | `INGEST-T5-2`, `INGEST-T5-1` | **ARTIFACT** |
| **`INGEST-TO5-AC5`** | **The overlap re-check** (above) is performed at the field-list edit, or explicitly handed to whoever makes that edit **by serial**, with the two fast-moving field names stated. **A hand-off names a person; "someone should check" is not a hand-off** | `INGEST-T5-1` | **SOURCE** |

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-transform schema-check HoldingsTab</run>
      <expect>Every rendered field present in the TypeScript type. MISSING = runtime undefined.</expect>
      <if_mismatch>STOP. A MISSING field is a runtime undefined on a page Andrew is watching; surface to COO~Z.</if_mismatch>
    </step>
    <step>
      <run>comp-transform ternary-audit HoldingsTab</run>
      <expect>The mode-branching sites. This IS the fix list for any new cohort/mode value — encode it, do not re-derive it.</expect>
      <if_mismatch>If a branch handles Models and not ETF (or vice versa), that is AC3's blast radius; report before editing.</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions</run>
      <expect>No new query-key collision if you introduce any new state (a vocabulary toggle for the side-by-side render would be new state).</expect>
      <if_mismatch>Resolve the key before writing the component.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>bunx tsc -b (portal)</run>
      <expect>ZERO typescript errors. Portal main worktree stays on DEV (Rule 19) — if you find it on PROD, `git checkout DEV` before any work.</expect>
      <if_mismatch>Do not commit. Zero-tsc is the portal gate.</if_mismatch>
    </step>
    <step>
      <run>/frontend-dev render, both modes</run>
      <expect>Silver-canvas colour law clean; Models mode visually unchanged (AC3's companion — the byte-diff is the hard evidence, the render is the sanity read).</expect>
      <if_mismatch>STOP. A grep cannot see contrast; only the screenshot can.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>comp-transform schema-check HoldingsTab (re-run)</run>
      <expect>Same field set as Phase 1 plus anything you deliberately added. No new MISSING.</expect>
      <if_mismatch>Surface to COO~Z.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<proof_of_spec>
  <!-- ISSUANCE half (COO~Z). POSITIONAL — no --expected-criteria flag:
         python .tools/proof-of-spec-check.py <instance>.json INGEST-TO5-AC1,INGEST-TO5-AC2,INGEST-TO5-AC3,INGEST-TO5-AC4,INGEST-TO5-AC5
       ⛔ CHECK THE RC, NEVER THE OUTPUT STRING; take it WITHOUT A PIPE. Coverage diff is BIDIRECTIONAL,
       so AC4 needs a row even if it lands KNOWN-UNREACHABLE — an expected id with no row refuses the
       whole instance. -->
  <criterion id="INGEST-TO5-AC1" cell_refs="INGEST-T5-2"/>
  <criterion id="INGEST-TO5-AC2" cell_refs="INGEST-T5-2"/>
  <criterion id="INGEST-TO5-AC3" cell_refs="INGEST-T5-1, INGEST-T5-2"/>
  <criterion id="INGEST-TO5-AC4" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO5-AC5" cell_refs="INGEST-T5-1"/>
  <criterion id="INGEST-TO5-AC6" cell_refs="INGEST-T5-1, INGEST-T5-2"/>
  <criterion id="INGEST-TO5-AC7" cell_refs="INGEST-T5-2, INGEST-T5-1"/>
  <expected_criteria>INGEST-TO5-AC1,INGEST-TO5-AC2,INGEST-TO5-AC3,INGEST-TO5-AC4,INGEST-TO5-AC5,INGEST-TO5-AC6,INGEST-TO5-AC7</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DE_ClientPlatform/deliverables/ETFS_INGEST.TO-5_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Premise oracles — run at pickup

| premise | the read that falsifies it |
|---|---|
| the colour map has no GICS keys | extract `SUB_ASSET_COLORS`' keys (`chartColors.ts:279`) → **21 keys, 0 of the 11 GICS sector names**; run a negative control key AND print a few real keys as the positive |
| the display map is Models-side | extract `SUB_ASSET_CLASS_DISPLAY_MAP` (`HoldingsTab.tsx:136`) → **13 keys, all Models segments** |
| the producer emits GICS sectors + cash | `sed -n '108,125p' data/etfs/scripts/gold/etf_positioning_gold.py` → `SUB_ASSET_CLASS_VOCAB` |
| the finer field is NOT pulled | `head -1` the landed `bbg/{as-of}/characteristics.csv` → **no `GICS_INDUSTRY_GROUP_NAME` column** |
| the Bloomberg labels ARE landing | `bbg/{as-of}/constituents/derived_sector_allocation.csv` → `sector_name` values like `"Health Care (Equity)"` |
| ⚠ the token `GICS` is absent from the Positioning plane | `comp-find -i "GICS" portal/src` → **5 hits / 412 files, ZERO in `pages/Positioning/`.** *His "GICS replaced" is a VALUE change, not a token to find — do not go looking for a string to edit* |

## Standing constraints

- **Portal main worktree stays on DEV, always** (Rule 19). **DE commits portal; DT pushes.** You do
  not push, and **you do not promote** — the promote is HELD on his two conditions and the word is his.
- **NEVER#3 / no served-key moves.** The platinum artifact and its route are not yours to change.
- **No alarm, no SNS, no SES, no monitor.**
- **Commit to your own lane; do NOT push.** Report as **"landed LOCAL @hash, rides integration"** —
  never a bare "landed".
- **Read the number, then write the sentence.**
- **Surprise channel:** `org/surprise_channel/ETFS_INGEST/` (`3.0.0_SA_CVO~Z`), coordinate `-Z-S{n}`.
  **OBSERVATION never interrupts; BLOCKING routes same-turn to me, cc CVO~Z; ARMED names a disarm
  owner same-turn. DISARMED ≠ REMEDIATED.** Mid-round the spec is **FROZEN** — route, do not adjudicate.
- **Status moves with the act, by you, in the same turn.**

## What "done" is here — stated because condition (ii) is easy to over-read

**Done is: Andrew can look at the DEV build and point at the vocabulary he wants.** It is **not**
"we picked one", and it is **not** the promote. C3 ruled the *candidate* and the *comparison surface*;
**the choice between the two rendered vocabularies is still his**, and so is the promote after it.
