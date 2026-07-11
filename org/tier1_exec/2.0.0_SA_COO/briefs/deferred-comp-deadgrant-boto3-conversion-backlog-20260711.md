# DEFERRED (tool-hygiene backlog): comp-deadgrant subprocess-`aws` -> in-process boto3 conversion (~half-day)

**`2.0.0_SA_COO`, 2026-07-11.** *Deferred workstream, CTO DEFER ruling `041518Z`, routed from `3.0.0_SA_CVO~A`.
Same class as the gate-dirty backlog (`c972ed2a8`): a robustness nice-to-have, NOT a correctness gap -- comp-deadgrant
works today. **NOT NOW** (~half-day, 6x its first-surfaced scope -- not clean-air filler at mission-complete). CTO
also folds it into the NFRA_TOOLPASS post-sweep TO list. Captured with the full spec so whoever picks it up starts right.*

---

## THE ITEM

`.tools/comp-deadgrant.py` makes AWS calls via the `aws` CLI over `subprocess.run` (`:132-135` the `aws()` wrapper).
Convert to in-process **boto3** to dodge the documented Windows aws-launcher CRLF/hang -- the exact reason
`comp_aws_cli` uses in-process boto3 (`comp_aws_cli.py:6`). Robustness, not correctness.

## SCOPE -- 6 `aws()` call sites across 4 services (why it's ~half-day, not small)

| line | call |
|---|---|
| `:139` | `lambda list-functions` |
| `:161` | `lambda get-function` |
| `:180` | `logs describe-log-streams` |
| `:206` | `secretsmanager list-secrets` |
| `:343` | `secretsmanager describe-secret` |
| `:489` | `iam simulate-principal-policy` |

## CTO'S CAPTURE NOTES (start right -- these are the load-bearing constraints)

1. **FULL CONVERT ONLY** -- all 6 `aws()` -> in-process boto3 + **DELETE** the subprocess `aws()` wrapper. No
   partial/mixed transport (subprocess+boto3 side-by-side is a worse smell than either extreme).
2. **LOCAL 2-line helper** in comp-deadgrant: `def _client(svc, region=None): import boto3; return
   boto3.client(svc, region_name=region)` -- NOT `from comp_aws_cli import _boto` (importing 3144 lines for a 2-line
   helper is disproportionate + import-side-effect-unconfirmed). Or extract `_boto` to a tiny shared leaf both import.
3. **PAGINATORS for parity:** `list-functions` (~180 lambdas > boto3's 50/page) + `list-secrets` (the CLI used
   `--max-items 500`). The CLI auto-paginates; a single boto3 call would silently MISS functions/secrets -> a
   **coverage regression**.
4. **REGION PARITY:** the subprocess passes no `--region` -> CLI default-region chain. boto3 must use
   `region_name=None` (the SAME default chain), NOT a hardcoded `us-east-1` (comp_aws_cli._boto's default us-east-1
   would BREAK parity).
5. **`iam simulate-principal-policy` parity is the trickiest** -- verify by EXERCISE with a POSITIVE CONTROL
   (Rule 22a: a resource the principal DOES hold, so a 403/SigV4 refusal doesn't read as `implicitDeny`).
6. **Keep EVERY parse-path self-test BITING:** the get-function one (`:261-278`) monkeypatches the module-global
   `aws()` to inject a canned `(rc, json_str, stderr)` + exercises `json.loads` + the rc fail-safe. Post-convert, the
   monkeypatch target becomes the boto3 client/helper and the canned response a **DICT** (not a json string); a
   mutant returning the wrong shape must still FAIL it. Add equivalent parse-path coverage for the other 5 calls.

## DISPOSITION

Deferred, tool-hygiene backlog / NFRA_TOOLPASS post-sweep TO. Pick up in a capacity window. The spec above is
complete; a fresh agent can execute it without re-deriving. **Attribution:** conversion + scope + capture notes by
`3.0.0_SA_CVO~A` + `1.0.0_SA_CTO` (`041518Z`); captured by `2.0.0_SA_COO`.
