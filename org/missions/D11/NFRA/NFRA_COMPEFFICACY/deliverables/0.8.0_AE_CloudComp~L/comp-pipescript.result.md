# comp-pipescript — T-10 per-tool result

T-10 / CE-t-10, measured by `0.8.0_AE_CloudComp~L`. Engine commit:
`44bc9852cc9d63549639668fd5c286f24f6c98e0` (LOCAL at this report; never pushed by this seat).

```json
{
  "schema": "NFRA_COMPEFFICACY_PRD v0.5 s.4",
  "identity.tool": "comp-pipescript",
  "identity.shim": ".tools/comp-pipescript",
  "identity.engine": "org/modules/graph/pipeline_cli.py",
  "identity.shim_quote": "comp-pipescript SHIM: .tools/comp-pipescript -> org/modules/graph/pipeline_cli.py",
  "identity.engine_vintage": "44bc9852cc9d",
  "identity.aliases": "ABSENT",
  "identity.purpose": "authoritative pipeline dependency and deployed-script verification tool",
  "identity.registration": "PRESENT: parser program comp-pipescript",
  "disclosure.default_run": "comp-pipescript deployed",
  "disclosure.subject": "pipeline tree and optional script filter",
  "disclosure.backend": "local script trees plus per-tree S3 buckets",
  "disclosure.vintage": "working-tree source plus live S3 head/list reads",
  "disclosure.denominator": "MATCH/STALE/MISSING and per-prefix S3 denominator rows",
  "disclosure.resolved_unresolved": "UNCOVERED, AWS_UNREACHABLE, ETAG_NOT_COMPARABLE and DECLARED-UNSWEPT are explicit",
  "disclosure.pagination": "ABSENT — S3 prefix output is fully read per bounded remote call",
  "answer.subject_absent": "SUBJECT_ABSENT_FROM_CORPUS: named filter matches no script in the selected tree",
  "answer.present_zero": "PRESENT_WITH_ZERO_RESULTS: named script is in the deployment corpus and has zero non-MATCH results",
  "answer.partial": "PARTIAL_OR_BLIND: BUDGET REACHED prints NOT-DECIDABLE and rc=4 for deployed",
  "answer.not_applicable": "NOT_APPLICABLE: sovereign-held BD deploy mode has no permitted population",
  "answer.skipped": "SKIPPED is a distinct F9 gate verdict and is never folded into PRESENT_WITH_ZERO_RESULTS",
  "rule_t.carrier": "--budget > COMP_BUDGET_S > 90 s default; --budget 0 unbounded",
  "rule_t.population": "six timeout sites: deployed head-object/listing/enumeration (four) and skipgate listing/provenance (two)",
  "rule_t.complete": "WITHIN BUDGET plus always-printed DEFERRED: 0 bucket",
  "rule_t.partial": "BUDGET REACHED plus PARTIAL_OR_BLIND and a DEFERRED bucket; deployed returns rc=4",
  "rule_t.cursor": "an indivisible remote operation leaves supplied --cursor unchanged; a larger-budget re-run is directed",
  "verdict_row": "deployed is verdict-bearing: rc=4 NOT-DECIDABLE is distinct from clean completion",
  "registry": "_FIRM_TO_PIPELINE enumerates bd, inf, cot, mdpf, advi; CLI firm choices are bd, inf, cot, mdpf",
  "etfs_finding": "ETFS is absent from the deployed firm registry and was not added; owner is the registry/coverage authority, not this audit",
  "passcraft": "archetype: deployed verification gate; bounded remote-operation and false-clean controls applied",
  "usage": "issuance measurement: 571 runs; F9 is a watched 15-file suite",
  "battery": ".tools/tests/test_comp_pipescript_battery.py: 6/6 direct and pytest; executable rc=0-at-expiry mutant fired",
  "overlap": "safe-deploy.sh consumes deployed; complete-run TOOL-03 MATCH semantics were not changed",
  "disposition_proposal": "CLEARED-candidate, pending CVO grading; T-10 completion evidence is local-only under the no-push rule"
}
```

## Evidence

- Tiny-budget deployed run: `--pipeline inf-gold --budget 0.001` returned `rc=4`, printed `BUDGET REACHED`, `STATE: NOT-DECIDABLE`, `ANSWER-STATE: PARTIAL_OR_BLIND`, and a deferred `s3_head_object` bucket.
- Complete state controls are planted in the new battery: absent and present-zero use a hermetic S3 response; held BD is the not-applicable control.
- COO distinct-seat FWD-9, Msg-ID 93771, ran `comp-pipescript deployed` at commit `44bc9852cc`; it returned `rc=4` at the default 90-second budget with the same NOT-DECIDABLE/PARTIAL_OR_BLIND/deferred evidence. This is a safe non-clean result, not a clean deployment verdict.
- F9 commit hook: `141 passed in 93.10s`; scoped direct and pytest battery: `6 passed` each.
- Push measurement at report: `origin/CLOUD=351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee`; `git merge-base --is-ancestor 44bc9852cc origin/CLOUD` rc=1. State: **LOCAL**. This seat did not run `git push`.
