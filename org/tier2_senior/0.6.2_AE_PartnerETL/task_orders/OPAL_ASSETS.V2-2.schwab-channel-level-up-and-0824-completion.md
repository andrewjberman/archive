# OPAL_ASSETS.V2-2 — Schwab channel level-up + 0824 completion

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>2.0.0_SA_COO (V2 decomposition; PRD author 1.0.0_SA_CTO)</issued_by>
<date>2026-07-14</date>
<status>complete</status>
<completed>2026-07-16 (self-mark; COO ruling 20260716T135723Z + CTO concurrence 135807Z; evidence body below)</completed>
<go>Half (a) is ALREADY ARMED (your existing remap-on-pull-terminal plan, unchanged — this TO does not re-order it). Half (b) is new material: begin when (a) is landed or during armed-wait idle hours.</go>
<project>OPAL_ASSETS — V2 Phase I bronze close-out</project>
<prd>docs/architecture/OPAL_ASSETS_V2_PRD.md §2 bar + V2-2 (@ 53ba45c5f); inherits CONSOLIDATION_PRD v1.6.0 whole</prd>

## THE GOAL — both master folders wrap per the §2 four-column bar
**(a) 0824 completion (armed, unchanged):** 0824 remap on pull-terminal (now ~5,928/5,966) + 13c 3-tier
verify + per-master live exercise. Your existing sequence stands verbatim.
**(b) si2 puller level-up (new):** the 0833/0824 puller is MID vs the C5 standard (PRD §1: 13c +
session-lock + T1-ruled, but NO set-identity landing guard, NO persisted manifest). Add:
- set-identity landing guard — shortfall AND surplus, verdict on ListObjectsV2 landed bytes, mutant
  transcript committed (the C2 lesson: assert DISTINCT LANDED KEYS / set-identity, never a write tally).
