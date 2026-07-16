# OPLMCP Entitlements Domain Split + AWS Domain + taxsma Integration — BUILD SPEC v0.1

**Author:** 0.2.0_DT_PortfolioAnalytics (Andrew-direct, 2026-07-16 session)
**Andrew's directive (verbatim intent):** "we need to develop the entitlements layer so that theyre
broken up by domain. there are entitlements for ms (graphapi) already set up, we also need an
entitlements for AWS." Scoping from the same session: nobody has AWS access except Andrew; Alyssa
(alyssa@opalinvest.com) gets a very narrow path — a daily-ETL-produced table for all 0833 clients,
reachable from her laptop via the gateway as `/tax-pt2 {account}`.
**Grounding vintage:** gateway app read at workspace CLOUD @ 77a523510 (entitlements.py,
integrations/base.py, tier.py); 0833 data facts verified live 2026-07-16 (see
`.claude/skills/tax-pt2/SKILL.md` constants).
**Gates:** entitlements core + IAM legs are CTO-arch-gate material (SCTY_PREMCP precedent);
gateway build rides the OPLMCP lane (0.5.0~A); gold-table leg is monolith/DS territory
(pure-addition, new-territory rule compliant).

---

## Current state (source-confirmed)

- `app/entitlements.py` — SCTY_PREMCP P1 write-scope gate: per-TIER grants of Graph WRITE classes
  (`write_comms`/`write_files`/`write_delete` from `destructive_ops.WRITE_CLASSES`), hot-reloaded
  from `ENTITLEMENTS_PATH` (`entitlements.txt`, line = `<tier> <write_class>`), fail-closed,
  master wildcard for reversible classes only. **Implicitly single-domain: MS/Graph.**
