# D9_TAXSMA TO-A — Tax SMA Ops STATE ASSESSMENT (SITEZ, read-only recon)

**Author:** 0.4.0_DS_ClientPlatform~Z · **Date:** 2026-08-19 (measurements 20:03–20:3xZ this session)
**TO:** `org/tier0_exec/0.0.0_AB_MSTR/task_orders/D9_TAXSMA.TO-A-SITEZ.state-assessment-recon.md`
**Kickoff triple:** prd=`docs/architecture/D9_TAX_SMA_OPS_PRD.md` · workstream=(a) §4.1 TO-A only · head_version=`@fac13ccc3a`
**Machine table:** `D9_TAXSMA_TO-A_LIVE_TRUTH_TABLE.json` (beside this file) · **Proof:** `D9_TAXSMA.TO-A_PROOF_OF_SPEC.json`
**Read-only throughout — every contradiction below is a FINDING, nothing was fixed in-pass.**
**Mid-pass ruling folded in (Andrew ~20:12Z, relay @`1e0ec3b079`): the (c1) DAILY-TRACKING leg
is WAIVED ahead of the Yang/Alyssa meeting — cuttable now. The rest of (c) still gates on the
meeting. (c1)-touching rows below carry WAIVED-BY-RULING, not "open-gated".**

## Executive read (the meeting's one-paragraph pre-read)

Everything recorded as built IS built, and almost nothing recorded as built has run since its
build day. The pt1 intake ran once (2026-07-15) while its upstream FIS feed still arrives twice
every trading morning through today — ~24 trading days of SSAVAIL files sit unfiled in the
mailbox. The PT2 producer chain is NEVER-SCHEDULED (exactly 1 lifetime invocation, build-day
2026-07-17; bronze/silver/gold all carry that one vintage; gold serves exactly one account). The
business has outrun the pipeline: the Yang/Alyssa master file (08-13) shows **11 accounts,
$27.71M target, 5 already TRADED on 08-05** — the S3 roster holds 3, the served gold holds 1.
One live surprise runs the OTHER direction: the Andrew+CTO-gated WS-4/WS-R5 IAM roles went LIVE
on 08-15 inside the OPAL_GWRENAME stack apply, with no WS-4 go-live record of their own (grants
verified least-privilege per plan). The gap between records and reality is mostly *cadence and
scale*, not code: the finish line is WS-5 scheduling + multi-account + re-establishing (or
automating) the operator cadence — plus the open sovereign words (accounts resolver egress;
#48 disposition — #42 was ruled SUPERSEDED by D7+D9 mid-pass @`3c8c3f1035`, and the (c1) leg
was WAIVED @`1e0ec3b079`).

---

## Part 1 — LIVE-TRUTH TABLE over run rows B1–B3 (+B4)

Rule-22a layer named per row: DESIRED (repo/TF) · APPLIED (live AWS / live M365) · EXERCISED
(did it run). Full machine form in the JSON beside this file.

### B1 — OPAL_TAXSMA (pt1 intake + guardrails)
| Layer | Verdict | Evidence |
|---|---|---|
| DESIRED | TRUE | `/tax-pt1` skill + Content Contract v1.0 + validator recipe in-repo (`.claude/skills/tax-pt1/SKILL.md`; contract `docs/briefs/OPAL_TAXSMA_SSAVAIL_CONTENT_CONTRACT.md`) |
| APPLIED | TRUE | Validator lives as gateway tool `validate_ssavail_attachment` on the live opal-gateway (tool present in live MCP roster; gateway whoami = Andrew Berman proxy, probed this session). Quarantine (`Flagged Files/`, childCount=1) + shared-cloud log (`Intake Logs/`) EXIST in SharePoint Shared/TAX/Short Sale — listed live |
| EXERCISED | **RAN ONCE — IDLE SINCE 07-15** | Exactly **1** intake log ever (`20260715-183800Z intake-log.md`; Intake Logs folder denominator: 1 file). Canonical folder census: **39 items** — the 07-15 first-live-run+backfill batch (covering 06-29→07-15) + pre-automation manual files (04-06→06-25) + **2 post-07-15 files (08-04, 08-05) with no intake log and no PRELIM pair = manual-placement signature**. Upstream feed **ALIVE through 08-19**: mailbox probe returned FIS forwards 2×/trading-morning (14 SSAVAIL rows of the first 15 search results; more pages exist). Andrew's cadence ruling (`099b1162c8`, verbatim *"Yes B now, we will do A later."*) expected an operator-cadence daily run; it is not being run. |

