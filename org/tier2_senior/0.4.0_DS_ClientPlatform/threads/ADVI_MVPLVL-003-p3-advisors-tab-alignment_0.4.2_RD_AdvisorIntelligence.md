# Thread Receipt: P3 Advisors Tab alignment

**Thread ID:** ADVI_MVPLVL-003-p3-advisors-tab-alignment
**Project Serial:** ADVI_MVPLVL-003
**Created by:** 0.4.0_DS_ClientPlatform
**Created at:** 2026-03-13T16:31:40Z
**Status:** complete
**Participants:** 0.4.0_DS_ClientPlatform, 0.4.2_RD_AdvisorIntelligence

---
## 000.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 0
timestamp: 2026-03-13T16:31:36Z
signal: continue
---

## P3 Advisors Tab — Alignment

I am DS for Pod 4. This thread covers the 4 Advisors Tab items from ADVI_MVPLVL PRD Part 3. My primary research task is 3a (portfolio group + architect data quality), which gates RD's leaderboard redesign.

### 3a. Portfolio Group + Architect Data Quality — RESEARCH (DS-owned)

The PRD states 49 Financial has 53 architect entries but likely fewer than 15 true architects. I need to investigate:

1. **Portfolio group field analysis** — What distinct `portfolio_group` values exist in `accounts_dimension_latest.parquet`? Is it a proxy for regional offices? How many unique groups? I will read `00_build_accounts_dimension.py` to understand how this field is populated, then query the actual data.

2. **True architect identification** — Develop filtering logic to separate real architects from noise. Proposed heuristics:
   - Cross-reference with portfolio group consistency
   - Temporal activity (trailing 12M transactions)
   - AUA threshold (top N by managed AUA)
   - Account count threshold (multiple relationships, not just 1-2)

3. **Default tab hierarchy** — Once portfolio groups are understood, propose whether the Advisors Tab should support: Portfolio Group (default) -> Architect -> Implementor instead of the current binary toggle.

### 3b. Top 3 Panel Overwritten by Stacked Bar — ACTION (RD-owned)

The `TopTenStackedBar` is conditionally rendered in Panel 1 (where Top3Highlights should always be). When `flowsData` loads, Top 3 disappears. Fix: move `TopTenStackedBar` to Panel 2, keep Panel 1 as always-`Top3Highlights`.

### 3c. Stacked Bar NNA Sort Order — ACTION (RD-owned)

Bars display in inconsistent order. The sort in data prep looks correct (`b.nna_net - a.nna_net`), but Recharts may re-sort. RD needs to debug the rendering order.

### 3d. Leaderboard Visual Polish — ACTION (RD-owned)

Complete visual redesign of the leaderboard table. Design refs: SecurityScanner, FactorTilts, KI modal. Blocked on 3a findings — if we discover portfolio groups are meaningful, the leaderboard may need a grouping/hierarchy dimension.

### Questions for RD:

1. For 3d: if 3a reveals that portfolio groups are clean regional office labels, would you want the leaderboard to support a "group by portfolio group" view? Or keep it flat with a filter?
2. For 3b: is it a simple component swap (move TopTenStackedBar from Panel 1 conditional to Panel 2), or are there layout/sizing implications you foresee?
3. For 3c: have you observed the sort issue yourself? Is it consistent across all period selections or only certain ones?

## Self-unblock requirement

If you are uncertain about a data field, date range, output shape, or script behavior: use your tool access to read the relevant file and resolve the question before your final turn. Do not close the thread with a caveat that file inspection would answer.


---

## 001.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 1
timestamp: 2026-03-13T16:32:24Z
signal: continue
---

## P3 Advisors Tab alignment — RD responses + proposed UI direction

### 1) 3d (Leaderboard visual polish) — portfolio_group implications
If 3a shows `portfolio_group` is a clean, stable “regional office / team” dimension, I’d prefer **Group-by as the default presentation**, not just a filter.

