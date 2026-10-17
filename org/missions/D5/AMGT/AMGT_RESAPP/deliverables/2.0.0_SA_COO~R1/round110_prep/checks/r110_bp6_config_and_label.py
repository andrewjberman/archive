"""AMGT_RESAPP round-110 PREP -- `AMGT-bp-6`: the function's configuration and one served label, read-only.

  python r110_bp6_config_and_label.py

Prints, from the LIVE function (`get-function-configuration` and one Lambda invoke, GET `/thesis` of RIO LN):
  CONFIG sha=<CodeSha256> modified=<LastModified> rev=<RevisionId> mem=<MemorySize> timeout=<Timeout> state=<State> update=<LastUpdateStatus>
  ENV keys=<sorted environment variable NAMES> (values are not printed)
  AMGT_AIFILL_ROOT in env: <True|False>
  RIO_LN periods[4] label=<label> fiscal_year=<fiscal_year> top_level_sum=<sum>
Writes nothing. Before the apply it reads the pre-act values (`Period 5`); after a successful apply it reads the new CodeSha256 and `Year not stated (column 5)`.
"""
import json

import boto3

FUNCTION = "opal-amgt-scoped-api"
KEY = "RIO_LN_Equity"


def main():
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    print("CONFIG sha=%s modified=%s rev=%s mem=%s timeout=%s state=%s update=%s" % (
        cfg.get("CodeSha256"), cfg.get("LastModified"), cfg.get("RevisionId"), cfg.get("MemorySize"), cfg.get("Timeout"),
        cfg.get("State"), cfg.get("LastUpdateStatus")))
    print("ENV keys=%s" % sorted(env))
    print("AMGT_AIFILL_ROOT in env: %s" % ("AMGT_AIFILL_ROOT" in env))
    event = {"rawPath": "/api/scoped/amgt/security/%s/thesis" % KEY, "queryStringParameters": None,
             "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    r = json.loads(lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(event).encode())["Payload"].read())
    body = json.loads(r.get("body") or "{}")
    periods = (body.get("segment_table") or {}).get("periods") or []
    p = periods[4] if len(periods) > 4 else {}
    print("RIO_LN periods[4] label=%s fiscal_year=%s top_level_sum=%s (status %s)" % (p.get("label"), p.get("fiscal_year"), p.get("top_level_sum"), r.get("statusCode")))


if __name__ == "__main__":
    main()