### B2 — OPAL_TAXSMA_PT2 (BD table chain)
| Sub-claim | Layer | Verdict | Evidence |
|---|---|---|---|
| WS-1 producer deployed | APPLIED | TRUE | `opal-assets-bd49f-reporting-pull` Active, LastModified 2026-07-17T23:06:53Z, python3.12/300s/1024MB (== TF), CodeSha256 `U1ujLtfbIVEjQxW8Fm+Rb8XeioAc2+e99cokHe7yLV8=`. (Member-level deployed-bytes-vs-built-from diff not run — declared exclusion.) |
| Trigger state | ALL 3 | **NEVER-SCHEDULED** | DESIRED: TF declares NO schedule, "MANUAL INVOKE ONLY" (`bd49f_reporting_pull.tf:14,120,140`). APPLIED: get-policy → ResourceNotFoundException (nothing may invoke it); `events list-rule-names-by-target` → `[]`; event-source mappings → `[]`. EXERCISED: **1 invocation in its entire life** — log streams total = 1 (2026/07/17); CloudWatch daily Invocations 2026-07-01→08-19 (50-day window) = one datapoint, Sum 1.0. See Trigger Census below. |
| WS-2/WS-3 silver+gold built, one-account proven | EXERCISED | TRUE, BUILD-DAY ONLY | bronze `reporting_{performance,costbasis,allocation}` each hold exactly 1 partition `2026-07-17/`; silver `fact_taxsma_report` = `date=2026-07-17/` only; gold `dim_taxsma_report` = `account=0027265115/` (Chiles) only. Nothing has run since. |
| Chain scripts deployed | DESIRED-only | **REPO-ONLY, NO S3 CODE HOME** | `comp-pipescript deployed` cannot place them: `not-in-tree` in every tree of its universe (its `--pipeline` enum = {bd,inf,cot,mdpf}\*; **no `assets` tree**). mdpf-scoped run: "NOTHING VERIFIED … resolved to a SHARED repo home as non-members, 0 scripts checked against S3" (denominators: matched 0 of 3 assets_gold, 0 of 1 silver, 0 of 20 gold, …). Scripts run as ad-hoc agent sessions today. Comp-tool coverage gap = defect per Rule 22. |
| WS-4 gateway scoped-IAM "REMAINING (Andrew+CTO gate)" | APPLIED | **FALSE — ROLES ARE LIVE (map-vs-territory)** | `opal-mcp-emp-alyssa-read` + `opal-mcp-emp-alyssa-onboard` EXIST, both Created **2026-08-15T02:32Z** — inside the OPAL_GWRENAME S3 apply window (08-14 22:28–23:34 EDT; the WS-4 TF rode in the renamed opal-gateway stack). Positive control: known-live producer role returned identically. Live read-role policy == DESIRED lean-SPLIT exactly (GetObject on `blackdiamond/49f/gold/dim_taxsma_report/*` + prefix-scoped ListBucket, nothing else). **No WS-4 go-live sequence record found** (COND-2/COND-3, `taxsma_rule22a_verify.sh` run, CTO go-live confirm — no record located this pass). Least-privilege holds; the finding is GATE-SEQUENCING, not over-grant. |
| WS-5 daily trigger / WS-6 productionized path | DESIRED | NOT BUILT | Consistent with record; WS-6 not probed beyond record (declared exclusion). |

### B3 — OPAL_TAXSMA_REGISTRY
| Layer | Verdict | Evidence |
|---|---|---|
| APPLIED | TRUE | `s3://opal-data-assets/blackdiamond/49f/_ops/taxsma_roster.json` exists — 1,645 B, LastModified **2026-07-21T19:56:37Z**, schema_version present |
| EXERCISED / currency | **23 DAYS BEHIND THE BUSINESS** | Roster: **3 accounts** (1 `active` Chiles/xref-resolved; 2 `pending_resolution` — Bump, Macy — blocked on the D2/D3 resolver-tier **sovereign egress word**). SharePoint master `Tax SMA Accounts.xlsx` (modified **08-13**): **11 accounts** — 5 TRADED 08-05 (Chiles, Nixon, Bump, Tracey, Macy), 2 opened-not-traded (Graff: margin-rate hold; Draine), 4 awaiting account opening (Lindsey, Ashok, Griffin, Genender). Nixon + Tracey are TRADED and unenrolled. |