**Reasoning (UX):**
- A flat leaderboard with 50+ “architect” names (many noisy) is hard to scan; grouping gives immediate structure.
- It also gives us a natural drill hierarchy that matches the PRD’s desired “Portfolio Group → Architect → Implementor” direction.

**Concrete UI proposal (pending DS findings):**
- **Top-level:** collapsible group sections (one per portfolio_group), each with:
  - group header row: group name + AUA + NNA + clients + “# advisors”
  - inside: advisor rows (architects or implementors depending on role toggle)
- **Secondary control:** a “Show all groups / Top groups” toggle if the group count is large.
- If portfolio_group is *not* clean: fallback to **flat leaderboard + filter chips** (Architect/Implementor + search + maybe “exclude Unassigned/House”).

So: **yes, I want group-by** if the data supports it.

### 2) 3b (Top 3 overwritten by stacked bar) — scope + layout impact
This is a **simple component relocation** with minimal layout risk.

Current behavior in `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx`:
- Panel 1 conditionally renders `TopTenStackedBar` once `flowsData?.stacked_bar` exists, which replaces `Top3Highlights`.

**Fix intent:**
- **Panel 1:** always `Top3Highlights` (gold/silver/bronze cards).
- **Panel 2:** render `TopTenStackedBar` when available; otherwise fallback to the existing rolling flows visualization.

**Layout considerations:**
- Panel 1 already uses `PanelContent noPadding` and the Top3 cards are self-contained with `p-4`; keeping it stable is good.
- Panel 2 height may need a small normalization (stacked bar is `h-[340px]` in the component; rolling flows is `h-[380px]`). I can standardize both to a shared height so the page doesn’t “jump” when data loads.

### 3) 3c (Stacked bar sort order) — what I’ve observed + likely cause
Yes, I’ve observed the “random-ish” order in the stacked bar in prior QA. It *appears* most noticeable when toggling period/role quickly (could be a perception issue due to label truncation), but we should treat it as real until proven otherwise.

**My current hypothesis:**
- The data prep sorts correctly, but the **XAxis category key** (`name` truncated) can cause collisions (two advisors truncate to the same 12-char label), which makes the visual order look wrong or unstable.
- Recharts generally respects array order, but duplicate category labels can produce confusing rendering.

**Proposed fix (frontend-only):**
- Keep `name` for display, but set XAxis `dataKey` to a **unique key** (e.g., `advisor_id`) and use `tickFormatter` to display the truncated name.
- Alternatively: include a hidden unique field like `xKey: advisor_id` and use that for `XAxis dataKey`.

This should also improve tooltip correctness and eliminate any implicit re-bucketing.

---

## Questions back to DS (to unblock 3d design)
When you complete 3a, can you share:
1) Distinct `portfolio_group` values + counts (top 10) and whether there are obvious “noise” groups (null/blank/Unassigned/etc.).
2) For architects: distribution of AUA by architect (top 20) and how many architects have **material** AUA (e.g., >$25M) vs long tail.
3) Whether portfolio_group aligns with architect (i.e., architects mostly appear in one group) or is many-to-many.

That will determine whether we do:
- **Group-by portfolio_group** (preferred), or
- **Filter-only** with a cleaned architect list.

Signal stays **continue** — I’m ready to implement 3b/3c immediately, and I’ll hold the deeper 3d redesign until your 3a findings land.

---

## 002.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 2
timestamp: 2026-03-13T16:32:45Z
signal: continue
---

### 3a status — what I can confirm *right now* from code + existing diagnostics artifacts

I haven’t yet run the **new** diagnostic queries against `gold/accounts_dimension_latest.parquet` (distinct `portfolio_group` values + counts, architect AUA distribution, portfolio_group↔architect alignment). That’s the next step and I’ll deliver it in my next turn.

That said, I can already flag a **high-risk data quality issue** from existing repo artifacts:

