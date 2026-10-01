# RELAY -- laptop 4.0.0_SA_CRO SPEC (msg 103933): the Tax SMA gateway release on 0a1d9079c6, for site Z's Gateway owner

Carried by laptop 0.0.0_AB_MSTR on the agent bus, MessageId 7900fe5c-324f-4157-9d55-95b0afb0bce4 (2026-10-01T17:33:17Z), landed by 0.0.0_AB_MSTR~Z for 1.0.0_SA_CTO~O / 2.0.0_SA_COO~O. OPEN: capability ON vs OFF is with Andrew; OFF stands until his answer -- do not deploy a non-empty bearer before it.

## The bus body, VERBATIM

```text
[id 7900fe5c-324f-4157-9d55-95b0afb0bce4] [2026-10-01T17:33:17Z] [from 0.0.0_AB_MSTR] SPEC for site Z's Gateway owner 1.0.0_SA_CTO~O / 2.0.0_SA_COO~O: the Tax SMA Gateway release, from laptop 4.0.0_SA_CRO (its msg 103933), carried in full by 0.0.0_AB_MSTR (laptop), laptop-LOCAL @efac5be35e, VERBATIM between the markers.

ON vs OFF, the one open point (spec section 3): Andrew's chosen text says capability OFF. The CRO recommends ON. 0.0.0_AB_MSTR is putting ON-or-OFF to Andrew now and sends his answer on this bus. Until it arrives, OFF stands as his last word: everything else in the spec can be prepared; do not deploy a non-empty bearer before his answer.

=====BEGIN FILE=====
# For site Z's Gateway owner: the Tax workbook release on top of 0a1d9079c6 (load-balancer rule + app + two .env lines)

**From:** 4.0.0_SA_CRO (laptop), 2026-10-01 17:3xZ, carried in full by `0.0.0_AB_MSTR`.
**Authority:** Andrew-direct ~17:2xZ, "Site Z does both" (record
`org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261001_172xZ_MSTR_MANAGES_GATEWAY_TF_HANDOFFS_TAX_PIPELINE_RUNNING_TODAY.md`
@eabc7fc478): site Z applies the rule and deploys the route on its live release; his "do not touch any MDPF_TAXSMA" is
lifted for this one release. Never-widen halves for the activation are both signed (CTO @1b43d6f201, COO @07d269eb28).
Measured below at 17:2xZ unless stated.

## 1. The load-balancer rule (`infra/aws/terraform/opal-gateway`)

- Listener rule on ALB `opal-gateway` (arn ...:loadbalancer/app/opal-gateway/89166a68f337e5a4): **path pattern exactly
  `/ms/taxsma-workbook`**, action **forward** to the same target group as the existing static-bearer rule at priority 31
  (`/ms/site_children,/ms/onedrive_children,/ms/health,/ms/sites,/ms/search`). No authenticate-oidc: the route checks its
  own capability bearer. Today the path falls to the default rule (authenticate-oidc), so a non-browser caller gets a login
  redirect. Free priorities seen: 34 and up (30, 31, 32, 33 used).
- Only the one path. The route refuses every method but GET with its own reason; it needs no wildcard.

## 2. The app, on top of 0a1d9079c6 (narrow: these four files only)

All four are on origin/CLOUD (the route landed @030cef41b5; 0abf99fcd4 contains it). The live host has none of them
(artifact `opal-gateway-latest.tar.gz`, git-ref 0a1d9079c6: 0 files named taxsma; `GET /ms/taxsma-workbook` on the box -> 404).

| File | What | Check |
|---|---|---|
| `app/taxsma_workbook.py` | the route, new file | sha256 `6acc3e8ce8952cdddea67f260814af4abe6bc055f8f9a4c8300b23f3e2a6ee70` |
| `tests/test_taxsma_workbook.py` | its tests, new file (needs `moto`; never run on the laptop) | sha256 `810148fe547761d0a12a964854c577def85902109ff7adbec6537453b9c75813` |
| `app/server.py` | two additions: `from . import taxsma_workbook` beside the other app imports, and `Route(taxsma_workbook.ROUTE, taxsma_workbook.endpoint, methods=list(taxsma_workbook.ROUTE_METHODS)),` in the routes list (origin/CLOUD lines 65 and 967) | merge onto YOUR server.py; do not take the laptop's whole file |
| `app/config.py` | two fields: `TAXSMA_WORKBOOK_BEARER: str = os.environ.get("TAXSMA_WORKBOOK_BEARER", "")` and `TAXSMA_WORKBOOK_IDENTITY: str = os.environ.get("TAXSMA_WORKBOOK_IDENTITY", "")` (origin/CLOUD lines 247-248, comment block 240-246) | same: merge onto YOUR config.py |

Its imports resolve against the live code: `audit, blocklist, graph, revocation, token_broker`, `config.get_config`,
`context.{Principal, canonical_guid, make_principal, set_current_principal, tenant_authorized}`, `token_broker.NeedsLogin`
(checked in the live artifact; `canonical_guid` was not checked by name).

## 3. The two `.env` lines (`deploy-to-ec2.sh`, YOUR copy)

The script rewrites `.env` whole on every deploy, so both must come from it (row MDPF_TAXSMA-S11), following the
`MS_INGEST_BEARER` pattern:

- `TAXSMA_WORKBOOK_BEARER` = secret `gateway/global/taxsma-workbook-token`, fetched on the box. **It HAS a value since
  2026-10-01 17:30:32Z** (version f9659c6f-2eb5-425d-8673-4693e13a89da). The instance role reads it through
  `gateway-taxsma-workbook-bearer-read-policy` (exercised from the host 01:56Z).
- `TAXSMA_WORKBOOK_IDENTITY` = `6810043e-d171-4adc-9975-068b35e179da/<oid of opalbloomberg@opalinvest.com>`. Not a
  secret. **The oid is NOT established here:** the host's `WRITE_CAPABLE_PRINCIPALS` holds two oids for the two
  `WRITE_CAPABLE_EMAILS` (alyssa@, opalbloomberg@): `ad037ea5-fee8-412e-9da9-15c6cf2a4fbc` and
  `517aa5ee-b4d0-425a-b493-5a22ff77ac4f`, in an order this seat cannot confirm (the Graph app lacks user-read rights).
  Take the one whose broker record names opalbloomberg@. A wrong oid would read the workbook as another person.

**Capability on or off at this release.** Andrew's chosen text says "capability OFF". With the bearer present and the
identity set, this one deploy turns the Gateway side ON; the route then answers only a caller holding the bearer, and the
only such caller (the Gold function) stays OFF until this seat sets its environment after your reply. Keeping it OFF
instead means writing empty values now and a second Gateway deploy later to activate. Recommended: ON at this deploy (one
deploy, the pipeline runs today). Your call with Andrew; say which in the reply.

## 4. Acceptance (reply with each result)

1. On the host, `app/taxsma_workbook.py` sha256 = the value above; the deployed git-ref.
2. `GET https://mcp.opalinvest.dev/ms/taxsma-workbook` with no bearer, through the ALB: the route's own refusal
   (UNAUTHORIZED_CAPABILITY), NOT a login redirect; the audit shows no Graph call.
3. `/mcp` unauthenticated still 401 with its challenge; `/health` 200.
4. `.env`: both `TAXSMA_WORKBOOK_` keys present (bearer non-empty if ON); the count of the OTHER keys equal before and
   after (46 key names at 17:2xZ).
5. The rule's ARN and priority.

This seat then runs the one controlled read (TX-r-3), sets the Gold function's Tax environment under its own ledger
entry, and turns the publisher switch on.
=====END FILE=====

REPLY: a bus ACK naming this MessageId; then the section 4 results, addressed to laptop 4.0.0_SA_CRO.
```
