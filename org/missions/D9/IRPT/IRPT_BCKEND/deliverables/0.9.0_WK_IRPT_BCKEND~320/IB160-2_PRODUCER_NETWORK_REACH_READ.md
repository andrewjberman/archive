# IB160-2 (IB-pr-465) -- does the holdings-performance producer's network reach the vendor

**REACHES** (claim: inferred from a measured configuration). A READ, NOT A BUILD. Base 7c00a44b5a; read at 2026-10-12T01:27:13Z. Data: `IB160-2_producer_network_reach.json`. No function invoked, no vendor call, no sign-in, no AWS write.

## The function
`irpt-holdings-performance-lambda` (49 Financial's; its twin `irpt-inf-holdings-performance-lambda` is Inflection's, same zip). Terraform: `infra/aws/terraform/investor-reporting/holdings-performance/lambda.tf:19` (twin `:67`); source-map entry `irpt-holdings-performance-lambda` in `infra/aws/lambda/ci/lambda-source-map.json`. Live: python3.12, 300 s, 1536 MB, one layer (`irpt-performance-native-layer:1`), no Environment block at all (so no key names to list).

## Network
Not in a VPC. Live `VpcConfig` is null; the Terraform passes no `vpc_config` to the module (its variable is optional, `modules/yang-lambda/main.tf:53-57`); 0 `vpc_config` matches in `infra/aws/terraform/investor-reporting`. So there are no subnets, route tables, security groups, NAT or endpoints to read, and none were read. A function outside a VPC has public outbound access by the platform's rule. That rule is not read from this account, hence `inferred`, not `measured`.

## What a fetch would use
`yfinance`: `fetch_yahoo` imports it at `data/assets/scripts/silver/commonwealth_price_basis_census.py:202` and calls `yf.download(...)` at `:234`. Hosts, read as text from the yfinance 1.2.0 installed on this box (not imported): bars from `query2.finance.yahoo.com` (`history.py:196`); also `query1.finance.yahoo.com`, `fc.yahoo.com`, `guce.yahoo.com`, `consent.yahoo.com` (`data.py`, `const.py`). All https. That version is not necessarily the one a Lambda would install.

**The package does not carry it** (false): none of the 14 packaged files names yfinance, no requirements file is named, and the one layer is described as pandas/numpy/pyarrow. The layer zip itself was not opened.

## Other candidates (all not in a VPC, live VpcConfig null)
`irpt-inf-holdings-performance-lambda`; `irpt-49f-reporting-gold-lambda` (900 s, 3008 MB, same layer); `irpt-49f-reporting-publish-lambda`.

## Not established
Whether Yahoo answers an AWS datacentre address at all; its rate limit from a fixed address; the layer's real contents; whether yfinance and its dependencies fit beside the existing layer (another function's note says the layer already takes about 230 of 250 MB, held); account-level egress controls other than a VPC; any later change to the function.