### B4 — Serve-layer ruling (gold-only, PII-free)
CONSISTENT: recorded CTO ruling 07-17; live gold prefix exists; the live Alyssa read-role grants
exactly that one prefix (measured this session). Anonymization-holds (COND-3) not re-verified —
declared exclusion, WS-3-layout gate owned by the (c)-sequence.

### TRIGGER CENSUS (the TO's named discriminator)
The producer is **neither NEVER-LAUNCHED nor STOPPED** — the false fork the TO warned about
resolves to a third state: **NEVER-SCHEDULED**. It launched exactly once, manually, at build-day
verification (07-17, the recorded Chiles proof), and was never a production feed that could
"stop". Build-day artifacts mimic a dead feed exactly as predicted; the three-plane read
(TF-no-schedule == live-no-trigger == one-invocation-ever) is what tells them apart. Per
CLAUDE.md's ad-hoc-runs rule, a production pipeline must have a schedule — WS-5 is that schedule
and is unbuilt (deliberately: WS-5 "owns the trigger" per the TF's own comments).

---

## Part 2 — WORKFLOW-AS-DESIGNED MAP (intake → generate → human execute)

Yang's 5-step spec (`tools/tax_sma/YANG_TAXSMA_AUTOMATION_SPEC.md`, verbatim source) vs built:

```
ONBOARDING (per account):
  SOP (SharePoint: "Tax Aware Capital Gains - SOP.docx", 07-27; Schwab acct opening,
      BT Master 0804-4932, SMA 145<->45% / SMA 200<->100% leverage, portfolio margin)
   -> [HUMAN: advisor + Schwab PM team]
   -> /tax-newacc {schwab#}  -> roster enroll + immediate pull        [BUILT, agent-run]
      DRIFT: the SOP contains NO enrollment-handoff step; it ends at "trading readiness"

DAILY CHAIN (per Yang's steps):
  1. SSAVAIL intake      /tax-pt1      AUTOMATED  BUILT, IDLE since 07-15
     (legacy twin /taxsma-step1 still present — consolidation debt)
  2. Cost basis          /tax-pt2      AUTOMATED  BUILT (derives from 0833 S3 master,
                                                  NO Schwab login) -> TAX/Tax Lot/{date}/
  3. FactSet conversion  /tax-pt3      AUTOMATED  BUILT (runs Yang's convert_cost_basis.py
                                                  VERBATIM) -> TAX/Initial Holding/{date}/
     ============ LAST AUTOMATED STEP (today) — the handoff artifact is the ============
     ============ Initial-Holding file set handed to Yang                   ============
  4. Optimization        MANUAL (Yang, FactSet/Axioma)          <- FIRST HUMAN STEP
  5. Trade-file convert  convert_optimization.py  DESCOPED (Andrew 07-14: "We don't need
     to focus on step 5 at this point") — canonical script exists in repo
     ==================== ⛔ THE GUARDRAIL (standing law, run A3) ====================
     THE SYSTEM GENERATES THE TRADE FILE; A HUMAN REVIEWS AND EXECUTES AT SCHWAB.
     NEVER auto-execute / auto-upload; NO Schwab/FactSet creds in code. When step 5
     builds, the trade file (Trade/{date}/schwab_upload_{date}.csv) is the handoff
     artifact and execution stays human. The (c1) guardrail TEST SET (deployed-bytes
     credential-absence, non-reachability of any upload call site, named handoff)
     gates the daily-unattended leg — priced at (c1), not here.
     ===============================================================================

PARALLEL REPORTING SPINE (analytics, not trade ops):
  producer lambda -> bronze reporting_{performance,costbasis,allocation}
                 -> silver fact_taxsma_report -> gold dim_taxsma_report (PII-free serve;
                    Alyssa read-role scoped to exactly this prefix)   [BUILT, build-day-only]
```

---

## Part 3 — BUCKET/PREFIX CONFORMANCE MAP vs 17b (FINDINGS ONLY, NO MOVES)

| Surface | State | Finding |
|---|---|---|
| `opal-data-assets/blackdiamond/49f/{bronze,silver,gold}` | **CONFORMING** | Matches 17b `{vendor}/{firm}/{medallion}` and monolith.tf's own declared `{source}/{scope}/{layer}` grammar (`monolith.tf:226`). Denominators: bronze = 6 prefixes (3 producer-owned `reporting_*` + `template_roster` + `allocation_390224` + `fees_435407`), silver = 3, gold = 1. |
| `blackdiamond/49f/_ops/` (roster, pull_state, probe) | CONFORMING-BY-RULING | Control-prefix outside layer grammar — explicitly ruled at registration (REGISTRY D1 ruling @`6fedafcd1b`). Declared exception, not drift. |
| Gold home vs the 17b 08-11 amendment | RULING-GATED, NOT A VIOLATION | The amendment puts product-gold at `opal-data-assets/portal/gold/{product}/{scope}/` with gold-as-parquet; taxsma gold sits in the vendor tree at `blackdiamond/49f/gold/` (partitioned by `account=`). Predates the amendment; 17b's own caution applies — a (c2) ruling input, never a move warrant. File-format inside partitions not inspected (declared exclusion). |
| Chain-script repo home `data/assets/scripts/{silver,gold}` | **GRAMMAR HOLE** | A shared repo home outside `comp-pipescript`'s pipeline universe, with NO S3 code home (`not-in-tree`; the Rule-13 S3-membership guard 404s). When (c1) productionizes the chain it must mint a code home + runner; today the scripts exist only in-repo and run as agent sessions. |
| SharePoint `TAX/` tree (Short Sale, Tax Lot, Initial Holding, Reporting, Billing/Tax SMA) | BY-DESIGN | The operator/business surface — deliberately outside the S3 grammar. |

---

## Part 4 — SHAREPOINT SYNC REVIEW (leg DELIVERED — envelope held)

Probes (my session, inheriting MSTR~Z's 20:0xZ envelope): `whoami` = Andrew Berman proxy ✓;
`find_sharepoint_site("Shared")` resolved the pinned site id ✓; `search_site_files` "Tax SMA":
Shared site = **200 rows** returned; Opal Capital site = **8 rows** (incl.
`Tax_Aware_Solutions_Cottonwood_template.pptx`, 07-21) — matching the inherited baseline. No
delta from MSTR's envelope; the leg never broke.

**The Yang/Alyssa doc set, located:**
- `Tax SMA Accounts.xlsx` — Shared/TAX area, modified **2026-08-13**. THE living master (Yang's
  spec names it as the master file). 11 accounts, read in full this session.
- `Tax SMA Accounts 20260805.xlsx` — a frozen 08-05 copy (rebalance-dated snapshot pattern).
- `Tax Aware Capital Gains - SOP.docx` — 07-27, the account-opening/onboarding SOP (read in
  full, 3 pp).
- `6.30 opal holdings tax sma template.xlsx/.csv` — 07-30 holdings template.
- `TAX/Reporting/2026Q2/Client Accounts 2Q26/` — per-client Q2 tax updates (Chiles, Macy pdfs).
- Operational folders: `TAX/Short Sale` (+ Intake Logs, Flagged Files), `TAX/Tax Lot`,
  `TAX/Initial Holding`.
- Repo-side canonical spec: `tools/tax_sma/YANG_TAXSMA_AUTOMATION_SPEC.md` (Yang's 5 steps
  verbatim + canonical converters).

**Doc-vs-built DRIFT LIST:**
1. **Scale drift (the headline):** master file 11 accounts / $27.71M / 5 traded-as-of-08-05 vs
   roster 3 accounts (07-21) vs gold serve 1 account (07-17). Nixon (inception 08-05) and
   Tracey (08-05) are TRADED and appear nowhere in the built system.
2. **SOP handoff gap:** the onboarding SOP ends at "trading readiness established" — no
   registry-enrollment step; `/tax-newacc` (the built entry point) is absent from the doc.
3. **Cadence drift:** the doc-side process assumes daily intake (Yang step 1 "every morning");
   built intake idle since 07-15 while the feed arrives daily (measured to 08-19).
4. **Strategy vocabulary:** NO drift — SMA 145/45% and SMA 200/100% consistent across SOP,
   master file, roster, and Schwab marketplace naming.
5. **Minor naming drift:** backfill filed stub files as `SSAVAIL* {date} STUB.ASC` in the main
   folder; the skill's rule is `Flagged Files/{base} {DATE} FLAGGED-{class}{ext}` (Flagged
   Files childCount=1). Cosmetic; note for the next intake pass.
6. **Observation for the meeting:** Last-Trade-Date 08-05 across all traded accounts + the
   08-05 frozen master copy suggest a ~monthly rebalance batch cadence; the built chain has
   never run against a rebalance date.

---

## Part 5 — HOLE LIST + REMAINING-WORK REGISTER

| # | Hole | Class | Feeds |
|---|---|---|---|
| H1 | WS-5 daily trigger unbuilt; producer NEVER-SCHEDULED (1 lifetime invocation) | build | (c1) — **WAIVED-BY-RULING @`1e0ec3b079`, cuttable now** |
| H2 | Multi-account unbuilt AND double-gated: silver/gold one-account; 2 of 3 roster accounts `pending_resolution` on the D2/D3 **sovereign egress word** (tier-2/3 resolver) | build + sovereign | (c1) (waived @`1e0ec3b079`) + Andrew's egress word (still open) |
| H3 | pt1 operator cadence not running since 07-15; feed alive; ~24 trading days unfiled (07-16→08-19 minus 2 manual dates) | ops/cadence | meeting item 2; (c1) option-A now cuttable per the waiver |
| H4 | WS-6 gateway wiring (Alyssa's Phase-B path) unbuilt while its WS-4 roles are now live | build | (c5) |
| H5 | **WS-4 gate-sequencing finding:** Andrew+CTO-gated security surface landed live 08-15 via the OPAL_GWRENAME stack apply, without its own go-live sequence record (COND-2/COND-3/`taxsma_rule22a_verify.sh`/CTO confirm — none located). Grants verified least-privilege. Needs explicit ratification or a retroactive run of the WS-4 sequence — CTO/Andrew call, FINDING ONLY | governance | routed via MSTR |
| H6 | Roster 23d behind master file; Nixon + Tracey traded-unenrolled | data currency | meeting item 3 |
| H7 | 4 open closeout-drift advisories on the TAXSMA record set (08-06, owner 2.0.0_SA_COO~Z, review_by 08-08 — 11d overdue; `closing_commit` field actually cites the MDPF_CANPLAT Wave-1 commit `f123fbf6e`, a comp-state-BEHIND trigger, not a TAXSMA closeout) | records | COO~Z |
| H8 | `comp-pipescript` universe lacks the `data/assets` tree — the chain scripts are unverdictable by the estate's own deploy instrument | comp-tool coverage gap (= defect, Rule 22) | CTO routing |
| H9 | Legacy skill twin `/taxsma-step1` beside `/tax-pt1` — consolidation debt (retire consumers first) | debt | (c)-time |
| H10 | Step-5 trade-file converter descoped-by-Andrew 07-14; canonical script exists; re-scope decision open | scope | meeting item 7 |
| H11 | Dead owner seat: 3 projects + TO #48 at `0.5.0_AE_OpalETL~A` (#42 disposed mid-pass: SUPERSEDED by D7+D9 @`3c8c3f1035`) | seat | Part 6 |
| H12 | Yang parked words: 07-01 swap-file adjudication; backfill ack (from #8, parked non-blocking) | vendor-intent | meeting item 8 |

WS-remainders per record, confirmed still open: PT2 {multi-account, WS-5, WS-6}; REGISTRY
{WS-R2 resolver ladder tiers 2/3 (sovereign-gated), WS-R3 ETL-reads-registry exercise at scale,
WS-R4 Phase-B}. WS-4/WS-R5 flipped from "remaining" to "landed-unratified" (H5).

---

## Part 6 — SEAT-OR-SUPERSEDE RECOMMENDATION (TOs #42, #48)

**I recommend; I do not dispose.** Disposition = Andrew (via MSTR ferry); flip mechanics = COO
per the banked inherit protocol (COO~Z 195042Z ack of MSTR~Z 194942Z).

**TO #42** (`ANDREW_DIRECT_20260714_taxsma_ticket_system_scoping.md`, was pending 36d at the
dead ~A lane) — **DISPOSED MID-PASS, NO RECOMMENDATION AUTHORED**: Andrew ruled it
**SUPERSEDED by the D7+D9 PRDs** (CTO card 10, record @`3c8c3f1035`, register flipped at the TO
file, swept to the sitez trunk @`e8b2c300b3`; MSTR~Z relay 202732Z). The 36-day taxsma-scoping
row therefore classifies per COO~Z's 201546Z note with the disposition now RESOLVED:
inherit = superseded-with-pointer, flip mechanics COO~Z's. For the record, both halves' living
work was already seated when the ruling landed: ticketing at the fresh `0.5.0_AE_OpalETL~Z`
seat (D7_TICKETING.TO-AC-SITEZ, activated 2026-08-19T19:2xZ), TAXSMA close-out under D9 (its
07-14 scoping deliverable @`293c062fb` had already been executed into the three OPAL_TAXSMA*
projects). Nothing on #42 rides to Andrew from this assessment.

**TO #48** (`ANDREW_DIRECT_20260715_uiux_design_centralization.md`, "executing" at the dead ~A
lane) — two unrelated halves:
- *#8 TAXSMA half:* build arc CLOSED by Andrew's own schedule ruling ("Yes B now"); its standing
  direction — *"We do need a daily schedule here"* — is exactly D9 (c1). **RECOMMENDATION:
  SUPERSEDE-INTO-D9(c1) with pointer**; the parked Yang words (H12) ride the meeting agenda.
- *#7 UIUX half:* not TAXSMA at all; the registered UIUX_DESIGN project carries its remainder
  (recorded in its project JSON as "the next TO"). **RECOMMENDATION: SUPERSEDE-WITH-POINTER to
  UIUX_DESIGN** (or re-seat under a UIUX wave — COO's mechanics either way).

**The three OPAL_TAXSMA\* projects' owner seat** (all at dead `0.5.0_AE_OpalETL~A`):
**RECOMMENDATION: re-seat at the (c) wave cut** — natural inheritor is the live
`0.5.0_AE_OpalETL~Z` seat (same 0.5.0 class, spawned today, already carrying D7 intake duty),
with Rule-13 lane split at TO level when (c) cuts (DS: silver/gold scripts; AE: producer,
trigger, IAM/TF). Matches §7-Q3's expected shape ("fresh 0.5.0-class respawn"). COO executes.

---

## Part 7 — YANG/ALYSSA MEETING AGENDA (one page)

**Premise (60 seconds):** every chain leg exists and was proven once (Chiles, mid-July); nothing
runs on its own; the book has grown 3→11 accounts and 5 are trading. The asks below close the
gap between "built once" and "runs daily at book scale."

1. **State of the world** — the live-truth table (Part 1) in one slide: built ✓, scheduled ✗,
   scaled ✗.
2. **Who runs the daily intake?** /tax-pt1 idle since 07-15; FIS feed alive daily. Options:
   (a) Alyssa takes the operator cadence per the standing "B now" ruling (skills are
   Alyssa-operable by design); (b) option A (scheduled-autonomous) = D9 (c1) — **now WAIVED
   ahead of this meeting (@`1e0ec3b079`) and cuttable**, still gated on the guardrail test set
   before the unattended leg ships. Decide the interim (a) regardless.
3. **Account catch-up:** enroll Nixon + Tracey now (traded 08-05, invisible to the pipeline);
   Bump + Macy need **Andrew's D2/D3 egress word** (tier-2 sanctioned exact-number query vs
   tier-3 account-api) to resolve; 6 more accounts are in the opening pipeline.
4. **Daily tracking at scale (S8c):** (c1) is WAIVED ahead of this meeting (@`1e0ec3b079`) —
   the cut needs no further permission; this item is now about SCOPE (WS-5 schedule +
   multi-account ETL reading the roster) and the guardrail-test gate, not about whether.
5. **Master-file custody:** `Tax SMA Accounts.xlsx` is the living source (Yang, 08-13). Agree
   the sync direction: does the S3 roster FOLLOW the xlsx (and who/what syncs it), or does
   enrollment move to /tax-newacc-first with the xlsx as view? (One-writer question.)
6. **Onboarding SOP handoff:** add the enrollment step to the SOP; confirm Alyssa's Phase-B
   read path (roles live 08-15; gateway wiring = WS-6, unbuilt).
7. **Step-5 re-scope:** trade-file conversion stays descoped or cuts with (c1)? Guardrail
   restated either way: the system GENERATES, a human EXECUTES — no auto-upload, ever.
8. **Yang's parked words:** the 07-01 swap-file adjudication (canonical 2.8MB vs EXTRA 13.5MB);
   backfill acknowledgment; role of `template_roster/` + the 6.30 holdings template.
9. **Reporting:** Q2 client updates exist manual in TAX/Reporting — fold into the gold serve
   layer later, or keep manual? (Feeds (c4) MDPF roll-in sequencing.)

---

## ADDENDUM (post-delivery, same session) — the 07-16 partner-call ingest folded in

Ingest ferried @`ad01cca427` (on-trunk @`4bf2f8f6a3`):
`org/tier1_exec/1.0.0_SA_CTO/deliverables/partner_calls/20260716_DASHBOARD_TAXSMA_REPORTING_INGEST_20260819.md`
(+ byte-faithful docx/vtt + 4 SMARTX Chan-account ledgers beside it). What it adds, by part:

- **Part 2 (workflow-as-designed) — the QUARTERLY REPORTING flow, previously invisible to this
  assessment:** per-client Excel off Yang's 2-page template (p1 identity/BMV/flows/EMV +
  QTD/YTD/1Y/3Y/SI returns; p2 period tax detail + positioning/sectors), quarterly cadence,
  Q2 ran 3-of-5 then-live accounts, ENTIRE-ACCOUNT no-sleeves ruling, BMV backed into from
  performance+EMV. Owners: Alyssa fills, Manav grants BD access, Andrew automates. This is a
  SECOND human-operated chain beside the daily one — quarterly, template-driven — and it is
  entirely manual today.
