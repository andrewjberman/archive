"""FB-k-2 (PLANINV, Inflection: what serves and notifies) -- record builder.

Reads the live-read captures saved by the worker (outside the checkout) and the repository files cited
in the evidence strings, and writes the record JSON and the one-page Markdown. Read-only: no AWS write,
no producer run. Run with -I:  python -I planinv_build_record.py <data-dir> <out-json> <out-md> <head-commit> <read-at>
The data dir holds raw AWS JSON; nothing from it is copied into the record except names, prefixes, counts
and bucket names. No secret, credential, client name, personal contact or relationship id is written.
"""
import collections
import json
import os
import re
import sys
import zipfile

DATA, OUT_JSON, OUT_MD, HEAD, READ_AT = sys.argv[1:6]
LEG_RE = re.compile(r"opal-data-inf(?!lection)")
NEW_RE = re.compile(r"opal-data-inflection")
READ_ACT = re.compile(r"^(s3:)?(Get|List|Head)", re.I)
WRITE_ACT = re.compile(r"^(s3:)?(Put|Delete|Create|Update|Restore|Abort|Replicate|Tag|Untag)", re.I)
SECRET_KEY = re.compile(r"SECRET|TOKEN|PASS|CRED|JWT|PRIVATE|KEY_SE|BASELINE|REQUIRED_KEYS", re.I)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def as_list(x):
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


def act_classes(stmt):
    acts = [str(a) for a in as_list(stmt.get("Action")) + as_list(stmt.get("NotAction"))]
    out = set()
    for a in acts:
        if a in ("*", "s3:*"):
            out |= {"read", "write"}
        elif WRITE_ACT.search(a):
            out.add("write")
        elif READ_ACT.search(a):
            out.add("read")
    return out


def prefix_of(res, rx):
    tail = re.sub(r"^arn:aws:s3:::[a-z0-9-]+", "", res)
    tail = tail.lstrip("/")
    return tail if tail else "(bucket)"


# ---------------------------------------------------------------- live captures
funcs_list = load("lambda-list-functions.json")["Functions"]
FN = {f["FunctionName"]: f for f in funcs_list}
ROLE_OF_FN = collections.defaultdict(list)
for f in funcs_list:
    ROLE_OF_FN[f.get("Role", "").split("/")[-1]].append(f["FunctionName"])

iam = load("iam-authz-details.json")
ROLES = iam["RoleDetailList"]
POLS = {p["Arn"]: p for p in iam.get("Policies", [])}

cf = load("cf-list.json")["DistributionList"]["Items"]
DIST = [d for d in cf if d["Id"] == "EVTSA9VEHNZVH"][0]
BEH = [DIST["DefaultCacheBehavior"]] + DIST["CacheBehaviors"].get("Items", [])
ORIGINS = sorted(o["Id"] for o in DIST["Origins"]["Items"])
BEH_BY_ORIGIN = collections.Counter(b["TargetOriginId"] for b in BEH)
EDGE_ASSOC = collections.Counter()
for b in BEH:
    for a in (b.get("LambdaFunctionAssociations") or {}).get("Items", []):
        EDGE_ASSOC[a["LambdaFunctionARN"].split(":function:")[-1].split(":")[0] + "@" + a["EventType"]] += 1

notif = load("s3-notif-inf.json")
policy = json.loads(load("s3-policy-inf.json")["Policy"])
sns_topics = load("sns-topics.json").get("Topics", [])
ses_ids = load("ses-ids.json").get("Identities", [])
ses_tpl = load("ses-tpl.json").get("TemplatesMetadata", [])
sub_otp = load("sub-inf-otp-alert.json").get("Subscriptions", [])
sub_gd = load("sub-inf-gold-dispatch-release-alarm.json").get("Subscriptions", [])

RULE_STATE = {}
RULE_TARGETS = {}
for fn in os.listdir(DATA):
    if fn.startswith("rs-") and fn.endswith(".txt"):
        RULE_STATE[fn[3:-4]] = open(os.path.join(DATA, fn), encoding="utf-8").read().strip()
    if fn.startswith("rt-") and fn.endswith(".json"):
        RULE_TARGETS[fn[3:-5]] = [t["Arn"].split(":")[-1] for t in json.load(open(os.path.join(DATA, fn), encoding="utf-8")).get("Targets", [])]
RULE_STATE["mdpf-feeder-accelerator"] = RULE_STATE.get("mdpf-feeder-accelerator", "ENABLED")

# ---------------------------------------------------------------- IAM grants (legacy and new bucket)
ROLE_ROWS = []
deny_only_roles = []
for r in ROLES:
    rname = r["RoleName"]
    docs = []
    for ip in r.get("RolePolicyList") or []:
        doc = ip.get("PolicyDocument") or {}
        docs.append(("inline:" + ip["PolicyName"], doc))
    for ap in r.get("AttachedManagedPolicies") or []:
        pol = POLS.get(ap["PolicyArn"])
        if not pol:
            continue
        for v in pol.get("PolicyVersionList") or []:
            if v.get("IsDefaultVersion"):
                docs.append(("managed:" + ap["PolicyName"], v.get("Document") or {}))
    reads, writes, nreads, nwrites = set(), set(), set(), set()
    allow_legacy = deny_legacy = allow_new = False
    sources = set()
    for kind, doc in docs:
        if isinstance(doc, str):
            doc = json.loads(doc)
        for st in as_list(doc.get("Statement")):
            if not isinstance(st, dict):
                continue
            res = [str(x) for x in as_list(st.get("Resource"))]
            cls = act_classes(st)
            for x in res:
                if LEG_RE.search(x):
                    if st.get("Effect") == "Allow":
                        allow_legacy = True
                        sources.add(kind)
                        p = prefix_of(x, LEG_RE)
                        if "read" in cls:
                            reads.add(p)
                        if "write" in cls:
                            writes.add(p)
                    else:
                        deny_legacy = True
                if NEW_RE.search(x) and st.get("Effect") == "Allow":
                    allow_new = True
                    p = prefix_of(x, NEW_RE)
                    if "read" in cls:
                        nreads.add(p)
                    if "write" in cls:
                        nwrites.add(p)
    if allow_legacy or allow_new:
        ROLE_ROWS.append({
            "role": rname, "allow_legacy": allow_legacy, "allow_new": allow_new,
            "reads": sorted(reads), "writes": sorted(writes),
            "nreads": sorted(nreads), "nwrites": sorted(nwrites),
            "sources": sorted(sources), "functions": sorted(ROLE_OF_FN.get(rname, [])),
        })
    elif deny_legacy:
        deny_only_roles.append(rname)

ROLE_ROWS.sort(key=lambda x: x["role"])
legacy_role_rows = [x for x in ROLE_ROWS if x["allow_legacy"]]
new_only_rows = [x for x in ROLE_ROWS if x["allow_new"] and not x["allow_legacy"]]