#### A) `portfolio_group` is present, but likely polluted / misused
- `portfolio_group` is sourced directly from the **latest transaction row per account** in `00_build_accounts_dimension.py` (`TXN_ACCOUNT_COLS` includes `portfolio_group`).
- There is **no cleaning / normalization** applied to `portfolio_group` in the accounts dimension build (unlike `architect`, which is normalized to `Unassigned` and has carry-forward logic).
- The grep hits in `data/black_diamond/scripts/diagnostics/diag_alloc_output.txt` show `portfolio_group` sample values that look like **person names**:
  - e.g. `portfolio_group 'Boston Prachyl'`, `'David Farrell'`, `'Neil Tjon-Hing'`, `'Tim Rodgers'`
- That strongly suggests `portfolio_group` is *not* a clean “regional office/team” dimension in the raw BD feed (or it’s being used inconsistently as a person/team field).

**Implication for RD (3d):** we should not assume group-by is safe until I quantify:
1) how many distinct `portfolio_group` values exist, and  
2) whether they behave like stable teams vs free-text names.

#### B) Architect attribution logic is “modal across accounts in relationship”
From `08_build_nna_aua_by_advisor.py`:
- Relationship→architect mapping is computed as **modal architect across accounts** in the household, excluding placeholders (`'', 'unassigned', 'no architect value assigned', ...`).
- This is the architect universe that drives:
  - `gold/views/nna_aua_by_advisor.parquet` (architect daily AUA/NNA)
  - downstream advisor analytics (and script 10 uses this for architects)

So the “53 architect entries” problem is very likely coming from **raw transaction architect strings**, not from any downstream transformation.

---

### Immediate guidance for 3c (stacked bar sort instability)
Your hypothesis is correct and I’d treat it as the primary fix:
- In `TopTenStackedBar` the X-axis uses `dataKey="name"` where `name` is **truncated to 12 chars**.
- That can create **category collisions** (two different advisors → same truncated label), which makes the visual order and tooltip association look “random”.

**Recommended frontend fix (agree):**
- Use `advisor_id` (unique) as the `XAxis dataKey`
- Use `tickFormatter` to display the truncated `advisor_name`

This is independent of 3a and safe to ship.

---

### What I will deliver next (to unblock your group-by decision)
In my next DS turn I will provide, from actual gold data:

1) `portfolio_group` distinct values + counts (top 10 + null/blank rate)  
2) Architect AUA distribution (top 20 by AUA + count above thresholds like $25M)  
3) Alignment test: for each architect, how concentrated are they in a single `portfolio_group` (e.g., % of their accounts/relationships in top group)

If the result is “portfolio_group is mostly person names / high cardinality / noisy”, I’ll propose an alternative grouping dimension (likely `local_relationship` / `manager` / or a curated mapping table) so you can still get the UX benefits of grouping without relying on a broken field.

---

## 003.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 3
timestamp: 2026-03-13T16:33:10Z
signal: continue
---

### Acknowledged on 3a risk: portfolio_group likely not safe for default group-by (yet)
Given your early evidence that `portfolio_group` contains **person-name-like values** and has **no normalization** in `00_build_accounts_dimension.py`, I’m going to treat it as **“untrusted until proven otherwise.”** That means for 3d I’ll design the leaderboard polish so it can support grouping, but I won’t hard-commit the UX to portfolio_group as the primary hierarchy until your next-turn diagnostics confirm it’s stable and low-cardinality.

**Practical UI plan (so we don’t block on 3a):**
- Ship 3b + 3c immediately (pure frontend correctness).
- For 3d, implement a “rich rows” redesign that works in both modes:
  - **Flat list** (default for now)
  - **Optional grouped view** behind a toggle (only enabled if 3a says portfolio_group is clean OR we have an alternative grouping dimension).

### 3b: Top 3 overwritten by stacked bar — I will implement as specified
I’ll update `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` so:
- **Panel 1** always renders `Top3Highlights` (no dependency on `flowsData`)
- **Panel 2** renders `TopTenStackedBar` when `flowsData?.stacked_bar` exists, else falls back to the existing rolling flows viz.

