# COMPLEARN P3a -- the behavior-source audit (cloud-ship vs host-local ruling substrate)

**Author:** 0.8.0_AE_CloudComp | **Date:** 2026-07-13 | **Status:** AUDIT COMPLETE -- per-source
dispositions below are RECOMMENDATIONS; the ruling is CTO~D's (arch owner per the COMPLEARN amendment).
**Ground vintage:** working-tree @ 19fde37de + live AWS reads 2026-07-13T02:3x-03:0xZ.
**Amendment executed:** `docs/architecture/NFRA_COMPLEARN_amend_loop-closure_20260710.md` A1/P3a
("Audit the 5 behavior sources; per source, decide cloud-ship vs explicit-host-local-with-alarm; promote
the staleness watch to a hard freshness gate; either make the 'nightly Fargate emit' claim TRUE or delete it.")

## 1. HEADLINE: the estate has MOVED since the 2026-07-10 audit -- two of P3a's three complaints are closed

1. **The "nightly Fargate emit" claim is NOW TRUE for the served surface** -- and I verified it at all
   three layers (Rule 22a), not from the TF: `comp_learns_producer.tf` landed (`15bc9ea12`); rule
   `opal-globgrph-comp-learns-producer-nightly` = `cron(0 4 * * ? *)` **ENABLED** (APPLIED, live
   describe-rule); **fired 3/3 nights** Jul-10/11/12 (CloudWatch `TriggeredRules`, zero
   `FailedInvocations`); the Jul-12 run's logs end `OK: served -> s3://.../served/comp_learns_status.json`
   + `COMP_LEARNS_PRODUCE_COMPLETE views_ok=6/6 computed_at=1783828848` (=Jul-12 **04:00:48Z**), and the S3
   object mtime matches. **CAUTION banked:** `aws s3 ls` prints LOCAL time (EDT) -- the object reading
   "Jul-12 00:00:56" is 04:00:56 UTC; I briefly hypothesized a missed tick off that artifact. It was a
   timezone read, not a stall.
2. **The emit trigger is no longer a silent single-host cron** -- it is a session-close hook
   (`.claude/settings.json:179` -> `tool_activity_emit_local.sh --detach`, throttled 3h, best-effort) so it
   self-heals with fabric activity, PLUS the cloud, host-independent freshness alarm
   (`tool_activity_freshness.tf`, "CTO ruling Option A req #1") watching staleness from outside the host.
   Live state: **all 5 catalog partitions written Jul-12 22:25:58Z** -- fresh.
3. **What remains genuinely OPEN:** (a) the WATCH->GATE promotion (nothing BLOCKS/refuses on a BEHIND
   vintage at read time -- sec. 4); (b) the ROUTING stream rides OUTSIDE the catalog + alarm (sec. 3, the
   one real coverage gap); (c) a one-line PRD text amend (sec. 5).

## 2. The source census (the "5 behavior sources", grounded at two layers)

There are 5 EMITTER PARTITIONS but 6 BEHAVIOR STREAMS -- the counts in prior docs differ because they
count different layers (CTO~A's "3 of 5 gitignored" counts streams; the wrapper's "2 of 5" counts emitter
partitions). Disclosed so nobody re-litigates it:

| # | Stream | File | Git | Emitter partition | In catalog? |
|---|---|---|---|---|---|
| 1 | rolling ledger | `org/compiler-tools-log.md` | TRACKED | `rolling_log` + `rolling_log_summary` (2 partitions, 1 file) | yes |
| 2 | session logs | `org/tier*/**/logs/**/*.md` | TRACKED | `session_log` | yes |
| 3 | rail | `org/mcp/comp-which-rail.log` | GITIGNORED host-only | `rail` | yes |
| 4 | telemetry | `org/mcp/agent_telemetry/*.jsonl` | GITIGNORED host-only | `telemetry` | yes |
| 5 | **routing** | `org/mcp/comproute-routing.jsonl` | GITIGNORED host-only | **NONE** | **NO -- scorer bypass** |

`comp_learns_score.load_corpus` (:155) reads routing DIRECTLY (`parse_routing_log`), not via the catalog.

## 3. Per-source disposition (the P3a ruling substrate -- CTO~D rules)

- **rolling_log / rolling_log_summary / session_log (git-tracked):** COULD cloud-ship, but RECOMMEND
  **explicit-host-local (status quo)** -- the wrapper's stated reason is load-bearing: a SINGLE writer
  stamps ONE parity vintage (`{repo_head_sha, computed_at}`); splitting tracked sources to a Fargate
  emitter while rail/telemetry stay host-local would produce two vintages for one catalog and break the
  comp-drift single-vintage seam (AMD-P3d). The constraint is now LOUD (wrapper header, this audit), not a
  comment -- which is what P3a asked for.
- **rail / telemetry (gitignored, host-only):** IRREDUCIBLY host-local -- no cloud runner can read them.
  **explicit-host-local-with-alarm (status quo, already built):** session-close hook emit + the cloud
  freshness alarm. Nothing to build.
- **routing (comproute-routing.jsonl) -- THE ONE REAL GAP:** host-only, read by the scorer directly,
  **invisible to the catalog AND to the freshness alarm** -- a stalled/duplicated routing log degrades
  COMPROUTE + the rail-consistency axis silently. RECOMMEND: add `source=routing` as a 6th emitter
  partition (the emitter already normalizes richer streams; ~1 parser) OR extend the freshness alarm to
  stamp it; either makes routing staleness observable. This is the P3a build item if CTO~D wants one.

## 4. The WATCH -> HARD GATE promotion (open; recommend the LIVELEARN pattern, not a cron)

Today: the cloud alarm fires on catalog staleness (host-independent, good) and `comp_learns_produce`
carries the AMD-P3d vintage seam (36h BEHIND disclosure in the served JSON) -- but **no consumer REFUSES
or loudly flags a BEHIND vintage at read time**; a stale catalog still SERVES quietly to a reader who
doesn't check. RECOMMEND: the exact consumption-driven pattern CTO~D just ratified for NFRA_LIVELEARN G1
(same arch family, zero new crons, LD-0175-clean): `comp-learns-status` (the reader) checks the served
`computed_at` seam at read time -> within-threshold = render + age line; BEHIND = LOUD banner (never
silent-stale), optionally `--strict` nonzero-exit for gating consumers. Small diff in
`infra/aws/globgrph/comp_learns_status.py` (my lane), CTO~D gates.

## 5. PRD text amend (one line, closes the "make TRUE or delete" clause)

`NFRA_COMPLEARN_PRD.md:65` still reads "Each tick: refresh `tool_activity` from the day's logs ..." -- a
Fargate CANNOT refresh tool_activity (3 host-only streams; sec. 2). The landed architecture is the correct
resolution: **host emits the catalog (session-close, where the data lives) -> cloud alarm watches it ->
the nightly Fargate producer READS the catalog + writes the served status.** Amend :65 to say the tick
"reads the day's tool_activity catalog" (not "refreshes from logs"). docs/architecture = ANY_CTO lane;
routed with this audit.

## 6. Compiler-tools + retrieval discipline notes (banked)

- comp-which routed the audit's estate questions; raw aws reads were operational (rule-legal).
- **Three consecutive silent-empty aws reads during this audit were MSYS leading-/ mangling** and nearly
  recorded a live log group as ABSENT -- now structurally killed by the `.tools/aws` shim (Andrew-direct,
  `AWS_SHIM_MSYS_MANGLING_20260713.md` @ 19fde37de). The last two audit reads ran THROUGH the shim.
- `aws events list-rules --name-prefix comp-learns` returned empty for a rule named
  `opal-globgrph-comp-learns-producer-nightly` -- **control the retrieval:** a prefix filter is a
  hypothesis about naming; confirm absence with the exact expected name (describe-rule), never a prefix.

## 7. What P3a leaves for build (post-ruling)

1. routing-stream visibility (6th partition OR alarm extension) -- sec. 3, my lane on GO.
2. read-time BEHIND gate in comp-learns-status -- sec. 4, my lane on GO.
3. PRD :65 one-line amend -- ANY_CTO.
P3b (leg-4 DRV flip) stays gated on the CTO-owned Goodhart gate; P3c (comp_log_auto disclosure) stays
sequenced behind the .tools daylight hold -- neither is touched by this audit.
