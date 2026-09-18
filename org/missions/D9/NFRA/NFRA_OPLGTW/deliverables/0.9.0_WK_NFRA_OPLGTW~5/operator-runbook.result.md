# NFRA_OPLGTW.TO-OG-o-2 -- the operator runbook and its status summary -- result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~5` | **Cut base:** CLOUD @3207f5ea09 (`OG-z-2` and `OG-x-1` merged) | **Cell:** OG-o-2
| **Commit:** `90999aaee5`

## What this cell built

- `infra/aws/ec2/opal-gateway/runbooks/SCHWAB_PILOT_RUNBOOK.md` (new) -- the ten-section operator runbook:
  named readers/moments (PRD's own paragraph, verbatim), onboarding, connector add/reuse, member
  connection, troubleshooting (three classes: authentication failure, terminal entitlement denial, data
  unavailability -- mapped to the contract's closed `error_codes`), audit read / status summary, grant
  change, revocation, rollback (PRD C6, two paths: disable the flag, or restore an older binary with its
  guardrails), and the chat-environment/retention/no-recall disclosure.
- `infra/aws/ec2/opal-gateway/ops/schwab_status.py` (new) -- the read-only status command: `health_report`
  (integration flag, access-state reachability via a synthetic `catalog_snapshot` probe key expected
  ABSENT, reader/catalog role assumability), `closure_report` (the SAME `Catalog.availability()` judgment
  the query/download path uses, for every master/dataset in the contract), `error_report` (counts only,
  from the acknowledged Schwab audit sink, by `event_type`/`classification`/`error_code`/`master`), and
  `build_report`/`format_report`/`main` wiring them into one CLI. No customer value is ever printed: every
  field is a master/dataset/date label or a closed-enum value already in `schwab_audit.RECORD_FIELDS`.
- `infra/aws/ec2/opal-gateway/tests/acceptance/WALKTHROUGH_PROTOCOL.md` -- the R-OG-12 amendment: section 4
  fixes RQ1-RQ6's dates to the sealed business date `2026-09-15` (the word "latest" removed from the
  section entirely, since `OG-v-3` sealed against 2026-09-15 and a newer qualified closure -- 2026-09-16 --
  already exists by hand-off); A7 gains step 4, the two masters' no-date "latest qualified date and
  available dates" ask, with its expected observation and evidence-to-record text.
- `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/probes/og_o2.py` (new) -- one
  function per OGO2-AC1..AC11: text-shape checks against the runbook/protocol sections, a
  `git cat-file -e HEAD:<path>` existence check for every `.py`/`.sh` path the runbook names (AC2), and a
  moto-fixture live run of `schwab_status.py`'s `build_report`/`format_report` scanned for its three
  section markers and the absence of an `@` character or the fixture's shared account id `99000001` (AC9).

## Amendment carried (R-OG-12)

Per the task order's own note: the protocol edit was ruled onto THIS cell rather than `TO-OG-v-4` because
the walkthrough is performed from the protocol before `OG-v-4` is spawned. AC10 and AC11 grade it here;
`OG-v-4` grades its own re-worded AC5 and new AC6-AC7 when it lands.

## Probe runs (all 11 mechanical criteria)

Every `og_o2.py AC<n>` invocation was run once against the committed worktree (commit `90999aaee5`) and
printed `VERDICT: PASS-OGO2-AC<n>` with its own denominator line -- see the proof-of-spec instance's
`acceptance` array for each invocation and its verbatim output. `OGO2-J1` is a judgment row: it carries no
verdict here (`status: UNVERIFIABLE-BY-INSTRUMENT`, `status_reason` naming `3.0.0_SA_CVO` at L9), per the
task order's `<proof_of_spec>` instruction that a PASS/FAIL on a judgment row is invalid.

## What this cell did not do (BOUNDS)

No rollback, grant change, connector act or deploy was run to write or verify this runbook -- its commands
are cited and checked for existence at HEAD, never exercised here. `ops/schwab_status.py` was run only
against a moto-emulated S3/DynamoDB world seeded from `tests/acceptance`'s own fixtures (AC9); no live AWS
call was made. The known red test (`tests/test_identity_scope.py::test_scoped_deny_by_default`, row
`NFRA_OPLGTW-S1`) and `identity_tool_allowlist.txt` were not touched.

## Surprises

None filed. The task order's premises held: the worktree carried `org/` and `.tools/`; every referenced
module (`app/schwab_audit.py`, `app/download_routes.py`, `ops/schwab_entitlement_admin.py`,
`app/integrations/schwab/catalog.py`, `app/integrations/schwab/aws_roles.py`,
`infra/aws/ec2/safe-ec2-deploy.sh`, `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh`) existed at HEAD as the
order described; the R-OG-12 amendment's own text was clear about which two places to edit in
`WALKTHROUGH_PROTOCOL.md`.
