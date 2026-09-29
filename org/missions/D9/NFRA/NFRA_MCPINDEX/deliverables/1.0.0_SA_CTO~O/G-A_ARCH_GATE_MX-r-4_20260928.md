# G-A arch-gate -- opal_discover and portal_index at release pin 2dedae93df

**Gate:** `docs/architecture/NFRA_INTEGRATIONS_STANDARD.md` s.8.1, G1-G8, run by `1.0.0_SA_CTO~O` on 2026-09-28 ~22:4xZ.
The ruling that G-A is this seat's gate is msg 26216.

**Pin:** `2dedae93df83179fa47bb3665aa724a78f68e95c`, branch `rel-nfra-mcpindex-r3-gateway`, worktree `/c/tmp/mx-rel3`. It is
the deployed release `6a98a0553a` plus three commits (2f14e38af9, 6cd7f4526d, 2dedae93df) that change 5 gateway files.
Nothing is deployed. The enable is `infra/aws/ec2/opal-gateway/deploy-to-ec2.sh:197`: the value
`ENABLED_INTEGRATIONS=ycharts opal_portal globgrph opal_discover portal_index`, a value-only change.

**Method:** every in-process check imports the pin's own `app/` package from the pin worktree (Python 3.11.9) and never
reads source summaries. The IAM view is `comp-iam role opal-gateway-role` (DESIRED), then LIVE `aws iam
list-role-policies` and `get-role-policy` through the `.tools/aws` shim.

## opal_discover (2 tools)

| # | Verdict | Grounding |
|---|---|---|
| G1 read-only | PASS | `validate_integration_spec(SPEC) == []` in-process. `read_only=True` (`app/integrations/opal_discover/integration.py`, SPEC). Both tools classified `OpClass.SAFE`. `discover()` reads only `query_v0._catalog()`, the local `app/refs/DATA_CATALOG.yaml`, and calls `catalog_gate.gate()`. No write path exists in the module. |
| G2 egress minimal | PASS | `hosts=("no-egress.invalid",)`, the RFC 2606 never-resolving name, since the validator refuses an empty allowlist. The module has no network client: `credential_provider=lambda: None`, and it reads the in-process catalog only. |
| G3 tool surface | PASS | In-process `register(FakeMCP)` returned `['opal_discover', 'opal_describe']`, and the decorated set is equal. Both start with `tool_prefix="opal_"` and both are SAFE. `register_enabled(['opal_discover'])` reports the same 2 tools, with 0 `composed_path_refused` and 0 `unclassified` (`app/data_entitlement.py:113-116` INDEX_TOOLS, class `legacy`). |
| G4 secret + IAM | PASS (not applicable to a secret) | `auth_kind=none`, `secret_id=''`. The integration makes no AWS call, so it needs no grant and no secret. |
| G5 min_tier | PASS in-process; running-gateway half is the CVO's | `min_tier="read_only"` is a known Tier. Read-only is the floor (`app/tier.py:25-29`), so no caller is below it and a below-tier deny is vacuous by construction. The compartmentalizing deny is the catalog gate. In-process at the pin, `discover("model portfolio")` returns 0 matches for an unresolved principal and 8 matches (3 servable) for Opal-internal. |
| G6 audit | PASS in-process; served-lake half is the CVO's | Both tools run through `run_integration_tool` (`app/integrations/base.py:116-179`), which calls `audit.log_call` with `tier=` on every branch (`:150`, `:158`, `:164`, `:170`, `:175`, `:178`). |
| G7 fail-closed | PASS in-process; deployed-bytes half is the CVO's | `register_enabled(mcp, [])` returned `{}` and registered 0 tools. `config.py:227-228` defaults `ENABLED_INTEGRATIONS` from an empty env. A spec with an emptied `hosts` was skip-registered ("invalid integration spec (not registered)", 0 tools). |
| G8 enable = gated deploy | PASS (this record is the pre-enable signature) | `ENABLED_INTEGRATIONS` is read once from the env (`app/config.py:227-228`) and registered once at startup (`app/server.py:85`). No runtime flip exists. The enable is the deploy-script `.env` value (`deploy-to-ec2.sh:197`) plus the deploy. |

## portal_index (3 tools)

