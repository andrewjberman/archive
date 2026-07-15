# OPAL_ASSETS.C3 — 0833 puller deployed → `bronze/schwab/08335338/` + scheduled; backfill copied in

<issued_to>0.6.2_AE_PartnerETL</issued_to>
<issued_by>1.0.0_SA_CTO (OPAL_ASSETS owner)</issued_by>
<date>2026-07-14</date>
<status>complete</status>
<closure date="2026-07-15 ~17:3xZ" by="0.6.2_AE_PartnerETL" authority="COO idle-capacity dispatch 20260715T170053Z item 2 (close-on-evidence citing the WS-A1 AC, no new work) + Andrew-direct proceed on the Glacier closure leg; re-parented into OPAL_CONSOLIDATION WS-A1 per the P0 wave 154917Z">
CLOSED ON EVIDENCE -- every AC discharged; the LAST open leg (AC5 Glacier) closed this window:
  AC1/AC2  daily REST pattern BOTH masters LIVE since 2026-07-14 (tag schwab-si2-iam-v1.3.0, rules
           canonical-schwab-si2-{08242234,08335338}-daily-pull ENABLED; monolith partitions landing daily,
           listing-verified -- the WS-A1 drain consumes them).
  AC3      SATISFIED-HISTORICAL (0833 backfill 6,932/6,932, CTO-verified, PRD S5 R6).
  AC4      remap both masters complete (0833 6,932/6,932 3-tier; 0824 remap run post-pull-terminal 07-14).
  AC5      GLACIER LEG COMPLETE 2026-07-15: 257 pre-floor objects enumerated AT RUN TIME (40 STANDARD +
           217 restored-ready, 0 frozen; window to 07-29), all 257 H1-attested 08242234, 0 quarantined ->
           257/257 copied + 3-TIER verified (set 257/257, size 257/257, ETag 246 single-part, MD5 11
           multipart streamed+hashed). PreFloorRestore grant REMOVED (commit 83c81bae5, apply 0-diff,
           tag schwab-si2-iam-v1.5.0); removal evidenced LIVE: simulate s3:RestoreObject on the exact
           01_raw key -> implicitDeny; positive control s3:GetObject same key SEPARATE invocation ->
           allowed (Rule 22a). Two remap-script defects found+fixed at execution (restored-visibility via
           listing RestoreStatus; dst listing per conditioned prefix) -- in the same commit.
  AC6      22a simulate battery banked at v1.2.0-v1.4.0 (6/6, DESIRED+APPLIED+EXERCISED).
  AC7      idempotency exercised (re-run skip counts in the remap; converter skipped-idempotent law).
  AC8      session logs 2026-07-14/15 with Compiler Tools; RAVC close to COO 20260715 (this closure's
           companion message), gates routed through CTO.
NOTE: PreFloorRawRead/PreFloorRawList grants REMAIN (their closure was not ruled) -- flagged to CTO as a
follow-up candidate. opal-data-schwab stays STAGING (C12 inventories it; nothing deleted).
</closure>
<state date="2026-07-14 ~04:4xZ" by="2.0.0_SA_COO (reconciliation)">
LANDED SO FAR: 0833 remap DONE (6,932/6,932, 3-tier, AC3-historical + AC4 partially discharged for 0833);
BOTH-MASTERS daily REST schedules APPLIED + LIVE (0d8607926 -> 6/1/0, tag schwab-si2-iam-v1.3.0, rules
ENABLED staggered, session-locked -- Andrew-direct ~03:4xZ executed ~04:08Z); RestoreObject grant applied
+ 217/217 Bulk restore RUNNING background. REMAINING: 0824 remap on pull-terminal (~06:00Z) + the live
per-master exercise on SDD-session-free + Glacier collection + grant removal (AC5). Pending is correct.
</state>
<hold_released date="2026-07-14 01:12Z" by="2.0.0_SA_COO" amended="2026-07-14 ~02:3xZ per Andrew-ordered review (findings 18/24/34/48) + rulings v1.3.8">
DISPATCH HOLD SATISFIED. The full authority chain (cited in full because a release without its chain is
indistinguishable from a breach):
  1. Andrew's release protocol (CTO relay, msg 20260714T005942Z): "Andrew is spawning YOU + DS + 0.6.2...
     spawned agents reach out to ME confirming readiness; I validate against the live roster and GO the
     staged TOs in dependency order." The GO condition Andrew set = respawn + readiness confirms, CTO
     holding the GO.
  2. Andrew ~01:07Z, verbatim: "You can direct these through COO, I do not want you to be distracted
     with Coordination. That can be their job."
  3. CTO's pre-authorization (msg 20260714T010814Z, verbatim): "GO RELAYS against the staged TOs AS
     WRITTEN... 0.6.2 on his readiness confirm: C3 PREP (IAM TF authored-NOT-applied + catch-up plan +
     remap plan). C3 landing/apply still gates through me" -- "pre-authorized, no round-trip to me needed."
  4. Precondition MET on the live roster (DS/0.6.2/0.5.0/0.7.0 all LIVE, verified at relay). ACK'd
     agent-side 20260714T011329Z.

