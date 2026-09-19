#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-9 battery -- the two-key test-principal packet on the real mint path.

DECLARE ONLY. Nothing is written to opal-users-v2 or opal-partner-49financial; no session is minted.

Arms (the face's R66-AC1):
  (a) KEYS: every attribute of K1 (opal-users-v2 PROFILE item), K1b (opal-partner-49financial item) and
      K2 (the session) -- present AND deliberately absent -- cited to the source line that READS it at
      HEAD (`m of m` cited), and the attribute names checked in the SERVED auth-handler bytes (the zip is
      downloaded and its sha256 must equal the live CodeSha256).
  (b) CENSUS of opal-partner-49financial: WRITERS on the identity plane (every IAM role and user
      simulated for PutItem/UpdateItem/DeleteItem/BatchWriteItem on the table ARN; resource policy read),
      and READERS in code (an UNSCOPED git grep over every tracked file at HEAD plus the portal repo at its
      HEAD, every production hit classified with its SENSE; an unclassified hit fails the arm, and a
      FALSE-MATCH classification is re-verified line by line).
  (c)/(d) the packet carries both branches per key, the rollback (K1b deleted FIRST) and the exercise
      plan -- checked by section markers in the COMMITTED packet.
  (e) the packet is committed (blob at HEAD == worktree), its census lines equal this run's re-derived
      counts, and `0` writes are measured on both tables before and after (the test prefixes absent;
      item counts printed).
Prints IBR66-TWO-KEY-PACKET-DECLARED-NOTHING-CREATED only when every arm holds. Re-derives everything
each run; never reads its own earlier output. Prints no e-mail, no URL, no secret, no row value beyond
counts.
"""
from __future__ import annotations

import base64
import collections
import concurrent.futures
import datetime
import fnmatch
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
AWS = os.path.join(WS, ".tools", "aws.cmd")
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-9_R66-AC1_battery_output.txt")
TOKEN = "IBR66-TWO-KEY-PACKET-DECLARED-NOTHING-CREATED"
PACKET_REL = ("org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/"
              "NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md")

USERS_TABLE = "opal-users-v2"
PARTNER_TABLE = "opal-partner-49financial"
AUTH_FN = "opalinvest-auth-handler"
TEST_PK_PREFIX = "USER#usr_irptrte_"
TEST_EMAIL_PREFIX = "irpt-rte1-test-"
WRITE_ACTIONS = ("dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem", "dynamodb:BatchWriteItem")
CALL_TIMEOUT_S = 180

F_DB = "infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts"
F_AUTH = "infra/aws/opalinvest_dev/lambda/auth-handler/src/auth.ts"
F_JWT = "infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts"
F_TYPES = "infra/aws/opalinvest_dev/lambda/auth-handler/src/types.ts"
F_PARTNER = "infra/aws/lambda/lib/partner/index.ts"
F_EDGE = "infra/aws/lambda-edge/auth-validator-edge/index.mjs"
F_RESOLVE = "infra/aws/lambda/investor-reporting/_scope/resolve.py"
F_TIER = "infra/aws/lambda-edge/auth-validator-edge/tier_policy.mjs"

# (key, attribute, SET <shape> | ABSENT, sense, [(file, literal the reader line contains)])
KEYS = [
    ("K1", "PK", "SET USER#usr_irptrte_<epoch>", "getUser reads the PROFILE item by PK after the e-mail lookup",
     [(F_DB, "Key: { PK: pk, SK: 'PROFILE' }")]),
    ("K1", "SK", "SET PROFILE", "the sort key getUser reads", [(F_DB, "Key: { PK: pk, SK: 'PROFILE' }")]),
    ("K1", "email", "SET irpt-rte1-test-<epoch>@opal.test (lower-case)",
     "the email-index GSI resolves the login; lower-cased at login; the token's sub",
     [(F_DB, "IndexName: 'email-index'"), (F_AUTH, "getUser(email.toLowerCase())"), (F_JWT, "sub: user.email,")]),
    ("K1", "passwordHash", "SET bcrypt(random password generated at run time, never recorded)",
     "the only credential the login checks",
     [(F_DB, "password_hash: item.passwordHash || item.password_hash"),
      (F_AUTH, "verifyPassword(password, user.password_hash)")]),
    ("K1", "name", "SET 'IRPT test principal (IB-rtf-3)'", "the token's name claim",
     [(F_DB, "    name: item.name,"), (F_JWT, "name: user.name,")]),
    ("K1", "role", "SET 'user'", "admin bypasses the edge advisor check and is FIRM_OPERATIONS on IRPT",
     [(F_DB, "    role: item.role,"), (F_JWT, "role: user.role,"), (F_EDGE, 'if (payload.role === "admin") return null;'),
      (F_RESOLVE, 'if (role == "admin" or advisor_role == "admin") and firm:')]),
    ("K1", "firmId", "SET '49financial'", "selects opal-partner-49financial and the firm claim",
     [(F_DB, "    firmId: item.firmId,"), (F_AUTH, "partnerIdentity = await getPartnerIdentity(user.email, user.firmId);"),
      (F_JWT, "const firmId = user.firmId || 'null';")]),
    ("K1", "status", "SET 'active'", "login and refresh refuse any other value",
     [(F_DB, "    status: item.status,"), (F_AUTH, "if (user.status !== 'active') {")]),
    ("K1", "createdAt", "SET ISO instant of creation", "the refresh token's row binding",
     [(F_DB, "created_at: item.createdAt || item.created_at,"), (F_JWT, "const born = user.createdAt || user.created_at || '';")]),
    ("K1", "createdBy", "SET '0.7.0_AE_CloudOps~V IB-rtf-3'", "provenance only -- the census marker for the row",
     [(F_DB, "created_by: item.createdBy || item.created_by,")]),
    ("K1", "userType", "ABSENT", "'Dev' is superadmin; absent -> no userType claim",
     [(F_DB, "userType: item.userType,"), (F_JWT, "...(userType && { userType }),"), (F_TYPES, "userType?: string; // 'Dev' = superadmin")]),
    ("K1", "mfaChannel/mfaEnabled", "ABSENT", "absent reads 'none'/false, so the MFA gate is skipped and nothing is sent",
     [(F_DB, "mfaChannel: (item.mfaChannel as MfaChannel) ?? 'none',"), (F_DB, "mfaEnabled: item.mfaEnabled ?? false,"),
      (F_AUTH, "if (user.mfaEnabled && user.mfaChannel && user.mfaChannel !== 'none') {")]),
    ("K1", "phoneNumber/phoneVerifiedAt", "ABSENT", "no phone on the row", [(F_DB, "    phoneNumber: item.phoneNumber,")]),
    ("K1", "mustChangePassword", "ABSENT", "absent reads false", [(F_DB, "must_change_password: item.mustChangePassword ?? item.must_change_password ?? false,")]),
    ("K1", "advisorKey/advisorId", "ABSENT", "getUser's mapping reads no advisor field -- written here it is never read",
     [(F_DB, "export async function getUser(email: string)")]),
    ("K1b", "email", "SET the SAME e-mail as K1 (the table's HASH key)", "the partner lookup key",
     [(F_PARTNER, "new GetCommand({ TableName, Key: { email } })")]),
    ("K1b", "advisorKey", "SET 'abby_horton'", "the token's advisorKey AND advisorId -> X-Advisor-Id -> FIRM_ADVISOR",
     [(F_PARTNER, "const advisorKey = response.Item.advisorKey as string | undefined;"),
      (F_DB, "advisorKey:  (raw.advisorKey  as string | undefined) ?? profile.advisorKey ?? '',"),
      (F_JWT, "advisorId:   partnerIdentity.advisorKey,")]),
    ("K1b", "firmRole", "ABSENT", "absent -> no firmRole claim; 'admin' would bypass the edge advisor check",
     [(F_PARTNER, "const firmRole = (response.Item.firmRole as string | undefined) ?? 'user';"),
      (F_DB, "const firmRole = typeof raw.firmRole === 'string' ? raw.firmRole : undefined;"),
      (F_EDGE, 'if (payload.firmRole === "admin") return null;')]),
    ("K1b", "advisorRole", "ABSENT", "absent -> '' -> FIRM_ADVISOR on IRPT (never FIRM_OPERATIONS); level 0 on ADVI tiers",
     [(F_DB, "advisorRole: (raw.advisorRole as string | undefined) ?? '',"),
      (F_RESOLVE, 'if (role == "admin" or advisor_role == "admin") and firm:'), (F_TIER, "const userLevel = ROLE_LEVEL[advisorRole] ?? 0;")]),
    ("K1b", "advisorName", "ABSENT", "display only; absent -> ''", [(F_DB, "advisorName: (raw.advisorName as string | undefined) ?? '',")]),
    ("K2", "access token", "EPHEMERAL, TTL 15m", "minted by the login; never recorded",
     [(F_JWT, "const ACCESS_TOKEN_EXPIRY = '15m';"), (F_AUTH, "const accessToken = await generateAccessToken(user, partnerIdentity);")]),
    ("K2", "refresh token", "EPHEMERAL, TTL 7d, bound to PK+createdAt", "dies with K1: refresh re-reads the row",
     [(F_JWT, "const REFRESH_TOKEN_EXPIRY = '7d';"), (F_JWT, "const rowKey = user.PK || `USER#${user.email}`;")]),
]
BUNDLE_NAMES = ["passwordHash", "email-index", "PROFILE", "firmId", "createdAt", "createdBy", "advisorKey",
                "userType", "mfaChannel", "mfaEnabled", "firmRole", "advisorRole", "advisorName"]

CODE_EXT = (".ts", ".tsx", ".js", ".mjs", ".cjs", ".py", ".tf", ".sh", ".ps1")
NONPROD_PREFIX = ("org/", "docs/", "archive/", "workflows/", ".scratch/", "deck_generation/")
P_TABLE = r"opal-partner-|partnerTableName|getPartnerProfile|getPartnerIdentity|partner_table|firm_49financial|partner-firm-table"
P_CLAIM = r"advisorRole|firmRole|advisorId|[xX]-[aA]dvisor-([iI]d|[rR]ole)"
SNS = "opal-partner-etl-ops-alerts"

# Every PRODUCTION file the two patterns hit, classified by what it does with the partner row or claim.
CLASS = {
    "infra/aws/lambda/lib/partner/index.ts": ("READER-DIRECT", "GetItem Key {email} -> advisorKey/firmRole: the identity-claim source"),
    "infra/aws/lambda/lib/partner/tableName.ts": ("READER-DIRECT", "the table-name builder for that GetItem"),
    F_DB: ("READER-DIRECT", "getPartnerIdentity -> the JWT advisor claims (MINT)"),
    F_AUTH: ("READER-DIRECT", "calls getPartnerIdentity at login, refresh and /auth/me (MINT)"),
    F_JWT: ("MINT", "writes advisorKey/advisorId/advisorRole/firmRole into the access token"),
    F_TYPES: ("MINT", "the claim type declarations"),
    "users/scripts/partners/partner_contracts.py": ("READER-DIRECT", "operator read-back GetItem verifying the advisorKey after provisioning"),
    "users/scripts/create_user_v2.py": ("WRITER-DIRECT", "operator PutItem of the partner row (_write_partner_table)"),
    "users/scripts/partners/provision_49financial.py": ("WRITER-DIRECT", "operator wrapper -> partner_contracts -> create_user_v2"),
    "users/scripts/partners/provision_cottonwood.py": ("WRITER-DIRECT", "operator wrapper -> partner_contracts -> create_user_v2"),
    "users/scripts/partners/provision_inflection.py": ("WRITER-DIRECT", "operator wrapper -> partner_contracts -> create_user_v2"),
    "infra/aws/terraform/portal-auth/iam.tf": ("IAM-GRANT", "GetItem on opal-partner-* to the auth-handler role (read)"),
    "infra/aws/terraform/shared-infra/main.tf": ("IAM-GRANT", "GetItem on opal-partner-* to the auth-handler role (read)"),
    "infra/aws/terraform/modules/partner-firm-table/main.tf": ("TABLE-DEF", "the table, HASH=email, GSI ByAdvisorRole, PITR, deletion protection"),
    "infra/aws/terraform/modules/partner-firm-table/outputs.tf": ("TABLE-DEF", "module outputs"),
    "infra/aws/terraform/partner-firms/49financial.tf": ("TABLE-DEF", "the 49financial instantiation"),
    "infra/aws/terraform/partner-firms/cottonwood.tf": ("TABLE-DEF", "another firm's instantiation"),
    "infra/aws/terraform/partner-firms/inflection.tf": ("TABLE-DEF", "another firm's instantiation"),
    "infra/aws/terraform/partner-firms/demo.tf": ("TABLE-DEF", "another firm's instantiation"),
    F_EDGE: ("ENFORCE-EDGE", "advisorId allow-list; role/firmRole 'admin' bypass; injects X-Advisor-Id/X-Advisor-Role"),
    F_TIER: ("ENFORCE-EDGE", "advisorRole -> ADVI tier level (advisor-intelligence paths only)"),
    "infra/aws/lambda-edge/auth-validator-edge/aggregate_gate.mjs": ("ENFORCE-EDGE", "aggregate gate on tier=internal; does not admit firmRole admin"),
    "infra/aws/lambda-edge/shared-advisor-router/index.mjs": ("ENFORCE-EDGE", "advisorId -> advisor S3 key routing"),
    "infra/aws/lambda-edge/shared-advisor-router/tier_policy.mjs": ("ENFORCE-EDGE", "advisorRole -> ADVI tier level"),
    "infra/aws/users/lambda/portal-authorizer/index.mjs": ("ENFORCE-APIGW", "passes advisorId/advisorRole/firmRole into the API Gateway context"),
    "infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py":
        ("ENFORCE-BACKEND", "L1 path scope by advisorId; advisorRole tier; role/firmRole admin bypass"),
    F_RESOLVE: ("ENFORCE-BACKEND", "X-Advisor-Id -> FIRM_ADVISOR; advisor_role admin -> FIRM_OPERATIONS"),
    "infra/aws/lambda/investor-reporting/_scope/global.py": ("ENFORCE-BACKEND", "reads X-Advisor-Id in the global-viewer resolver"),
    "infra/aws/lambda/investor-reporting/_authz/enforce.py": ("ENFORCE-BACKEND", "reads X-Advisor-Id in the Enforcer"),
    "infra/aws/lambda/investor-reporting/holdings/resolve.py": ("ENFORCE-BACKEND", "holdings' own copy of the classifier (X-Advisor-Id/Role)"),
    "infra/aws/lambda/investor-reporting/holdings/enforce.py": ("ENFORCE-BACKEND", "holdings' own Enforcer (X-Advisor-Id)"),
    "infra/aws/auth/validator.py": ("LIBRARY-UNMEASURED", "the unified validator module; its deployed consumers are not censused here"),
    "infra/aws/auth/validator.ts": ("LIBRARY-UNMEASURED", "the unified validator module; its deployed consumers are not censused here"),
    "infra/aws/users/_archive_pre_2026-04-15/guardrails/tier_filter.py": ("ARCHIVE", "archived pre-2026-04-15 code"),
    "infra/aws/terraform/bd-pipeline/api-gateway.tf": ("ROUTE-TEXT", "{advisorId} path parameter in route keys, not a claim read"),
    "infra/aws/terraform/partners-api/api-gateway.tf": ("ROUTE-TEXT", "{advisorId} path parameter in route keys, not a claim read"),
    "infra/aws/terraform/shared-infra/apigateway-portal/routes.tf": ("ROUTE-TEXT", "comments naming {advisorId} route paths"),
    "infra/aws/terraform/shared-infra/dynamo.tf": ("ROUTE-TEXT", "a comment on the firmRole rollout date"),
    "data/black_diamond/scripts/gold/D_00.portal_aggregates.py": ("ROUTE-TEXT", "a comment naming advisorId path parameters"),
    "data/cot/scripts/gold/D_00.portal_aggregates.py": ("ROUTE-TEXT", "a comment naming advisorId path parameters"),
    "data/assets/scripts/gold/runners_49f/d00_served_shape_census.py": ("ROUTE-TEXT", "a {advisorId} route template string"),
    ".tools/portal-hooks/d1_gate_test.py": ("TEST", "portal hook test fixture"),
}
FALSE_MATCH_SNS = {
    "data/inf/scripts/gold/lib/aor_attribution_audit.py", "infra/aws/lambda/infrastructure_monitor/lambda_function.py",
    "infra/aws/lambda/partner-etl-ops-sqs-consumer/lambda_function.py", "infra/aws/terraform/inf-pipeline/alarms.tf",
    "infra/aws/terraform/inf-pipeline/iam.tf", "infra/aws/terraform/partner-etl-ops-alerts/main.tf",
    "infra/aws/terraform/partner-etl-ops-alerts/ops-alerts.tf", "infra/aws/terraform/shared-infra/partner-etl-ops-sqs-consumer.tf",
}

LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str, cwd: str = WS) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=300)
    return out.returncode, out.stdout


def aws(*args: str) -> tuple[int, str, str]:
    try:
        out = subprocess.run([AWS, *args], capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=CALL_TIMEOUT_S)
        return out.returncode, out.stdout, out.stderr.strip()
    except subprocess.TimeoutExpired:
        return 124, "", "TIMEOUT after %ss" % CALL_TIMEOUT_S


def head_short() -> str:
    return git("rev-parse", "--short=10", "HEAD")[1].strip()


# --------------------------------------------------------------------------- (a) keys
def arm_a_keys() -> bool:
    emit("(a) KEYS -- every attribute cited to the source line that reads it at HEAD, then the served bytes")
    hs = head_short()
    cache: dict[str, list[str]] = {}
    n_cited = 0
    for key, attr, state, sense, refs in KEYS:
        cites, ok = [], True
        for f, lit in refs:
            if f not in cache:
                rc, txt = git("show", "HEAD:" + f)
                cache[f] = txt.splitlines() if rc == 0 else []
            ln = next((i + 1 for i, line in enumerate(cache[f]) if lit in line), 0)
            ok = ok and ln > 0
            cites.append("%s:%s @%s" % (f, ln if ln else "NOT-FOUND", hs))
        if key == "K1" and attr == "advisorKey/advisorId":
            src = "\n".join(cache.get(F_DB, []))
            m = re.search(r"export async function getUser\(email: string\).*?\n  return \{(.*?)\n  \} as User;", src, re.S)
            ok = ok and bool(m) and "advisor" not in m.group(1).lower()
            if m:
                start = src[: m.start(1)].count("\n") + 1
                cites.append("%s:%d-%d @%s (getUser mapping: %s)" % (F_DB, start, start + m.group(1).count("\n"), hs,
                             "no advisor field" if ok else "HAS an advisor field"))
        n_cited += ok
        emit("  %-3s %-26s %-58s %s" % (key, attr, state, "CITED" if ok else "NOT CITED"))
        emit("      sense: %s" % sense)
        for c in cites:
            emit("      reader: %s" % c)
    emit("  attributes cited: %d of %d" % (n_cited, len(KEYS)))

    rc, so, _ = aws("lambda", "get-function-configuration", "--function-name", AUTH_FN, "--query", "CodeSha256", "--output", "text")
    live = so.strip() if rc == 0 else ""
    rc, loc, se = aws("lambda", "get-function", "--function-name", AUTH_FN, "--query", "Code.Location", "--output", "text")
    served_ok, present = False, 0
    if rc == 0 and loc.strip():
        blob = urllib.request.urlopen(loc.strip(), timeout=CALL_TIMEOUT_S).read()  # URL never printed
        got = base64.b64encode(hashlib.sha256(blob).digest()).decode()
        served_ok = bool(live) and got == live
        text = "\n".join(zipfile.ZipFile(io.BytesIO(blob)).read(n).decode("utf-8", errors="replace")
                         for n in zipfile.ZipFile(io.BytesIO(blob)).namelist() if n.endswith((".js", ".mjs")))
        missing = [n for n in BUNDLE_NAMES if n not in text]
        present = len(BUNDLE_NAMES) - len(missing)
        email_key = bool(re.search(r"Key:\s*\{\s*email\s*:", text))
        emit("  served %s: zip sha256(b64) %s %s live CodeSha256 %s" % (AUTH_FN, got, "==" if served_ok else "!=", live))
        emit("  attribute names referenced by the served bundle: %d of %d%s; partner GetItem Key {email} present=%s"
             % (present, len(BUNDLE_NAMES), (" MISSING %s" % missing) if missing else "", email_key))
        served_ok = served_ok and not missing and email_key
    else:
        emit("  get-function rc %s: %s" % (rc, se[-200:]))
    return n_cited == len(KEYS) and served_ok


# --------------------------------------------------------------------------- (b) census
def _as_list(x):
    return [x] if isinstance(x, str) else list(x or [])


def _documents(iam, kind, name):
    docs, attached = [], []
    if kind == "role":
        for n in iam.list_role_policies(RoleName=name)["PolicyNames"]:
            docs.append(iam.get_role_policy(RoleName=name, PolicyName=n)["PolicyDocument"])
        attached = iam.list_attached_role_policies(RoleName=name)["AttachedPolicies"]
    else:
        for n in iam.list_user_policies(UserName=name)["PolicyNames"]:
            docs.append(iam.get_user_policy(UserName=name, PolicyName=n)["PolicyDocument"])
        attached = list(iam.list_attached_user_policies(UserName=name)["AttachedPolicies"])
        for g in iam.list_groups_for_user(UserName=name)["Groups"]:
            for n in iam.list_group_policies(GroupName=g["GroupName"])["PolicyNames"]:
                docs.append(iam.get_group_policy(GroupName=g["GroupName"], PolicyName=n)["PolicyDocument"])
            attached += iam.list_attached_group_policies(GroupName=g["GroupName"])["AttachedPolicies"]
    for a in attached:
        v = iam.get_policy(PolicyArn=a["PolicyArn"])["Policy"]["DefaultVersionId"]
        docs.append(iam.get_policy_version(PolicyArn=a["PolicyArn"], VersionId=v)["PolicyVersion"]["Document"])
    return [json.loads(urllib.parse.unquote(d)) if isinstance(d, str) else d for d in docs]


def _matching_allow(iam, kind, name, arn):
    hits = []
    for d in _documents(iam, kind, name):
        stmts = d.get("Statement")
        for s in (stmts if isinstance(stmts, list) else [stmts]):
            if not isinstance(s, dict) or s.get("Effect") != "Allow":
                continue
            acts = [a for act in WRITE_ACTIONS for a in _as_list(s.get("Action")) if fnmatch.fnmatch(act.lower(), a.lower())]
            res = [r for r in _as_list(s.get("Resource")) if fnmatch.fnmatch(arn, r)]
            if acts and res:
                hits.append(s.get("Sid") or "<no-sid>")
    return hits


def writer_census() -> dict:
    import boto3
    iam = boto3.client("iam")
    ddb = boto3.client("dynamodb", region_name="us-east-1")
    arn = ddb.describe_table(TableName=PARTNER_TABLE)["Table"]["TableArn"]
    try:
        ddb.get_resource_policy(ResourceArn=arn)
        rp = "PRESENT"
    except ddb.exceptions.PolicyNotFoundException:
        rp = "NONE"
    except Exception as exc:  # noqa: BLE001
        rp = "UNREADABLE (%s)" % type(exc).__name__
    principals = []
    for page in iam.get_paginator("list_roles").paginate():
        principals += [("role", r["RoleName"], r["Arn"]) for r in page["Roles"]]
    for page in iam.get_paginator("list_users").paginate():
        principals += [("user", u["UserName"], u["Arn"]) for u in page["Users"]]
    irrelevant = {"dynamodb:LeadingKeys", "dynamodb:Select", "dynamodb:Attributes"}

    def sim(p):
        kind, name, parn = p
        for attempt in range(4):
            try:
                res = iam.simulate_principal_policy(PolicySourceArn=parn, ActionNames=list(WRITE_ACTIONS),
                                                    ResourceArns=[arn])["EvaluationResults"]
                allowed = sorted(r["EvalActionName"] for r in res if r["EvalDecision"] == "allowed")
                miss = sorted({k for r in res for k in (r.get("MissingContextValues") or []) if k not in irrelevant})
                return p, allowed, miss, None
            except Exception as exc:  # noqa: BLE001
                code = getattr(exc, "response", {}).get("Error", {}).get("Code", type(exc).__name__)
                if code in ("NoSuchEntity", "InvalidInput") or attempt == 3:
                    return p, [], [], code
                time.sleep(1.5 * (attempt + 1))

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(sim, principals))
    writers = [(p, a) for p, a, _, e in results if a and not e]
    errors = [(p[0], p[1], e) for p, _, _, e in results if e]
    unknown = [(p, m) for p, a, m, e in results if not a and m and not e]
    settled = [p for p, _ in unknown if not _matching_allow(iam, p[0], p[1], arn)]
    unknown = [(p, m) for p, m in unknown if p not in settled]
    per_action = collections.Counter(x for _, a in writers for x in a)
    return {"arn": arn, "resource_policy": rp, "principals": principals, "writers": writers, "errors": errors,
            "unknown": unknown, "settled": settled, "per_action": per_action}


def _classify_hit(path: str, lines: list[str]) -> tuple[str, str]:
    if path in FALSE_MATCH_SNS:
        if all(SNS in ln for ln in lines):
            return "FALSE-MATCH", "every hit is the SNS topic %s, not the table" % SNS
        return "UNCLASSIFIED", "listed as an SNS false match but a hit line is not the topic"
    if path in CLASS:
        return CLASS[path]
    if "/tests/" in path or path.rsplit("/", 1)[-1].startswith("test_") or path.endswith("fixtures.py"):
        return "TEST", "a test or fixture"
    return "UNCLASSIFIED", "no rule"


def code_census() -> dict:
    out = {}
    hs = head_short()
    tracked = len(git("ls-files")[1].splitlines())
    for name, pat in (("TABLE", P_TABLE), ("CLAIM", P_CLAIM)):
        _, raw = git("grep", "-n", "-I", "-E", pat, "HEAD", "--")
        by_file: dict[str, list[str]] = collections.defaultdict(list)
        for ln in raw.splitlines():
            parts = ln.split(":", 3)
            if len(parts) == 4:
                by_file[parts[1]].append(parts[3])
        prod = {f: v for f, v in by_file.items() if f.endswith(CODE_EXT) and not f.startswith(NONPROD_PREFIX)}
        other = collections.Counter(f.split("/")[0] for f in by_file if f not in prod)
        cls = {f: _classify_hit(f, v) for f, v in prod.items()}
        out[name] = {"files": len(by_file), "prod": prod, "other": other, "cls": cls, "head": hs, "tracked": tracked}
    _, wl = git("worktree", "list", "--porcelain")
    main_wt = next((ln[len("worktree "):].strip() for ln in wl.splitlines() if ln.startswith("worktree ")), "")
    portal = os.path.join(main_wt, "portal")
    prc, ph = git("rev-parse", "--short=10", "HEAD", cwd=portal)
    out["portal_head"] = ph.strip() if prc == 0 else "UNREAD"
    for name, pat in (("TABLE", P_TABLE), ("CLAIM", P_CLAIM)):
        rc, raw = git("grep", "-l", "-I", "-E", pat, "HEAD", "--", cwd=portal)
        files = [ln.split(":", 1)[1] for ln in raw.splitlines() if ":" in ln] if rc in (0, 1) else []
        out["portal_" + name] = files
    return out


def arm_b_census(packet_text: str) -> tuple[bool, dict]:
    emit("(b) CENSUS of %s -- writers (identity plane) and readers (code)" % PARTNER_TABLE)
    w = writer_census()
    n_p = len(w["principals"])
    n_roles = sum(1 for p in w["principals"] if p[0] == "role")
    emit("  table %s; resource policy: %s" % (w["arn"], w["resource_policy"]))
    emit("  IDENTITY plane: %d principals simulated (%d roles, %d users) for %s on the table ARN"
         % (n_p, n_roles, n_p - n_roles, "/".join(a.split(":")[1] for a in WRITE_ACTIONS)))
    emit("  unsimulated: %d %s; UNKNOWN after statement reading: %d %s; settled by statement reading: %d"
         % (len(w["errors"]), w["errors"][:5], len(w["unknown"]), [(p[1], m) for p, m in w["unknown"]][:5], len(w["settled"])))
    emit("  WRITERS: %d of %d principals may write %s (any of the %d actions); per action %s"
         % (len(w["writers"]), n_p, PARTNER_TABLE, len(WRITE_ACTIONS),
            dict(sorted((a.split(":")[1], c) for a, c in w["per_action"].items()))))
    for (kind, name, _), acts in sorted(w["writers"], key=lambda x: (x[0][0], x[0][1])):
        emit("    %-4s %-45s %s" % (kind, name, ",".join(a.split(":")[1] for a in acts)))
    names = {p[1]: a for p, a in w["writers"]}
    pos = "Andrew_Berman" in names
    neg = "opalinvest-auth-lambda-role" not in names
    emit("  positive control: user Andrew_Berman (administrator) is a writer: %s" % pos)
    emit("  negative control: opalinvest-auth-lambda-role (GetItem-only grants) is NOT a writer: %s" % neg)

    c = code_census()
    t, cl = c["TABLE"], c["CLAIM"]
    emit("  CODE census: git grep over %d tracked files at HEAD %s (unscoped), plus the portal repo at HEAD %s"
         % (t["tracked"], t["head"], c["portal_head"]))
    unclassified = 0
    for label, d in (("TABLE-TOUCH (%s)" % P_TABLE, t), ("CLAIM-CONSUMER (%s)" % P_CLAIM, cl)):
        emit("  %s: %d files hit; PRODUCTION code %d; other %d %s"
             % (label, d["files"], len(d["prod"]), d["files"] - len(d["prod"]), dict(d["other"].most_common(8))))
        by_class = collections.Counter(v[0] for v in d["cls"].values())
        emit("    by class: %s" % dict(sorted(by_class.items())))
        for f in sorted(d["prod"]):
            k, sense = d["cls"][f]
            unclassified += k == "UNCLASSIFIED"
            emit("    %-16s %s -- %s (%d hit lines)" % (k, f, sense, len(d["prod"][f])))
    direct_readers = sorted(f for f, v in t["cls"].items() if v[0] == "READER-DIRECT")
    direct_writers = sorted(f for f, v in {**t["cls"], **cl["cls"]}.items() if v[0] == "WRITER-DIRECT")
    enforcers = sorted(f for f, v in cl["cls"].items() if v[0].startswith("ENFORCE"))
    emit("  READERS of the row (direct): %d -- %s" % (len(direct_readers), direct_readers))
    emit("  CODE WRITERS of the row (operator scripts): %d -- %s" % (len(direct_writers), direct_writers))
    emit("  CLAIM ENFORCERS downstream (the SENSE the row sets): %d" % len(enforcers))
    emit("  portal repo: TABLE-TOUCH %d files %s; CLAIM-CONSUMER %d files (client-side SPA, tests and docs: "
         "display and routing, not an enforcement point)" % (len(c["portal_TABLE"]), c["portal_TABLE"], len(c["portal_CLAIM"])))
    emit("  unclassified production hits: %d" % unclassified)

    stated = {
        "CENSUS-WRITERS": "%d of %d" % (len(w["writers"]), n_p),
        "CENSUS-READERS-DIRECT": "%d of %d" % (len(direct_readers), len(t["prod"])),
        "CENSUS-CLAIM-ENFORCERS": "%d of %d" % (len(enforcers), len(cl["prod"])),
    }
    match = True
    for k, v in stated.items():
        m = re.search(r"%s: (\d+ of \d+)" % k, packet_text)
        got = m.group(1) if m else "ABSENT"
        match = match and got == v
        emit("  packet line %s: packet says %s, this run %s -> %s" % (k, got, v, "EQUAL" if got == v else "DIFFERS"))
    ok = (not w["errors"] and not w["unknown"] and pos and neg and unclassified == 0 and match)
    return ok, {"writers": len(w["writers"]), "principals": n_p}


# --------------------------------------------------------------------------- (e) zero writes
def zero_write_measure(label: str) -> tuple[bool, str]:
    rows = []
    ok = True
    for table, attr, prefix in ((USERS_TABLE, "PK", TEST_PK_PREFIX), (USERS_TABLE, "email", TEST_EMAIL_PREFIX),
                                (PARTNER_TABLE, "email", TEST_EMAIL_PREFIX)):
        rc, so, se = aws("dynamodb", "scan", "--table-name", table, "--select", "COUNT",
                         "--filter-expression", "begins_with(#a, :p)",
                         "--expression-attribute-names", json.dumps({"#a": attr}),
                         "--expression-attribute-values", json.dumps({":p": {"S": prefix}}), "--output", "json")
        d = json.loads(so) if rc == 0 else {}
        ok = ok and rc == 0 and d.get("Count") == 0
        rows.append("%s %s begins_with '%s': %s of %s scanned" % (table, attr, prefix, d.get("Count"), d.get("ScannedCount")))
    for r in rows:
        emit("  %s: %s" % (label, r))
    return ok, "|".join(rows)


def packet_checks() -> tuple[bool, str]:
    emit("(c)(d)(e) THE PACKET -- committed, unchanged, carrying both branches, the rollback order and the plan")
    rc, blob_head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    blob_head = blob_head if rc == 0 else ""
    _, blob_wt = git("hash-object", PACKET_REL) if os.path.exists(os.path.join(WS, PACKET_REL)) else (1, "")
    committed = rc == 0 and blob_head.strip() == blob_wt.strip() and bool(blob_head.strip())
    emit("  packet %s: blob at HEAD %s, worktree %s -> %s" % (PACKET_REL, blob_head.strip() or "ABSENT",
         blob_wt.strip() or "ABSENT", "COMMITTED, UNCHANGED" if committed else "NOT COMMITTED OR CHANGED"))
    text = git("show", "HEAD:" + PACKET_REL)[1] if rc == 0 else ""
    markers = ["## K1 ", "## K1b ", "## K2 ", "BRANCH -- K1b PRESENT", "BRANCH -- K1b ABSENT", "ROLLBACK",
               "DELETE ORDER: K1b FIRST", "## THE EXERCISE PLAN", "NOTHING IS CREATED BY THIS PACKET"]
    missing = [m for m in markers if m not in text]
    emit("  section markers present: %d of %d%s" % (len(markers) - len(missing), len(markers),
         (" MISSING %s" % missing) if missing else ""))
    return committed and not missing, text


def main() -> int:
    emit("IB-rtf-9 R66-AC1 battery -- run at %s -- worktree HEAD %s" % (now(), git("rev-parse", "HEAD")[1].strip()))
    emit("")
    emit("(e) ZERO WRITES -- measured BEFORE")
    before_ok, before = zero_write_measure("before")
    emit("")
    a_ok = arm_a_keys()
    emit("")
    p_ok, packet_text = packet_checks()
    emit("")
    b_ok, _ = arm_b_census(packet_text)
    emit("")
    emit("(e) ZERO WRITES -- measured AFTER")
    after_ok, after = zero_write_measure("after")
    emit("  test prefixes absent before and after on both tables: %s" % (before_ok and after_ok))
    emit("")
    arms = {"(a) keys": a_ok, "(b) census": b_ok, "(c)(d)(e) packet": p_ok, "(e) zero writes": before_ok and after_ok}
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else "FAIL"))
    if all(arms.values()):
        emit("RESULT: R66-AC1 PASS -- the two-key packet declared on the real mint path; nothing created")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R66-AC1 FAIL -- %d of %d arms hold" % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