- **Part 1/5 (SOURCE MAP with rationale):** returns-net-of-fees ← Black Diamond (because 49F
  turned OFF Schwab's client performance); cost basis + realized/unrealized ← Schwab; sectors +
  holdings ← FactSet pre-pulls; benchmarks ← Bloomberg (49F custom benchmarks, S&P/AGG
  declined).
- **THE FLAG, TESTED (not adopted):** *"returns ← BD"* vs the estate's own 49F TWR chain.
  Live/deployed read this session: `data/assets/scripts/gold/runners_49f/c02_twr_engine.py`
  (+ lineage + tests; CVO spec 08-11 — post-dates the call) writes
  `s3://opal-data-49financial/gold/advi/canonical/twr_daily/` — **LIVE, partitions through
  `date=2026-08-18` (T-1 current)**, GROSS/NET pair with the fee-management lever (so the
  net-of-fees semantics BD supplied is covered in-form). **VERDICT: the daily-returns leg of
  that cell is SUPERSEDED-BY-ESTATE (evidence above); the PERIOD-form leg is NOT YET** —
  `canonical/twr_periods/` listed EMPTY this session (0 rows; tree searched:
  opal-data-49financial), and the Q2 template consumes period returns (QTD/YTD/1Y/3Y/SI).
  The template's other source cells (Schwab cost basis: /tax-pt2 covers; FactSet
  sectors/holdings: manual pre-pulls; Bloomberg benchmarks: manual) are unchanged by the
  estate today.
