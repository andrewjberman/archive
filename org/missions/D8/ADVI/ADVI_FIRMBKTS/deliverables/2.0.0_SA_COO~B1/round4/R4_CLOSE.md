# ADVI_FIRMBKTS -- round 4 close: the window ran; 49financial serves from its own bucket (2.0.0_SA_COO~B1, dell1, 2026-10-13 ~05:1xZ)

**Instrument:** the issuer's checks in `deliverables/2.0.0_SA_COO~B1/round4/checks/` and `round3/checks/`, each actor's instance
validated with `proof-of-spec-check.py --governing-order`, and read-only live AWS reads by `cloudops-dell1-agent-user` at the times named
(distribution, Lambda configurations, S3 listings and heads, CloudWatch metrics and logs, CloudTrail lookups). Where this seat could
not read (IAM simulate: the dell1 identity is refused), the laptop lane's printed lines are cited as theirs.
`round-close-check.py --project ADVI_FIRMBKTS --round 4`: 48 orders, 47 complete, 0 not complete outside the verdict, proofs 47 of 47,
judgment 0, verdict **MAY-CLOSE** (read 04:5xZ after the round-close hygiene commit `ca1fe40a70`).

## The result: the window's acts (all landed 2026-10-12, each with its signed pair)

| act | what | executor | result (read by this seat unless marked) |
|---|---|---|---|
| 0 and addendum | producers' grant and the Delete statement | FB1 / FBL | applied under both halves (`FB-f-16` @2658e9ff96) |
| 3b, 3c, 4b identity | readers' admission, exec-summary fence row, exec-summary canonical-put policy | FB1 (apply), FBL (close simulation) | `FB-f-14`, `FB-f-17`, `FB-f-18` applied; `FB-f-15` re-run from the committed `r4_sim.py`: 9 of 9 admitted allowed, 2 of 2 negatives explicitDeny, OAI one Get-only statement (laptop commit d6093ad983; not re-run here) |
| 2 producers' mode move | 19 `.py` objects and the dispatcher switch, `MOVE_TS` 2026-10-12T06:22:08Z | FB1 (`FB-f-9`) | deployed-equal 20 of 20 (`--ref a9f4bac7b5`); the first scheduled chain after act 4 (23:00Z fallback, exit 0, 23:00:11Z-01:18:35Z): new home written 11 of 11 classes, legacy home 0 keys modified since `MOVE_TS` (my reads 23:52Z and 01:30Z) |
| 3 delta copy | 49,110 overwrites and 121 new keys, rollback record per key | FB1 (`FB-f-10`) | DEST-VS-MANIFEST EQUAL 53,031 / 0 / 0 / 0, SOURCE UNCHANGED (my re-run 07:38Z); ownership key equal |
| 4b, 4c Lambdas | exec-summary-generator and opal-partners-data to `canonical` (code and ONE env key each) | FB1 (`FB-f-13`) | CodeSha256 `fdPwodukz88d...` and `c9FXD84szSBD...` (equal my rehearsal; live read); partners sample EQUAL 8 of 8 (7 by body hash, one gzip case by decompressed content, claim `replayed-prior-artifact`); **4b's put NOT EXERCISED** (below) |
| 4 flip, flip commit | the ONE registry value, 16 files, merged | worker ~53 (`FB-g-30`) | `69679b90e3`; `r4_flipcommit --verify` 4 of 4 on the commit itself (my detached checkout) |
| 4 flip, eight re-pins | `loaders.py` at the flip commit in 8 source-map rows | worker ~54 (`FB-g-31`) | `e274a0e60c`; `r4_repin` 3 of 3 at the re-pin commit |
| 4 IRPT leg | eight consumers redeployed 14:03:43Z-14:13:46Z | FB1 (`FB-f-11`) | `r4_act4 --arms irpt` 8 of 8 live; the actor's expectation file equals the issuer's; ycharts-generate from `scratch/r4-act4-ycharts-pin` (CTO 4312); sample 14 of 14 EQUAL |
| 4 edge leg | router v28 x5, guard v7 x5, validator v23 x26 at 15:12:43Z-15:15:10Z | FBL (`FB-f-19`) | `r4_act4 --arms edge` 6 of 6 live (my read), WAF ACL equal rule by rule (the laptop's lines) |
| c290 SMS | account `default_sms_type = "Transactional"` | FBL (`FB-f-20`) | applied 2026-10-11 17:19Z, plan 1 to change; the real SEV1 publish is Andrew's word (not given) |
| Inflection fence admit | one scoped row, three statements on `opal-data-inflection`, applied 01:17:20Z-01:18:05Z | FBL (`FB-f-21`) | live policy carries the three; product-path walk (dell2 COO~P2, 02:15Z): 11 GETs 200, body COMPUTED, explicit-deny 0 before and after; my log read agrees |

Built dormant and merged earlier in the round (graded at their drains): the readers' mode seams `FB-g-1..-18`, the registry and builder
work `FB-g-19..-29`, the SMS census `FB-g-32` (54 publishers), the Terraform variable carriers `FB-g-33`, `-34`, `FB-g-35`, the partners
event census `FB-g-36` and the edge test expectations `FB-g-37`.

## What the run does not show (stated, not graded)

- **4b's put is not exercised.** `exec-summary-generator` is triggered by a `chain-complete` event (`exec-summary-trigger`, no schedule), not a
  04:30Z cron (the issuer's premise, wrong). The dispatcher's `put-events` fails at every chain close since at least 2026-04-25; the
  generator has not run since 2026-05-03 (invocations 7 on 04-26, 1 on 05-03, none since; TriggeredRules none since 09-01). The summaries
  have been stale since 2026-05-04, before and independent of the move (row `D1-S40`; CTO ADDENDUM 12: no manual invoke, a read-only diagnosis
  cell in round 5, the fix under its own pair).
- **No live 49financial request crossed the router after the edge leg** (25 router lines in 45 minutes, all cottonwood). The router
  behaviors for 49financial are evidenced by the oracle (nine pairs HEAD 9 of 9 in the canonical bucket), the handler probe and the
  gates (router 52 pass, guard 47 pass), not by live traffic.
- **The validator's canonical ownership read is not exercised** (27 v23 request lines, none on an accounts or relationship path; L6
  closed as a labelled residual, CTO-ruled).
- **The performance adapter's evidence write is not exercised** (the stored selection is unreadable to the actor); its canonical read was
  simulated allowed and then exercised on the Inflection path by dell2. The adapter's PutObject grants are on IRPT's own buckets.
- **The AFTER sample is a sample:** 14 of 14 over seven functions; the performance adapter and the validator are read apart.
- **The staff view:** the portal's `ROUTER_FIRM_SUFFIX` still sends `?firm=bd` for 49financial; after the flip that slug is refused for
  `platinum/advi/49financial/` and reads the frozen legacy bucket for other classes (router probe). `?firm=49financial` works. A portal
  follow-up, client-facing module, PROD needs Andrew's word.
- **Two unreleased commits of other projects are not shipped by this round:** MDPF_SECCLASS `77849c4924` (C_06, D_04) and, in
  ycharts-generate, IRPT_YCDGEN/IRPT_BCKEND `8af5a63bae`, `4c4dbeda86`, `74bbdbb322` (deployed artifact is their pre-state plus the flip;
  CALL `894b` read by `2.0.0_SA_COO~P2`).

## Defects of the issuer in this round (named)

`S22` the `for_each` key typed as the bucket name in `FB-f-21` (AC1 vacuous; corrected); the `cron(30 4 ...)` premise of the runbook's
step 9; "no chain ran at 23:00Z" (it did); the `--base HEAD` of the flip verifier and the sample tool's gzip hash (both fixed in the
tools); `FB-g-37` was cut late: the edge build gates were not run at the flipped tree before the GO (they read 42/9 and 43/3).

