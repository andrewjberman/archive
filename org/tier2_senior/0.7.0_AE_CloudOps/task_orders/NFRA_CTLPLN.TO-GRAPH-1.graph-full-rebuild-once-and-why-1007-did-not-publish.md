<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-GRAPH-1.graph-full-rebuild-once-and-why-1007-did-not-publish</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>cancelled</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/tier1_exec/1.0.0_SA_CTO/deliverables/FAST_FIX_RULINGS_20261008_162xZ.md</decomp_doc> graph item F3 (ACCEPTED by 1.0.0_SA_CTO; "needs a live 0.7.0_AE_CloudOps seat"), from the list `org/tier1_exec/4.0.0_SA_CRO/deliverables/GRAPH_COHERENCE_FAST_FIXES_20261008.md` row F3 @6418d9ab13. A fast-fix act on Andrew's ~16:0xZ order, cut by this lane on 1.0.0_SA_CTO direction msg 106983.
<owned_cells>F3</owned_cells>
</decomp_ref>

  <cancellation>
    CANCELLED 2026-10-08 ~16:4xZ by the issuer on 1.0.0_SA_CTO msg 107002: graph F3 is withdrawn in the ruling file. Its
    premise was false: 4.0.0_SA_CRO msgs 106999/107000 read the projection manifests live and the nightly full rebuild
    published every night 10-04 to 10-08; "last full 10-04" came from a marker field each incremental overwrites. STOP sent
    to 0.7.0_AE_CloudOps at 16:44:57Z. The seat confirmed at 16:45:32Z (msg 107003): NO FIRE, no cloud object changed, no
    ledger opened. Its read: rule opal-globgrph-derive-runner-nightly ENABLED cron(0 2 * * ? *) (item2a.tf:439-442) ->
    globgrph-derive-runner:9 -> projection-worker:6; full-fallback published with POINTER_PUT_OK on 10-05 02:27:24Z
    (29478 nodes), 10-06 02:26:42Z (29517), 10-07 02:28:24Z (29531); pointer at cancel = 10-08T12:54:23.609381+00:00,
    LastModified 12:55:07Z, SHA256 7d8160ec6b8fe37c3ac84c081ac8d4de55e5f42de02b5f2d709efbb8e1c19a14.
  </cancellation>

  <objective>
    Run the estate graph's nightly FULL rebuild once, ad hoc, and find out why the 2026-10-07 nightly full rebuild did not
    publish. The last full rebuild that published is 2026-10-04; the served copy has lived on incremental updates since.
    This is an ad-hoc QA run: the next scheduled nightly stays the acceptance.
  </objective>

  <context>
    The served pointer is `projection/current.json`; at the list's cut it named the 2026-10-08T12:54:23Z vintage (an
    incremental). `comp-kuzu` prints a `VINTAGE:` line on every answer. Background on the producers:
    `infra/system/02_graph_infra.md` line 16 (`comp-aws derive`, the cloud producer, nightly; `comp-kuzu-full`, the local
    projection). Code under `infra/aws/globgrph/` (`kuzu_nessie_load.py`, `kuzu_incremental_refresh.py`, `node_health.py`).
    Which producer writes the nightly FULL build and where it is scheduled is your first read; do not assume it from this text.
  </context>

  <never_widen>
    Moving `projection/current.json` moves served output. The two halves:
    - CTO: the ruling file above, item F3, accepting the F3 row as written, whose rollback is "Repoint
      `projection/current.json` to the 2026-10-08T12:54:23Z vintage, which is the current pointer" and whose blast radius
      is "A bad full build is served to every box until it is repointed. The incremental path is unaffected either way."
    - COO (this order, 2.0.0_SA_COO~C): BLAST RADIUS = the one pointer object `projection/current.json` and the new vintage
      objects the producer writes beside the existing ones; no existing vintage object is deleted or overwritten; no code,
      schedule or infrastructure change. ROLLBACK, per key: `projection/current.json` rewritten to the exact bytes you saved
      at step 3. BOTH BRANCHES: (a) the build publishes and passes step 6 -> leave it served; (b) it fails, or publishes and
      fails step 6 -> roll back the pointer the same session. A run that does not publish leaves the pointer untouched: read
      it and say so.
  </never_widen>

  <the_act>
    Load /cloud-ops. State your EXPECTED OUTCOME in your log before step 4 (the ruling requires it) and the measured
    result after.
    1. FIND the producer of the nightly full rebuild: its resource (function, task, state machine or host job), its schedule
       (rule name and cron, DESIRED in the repo vs APPLIED live), and the code it runs. Cite file:line and the live
       describe output.
    2. WHY 2026-10-07 DID NOT PUBLISH: read that night's run (logs, execution history, exit) and say which of these it was:
       did not fire / fired and failed (the error) / built and did not repoint (why) / other. Quote the evidence. If the
       2026-10-05 and 2026-10-06 nights also did not publish, say so with the same evidence.
    3. BEFORE: save the bytes of `projection/current.json` and its LastModified (UTC, `s3api`), and one `comp-kuzu` answer's
       `VINTAGE:` line.
    4. Open ONE NEVER-2 ledger entry in `org/critical_paths/change_management/` naming the producer, the saved pointer and
       the rollback.
    5. FIRE the same producer once, ad hoc, exactly as its schedule fires it (same input), with no code or config change.
       If step 2 found a defect that makes the run certain to fail again, STOP before firing and report it: a fix is a
       separate cell.
    6. AFTER: read `projection/current.json` (bytes, LastModified) and a `comp-kuzu` answer's `VINTAGE:` line; the vintage
       must be the new full build's. Run two read checks against the served graph: a node count per main type against the
       2026-10-04 full build's counts (state each; a drop over 10% in any type is a FAIL), and the corrected F2 Cypher
       example (`.tools/comp-which`, the cloud-census example landed @bed9b6d07b) returning rows. FAIL -> roll back the
       pointer (step 3's bytes), re-read it, and report.
    7. Close the ledger entry. APPLIED (one ad-hoc publish), not EXERCISED, until the next scheduled nightly publishes on
       its own: name that fire's time in your report.
  </the_act>

  <bounds>
    - One ad-hoc fire of the existing producer. No edit to any code, Terraform, schedule or IAM. `safe-apply` is not needed
      because nothing is applied; if any step would need an apply, STOP and report.
    - No delete of any vintage object. No push of a shared branch. No Dell credential.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
    org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
  </paths>

<preflight>
comp-schedule: RUN by the applier at step 1 (the nightly's rule DESIRED vs APPLIED); the scheduled fire stays the acceptance.
comp-iam: DECLARED-NOT-APPLICABLE no identity change; the applier's own credentials fire an existing producer.
comp-adversary: RUN -- a bad full build served to every box (step 6 count and query checks, pointer rollback by saved bytes); an ad-hoc fire masking a broken schedule (step 2 reads the scheduled nights first, step 7 names the next scheduled fire as acceptance); firing a run certain to fail (step 5 STOP); BLIND: whether the Dells can read the result (graph F1, cell 2 of CT-a-1, not yet applied).
lane: the <paths> block names the ledger, the sentinel, the seat's own deliverables and logs, and the project's surprise channel.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="F3"><invocation>comp-kuzu "MATCH (n) RETURN count(n)"</invocation><expect>VINTAGE:</expect></criterion>
</proof_of_spec>
  AC1's VINTAGE line must name the new full build's time (or, on rollback, 2026-10-08 12:54:23 UTC); state which in the proof row.
  Base read by the issuer at the cut (laptop, ~16:4xZ): `VINTAGE: Built from the estate as of 2026-10-08 12:54:23 UTC ...
  prefix=projection/2026-10-08T12:54:23.609381+00:00/`, count 29586.

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the producer and its schedule
    (DESIRED vs APPLIED); the 2026-10-07 cause with evidence; the expected outcome you stated; the before and after
    pointer (bytes digest, LastModified UTC) and VINTAGE lines; the per-type counts against 2026-10-04; the F2 query's row
    count; published-and-kept or rolled-back, with the time in UTC in the subject line; the next scheduled fire's time; the
    ledger entry's path and close; surprise rows filed; commit hashes and the measured push state.
  </report>
</task_order>
