# ADVI_BDPARITY.P1-PROBE BP1-1 -- the pull extension, BUILT and RULED-CONFORMANT, awaiting an AE lane to land it

**Seat:** `0.4.0_DS_ClientPlatform~C` | **Clock:** 2026-08-30T01:5xZ (read) | **TO:** `ADVI_BDPARITY.P1-PROBE`, AC **BP1-1**

> **AMENDED 01:5xZ, same session.** The first version of this note described a `raise`-on-missing-anchor
> and then an OMIT-the-SI-range behaviour. **Both are superseded** by `3.0.0_SA_CVO` 84169 and the
> measurement that forced it (section 3 below). The superseded text is not preserved here because it
> describes behaviour that no longer exists in the file -- what IS preserved is why it changed.

## What this is

The code half of BP1-1. It closes the gap the issuer amendment (2026-08-29T17:5xZ, finding **A2**)
recorded: the ruled period set **QTD / YTD / 1Y / SI** is not obtainable from the payload builder as
drafted, which emitted `Custom` + two trailing **calendar years** + `SinceInception`.

**Subject file:** `infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py`
**Patch:** `ADVI_BDPARITY_BP1-1_pull_extension_20260830.diff`
**Probe:** `ADVI_BDPARITY_BP1-1_builder_probe_20260830.py` -- **25 of 25 arms, rc=0**

## 1. What changed (5 things)

1. `_trailing_12m_range()` -- **1Y** as a `Custom` with COMPUTED dates. No new BD dateRange type
   needed (A2: *"NOT AT RISK"*). A trailing full calendar year is not a trailing twelve months.
2. `_ytd_ranges()` -- **YTD** as a **Jan-1 `Custom`**, the shape already proven on this endpoint.
   `ytd_mode="typed"`/`"both"` exist but are **not** for the authorized pull (section 3).
3. `return_method` is a **PARAMETER** (default `"Annualized"`, unchanged on the wire) -- methodology
   cell (ii). The ruling lands as a call site, not a code change plus a redeploy.
4. **The SI range is ALWAYS REQUESTED**, with `si_probe_start = inception or q_start`. That start is
   **a PROBE VALUE, NOT AN ANCHOR ASSERTION** -- BD overrides it either way (section 3). The strict
   no-default rule lives on **our linking side**: the SI cell is computed only from the **RETURNED**
   start; no returned start -> `UNAVAILABLE-NO-ANCHOR`, never defaulted.
5. `requested_range_index()` -- exposes the requested ranges **with their array index**, because
   position is the join (section 3).

## 2. The lane position, stated plainly

- `1.0.0_SA_CTO` **83426** (re-read at source, 17:47Z follow-on, verbatim): *"builder edit IN LANE,
  live BD call NOT, and the new ranges carry no reconciliation."*
- **But `safe-commit.sh` REFUSES this lane**: `infra/aws/**` is `CLOUD_OPS_OR_ETL` (*"any AE agent"*),
  and `0.4.0_DS_ClientPlatform~C` is not in `permitted_agents`.
- **These are two different mechanisms and they do not contradict.** CTO settled VENDOR EGRESS; the
  owned-paths gate answers WHICH LANE MAY LAND A FILE. A ruling on one is not a grant on the other.
- **No `GIT_COMMIT_AUTHOR_OVERRIDE` was taken**, though precedent exists on this exact file
  (`f559cbc516`, *"Lane override: WS-1 TO @8bf441b1c"*). A live AE seat owns the lane; taking an
  audited exception when the owner is awake is manufacturing an exception for convenience.

⚠ **WORKING-TREE EXPOSURE.** The change is **UNCOMMITTED and live in the SHARED worktree**, in the
puller every AE seat may touch. `3.0.0_SA_CVO` 84169 item 4(a) recommends it land **before the next
window's deploy leg reads the tree**, because a half-landed builder in a deploy leg is the c02 shape
again. The `.diff` here is the durable copy -- `git apply` it if the working-tree change is lost.

## 3. THE MEASUREMENTS -- all on bytes already in bronze, ZERO vendor calls

**(a) No bronze artifact carries a BD account-inception FIELD.** The reporting bronze prefix holds
exactly **3 objects** (one account, `22596361`, `as_of` 2026-06-30). The performance object has **75
distinct keys and ZERO match `incep`**.

**(b) BD SUBSTITUTES ITS OWN INCEPTION and ignores the `startDate` we send.** Roster
`trade_start_date` = **2026-04-08**; BD returned SI = **2026-03-16 .. 2026-06-30**, 23 days earlier.
Corroborated by a second, independent instrument: that range carries `beginningMarketValue = 0.0`
with `endingMarketValue = 35,073.20` (the signature of an inception), while the 2025 and 2024 ranges
carry BMV **and** EMV of 0.0 (the account did not exist). **This validates cell (i) by mechanism: the
ruled anchor is the one the vendor enforces.**

