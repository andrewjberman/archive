<to_id>NFRA_GLOBGRPH.TO-Q1</to_id>
<project>NFRA_GLOBGRPH</project>
<title>comp-queue: in-flight (uncommitted) event visibility in the comp-kuzu provenance header</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<issued_by>2.0.0_SA_COO (Andrew-direct authorized, AE proposal 170220Z 2026-06-12)</issued_by>
<issued_date>2026-06-12</issued_date>
<status>closed-superseded -- per COO ruling 20260618T154005Z. NFRA_GLOBGRPH genuinely CLOSED 2026-06-16 (Completed table, completed-date set, forward-work re-homed to BACKLOG). TO-Q1 was a deferred P3 visibility enhancement (in-flight/uncommitted event surfacing in the comp-kuzu provenance header) NOT a correctness fix (read-your-own-writes goes live per F5) and was not captured in the close re-home; COO adding it to BACKLOG.md. Not shipped, not a zombie -- a deferred enhancement re-homed to backlog. Status flipped this cycle (TO-recon, COO-ruled).</status>
<priority>P3 — visibility enhancement, NOT a correctness fix (read-your-own-writes still goes live per F5). Cheap, closes the last "header could quietly mislead" seam.</priority>

<background>
TO-F6's marker tracks COMMITTED Nessie HEAD only. During the SQS MaximumBatchingWindowInSeconds=120 debounce + Lambda processing (~2-3 min worst case), N CloudTrail events sit UNCOMMITTED in opal-globgrph-incremental-events. A mid-batch comp-kuzu query honestly reads "Nessie HEAD: current" (current vs committed) but is silently blind to the in-flight delta. The marker made COMMITTED staleness visible; this makes IN-FLIGHT staleness visible -- same philosophy, one layer earlier. Andrew framing: the pending delta is tiny (a few ARNs) -> surfacing it is network-time, not read-latency; "that header could quietly mislead" is the seam to close.
</background>

<scope>
MVP (ship first, cheap): comp-kuzu provenance header gains a PENDING line via a single NON-DESTRUCTIVE SQS get-queue-attributes(ApproximateNumberOfMessages) on opal-globgrph-incremental-events:
  "PENDING: ~N event(s) in flight (<=2min debounce, not yet committed)"  (omit line / "PENDING: 0" when empty)
  Implement in _provenance.format_provenance_header (nessie source only) or a kuzu_cli pre-query call. Best-effort (SQS unreachable/no-perms -> silent skip, never break the query). NOTE: ApproximateNumberOfMessages is eventually-consistent (~seconds lag) -- label it "approx".

v2 (gated on whether CONTENT is worth it -- SQS is NOT peekable without consuming): a lightweight pending-INDEX. Add a 2nd EventBridge target on the cloudtrail-mgmt rule -> DynamoDB table (PK=arn, TTL ~10min) OR S3 pending/ prefix; the 2b Lambda DELETEs the index rows it just committed (in the same handler, post-commit, best-effort). comp-queue / the header reads the index -> shows the actual pending ARNs. = Terraform (item2b.tf: rule target + DDB table + IAM) + Lambda code (clear-on-commit) = full deploy cycle.

v3 (optional, defer): overlay -- annotate "pending change" on affected nodes in the kuzu result. Heavier; only if v2 proves the content is used.

SCOPE BOUNDARY: visibility only. Does NOT change the graph's role or the F5 read-your-own-writes doctrine (that still goes to live AWS). Does NOT touch the write path / marker / CAS.
</scope>

<iam>
MVP: the comp-kuzu invoker (dev box / agent role) needs sqs:GetQueueAttributes on the queue -- check; likely already broad. v2: Lambda needs dynamodb:DeleteItem/Query (or s3:Delete) on the index + EventBridge target IAM.
</iam>

<acceptance_criteria>
- MVP: with K messages queued (inject K via a throwaway event burst or read live during organic activity), comp-kuzu header shows "PENDING: ~K"; empty queue -> no PENDING line or "PENDING: 0". Best-effort proven (kill SQS perms -> header still renders, line silently absent).
- v2 (if built): index populated on event arrival, CLEARED on the 2b commit that consumes those ARNs; comp-queue lists the live pending ARNs; index self-empties within the TTL after a quiet period.
- graph-call-manifest.yaml / comp-tools.yaml: PENDING-line surface note -> COO author-line patch (exec-owned), same as F-series.
- No write-path/marker/CAS change; F5 doctrine unchanged.
- RAVC2 to COO on MVP completion; flag if v2 seems worth building.
</acceptance_criteria>
