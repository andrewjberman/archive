<to_id>NFRA_LAMBDAMAP.BASELINE-INIT</to_id>
<project>NFRA_LAMBDAMAP</project>
<title>comp-lambdamap `baseline` mode: capture live CodeSha256 as artifact_sha256 for null-sha (untracked) entries -- dry-run default, CVO-gated --write -- closes the ~34-Lambda CI drift-detection coverage gap</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<consult>3.0.0_SA_CVO (comp-lambdamap write-governance owner -- gates --write per-entry, verdict ed13b714a pattern); 2.0.0_SA_COO (endorsed the follow-on)</consult>
<issued_by>self-filed 0.7.0_AE_CloudOps~A 2026-07-02, per COO "file it in your lane" + CVO endorsement (both on the tranche-1 CI drift-coverage thread)</issued_by>
<issued_date>2026-07-02</issued_date>
<status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "NFRA_LAMBDAMAP" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: active-queued (LOW-PRI, non-urgent -- the ~34 are ancillary scanners/serving; the sensitive-6 are already covered by tranche-1)</status>

<priority>
LOW-PRI / non-urgent. This is a drift-DETECTION coverage-closer, not a live break. Feeds CLAUDE.md Rule-22a Clause-C (sha-coverage). The SENSITIVE subset (trade-authorizer/trade-auth-handler/trade-identifier-cache/opal-bd-transaction-consolidator/opal-inf-value-parity/opal-globgrph-freeze-monitor) was hand-written under CVO gate 2026-07-02 (commit 97059db92); this TO covers the REMAINING ~34 reusably (compiler-thesis: build the tool, don't hand-maintain 34 entries).
</priority>

<context>
CVO estate-audit (relayed by COO 2026-07-02): 40 of 172 .functions in infra/aws/lambda/ci/lambda-source-map.json have NO artifact_sha256 -> they sit OUTSIDE CI code-drift-detection (a `comp-lambdamap sha` recorded-vs-live check has no baseline to compare). FINDING (0.7.0~A, grounded 2026-07-02): `comp-lambdamap derive` CANNOT baseline-init these -- derive reconciles ONLY the STALE-RECORD class (an EXISTING artifact_sha256 that has drifted from live); a null-sha entry is not a drift candidate (`derive --only <null-sha set>` returns "0 of 0 drift candidates"). So baseline-INIT (snapshot current live CodeSha256 as the reference) is a DISTINCT operation the tool lacks.
</context>

<scope>
BUILD a `comp-lambdamap baseline` subcommand (org/modules/graph/lambdamap_cli.py; .tools/comp-lambdamap dispatch):
1. For each .functions entry with artifact_sha256 == null (optionally scoped by --only NAMES), pull the LIVE CodeSha256 (aws lambda get-function-configuration) and propose it as the baseline.
2. DRY-RUN by default (print the proposed {name -> live CodeSha256} table; NO write). Mirror derive's UX.
3. --write is CVO-GATED (same governance as derive --write, verdict ed13b714a). On --write, add artifact_sha256 = live CodeSha256 AND artifact_sha256_provenance = "baseline-init: live-CodeSha256 snapshot <date>, no deploy provenance, drift-detection reference only" (the honest-disclosure limb -- baseline-init enshrines CURRENT-DEPLOYED as reference; it is NOT a source-parity cert, esp for EXTERNAL/no-repo Lambdas).
4. Preserve source-map formatting (surgical/additive JSON -- the tranche-1 write proved round-trip json.dump(indent=2) fidelity; reuse that, or targeted insertion).
5. Guard: refuse to overwrite an existing (non-null) artifact_sha256 (that's derive's job, not baseline's).
Target set = the ~34 remaining untracked (the 40 minus the sensitive-6 already done): mostly seeking-alpha/news/find-insure-serving/security+cost scanners/orchestrators/market-update. Enumerate live at build time (jq '.functions|to_entries[]|select(.value.artifact_sha256==null)').
</scope>

<acceptance_criteria>
1. `comp-lambdamap baseline [--only NAMES]` dry-run lists every null-sha entry with its live CodeSha256; no mutation.
2. `--write` CVO-gated; on gate, writes artifact_sha256 + provenance note, surgical additive diff, JSON re-validated.
3. Refuses to touch entries that already carry an artifact_sha256.
4. A regression/unit test (org/modules/graph/tests/test_lambdamap.py extension) covers baseline-init: null-sha -> proposed live sha; non-null -> skipped.
5. The ~34 untracked reduced to 0 (or the residual EXTERNAL-unresolvable set explicitly logged, no silent cap).
6. RAVC COO + CVO on land (CVO re-confirms the batch).
</acceptance_criteria>

<references>
  <ref type="commit">97059db92 (tranche-1 sensitive-6 hand-written baseline, CVO GATE=GREEN)</ref>
  <ref type="code">org/modules/graph/lambdamap_cli.py ; .tools/comp-lambdamap ; infra/aws/lambda/ci/lambda-source-map.json</ref>
  <ref type="gate">CVO derive --write governance, verdict ed13b714a</ref>
  <ref type="rule">CLAUDE.md Rule-22a Clause-C (sha-coverage)</ref>
</references>

<lane_note>
AE (comp-lambdamap owner). LOW-PRI queued behind live work. The sensitive subset is ALREADY covered -- this is the systematic closer for the ancillary tail. CVO gates --write; do NOT land the mutation without the per-entry gate.
</lane_note>