- `app/integrations/base.py` — integration framework: `AuthKind.NONE` ("read-only in-estate
  source") exists and is the intended model for S3-backed tools; per-call identity
  (`get_current_email`) + audit + `min_tier` gate; fail-closed `ENABLED_INTEGRATIONS`.
- **No per-email dimension anywhere; no AWS-aware entitlement anywhere; no git entitlements
  (none needed — the gateway brokers no git).**

## Target design

### Leg 1 — domain-partitioned entitlements (app/entitlements.py + entitlements.txt)

**File format (hot-reload, backwards compatible):**
```
# legacy line (unchanged semantics, implicit domain=ms):
#   <tier> <write_class>
standard write_files

# domain-scoped line:
#   <principal> <domain>:<class>
#   principal = tier:<tier> | user:<email-lowercase>
tier:standard    ms:write_files          # identical meaning to the legacy line
user:alyssa@opalinvest.com  aws:read_taxsma
```
Parse rule: a first token containing `:` -> new form; bare token -> legacy (domain=ms, principal
tier). Unknown domain, unknown class, malformed line -> line ignored (grants never widen on a
parse failure); unreadable file -> seed stands (the existing rule, kept verbatim).

**Domain class registries:**
- `ms` -> existing `destructive_ops.WRITE_CLASSES` (untouched).
- `aws` -> NEW `app/aws_classes.py`: `AWS_CLASSES: dict[str, dict]`, each class =
  `{description, kind: "s3_read", s3_bucket, s3_prefixes: [...], master_wildcard: bool}`.
  Seed class: `read_taxsma` = `{s3_bucket: "opal-data-assets",
  s3_prefixes: ["schwab/08335338/gold/dim_taxsma_costbasis/"], master_wildcard: True}`.
  The registry is DOCUMENTATION + app-layer bound for the tool; the ENFORCED AWS boundary is IAM
  (leg 3). An AWS class is read-only by construction in v1 (`kind: s3_read` only — a future
  mutating AWS class must land with master_wildcard=False and its own CTO gate).

**API:** keep `is_entitled(tier, wclass)` verbatim for the MS callers (tools.py `_run` untouched).
Add `is_entitled_domain(domain, cls, tier, email) -> bool`:
1. class must exist in the domain registry (else deny);
2. grant if `user:<email>` line matches, OR tier line matches, OR
   (tier is MASTER_ADMIN and class.master_wildcard) — Andrew's implicit coverage lands here;
3. READ_ONLY tier: aws reads MAY be granted by explicit user/tier line (unlike ms writes) —
   an aws:s3_read class is non-mutating; the ms READ_ONLY hard-deny stays ms-only.

### Leg 2 — the `taxsma` integration (app/integrations/taxsma/)

- `IntegrationSpec(id="taxsma", auth_kind=AuthKind.NONE, tool_prefix="taxsma_", read_only=True,
  min_tier="standard", hosts=())` + NEW spec field `entitlement: "aws:read_taxsma"` (optional,
  fail-closed when set) enforced in the shared dispatch beside min_tier — this field is the
  reusable per-email mechanism for every future narrow grant.
- One tool v1: `taxsma_costbasis(account: str, asof: str = "")` ->
  reads `s3://opal-data-assets/schwab/08335338/gold/dim_taxsma_costbasis/date={asof|latest}/`
  via the INSTANCE ROLE (boto3), filters to `account` (zero-padded), returns the account's
  cost-basis/fees/performance rows + meta (vintage, row count, sha256). Refuses an account whose
  roster row is not `Opal Tax SMA*` UNLESS caller is master (the Alyssa-scope question Andrew
  left open defaults CLOSED; his own access unrestricted).
- Enable via `ENABLED_INTEGRATIONS` + deploy per the YCharts template; Andrew /mcp reconnect after.

### Leg 3 — IAM (Terraform, gateway EC2 role)

- Policy addition (pure add): `s3:GetObject` on
  `arn:aws:s3:::opal-data-assets/schwab/08335338/gold/dim_taxsma_costbasis/*` +
  `s3:ListBucket` on `arn:aws:s3:::opal-data-assets` with prefix condition
  `schwab/08335338/gold/dim_taxsma_costbasis/`.
- **Rule 22a battery before first live call:** `simulate-principal-policy` ONE `--resource-arns`
  per invocation; positive control as a SEPARATE invocation; `--context-entries` for the
  ListBucket prefix condition (a conditioned statement with no context returns implicitDeny
  byte-identical to a real deny). Also the NEGATIVE control: simulate a key OUTSIDE the prefix
  (e.g. `.../silver/fact_uln/...`) and require implicitDeny — the grant must not leak monolith-wide.
- safe-apply; deploy-completion ledger entry; tag.

### Leg 4 — the gold table `dim_taxsma_costbasis` (monolith/DS lane)

- Daily, ALL 0833 accounts (Andrew: growth-proof), produced POST-silver in the existing 0833
  conversion chain (bd49f dims runner precedent). GOLD not silver — it is a parse-down projection
  (naming law: silver `fact_*` complete / gold `dim_*` projections / gold is the ONE parse-down point).
- Columns (from the tax-pt2 methodology pins): account_id, asof, lot-level costbasis fields
  (the Schwab lot-level-export shape from fact_ult), posted-fee ledger aggregates (margin
  interest / borrow / advisor-fee MTD+QTD from fact_trn), realized ST/LT + unrealized ST/LT,
  daily MV, schedule fields joined from the BD fees pull (Account Fee Schedule, bp), schema_version.
- Zero-rows-for-a-live-Tax-SMA-account = producer FAIL (the ULT trap gate, moved upstream).

## Acceptance

1. Unit: legacy `standard write_files` parses identically pre/post; unknown domain line inert;
   `user:` line grants exactly that email; master wildcard covers aws:read_taxsma; unreadable
   file -> seed; READ_ONLY + explicit aws grant -> allowed for aws, still denied all ms writes.
2. Live (exercise, not config-read): alyssa@ calls `taxsma_costbasis` -> rows + audit-lake entry
   carrying her email; a third standard-tier user -> DENIED (the per-email gate discriminates
   within a tier — this is the sharp test); Andrew -> allowed with no explicit line (wildcard).
3. IAM: the 22a battery incl. the negative control (out-of-prefix implicitDeny).
4. End-to-end: `/tax-pt2 27265115` Phase-B path returns the same numbers as the Phase-A direct-S3
   path for the same asof (the parity check that retires Phase A).

## Sequencing

Leg 4 (table) and Leg 1 (entitlements core) in parallel -> Leg 3 (IAM) -> Leg 2 (integration,
consumes all three) -> acceptance -> flip `/tax-pt2` skill Phase B live. CTO gate sits on Legs 1+3;
OPLMCP lane builds 1+2; DS/monolith lane builds 4.
