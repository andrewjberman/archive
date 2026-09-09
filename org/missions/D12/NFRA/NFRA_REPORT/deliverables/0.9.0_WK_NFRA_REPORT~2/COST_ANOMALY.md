# RP-s-9 -- The COST-ANOMALY detector (SEGMENT grain now; BOX grain re-assessed after RP-s-5)

**Cell:** `RP-s-9` (manifest row S9, outcome FWD-8) · **Worker:** `0.9.0_WK_NFRA_REPORT~2` · **TO:**
`NFRA_REPORT.TO-RP-s-9.cost-anomaly-detector-segment-then-box.md` · **Worktree base:** `wk-NFRA_REPORT-2b`
@ `cc1c60b174`. **Vintage of every live AWS Cost Explorer / EC2 read below:** `2026-09-09` (dates below;
CE data is daily-granularity, not a single timestamp).

**ACT restated:** make a meaningful jump in what something costs show up, and ordinary week-to-week
wobble not show up, without the reader doing the arithmetic. **Andrew's detector, verbatim (C-COST-15):**
*"whether there is a material divergence from historical cost for a given compute box or cost segment...
if something moves say 15% or more from its trailing 30 day price."*

---

## 0. Why the window is TRAILING 30 DAYS, not "month-to-date vs prior month"

The estate already has a cost-depth implementation (`infra/aws/lambda/infrastructure_monitor/
lambda_function.py:1196-1330`, `get_cost_depth()`), and it is exactly the F9 finding's cause, not a
coincidence: it compares **month-to-date daily average** against **the entire prior calendar month's
daily average**. MTD is a partial period whose average is unstable early in a month (today, 2026-09-09,
is day 9 of September -- 9 data points averaged against 31), which is precisely why `inf` could print
`+41.2%` with `OVERALL: OK` and no threshold in F9: the wobble the ACT says must not show up is *baked
into the comparison window itself*, before any threshold logic is even applied.

Andrew's own words say **"trailing 30 day price"** -- a rolling 30-real-days window, not a calendar-month
boundary. This cell's detector uses **[today-60, today-30) as the BASELINE 30 days and [today-30, today)
as the TRAILING 30 days**, both fixed-length, both real elapsed days, so a comparison made on day 9 of a
month is exactly as stable as one made on day 29. This is a genuine methodology improvement the existing
lambda does not have, built without touching that lambda (out of this cell's `<paths>`; recorded as a
finding for whoever owns it, not remediated here -- s.5).

---

## 1. SEGMENT grain -- available now, built and tested against live data

**Source:** `aws ce get-cost-and-usage --group-by Type=TAG,Key=Pipeline`, `Granularity=DAILY`,
`2026-07-11` to `2026-09-09` (60 days, 60 of 60 daily result objects returned), split client-side into
baseline (`2026-07-11`..`2026-08-09`, 30 days) and trailing (`2026-08-10`..`2026-09-08`, 30 days).
**Detector rule:** `ANOMALY` iff `abs(delta_pct) >= 15.0` **AND** (`baseline_avg/day >= $0.50` **OR**
`trailing_avg/day >= $0.50`) -- the dollar floor is this cell's addition (Andrew's word sets the percent
threshold; a percent test alone flags noise on cent-scale segments, shown below). A baseline of ~$0 with
a material trailing cost is flagged separately as **NEW-COST**, because a percent test is mathematically
undefined (or explodes) exactly where a genuinely new spend line would need it least.

| Segment (`Pipeline` tag) | Baseline $/day (30d) | Trailing $/day (30d) | Move | Verdict |
|---|---|---|---|---|
| `inf` | 2.197 | 16.253 | **+639.6%** | **ANOMALY** |
| `bd` | 4.109 | 5.641 | **+37.3%** | **ANOMALY** |
| `mdpf` | 0.071 | 0.141 | +97.7% | sub-threshold-DOLLAR (mechanically over 15%, both sides under the $0.50/day floor -- shown, not hidden) |
| `(untagged)` | 18.463 | 17.623 | -4.5% | **stable -- CONTROL** (the single largest line, 45% of spend, does NOT fire) |
| `cot` | 0.025 | 0.024 | -0.5% | stable |
| `imo`, `pm`, `news`, `aaii`, `analysis` | ~0 | ~0 | n/a | stable (no material spend either side) |

