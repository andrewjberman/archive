# TO ADVI_49F.c00-FIX — the c00 in-kind (IC) flow-leg defect (LAPTOP, DS~A runner-chain lane) — PRIORITY

<task_order id="ADVI_49F.c00-FIX" project="ADVI_49F">
<issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-19T19:55Z</issued>
<dated>FIRST substantive row at your THU respawn -- staged tonight so the seat finds it, not so it waits</dated>
<status>staged -- GO paired; NEEDED UNDER EITHER FLIP TIMING (see the fork below -- do not wait on it)</status>
<priority>P1-PRIORITY. Routed by CTO 194648Z off CRO~A's 194539Z finding; scope amended 194759Z.</priority>
<authority>CRO~A's BD_PERFORMANCE_ENDPOINT_VS_GIPS_ENGINE_COMPARISON_20260819.md (every link read). CTO routing 194648Z + scope amendment 194759Z. Placement: LAPTOP (runner chain + deploy leg).</authority>
</task_order>

## The defect (INPUT-class, precisely bounded)
`c00` emits IC (in-kind) flow legs with **`in_kind_value=0.0` AND `in_kind_unvalued=False`** — its
own docstring's never-zero-buried promise **violated by its own output** — and **no quantity column
survives into the emitted rows.**

**Measured:** 202/202 IC legs across 03-24..03-27, 42 accounts.
**Consequence:** per-account TWR is unreliable on in-kind-funded accounts — **+341%** on a $3.70
`cf_net` day; **+627% SI vs BD's -8.13%** on the specimen.

**EXPLICITLY NOT IMPEACHED — do not widen the blast radius:** the valuations (the 309/312 tie
STANDS), non-IC accounts, and the engine's daily-linking method. **This is an INPUT defect, not an
engine defect.** Fix the input.

## Scope
1. **Carry `in_kind_value`** through to the emitted rows.
2. **Set `in_kind_unvalued=True` where genuinely unvalued** — honor the docstring rather than
   emitting a value that asserts "valued at zero."
3. **Preserve `quantity` into emitted rows.**

## FIRST ACT — A FEASIBILITY READ, BEFORE ANY CODE
Can fix + redeploy + floor re-pin complete **comfortably inside Thursday WITHOUT compressing the
pin/twin gates?** Report that read to COO before you build. It is the input to a sovereign timing
decision (below) and it is worth more early and rough than late and precise.

## SECOND ACT — THE FULL-HISTORY IC CENSUS (scope amendment, CTO 194759Z)
**THE 42-ACCOUNT FIGURE IS A 4-DAY FLOOR, NOT THE AFFECTED UNIVERSE.** One pass across **ALL**
`flow_ledger` partitions (~526): distinct accounts with >=1 IC leg + the dates, **plus the
materiality read** — does any serve-scope TWR window span such a day? **Print the denominator.**

⚠ **A COUNT YOU DID NOT PAGINATE IS A PAGE SIZE WEARING A TOTAL'S CLOTHING.** Materialise the
partition set and count client-side; never a `--query 'length(...)'` over a paginated `list-*`, and
never `--no-paginate` (it returns page 1 as a clean, complete-looking result). An ABSENCE verdict
carries its denominator printed beside it.

**If a pre-fix declaration ships before this census lands, its wording is EXACTLY: "42 accounts
across 4 SAMPLED days; full census pending at the fix TO."** Never the 4-day count wearing the
universe's clothing.

## Acceptance criteria
- **C00-1 FEASIBILITY READ REPORTED** (Thursday-comfortable: yes/no, with what it would compress).
- **C00-2 FULL-HISTORY IC CENSUS** across all ~526 partitions: distinct affected accounts + dates +
  materiality read, **denominator printed**.
- **C00-3 THE FIX LANDS:** `in_kind_value` carried, `in_kind_unvalued=True` where unvalued,
  `quantity` preserved into emitted rows.
- **C00-4 HARNESS RE-RUN IS THE ACCEPTANCE ORACLE** — CRO~A's matched-window harness, already built,
  minutes per account. **Post-fix the +341% day re-reads ~0% and SI ties BD in-band.** This TO is
  not accepted on a code review or a green deploy; it is accepted on that re-read.
- **C00-5 DEPLOY VERIFIED** on the deployed artifact (Rule 22a CODE layer — the deployed bytes,
  resolved through the build input, never by filename), not rc=0.
- **C00-6 proof instance VALID rc=0 positional: ids C00-1..C00-6.** MEASURED/RULED rows only.

<proof_of_spec>
  <expected_criteria>C00-1,C00-2,C00-3,C00-4,C00-5,C00-6</expected_criteria>
  <instance_path>org/tier2_senior/0.4.0_DS_ClientPlatform~A/deliverables/ADVI_49F.c00-FIX_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## THE TIMING FORK IS NOT YOURS — AND IT DOES NOT HOLD YOU
Andrew decides: **(a)** fix-before-flip (re-pin Thursday, some Friday compression risk) vs
**(b)** flip Friday as planned with the defect DECLARED (42 accounts annotated in the flip
acceptance + the known-defect register), fix = the drive-to-EXACT loop's first act, MON at latest.
**CTO's REC is (b) UNLESS your feasibility read says (a) is comfortably free.** CTO is putting the
fork to Andrew. **This TO is needed under EITHER answer — build it; the fork changes WHEN it lands,
never WHETHER.**

## Do not
- ⛔ **DO NOT LET THIS TOUCH THURSDAY'S 12:45Z FIRST GREEN.** That run proves the floor and its
  artifacts serve nothing until flip. Leave it alone.
- Do not widen into the valuation chain or the linking method — both explicitly not impeached.
- Do not annotate accounts as affected off the 4-day sample; that is what C00-2 is for.

## Reporting
COO at the feasibility read (fast, same session), at census-complete, and at harness-re-run.
cc CTO (gate) and CRO~A (harness owner + the finder). CRO~A's wider stratified comparison
deliberately waits until post-fix so it measures parity rather than the known break — endorsed;
do not ask them to run it early.