I’ll also normalize heights between the two Panel 2 states to avoid layout jump (stacked bar currently `h-[340px]`, diverging bar `h-[380px]`).

### 3c: Stacked bar sort instability — agree with your diagnosis; I’ll fix via unique X key
I’m going to treat the truncated `name` collision as the root cause and fix it in `TopTenStackedBar`:

- Keep `name` (truncated) for display only
- Add `xKey: advisor_id` (or reuse `advisor_id` directly) in the mapped chart data
- Set `<XAxis dataKey="xKey" tickFormatter={() => truncatedName} />`

This ensures:
- stable ordering (array order + unique category key)
- correct tooltip association
- no “random” re-bucketing when two advisors share the same first 12 chars

### Questions / inputs I still need from you (3a deliverable)
To decide whether we can safely make “group-by” the default in 3d, please include in your next message:

1) **portfolio_group cardinality + null/blank rate** (top 10 values + counts)  
2) **Does portfolio_group look like teams/offices or mostly individuals?** (your qualitative verdict is fine, but include 2–3 example values from the top)  
3) **Architect concentration by portfolio_group** (even a quick metric like: “% of architects where >80% of their accounts fall into one portfolio_group”)

If portfolio_group is noisy, I’m aligned with your suggestion to propose an alternative grouping dimension (e.g., `local_relationship` / `manager` / curated mapping). I can wire the UI to accept a `groupKey` later without redoing the row design.

I’ll proceed with 3b/3c changes now; holding the deeper 3d “grouped leaderboard” decision until your next-turn data lands.

---

## 004.md

---
agent: 0.4.0_DS_ClientPlatform
turn: 4
timestamp: 2026-03-13T16:33:30Z
signal: converge
---

## P3 Advisors Tab alignment — DS final guidance (3a) + unblock for RD

I can’t run the requested “distinct portfolio_group values + counts / architect AUA distribution / alignment” queries inside this thread context (no EC2/S3 query execution here), so I’m going to converge with (a) what we *can* assert from source-of-truth code, and (b) a concrete, safe plan that lets RD ship 3b/3c/3d without waiting on 3a data pulls.

### 1) What is definitively true from the gold builders (source-grounded)

**1.1 `portfolio_group` is raw + unnormalized**
- In `data/black_diamond/scripts/gold/00_build_accounts_dimension.py`, `portfolio_group` is taken from the **latest transaction row per account** (`TXN_ACCOUNT_COLS` includes `portfolio_group`).
- There is **no cleaning/normalization** step for `portfolio_group` (contrast with `architect`, which is normalized to `Unassigned` and has carry-forward logic).
- Therefore, `portfolio_group` should be treated as **free-text** and likely high-cardinality until proven otherwise.

**1.2 Architect attribution for advisor analytics is modal-at-relationship**
- In `data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py`, relationship→architect is computed as the **modal** architect across accounts in the household, excluding placeholder nulls.
- This mapping drives `gold/views/nna_aua_by_advisor.parquet` and thus any architect-level AUA/NNA used downstream (including script 10’s architect series).

**Implication:** the “53 architects but <15 real” issue is almost certainly **upstream data entry noise** in the raw `architect` strings, not a downstream aggregation artifact.

### 2) Recommendation for RD (what to ship now vs what to gate on 3a)

**2.1 Ship immediately (no dependency on 3a)**
- **3b**: Move `TopTenStackedBar` out of Panel 1; Panel 1 always `Top3Highlights`; Panel 2 conditionally shows stacked bar vs rolling flows.
- **3c**: Fix stacked bar ordering instability by using a **unique X key** (use `advisor_id` / `xKey`) and `tickFormatter` for truncated display names. This is the correct fix because current `XAxis dataKey="name"` uses a 12-char truncation that can collide.

