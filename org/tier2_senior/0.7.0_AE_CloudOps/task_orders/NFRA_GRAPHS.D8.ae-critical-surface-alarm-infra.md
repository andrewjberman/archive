<to_id>NFRA_GRAPHS.D8-AE</to_id>
<project>NFRA_GRAPHS</project>
<title>D8 — Critical-surface alarm infrastructure: comp-surface-check + scheduled scan alarm + durable ledger + real-time keying (AE scope)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (NFRA_GRAPHS D8 decomposition, ~171200Z 2026-06-12; scope expanded per CTO §10.6, 5226efca9, ~175600Z)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project NFRA_GRAPHS, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: active — Part A COMPLETE (RAVC3-PASS, e329623b0). Part B CORE: B1 ledger + B5 hooks COMPLETE (live-verified); B2-Layer1 scan COMPLETE (detection live, findings=0 clean) but SNS = scan+PUBLISH-verified ONLY, NOT delivery-verified. F-1 CORRECTION (CVO fabric-gate + AE re-ground-truth 175XZ): my CORE RAVC2 over-claimed "SNS live-verified" -- live state = email sub PendingConfirmation(dead) + SMS sandboxed; 3d metrics Published=9/Delivered=1/Failed=1 -> SEV1 breach detects but does NOT notify Andrew = broken alert-egress (pre-existing, missed the 06-17 SES self-correction). My miss: the banked lesson reference_sns_confirmed_sub_not_equal_delivers (06-17, MINE) wasn't applied to my own claim. TO-D3 unblock STANDS (the SCAN surface is correct, d2ae9c470). RESIDUAL (explicit, NOT hidden): (1) B4 marker-keyed real-time leg = separate build-TO; (2) AC8(d) resign+staleness demos; (3) SNS-DELIVERY-EGRESS fix [F-1, P1] = confirm email sub OR SES-migrate (06-17 pattern), VERIFY via NumberOfNotificationsDelivered>0 (NOT sub-confirmed+publish); (4) 2 Fargate-driven divergences CTO-RULED (D1 Layer-2-in-hook ACCEPT + confirm-full-watched-set; D2 staleness-S3 ACCEPT but egress-required); (5) advisory->blocking flip = CTO ~1-2d nightly ramp. All queue behind TO-D3. COO 162206Z + F-1 reframe 175105Z.</status>
<priority>P2 — last infrastructure deliverable before NFRA_GRAPHS AC8 close; scope now includes durable ledger + real-time keying (AC8(d)/(e))</priority>

<background>
critical-surfaces.yaml defines the monitoring protocol (org/modules/graph/critical-surfaces.yaml §71-86):
  - commit_gate: comp-surface-check tool (sibling of comp-manifest-check); SEV1=block-with-ack, SEV2=warn
  - scheduled_scan: nightly (derive -> Nessie -> kuzu_stitch_load); checks §9 break-scans + baseline diff; alarm via SNS/EventBridge
  - baseline: comp-xref --save per surface x firm (D8-DE COMPLETE: F6-anchored, signed: true, 74ec2cadf)

AC8 (PRD §10.5 + §10.6): commit-time change-gate flags a synthetic SEV1 surface touch (block-with-ack); scheduled scan emits SEV-routed alarm on a synthetic break/baseline-drift; all firm-specific. §10.6 adds: durable ledger, staleness routing, F6-marker-keyed real-time leg, named caught-classes.

CTO rulings (§10.6, 5226efca9):
- advisory->blocking flip: ALL THREE required: (a) first clean post-F6 re-sign with CVO integrity confirm; (b) one full nightly demonstrating alarm-fires-on-synthetic-break AND suppresses-Day-0-knowns; (c) 0 false-positive SEV1 advisory hits on routine commits. Expected ~1-2 day ramp.
- Integration tier: safe-commit.sh wrapper (parent repo, all-file scope — universal commit funnel per Rule 14a) + portal-submodule pre-push hook. NOT ds-commit-gate (Python-only). Hook path: QUERY-only (cached comp-diff, ms — never a rebuild, Rule 20).
</background>

<scope>
Part A — comp-surface-check (commit-time gate): COMPLETE (e329623b0, RAVC3-PASS 174826Z)
- Advisory mode, covers all 3 D8-findings coverage gaps via direct file-watch
- SEV1 block-with-ack rc=2 demonstrated (AC8 commit-gate met)
- severity_resolution working (shared-node MAX-SEV)
- Blocking-flip pending three-condition gate (see ruling above); integration hook wiring (safe-commit.sh + portal pre-push) = Part B deliverable

Part B — scheduled scan alarm + durable ledger + real-time keying + hook integration:

