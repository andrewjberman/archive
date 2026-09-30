# MX-r-5 PHASE B -- what the worker measured (no grading)

Deployer 0.9.0_WK_NFRA_MCPINDEX~14. Release: deploy-only 093fc247c6306dc0e5d26d92107dc9519965c7ad (gateway tree
2e839aeec903d6c7bc65cfba60017e4e5e925614 = release a7e15b2220, base 63264dfb22). Deployed 2026-09-29T10:11:34Z.
Ledger nfra-mcpindex-r4-gateway-release: CLOSED, 4 of 4 legs proven, sentinel removed. Not rolled back.

## Step 0 (R1), read before any act
| read | value |
|---|---|
| /c/tmp/mx-dep6 HEAD | 093fc247c6306dc0e5d26d92107dc9519965c7ad |
| nested mcportal | a3bff71, 0 status lines |
| live gateway by content | host sha256 of 79 files = the `-latest` artifact (63264dfb22) 79 of 79, and = the /c/tmp/mx-rb6 rebuild 79 of 79 |

## The deploy
`bash infra/aws/ec2/safe-ec2-deploy.sh opal-gateway infra/aws/ec2/opal-gateway/deploy-to-ec2.sh` from /c/tmp/mx-dep6.
- Run 1 (no ack): the halt gate printed 208 pending inbox items, all ledger-scan RED/HELD-STALE mail and CRO mail, 0 lines
  containing STOP, none naming opal-gateway; it exited 1 BEFORE any build or upload (log /c/tmp/mx-dep6-deploy.haltgate-refusal.log).
- Run 2 with `HALT_ACK=1` (the MX-r-4 precedent: ack only when the gate reads 0 STOP): built
  opal-gateway-093fc247c6.tar.gz (404K, mcportal a3bff71ffa), uploaded it and `-latest`, SSM 4d4ed9ff-4d67-463b-b89c-71c94a33039e
  `deploy Success`, `opal-gateway active`, `AS metadata serves`, `DEPLOY-EXIT=0` (log /c/tmp/mx-dep6-deploy.log).

## R2, the host read back after the deploy
| check | before | after |
|---|---|---|
| /health | 200 | 200 |
| `.env` ENABLED_INTEGRATIONS | `ycharts opal_portal globgrph opal_discover portal_index` | identical (same 5 ids) |
| `.env` lines with `=` | 27 | 27 |
| opal-gateway MainPID | 429157 | 432313 (restarted, active) |
| tool-name list | 51 | 52 |
| tools added / removed | | added `mdpf_get_model_benchmarks`; removed none |
| host files (79) vs the uploaded artifact opal-gateway-093fc247c6 | | 79 of 79 identical |
| host files vs the dep-tree pre-deploy rebuild | | 79 of 79 identical |
| host files changed from the 63264dfb22 state | | exactly 4: app/data_entitlement.py, app/integrations/opal_discover/integration.py, app/integrations/portal_index/integration.py, app/refs/DATA_CATALOG.yaml (0 added, 0 removed) |
| app/integrations/schwab/engine.py sha256 | 51245cf3acd2... | 51245cf3acd2... = 63264dfb22's version |

The tool list was read by importing `app.server` on the host with the host's own `.env` values (the MX-r-4 probe method).
The two lists are in `probes/tools_before_MX-r-5.txt` and `probes/tools_after_MX-r-5.txt`; `diff` prints one line:
`> mdpf_get_model_benchmarks`.

## r5.J1 material: what discover names, in-process on the host's deployed tree
Run on i-07dccb1615503ac99 with the host's `.env`, the opal-internal class constant (no user identity, no authenticated
session), live S3 HEADs on the instance role. It is what the deployed `discover()` names, not a client session's answer,
and the worker did not call the purpose-built tools or read any served object: the portal-side figure and as-of are the
issuer's principal-session close run. Full output: `probes/discover_on_host_MX-r-5.txt`. `SPEC.hosts` prints
`['opal-data-portal-v2.s3.amazonaws.com']`.

| surface | ask | catalogued | first match | next_tool | latest_value (held) | served_written_at (measured) |
|---|---|---|---|---|---|---|
| platinum/mdpf | model portfolio AUM | yes, 8 matches | mp.01.aum-metrics | mdpf_get_aum_metrics {scope: global} | 2026-08-10 | 2026-09-28T13:50:51Z |
| platinum/etfs | ETF holdings and fund flows | NO (0 matches) | none | none | | |
| platinum/advi | ADVI advisor tenant data | NO (0 matches) | none | none | | |
| json/* | What is year to date performance on the ST model | yes, 6 matches | mp.05.model-portfolio-benchmarks | mdpf_get_model_benchmarks {} | 2026-08-10 | 2026-09-26T11:06:31Z |

Facts a grader may want: the catalog holds no platinum/etfs row (MX-t-10 is not in this release) and no platinum/advi row, so
discover answers NOT_CATALOGUED for those two asks; the two mdpf rows after mp.01 (mp.02, mp.03) name their own tools; for
the json/* ask the second and third matches (mp.04, mp.06) have no purpose-built tool and name `query_v0` labelled an HTTP
route, `POST /query/v0`. The asks are the worker's, chosen to reach each surface; the issuer's close run chooses its own.