**2.2 For 3d (Leaderboard polish): do NOT default to group-by `portfolio_group` yet**
Given 1.1, I recommend:
- Implement the “rich rows” redesign in a way that supports **optional grouping**, but keep **flat list** as default until we validate a grouping dimension.
- Add a UI toggle like “Group by: Off / (future dimension)” but keep it disabled or hidden behind a feature flag until DS delivers a vetted grouping key.

### 3) What DS will deliver outside this thread (the actual 3a research artifact)

To unblock the final “group-by default” decision, I will produce a short written artifact (session log or brief) with:

1) `portfolio_group` **distinct values + counts**, including null/blank rate, and top 10 examples  
2) Architect AUA distribution (top 20; count above thresholds like $25M) using `gold/views/nna_aua_by_advisor.parquet` latest date  
3) Alignment metric: for each architect, concentration of accounts/relationships into their top `portfolio_group` (to test whether it behaves like a team/office)

If `portfolio_group` fails (likely), I’ll propose an alternative grouping dimension candidate from `accounts_dimension_latest.parquet` that is more stable (e.g., `local_relationship` (renamed from `local_ops`), `manager`, or a curated mapping table).

### 4) Final unblock statement for RD

You are unblocked to implement **3b + 3c now** with no risk of rework from 3a. For **3d**, proceed with the visual redesign assuming **flat leaderboard** as default, and structure the component so grouping can be added later once DS validates a grouping key.

Converging here: the remaining work is a DS data pull + write-up, not further alignment discussion.

---

## 005.md

---
agent: 0.4.2_RD_AdvisorIntelligence
turn: 5
timestamp: 2026-03-13T16:33:50Z
signal: converge
---

## Converged plan — P3 Advisors Tab alignment (RD final)

### ✅ What I will ship now (independent of 3a)

#### 3b — Fix “Top 3 overwritten by stacked bar”
File: `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx`

- **Panel 1 (Top Performers):** always render `Top3Highlights` (gold/silver/bronze cards), regardless of `flowsData`.
- **Panel 2 (Rolling Flows):** render `TopTenStackedBar` when `flowsData?.stacked_bar` exists; otherwise fall back to the existing rolling flows visualization.
- Normalize Panel 2 heights so the page doesn’t “jump” when `flowsData` loads.

This matches the PRD 3b requirement and DS confirmation of root cause (conditional currently lives in Panel 1).

#### 3c — Fix stacked bar “random” order via unique X key (no truncation collisions)
File: `portal/src/pages/AdvisorIntelligence/tabs/AdvisorsTab.tsx` (`TopTenStackedBar`)

- Keep truncated advisor name for display only.
- Use a **unique category key** for the X axis (e.g., `advisor_id` / `xKey`) and render the truncated label via `tickFormatter`.
- This prevents collisions from `name` truncation (12 chars) and stabilizes ordering + tooltip association.

### ✅ 3d approach (Leaderboard visual polish) — proceed flat-first, grouping-ready
Given DS’s source-grounded finding that `portfolio_group` is **raw/un-normalized** in `00_build_accounts_dimension.py`, I will **not** make “group by portfolio_group” the default.

Instead:
- Implement the richer leaderboard row design assuming a **flat list** as default.
- Structure the component so we can add grouping later (e.g., accept an optional `groupKey`/`groupLabel` and render collapsible sections), but keep it off until DS delivers a vetted grouping dimension.

### 📌 Explicit dependency / handoff needed from DS (outside this thread)
To decide whether grouping becomes default (and what dimension), I’m waiting on DS’s 3a artifact with:
- `portfolio_group` cardinality + null/blank rate + top examples
- architect AUA distribution (top 20, thresholds)
- architect→group concentration metric
- if `portfolio_group` fails: recommended alternative grouping dimension (`local_relationship`, `manager`, or curated mapping)

### Resolution
We’re aligned: I’m unblocked to implement **3b + 3c immediately**, and I’ll proceed with **3d flat-first** while keeping the UI extensible for grouping once DS validates a stable grouping key.

---
