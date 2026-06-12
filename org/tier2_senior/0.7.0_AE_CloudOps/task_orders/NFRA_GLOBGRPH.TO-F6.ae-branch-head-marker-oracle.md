<to_id>NFRA_GLOBGRPH.TO-F6</to_id>
<project>NFRA_GLOBGRPH</project>
<title>TO-F6 — Branch-head marker oracle: writer-stamp + reader-key + PROVISIONAL interim label (AC10b P0 fix)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (CTO decomposition handoff 154026Z, PRD v0.4.3 F6, ws-charter cycle 0009)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>active</status>
<priority>P0-follow — AC10(b) re-cert required; PROVISIONAL label is same-day; writer+reader parts follow in-session</priority>

<references>
  <ref type="prd">docs/architecture/NFRA_GLOBGRPH_PRD.md §2b F6 (v0.4.3, 957513885)</ref>
  <ref type="cvo-verdict">dc06744c6 — stress-test P0: AC10(b) FAILED (mtime-scan is not HEAD; 2b Lambda commit undetectable from dev box)</ref>
  <ref type="cto-ruling">154026Z — F6 branch-head marker as the HEAD oracle; 3-part decomposition below</ref>
  <ref type="interim">Default-flip STANDS (do not roll back); PROVISIONAL label required until F6 lands</ref>
</references>

<scope>
Three parts in strict priority order. Parts 1 → 2 → 3; do NOT start part 3 before part 2 is committed.

---

**PART 1 — INTERIM LABEL (micro-patch; lands FIRST, same-day):**

