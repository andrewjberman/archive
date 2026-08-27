<to_id>ADVI_COTETL.AUAFIX-L6</to_id>
<project>ADVI_COTETL</project>
<title>cot AUA exclusion rule = SNAPSHOT-ZEROED ONLY: remove the AP no-activity gate (45d/180d) from the cot path -- the exclusion RULE is wrong (~$3M understatement)</title>
<assigned_to>0.4.0_DS_ClientPlatform</assigned_to>
<issued_by>2.0.0_SA_COO (AUAFIX scope-add, 2026-06-18; Andrew-direct business rule via AE; PRD update pending CTO)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project ADVI_COTETL, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: pending</status>
<priority>HIGH (correctness -- a certified-AUA producer applies a WRONG exclusion rule) -- but bundles into DS tomorrow-AM re-engagement. DISTINCT from L1 (chain-freeze) + L2 (source-cadence): it's "the exclusion RULE is wrong", INDEPENDENT of the freeze. Andrew-direct business rule (relayed via AE 201554Z); CTO updating the PRD -- align framing if CTO's update adds nuance.</priority>

<references>
  <ref type="prd">docs/architecture/ADVI_COTETL_AUAFIX_PRD.md -- CTO RULED + FOLDED L6 into the PRD (19ca71f96 + AC6). This TO aligned to the CTO ruling.</ref>
  <ref type="cto-ruling">CTO 201908Z (19ca71f96): cot AUA exclusion collapses to ONE rule -- snapshot-zeroed ONLY. (a) REMOVE AP no-activity gate (D_04:1224 / D_03:610 / C_06); (b) AUTOMATE snapshot-zeroed as the general predicate, REPLACING the manual 4-account aua_overrides.json (verify the auto-set catches the validated-4 first); (c) REMOVE the phantom <$100 gate (CTO's interpretation of "zeroed" -- carries a flag for Andrew's veto; small $). Correctness change to a SERVED metric -> verify-on-served before cert; co-verify w/ L1+L2 at L5.</ref>
  <ref type="andrew-rule">Andrew-direct business rule (via AE 0.7.0_AE_CloudOps 201554Z): cot AUA exclusions = SNAPSHOT-ZEROED ONLY (exclude accounts the snapshot shows at $0 = money gone / txns lagging = the existing ghost/RC6 rule). The AP "no-activity" gate (45d/180d) is WRONG for cot.</ref>
  <ref type="ground-truth">AE confirmed the AP no-activity gate is ACTIVE TODAY at: D_04.client_portal_summary.py:1224 (the CERTIFIED-AUA producer) + D_03 + C_06 -- excluding dormant-but-real accounts. Impact: ~$3M understatement (corrected AUA ~$365.7M vs the $362.6M served). lib/exclusions.py is the edit point.</ref>
  <ref type="snapshot-first">memory/project_cot_snapshot_first_no_inject_no_schwab -- cot is snapshot-first; the snapshot-zeroed exclusion (money-gone) is the CORRECT cot rule; the AP activity-gate is a 49F/bd-fork rule that doesn't fit cot.</ref>
</references>

