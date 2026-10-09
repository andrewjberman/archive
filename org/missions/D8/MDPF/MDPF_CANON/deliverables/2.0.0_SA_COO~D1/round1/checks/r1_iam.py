"""r1_iam.py -- MDPF_CANON round 1, cell CN-a-1 (issuer 2.0.0_SA_COO~D1): THE PER-FIRM GOLD WRITERS.

Usage (repo root of the checkout under test): python <this file> [--no-live]

PRD v2.9 CONTRACTS "the firm gold writer" (@12adb87963, CTO ruling (a), msg 2995) and the CVO's L6 condition
(msg 3000): one principal PER FIRM, its name `name()` output with the firm in the scope slot, assumed by
`mdpf-gold-lambda`, its ONLY write grant the firm's gold prefix from `address()`; the live DenyForeignFirmPrincipals
admits each name with no edit. The precedent is MDPF_TAXSMA's roles in the same file (iam.tf, taxsma_49f/_cot).

Reads (never writes): infra/aws/terraform/mdpf-pipeline/iam.tf and gold-lambda.tf, lib/opal_naming.py name(), and
(unless --no-live) each firm bucket's live policy through the .tools/aws shim.

Arms:
  1 NAMES     per firm (49financial, inflection, cottonwood): a `module` block with source ../modules/opal_name,
              system "mdpf", scope "<firm>", function "gold-writer", kind "role"; the role resource takes its name
              from that module; no role name is typed anywhere in the two files.
  2 GRANT     the role's inline policy: every S3 ARN is the firm bucket (ListBucket) or
              <bucket>/mdpf/<firm>/gold/<artifact>/* for the four artifacts -- nothing else (no platinum, no state,
              no wildcard prefix); the bucket and the firm come from the module's maps (locals), never typed.
  3 TRUST     the role trusts aws_iam_role.mdpf_gold_lambda.arn; a gold-Lambda policy allows sts:AssumeRole on the
              three roles; gold-lambda.tf passes GOLD_WRITER_ROLE_ARN_<FIRM> = aws_iam_role.<role>.arn per firm.
  4 GLOBAL    the gold Lambda's own role may Put/Get mdpf/global/gold/<artifact>/* in opal-data-mdpf (the composite,
              which no fence guards), the four artifacts only.
  5 ADMITTED  (live) each name() role ARN matches one ArnNotLike pattern of that firm bucket's live
              DenyForeignFirmPrincipals statement -- the fence admits it with no edit (FWD-6).
  6 PLANTED   the grant comparator refuses a platinum ARN and a state ARN; a typed role name is caught.
Prints one line per arm and "ROUND 1 GOLD WRITERS: <k> of <n> arms"; exit 0 only when every arm passes.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or os.getcwd()
sys.path.insert(0, ROOT)
from lib.opal_naming import name  # noqa: E402

IAM = os.path.join(ROOT, "infra/aws/terraform/mdpf-pipeline/iam.tf")
GOLD = os.path.join(ROOT, "infra/aws/terraform/mdpf-pipeline/gold-lambda.tf")
FIRMS = ("49financial", "inflection", "cottonwood")
ARTIFACTS = ("account_distribution", "account_units", "aggregate_aua_timeseries", "aum_metrics")
LIVE = "--no-live" not in sys.argv

iam = open(IAM, encoding="utf-8").read()
gold = open(GOLD, encoding="utf-8").read()


def hcl_strings(text):
    """Every double-quoted HCL string in text, with a quote inside a ${...} interpolation kept inside the string
    (amended on row MDPF_CANON-D1-W7-S1: `"arn:aws:s3:::${module.m.scope_bucket["mdpf"]}/..."` is ONE string)."""
    out, i, n = [], 0, len(text)
    while i < n:
        if text[i] != '"':
            i += 1
            continue
        j, depth, buf = i + 1, 0, []
        while j < n:
            c = text[j]
            if depth == 0 and c == '"':
                break
            if c == "\\" and j + 1 < n:
                buf.append(text[j:j + 2])
                j += 2
                continue
            if text.startswith("${", j):
                depth += 1
                buf.append("${")
                j += 2
                continue
            if c == "}" and depth:
                depth -= 1
            buf.append(c)
            j += 1
        out.append("".join(buf))
        i = j + 1
    return out


def blocks(src, kind, label=None):
    """Top-level HCL blocks `<kind> "<a>" ["<b>"] { ... }` with their labels and bodies (brace-matched)."""
    out = []
    for m in re.finditer(r'(?m)^%s\s+"([^"]+)"(?:\s+"([^"]+)")?\s*\{' % re.escape(kind), src):
        depth, i = 1, m.end()
        while depth and i < len(src):
            depth += {"{": 1, "}": -1}.get(src[i], 0)
            i += 1
        labels = (m.group(1), m.group(2))
        if label is None or label in labels:
            out.append((labels, src[m.end():i - 1]))
    return out


def attr(body, key):
    m = re.search(r'(?m)^\s*%s\s*=\s*"([^"]*)"' % re.escape(key), body)
    return m.group(1) if m else None


def name_modules(firm):
    hits = []
    for (lbl, _), body in blocks(iam, "module"):
        if (attr(body, "source") == "../modules/opal_name" and attr(body, "system") == "mdpf" and attr(body, "scope") == firm
                and attr(body, "function") == "gold-writer" and attr(body, "kind") == "role"):
            hits.append(lbl)
    return hits


def role_for(module_label):
    for (_, rlabel), body in blocks(iam, "resource", None):
        pass
    for (t, rlabel), body in blocks(iam, "resource"):
        if t == "aws_iam_role" and re.search(r'name\s*=\s*module\.%s\.name\b' % re.escape(module_label), body):
            return rlabel, body
    return None, None


def policies_for(role_label):
    out = []
    for (t, plabel), body in blocks(iam, "resource"):
        if t == "aws_iam_role_policy" and re.search(r'role\s*=\s*aws_iam_role\.%s\.(id|name)\b' % re.escape(role_label), body):
            out.append((plabel, body))
    return out


GRANT_OK = re.compile(r'^arn:aws:s3:::\$\{local\.[a-z0-9_]+\}(/mdpf/\$\{local\.[a-z0-9_]+\}/gold/(%s)/\*)?$' % "|".join(ARTIFACTS))


def grant_faults(arns):
    f = []
    for a in arns:
        if not GRANT_OK.match(a):
            f.append(f"GRANT: {a} is not the firm bucket or a firm gold prefix of the four artifacts")
    return f


def s3_arns(body):
    return [s for s in hcl_strings(body) if s.startswith("arn:aws:s3:::")]


arms = []


def arm(label, fn):
    f = []
    try:
        detail = fn(f) or ""
    except Exception as e:  # noqa: BLE001 -- an arm that raises is a failed arm, said in its line
        f.append("RAISED: " + str(e).splitlines()[0][:200])
        detail = ""
    arms.append((label, not f, detail if not f else " | ".join(f)))


roles = {}


def a_names(f):
    for firm in FIRMS:
        mods = name_modules(firm)
        if len(mods) != 1:
            f.append(f"{firm}: {len(mods)} opal_name module(s) with function gold-writer, kind role (want 1)")
            continue
        rl, body = role_for(mods[0])
        if not rl:
            f.append(f"{firm}: no aws_iam_role takes its name from module.{mods[0]}.name")
            continue
        roles[firm] = (mods[0], rl, body)
    typed = [name("mdpf", fm, "gold-writer", "role") for fm in FIRMS]
    for t in typed:
        if t in iam or t in gold:
            f.append(f"TYPED: the role name {t} is typed in the Terraform")
    return "names: " + ", ".join(typed)


def a_grant(f):
    if len(roles) != 3:
        f.append("INPUT: arm 1 did not resolve three roles")
        return ""
    n = 0
    for firm, (_, rl, _) in roles.items():
        pols = policies_for(rl)
        if not pols:
            f.append(f"{firm}: no aws_iam_role_policy on aws_iam_role.{rl}")
            continue
        arns = [a for _, b in pols for a in s3_arns(b)]
        if not any("/gold/" in a for a in arns):
            f.append(f"{firm}: no gold prefix granted")
        f.extend(f"{firm}: {x}" for x in grant_faults(arns))
        n += len(arns)
    return f"{n} S3 ARN(s) across the three roles, every one the firm bucket or a firm gold prefix"


def a_trust(f):
    if len(roles) != 3:
        f.append("INPUT: arm 1 did not resolve three roles")
        return ""
    for firm, (_, rl, body) in roles.items():
        if "aws_iam_role.mdpf_gold_lambda.arn" not in body:
            f.append(f"{firm}: aws_iam_role.{rl} does not trust aws_iam_role.mdpf_gold_lambda.arn")
    assume = [b for (t, _), b in blocks(iam, "resource") if t == "aws_iam_role_policy"
              and re.search(r'role\s*=\s*aws_iam_role\.mdpf_gold_lambda\.(id|name)\b', b) and "sts:AssumeRole" in b]
    joined = "\n".join(assume)
    for firm, (_, rl, _) in roles.items():
        if f"aws_iam_role.{rl}.arn" not in joined:
            f.append(f"{firm}: no gold-Lambda policy allows sts:AssumeRole on aws_iam_role.{rl}.arn")
        envk = "GOLD_WRITER_ROLE_ARN_" + firm.upper()
        if not re.search(r'%s\s*=\s*aws_iam_role\.%s\.arn' % (envk, re.escape(rl)), gold):
            f.append(f"{firm}: gold-lambda.tf does not pass {envk} = aws_iam_role.{rl}.arn")
    return "each role trusts mdpf-gold-lambda; the Lambda may assume each; the env carries each ARN"


def a_global(f):
    pols = [b for (t, _), b in blocks(iam, "resource") if t == "aws_iam_role_policy"
            and re.search(r'role\s*=\s*aws_iam_role\.mdpf_gold_lambda\.(id|name)\b', b)]
    arns = [a for b in pols for a in s3_arns(b) if "/mdpf/global/gold/" in a or "mdpf/${" in a and "/gold/" in a]
    got = {art for art in ARTIFACTS if any(re.search(r'/mdpf/(global|\$\{local\.[a-z0-9_]+\})/gold/%s/\*$' % art, a) for a in arns)}
    missing = sorted(set(ARTIFACTS) - got)
    if missing:
        f.append("GLOBAL: the gold Lambda's own role has no Put on mdpf/global/gold/ for " + ", ".join(missing))
    extra = [a for a in arns if not re.search(r'/gold/(%s)/\*$' % "|".join(ARTIFACTS), a)]
    if extra:
        f.append("GLOBAL: unexpected composite gold grant(s): " + ", ".join(extra))
    return f"{len(got)} of 4 composite gold artifacts granted to the gold Lambda's own role"


def a_admitted(f):
    if not LIVE:
        return "skipped (--no-live)"
    from lib.opal_naming import address
    aws = os.path.join(ROOT, ".tools", "aws")
    for firm in FIRMS:
        bucket = address("mdpf", firm, "gold", "aum_metrics", "date=2026-10-08").split("/")[2]
        r = subprocess.run(["bash", aws, "s3api", "get-bucket-policy", "--bucket", bucket, "--query", "Policy", "--output", "text"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            f.append(f"{firm}: get-bucket-policy {bucket} rc={r.returncode}: {r.stderr.strip()[:160]}")
            continue
        stmts = [s for s in json.loads(r.stdout).get("Statement", []) if s.get("Sid") == "DenyForeignFirmPrincipals"]
        if len(stmts) != 1:
            f.append(f"{firm}: {len(stmts)} DenyForeignFirmPrincipals statement(s) in {bucket}")
            continue
        pats = stmts[0].get("Condition", {}).get("ArnNotLike", {}).get("aws:PrincipalArn", [])
        pats = [pats] if isinstance(pats, str) else pats
        role = name("mdpf", firm, "gold-writer", "role")
        arn = f"arn:aws:iam::313476888478:role/{role}"
        if not any(fnmatch.fnmatchcase(arn, p) for p in pats):
            f.append(f"{firm}: {arn} matches none of {bucket}'s {len(pats)} admitted patterns")
    return "each name() role is admitted by its bucket's live DenyForeignFirmPrincipals, unedited"


def a_planted(f):
    good = ["arn:aws:s3:::${local.gw_49f_bucket}", "arn:aws:s3:::${local.gw_49f_bucket}/mdpf/${local.gw_49f_long}/gold/aum_metrics/*"]
    if grant_faults(good):
        f.append("a correct grant set is refused")
    for bad in ("arn:aws:s3:::${local.gw_49f_bucket}/mdpf/${local.gw_49f_long}/platinum/aum_metrics/*",
                "arn:aws:s3:::${local.gw_49f_bucket}/mdpf/${local.gw_49f_long}/state/aum_metrics/*",
                "arn:aws:s3:::${local.gw_49f_bucket}/mdpf/${local.gw_49f_long}/gold/*",
                "arn:aws:s3:::opal-data-49financial/mdpf/49financial/gold/aum_metrics/*"):
        if not grant_faults([bad]):
            f.append(f"mutant not refused: {bad}")
    return "platinum, state, wildcard and typed-bucket grants refused; a correct set passes"


arm("NAMES: one opal_name module per firm (function gold-writer, kind role), the role named by it, none typed", a_names)
arm("GRANT: each role's S3 grants are its firm bucket or its firm gold prefix of the four artifacts only", a_grant)
arm("TRUST: each role trusts mdpf-gold-lambda, the Lambda may assume it, gold-lambda.tf passes its ARN", a_trust)
arm("GLOBAL: the gold Lambda's own role may write the composite gold of the four artifacts in opal-data-mdpf", a_global)
arm("ADMITTED: the live DenyForeignFirmPrincipals admits each name() role with no edit", a_admitted)
arm("PLANTED: the grant comparator refuses platinum, state, wildcard and typed-bucket grants", a_planted)

ok = 0
for label, passed, detail in arms:
    ok += passed
    print(f"{'ARM PASS' if passed else 'ARM FAIL'} {label} :: {detail}")
print(f"ROUND 1 GOLD WRITERS: {ok} of {len(arms)} arms")
sys.exit(0 if ok == len(arms) else 1)