⛔ **BOUND: n=1, and the requested start was LATER than BD's inception.** The discriminating case --
requested start EARLIER -- is **unobserved**. Face finding **A3 is WEAKENED, NOT CLEARED**: what is
established is that A3's mechanism as written did not occur here. **The face is not amended.**

**(c) BD returns `name: None` and `type: None` on EVERY returned dateRange** -- 4 of 4 distinct
objects, 5,864 occurrences. **A response cannot be joined by label.** Array order IS stable: **1
distinct order signature across all 11 containers**, mapping positionally onto the request array.

**(d) 0 of 10 cohort candidates have a known BD inception** (roster ids `{22596361, 22659431,
23221671}` vs the candidates' `bd_internal_id` space). So the two-pass SI design is **required for
this cohort, not merely preferred** -- there is no anchor to send.

## 4. What `3.0.0_SA_CVO` 84169 ruled off those measurements

- **The discriminator is the triple `(requested_index, returned startDate, returned endDate)`.**
  Position finds the cell; **the dates certify it.** Position alone would let a silently re-ordered or
  dropped range read as a match. The probe **re-checks the order signature on every response** and
  refuses the whole response if it changes (an order change is an instrument failure, not a finding).
- **`ytd_mode="custom"` for the authorized pull.** `"both"` would request two ranges with identical
  dates that BD returns no label to tell apart -- it would spend the authorized pull on an ambiguity.
- **The SI cell is TWO-PASS**: pass 1, the pull returns BD's SI start per account (the anchor census);
  pass 2, our module links from that anchor, **offline, no second vendor call**, with the
  admissibility test (anchor >= our gold coverage start, else `UNAVAILABLE-NO-COVERAGE`).

## 5. Evidence, and the control that found my own bug

**25 of 25 arms, rc=0** (read unpiped). `commit-gate.sh` clean. **`DRY_RUN` remains 1** -- `_request()`
still refuses to open a socket; nothing here makes or enables a vendor call.

**The baseline control.** HEAD's untouched version through the same probe **FAILS** `ruled/YTD-present`,
`ruled/1Y-trailing-12m`, the ruled-set arm (`present={QTD:True, YTD:False, 1Y:False, SI:True}`) and
`ytd/default-is-proven-Custom-shape`.

> **IT CAUGHT A DEFECT IN MY OWN HARNESS.** The ruled-set arm was first written as
> `len(dateRanges) >= 4`. It **PASSED on the baseline** -- which has exactly 4 ranges
> (`Custom`/`2025`/`2024`/`SI`), none of them YTD or 1Y. **A COUNT stood in for a SET and certified
> what it could not see.** Rewritten as a per-period relation. Found by running the baseline, not by
> re-reading the arm.

⚠ **HONEST LIMIT ON THE BATTERY, disclosed rather than discovered later:** the baseline **cannot reach**
the SI/join arms -- it raises `TypeError` on the new kwargs -- so those arms are **not**
baseline-controlled. Their substitute control is a pair that fails from different truths (anchor
present -> 1 SI range at a known index; anchor absent -> the probe-start fallback). `3.0.0_SA_CVO`
84169 graded this **as disclosed, not as a gap**, to be re-read on real bytes at the probe table.

**BOUND: these arms score the PAYLOAD, not a BD response.** Nothing here establishes that BD accepts a
Jan-1 `Custom` as YTD or returns what we mean by 1Y. That is what the authorized pull measures.

## 6. The ask, and who holds it

| # | Item | Holder |
|---|---|---|
| 1 | **Land the patch under an AE lane** (or the issuer authorises the audited override) -- CVO recommends before the next window's deploy leg | a live AE seat / `2.0.0_SA_COO` |
| 2 | Terraform deploy -- code deploy is Terraform-only (CLAUDE.md NEVER), infra is DT/AE (Rule 13) | DT/AE |
| 3 | ~~The two methodology cells~~ **RULED** @`f11fb765ad`, mechanism clarified in 84169 | `3.0.0_SA_CVO` -- **closed** |
| 4 | **Rider-4 probe-account SELECTION -- THE REMAINING GATE.** `4.0.0_SA_CRO` base is NOT LIVE; card D2-T69-R2 at Andrew | `4.0.0_SA_CRO` / Andrew |

**Nothing fires before the cohort is named.** The request is prepared against the cohort candidates
@`9368be5bc4`; the pull fires within the recorded scope (ruled QTD/YTD/1Y/SI, 3-5 accounts, no
schedule, no cadence) and nothing wider.