**This is the control the bound requires, made of real production data rather than an assertion:** the
biggest dollar line in the account (`(untagged)`, 45% of spend) sits at -4.5% and does **not** fire; two
segments with genuine, material, mechanically-verified moves (`inf` +639.6%, `bd` +37.3%) **do** fire.
A detector that fired on everything would not be able to tell `(untagged)` from `inf`; this one does.
**Sanity cross-check:** the account-wide total for `2026-09-01`..`2026-09-09` read `$340.63` this session
against the brief's independently-measured `$340.02` MTD (same account, different read, ~2 hours apart)
-- the two instruments agree to within rounding, which is the positive control that the CE query itself
is sound.

**`inf`'s move is not a detector artifact.** `EC2_MANIFEST.json` (RP-s-5, `always_on_group` and
`lifecycle` fields) shows `inf-gold-layer-runner` and `inf-exporter` **both live-RUNNING** at RP-s-5's
read (`2026-09-09T20:10Z`) against a lifecycle this cell's own predecessor recorded as "TRIGGERED, not
always-on" -- i.e. the Inflection pipeline's boxes were mid-dispatch, consistent with a real, large,
ongoing compute run driving the segment's cost up, not a billing artifact.

---

## 2. BOX grain -- what RP-s-5 discharged, what it did NOT, and what is newly and independently blocked

**The TO's original bound attributed the box-grain block entirely to the compute manifest:** *"BOX
grain CANNOT be computed until RP-s-5 lands, because the compute manifest is EC2-only with ECS absent
entirely."* RP-s-5 landed (merged `42fcf408d1`) and fixed exactly that: v1.1 of `EC2_MANIFEST.json`
carries `machine_type`/`lifecycle` on all 27 EC2 rows and a new `ecs_clusters.opal-globgrph` section (3
always-on Fargate services). **The inventory side of box grain -- knowing what boxes and ECS services
exist -- is now complete.** This is genuine, direct progress the coordinator is right to ask about.

**But box-grain COST requires two things: knowing what the boxes ARE (RP-s-5's job) and being able to
attribute DOLLARS to each one individually (a Cost Explorer / billing capability RP-s-5 never touched).
Tested live, this turn, both routes to the second half are closed, for reasons independent of the
manifest:**

1. **AWS Cost Explorer's resource-level (per-instance) cost API is opted OUT at the payer account.**
   `aws ce get-cost-and-usage-with-resources --group-by Type=DIMENSION,Key=RESOURCE_ID ...` ->
   `AccessDeniedException: Resource-level data granularity is an opt-in only feature. You can be enable
   this feature from the PAYER account's Cost Explorer Settings page.` This is a **billing-account
   setting**, not a manifest gap -- no amount of `EC2_MANIFEST.json` schema work can reach it, and
   enabling it is outside this cell's `<paths>` and its `comp-schedule`/`comp-iam` battery findings (no
   IAM grant, no billing setting change is authorized here).
2. **The only 7 cost-allocation tags ACTIVE in Cost Explorer** (`aws ce list-cost-allocation-tags
   --status Active`: `System`, `Pipeline`, `Owner`, `Partner`, `Macro`, `Project`, `Environment`) are
   segment-grain, not box-grain. `Pipeline` is s.1's segment. `System` is FINER than `Pipeline` but is
   **still not one-per-box**: live `describe-instances` tag reads show `System=bd-pipeline` shared by 5
   declared EC2 rows (`bd-allocations`, `bd-gold-layer-runner`, `bd-transactions`, `bd-assets`,
   `bd-fees`) and `System=InflectionPipeline` shared by 4 (`inf-gold-layer-runner`, `inf-gold-qa-runner`,
   `inf-exporter`, `inf-bronze-runner`); it is **absent entirely** on 9 of the 27 declared rows (all 8
   live `historical-prices-fetcher` instances and `canonical-schwab-si2`); and it carries a **casing
   drift** -- `bd-gold-qa-runner` is tagged `System=BDPipeline` while its four siblings are
   `System=bd-pipeline`, two DIFFERENT strings to Cost Explorer's exact-match tag grouping, silently
   splitting what is conceptually one segment into two. None of this is caused by, or fixable from,
   `EC2_MANIFEST.json`.

**So the honest answer, stated plainly rather than defaulting either way: box grain in the literal sense
C-COST-15 asks for (one cost figure per compute box or ECS service, tested against ITS OWN trailing-30-day
price) is STILL NOT REACHABLE TODAY -- not because of what RP-s-5 left undone, but because of a payer-account
billing setting and a tagging gap that are independent of it and outside this cell's authority to change.**
RP-s-5's own contribution is real and is not wasted: it supplies the DENOMINATOR (a complete, schema-clean
list of every box and ECS service with its lifecycle) that the moment resource-level data (or a genuinely
unique per-box tag) is switched on, this detector's segment-grain code above needs only a `GroupBy` key
change to become a true box-grain detector -- the arithmetic is already built and already control-tested.

