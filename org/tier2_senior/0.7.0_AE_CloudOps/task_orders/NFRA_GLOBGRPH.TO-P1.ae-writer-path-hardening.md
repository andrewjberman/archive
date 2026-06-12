<to_id>NFRA_GLOBGRPH.TO-P1</to_id>
<project>NFRA_GLOBGRPH</project>
<title>TO-P1 — Writer-path hardening: fast-forward-only CAS + orphan self-detection</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO ruling 984773e0e, 160643Z 2026-06-12)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>complete</status>
<priority>P1 — silent intraday data loss (bounded by nightly heal), bounded-scope fix, no architectural changes</priority>

<references>
  <ref type="cto-ruling">984773e0e — writer-path hardening spec: fast-forward-only CAS + orphan self-detection</ref>
  <ref type="root-cause-commit">c454b6cd — parent=None ORPHAN produced by 2b pyiceberg-overwrite path; committed OFF-BRANCH; increment LOST (never reached main)</ref>
  <ref type="context">TO-F6 fixed the READER (marker follows Nessie's ref HEAD). This TO fixes the WRITE PATH serialization contract. Both required for complete integrity.</ref>
  <ref type="prd">docs/architecture/NFRA_GLOBGRPH_PRD.md §2b (v0.4.1+) — CTO will fold overwrite-path correction into §2b at next PRD touch</ref>
</references>

<background>
The CVO stress-test root cause (c454b6cd) revealed that the 2b pyiceberg-overwrite path can commit OFF-BRANCH, producing a parent=None ORPHAN commit. The increment is LOST — it never reached Nessie's main branch HEAD. The marker oracle (TO-F6) fixed readers: readers now key off the Nessie REST branch HEAD post-marker-stamp. But the write path itself still lacks a serialization contract — under concurrent 2b+F3 commits, a race can produce silent data loss bounded by the nightly full-overwrite heal. P1 not P0 because nightly heals the served graph daily.

v0.4.1 claimed "Nessie serializes" — that held only for writers using Nessie's native commit protocol. The pyiceberg-overwrite path bypasses it. This TO closes the gap.
</background>

<scope>
Two parts, can be implemented in one commit:

---

**PART A — Fast-forward-only CAS commits:**

For every writer that uses pyiceberg-overwrite-under-Nessie-REST (at minimum: `incremental_updater/lambda_function.py` 2b path; also `comp_aws_snapshot.py` TO-F3 path if it uses the same overwrite mechanism — check):

1. Before writing: GET the current Nessie branch HEAD commit hash (`GET /api/v1/trees/{branch}` → `hash`). This is the expected-parent.
2. Write the iceberg table (pyiceberg overwrite).
3. After write, resolve the Nessie commit the write produced. Verify: the produced commit's parent hash == expected-parent from step 1.
4. If parent mismatch (off-branch / orphan): **LOUD FAILURE** — raise `NessieWriteConflict` (or equivalent), do NOT stamp the marker, and do NOT silently swallow the error. Let the Lambda invocation fail loudly (CloudWatch alarm-visible).
5. If parent match: proceed to marker stamp as normal.
6. On conflict: bounded retry (max 3 attempts, exponential backoff 1s/2s/4s, re-GET HEAD each retry). After max retries: loud failure, do not silently drop the increment.

The goal is: if two writers race and one commits off-branch, the loser detects it LOUD rather than silently losing its increment.

---

**PART B — Writer orphan self-detection:**

Immediately after every Nessie commit (before the marker stamp), verify that the landed commit is reachable from Nessie's current branch HEAD:

```
GET /api/v1/trees/{branch} → branch_head_hash
GET /api/v1/trees/{branch}/log?maxRecords=5 → recent commit hashes
```

If the committed hash is NOT in the recent log (or if `parent == null` in commit metadata): this is an ORPHAN.

Action on orphan detection:
- Log `ERROR: Nessie commit {hash} is an ORPHAN (parent=None or not reachable from branch HEAD). Skipping marker stamp.`
- Do NOT stamp the marker (a stale marker is better than a marker pointing at orphaned state).
- Raise an exception so the Lambda invocation fails loudly (NOT a soft warning).

Implementation note: the Nessie REST log endpoint returns recent commits in order. A committed hash missing from the top-5 with a non-null parent is a strong orphan signal. Tune the window if needed, but prefer loud false-positives over silent data loss.

---

**SCOPE BOUNDARY:** Do not redesign the pyiceberg-overwrite mechanism itself (separate architectural work). The goal is detection + loud failure + retry, not rewriting the iceberg write protocol. Three similar lines in 2 files; no new abstractions needed.

</scope>

<compiler_tools_mandate>
  <phase id="1" when="before any code change">
    <step>
      <run>comp-iam service incremental_updater</run>
      <expect>Verify Nessie REST GET permissions (branch HEAD + commit log) are covered. IAM already has the S3WarehouseWrite grant; the REST calls are internal VPC calls if derive_runner, Lambda if 2b. Flag any new permission gap.</expect>
    </step>
    <step>
      <run>comp-pipescript deployed infra/aws/lambda/globgrph/incremental_updater/lambda_function.py</run>
      <expect>MATCH on baseline before you start — confirm current deployed version is v0.1.11 (post-F6). STALE = deploy cycle still pending from F6.</expect>
    </step>
  </phase>
  <phase id="2" when="after both parts committed and Lambda deployed">
    <step>
      <run>comp-pipescript deployed infra/aws/lambda/globgrph/incremental_updater/lambda_function.py</run>
      <expect>MATCH — deployed code is the CAS + orphan-detection version.</expect>
      <if_mismatch>STALE = deploy cycle incomplete. Do not RAVC2 until MATCH.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
- (a) Fast-forward-only CAS: concurrent 2b + F3 commit test (fire both simultaneously or in tight sequence) — Nessie commit log shows SERIALIZED lineage (linear parent chain, no forks). No increment lost — both row-sets present in served graph post-nightly or post-comp-kuzu refresh.
- (b) Orphan self-detection: inject a synthetic orphan (simulate c454b6cd class: commit off-branch or forge parent=None) — writer detects it, logs ERROR at orphan class, skips marker stamp, raises exception (Lambda invocation non-zero rc).
- (c) Zero orphans: post concurrent-commit test, scan Nessie commit log for parent=None entries — 0 orphans produced.
- Lambda deploy: terraform plan 0-diff post-apply; tagged; pushed --follow-tags.
- RAVC2 to COO: commit hashes + concurrent-commit test log evidence + orphan-inject test log + comp-pipescript MATCH.
</acceptance_criteria>

<cross_domain_coordination>
- graph-call-manifest.yaml / comp-tools.yaml: no surface change expected (write-path internals only). No exec-author-line patch needed unless comp-kuzu surface changes.
- derive_runner (Fargate): if the overwrite path in derive_runner also uses pyiceberg-overwrite, apply the same CAS + orphan-check. AE judgment call — if derive_runner uses a different write mechanism (append-only or different Nessie commit API), confirm in RAVC2.
- TO-F6 container rebuild (urgent dispatch, same session): these are orthogonal — the container rebuild activates the marker stamp for derive_runner; this TO hardens the commit serialization. Both can proceed concurrently.
- Never-widen: this is a correctness/reliability fix, not a served-output change. No never-widen sign-off required — the fix reduces silent data loss, not adds new data.
</cross_domain_coordination>
