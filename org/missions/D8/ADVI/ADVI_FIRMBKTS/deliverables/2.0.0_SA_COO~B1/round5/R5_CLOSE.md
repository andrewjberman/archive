# ADVI_FIRMBKTS -- round 5 close: the cutover's open reads (2.0.0_SA_COO~B1, dell1, 2026-10-13 ~07:4xZ)

**Instrument:** the issuer's checks in `deliverables/2.0.0_SA_COO~B1/round5/checks/` (`r5_fwd1.py`, `r5_checks.py`) and
`round4/checks/r4_scope.py`; each instance validated with `proof-of-spec-check.py --governing-order`; each criterion re-run by the
issuer at the merged HEAD (not the worker's tree) after the drain. `round-close-check.py --project ADVI_FIRMBKTS --round 5`: 8 orders,
7 complete, 0 not complete outside the verdict (FB-h-5 is `parked`, see below), proofs 7 of 7, judgment 0, verdict **MAY-CLOSE**.
Class: LOCAL reads, records and test files; WORLD only by the path floor (FB-h-4, FB-h-8). Nothing served moved; no AWS write.

## The result

| order | cell | executor | result |
|---|---|---|---|
| `FB-h-1`, `FB-h-2` | FWD-1: 22 locations (the 11 that disagreed in round 4, 11 controls) read blind again | `~61`, `~62` (worker-light) | `r5_fwd1.py agree`: the 11 agree on all four fields and equal the key 11 of 11; the 11 controls 11 of 11. Each reader's worktree: `LOCATIONS.json` alone, one commit, `OPENED: none`. Ingested `5c6a05e689`. |
| `FB-h-3` | the validator's ownership decisions replayed offline on both maps | `~63` | merged `675154376d`: `REPLAY pairs=2127 mismatches=0 control_mismatches=1 accounts=1501 relationships=626`; the handler's own request was `opal-data-49financial` `advi/49financial/platinum/49financial/ownership_map.json`. The maps are NOT byte-equal (193 advisors, 24,161 accounts, 10,813 relationships each; only `generated_at` differs). |
| `FB-h-4` | the validator's ownership-key spec follows the flip (`D1-C-S33`) | `~64` | merged `a579ab8193`: 7 pass 0 fail (base 5/1); the mutant arm (list emptied in a copy) FAILS with 2 fail (base fail=0). |
| `FB-h-5` | the validator's canonical read exercised once by a non-admin request | `0.7.0_AE_CloudOps~FB1` | **PARKED**, owner `1.0.0_SA_CTO~DELL1`. Organic: 17 lines on the two paths since 15:15:10Z, all `tier=internal` (admin bypass), 0 non-admin; events fetch_failed, schema_mismatch, not_in_ownership_map, scoping_denied 0 each (7 regions, 9,136 lines, v23; rows `D1-S41`). Driven: the CTO's walker account (ADDENDUM 1) reads role=admin, userType=Dev (row `D1-S42`): the validator bypasses it before any ownership read, so it cannot be the non-admin read. |
| `FB-h-6` | the exec-summary put-events diagnosis (read-only) | `~65` | merged `1b7104b267`: INDETERMINATE (below). |
| `FB-h-7` | the BD pricing findings S32-S34 quantified (read-only) | `~66` | merged `47f7ddebcf`: S32 moves; recommendation BRIEF_TO_CRO (below). |
| `FB-h-8` | the fence instrument: explicit UTF-8 and the object-shape fixture (`D1-S28`) | `0.7.0_AE_CloudOps~FB1` | closed as the encoding fix at `38f8179f10` on the CTO's ruling (msg 4674): the instrument runs to its last line with no environment override (base: a cp1252 crash); it still reads `ok=False` for four reasons (row `D1-S43`), routed to NFRA_CTLPLN. |
| (item 6, at the cut) | act 2's first scheduled chain read | the issuer | `new-home --since 2026-10-13T03:30:00Z`: 11 of 11 served classes written; `old-home --since 2026-10-12T06:22:08Z`: 0 keys of 11 classes modified (read 06:20Z). |

### FWD-1, stated for the CVO

All 11 disagreements follow ONE rule (the table is the component immediately after the tier); 9 are ruled, 2 fixed (`code/`), no mapping row
changes (`RULING_FWD1_R5.md`). **The readers' face now STATES that rule**, so a reader that obeys it agrees by construction on grammar
conforming strings; the read shows the rule is learnable and unambiguous, not that the mapping's table is the right grain for classes 8-11
(that is the CTO's ratified grain). Independence is the round-4 construction (one-commit tree), the readers are subagents of this session on
one model. The 11 controls guard against a face regression only.

### FWD-4

The validator decides alike on both maps for 2,127 requests built from the legacy map, through its own handler (S3 and key slots mocked; a
locally generated key; the handler requested the canonical key itself). That is the OFFLINE half. The LIVE half is **NOT EXERCISED**: no
non-admin request has crossed the validator on those paths since 15:15:10Z (17 admin-bypass lines; 418 advisor-tier lines exist on other
paths). `D1-S17`'s remediation therefore stays open (the CTO's ADDENDUM 1 item 2: FWD-4 rests on the offline replay plus the first organic
non-admin line).

### The exec-summary diagnosis (FB-h-6), stated

CloudTrail `LookupEvents` returns 0 PutEvents in 17 of 17 enabled regions over 2026-07-15 to 10-13; the bus, the ENABLED rule (pattern
`source bd-pipeline.gold-chain`, `detail-type chain-complete`, target the generator), the Lambda resource policy and `bd-exporter-ec2-role`'s
`events-emit` statement all read correct; no events Deny was read (the SCP read was denied). So the put-events error text is not in any
record. **Stated, not graded:** the zero shows that no call reached the API only if PutEvents is a CloudTrail-recorded class; the worker's
positive control was the events source in general, and the repository holds no other emitter to control with. The runner's CLI identity,
region and output format were not readable by a read-only order. The next act (a runner-side read, or one non-matching test event on the bus)
is a write: it waits on the CTO. The summaries stay stale since 2026-05-04.

### The BD pricing quantification (FB-h-7), stated

- **S32** (measured, re-computed by the issuer from the worker's fetched files with its own code: equal): 830 of 5,366 asset-days (450
  assets; 20 weekday partitions, 2 zero-row) change the T-1 median when de-duplicated by `transaction_id`; max price delta 753.5. The
  `x quantity` amount is `null` (not computed). Writers: `bd_price_update.py:609`, the Lambda twin `lambda_function.py:441`,
  `build_canonical_prices_v2.py:660`.
- **S33** (2026-10-09): 11,108 tied assets in the current file set; `alternative_differs` 0 there (every tie loses to a later-dated row);
  **inferred, not in the record (row W66-S2): AS OF the 10-09 run, 3,906 of 11,108 alternative prices differ.** The record's zero is the
  present state, not the 10-09 served state; dell2's 34 of 160 is the held universe, this is every asset in the file.
- **S34:** B_03 reran (2,473 of 2,473 objects rewritten 2026-10-13T05:13Z); the Lambda twin 35 invocations since 09-02 (its line-143 call
  inferred: no INFO lines logged); the silver script has no run record; served 2026-08-20..23 objects: 2 of 12 changed under the
  instant reading, 0 under the strict day-after reading (the record carries 2). The first version after 08-23 begins 2026-09-27 (row W66-S4).
- **Recommendation: BRIEF_TO_CRO**, on S32 alone. The grader enforces the CTO's rule (any non-zero count goes to the CRO).

## Defects of the issuer in this round (named)

1. AC2 of `FB-h-3` and AC1 of `FB-h-7` named a path in the base checkout, where the record exists only after the drain: both read ABSENT in
   the worker's worktree (rows `W63-S4`, `W66-S8`, BLOCKING, check artifacts); both PASS at the merged HEAD and were re-graded by the issuer.
2. `FB-h-3`'s mock list omitted the render-key branch; two of the worker's probe runs reached a Secrets Manager read of the render public-key
   secret outside the two-S3-read bound (row `W63-S1`, inferred, not in CloudTrail); the replay itself makes no such call.
3. `FB-h-7`'s order named `gold/bd_price_update.py`; the file is under `silver/` (row `W66-S1`). `FB-h-6`'s order bounded the read to us-east-1;
   the worker swept 17 regions because the emit names none (row `W65-S2`), read-only.
4. `FB-h-8`'s close was the issuer's reading of the CTO's msg 4653 ("ok=True and 7/7"): four further causes were unnamed (`D1-S43`).
5. `FB-h-5` named no whose-session; the CTO's answer (the walker) was itself an admin identity: the order parked twice (`D1-S41`, `D1-S42`).

## What the run does not show (stated, not graded)

- The validator's canonical ownership read under a non-admin request is not exercised (FWD-4 live half).
- The put-events failure's cause (FB-h-6 INDETERMINATE); the generator has not run since 2026-05-03.
- That the readers' agreement holds for a face without the table sentence (it was added as the fix).
- The pricing counts are on the CURRENT served set; S33's as-of figure is inferred; the dollar amount (price delta x quantity) is not computed.

## What changed at the close

1. `FB-h-1` to `FB-h-4`, `-6`, `-7`, `-8` flipped complete; `FB-h-5` parked (owner and un-park condition in its record face).
2. `FB-f-9` AC2 and AC3 name the recorded `MOVE_TS` (`D1-C-S34`, `f21abbf184`); `FB-h-8`'s AC1 amended on the CTO's ruling.
3. `dep_stage` EXECUTING -> ROUND_CLOSE.

## What is open (owners)

| item | owner | condition |
|---|---|---|
| FWD-4 live half: one non-admin validator line on the accounts or relationship paths | `1.0.0_SA_CTO~DELL1` (`FB-h-5` parked) | the first organic advisor-tier line, or a non-admin session a seat holds |
| the put-events cause: runner-side read, or one non-matching test event | `1.0.0_SA_CTO~DELL1` | his ruling (a write); then the fix cell under a pair naming up to 158 summary keys |
| the BD pricing rules (S32 first) | `4.0.0_SA_CRO` (a brief under its own project) | `FB-h-7`'s recommendation |
| `D1-S43` (the fence instrument's four re-baseline causes) | NFRA_CTLPLN via MSTR (CTO msg 4674) | the owner's re-baseline; the simulator arms need the laptop identity |
| `D1-W60-S3` (naming gate `/tests/` vs `test/`) | LGIC_ENFORCE (CTO) | the gate's owner |
| c290: one real SEV1 publish delivered | Andrew | his word |
| portal `ROUTER_FIRM_SUFFIX` (`49financial` -> `bd`) | Andrew for PROD | client-facing module |
| PRD sequencing R3 (the `mdpf/{firm}/platinum/*` grant) and R4 (the joint reader census) | `1.0.0_SA_CTO~DELL1` | named into a later enrichment list |
| armed or blocking rows of this round | the CVO | `D1-S41`..`S43`, `W63-S4`, `W65-S1` (ARMED, disarm owner this seat), `W66-S2` (ARMED, disarm owner this seat), `W66-S8` |