## What changed at the close

1. `FB-g-30`, `FB-g-31` flipped complete (both instances VALID); `FB-g-16` re-graded at its merge commit (5 of 5 arms; AC3 from the merge
   diff); four instance files renamed to their orders' names (`git mv`, bytes unchanged) (`ca1fe40a70`).
2. Crossbox `b312` and `d5e7` closed SUPERSEDED by the acked `894b` under the CVO~L verdict; `ae20`, `5a5a`, `843a`, `796f`, `79e4`,
   `2b72` from-sides closed.
3. `dep_stage` EXECUTING -> ROUND_CLOSE.

## What is open (owners)

| item | owner | condition |
|---|---|---|
| c290 close: one real SEV1 publish delivered | Andrew (word asked by the CTO) | his word |
| portal `ROUTER_FIRM_SUFFIX` (`49financial` -> `bd`) | FIRMBKTS round 5 + Andrew for PROD | client-facing module |
| exec-summary generator dormant since 05-04: read-only diagnosis of the `put-events` failure, then the fix under a pair naming up to 158 keys | round 5 cell (CTO ADDENDUM 12) | the diagnosis first |
| `mdpf/{firm}/platinum/*` serving grant before CANON M9 | round 5 named cell (CTO R3) | own pair |
| joint reader census (MDPF readers of `opal-data-bd/-inf/-cot`) before F12's clock | round 5 (CTO R4) | with denominator |
| the PutObject simulate of the adapter against IRPT's reporting bucket; the real evidence run | IRPT_PERFADPT's COO | next server-issued selection |
| F8 Inflection (FWD-7/FWD-8), F9 Cottonwood, F12 retirements | Andrew's rulings / not started | no clock running |
| scratch branch `scratch/r4-act4-ycharts-pin` | this seat | delete once a later IRPT release supersedes it |
| armed/blocking rows to disposition | the CVO (adjudication) | `D1-S21`..`S22`, `D1-S35`..`S40`, `W54-S2`, `W60-S3` and the open check-artifact rows of workers ~39, ~53 to ~60 |