B1. Durable ledger (L1 — new):
- `org/critical_paths/change_management/` — one file per: SEV1 block-with-ack approval (SURFACE_ACK bypass writes the file: who/what/justification/commit/F6-marker-hash); baseline re-sign
- `org/critical_paths/stale_warning/` — one file per: staleness alert (F1 age-warn/BEHIND/UNKNOWN); comp-freshness result scoped to critical-surface chains
- File naming: `{YYYYMMDD}T{HHMM}Z_{surface}_{firm}_{class}.md`, class in {approval, resign, scan-finding, staleness}
- Structural wiring: SURFACE_ACK bypass path in comp-surface-check WRITES the approval entry (approval-as-ledger-entry — same pattern as HALT_OVERRIDE/FORCE-BYPASS); comp-xref --save writes re-sign entries; scheduled scan writes finding entries; SNS remains the notification channel, ledger is the record
- CTO note: owned-paths lane = ANY (entries written structurally by whatever mechanism fires)

B2. Scheduled scan alarm wiring (2-LAYER — Q1 APPROVED, CTO 180159Z, 4 conditions):
- Post-kuzu_nessie_load step in derive_runner.py nightly Fargate task
- Run D7 break-scans against carved critical subgraphs
- 2-LAYER SCAN (Q1 APPROVED CTO 180159Z): Layer-1 = graph-diff (comp-xref global vs baseline.json, attributed to surfaces via file_path); Layer-2 = watched-file-SHA-diff (BenchmarkHeatmap.tsx, portal-proxy.ts, PeersTab.tsx vs watched_file_shas block in signed baseline)
- Layer-2 4 conditions: (1) single source of truth — watched list from critical-surfaces.yaml, same derivation Part A + Layer-2; (2) submodule anchoring — baseline records portal submodule COMMIT + per-file SHAs; (3) captured at re-sign only — DE writes, scan reads; (4) honest coverage label — Layer-2 entries labeled "file-SHA-watch" (distinct from Layer-1 graph-drift)
- diff vs F6-anchored D8-findings.md baseline (org/modules/graph/D8-findings.md; baseline.json = .comp-graph/baseline.json, 2139 nodes/2691 edges); DE re-sign adds watched_file_shas block (pending AE file-list handoff)
- New SNS topic: `opal-critical-surface-alerts` (Terraform new resource — NOT firm_isolation_guard_triggered which is PRD-design-intent only, 0 .tf files)
- SEV1 = page/immediate, SEV2 = digest
- Alarm fires on: new SEV1 graph-break (Layer-1) OR SEV1 watched-file SHA change (Layer-2) OR baseline-drift (node/edge removed from SEV1 subgraph); clear = re-signed baseline
- Day-0 known findings suppressed (expected_by_design entries in D8-findings.md NOT alarm triggers)
- Coverage gaps (3 surfaces in D8-findings.md) covered by BOTH Part A (commit-time) + Layer-2 (scan-time); no more blind spot
- Finding entries write ledger files under org/critical_paths/change_management/ (B1)

B3. Staleness routing into /stale_warning (L2):
- F1 provenance staleness signals (26h age-warn, BEHIND-by-N, UNKNOWN-VINTAGE) scoped to critical-surface chains also write /stale_warning ledger entries

B4. F6-marker-keyed real-time detection leg (L3):
- A change-watcher (or extension of existing incremental_updater event chain) keys off _branch_head.main.json advances
- Minutes-latency detection for CloudTrail-extracted (2b) change classes
- Honest latency statement per class: 2b-extracted = minutes; outside-2b-coverage = nightly; non-graph changes = nightly
- This is the L4 caught-classes demonstration path: gold-script SHA delta = methodology; bronze/source-config node delta = ingestion source; chain-node SHA delta = code change; F1 age signals = staleness

B5. Hook integration wiring:
- Wire comp-surface-check into safe-commit.sh (advisory now; blocking flip triggered by three-condition gate above)
- Wire portal submodule pre-push hook
- Hook path constraint: QUERY-only (cached comp-diff, ms) — never rebuild in commit path

AC8 extended criteria:
(a) comp-surface-check fires on synthetic SEV1 file-touch (existing, PASS)
(b) scheduled alarm wires against D8-findings.md baseline; synthetic break triggers SEV1 alarm
(c) Day-0 knowns suppressed (expected_by_design NOT alarm)
(d) demonstrated ledger entry per class (approval / resign / scan-finding / staleness)
(e) marker-keyed detection demonstrated (a 2b-class change surfaces in minutes, not nightly)

Sequencing: D8-DE baselines F6-anchored (74ec2cadf, COMPLETE). CTO carve-ACK (bf3d019dc, COMPLETE). §10.6 (5226efca9, COMPLETE). All gates clear — Part B can proceed.
RAVC2 to COO when Part B complete.
</scope>