- **Meeting agenda addition (item 10):** quarterly reporting automation — whether Q3 reports
  draw returns from the estate TWR chain (period forms pending) instead of BD, and whether the
  template fill becomes a generated artifact. Population facts from the call (3-of-5 live then;
  5 traded now per the 08-13 master) size it.
- **Part 4 addition:** the call names further doc-sync targets located in the OCIO-models
  Dashboard tree (`.../2026 Q2/` per-client files, FactSet pull files) — enumerated for the
  meeting, not drift-listed this pass (declared exclusion: OneDrive/OCIO tree not walked).

## Denominator register (D9A-3)

Every count above carries its frame; the load-bearing ones: comp-find taxsma filename census
**49/49 hits enumerated, 26,352–26,357 files scanned** (live-tree churn of ~5 files between
calls, noted); comp-estate **29 verticals / 138 chains listed, 0 taxsma** (absence verdict names
the instrument's own registry, not a bucket); trigger census **50-day metric window, 1
datapoint; 1 log stream total**; Short Sale folder **39 items**; Intake Logs **1 file**; mailbox
probe **15 rows page 1 (14 SSAVAIL), pagination live (nextLink present)**; roster **3 accounts**;
master xlsx **11 account rows + total row, sheet 22×13 used range**; Shared-site search **200
rows**; Opal-Capital-site search **8 rows**; bronze/silver/gold prefix counts **6/3/1**; WS-4
role probes **2 targets + 1 positive control**. S3 absence verdicts in this doc all name
`opal-data-assets` (the one tree searched); no cross-tree absence is claimed anywhere.