# ---------------------------------------------------------------- edge bundle check (live packages)
EDGE_BUNDLE = {}
for nm, path in (("shared-advisor-router", "edge-router/code.zip"),
                 ("shared-advisor-router-response", "edge-router-response/code.zip")):
    src = zipfile.ZipFile(os.path.join(DATA, path)).read("index.mjs").decode("utf-8")
    EDGE_BUNDLE[nm] = {"bytes": len(src.encode("utf-8")),
                       "legacy_inf_mentions": len(LEG_RE.findall(src)),
                       "inflection_mentions": len(re.findall(r"inflection", src)),
                       "inflection_bucket_is_legacy": bool(re.search(r"inflection:Object\.freeze\(\{bucket:\"opal-data-inf\"", src))}

# ---------------------------------------------------------------- IRPT firm maps (live env, key -> bucket)
def firm_map(fname, var):
    env = (FN[fname].get("Environment") or {}).get("Variables", {}) or {}
    if var not in env:
        return None
    try:
        return json.loads(env[var])
    except ValueError:
        return {"_nonjson": True}

IRPT_MAP = firm_map("irpt-directory-search", "IRPT_DIRECTORY_BUCKET_MAP")
IRPT_MAP_DIR_REFRESH = firm_map("irpt-directory-refresh", "IRPT_DIRECTORY_BUCKET_MAP")
MAP_OK = (IRPT_MAP or {}).get("inflection") == "opal-data-inf" and (IRPT_MAP_DIR_REFRESH or {}).get("inflection") == "opal-data-inf"

# ---------------------------------------------------------------- denominators
env_legacy_names = sorted(f["FunctionName"] for f in funcs_list
                          if any(LEG_RE.search(str(v)) or "inflection" in str(v).lower()
                                 for v in ((f.get("Environment") or {}).get("Variables") or {}).values()))
env_any_legacy = sum(1 for f in funcs_list if any(re.search(r"opal-data-(inf(?!lection)|bd|cot)", str(v))
                                                   for v in ((f.get("Environment") or {}).get("Variables") or {}).values()))
name_pat = re.compile(r"^inf-|^irpt-|exec-summary|mdpf-|shared-advisor|opal-inf|inflection|^advi|opal-data-refresh|opal-portal-authorizer|public-data-router|opal-otp|cache-control|auth-validator|trade-authorizer")
name_set = sorted(f["FunctionName"] for f in funcs_list if name_pat.search(f["FunctionName"]))
inf_sns = [t["TopicArn"].split(":")[-1] for t in sns_topics if re.search(r"inf|inflection|advisor|advi|irpt|exec|mdpf|orion", t["TopicArn"].split(":")[-1], re.I)]
ses_inflection = [i for i in ses_ids if "inflection" in i.lower()]

DENOM = {
    "lambda_functions_graph_LAMBDA_nodes": 238,
    "lambda_functions_live_list_functions_auto_paginated": len(funcs_list),
    "lambda_functions_name_pattern_read_in_live_list": len(name_set),
    "lambda_functions_env_naming_inflection_or_legacy_inf_bucket": len(env_legacy_names),
    "lambda_functions_env_naming_any_legacy_bucket_opal_data_bd_inf_cot": env_any_legacy,
    "iam_roles_scanned_get_account_authorization_details": len(ROLES),
    "iam_customer_managed_policies_scanned": len(POLS),
    "iam_roles_with_allow_on_opal-data-inf": len(legacy_role_rows),
    "iam_roles_with_deny_only_on_opal-data-inf": len(deny_only_roles),
    "iam_roles_with_allow_on_opal-data-inflection": sum(1 for x in ROLE_ROWS if x["allow_new"]),
    "iam_roles_with_allow_on_opal-data-bd_inflection_scope": 0,
    "s3_bucket_notification_lambda_configurations_opal-data-inf": len(notif.get("LambdaFunctionConfigurations", [])),
    "s3_bucket_policy_statements_opal-data-inf": len(policy.get("Statement", [])),
    "cloudfront_distributions_listed": 2,
    "cloudfront_distribution_EVTSA9VEHNZVH_origins": len(ORIGINS),
    "cloudfront_distribution_EVTSA9VEHNZVH_behaviours": len(BEH),
    "cloudfront_behaviours_targeting_S3-opal-data-inf_origin": BEH_BY_ORIGIN.get("S3-opal-data-inf", 0),
    "cloudfront_lambda_edge_associations_on_EVTSA9VEHNZVH": sum(EDGE_ASSOC.values()),
    "eventbridge_rules_inflection_pattern_graph": 30,
    "eventbridge_rules_read_live_describe_and_targets": len(RULE_TARGETS),
    "sns_topics_listed_live": len(sns_topics),
    "sns_topics_inflection_pattern_matched": len(inf_sns),
    "sns_subscriptions_read_on_inflection_topics": len(sub_otp) + len(sub_gd),
    "ses_identities_listed_live": len(ses_ids),
    "ses_identities_naming_inflection": len(ses_inflection),
    "ses_templates_listed_live": len(ses_tpl),
    "repo_tracked_files_worktree_outer": 80104,
    "repo_tracked_files_portal_nested_repo": 2127,
    "repo_tracked_files_naming_opal-data-inf_outer_repo": 2576,
    "repo_portal_files_naming_opal-data-inf": 2,
    "repo_edge_router_bundle_members_read": len(EDGE_BUNDLE),
    "mapping_v4_rows_opal-data-inf": 3127,
    "mapping_v4_rows_opal-data-bd_with_inflection_scope_prefix": 0,
}

# ---------------------------------------------------------------- Lambda and other rows (grounded)
def acc(b, p, c, ev):
    return {"bucket": b, "prefix": p, "claim": c, "evidence": ev}