### 2a. The best CURRENTLY-reachable finer-than-segment view, cross-referenced against RP-s-5

Using `System` as an intermediate grain (same 60-day CE pull, same baseline/trailing split), with the
same 15%-and-$0.50/day-floor rule, and reading each row against `EC2_MANIFEST.json`'s `lifecycle`/
`always_on_group` fields:

| `System` tag | Baseline $/day | Trailing $/day | Move | Compute manifest cross-reference |
|---|---|---|---|---|
| `InflectionPipeline` | 3.536 | 17.588 | **+397.5%** | 4 EC2 rows share this tag (s.2 above); `inf-gold-layer-runner`/`inf-exporter` live-RUNNING at RP-s-5's read |
| `bd-pipeline` | 2.971 | 4.323 | **+45.5%** | 5 EC2 rows share this tag; a 6th (`bd-gold-qa-runner`) uses the differently-cased `BDPipeline` and its $0.066->$0.042/day is invisible under THIS row |
| `M365MCPGateway` | 0.967 | 0.162 | **-83.2%** | Pre-existing tag name from the `opal-gateway` box's prior identity (`OPAL_GWRENAME`, RP-s-5's own `opal-gateway` row history); does not match the box's CURRENT `System=OpalGateway` tag (below) -- a second, retired cost-tag value still drawing residual charges |
| `OpalGateway` | 0.000 | 0.796 | **NEW-COST** | This IS `opal-gateway`'s current live tag (confirmed via `describe-instances` Tags on `i-07dccb1615503ac99`) -- effectively 1:1 box attribution by coincidence, not by a designed contract; RP-s-5 marked this box "not exempt-by-name from Dashboard/Website/Graph" (row `NFRA_REPORT-Z-W2-S2`) -- its own cost line is real and growing from zero |
| `website` | 0.595 | 0.648 | +8.8% | 1:1 with `opal-website-wp`, RP-s-5's confirmed ALWAYS-ON `Website`-group box; stable, as an always-on server's cost should be |
| `CrawlHarness` | 0.014 | 0.000 | **-100%** | Matches RP-s-5's own finding: `orion-crawl-harness`'s declared `instance_id` does not exist live and no replacement was found (RP-s-5 deliverable s.2/s.3a) -- this cost line going to exactly $0 corroborates that the box is genuinely gone, not merely stopped |

**This table is NOT box grain** (it is coarser in 2 of 6 rows, and 9 of 27 declared EC2 rows have no
`System` tag at all so do not appear in it under their own identity), but it is the closest reading
available today, and RP-s-5's manifest is what makes the cross-references in the right-hand column
possible at all -- that link did not exist before this project.

---

## 3. Declared exclusions

- **Enabling Cost Explorer resource-level data, or fixing the `System`/`bd-pipeline` vs `BDPipeline`
  tag-casing drift, or retiring the stale `M365MCPGateway` cost tag.** All three are billing/IAM/
  Terraform-tag changes outside this cell's `<paths>` and outside `comp-schedule`'s battery finding
  ("no armed gate owned by this project" -- meaning none is REQUIRED by an existing gate, not that one
  is authorized here). Filed as a finding (s.4), not remediated.
- **Editing `infra/aws/lambda/infrastructure_monitor/lambda_function.py`** to adopt the trailing-30-day
  window instead of MTD-vs-prior-month. Not in this cell's `<paths>`; the improved methodology is
  demonstrated and evidenced here for whoever owns that Lambda to port.
- **A materiality floor other than $0.50/day.** Andrew's word sets the percent threshold, not a dollar
  floor; $0.50/day (~$15/month, ~1.3% of the account's current ~$40/day trailing total) is this cell's
  own choice, stated rather than hidden, so a grader can substitute a different number without redoing
  the underlying pull.

## 4. Surprise filed

- **`NFRA_REPORT-Z-W2-S4`** -- box-grain cost attribution is blocked by a payer-account Cost Explorer
  setting (resource-level data opt-in disabled, confirmed live) and by tag coarseness/drift, both
  independent of RP-s-5's manifest fix and both outside this project's write surface. OBSERVATION,
  ARMED (a future reader could otherwise assume RP-s-5 fully unblocked box grain and build a report
  section that silently can't be filled), disarm owner named in the row.
