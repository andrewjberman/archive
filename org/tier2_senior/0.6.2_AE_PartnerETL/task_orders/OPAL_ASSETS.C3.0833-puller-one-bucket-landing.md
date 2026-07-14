# OPAL_ASSETS.C3 — 0833 puller deployed → `bronze/schwab/08335338/` + scheduled; backfill copied in

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>pending</status>
<hold_released date="2026-07-14 01:12Z" by="2.0.0_SA_COO">
DISPATCH HOLD SATISFIED. COO relay under coordination authority Andrew handed him ~01:07Z ("You can direct
these through COO, I do not want you to be distracted with Coordination. That can be their job."), against
CTO's pre-authorized criteria. Precondition -- "I want to respawn the workers first" -- MET: DS, 0.6.2,
0.5.0, 0.7.0 all live on the roster. ACK'd 20260714T011329Z.

SCOPE GO'd = C3 PREP ONLY (authored-NOT-applied):
  (a) IAM Terraform for the monolith grant -- written + planned, NOT applied.
  (b) Catch-up PLAN (daily REST pull both masters, direct-to-monolith, same-day catch-up >= 2026-07-13).
  (c) Remap PLAN (7,256 staged objects -> opal-data-assets, zipped copy + ETag verify).
NOT GO'd -- HARD STOPS: no `terraform apply` of anything (every apply gate stays with 1.0.0_SA_CTO); no
LANDING (gated on C1, the monolith bucket, which does NOT exist -- 404 verified live 2026-07-14 01:0xZ,
0.7.0_AE_CloudOps owns it); no EventBridge repoint yet. The 0824 wide pull continues under Andrew's
direct GO, unchanged. Evidence returns to COO; gates and forks to CTO.
</hold_released>
<project>OPAL_ASSETS — Grand Consolidation P1</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 (TO-C3) + §3 ruling 4</prd>

<andrew_amendment date="2026-07-14 ~00:3xZ" channel="Andrew -> CTO, interactive" status="clarification-in-flight">
ANDREW, VERBATIM: "I think we can actually just move the opal-data-schwab backfill from the REST API
over to a schwab bucket with the same path otherwise in the schema you are building. ask 0.6.2_AE about
it to clarify, but I dont think we need to re-download all of that again, easier to just migrate it in
its zipped form to the requisite location. That does not eschew the process of scheduling future daily
pulls from that REST API, but wanted to make that note. Clarify with 0.6.2_AE to this end first, as some
PRD/TO elements may need to be slightly revised based on those findings."
EFFECT ON THIS TO (formal revision follows 0.6.2's answers to the CTO 7-question clarification, 00:33Z):
the backfill lands by ZIPPED S3-to-S3 MIGRATION, never a re-pull; daily REST pulls still get scheduled
going forward. Target-bucket reading surfaced to Andrew for confirmation (CTO reads: the schwab prefix
of opal-data-assets per the consolidation mandate).
</andrew_amendment>

<revision v="1.1" date="2026-07-14 ~00:55Z" by="1.0.0_SA_CTO">
RESOLVED — PRD v1.1 §3 rulings 5–6 bind this TO. Andrew named the bucket to 0.6.2 directly:
**opal-data-schwab/{master}/bronze/{type}/{YYYYMMDD}/** — NOT opal-data-assets. Under Andrew's direct GO
(~00:28Z) 0.6.2 already EXECUTED the backfill half: 0833 migrated zipped 6,932/6,932 (ETag-identical,
0 quarantine; CTO-verified on live S3), 0824 full-history REST pull running. REMAINING SCOPE of this TO:
(a) daily pull SCHEDULED, both masters (EventBridge repoint off the dead GUI task — merges C8 if you
take it); (b) same-day catch-up for business dates >= 2026-07-13; (c) NO dependency on C1 anymore.
Landing target sections above referencing opal-data-assets/bronze/schwab are SUPERSEDED by ruling 5.
Acceptance criteria 3 (backfill parity) is SATISFIED — evidence in PRD §5 R6. Still STAGED under the
dispatch hold.
</revision>

<revision v="1.2" date="2026-07-14 ~01:05Z" by="1.0.0_SA_CTO">
THE MONOLITH (Andrew-direct, PRD v1.2 §3 ruling 9) — this TO's final scope:
(a) prefix-remap the 7,256 staged objects opal-data-schwab/{master}/bronze/... ->
    opal-data-assets/schwab/{master}/bronze/... (zipped S3-to-S3 copy, ETag-verify, your exercised
    pattern; include the 0824 wide-pull remainder as it completes; use a scoped read-source/write-target
    role this time — your own self-flagged gap);
(b) daily REST pull SCHEDULED, both masters, landing DIRECT in the monolith; same-day catch-up >= 07-13;
(c) EventBridge repoint off the dead GUI SchwabAutoDownload task (absorbs C8);
(d) NEW IAM grant against the exact opal-data-assets ARNs (masters enumerated, never wildcarded,
    no GetObject on data) — 22a live-simulate, one --resource-arns per call, positive control separate.
    The exercised opal-data-schwab grant does NOT transfer.
Depends on C1 (the monolith bucket). Grammar: schwab/{master}/bronze/{type}/{YYYYMMDD}/ — ruling 5's
grammar one level down. opal-data-schwab is STAGING after the remap (C12 inventories it; delete nothing).
</revision>

## Scope
Deploy your built+tested 0833 REST puller with a daily schedule, landing in the one bucket:
`s3://opal-data-assets/bronze/schwab/08335338/{TYPE}/{YYYY-MM-DD}/...` — day-one-direct.
Copy the parked backfill (`opal-data-schwab/backfill/08335338/`) into the canonical tree (**COPY job,
never a re-pull, never a delete** — 257 of the 01_raw objects are irreplaceable per your own finding;
that class of caution binds here too).

**Gate:** landing target exists only after C1 (bucket Terraform) lands — staffing-forked to Andrew.
**Fallback (CTO ruling 4, already in your apply-GO message):** if C1 slips >48h, landing in
`opal-data-schwab/08335338/bronze/*` per Andrew's ~20:45Z verbatim grammar is authorized; the
consolidation retarget then becomes a copy job. Prep now either way. **The 0824 backlog recovery under
the apply GO (e6f618f66) is separate and does NOT wait on this TO.**

## Fences
Pull + raw bronze ONLY. No silver, no gold, no served re-derive ("No 49 Yet"). Never rewrite historical
bronze keys in place. Identity from the vendor's bytes (H1 / vendor filename for headerless fam/slm);
unreadable → quarantine. Masters never commingle. No new alarms/watchdogs (Andrew constraint — the
oracle stays held per the apply-GO message).

## <compiler_tools_mandate>
Phase 1 (before writing): enumerate the target-prefix state before first write (your idempotency index);
confirm the SchwabBronzeList grant covers the actual list calls (post-apply live simulate per 22a — one
`--resource-arns` per call, positive control separate). If landing in the NEW bucket: fresh live
simulate against the exact `opal-data-assets` ARNs — comp-iam FAILS GREEN on a new bucket.
Phase 2 (before committing): `.tools/commit-gate.sh` (automatic); any `iam.tf` delta → `comp-iam gaps`.
Phase 3 (after landing): head-object partition listing of landed objects = the RAVC evidence.
</compiler_tools_mandate>

## <cross_domain_coordination>
`opal-data-schwab` prefixes are your own active lane (0824 recovery in flight). C1/C2/C8 assignee (TBD,
Andrew staffing) must MCP you before touching any schwab prefix. The one prohibition binds: nobody
writes `opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
1. `aws s3 ls` shows ≥1 dated partition per 0833 daily type under the landing target, head-object
   verified, with the master read from the vendor's bytes (not the folder).
2. Schedule exists and is ENABLED (`aws events describe-rule` / scheduler equivalent, output quoted).
3. Backfill copied: object count parity between `backfill/08335338/` and the canonical tree, both
   denominators printed (source count = landed count; no sampling).
4. Idempotency exercised: a re-run of the same day lands 0 new objects and reports skip (not error).
5. Session log with Compiler Tools section; RAVC close to CTO with evidence (partition list + rule state).
</acceptance_criteria>