<scope>
Correct the cot AUA exclusion rule to SNAPSHOT-ZEROED ONLY:
1. **RE-VERIFY at fix-time (premise discipline -- do not assert blindly):** confirm the AP no-activity gate (45d/180d) is in fact ACTIVE on the cot path at D_04.client_portal_summary.py:1224 + D_03 + C_06 (AE's ground-truth), and that removing it yields the corrected AUA (~$365.7M expected). If the live code differs from AE's read, surface it before editing.
2. **(a) REMOVE the AP no-activity gate** from the COT path at D_04:1224 / D_03:610 / C_06 (keep it for 49F/bd paths -- per-firm rule; cot-path-scoped, NOT a global removal). The main AUA add-back.
3. **(b) AUTOMATE snapshot-zeroed as the GENERAL predicate** (CTO ruling): replace the MANUAL 4-account aua_overrides.json with an automated snapshot-$0 predicate -- BUT first VERIFY the auto-set catches the validated-4 (don't drop the manual list until the auto-predicate provably covers it). The cot exclusion collapses to this ONE rule (the ghost/RC6 money-gone snapshot-zeroed).
4. **(c) REMOVE the phantom <$100 gate** (CTO ruling -- CTO's interpretation of "zeroed"; CARRIES A FLAG FOR ANDREW'S VETO): remove it; if Andrew wants a dust-floor, it's a 1-line scope tweak that does NOT reopen (a)/(b). Small $ either way.
5. **Re-verify the corrected AUA** on the SERVED artifact (post the next gold-run / L1 nightly): AP-gated dormant-but-real accounts now INCLUDED; corrected AUA ~$365.7M+ (vs ~$362.63M served); snapshot-$0 accounts still excluded. Reconcile account-level deltas. Co-verify with L1+L2 at L5 (do NOT certify the corrected AUA off L6 alone while L1/L2 are still moving -- all three feed the SAME final AUA).
DS commit cycle per Rule 13 (ds-commit-gate; comp-pipescript io on D_04/D_03/C_06 for column-gaps + consumers of the AUA).
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before editing lib/exclusions.py">
    <step>
      <run>comp-pipescript io [D_04.client_portal_summary.py + D_03 + C_06] -- confirm the AP-gate is on the cot path + map AUA consumers; re-verify line 1224 is the active gate</run>
      <expect>AP no-activity gate confirmed ACTIVE on the cot AUA path at the cited locations; consumers of the certified AUA mapped (so the +$3M correction's blast is known).</expect>
      <if_mismatch>If the gate is NOT active where AE cited, or the cot path already excludes it, STOP + surface to COO/CTO -- the premise (AE's read) needs reconciling before the edit (re-verify-at-fix-time).</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>ds-commit-gate (py_compile + ds-precommit + ruff FA) + confirm the AP-gate removal is COT-PATH-SCOPED (49F/bd paths still gate -- per-firm separation, Rule 13/bd-cot-separation)</run>
      <expect>Clean gate; the edit is cot-scoped (NOT a global AP-gate removal -- that would break 49F/bd).</expect>
      <if_mismatch>If the AP-gate is shared-code (not firm-scoped), the fix needs a firm-conditional -- do NOT remove it for 49F/bd. Surface the shared-code structure to CTO.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after the gold-run (served verify)">
    <step>
      <run>Read the SERVED cot AUA artifact's value post-fix (head-object / comp-freshness)</run>
      <expect>Corrected AUA ~$365.7M (AP-gated dormant-but-real accounts re-included; snapshot-$0 still excluded). The ~$3M understatement resolved.</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
- **CTO owns the PRD update** (AE relayed the scope-add) -- align this TO's framing if CTO's PRD update adds nuance. The threshold sub-decisions (snapshot-zero automation + phantom<$100) route to CTO (possible Andrew confirm).
- **Independent of L1/L2** -- the exclusion rule is wrong regardless of the chain-freeze (L1) or basis-cadence (L2). But the served-verify (phase 3) wants a gold-run -- coordinate with L1 (if L1 confirms the chain fires on the 06-19 nightly, L6's fix can land on that run; if L1 needs a manual run, fold L6).
- **L5 (CVO+AE) covers the corrected-AUA check** once DS lands L6 -- AE's L5 verify includes the ~$365.7M corrected-AUA assertion.
- **Per-firm separation (Rule 13):** the AP-gate stays for 49F/bd -- this is a COT-PATH-SCOPED removal, never global.
- **Bundles into DS tomorrow-AM** alongside L1-silver/L2-DS/L3 + the NNA value-gate decompose.
</cross_domain_coordination>

<acceptance_criteria>
- AC6 (PRD, CTO-ruled): the cot AUA exclusion rule is SNAPSHOT-ZEROED ONLY. (a) AP no-activity gate REMOVED from the cot path (D_04:1224/D_03:610/C_06; re-verified active first), 49F/bd unaffected; (b) snapshot-zeroed AUTOMATED as the general predicate, replacing the manual aua_overrides.json -- auto-set verified to catch the validated-4 before the manual list is dropped; (c) phantom <$100 gate REMOVED (with the Andrew-veto flag honored if he wants a dust-floor).
- Corrected AUA ~$365.7M+ on the SERVED artifact (vs ~$362.63M served); account-level deltas reconciled; snapshot-$0 still excluded.
- Premise re-verified at fix-time (AP-gate confirmed active at the cited lines before the edit), not asserted blind.
- Co-verified with L1+L2 at L5 (the corrected AUA is NOT certified off L6 alone while L1/L2 move).
- Session log Compiler Tools section reproduces every `<run>` with the served-AUA value + pass/fail.
</acceptance_criteria>

<data_reprocess_scope><conditional>The exclusion-rule fix re-emits the corrected AUA on the next gold-run (the L1 nightly or a manual run). No bronze/silver reprocessing -- a gold-tier business-rule correction in lib/exclusions.py. Served AUA value changes (~$362.6M -> ~$365.7M) -- this is a CORRECTION (fresher-AND-more-correct), not a widen; ships with a before/after note (the +$3M is the dormant-but-real re-inclusion, Andrew-direct).</conditional></data_reprocess_scope>

---
**RECONCILED-COMPLETE 2026-06-23** (COO /drive 132528Z): snapshot-zeroed-only exclusion rule landed; part of the $24M AUAFIX, CVO-certified 06-22. DONE.

**FALSE-CLOSURE FOUND + REOPENED 2026-07-07** (COO /prd-delta cleanup pass, source-grounded per Rule 22a/22): the 2026-06-23 "DONE" note above was WRONG -- this fix never actually landed. Live source confirms `apply_ap_gate` is still called unconditionally on the cot path today, with NO cot-specific bypass:
- `data/cot/scripts/gold/D_04.client_portal_summary.py:1265-1273` -- comment reads "AP gate (same as D_03)" / "AP active-account gate..." -- calls `apply_ap_gate(lots, ap_last_seen, data_as_of, ...)` unconditionally.
- `data/cot/scripts/gold/D_03.composition_artifacts.py:661` -- same call confirmed present (import at line 94).
- This means the AP no-activity gate (45d/180d) -- the rule Andrew directly ruled WRONG for cot -- is still excluding dormant-but-real Cottonwood accounts from served AUA TODAY. The original ~$3M understatement this TO was filed to fix has never actually been corrected; it is a live, current, active correctness gap in a served financial number.
- Root cause of the false closure: an unrelated batch "reconcile-close" COO pass on 2026-06-23 flipped multiple AUAFIX sub-TOs to DONE based on the overall $24M AUAFIX headline figure landing, without individually verifying each sub-item's own acceptance criteria. This TO's own compiler-mandate Phase 1 step (re-verify the gate is active before editing) was never actually run.
- REOPENED to `<status>pending</status>`. Dispatching to 0.4.0_DS_ClientPlatform now with the original scope/compiler-mandate (still valid, unexecuted) -- re-verify per Phase 1, then execute (a)/(b)/(c) as originally scoped, then re-verify on the SERVED artifact per Phase 3 before any closure claim. CTO + CVO notified (CVO's 06-22 cert record referenced this item; the cert record needs its own correction/scoping note).

**PART (a) LANDED+DEPLOYED 2026-07-07T18:18Z** (DS): Re-verified per Phase 1 (gate confirmed active at D_03:661 + D_04:1270, source-grounded). Andrew separately reconfirmed in-session: "any 'dormant' rules need to go immediately." Executed (a) cot-wide -- commit fa7792b70, deployed to s3://opal-data-cot/code/gold/, verified deployed-byte-identical (not rc=0). Rule 13 cot-scoped (49F/bd untouched). BONUS FINDING: swept the whole cot gold tree (not just the D_03/D_04 originally cited) and found a THIRD dormant-gate instance -- an inline reimplementation in C_06.client_mix_timeseries.py (feeding mix_daily_summary.json + client AUA timeseries) that the original reopen note missed. Fixed + dead apply_ap_gate/build_ap_last_seen/load_insurance_config defs removed from cot lib/exclusions.py (0 callers post-sweep) so it can't silently re-wire.
SERVED-VERIFY PENDING: next natural cot gold chain run, 02:00 UTC nightly (no ad-hoc run per CLAUDE.md). Corrected AUA ~$365.7M expected vs ~$362.6M currently served. NOT claiming (a) fully closed until served-verified + co-verified with L1/L2 at L5.
(b)/(c) IN PROGRESS: DS found a real new risk in (c) before touching cube-build logic -- a naive <$100 dust-floor flip could let a stale-cube ghost account (e.g. z0812933851: $0.04 silver / $2.26M stale cube) leak past bd_diminished's alloc>=$100 check, causing a NEW ~$2.26M overstatement. (c) needs a reconciliation-aware fix, not a 1-liner; grounding against live silver/allocations before proposing one. (c) still carries the Andrew-veto dust-floor flag either way.

**(b)/(c) HARD-BLOCKED 2026-07-09T19:35Z (DS) -- the grounding source is CORRUPT, not merely stale.**
(b) automates "snapshot-zeroed" as the exclusion predicate and (c)'s reconciliation-aware fix grounds
against live `silver/allocations`. Both are UNSAFE to author right now: **`silver/allocations` has been
0 rows since 2026-06-22.** Data-confirmed, not inferred:
- `s3://opal-data-cot/silver/allocations/2026-07-09.parquet` -> **0 rows**, 59 cols (the constant
  32,535 B is bare parquet schema).
- Bronze source: `forwardfill_v2/allocations/ALLOCATIONS_DAILY_*.xlsx` = real 275-292 KB through
  06-21, then constant ~4,303 B for 06-22..07-09 (18 days). Row-counted (openpyxl): 06-15 = 1,278
  data rows; 07-08 = **0** data rows. `unrealized` likewise (~3,742 B). PERIOD tables (realized,
  transactions) unaffected -- the exact SNAPSHOT-vs-PERIOD split `SNAPSHOT_TABLES` predicts.
- Mechanism (source-confirmed): `a7a4d974c` (2026-06-22, DS) set the snapshot tables
  `CurrentDay -> ("Custom",14)`. Under Custom, `_window_for` ends at `_as_of_for(table, run_date)`,
  which with `BD_SNAPSHOT_ASOF_LAG_BDAYS` defaulted to 0 (cot never opts in) is `run_date` verbatim.
  `run_date = args.date or _today_utc()` (cot_bronze_ingest.py:890/:264, wall-clock UTC) and the runner
  fires 02:00Z = 22:00 ET the PRIOR day -> BD is asked for a point-in-time snapshot on a date that has
  not begun in ET -> a well-formed header-only workbook. The prior `CurrentDay` masked this by ignoring
  the dates. The 06-22 AUAFIX-DATEMODE-A traded a mis-stamp freeze for a zero-row freeze.

**Why this BLOCKS (b) specifically, and why proceeding would be a severe error:** an automated
snapshot-zeroed predicate reads "account absent from / $0 in the snapshot" as "money gone -> EXCLUDE."
Against a 0-row allocations table, EVERY account is snapshot-zeroed -> the predicate would exclude the
entire book, and it would do so *silently and plausibly*. Authoring or tuning it against this data would
bake the freeze into the exclusion rule. Held until the forward path is unfrozen.

**Design requirement this incident adds to (b) (carry into the implementation):** the snapshot-zeroed
predicate MUST **fail-closed / ABSTAIN** when its snapshot source is empty or absent -- if the snapshot
table has 0 rows, the predicate must refuse to classify and ALARM, never mark the book zeroed. An
exclusion rule whose input can silently vanish needs a source-liveness precondition, exactly as
`_export_has_data_rows` gives the bronze layer. This is the durable form of AC6(b).

Escalated 2026-07-09T19:27-19:28Z to 0.6.0_AE_PartnerETL (owns `BD_SNAPSHOT_ASOF_LAG_BDAYS` + the
runner), 1.0.0_SA_CTO (gate call on setting it =1 for cot, before the 02:00Z run), 2.0.0_SA_COO.
Runner env is infra, not the DS lane (Rule 13) -- DS did not touch it.

**Phase-3 served-verify for (a): RAN, INCONCLUSIVE -- not claiming (a) closed.**
Served `platinum/firm/dashboard.json` + `header_metrics.json` (generated 2026-07-09T02:04Z,
data_as_of 2026-07-07): `total_aua = $434,451,347.11`. The TO's expected ~$365.7M was derived from
06-18-era data and is NOT a valid comparator against a 07-07 as-of, so AC "corrected AUA ~$365.7M+ on
the SERVED artifact" cannot be evaluated as written -- the expected value needs recomputing on current
data before (a) can be certified. Two observations recorded, neither asserted as defects:
- `fee_earning_aua = 0.00`, `non_fee_earning_aua == total_aua` (may be legitimate for cot).
- `total.new_client_aua = 0.00` AND `total.existing_client_aua = 0.00` while `total.aua = $434.45M` --
  these do not sum to the total. Needs grounding; flagged, not claimed.
Per the TO's own rule, (a) is NOT certified off L6 alone while L1/L2 move (co-verify at L5).