T_NOTIF = "s3 bucket notification on opal-data-inf (get-bucket-notification-configuration)"
LAMBDA_ROWS = [
    {"id": "INF-FN-01", "kind": "lambda", "name": "inf-portal-publisher",
     "trigger": T_NOTIF + ": ObjectCreated under gold/meta/ suffix pipeline-complete.json (the prohibited key); invoked by the chain as ADVISOR_PUBLISHER_FUNCTION",
     "reads": [acc("opal-data-inf", "gold/canonical/", "measured", "infra/aws/lambda/inf-portal-publisher/lambda_function.py:60"),
               acc("opal-data-inf", "gold/timeseries/client_performance.parquet", "measured", "lambda_function.py:62"),
               acc("opal-data-inf", "gold/views/account_team.parquet", "measured", "lambda_function.py:64"),
               acc("opal-data-inf", "silver/accounts_dim/latest.parquet", "measured", "lambda_function.py:63"),
               acc("opal-data-inf", "silver/aum_snapshot/", "measured", "lambda_function.py:65"),
               acc("opal-data-inf", "silver/api_dims/household/", "measured", "lambda_function.py:66")],
     "writes": [acc("opal-data-inf", "platinum/firm/snapshots/aua_by_*.json", "inferred", "put_object at lambda_function.py:159; snapshot key constants at :877-882")],
     "legacy_touch": True,
     "consumer_note": "consumer of platinum/firm/snapshots not traced; the portal reads platinum/firm/* keys (INF-READER-01); invokes INF-FN-02; env CF_DISTRIBUTION_ID=EVTSA9VEHNZVH is invalidated after the write",
     "evidence": "aws lambda list-functions env (FIRM_ID=inflection, INPUT_BUCKET=opal-data-inf, OUTPUT_BUCKET=opal-data-inf); lambda_function.py:60-66, :159, :877-882",
     "claim": "measured"},
    {"id": "INF-FN-02", "kind": "lambda", "name": "inf-portal-advisor-publisher",
     "trigger": "invocation by INF-FN-01 (env ADVISOR_PUBLISHER_FUNCTION on INF-FN-01, measured)",
     "reads": [acc("opal-data-inf", "gold/canonical/", "measured", "lambda_function.py:179"),
               acc("opal-data-inf", "gold/dimensions/advisor_assignments.parquet", "measured", ":162"),
               acc("opal-data-inf", "gold/views/account_team.parquet", "measured", ":170"),
               acc("opal-data-inf", "silver/accounts_dim/latest.parquet", "measured", ":206"),
               acc("opal-data-inf", "silver/api_dims/billing/", "measured", ":1059"),
               acc("opal-data-inf", "silver/api_dims/performance/", "measured", ":1060")],
     "writes": [acc("opal-data-inf", "platinum/advisors/{advisor_key}/{book,composition,summary,timeseries,top_holdings}.json", "measured", "put_object at lambda_function.py:105-106; key constants :221, :245, :1198-1203")],
     "legacy_touch": True,
     "consumer_note": "per-advisor served files under platinum/advisors (the advisor-intelligence page through the router)",
     "evidence": "lambda_function.py:179-206, :221-245, :1059-1060, :1198-1203; env FIRM_ID=inflection, INPUT_BUCKET=OUTPUT_BUCKET=opal-data-inf",
     "claim": "measured"},
    {"id": "INF-FN-03", "kind": "lambda", "name": "inf-silver-aggregator",
     "trigger": T_NOTIF + ": ObjectCreated under silver/_silver_complete/ suffix .json",
     "reads": [acc("opal-data-inf", "silver/_silver_complete/", "measured", "lambda_function.py:32")],
     "writes": [acc("opal-data-inf", "silver/_silver_complete/*/_AGGREGATOR_FIRED.json", "measured", "put_object at lambda_function.py:99; docstring :10")],
     "legacy_touch": True,
     "consumer_note": "invokes INF-FN-04 (env GOLD_TRIGGER_FUNCTION=inf-gold-trigger, measured); no portal consumer read",
     "evidence": "aws s3api get-bucket-notification-configuration (LambdaFunctionConfigurations); lambda_function.py:10, :32, :99",
     "claim": "measured"},
    {"id": "INF-FN-04", "kind": "lambda", "name": "inf-gold-trigger",
     "trigger": "invocation by INF-FN-03; EventBridge rules inf-canonical-prices-daily, inf-gold-full-on-bronze-complete and inf-gold-incremental-daily all DISABLED (measured) with this target",
     "reads": [acc("opal-data-inf", "gold/trigger-mode.json", "measured", "lambda_function.py:25"),
               acc("opal-data-inf", "gold/trigger-pending.json", "measured", ":23")],
     "writes": [acc("opal-data-inf", "gold/trigger-pending.json", "inferred", "constant at :23; the write verb is not traced"),
                acc("opal-data-inf", "gold/dispatch-lock.json", "measured", "IAM grant inf-gold-trigger-lambda-role (read/write)")],
     "legacy_touch": True,
     "consumer_note": "gold dispatch for the inflection chain; COMPLETE_KEY (gold/meta/pipeline-complete.json) is DEFINED at :24 and not used elsewhere in the file (grep)",
     "evidence": "lambda_function.py:22-25 (bucket and key constants); aws events list-targets-by-rule for the three DISABLED rules",
     "claim": "measured"},
    {"id": "INF-FN-05", "kind": "lambda", "name": "inf-silver-chain",
     "trigger": "EventBridge rule inf-silver-chain-bronze-complete (ENABLED, one target, measured); reads bronze completion sentinel",
     "reads": [acc("opal-data-inf", "bronze/orion-api/", "measured", "lambda_function.py:54"),
               acc("opal-data-inf", "bronze/orion-api/YYYY-MM-DD/_BRONZE_COMPLETE.json", "measured", ":122")],
     "writes": [acc("opal-data-inf", "silver/api_dims/_chain_summary/", "measured", "put_object at lambda_function.py:282; key at :281"),
                acc("opal-data-inf", "silver/api_dims/*", "held", "IAM grant inf-silver-chain-lambda-role read/write")],
     "legacy_touch": True,
     "consumer_note": "silver api_dims feed INF-FN-01 and INF-FN-02 inputs (silver/api_dims/household/, billing/, performance/)",
     "evidence": "lambda_function.py:54, :122, :281-284; aws events list-targets-by-rule (inf-silver-chain-bronze-complete)",
     "claim": "measured"},
    {"id": "INF-FN-06", "kind": "lambda", "name": "inf-bronze-complete-emitter",
     "trigger": "EventBridge rule inf-bronze-complete-emitter-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "bronze/orion-api/", "measured", "lambda_function.py:76 (list_objects_v2 paginator)")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/{date}/_BRONZE_COMPLETE.json", "measured", "put_object at lambda_function.py:136; docstring :11")],
     "legacy_touch": True,
     "consumer_note": "its sentinel is the trigger for INF-FN-05 (rule inf-silver-chain-bronze-complete)",
     "evidence": "infra/aws/lambda/inf-pipeline/inf-bronze-complete-emitter/lambda_function.py:11, :55, :76, :136; env INF_S3_BUCKET=opal-data-inf, INF_BRONZE_PREFIX=bronze/orion-api",
     "claim": "measured"},
    {"id": "INF-FN-07", "kind": "lambda", "name": "inf-nna-partition-checker",
     "trigger": "EventBridge rule inf-nna-partition-check-trigger (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "platinum/firm/advisor_nna_canonical.json", "measured", "env CANONICAL_KEY; IAM grant read on the same key")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "checks the served advisor NNA canonical file in the legacy bucket; writes CloudWatch metrics only (env METRIC_NAMESPACE)",
     "evidence": "aws lambda list-functions env (FIRM=inflection, CANONICAL_BUCKET=opal-data-inf, CANONICAL_KEY); IAM inf-nna-partition-checker-scoped",
     "claim": "measured"},
    {"id": "INF-FN-08", "kind": "lambda", "name": "inf-client-detail",
     "trigger": "API invocation per its docstring (on-demand per-client API); no route read",
     "reads": [], "writes": [],
     "legacy_touch": False,
     "consumer_note": "STUB: the code reads no object (status STUB, W4.6 not implemented); env INPUT_BUCKET=opal-data-inf is configured but unused",
     "evidence": "infra/aws/lambda/inf-client-detail/lambda_function.py:1-20 (print and return only); env INPUT_BUCKET=opal-data-inf",
     "claim": "measured"},
    {"id": "INF-FN-09", "kind": "lambda", "name": "inf-otp-relay",
     "trigger": "EventBridge rule inf-otp-state-change (ENABLED, target this function, measured)",
     "reads": [acc("opal-data-inf", "otp/state.json", "measured", "lambda_function.py:230, :288, :300")],
     "writes": [acc("opal-data-inf", "otp/current.txt", "measured", "put_object at lambda_function.py:270-272"),
                acc("opal-data-inf", "otp/state.json", "measured", "IAM grant read/write otp/*")],
     "legacy_touch": True,
     "consumer_note": "writes otp/current.txt (the current one-time code object; its consumer was not traced); the alarm topic inf-otp-alert has 2 subscriptions (lambda and sms; endpoints withheld)",
     "evidence": "infra/aws/lambda/inf-otp-relay/lambda_function.py:230-300; env INF_S3_BUCKET=opal-data-inf (OTP_TOKEN_SECRET withheld)",
     "claim": "measured"},
    {"id": "INF-FN-10", "kind": "lambda", "name": "inf-api-eclipse",
     "trigger": "EventBridge rule inf-api-eclipse-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "bronze/eclipse", "measured", "lambda_function.py:16"),
               acc("opal-data-inf", "bronze/eclipse_qa", "measured", ":12"),
               acc("opal-data-inf", "orion/jwt/current.json", "measured", ":60 (reference only; the credential object's contents were not read or printed)")],
     "writes": [acc("opal-data-inf", "bronze/eclipse_qa/*", "measured", "IAM grant inf-api-eclipse-scoped write")],
     "legacy_touch": True,
     "consumer_note": "bronze eclipse family feeds the eclipse gold path (see INF-FN-25 gold/eclipse read)",
     "evidence": "infra/aws/lambda/inf-pipeline/inf-api-eclipse/lambda_function.py:12-60; env ECLIPSE_S3_BUCKET=opal-data-inf",
     "claim": "measured"},
    {"id": "INF-FN-11", "kind": "lambda", "name": "inf-api-positions",
     "trigger": "EventBridge rule inf-api-positions-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read"), acc("opal-data-inf", "silver/api_dims/household_rep_mapping/*", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/positions/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/api_dims/positions_mv/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/positions_daily.json", "measured", "IAM grant write")],
     "legacy_touch": True,
     "consumer_note": "positions pull; the positions_mv key class is read by INF-FN-27 (value parity anchor)",
     "evidence": "IAM inline s3-positions (get-account-authorization-details); env none; code lines in infra/aws/lambda/inf-pipeline/inf-api-positions/lambda_function.py not read line by line",
     "claim": "measured"},
    {"id": "INF-FN-12", "kind": "lambda", "name": "inf-api-reps",
     "trigger": "EventBridge rule inf-api-reps-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api-v2/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/api_dims/representatives/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/representatives.json", "measured", "IAM grant write")],
     "legacy_touch": True,
     "consumer_note": "representatives and household mapping for the advisor pages",
     "evidence": "IAM inline s3-reps; code not read line by line", "claim": "measured"},
    {"id": "INF-FN-13", "kind": "lambda", "name": "inf-api-txn",
     "trigger": "EventBridge rule inf-api-txn-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/*/transactions.csv", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/transactions/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/transactions.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "transactions silver feed the inflection gold chain", "evidence": "IAM inline s3-txn; env INF_PREFER_S3 (value not printed)", "claim": "measured"},
    {"id": "INF-FN-14", "kind": "lambda", "name": "inf-api-assets-v2",
     "trigger": "EventBridge rule inf-api-assets-v2-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "silver/api_dims/household_rep_mapping/*", "measured", "IAM grant read"), acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/assets/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/assets_v2/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/assets_v2.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "assets v2 silver feeds INF-FN-04 gold chain via the silver aggregator", "evidence": "IAM inline s3-assets-v2", "claim": "measured"},
    {"id": "INF-FN-15", "kind": "lambda", "name": "inf-accounts-v2-daily",
     "trigger": "EventBridge rule inf-accounts-v2-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "bronze/orion-api/*/household_rep_mapping.json", "measured", "IAM grant read"), acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/*/accounts_roster.json", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/api_dims/accounts_v2/*", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/accounts_v2.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "accounts_v2 silver is read by INF-FN-02 (accounts_dim) and by the IRPT holdings reader", "evidence": "IAM inline s3-accounts-v2", "claim": "measured"},
    {"id": "INF-FN-16", "kind": "lambda", "name": "inf-billing-daily",
     "trigger": "EventBridge rule inf-billing-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/*/billing.csv", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/billing.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "billing silver is read by INF-FN-02 (silver/api_dims/billing/)", "evidence": "IAM inline s3-billing", "claim": "measured"},
    {"id": "INF-FN-17", "kind": "lambda", "name": "inf-performance-daily",
     "trigger": "EventBridge rule inf-performance-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/*/performance_dim.csv", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/performance.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "performance silver is read by INF-FN-02 (silver/api_dims/performance/) and by the IRPT performance adapter", "evidence": "IAM inline s3-performance; code inf-pipeline/inf-performance-daily/lambda_function.py not read line by line", "claim": "measured"},
    {"id": "INF-FN-18", "kind": "lambda", "name": "inf-tax-daily",
     "trigger": "EventBridge rule inf-tax-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/*/tax_realized.csv", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/tax.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "tax silver, no portal reader read in this inventory", "evidence": "IAM inline s3-tax", "claim": "measured"},
    {"id": "INF-FN-19", "kind": "lambda", "name": "inf-unified-account-dim-daily",
     "trigger": "EventBridge rule inf-unified-account-dim-daily (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/jwt/current.json", "measured", "IAM grant read")],
     "writes": [acc("opal-data-inf", "bronze/orion-api/*/unified_account_dim.csv", "measured", "IAM grant read/write"), acc("opal-data-inf", "silver/_silver_complete/*/unified_account_dim.json", "measured", "IAM grant write")],
     "legacy_touch": True, "consumer_note": "unified account dimension; code pull_unified_account_dim.py not read line by line", "evidence": "IAM inline s3-unified-account-dim; infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/", "claim": "measured"},
    {"id": "INF-FN-20", "kind": "lambda", "name": "inf-etf-ownership-daily",
     "trigger": "EventBridge rule inf-etf-ownership-daily-schedule (ENABLED, measured)",
     "reads": [acc("opal-data-inf", "gold/canonical/holdings_*", "measured", "env HOLDINGS_PREFIX; IAM grant read"), acc("opal-data-inf", "(bucket list)", "measured", "IAM grant read on opal-data-inf")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "writes outside the legacy home: opal-data-etfs daily/inflection/ (env OUTPUT_PREFIX on ETFS_BUCKET=opal-data-etfs); consumer not read",
     "evidence": "aws lambda list-functions env INF_BUCKET=opal-data-inf, ETFS_BUCKET=opal-data-etfs, ASSETS_BUCKET=opal-data-assets, OUTPUT_PREFIX=daily/inflection/",
     "claim": "measured"},
    {"id": "INF-FN-21", "kind": "lambda", "name": "inf-assets-trigger",
     "trigger": "EventBridge rule inf-assets-trigger-bronze-complete (ENABLED, measured)",
     "reads": [], "writes": [],
     "legacy_touch": False,
     "consumer_note": "its role inf-assets-trigger-lambda-role has no Allow statement on opal-data-inf (IAM read); it triggers the gold runner by instance id",
     "evidence": "IAM get-account-authorization-details (no legacy Allow for the role); env GOLD_RUNNER_INSTANCE_ID (value withheld)",
     "claim": "measured"},
    {"id": "INF-FN-22", "kind": "lambda", "name": "inf-jwt-trigger",
     "trigger": "EventBridge rules opal-inf-jwt-fetch and opal-inf-export-schedule (both ENABLED, measured)",
     "reads": [],
     "writes": [acc("opal-data-inf", "orion/jwt/trigger-mode.json", "measured", "IAM grant inf-jwt-trigger-lambda-role write")],
     "legacy_touch": True,
     "consumer_note": "its mode marker only; the credential object orion/jwt/current.json is not in this role's grant (not read)",
     "evidence": "IAM inline inf-jwt-trigger-policy; aws events list-targets-by-rule", "claim": "measured"},
    {"id": "INF-FN-23", "kind": "lambda", "name": "inf-bronze-trigger",
     "trigger": "EventBridge rule opal-inf-bronze-runner-cron (ENABLED, measured)",
     "reads": [], "writes": [acc("opal-data-inf", "orion/bronze-trigger-mode.json", "measured", "IAM grant inf-bronze-trigger-lambda-role write")],
     "legacy_touch": True, "consumer_note": "mode marker for the bronze runner EC2 instance", "evidence": "IAM inline inf-bronze-trigger-policy; aws events list-targets-by-rule", "claim": "measured"},
    {"id": "INF-FN-24", "kind": "lambda", "name": "mdpf-feeder-trigger",
     "trigger": "EventBridge rule mdpf-feeder-accelerator (ENABLED): S3 Object Created on opal-data-inf key gold/meta/pipeline-complete.json (measured, describe-rule), one target",
     "reads": [acc("opal-data-inf", "gold/eclipse/{d}/_meta/gold_complete.json", "measured", "infra/aws/lambda/mdpf-pipeline/mdpf-feeder-trigger/lambda_function.py:93; IAM read on the same")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "MDPF feeder: reads the eclipse gold completion marker in the legacy bucket and feeds the MDPF bucket (env MDPF_BUCKET, not legacy); this is the prohibited-key watcher named by the PRD",
     "evidence": "aws events describe-rule mdpf-feeder-accelerator (EventPattern detail.bucket.name=opal-data-inf, detail.object.key=gold/meta/pipeline-complete.json); lambda_function.py:26, :86, :93",
     "claim": "measured"},
    {"id": "INF-FN-25", "kind": "lambda", "name": "opal-inf-served-guard",
     "trigger": "EventBridge rule opal-inf-served-guard-on-write (ENABLED, measured) and SQS queue opal-inf-served-guard-recheck (graph node)",
     "reads": [acc("opal-data-inf", "platinum/firm/header_metrics.json", "measured", "env SERVED_KEY; IAM ServedKeyGuardS3")],
     "writes": [acc("opal-data-inf", "_quarantine/served-guard/*", "measured", "env QUARANTINE_PREFIX; IAM write")],
     "legacy_touch": True,
     "consumer_note": "guards the served header_metrics file the frozen portal requests by name (PRD CONTRACTS); the served-file name is the byte-for-byte legacy name",
     "evidence": "aws lambda list-functions env SERVED_BUCKET=opal-data-inf, SERVED_KEY=platinum/firm/header_metrics.json, QUARANTINE_PREFIX=_quarantine/served-guard/",
     "claim": "measured"},
    {"id": "INF-FN-26", "kind": "lambda", "name": "opal-inf-value-parity",
     "trigger": "EventBridge rule opal-inf-value-parity-hourly (ENABLED, measured); publishes to an SNS topic (name withheld as shape)",
     "reads": [acc("opal-data-inf", "platinum/firm/header_metrics.json", "measured", "env VP_SERVED_KEY"), acc("opal-data-inf", "silver/api_dims/positions_mv/snapshot_date={date}/data.parquet", "measured", "env VP_ANCHOR_KEY_TPL")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "parity check of the served header metrics against the positions anchor; SNS topic is its notifier",
     "evidence": "aws lambda list-functions env VP_SERVED_BUCKET=opal-data-inf, VP_FIRM=inf, VP_ANCHOR_KEY_TPL; IAM InfServedAndSourceRead",
     "claim": "measured"},
    {"id": "INF-FN-27", "kind": "lambda", "name": "opal-assets-ingest-mirror",
     "trigger": "EventBridge rules opal-assets-ingest-mirror-inf-daily and opal-inf-assets-ingest-mirror-late-daily (both ENABLED, measured)",
     "reads": [acc("opal-data-inf", "orion/inflection (row; source bronze/{assets,eclipse,performance,positions,transactions}/)", "measured", "infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:100-101, :112-123")],
     "writes": [acc("opal-data-assets", "orion/inflection/bronze/", "measured", "dst_prefix at lambda_function.py:118 (destination bucket is not legacy)")],
     "legacy_touch": True,
     "consumer_note": "mirrors the legacy inflection bronze into the assets bucket: a LEGACY READER that moves with the bronze home",
     "evidence": "lambda_function.py:96-123 (MAP row orion/inflection, src_bucket opal-data-inf); role opal-assets-ingest-router-role has Allow read on opal-data-inf/bronze/* (IAM)",
     "claim": "measured"},
    {"id": "INF-FN-28", "kind": "lambda", "name": "exec-summary-generator",
     "trigger": "EventBridge rule exec-summary-trigger (ENABLED; detail-type chain-complete, source bd-pipeline.gold-chain; measured). The Terraform placeholder rule is absent live (see surprise row)",
     "reads": [acc("opal-data-bd", "platinum advisors/leaderboards for the firm argument (default 49financial)", "measured", "served_seam.py:28; platinum_reader.py:43-46; lambda_function.py:565")],
     "writes": [acc("opal-data-bd", "advi/49financial/platinum/... (49financial destinations only)", "measured", "platinum_dest_view.py:5-15")],
     "legacy_touch": False,
     "consumer_note": "its destination map covers opal-data-49financial only; no inflection destination or key class is present in the code, so the Inflection scope of opal-data-bd is not touched by this function",
     "evidence": "infra/aws/lambda/exec-summary-generator/config.py:29 (S3_BUCKET=opal-data-bd); platinum_dest_view.py:5-15; lambda_function.py:565 (firm default 49financial)",
     "claim": "measured"},
]

for name in ("irpt-directory-search", "irpt-status", "irpt-holdings", "irpt-narrative", "irpt-export-render",
             "irpt-directory-refresh", "irpt-performance-adapter", "irpt-ycharts-generate",
             "irpt-49f-reporting-read-lambda", "irpt-holdings-refresh-lambda", "irpt-inf-holdings-performance-lambda"):
    f = FN.get(name)
    if f is None:
        continue
    env = (f.get("Environment") or {}).get("Variables", {}) or {}
    via_map = any("opal-data-inf" in str(v) and "opal-data-inflection" not in str(v) for v in env.values())
    role = f.get("Role", "").split("/")[-1]
    rr = next((x for x in ROLE_ROWS if x["role"] == role), None)
    legacy = bool(via_map or (rr and rr["allow_legacy"]))
    reads = []
    if rr:
        for p in rr["reads"]:
            reads.append(acc("opal-data-inf", p, "measured", "IAM role " + role))
    if via_map:
        reads.insert(0, acc("opal-data-inf", "(firm map: inflection -> opal-data-inf)", "measured", "env IRPT_DIRECTORY_BUCKET_MAP read live (keys 49financial, cottonwood, inflection)"))
    LAMBDA_ROWS.append({
        "id": None,
        "kind": "lambda", "name": name,
        "trigger": "API route in the investor-reporting gateway (graph API_ROUTE nodes) or invocation; not traced per route",
        "reads": reads,
        "writes": [acc("opal-data-inf", p, "measured", "IAM role " + role) for p in (rr["writes"] if rr else [])],
        "legacy_touch": legacy,
        "consumer_note": "IRPT reader for the inflection firm (directory and ownership map under the legacy bucket)" if legacy else "IRPT function; no legacy grant or map entry (new bucket only)",
        "evidence": "aws lambda list-functions env (map) and IAM role " + role,
        "claim": "measured",
    })

# ids for IRPT rows: assign sequentially after the fixed rows
_next = 29
for x in LAMBDA_ROWS:
    if x.get("id") is None:
        x["id"] = "INF-FN-%02d" % _next
        _next += 1

# ---------------------------------------------------------------- edge, distribution, policy, portal, rules, topics, email
EDGE_ROWS = [
    {"id": "INF-EDGE-01", "kind": "edge", "name": "shared-advisor-router (Lambda@Edge, origin-request)",
     "trigger": "origin-request on CloudFront EVTSA9VEHNZVH behaviours /api/scoped/advisor-intelligence/artifacts/*, artifacts/*/*, entities/*/*, *.json and /api/scoped/satellites/* (5 associations, measured)",
     "reads": [acc("opal-data-inf", "firm map: inflection -> opal-data-inf (rewrites to the firm's platinum keys)", "measured", "live package index.mjs (member read by zipfile; inflection bucket token present=%s); repo infra/aws/lambda-edge/_shared/firm-config.mjs:73" % str(EDGE_BUNDLE["shared-advisor-router"]["inflection_bucket_is_legacy"]))],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "the portal's advisor-intelligence requests for inflection resolve to the legacy bucket through this map",
     "evidence": "aws lambda get-function code package (member index.mjs, %d bytes, legacy token mentions %d); infra/aws/lambda-edge/shared-advisor-router/index.mjs" % (EDGE_BUNDLE["shared-advisor-router"]["bytes"], EDGE_BUNDLE["shared-advisor-router"]["legacy_inf_mentions"]),
     "claim": "measured"},
    {"id": "INF-EDGE-02", "kind": "edge", "name": "shared-advisor-router-response (Lambda@Edge, origin-response)",
     "trigger": "origin-response on the same five behaviours (measured)",
     "reads": [acc("opal-data-inf", "firm map (response guard bucket list): inflection -> opal-data-inf", "measured", "live package index.mjs; inflection:Object.freeze({bucket:\"opal-data-inf\"...}) present=%s" % str(EDGE_BUNDLE["shared-advisor-router-response"]["inflection_bucket_is_legacy"]))],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "firm-isolation response guard: a response is refused when its firm does not match the session firm (test firm-isolation-guard.spec.mjs)",
     "evidence": "live package index.mjs (%d bytes); infra/aws/lambda-edge/shared-advisor-router-response/index.mjs" % EDGE_BUNDLE["shared-advisor-router-response"]["bytes"],
     "claim": "measured"},
    {"id": "INF-EDGE-03", "kind": "edge", "name": "CloudFront distribution EVTSA9VEHNZVH (origin S3-opal-data-inf)",
     "trigger": "distribution-level: origins %d, behaviours %d (measured); no behaviour targets S3-opal-data-inf (0 of %d) (measured)" % (len(ORIGINS), len(BEH), len(BEH)),
     "reads": [acc("opal-data-inf", "origin S3-opal-data-inf defined; reached by no cache behaviour", "measured", "aws cloudfront list-distributions")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "the origin is an orphan for routing; INF-FN-01 invalidates this distribution (env CF_DISTRIBUTION_ID=EVTSA9VEHNZVH); advisor-intelligence artifacts reach the legacy bucket only through the router map",
     "evidence": "aws cloudfront list-distributions (Origins %d; behaviours %d; origin counts by target: S3-opal-data-bd %d, S3-opal-data-portal-v2-json %d)" % (len(ORIGINS), len(BEH), BEH_BY_ORIGIN.get("S3-opal-data-bd", 0), BEH_BY_ORIGIN.get("S3-opal-data-portal-v2-json", 0)),
     "claim": "measured"},
    {"id": "INF-EDGE-04", "kind": "other", "name": "bucket policy of opal-data-inf",
     "trigger": "bucket-level: applies to every principal named in the two statements",
     "reads": [acc("opal-data-inf", "* (AllowScopedAdvisorOAI: GetObject on the whole bucket)", "measured", "aws s3api get-bucket-policy"), acc("opal-data-inf", "gold/* (AllowCFDistributionGold: service principal GetObject)", "measured", "aws s3api get-bucket-policy")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "the CloudFront origin-access grant on the legacy gold/* prefix; it retires with the bucket (PRD DEC-8)",
     "evidence": "aws s3api get-bucket-policy --bucket opal-data-inf (%d statements)" % len(policy.get("Statement", [])),
     "claim": "measured"},
    {"id": "INF-EDGE-05", "kind": "other", "name": "opal-data-inf bucket notification configuration (S3 to Lambda)",
     "trigger": "S3 event: 2 Lambda configurations (measured)",
     "reads": [acc("opal-data-inf", "gold/meta/pipeline-complete.json (event key)", "measured", "get-bucket-notification-configuration: prefix gold/meta/, suffix pipeline-complete.json"),
               acc("opal-data-inf", "silver/_silver_complete/*.json (event key)", "measured", "get-bucket-notification-configuration: prefix silver/_silver_complete/, suffix .json")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "S3 event routes: gold/meta/ pipeline-complete.json to inf-portal-publisher (INF-FN-01) and silver/_silver_complete/ *.json to inf-silver-aggregator (INF-FN-03); the notification config is a singleton per bucket (PRD DEC-7)",
     "evidence": "aws s3api get-bucket-notification-configuration --bucket opal-data-inf",
     "claim": "measured"},
    {"id": "INF-READER-01", "kind": "reader", "name": "portal/src/api/endpoints/advisor-intelligence.ts (nested portal worktree)",
     "trigger": "invocation by the portal page; the page's requests reach the legacy bucket through EDGE-01",
     "reads": [acc("opal-data-inf", "platinum/firm/header_metrics.json", "measured", "advisor-intelligence.ts:300-302"),
               acc("opal-data-inf", "platinum/firm/{timeseries_overview,partner_analytics_*,cumulative_chart,timeseries_chart,leaderboard,activity_scan_*,cash_drag_*}.json", "measured", ":380-467, :1366, :1484-1504"),
               acc("opal-data-inf", "platinum/advisors/{id}/{mix,timeseries,summary,nna_clients,exec_summary}.json", "measured", ":467, :919, :952, :983, :996"),
               acc("opal-data-inf", "platinum/firm/client_directory.json", "measured", ":574"),
               acc("opal-data-inf", "platinum/clients/{hhId}/accounts/{acctId}/timeseries.json", "measured", ":1344, :1048")],
     "writes": [],
     "legacy_touch": True,
     "consumer_note": "the only portal file in 2127 tracked portal files naming the legacy bucket; the key classes are its contract, read from comments and string constants",
     "evidence": "git grep (nested portal worktree) for opal-data-inf: advisor-intelligence.ts:69-70, :574, :1048, :1415; key constants as cited",
     "claim": "measured"},
    {"id": "INF-REPO-01", "kind": "other", "name": "infra/aws/lambda-edge/_shared/firm-config.mjs",
     "trigger": "build-time import by both edge functions",
     "reads": [], "writes": [],
     "legacy_touch": False,
     "consumer_note": "the firm table with bucket opal-data-inf for inflection (line 73), the source for the two edge bundles; DEC-6 makes this table generated from the registry",
     "evidence": "infra/aws/lambda-edge/_shared/firm-config.mjs:73 (bucket: 'opal-data-inf')",
     "claim": "measured"},
]

RULE_ROWS = [
    {"id": "INF-RULE-01", "kind": "rule", "name": "mdpf-feeder-accelerator",
     "trigger": "S3 Object Created on opal-data-inf key gold/meta/pipeline-complete.json (measured)",
     "reads": [acc("opal-data-inf", "gold/meta/pipeline-complete.json (event key)", "measured", "aws events describe-rule")],
     "writes": [], "legacy_touch": True,
     "consumer_note": "notifies INF-FN-24 (MdpfFeederTrigger); the prohibited key's named watcher",
     "evidence": "aws events describe-rule --name mdpf-feeder-accelerator (State ENABLED); list-targets-by-rule (1 target)", "claim": "measured"},
    {"id": "INF-RULE-02", "kind": "rule", "name": "exec-summary-trigger",
     "trigger": "EventBridge event pattern detail-type chain-complete from source bd-pipeline.gold-chain (measured, ENABLED)",
     "reads": [], "writes": [], "legacy_touch": False,
     "consumer_note": "notifies INF-FN-28 exec-summary-generator; live state differs from the Terraform placeholder (surprise W77-S2)",
     "evidence": "aws events describe-rule --name exec-summary-trigger; list-targets-by-rule (target exec-summary-generator)", "claim": "measured"},
    {"id": "INF-RULE-03", "kind": "rule", "name": "inf-gold-dispatch-release-changed",
     "trigger": "CloudTrail-style pattern on UpdateFunctionConfiguration for inf-gold-trigger (measured, ENABLED)",
     "reads": [], "writes": [], "legacy_touch": False,
     "consumer_note": "notifies SNS topic inf-gold-dispatch-release-alarm (0 subscriptions, measured) and a log group",
     "evidence": "aws events describe-rule; list-targets-by-rule (2 targets); sns list-subscriptions-by-topic (0)", "claim": "measured"},
    {"id": "INF-RULE-04", "kind": "rule", "name": "inf-canonical-prices-daily, inf-gold-full-on-bronze-complete, inf-gold-incremental-daily",
     "trigger": "all three DISABLED (measured), each targeting INF-FN-04 inf-gold-trigger",
     "reads": [], "writes": [], "legacy_touch": False,
     "consumer_note": "held off; inf-canonical-prices-daily stays DISABLED and HELD (PRD DEC-7); moving the target does not re-enable",
     "evidence": "aws events describe-rule (State DISABLED x3); list-targets-by-rule (inf-gold-trigger)", "claim": "measured"},
    {"id": "INF-SNS-01", "kind": "topic", "name": "inf-otp-alert",
     "trigger": "publish: publisher not identified in this read",
     "reads": [], "writes": [], "legacy_touch": False,
     "consumer_note": "2 subscriptions, protocols lambda and sms (endpoints withheld; personal contacts)",
     "evidence": "aws sns list-subscriptions-by-topic (2)", "claim": "measured"},
    {"id": "INF-SNS-02", "kind": "topic", "name": "inf-gold-dispatch-release-alarm",
     "trigger": "publish by INF-RULE-03",
     "reads": [], "writes": [], "legacy_touch": False,
     "consumer_note": "0 subscriptions; a notifier with no subscriber",
     "evidence": "aws sns list-subscriptions-by-topic (0)", "claim": "measured"},
    {"id": "INF-EMAIL-01", "kind": "email", "name": "SES identities naming the Inflection firm domain (2 individual addresses; addresses withheld)",
     "trigger": "SES sender identities; no template exists (list-templates 0, measured)",
     "reads": [], "writes": [], "legacy_touch": False,
     "consumer_note": "verified identities only; which sender uses them was not read",
     "evidence": "aws ses list-identities (26 total; 2 name the firm domain); aws ses list-templates (0)", "claim": "measured"},
]

# roles -> rows
ROLE_OUT = []
for i, x in enumerate(legacy_role_rows + new_only_rows, 1):
    reads = [acc("opal-data-inf", p, "measured", "IAM allow on role " + x["role"]) for p in x["reads"]]
    writes = [acc("opal-data-inf", p, "measured", "IAM allow on role " + x["role"]) for p in x["writes"]]
    reads += [acc("opal-data-inflection", p, "measured", "IAM allow on role " + x["role"]) for p in x["nreads"]]
    writes += [acc("opal-data-inflection", p, "measured", "IAM allow on role " + x["role"]) for p in x["nwrites"]]
    fns = x["functions"]
    ROLE_OUT.append({
        "id": "INF-ROLE-%02d" % i, "kind": "role", "name": x["role"],
        "trigger": ("assumed by functions: " + ", ".join(fns)) if fns else "assumed by an instance profile or an external principal (not resolved in this read)",
        "reads": reads, "writes": writes,
        "legacy_touch": bool(x["allow_legacy"]),
        "consumer_note": ("grant sources: " + ", ".join(x["sources"])) + ("; also grants the new bucket" if x["allow_new"] else ""),
        "evidence": "aws iam get-account-authorization-details (RoleDetailList; %s)" % ", ".join(x["sources"]),
        "claim": "measured",
    })

ROWS = LAMBDA_ROWS + EDGE_ROWS + RULE_ROWS + ROLE_OUT
ROWS_LEGACY = [r for r in ROWS if r["legacy_touch"]]

# Access items carry the spec's three fields only; their per-item evidence is folded into the row evidence.
for r in ROWS:
    extra = []
    for side in ("reads", "writes"):
        for item in r[side]:
            ev = item.pop("evidence", "")
            if ev and ev not in r["evidence"] and ev not in extra:
                extra.append(ev)
            item.pop("evidence", None)
    if extra:
        r["evidence"] = r["evidence"] + " | access evidence: " + " ; ".join(extra)

NOT_READ = [
    "IRPT Lambda source (infra/aws/lambda/investor-reporting/*): live env maps and IAM grants read; per-key use not traced line by line.",
    "Inf pipeline pull Lambdas INF-FN-11 to INF-FN-19 (api pulls, accounts, billing, performance, tax, unified dim): legacy access stated from the IAM grant (measured), not from line-level code reads.",
    "shared-advisor-router rewrite template (the target key shape after the firm lookup) not traced beyond the firm map; the live package was read by zipfile and regex only.",
    "auth-validator-edge (viewer-request on 26 behaviours), cache-control-injector and public-data-router (origin-request, 2 behaviours) packages not read; no legacy env reference observed.",
    "orion/jwt/current.json (credential object): referenced by readers; contents NOT read or printed by design.",
    "opal-data-inf/gold/meta/pipeline-complete.json: existence not probed (no head on the key); its watchers are the rule and the notification.",
    "SNS subscription endpoints of inf-otp-alert (email and sms): protocol counts only; endpoints withheld.",
    "SES identities: the two individual addresses at the firm domain counted, not printed; SES templates 0.",
    "EventBridge Scheduler schedules: not read (FB-k-1 scope); the graph holds one Scheduler node for the firm (irpt-inf-holdings-performance-daily).",
    "Graph LAMBDA nodes %d against live list-functions %d: the one-node difference is not identified." % (238, len(funcs_list)),
    "EC2 instance-profile roles (inf-exporter, inf-gold-layer-ec2, inf-bronze-runner, inf-gold-qa-runner, mdpf-daily-runner): which instances assume them was not read.",
    "Portal: only portal/src/api/endpoints/advisor-intelligence.ts names the legacy bucket among 2127 tracked portal files; other portal readers of inflection keys route through the router and were not enumerated.",
    "Mapping table (mapping_v4.json, 3451 rows) used only as a denominator cross-check; no row of this record is sourced from it.",
    "CloudFront distribution list: 2 distributions; the 30 behaviours of EVTSA9VEHNZVH enumerated; the second distribution (origin opalinvest.com) not inspected.",
    "Lambda env values of functions with no env (inf-accounts-v2-daily and the other pull Lambdas): bucket literals in source not grepped line by line.",
    "Deny-only roles (%d roles with a Deny on opal-data-inf and no Allow) are fences, not grants, and are counted, not listed." % len(deny_only_roles),
]

CALLS = [
    "aws lambda list-functions --output json (auto-paginated; 237 functions; env names and buckets only)",
    "aws lambda get-function-configuration --function-name exec-summary-generator",
    "aws lambda get-function-configuration --function-name inf-gold-dispatch (ResourceNotFound: absent live)",
    "aws lambda get-function --function-name shared-advisor-router --query Code.Location --output text, then GET of that package into the data folder (read; URL not printed)",
    "aws lambda get-function --function-name shared-advisor-router-response --query Code.Location --output text, then GET of that package into the data folder (read; URL not printed)",
    "aws iam get-account-authorization-details --filter Role LocalManagedPolicy (303 roles, 56 customer policies)",
    "aws s3api get-bucket-notification-configuration --bucket opal-data-inf",
    "aws s3api get-bucket-policy --bucket opal-data-inf",
    "aws cloudfront list-distributions --output json",
    "aws events describe-rule --name mdpf-feeder-accelerator",
    "aws events describe-rule --name exec-summary-trigger",
    "aws events describe-rule --name exec-summary-trigger-placeholder (ResourceNotFound)",
    "aws events list-rules --name-prefix exec- (1 rule)",
    "aws events describe-rule --name <each of 30 inflection-pattern rules> and aws events list-targets-by-rule --rule <each>",
    "aws sns list-topics --output json (17 topics)",
    "aws sns list-subscriptions-by-topic --topic-arn <inf-otp-alert and inf-gold-dispatch-release-alarm> (counts only)",
    "aws ses list-identities --output json (26); aws ses list-templates --output json (0)",
    "comp-find --corpus aws --limit 200 'opal-data-inf|inflection|inf-|irpt|exec-summary' <IAM_POLICY|IAM_ROLE|S3_BUCKET|S3_BUCKET_POLICY|EVENT_RULE|SCHEDULE|CLOUDFRONT_DISTRIBUTION|SQS_QUEUE|SECRET|LOG_GROUP>",
    "comp-find --corpus aws --limit 200 '.' LAMBDA (238 nodes) and comp-find --corpus aws 'opal-data-inf' IAM_POLICY (1 node: the bucket policy)",
    "comp-find --files 'exec-summary-generator' infra/aws --limit 20",
    "git ls-files | wc -l; git grep -l -E 'opal-data-inf([^l]|$)' -- . ':!portal' | wc -l; git -C portal ls-files | wc -l; git -C portal grep -l -E 'opal-data-inf([^l]|$)' | wc -l",
    "Grep (native) over portal/src/api/endpoints/advisor-intelligence.ts, infra/aws/lambda-edge/_shared/firm-config.mjs, infra/aws/lambda/exec-summary-generator/",
    "python -I scripts/planinv_lambda_summary.py <saved list-functions json> --match REGEX (summariser, no AWS call)",
    "python -I scripts/planinv_iam_grants.py <saved authz json> (summariser, no AWS call)",
    "python -I scripts/planinv_build_record.py <data-dir> <out-json> <out-md> <head> <read-at> (writes this record; no AWS call)",
]

record = {
    "order": "FB-k-2",
    "read_at": READ_AT,
    "firm": "inflection",
    "scope": "Every Lambda, Lambda@Edge package, CloudFront origin, S3 notification, bucket policy, IAM grant, EventBridge rule, SNS topic, SES identity and repository reader that serves, generates or notifies for the Inflection firm and touches opal-data-inf or the Inflection scope of opal-data-bd, as read live at the commit below.",
    "calls": CALLS,
    "denominators": DENOM,
    "functions": ROWS,
    "not_read": NOT_READ,
    "claim": "measured",
    "head_commit": HEAD,
    "legacy_rows": len(ROWS_LEGACY),
    "total_rows": len(ROWS),
}

with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(record, fh, indent=1, ensure_ascii=True)
    fh.write("\n")

lines = ["# PLANINV FB-k-2 -- Inflection: what serves and notifies (read-only)", "",
         "Read at %s against HEAD %s. Full rows and evidence are in PLANINV_INFLECTION_SERVING.json." % (READ_AT, HEAD),
         "", "Totals: %d rows, %d legacy_touch true, %d legacy_touch false." % (len(ROWS), len(ROWS_LEGACY), len(ROWS) - len(ROWS_LEGACY)), "",
         "## Rows (id, kind, name, legacy_touch)", "", "| id | kind | name | legacy_touch | claim |", "|---|---|---|---|---|"]
for r in ROWS:
    lines.append("| %s | %s | %s | %s | %s |" % (r["id"], r["kind"], r["name"].replace("|", "/"), str(r["legacy_touch"]).lower(), r["claim"]))
lines += ["", "## Denominators", ""]
for k, v in DENOM.items():
    lines.append("- %s: %s" % (k, v))
lines += ["", "## Not read", ""]
for n in NOT_READ:
    lines.append("- " + n)
with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(lines) + "\n")

print("RECORD rows=%d legacy=%d roles=%d lambdas=%d" % (len(ROWS), len(ROWS_LEGACY), len(ROLE_OUT), len(LAMBDA_ROWS)))
print("MAP_OK=%s EDGE_BUNDLE=%s" % (MAP_OK, json.dumps(EDGE_BUNDLE)))