- persisted per-pull meta manifest under `{source}/{scope}/meta/pulls/` (ruling 21 home).
KEEP: 13c 3-tier copy verify, session-lock, T1 recon stays a SILVER-parser control (not bronze's job).

## SEQUENCING (unchanged, explicit)
0824-terminal -> per-master exercise + 0824 remap -> V2-3 deletion chain (Andrew GO -> your temp grant
[at CTO's gate now, routed 05:58Z] -> delete off EXACT key list @ 2cc0f8fee -> guard re-run, baseline
2,269 -> 0) -> (b) level-up whenever it fits without delaying the above.

## <compiler_tools_mandate>
PRD §2 bar col 3, verbatim: "IAM CLEAN (22a, 'no fucked up iams') — per producer role: live
`simulate-principal-policy` on the EXACT ARNs it writes/reads, ONE `--resource-arns` per call, positive
controls as SEPARATE invocations, negative controls = a firm bucket + the Door-6 sentinel key + an
out-of-scope monolith prefix. Recorded simulate outputs are the evidence; a comp-iam GREEN is not."
Every .py `from __future__ import annotations` (Rule 15). `.tools/commit-gate.sh` pre-commit.
Denominators enumerated AT RUN TIME (13b), never quoted from a doc.
</compiler_tools_mandate>

## <cross_domain_coordination>
New-territory: additive only. The reap role is SEPARATE (opal-c2-orphan-reap-role); the remap role stays
delete-incapable — that property is preserved, never amended. Nothing touches INF/bd/cot planes. Nothing
writes the Door-6 key. Glacier 257 stays background fill (Andrew: holds up nothing).
</cross_domain_coordination>

## <acceptance_criteria>
1. Both master folders (schwab/08335338, schwab/08242234) wrap per the §2 bar — all four columns green,
   each cell cited to a live primitive (listing/simulate/schedule+landed-bytes).
2. Guard mutant transcripts committed for the puller (shortfall + surplus + collision).
3. Manifest lands per pull; listing-cited.
4. RAVC evidence to COO at each gate (as you already do).
</acceptance_criteria>

## <completion_evidence> (self-mark 2026-07-16 ~14:0xZ, 0.6.2_AE_PartnerETL)

**Closed on COO's (ii)-then-(i) ruling 20260716T135723Z + CTO's in-window concurrence 20260716T135807Z.**
The TO's SCOPE (ADD = 2 items) and its ACCEPTANCE BAR (all four §2 columns green) contradicted each other:
the premise "MID vs C5 ... but NO guard, NO manifest" assumed retry/backoff was already present. COO ruled
the drafting error does not manufacture build scope (option (iii) rejected); the retry cell was DETERMINED
by a bounded artifact read, then carried at its true state.

### The §2 four-column bar -- every cell on a live primitive (full table: RAVC 20260716T135555Z)

| col | 08335338 | 08242234 | verdict |
|---|---|---|---|
| 1 BACKFILL COMPLETE | sweep `20260716T121550Z-f0c6ab35`: bronze_keys=6972 types=18, shortfall_pre/post=0, surplus=0, collisions=0, holes_named=[tcf,tcfx,tnn] | same run: bronze_keys=6257 types=17, all zeros | **GREEN** |
| 2 DAILY INTERVAL SOLID | rule `canonical-schwab-si2-08335338-daily-pull` ENABLED `cron(45 9,21 * * ? *)`; FIRE 09:45:52Z -> downloaded=13 -> LAND exactly 13 keys w/ bytes 09:46:02-09:46:41Z -> converter 09:46:33Z T1 101144==101144 | rule `...-08242234-daily-pull` ENABLED `cron(15 10,22 * * ? *)`; FIRE 10:15:19Z -> downloaded=11 -> LAND exactly 11 keys w/ bytes 10:15:28-10:16:02Z | **GREEN** |
| 3 IAM CLEAN (22a) | 11 SEPARATE simulate invocations, ONE `--resource-arns` each, on `quartz-si2-spike-role` | (same role serves both masters) | **GREEN** |
| 4 ROBUSTNESS AT C5 | 5 of 6 (guard / manifest / denominators / ASCII / parse-boundary) | same | **5/6 -- retry ABSENT, carried** |

- **Denominators run-time enumerated (13b), never quoted.** Independent `aws s3 ls --recursive` taken BEFORE
  reading the manifests ties their denominators EXACTLY on both masters (0833 6972/8468; 0824 6257/7633).
- **The col-1 field discriminates** -- the same field read `shortfall_pre=344` on the completing sweep
  `20260715T181504Z-64a7e1f5`. Scan denominator: 37 most-recent 0833 manifest keys, exactly 2 were sweeps.
- **Col-1 scope, stated:** the box guard proves set-identity vs source-of-record for the ROLLING WINDOW only
  (it says so: "run-window scope"). Full-history backfill cites CTO's `PARITY_CERTIFICATION_20260715.md`
  @ `6bfd97204`, independently confirmed by my leg-4 parity RAVC (CTO ACCEPTED 20260716T133027Z).
- **Col-2 is trading-calendar-resolved BY CONSTRUCTION:** the puller resolves the frontier itself
  (`while (-not (Is-TradingDay $d))`, :206); both records carry `trading_frontier=2026-07-15` on a 07-16 fire.
- **Col-3 ran the 22a trap BOTH WAYS** rather than asserting it: `MonolithSchwabList` is Condition-bearing,
  so (a) no `--context-entries` -> `implicitDeny` (a FALSE deny on a grant used every 12h in production);
  (b) with `s3:prefix=schwab/08335338/bronze/` -> `allowed`; (c) control `s3:prefix=inf/gold/` ->
  `implicitDeny`, so (b) is not vacuous. Negatives = the column's prescribed set: bd + cot `explicitDeny`,
  Door-6 sentinel `explicitDeny` (SIMULATION ONLY -- key never written), meta/conversions + silver
  `implicitDeny`. Recorded simulate outputs are the evidence; no comp-iam GREEN is cited.

### Criteria
1. **SATISFIED with one carried cell** (col 4 = 5/6; see residual). 2. **SATISFIED** -- guard mutant
transcripts @ `c03a8529c`. 3. **SATISFIED** -- manifest lands per pull under the ruling-21 home
`schwab/{m}/meta/pulls/`, listing-cited (4 records, 2 per master). 4. **SATISFIED** -- RAVC at each gate.

### Carried residual -> CTO's gate (routed 20260716T140427Z; V2-1 precedent pre-agreed)
**retry/backoff HTTP client: ABSENT -- DETERMINED, not assumed.** One client fn `Invoke-Sdd` (:296,
`System.Net.HttpWebRequest`), two unwrapped call sites (:324 search, :448 download); no loop/backoff/attempt
counter; `:303` catches `WebException` only to RETURN the error response. **Severity is resilience, NOT
correctness:** every failure path is loud (search non-200 -> `Die 2` + SNS page; download failures -> per-file
catch -> `failed`/`failures` in the manifest; `accounted = dl+skip+fail` must equal `ENUMERATED`) and the
12h cadence + skip-if-landed idempotency re-attempts a missed file -- the retry exists at the SCHEDULE
level, not the request level. True cost = <=12h latency on one file from a transient hiccup. Fix shape:
bounded attempt loop + backoff around Invoke-Sdd's two call sites (PS1 analogue of V2-1's
urllib->requests+Retry). P2/P3; open question at CTO's gate is whether to build it into a vehicle WP7 may
re-home.

### Correction on the record
My RAVC-4 (20260716T133845Z/135555Z) claimed the puller had "zero HTTP call sites" and "delegates to a .NET
assembly". **FALSE** -- my grep pattern omitted `HttpWebRequest`, so a negative result from a pattern I
never wrote became a claim about the artifact, then a mechanism. Corrected to CTO + COO at 140335Z/140427Z
before anything acted on it. The vendor DLLs are loaded, but only for XML serialize/deserialize + request
types. **An UNDETERMINED I was comfortable with was concealing an ordinary mistake; only opening the file
caught it.**

### Incidental (feeds the (iii) P2 post-mortem)
The 07-07 silent-miss cell is **already structurally closed in this puller**: `# >>> ZERO ON A TRADING DAY
IS A FAILURE, NOT A SHRUG. This is the exact cell the GUI channel died in. <<<` -> `Die 2 "... This is a
DEAD CHANNEL, not a quiet one."`, plus `Die()`'s header "FAIL LOUD. The predecessor's fatal flaw was a
benign-sounding rc=0 on a dead channel." The 07-07 MECHANISM itself stays OPEN -- today's code being immune
says nothing about the old path's behaviour.
</completion_evidence>