In `_provenance.py` (or wherever the commit-distance line is emitted in comp-kuzu's provenance header), change the existing commit-distance output line from bare BEHIND/current to include the label:

  `HEAD-ORACLE PROVISIONAL (mtime-scan; may under-detect incremental advances)`

Until the marker (Part 2+3) lands, every comp-kuzu invocation must surface this label on the commit-distance line so the known failure mode is never silent. The label disappears when Part 3 retires the mtime-scan.

Acceptance: `comp-kuzu` (no-arg) provenance header shows the PROVISIONAL label on the commit-distance line.

---

**PART 2 — MARKER WRITER-SIDE:**

Every successful Nessie-commit writer stamps `s3://opal-globgrph-warehouse/_branch_head.main.json` (atomic S3 PUT) immediately after its Nessie commit succeeds. Three writers to update:

(a) **Item-2a derive_runner** (Fargate nightly): after `commit_to_iceberg()` returns, PUT the marker. Writers: ECS task, in-VPC.

(b) **Item-2b incremental Lambda** (`infra/aws/lambda/globgrph/incremental_updater/lambda_function.py`): after the successful Nessie overwrite/delete commit, PUT the marker. **This is a Lambda code change = full Terraform deploy cycle per Rule 1/2** (commit → terraform plan → safe-apply → verify → tag → push --follow-tags).

(c) **TO-F3 comp-aws snapshot `--commit-to-nessie` path** (`infra/aws/globgrph/comp_aws_snapshot.py` or similar): after the opt-in Nessie commit, PUT the marker.

Marker JSON schema (minimum required fields):
```json
{
  "nessie_commit_hash": "<hash>",
  "committed_at_iso": "<ISO-8601 UTC>",
  "writer_id": "<derive_runner|incremental_updater|comp_aws_snapshot>",
  "table_metadata": {
    "<table_name>": {
      "metadata_location": "<s3://...metadata.json>",
      "snapshot_id": <int>
    }
  }
}
```

**Monotonicity guard:** before PUT, GET the existing marker; only overwrite if own `committed_at_iso` is newer than the marker's. A brief race is benign (self-heals on next write; worst case is a short labeled under-detection window). If GET returns NoSuchKey, proceed unconditionally.

IAM: the 2b Lambda role (and derive_runner task role) must have `s3:PutObject` + `s3:GetObject` on `opal-globgrph-warehouse/_branch_head.main.json`. Verify with `comp-iam service incremental_updater` / `comp-iam service derive_runner` before coding; flag any gap in RAVC2.

Acceptance: after a successful 2b Lambda invocation (or derive_runner run), `aws s3 cp s3://opal-globgrph-warehouse/_branch_head.main.json /tmp/marker.json && cat /tmp/marker.json` shows the expected hash + ts + writer_id + table_metadata.

---

**PART 3 — MARKER READER-SIDE:**

(a) **`_provenance.py` commit-distance:** replace the mtime-scan oracle with the marker. Read `_branch_head.main.json`; compute commit-distance as: manifest's pinned snapshot-id vs marker's snapshot-id (or hash). If marker absent/unparseable: emit loud `HEAD-ORACLE UNKNOWN (no branch-head marker)` label (NOT the old PROVISIONAL label). The PROVISIONAL label from Part 1 is retired once this lands.

(b) **`kuzu_nessie_load.py` source-selection:** load metadata from exactly the `table_metadata[table].metadata_location` paths in the marker (not the mtime-newest scan). If marker absent: fall back to current behavior + loud `HEAD-ORACLE UNKNOWN` label.

---

**IMPORTANT CONSTRAINTS:**
- Default-flip STANDS: do not roll back `comp-kuzu` default to kuzu_nessie_db. Parts 1+2+3 fix the oracle; the default was already correct per nightly freshness.
- TO-F3 live-demo decision stays separate (network reachability path, not the same issue).
- AE holds CVO's P1s (no-egress vpc_endpoints.tf + kuzu reader lock kuzu_cli.py:55): bundle with F6 or handle separately per your judgment. COO has no opinion on bundling; just flag in RAVC2.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before any code change">
    <step>
      <run>comp-iam service incremental_updater</run>
      <expect>Confirms s3:PutObject + s3:GetObject on opal-globgrph-warehouse (or identifies the gap for iam.tf addition).</expect>
      <if_mismatch>Add the permissions to iam.tf; run comp-iam gaps after the change before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="after Part 1 committed">
    <step>
      <run>comp-kuzu (no-arg, provenance header on stderr)</run>
      <expect>PROVISIONAL label visible on the commit-distance line. Live, same-day.</expect>
      <if_mismatch>Label not emitted = Part 1 incomplete. Fix before proceeding.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after Part 2 (2b Lambda) deployed">
    <step>
      <run>comp-pipescript deployed infra/aws/lambda/globgrph/incremental_updater/lambda_function.py (or equivalent)</run>
      <expect>MATCH — deployed code is the marker-stamping version.</expect>
      <if_mismatch>STALE = deploy cycle incomplete.</if_mismatch>
    </step>
  </phase>
  <phase id="4" when="after Part 3 deployed">
    <step>
      <run>comp-kuzu (no-arg) — confirm PROVISIONAL label GONE and marker-keyed commit-distance present</run>
      <expect>No PROVISIONAL label; commit-distance keyed to marker (or HEAD-ORACLE UNKNOWN if no marker yet).</expect>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
- Part 1: comp-kuzu provenance header shows `HEAD-ORACLE PROVISIONAL (mtime-scan; may under-detect incremental advances)` on commit-distance line. Same-day.
- Part 2: marker object exists at s3://opal-globgrph-warehouse/_branch_head.main.json post-writer-invocation; JSON parses; contains nessie_commit_hash + committed_at_iso + writer_id + table_metadata.
- Part 3: PROVISIONAL label retired; commit-distance keyed to marker; HEAD-ORACLE UNKNOWN loud path fires on absent marker.
- AC10(b) re-cert (CVO queue): in-VPC 2b Lambda commit -> dev-box comp-kuzu shows BEHIND via marker -> kuzu_nessie_load refresh serves state WITH the committed row. This is the c454b6cd failure class used as the test case.
- NEW AC10(d) (CVO queue): same end-to-end marker-oracle demonstration.
- Lambda deploy (Part 2b): terraform plan 0-diff post-apply; tagged; pushed --follow-tags.
- RAVC2 to COO: commit hashes + Part 1 smoke evidence + Part 2 marker JSON + Part 3 comp-kuzu header + AC10(b)/(d) cert note (or flag if in-VPC-gated like TO-F3).
</acceptance_criteria>

<cross_domain_coordination>
- P1s from CVO verdict (no-egress vpc_endpoints.tf gap + kuzu reader lock kuzu_cli.py:55): AE's call on bundling with F6 or separate. Surface the decision in RAVC2.
- graph-call-manifest.yaml / comp-tools.yaml: if the comp-kuzu or kuzu_nessie_load surface changes (it will in Part 3), flag the patch in RAVC2 for COO author-line commit (exec-owned, same pattern as TO-F1/F2 handoffs).
- TO-F3 live-demo (in-VPC-gated): orthogonal to F6 oracle path; no coordination needed.
</cross_domain_coordination>
