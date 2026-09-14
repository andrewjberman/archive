"""census.py -- EN-t-1 Terraform-label census (0.9.0_WK_LGIC_ENFORCE~3). Scratch instrument; output is the deliverable.

Applies org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md by its written steps (G1, G2, G3, grammar, G6),
hand-coded, because lib/opal_naming.py grade() is not at the base. `python census.py selftest` grades the rule's own
worked cases and prints every disagreement (the control on this hand-coding). `python census.py build` writes the census.
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tfscan  # noqa: E402

RULE = "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md"
SCHEMA = "org/standards/NAMING_SCHEMA.json"
OUT = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/TF_LABEL_CENSUS.md"

S = json.load(open(SCHEMA, encoding="utf-8"))
KINDS = S["kind"]["by_type"]
NOT_GRADED = {k for k, v in S["types_not_graded_by_kind"].items() if v.startswith("NOT GRADED")}
DOMAIN = set(KINDS) | set(S["types_not_graded_by_kind"])

# ---- V vocabularies, from the rule's section V (copied as written)
V1_PRODUCT = {"mdpf", "etfs", "irpt", "advi", "yang", "news", "astn", "amgt", "trade"}
V1_VENDOR = {"schwab", "blackdiamond", "orion", "eclipse", "smartx", "pathfinder", "trueshares", "ycharts", "fred", "seeking-alpha"}
V1 = V1_PRODUCT | V1_VENDOR
V2 = {"estate", "globgrph", "semantic", "agentbus", "cmtque", "opsec", "firmsep", "consolidation", "canonical", "gldinc", "quartz",
      "find", "harvest", "imo"}
FIRM_LONG_SHORT = {"49financial": "49f", "inflection": "inf", "cottonwood": "cot", "demo": "demo"}
FIRM_SHORT_LONG = {v: k for k, v in FIRM_LONG_SHORT.items()}
FIRM_TOKENS = set(FIRM_LONG_SHORT) | set(FIRM_SHORT_LONG)
MASTERS = {"08242234", "08335338"}
SCOPE_TOKENS = FIRM_TOKENS | MASTERS | {"global", "mockadv"}
V3_OTHER = {"wsb", "wsd", "historical", "daily", "weekly", "monthly", "hourly", "exec", "infrastructure", "market", "etf", "ec2",
            "cloudfront", "portfolio", "cross", "s3", "cloudwatch", "invoke", "secretsmanager", "lambda", "kms", "secrets"}
CADENCES = {"daily", "weekly", "monthly", "hourly"}
TIERS = ["bronze", "silver", "gold", "platinum", "state", "code"]
ACCT = "313476888478"


class Raise(Exception):
    pass


# ---------------------------------------------------------------- G3 tokeniser
def camel_split(piece):
    p = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", piece)
    p = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", p)
    return [x.lower() for x in p.split() if x]


def tokens_of(s):
    """N1-N3: split on - _ . and camel boundaries, lowercase. Rejects characters outside [A-Za-z0-9-_.]."""
    if not s or re.search(r"[^A-Za-z0-9._-]", s):
        raise Raise("G3 N1: characters outside letters, digits and - _ . (%r)" % s)
    out = []
    for piece in re.split(r"[-_.]", s):
        if piece:
            out.extend(camel_split(piece))
    # 'seeking' 'alpha' is one V1 token (V1 row fred / seeking-alpha)
    merged, i = [], 0
    while i < len(out):
        if out[i] == "seeking" and i + 1 < len(out) and out[i + 1] == "alpha":
            merged.append("seeking-alpha")
            i += 2
        else:
            merged.append(out[i])
            i += 1
    return merged


def drop_generated(toks):
    """N4: a final token of 14+ digits fills no slot."""
    if toks and re.fullmatch(r"\d{14,}", toks[-1]):
        return toks[:-1], True
    return toks, False


# ---------------------------------------------------------------- R3 bd reading
def bd_reading(toks, i):
    nb = [toks[j] for j in (i - 1, i + 1) if 0 <= j < len(toks)]
    return "vendor" if any(t in FIRM_TOKENS for t in nb) else "firm"


def is_scope(toks, i):
    t = toks[i]
    return t in SCOPE_TOKENS or (t == "bd" and bd_reading(toks, i) == "firm")


def scope_short(toks, i):
    t = toks[i]
    if t == "bd" or t == "mockadv":
        return "49f"
    return FIRM_LONG_SHORT.get(t, t)


def scope_long(t):
    if t in ("bd", "mockadv"):
        return "49financial"
    return FIRM_SHORT_LONG.get(t, t)


# ---------------------------------------------------------------- R: resource grammar
def resource_canonical(toks, ntype):
    """R1-R9 on normalised tokens. Returns (canonical, why_steps)."""
    why = []
    if not toks:
        raise Raise("G3: no tokens")
    n = len(toks)
    sys_idx, system = None, None
    t1 = toks[0]
    vendor_bd = lambda i: toks[i] == "bd" and bd_reading(toks, i) == "vendor"  # noqa: E731
    if (t1 in V1) or vendor_bd(0):
        sys_idx, system = 0, ("blackdiamond" if t1 == "bd" else t1)
        why.append("R1.a system %s" % system)
    elif t1 == "opal":
        t2 = toks[1] if n > 1 else None
        if t2 is not None and (t2 in V1 or vendor_bd(1)):
            system = "blackdiamond" if t2 == "bd" else t2
            toks = toks[1:]
            n = len(toks)
            sys_idx = 0
            why.append("R2 opal is a null prefix before V1 %s" % system)
        elif t2 in V2:
            raise Raise("R2: t2 %s is in V2 (row LGIC_NAMING-W1-S2)" % t2)
        else:
            sys_idx, system = 0, "opal"
            why.append("R2 system opal")
    elif t1 in V2:
        raise Raise("R1.c: t1 %s is in V2 (row LGIC_NAMING-W1-S2)" % t1)
    elif t1 in V3_OTHER or is_scope(toks, 0) or (ntype == "LAMBDA_LAYER"):
        label = "R1.e library-first layer" if (ntype == "LAMBDA_LAYER" and not (t1 in V3_OTHER or is_scope(toks, 0))) else "R1.d t1 %s is V3" % t1
        for j in range(1, n):
            if toks[j] in V2:
                raise Raise("R1.d: V2 token %s before any V1 token" % toks[j])
            if toks[j] in V1 or vendor_bd(j):
                sys_idx, system = j, ("blackdiamond" if toks[j] == "bd" else toks[j])
                break
        if system is None:
            system = "{system}"
            why.append(label + "; no later V1 token, {system}")
        else:
            why.append(label + "; system %s" % system)
    else:
        raise Raise("R1.f: t1 %s is in no vocabulary" % t1)
    # R4 scope
    scope_idx = [i for i in range(n) if i != sys_idx and is_scope(toks, i)]
    scopes = {scope_short(toks, i) for i in scope_idx}
    if len(scopes) > 1:
        raise Raise("R4: two different scopes %s" % sorted(scopes))
    scope = scopes.pop() if scopes else None
    if scope:
        why.append("R4 scope %s" % scope)
    # R5 function: tokens before the system (not scope) then after
    before = [toks[i] for i in range(0, sys_idx if sys_idx is not None else 0) if i not in scope_idx]
    after = [toks[i] for i in range((sys_idx + 1) if sys_idx is not None else 0, n) if i not in scope_idx]
    if sys_idx is None:  # {system}: every non-scope token is function
        before, after = [], [toks[i] for i in range(n) if i not in scope_idx]
    func = before + after
    # R6 / R7 / R8 last slot
    if ntype in ("EVENT_RULE", "SCHEDULE"):
        if func and (func[-1] in CADENCES or ("on" in func[:-1])):
            why.append("R7 cadence last")
        else:
            cad = [i for i, t in enumerate(func) if t in CADENCES]
            if cad:
                c = func.pop(cad[0])
                func.append(c)
                why.append("R7 cadence %s moved to end" % c)
            else:
                func.append("{cadence}")
                why.append("R7 {cadence} appended")
    else:
        kinds = KINDS[ntype]
        if func and func[-1] in kinds:
            why.append("R6 last %s is a kind" % func[-1])
        else:
            func.append(kinds[0])
            why.append("R6 %s appended" % kinds[0])
    parts = [system] + ([scope] if scope else []) + func
    return "-".join(parts), why


def alias_substitute(name, bucket_or_key=False):
    """V-4: replace alias tokens in place, nothing else."""
    parts = re.split(r"([-/])", name)
    toks = [p for p in parts if p not in ("-", "/")]
    out, ti = [], 0
    for p in parts:
        if p in ("-", "/"):
            out.append(p)
            continue
        t = p
        if p == "bd":
            if bucket_or_key:
                t = "49financial"
            else:
                t = "blackdiamond" if bd_reading(toks, ti) == "vendor" else "49f"
        elif p == "mockadv":
            t = "49financial" if bucket_or_key else "49f"
        elif not bucket_or_key and p in FIRM_LONG_SHORT:
            t = FIRM_LONG_SHORT[p]
        elif bucket_or_key and p in FIRM_SHORT_LONG:
            t = FIRM_SHORT_LONG[p]
        out.append(t)
        ti += 1
    return "".join(out)


def g6(name, canon, bucket_or_key=False):
    if re.search(r"\{(system|source|scope|tier|cadence|entity)\}", canon):
        return "OUT-OF-PATTERN", "V-2"
    if canon == name:
        return "CONFORMANT", "V-3"
    if alias_substitute(name, bucket_or_key) == canon:
        return "ALIAS", "V-4"
    return "OUT-OF-PATTERN", "V-5"


def grade_resource(name, ntype):
    affix = ""
    base = name
    if ntype == "SQS_QUEUE" and base.endswith(".fifo"):
        base, affix = base[:-5], ".fifo"
    if ntype == "IAM_POLICY" and "#" in base:
        x, _, rest = base.partition("#")
        v, c, why = grade_bucket(x) if x.startswith("opal-") else grade_resource(x, "IAM_POLICY")
        return v, c + "#" + rest, ["R8 resource policy"] + why
    toks = tokens_of(base)
    toks, gen = drop_generated(toks)
    canon, why = resource_canonical(toks, ntype)
    if gen:
        why.insert(0, "N4 generated suffix dropped")
    canon += affix
    v, step = g6(name, canon)
    return v, canon, why + [step]


# ---------------------------------------------------------------- S: secrets
def grade_secret(name):
    segs = [s for s in name.split("/")]
    if any(s == "" for s in segs):
        raise Raise("S1: empty segment in %r" % name)
    seg_toks = [tokens_of(s) for s in segs]
    why = []
    # system slot: first token of segment 1
    t1 = seg_toks[0][0]
    sys_pos, system = None, None

    def vbd(si, ti):
        st = seg_toks[si]
        return st[ti] == "bd" and bd_reading(st, ti) == "vendor"
    if t1 in V1 or vbd(0, 0):
        sys_pos, system = (0, 0), ("blackdiamond" if t1 == "bd" else t1)
    elif t1 == "opal":
        t2 = seg_toks[0][1] if len(seg_toks[0]) > 1 else (seg_toks[1][0] if len(seg_toks) > 1 else None)
        if t2 in V1:
            system = t2
            sys_pos = (0, 1) if len(seg_toks[0]) > 1 else (1, 0)
            seg_toks[0] = seg_toks[0][1:] if len(seg_toks[0]) > 1 else seg_toks[0]
            if sys_pos == (0, 1):
                sys_pos = (0, 0)
            else:
                seg_toks[0] = []
        elif t2 in V2:
            raise Raise("R2 (via S2): t2 %s is in V2" % t2)
        else:
            sys_pos, system = (0, 0), "opal"
    elif t1 in V2:
        raise Raise("R1.c (via S2): t1 %s is in V2" % t1)
    elif t1 in V3_OTHER or t1 in SCOPE_TOKENS or t1 == "bd":
        for si in range(1, len(seg_toks)):
            f = seg_toks[si][0] if seg_toks[si] else None
            if f in V2:
                raise Raise("R1.d (via S2): V2 token %s before any V1 token" % f)
            if f in V1:
                sys_pos, system = (si, 0), f
                break
        if system is None:
            system = "{system}"
    else:
        raise Raise("R1.f (via S2): t1 %s is in no vocabulary" % t1)
    why.append("S2 system %s" % system)
    # remove the system token
    if sys_pos is not None and seg_toks[sys_pos[0]]:
        seg_toks[sys_pos[0]] = seg_toks[sys_pos[0]][:sys_pos[1]] + seg_toks[sys_pos[0]][sys_pos[1] + 1:]
    # scope: any V4 token anywhere (whole token)
    scopes = set()
    for si, st in enumerate(seg_toks):
        keep = []
        for ti, t in enumerate(st):
            if t in SCOPE_TOKENS or (t == "bd" and bd_reading(st, ti) == "firm"):
                scopes.add("49f" if t in ("bd", "mockadv") else FIRM_LONG_SHORT.get(t, t))
            else:
                keep.append(t)
        seg_toks[si] = keep
    if len(scopes) > 1:
        raise Raise("R4 (via S3): two different scopes %s" % sorted(scopes))
    scope = scopes.pop() if scopes else None
    why.append("S3 scope %s" % (scope or "omitted"))
    purpose = [ "-".join(st) for st in seg_toks if st]
    canon = "/".join([system] + ([scope] if scope else []) + purpose)
    v, step = g6(name, canon)
    return v, canon, why + ["S4 purpose %s" % "/".join(purpose), step]


# ---------------------------------------------------------------- L: log groups
L_SERVICE = {"lambda": "LAMBDA", "codebuild": "CODEBUILD_PROJECT", "stepfunctions": "STATE_MACHINE", "events": "EVENT_RULE",
             "ecs": "ECS_TASK_DEFINITION"}


def grade_log_group(name):
    if not name.startswith("/"):
        raise Raise("G2.3: log group not beginning / is AWS-fixed")
    if name.startswith("/aws/ecs/containerinsights/"):
        raise Raise("G2.3: /aws/ecs/containerinsights/ is AWS-fixed")
    segs = name.split("/")[1:]
    if segs and segs[0] == "aws":
        if len(segs) >= 3 and segs[1] == "vendedlogs" and segs[2] == "states":
            prefix, ntype, rest = "/aws/vendedlogs/states/", "STATE_MACHINE", segs[3:]
        elif len(segs) >= 2 and segs[1] in L_SERVICE:
            prefix, ntype, rest = "/aws/%s/" % segs[1], L_SERVICE[segs[1]], segs[2:]
        else:
            raise Raise("L2: service %r gives no type" % "/".join(segs[1:3]))
        l4 = False
    else:
        if not segs or segs[0] not in L_SERVICE:
            raise Raise("L4/L2: service %r gives no type" % (segs[0] if segs else ""))
        prefix, ntype, rest, l4 = "/aws/%s/" % segs[0], L_SERVICE[segs[0]], segs[1:], True
    rest_s = "-".join(rest)
    edge = ""
    if rest_s.startswith("us-east-1."):
        edge, rest_s = "us-east-1.", rest_s[len("us-east-1."):]
    if not rest_s:
        raise Raise("L3: no resource name after the service")
    v, c, why = grade_resource(rest_s, ntype)
    canon = prefix + edge + c
    if l4 and v in ("CONFORMANT", "ALIAS"):
        v = "OUT-OF-PATTERN"
        why = why + ["L4 never CONFORMANT"]
    return v, canon, ["L3 %s graded as %s: %s" % (rest_s, ntype, v)] + why


# ---------------------------------------------------------------- B: buckets
def grade_bucket(name):
    """G3 first (the rule's step order): the B steps read the normalised form; G6 compares the name as written."""
    norm = "-".join(tokens_of(name))
    if norm in S["bucket"]["standing_shared"]:
        v, step = g6(name, norm, bucket_or_key=True)
        return v, norm, ["B1 standing shared", step]
    if norm.startswith("opal-data-"):
        toks = tokens_of(norm[len("opal-data-"):])
        f = toks[0]
        more = len(toks) > 1
        if f in FIRM_LONG_SHORT or f in MASTERS or f == "global" or f in V1_PRODUCT:
            canon = "opal-data-" + f
            why = ["B2 scope key %s" % f]
        elif f in FIRM_SHORT_LONG or f in ("bd", "mockadv"):
            canon = "opal-data-" + scope_long(f)
            why = ["B2 short/alias %s -> %s" % (f, scope_long(f))]
        elif f in V1_VENDOR:
            canon = "opal-data-{scope}"
            why = ["B2 vendor %s is never a data bucket's scope" % f]
        elif f in V2:
            raise Raise("B2: first token %s is in V2" % f)
        else:
            raise Raise("B2: first token %s is in no vocabulary" % f)
        if more:
            why.append("B2 scope key followed by more tokens")
        v, step = g6(name, canon, bucket_or_key=True)
        return v, canon, why + [step]
    if norm.startswith("opal-"):
        toks = tokens_of(norm[len("opal-"):])
        if toks and toks[0] == ACCT:
            purpose, why = toks[1:], ["B3 account id second"]
        elif ACCT in toks:
            purpose, why = [t for t in toks if t != ACCT], ["B3 account id moves to second"]
        else:
            purpose, why = toks, ["B3 account id inserted"]
        canon = "-".join(["opal", ACCT] + purpose)
        v, step = g6(name, canon, bucket_or_key=True)
        return v, canon, why + [step]
    canon = "opal-%s-%s" % (ACCT, norm)
    return "OUT-OF-PATTERN", canon, ["B4 not opal-"]


# ---------------------------------------------------------------- K: keys (only what the tree carries)
def grade_key(name):
    base = name.split(" ", 1)[0]
    segs = base.split("/")
    s1 = segs[0]
    if s1 == "code" or s1 in TIERS:
        raise Raise("K5/K6: a tier-first or root code key needs the LIST walk; not hand-coded in this census (none expected)")
    if s1 not in V1:
        raise Raise("K1: segment 1 %r is neither a source nor a tier" % s1)
    out, why = [s1], ["K1 source-first %s" % s1]
    rest = segs[1:]
    if rest:
        sc = rest[0]
        if sc in FIRM_LONG_SHORT or sc in MASTERS or sc == "global" or sc in V1_PRODUCT:
            out.append(sc)
            rest = rest[1:]
        elif sc in FIRM_SHORT_LONG or sc in ("bd", "mockadv"):
            out.append(scope_long(sc))
            rest = rest[1:]
        else:
            out.append("{scope}")
    if rest:
        if rest[0] in TIERS:
            out.append(rest[0])
            rest = rest[1:]
        else:
            out.append("{tier}")
        if rest and rest[0] == "platinum":
            raise Raise("K4a: platinum membership needs the LIST; not hand-coded (none expected)")
    out += rest
    canon = "/".join(out)
    v, step = g6(base, canon, bucket_or_key=True)
    return v, canon, why + [step]


# ---------------------------------------------------------------- G1/G2 dispatch
def grade(name, ntype):
    """-> (verdict, canonical, why). verdict in CONFORMANT, ALIAS, OUT-OF-PATTERN, NOT-GRADED, RAISE."""
    try:
        if ntype not in DOMAIN:
            raise Raise("G1.1: %r is not one of the 33 node types" % ntype)
        if ntype in NOT_GRADED:
            return "NOT-GRADED", "", ["G1.2 %s is NOT GRADED" % ntype]
        if ntype == "SECURITY_GROUP" and name == "default":
            raise Raise("G2.1: default security group is AWS-fixed")
        if ntype in ("IAM_POLICY", "IAM_ROLE") and (name.startswith("AWS") or name.startswith("Amazon")):
            raise Raise("G2.2: AWS/Amazon prefix is AWS-fixed")
        if ntype == "SECRET":
            return grade_secret(name)
        if ntype == "LOG_GROUP":
            return grade_log_group(name)
        if ntype in ("S3_BUCKET", "S3_BUCKET_POLICY"):
            v, c, w = grade_bucket(name)
            return v, c, (["B5 graded as its bucket"] if ntype == "S3_BUCKET_POLICY" else []) + w
        if ntype == "S3Key":
            return grade_key(name)
        return grade_resource(name, ntype)
    except Raise as exc:
        return "RAISE", "", [str(exc)]


# ---------------------------------------------------------------- selftest against the rule's worked cases
def selftest():
    txt = open(RULE, encoding="utf-8").read().replace("\r\n", "\n")
    cases = json.loads(re.search(r"```json\n(.*?)\n```", txt, re.S).group(1))["worked_cases"]
    bad = 0
    skipped = 0
    for c in cases:
        if c["type"] == "S3Key" and (c["name"].split("/")[0] in TIERS or "platinum" in c["name"].split("/")[:3]):
            skipped += 1
            print("SKIP (K5/K6/K4a LIST walk not hand-coded): %s" % c["name"])
            continue
        v, canon, why = grade(c["name"], c["type"])
        want_v, want_c = c["verdict"], c.get("canonical_form", "")
        ok = v == want_v and (want_v in ("RAISE", "NOT-GRADED") or canon == want_c)
        if not ok:
            bad += 1
            print("DISAGREE %s (%s): rule=%s %s  mine=%s %s  %s" % (c["name"], c["type"], want_v, want_c, v, canon, why))
    print("WORKED CASES: %d  GRADED: %d  SKIPPED: %d  DISAGREE: %d" % (len(cases), len(cases) - skipped, skipped, bad))
    return bad


# ================================================================ the Terraform side (this census's reading)
# Terraform resource type -> (node_type, own-name attribute). The rule's domain (G1.1) is the 33 node types; a
# Terraform type is not one, so this map is the census's reading, stated in the prose and filed as a row.
TF_NODE = {
    "aws_lambda_function": ("LAMBDA", "function_name"),
    "aws_iam_role": ("IAM_ROLE", "name"),
    "aws_iam_policy": ("IAM_POLICY", "name"),
    "aws_iam_role_policy": ("IAM_POLICY", "name"),
    "aws_iam_user_policy": ("IAM_POLICY", "name"),
    "aws_iam_instance_profile": ("INSTANCE_PROFILE", "name"),
    "aws_security_group": ("SECURITY_GROUP", "name"),
    "aws_api_gateway_rest_api": ("API_GW", "name"),
    "aws_apigatewayv2_api": ("API_GW", "name"),
    "aws_dynamodb_table": ("DYNAMODB_TABLE", "name"),
    "aws_sqs_queue": ("SQS_QUEUE", "name"),
    "aws_sns_topic": ("SNS_TOPIC", "name"),
    "aws_cloudwatch_metric_alarm": ("CW_ALARM", "alarm_name"),
    "aws_lambda_layer_version": ("LAMBDA_LAYER", "layer_name"),
    "aws_instance": ("EC2_INSTANCE", "tags.Name"),
    "aws_codebuild_project": ("CODEBUILD_PROJECT", "name"),
    "aws_ssm_document": ("SSM_DOCUMENT", "name"),
    "aws_ecs_task_definition": ("ECS_TASK_DEFINITION", "family"),
    "aws_sfn_state_machine": ("STATE_MACHINE", "name"),
    "aws_lb": ("LOAD_BALANCER", "name"),
    "aws_ecs_cluster": ("ECS_CLUSTER", "name"),
    "aws_cloudwatch_event_rule": ("EVENT_RULE", "name"),
    "aws_scheduler_schedule": ("SCHEDULE", "name"),
    "aws_cloudwatch_log_group": ("LOG_GROUP", "name"),
    "aws_s3_bucket": ("S3_BUCKET", "bucket"),
    "aws_s3_bucket_policy": ("S3_BUCKET_POLICY", "bucket"),
    "aws_s3_object": ("S3Key", "key"),
    "aws_secretsmanager_secret": ("SECRET", "name"),
    "aws_iam_user": ("IAM_USER", "name"),
    "aws_route53_record": ("ROUTE53_RECORD", "name"),
    "aws_kms_key": ("KMS_KEY", None),
    "aws_cloudfront_distribution": ("CLOUDFRONT_DISTRIBUTION", None),
    "aws_vpc_endpoint": ("VPC_ENDPOINT", None),
    "aws_apigatewayv2_route": ("API_ROUTE", None),
}
# Terraform types that carry their OWN name but map to no node type: graded, and RAISE at G1.1.
TF_OWN_UNMAPPED = {
    "aws_ecr_repository": "name", "aws_cloudwatch_log_metric_filter": "name", "aws_glue_catalog_table": "name",
    "aws_wafv2_ip_set": "name", "aws_service_discovery_service": "name", "aws_ecs_service": "name",
    "aws_wafv2_web_acl": "name", "aws_glue_catalog_database": "name", "aws_cloudtrail": "name", "aws_ssm_parameter": "name",
    "aws_cloudwatch_log_subscription_filter": "name", "aws_cloudfront_cache_policy": "name",
    "aws_ses_event_destination": "name", "aws_ssm_activation": "name", "aws_s3_bucket_metric": "name",
    "aws_service_discovery_private_dns_namespace": "name", "aws_pipes_pipe": "name", "aws_apigatewayv2_stage": "name",
    "aws_lb_target_group": "name", "aws_athena_workgroup": "name", "aws_cloudfront_function": "name",
    "aws_cloudwatch_log_delivery_source": "name", "aws_cloudwatch_log_delivery_destination": "name",
    "aws_apigatewayv2_authorizer": "name", "aws_ses_configuration_set": "name", "aws_kms_alias": "name",
    "aws_api_gateway_stage": "stage_name", "aws_cloudwatch_dashboard": "dashboard_name",
    "aws_cur_report_definition": "report_name", "aws_cloudwatch_log_resource_policy": "policy_name",
}
ID_IS_NAME = {"aws_s3_bucket", "aws_iam_role", "aws_iam_instance_profile", "aws_cloudwatch_log_group", "aws_dynamodb_table",
              "aws_lambda_function"}
LIT = re.compile(r'"((?:[^"\\$%]|\\.|\$(?!\{)|%(?!\{)|\$\$\{)*)"')


def node_of(rtype):
    if rtype in TF_NODE:
        return TF_NODE[rtype][0]
    return None


def own_attr(rtype):
    if rtype in TF_NODE:
        return TF_NODE[rtype][1]
    return TF_OWN_UNMAPPED.get(rtype)


def unescape(s):
    return s.replace("$${", "${").replace('\\"', '"').replace("\\\\", "\\")


class Dir:
    def __init__(self):
        self.locals, self.vars, self.own = {}, {}, {}


def resolve(raw, d, depth=0):
    """-> (string or None, chain list, reason)."""
    if depth > 12:
        return None, [], "resolution depth exceeded"
    raw = raw.strip()
    m = LIT.fullmatch(raw)
    if m:
        return unescape(m.group(1)), [], ""
    m = re.fullmatch(r"(local|var)\.([A-Za-z_][A-Za-z0-9_-]*)", raw)
    if m:
        table = d.locals if m.group(1) == "local" else d.vars
        if m.group(2) not in table:
            return None, [], "%s has no %s in the same directory" % (raw, "literal local" if m.group(1) == "local" else "default")
        s, chain, why = resolve(table[m.group(2)], d, depth + 1)
        return s, [raw] + chain, why
    m = re.fullmatch(r"(aws_[a-z0-9_]+)\.([A-Za-z_][A-Za-z0-9_-]*)\.([a-z_]+)", raw)
    if m:
        rt, lb, at = m.groups()
        key = rt + "." + lb
        if key not in d.own or not (at == own_attr(rt) or (at == "id" and rt in ID_IS_NAME) or (at == "name" and own_attr(rt) == "name")):
            return None, [], "%s is not a same-directory resource name attribute" % raw
        s, chain, why = resolve(d.own[key], d, depth + 1)
        return s, [raw] + chain, why
    if raw.startswith('"') and raw.endswith('"') and ("${" in raw or "%{" in raw):
        body = raw[1:-1]
        if "%{" in body:
            return None, [], "template directive %{...}"
        out, chain, pos = [], [], 0
        for mm in re.finditer(r"(?<!\$)\$\{([^{}]*)\}", body):
            out.append(unescape(body[pos:mm.start()]))
            s, c, why = resolve(mm.group(1), d, depth + 1)
            if s is None:
                return None, [], why or ("${%s} not resolvable" % mm.group(1))
            out.append(s)
            chain += c
            pos = mm.end()
        rest = body[pos:]
        if "${" in rest.replace("$${", ""):
            return None, [], "nested interpolation"
        out.append(unescape(rest))
        return "".join(out), chain, ""
    return None, [], "expression %s is not a literal, a same-directory local/variable default, or a same-directory resource name" % raw[:80]


def tf_files():
    out = subprocess.run(["git", "ls-files", "infra/aws/terraform"], capture_output=True, text=True, check=True).stdout
    return sorted(f for f in out.splitlines() if f.endswith(".tf"))


def commented_heads(text, blocks):
    """resource heads a raw line regex sees that the scanner does not (inside /* */ comments)."""
    have = {b["line"] for b in blocks if b["kind"] == "resource"}
    out = []
    for m in re.finditer(r'(?m)^[ \t]*resource[ \t]+"([^"]+)"[ \t]+"([^"]+)"', text):
        ln = text.count("\n", 0, m.start()) + 1
        if ln not in have:
            out.append((ln, m.group(1), m.group(2)))
    return out


def build():
    files = tf_files()
    parsed, dirs = {}, collections.defaultdict(Dir)
    for f in files:
        text = open(f, encoding="utf-8").read().replace("\r\n", "\n")
        blocks = tfscan.scan(text)
        parsed[f] = (text, blocks)
        d = dirs[os.path.dirname(f)]
        for b in blocks:
            if b["kind"] == "locals":
                for k, _, v in b["attrs"]:
                    d.locals[k] = v
            elif b["kind"] == "variable" and b["labels"]:
                for k, _, v in b["attrs"]:
                    if k == "default":
                        d.vars[b["labels"][0]] = v
            elif b["kind"] == "resource" and len(b["labels"]) == 2:
                at = own_attr(b["labels"][0])
                for k, _, v in b["attrs"]:
                    if k == at:
                        d.own[b["labels"][0] + "." + b["labels"][1]] = v
    labels, names, stats = [], [], collections.Counter()
    commented, no_own, own_absent, module_args = [], collections.Counter(), [], collections.Counter()
    kinds = collections.Counter()
    for f in files:
        text, blocks = parsed[f]
        commented += [(f,) + c for c in commented_heads(text, blocks)]
        d = dirs[os.path.dirname(f)]
        for b in blocks:
            kinds[b["kind"]] += 1
            if b["kind"] == "module":
                for k, _, v in b["attrs"]:
                    if re.search(r"(^name$|_name$|^bucket$)", k) and LIT.fullmatch(v.strip()):
                        module_args[k] += 1
            if b["kind"] != "resource":
                continue
            rtype, label = b["labels"][0], b["labels"][1]
            ntype = node_of(rtype)
            v, canon, why = grade(label, ntype if ntype else rtype)
            labels.append({"file": f, "line": b["line"], "type": rtype, "node_type": ntype, "label": label,
                           "verdict": v, "canonical": canon, "why": "; ".join(why)})
            at = own_attr(rtype)
            if at is None:
                no_own[rtype] += 1
                continue
            if at == "tags.Name":
                hit = None
                for k, ln, raw in b["attrs"]:
                    if k == "tags":
                        mm = re.search(r'\bName[ \t]*=[ \t]*("(?:[^"\\\n]|\\.)*"|[^\n,}]+)', raw)
                        if mm:
                            hit = (ln + raw[:mm.start()].count("\n"), mm.group(1).strip())
                found = [hit] if hit else []
            else:
                found = [(ln, raw) for k, ln, raw in b["attrs"] if k == at]
            if not found:
                own_absent.append("%s:%d %s.%s (no %s)" % (f, b["line"], rtype, label, at))
                continue
            for ln, raw in found:
                s, chain, reason = resolve(raw, d)
                lit = LIT.fullmatch(raw.strip())
                row = {"file": f, "line": ln, "type": rtype, "node_type": ntype, "attribute": at,
                       "value": unescape(lit.group(1)) if lit else raw}
                if lit:
                    row["value_claim"] = "measured: a literal as written"
                    stats["literal"] += 1
                elif s is not None:
                    row["resolved"] = s
                    row["value_claim"] = "inferred: resolved in the same directory via %s; a variable default can be overridden at apply" % " -> ".join(chain)
                    stats["resolved"] += 1
                else:
                    stats["unresolved"] += 1
                    row["value_claim"] = "absent: %s" % reason
                # G1 decides before the name is read: a type outside the domain RAISES (G1.1) and a NOT GRADED type
                # returns NOT-GRADED (G1.2) whatever the value; only a graded type needs the value placed (G3).
                if s is None and ntype is not None and ntype not in NOT_GRADED:
                    row.update({"verdict": "RAISE", "canonical": "",
                                "why": "G3: a Terraform expression the tokeniser cannot place (%s)" % reason})
                    names.append(row)
                    continue
                gv, gc, gw = grade(s if s is not None else raw, ntype if ntype else rtype)
                row.update({"verdict": gv, "canonical": gc, "why": "; ".join(gw)})
                names.append(row)
    return {"files": files, "labels": labels, "names": names, "stats": stats, "commented": commented, "no_own": no_own,
            "own_absent": own_absent, "module_args": module_args, "kinds": kinds}


def summarize(r):
    lab, nam = r["labels"], r["names"]
    print("tf_files %d  labels %d  name_attributes %d" % (len(r["files"]), len(lab), len(nam)))
    print("kinds", dict(r["kinds"]))
    print("commented heads", r["commented"])
    print("value forms", dict(r["stats"]))
    print("own-name absent", r["own_absent"])
    print("module literal name args", dict(r["module_args"]))
    print("no-own types", sum(r["no_own"].values()), len(r["no_own"]))
    for key, rows in (("LABELS", lab), ("NAMES", nam)):
        print("==", key, dict(collections.Counter(x["verdict"] for x in rows)))
        raise_steps = collections.Counter(x["why"].split(":")[0] for x in rows if x["verdict"] == "RAISE")
        print("   RAISE steps", dict(raise_steps))
        byn = collections.defaultdict(collections.Counter)
        for x in rows:
            byn[x["node_type"] or "(no node type)"][x["verdict"]] += 1
        for k in sorted(byn):
            print("   %-24s %s" % (k, dict(byn[k])))


if __name__ == "__main__":
    if sys.argv[1:] == ["selftest"]:
        sys.exit(1 if selftest() else 0)
    if sys.argv[1:] == ["summary"]:
        summarize(build())