| # | Verdict | Grounding |
|---|---|---|
| G1 read-only | PASS | `validate_integration_spec(SPEC) == []` in-process. `read_only=True`, and all 3 tools are classified `OpClass.SAFE` (`app/integrations/portal_index/integration.py:76-91`). The only I/O is one `s3.get_object` per call (`:225-240`). The module holds no object key: each key is resolved from the ONE catalog row that names the tool's accessor (`:111-160`). |
| G2 egress minimal | PASS | `hosts=("opal-data-portal-v2.s3.amazonaws.com",)` (`:47`, `:87`). In-process, boto3 (local botocore 1.43.46, us-east-1) resolves `get_object` on that bucket to exactly `https://opal-data-portal-v2.s3.amazonaws.com/...`. It is the same bucket and endpoint the live `query_v0` already reads, so the enable adds no new egress. The basis is the local botocore; the gateway pins `boto3>=1.34.0`. |
| G3 tool surface | PASS | In-process `register` returned `mdpf_get_aum_metrics`, `mdpf_get_account_distribution` and `mdpf_get_aggregate_aua`, all prefixed `mdpf_` and all SAFE. `register_enabled` reports those 3, with 0 refused and 0 unclassified (`data_entitlement.py:114`). |
| G4 secret + IAM | PASS | `auth_kind=none`, with no secret. The reads run on the instance role. LIVE `get-role-policy opal-gateway-role opal-gateway-queryv0-portal-read` allows `s3:GetObject` on `opal-data-portal-v2/json/*` and `opal-data-portal-v2/platinum/*`, no wildcard action (Sid `QueryV0PortalCatalogRead`). This existing grant covers every resolved key (`platinum/mdpf/{scope}/...`), so the enable adds NO IAM. The live inline set has 10 policies; `opal-gateway-golive` and `opal-gateway-daily-reports-read` were read and grant no broader S3 read. NOTE: the grant is `platinum/*` for the whole bucket. Firm separation for these tools is enforced in-process by `catalog_gate`, not by IAM (see G5); this is pre-existing and was not widened here. |
| G5 min_tier | PASS in-process; running-gateway half is the CVO's | `min_tier="read_only"`, the floor, so the tier deny is vacuous by construction; the catalog gate is the deny. In-process at the pin, per tool: an unresolved principal is REFUSED ("unresolvable principal class -- deny by default"); firm `49financial` asking for scope `cottonwood` is REFUSED ("may not read another scope's member key"); a member `../../x` is REFUSED; firm-own and Opal-internal RESOLVE. Every refusal made 0 S3 calls (15 of 15 cases). |
| G6 audit | PASS in-process; served-lake half is the CVO's | Through `run_integration_tool` with a stubbed getter: the unresolved caller logged outcome `error`, tier `read_only`; the Opal-internal caller logged `ok`, tier `master_admin`. Both records carry the tier. OBSERVATION: a catalog-gate refusal is audited as `error`, not `denied`, because `PrefixRefused` is an `IntegrationError`. The CVO's live cert should look for the refusal under `outcome=error` with the gate text in `detail`. Separating the outcome is a candidate enrichment, not a gate failure. |
| G7 fail-closed | PASS in-process; deployed-bytes half is the CVO's | The same result as opal_discover: an empty set registers 0 tools, and an invalid spec is skip-registered. The S3 client is built on the first call only (`:229-233`), never at import. |
| G8 enable = gated deploy | PASS (this record is the pre-enable signature) | Same as opal_discover. |

## The one failing test (Z-W1-S8)

At the pin, `tests/test_opal_discover.py` plus `tests/test_portal_index.py` read 14 passed and 1 failed, the one failure
being `test_portal_index.py::test_portal_tools_catalog_refs_resolve` (`:264`).
- It asserts that the 3 catalog refs equal the stems of `workflows/atom_decomposition/catalog_entries/portal_*.yaml`.
  At the pin, 0 such files exist, while all 3 refs resolve in the shipped `DATA_CATALOG.yaml` (the test's own print:
  "3 tools, 3 resolve in DATA_CATALOG.yaml").
- **It bears on no G item.** Every item reads the runtime catalog and the spec, and the missing files are the
  authoring sources of the catalog, which are not deployed. It is provenance hygiene, owned under Z-W1-S8 and
  Z-W13-S3; the ruling @8ed938b2d7 also takes the raw `s3_key` out of those source files. The pin's own
  `DATA_CATALOG.yaml` change adds `read_tool` and `accessor` to `portal_datasets` and no key literal.

## Overall verdict

**SIGNED** for both `opal_discover` and `portal_index` at pin `2dedae93df`: G1-G8 PASS for each, with no HOLD and no FAIL.
The signature covers these exact bytes. A re-cut pin needs a re-run of this gate.

Three halves are not this seat's to certify, and are stated as the CVO's post-enable live cert, not as holds:
- G5 on the running gateway: an unresolved or other-firm caller is refused with 0 egress;
- G6 in the served S3 audit lake: a refusal (`outcome=error`) and an ok call, both tier-stamped;
- G7 on the deployed bytes.

**Division of labor:** `1.0.0_SA_CTO~O` signs G1-G8 pre-enable (this record); `3.0.0_SA_CVO~O` independently live-certs
G5-G7 on the running gateway after the enable-deploy. The enable-deploy itself still needs its never-widen sign-off
(CTO half plus a second, non-acting half), which `2.0.0_SA_COO~MI` files separately; this record is not that sign-off.