SCOPE GO'd = C3 PREP ONLY (authored-NOT-applied). Item letters below are THIS BLOCK'S GO-scope letters,
distinct from revision v1.2's scope letters -- do not cross-reference them:
  (i)   IAM Terraform for the monolith grant -- written + planned, NOT applied.
  (ii)  Catch-up PLAN (daily REST pull both masters, direct-to-monolith, same-day catch-up >= 2026-07-13).
  (iii) Remap PLAN (staged objects -> opal-data-assets; denominator ENUMERATED AT RUN TIME per ruling 13b
        -- never a document count; verify per ruling 13c's 3-TIER protocol, never naive ETag-identity).
  (iv)  [v1.3.8 addition] Glacier leg: RestoreObject grant (01_raw/* on the dedicated remap role ONLY,
        BULK/Days=14) authored + planned to CTO's gate; restore is C1-INDEPENDENT and kicks off on grant
        apply; RESTORE -> WAIT -> COPY -> VERIFY(13c MD5 tier inside the window); grant REMOVED at
        migration completion (closure step).
NOT GO'd -- HARD STOPS: no `terraform apply` of anything (every apply gate stays with 1.0.0_SA_CTO); no
LANDING (gated on C1, which 404'd live 2026-07-14 01:0xZ; 0.7.0_AE_CloudOps owns it -- apply GO'd 02:03Z,
in flight; **SUBSEQUENTLY LANDED + COO-verified live ~02:55Z — the landing gate is DISCHARGED and the
landing GO issued 20260714T025839Z**); the schedule work per (c)-as-amended: CREATE-NEW only, no repoint.
The 0824 wide pull continues under Andrew's direct GO, unchanged. Evidence returns to COO; gates and
forks to CTO through COO.
</hold_released>
<project>OPAL_ASSETS — Grand Consolidation P1</project>
<prd>docs/architecture/OPAL_ASSETS_CONSOLIDATION_PRD.md §4 row C3 + §3 rulings 5/6-as-amended/9/13b/13c + the v1.3.8 Glacier ruling (binding vintage: v1.3.8 @ a0ed08933 + the 01_raw scope addition @ 27841e6ab; ruling 4 is SUPERSEDED-BY-5, provenance only)</prd>

<andrew_amendment date="2026-07-14 ~03:4xZ" channel="Andrew -> COO, interactive" status="binding -- answers 0.6.2's ~03:2xZ offer">
ANDREW, VERBATIM: "We need daily rest pattern for both 0833 and 0824 on that box, yes."
SCOPE AS RECORDED: the "yes" answers 0.6.2's standing offer -- stand up the daily REST pull pattern for
BOTH masters on the Schwab SI2 box, SOONER rather than waiting for the 0824 wide pull to go terminal.
This elevates C3(b) [puller retarget, both masters, monolith-direct] + C3(c)-as-amended [CREATE-NEW
schedule -- the create-new ruling stands] to the lane's front. Mechanics remain the assignee's + CTO's
gates: the do-not-repoint-a-running-producer discipline governs HOW the deploy lands while the 0824 wide
pull is mid-flight (0.6.2's own staging escape hatch exists for exactly this); applies via safe-apply
through CTO as always. The 0833 silent-freeze-at-07-10 exposure 0.6.2 flagged is the WHY.
</andrew_amendment>

<andrew_amendment date="2026-07-14 ~02:41Z" channel="Andrew -> COO, interactive" status="binding -- priority ruling on the Glacier/257 leg">
ANDREW, VERBATIM: "i dont care about the glacier schwab data that much to hold up our work here."
SCOPE AS RECORDED (surfaced, not adjudicated): a PRIORITY ruling, not a reversal -- the ~01:4xZ migrate
ruling ("We can keep those unique files in bronze, bring them over in migration") STANDS, but the
Glacier/257 restore leg is BACKGROUND FILL: it holds up NOTHING, it preempts NOTHING, and no main-line
work (C1 apply, C3 remap/schedule, any C-series lane) waits on or yields to it. The restore-kick urgency
in the 02:37Z apply-GO relay ("every hour it waits...") is INVERTED: kick it whenever it costs nothing,
let the thaw run unattended, collect the 257 whenever they are ready. If the leg ever competes with
main-line work for attention or a gate slot, the main line wins without asking.
</andrew_amendment>

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
(c) *(AMENDED per CTO ruling 20260714T030017Z under the new-territory rule — the original "EventBridge
    repoint off the dead GUI SchwabAutoDownload task" is DEAD: a repoint MODIFIES an existing scheduler,
    which new-territory forbids.)* **CREATE A NEW EventBridge schedule driving the REST puller.** The
    dead GUI task and `canonical-schwab-si2-download-schedule` stay UNTOUCHED — they do harmless nothing
    on the 08:35/20:35 cycle (verified live) and retire WITH the legacy pipeline per the standing
    pattern; two schedules do not collide when one drives a corpse. (Still absorbs C8's intent: the
    daily pull gets a working schedule.)
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

**Gate:** landing target exists only after C1 (bucket Terraform) lands — `0.7.0_AE_CloudOps` owns it,
apply GO'd 02:03Z.
**Fallback — SUPERSEDED, DO NOT USE (review finding 23/31/44):** the v1.0 fallback ("if C1 slips >48h,
land in `opal-data-schwab/08335338/bronze/*`") is DEAD under ruling 9 (THE MONOLITH is the only home;
`opal-data-schwab` is STAGING) and under the hold_released hard stop (no landing anywhere until C1). It
is retained in this paragraph only so its absence is not mistaken for an omission. **The 0824 backlog
recovery under the apply GO (e6f618f66) is separate and does NOT wait on this TO.**

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
Phase 3 (after landing): ListObjectsV2 partition listing (key + ETag + Size) of landed objects = the
RAVC evidence (listing-based per the 20260714T024205Z ruling; head-object is never the acceptance
instrument).
</compiler_tools_mandate>

## <cross_domain_coordination>
`opal-data-schwab` prefixes are your own active lane (0824 recovery in flight). `0.7.0_AE_CloudOps`
(C1/C2 owner; C8 is absorbed into this TO) must MCP you before touching any schwab prefix. The one
prohibition binds: nobody writes `opal-data-inf/gold/meta/pipeline-complete.json`.
</cross_domain_coordination>

## <acceptance_criteria>
*(Reconciled 2026-07-14 ~02:3xZ to the v1.2 final scope + v1.3.8 — review finding 33: the original AC set
predated rulings 9/13b/13c and did not cover the GO'd scope.)*
1. `aws s3 ls` shows ≥1 dated partition per 0833 daily type under the MONOLITH landing target
   (`opal-data-assets/schwab/{master}/bronze/{type}/{YYYYMMDD}/`), **verified LISTING-BASED —
   ListObjectsV2 key + ETag + Size (CTO ruling 20260714T024205Z; your remap role structurally cannot
   head-object the monolith, and that role shape is the ratified design property)**, master read from
   the vendor's bytes (not the folder).
2. Schedule exists and is ENABLED (`aws events describe-rule` / scheduler equivalent, output quoted).
3. *(SATISFIED-HISTORICAL — v1.1: the 0833 backfill migration is DONE, 6,932/6,932 ETag-identical,
   CTO-verified, PRD §5 R6. Kept for provenance; not re-run.)*
4. REMAP (v1.2 scope a): staged objects copied into the monolith with the denominator ENUMERATED AT RUN
   TIME from the source at copy time (ruling 13b — never a document count), remap run after the 0824 pull
   is terminal or re-run to convergence, verified per ruling 13c's 3-TIER protocol (listing-ETag
   single-part / source-stream-MD5 vs dest-ETag multipart / size always). Both denominators printed.
5. GLACIER LEG (v1.3.8): the 257-class pre-floor objects restored (BULK), copied inside the restore
   window, H1-observed master per file (scan-for-exactly-one, positional indexing banned), unreadable ->
   quarantine; the RestoreObject grant REMOVED at completion, removal evidenced by a fresh live simulate
   showing implicitDeny.
6. MONOLITH IAM (v1.2 scope d): live simulate per 22a against the exact opal-data-assets ARNs — one
   `--resource-arns` per call, positive control its own invocation, `--context-entries` on conditioned
   statements. DESIRED + APPLIED + EXERCISED reported separately.
7. Idempotency exercised: a re-run of the same day lands 0 new objects and reports skip (not error).
8. Session log with Compiler Tools section; RAVC close **to COO** with evidence (partition list + rule
   state + simulate outputs); gates and forks to CTO through COO.
</acceptance_criteria>
