<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-05-25-demov1-to7-snapshot-clean</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-25</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <project_code>ADVI_DEMOV1</project_code>
    <priority>Medium -- Phase-5-followon (structural-bug-not-binding-gate-risk per LD-0030 sequencing pattern). Re-routed AE~C → AE 0.7 base per Andrew sovereign LD-0068 2026-05-25T~23:05Z "just do base AE, get it going on LD 0067 and lets continue".</priority>
    <sla>~1-2d wall (design choice + impl + transform re-run verify). Sequence in LD-0067 WS-A spec pre-positioning window (~1-2 days) when AE 0.7 capacity permits.</sla>
    <!-- AUTHORED 2026-05-25T20:0XZ by 2.0.0_SA_COO under ws CTO [RAVC2-AC1-FINDING-RULING] §6 authorization
         block. Phase-5-followon class. Originally dispatch_held=true pending Andrew Q1 AE~C spawn auth.
         RE-ROUTED 2026-05-25T~23:25Z by 2.0.0_SA_COO per LD-0068 base AE 0.7 spawn (not ~C tilde):
         issued_to flipped to base; status=pending + dispatch_held=false; GO MCP dispatched to AE 0.7
         base inbox same turn. Per LD-0068, AE 0.7 is also pre-positioning for LD-0067 Workstream B
         (Docker quarantine impl) during ws CTO Workstream A spec landing (~1-2 days) — .007 can
         either fit in the pre-positioning window OR sequence after LD-0067 WS-B per AE capacity-assessment. -->

  </metadata>

  <references>
    <prd>docs/architecture/ADVI_DEMOV1.md (v0.1.3+ — section to be amended on ship)</prd>
    <project_json>org/projects/ADVI_DEMOV1.json</project_json>
    <ravc2_evidence>docs/proposals/advi-demov1-phase5-ravc2/evidence_package_LD-0055.md §4 + §9.1</ravc2_evidence>
    <authorizing_ruling>ws CTO [RAVC2-AC1-FINDING-RULING] 2026-05-25T20:0XZ (Option (c) ratified) — §6 authorizes COO to author + dispatch as part of ruling</authorizing_ruling>
    <related_to>org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_DEMOV1.002.dsc-transform-engine-two-pass-pseudonymizer.md (transform-engine implementation)</related_to>
    <claude_md_rules>CLAUDE.md Rules 7-12 (EC2 deploy + S3 artifact model); Rule 17 (silver-tier passthrough discipline does NOT apply — this is a demo-transform write-path concern, not a silver-conversion concern)</claude_md_rules>
  </references>

  <objective>
    Address demo-bucket write-path snapshot-clean discipline gap surfaced during Phase 5 RAVC2 AC2 probe: `data/demo/scripts/transform/fake_identities.py:480-509` advisor() factory uses faker-library RNG slugs (via `_used_slug` salting probe) producing different slug per real-advisor across runs. Different slug -> different S3 path -> no S3 PUT overwrite -> accumulation across runs. Empirical: LD-0055 demo bucket has 1,768 advisor objects (168 LD-0055-fresh slugs + 168 attempt-13-residual slugs = 336 distinct slugs) vs bd's 884 (168 real advisors). Per PRD §1 "identical file structure" + §3 "static snapshot clone" intent, this is a structural divergence. End-state: post-fix re-run of transform produces demo bucket with object-count parity to bd (884 advisors == 884 advisors) without breaking R5/R6 binding-gate semantics.
  </objective>

  <context>
    During Phase 5 RAVC2 AC2 (bucket parity) probe 2026-05-25T19:55Z, ws COO surfaced empirical finding: demo total platinum/ object count = 23,144 vs bd = 22,260 (+884 delta). Per-tier decomposition: clients/, accounts/, firm/ all parity-clean (0 delta each); advisors/ exactly 2.00x (884 -> 1,768) uniform across all 6 file types (exec_summary/mix/nna_clients/positions/summary/timeseries). Slug-set intersection bd ∩ demo = 0 (disjointness preserved); demo unique slugs = 336. S3-LastModified partition shows clean 168 May 25 + 168 May 24 = 336 split (run-by-run accumulation pattern).

    Root cause (per ws CTO ruling §2): faker-library RNG slug write-path lacks snapshot-clean semantics. Clients + accounts use z-prefix hash (deterministic from real-id) -> z-id stable across runs -> S3 PUT overwrites -> snapshot-correct. Advisors use faker-library RNG slug -> different slug per run -> different S3 path -> no overwrite -> accumulate.

    R5 binding-gate PASS-CLEAN holds across all 23,144 demo objects (the structural `_embeds_real` guard catches accumulated objects identically to fresh ones; per RAVC2 §5). AC5 advisor-disjointness verified PASS at consumer-read layer (leaderboard.json references 154 advisors all from May 25 LD-0055-fresh set; zero May 24 residual leakage; per RAVC2 §7.5). The accumulation is invisible at consumer-read; the bug is at the write-path snapshot-clean layer only.

    PRD `docs/architecture/ADVI_DEMOV1.md` L15 ("identical file structure") + L19 ("frozen, refreshable static snapshot") + L59 ("static snapshot clone") specify snapshot semantics. The accumulation IS a structural divergence from PRD intent within demo-bucket scope.

    Per ws CTO ruling §6 authority block, this TO authored under same ruling that closes Phase 5 RAVC2 with PASS-WITH-STRUCTURAL-FINDING. NOT a Phase 5 close blocker; Phase-5-followon class per LD-0030 sequencing pattern (durable-followon, not immediate supersession).
  </context>

  <scope>
    <in_scope>
      DELIVERABLE A -- Design choice between two structural fixes.
        Option (i): clean-before-write advisors/ subpath in transform. Execute an `aws s3 rm s3://opal-data-demo/platinum/advisors/ --recursive` (or equivalent boto3 delete) BEFORE the advisor-write phase of demo_transform.py. Preserves faker-library RNG-driven slug generation (no semantic change in fake_identities.py). Simpler, smaller diff, less invariant-coverage; may need careful sequencing to not interfere with parallel transform phases.

        Option (ii): faker-seed-by-id deterministic refactor. Replace the probe-based `_used_slug` salting in `fake_identities.py:480-509` advisor() factory with a deterministic hash-derived seed per real-advisor-id (analogous to z-prefix hash used for clients/accounts). Same real-advisor -> same fake slug across all runs -> S3 PUT overwrites cleanly. Full determinism across the transform (no remaining accumulation surface); more invasive code change; may require regression testing against existing leaderboard / advisor-detail consumer pages.

        AE author selects design with brief justification (~1 paragraph) at the proposal stage of this TO; CTO reviews + ratifies before implementation start. Either fix is acceptable per ws CTO ruling §2.

      DELIVERABLE B -- Implementation + transform re-run verification.
        - Implement the selected design (i) or (ii) in `data/demo/scripts/transform/fake_identities.py` and/or `demo_transform.py` per choice.
        - Deploy to demo-transform-runner EC2 (i-03343a6072834f77d) via safe-ec2-deploy.sh (S3 artifact model per CLAUDE.md Rules 7-12).
        - Trigger fresh transform run via SSM with the same parameters as LD-0055 (read opal-data-bd/platinum/** -> write opal-data-demo/platinum/**).
        - Verify post-fix object-count parity: `aws s3 ls s3://opal-data-demo/platinum/advisors/ --recursive --summarize` returns 884 objects (== bd's 884), 168 unique slugs (== bd's 168).
        - Verify R5 binding-gate PASS-CLEAN maintained: pii_leak_scan_result.json `leak_count=0` post-fix.
        - Verify AC5 advisor-disjointness independent of leaderboard read mode: leaderboard.json's advisor entries ⊂ demo advisors/ slug set regardless of whether read pulls in-RAM mapping or scans folder.

      DELIVERABLE C -- PRD addendum (small).
        - Append section to `docs/architecture/ADVI_DEMOV1.md` Phase 3 / §3 describing the snapshot-clean discipline at write-path level. Concise (~10-15 lines) — capture the design choice (i or ii) + the invariant ("each transform run produces demo bucket with object-count parity to bd at every tier including advisors/").
        - CTO ratifies the PRD addendum via standard owned-paths POD_DOCS_OR_EXEC lane.

      DELIVERABLE D -- RAVC2-followon notification.
        - On TO close, AE~C sends RAVC2 to ws COO (+ CC ws CTO) confirming:
          - Object-count parity achieved (884 == 884 at advisors/);
          - R5 PASS-CLEAN maintained;
          - AC5 advisor-disjointness invariant holds independent of read mode;
          - Design choice + impl summary;
          - PRD addendum landed.
        - ws COO 3-step closes ADVI_DEMOV1 if no other followon items remain (Phase 5 RAVC2 close was on this run, .007 close is the last structural followon).
    </in_scope>

    <out_of_scope>
      - Re-running R5 PII-leak scan in extended-coverage mode (existing R5 PASS-CLEAN at 23,144 objects is binding-gate sufficient).
      - Visual-smoke AC4 (post-DE track; gated on DE lane availability; not blocked by .007).
      - CVO option-(b) in-run reconcile-artifact capture (separate forward-fix for future Phase-5-class gates per RAVC2 §9.2; not in .007 scope).
      - PRD scope re-litigation -- the snapshot-clone intent is CTO-confirmed in [RAVC2-AC1-FINDING-RULING] §1; .007 implements the structural compliance.
    </out_of_scope>
  </scope>

  <acceptance_criteria>
    <ac1>
      Design choice (Option (i) clean-before-write OR Option (ii) faker-seed-by-id) selected + ratified by ws CTO at proposal stage. Justification documented in TO body (~1 paragraph) before implementation start.
    </ac1>
    <ac2>
      Post-fix transform re-run produces demo bucket with object-count parity to bd at advisors/ subpath: `aws s3 ls s3://opal-data-demo/platinum/advisors/ --recursive --summarize` returns 884 objects + 168 unique slugs (matching bd exactly). No accumulation across the re-run vs pre-fix LD-0055 state.
    </ac2>
    <ac3>
      Post-fix transform run R5 binding-gate PASS-CLEAN maintained: `pii_leak_scan_result.json` `leak_count=0` and `errors: []`. Object-count in scan output drops from 23,144 (LD-0055 accumulated) to ~22,260 (post-clean) -- reflects the eliminated accumulation.
    </ac3>
    <ac4>
      AC5 advisor-disjointness invariant holds independent of leaderboard read mode:
        - leaderboard.json's advisor_id set ⊂ demo S3 advisors/ slug set
        - demo S3 advisors/ slug set ⊂ {LD-{re-run}-fresh slugs} (no accumulated residual)
        - bd advisor names ∩ demo S3 slug set = 0 (cross-bucket disjointness preserved per existing pseudonymization)
    </ac4>
    <ac5>
      PRD addendum landed at `docs/architecture/ADVI_DEMOV1.md` Phase 3 / §3 section. CTO ratifies via standard owned-paths POD_DOCS_OR_EXEC lane.
    </ac5>
    <ac6>
      RAVC2-followon to ws COO confirming all of AC1-AC5 + design choice + impl summary + PRD addendum reference + post-fix S3 inventory snapshot. ws COO 3-step closes ADVI_DEMOV1 on RAVC2-acceptance if no other followon items remain.
    </ac6>
  </acceptance_criteria>

  <dispatch_unblock_condition>
    AE~C lane spawned + active per Andrew sovereign ratification at RAVC2-bundle-ready moment (CY-0128 §3 + Task #10 routing decision). On Andrew GO for AE~C spawn, this TO flips dispatch_held=false + COO sends GO MCP to AE~C with the proposal-stage design-choice request.
  </dispatch_unblock_condition>

</task_order>
