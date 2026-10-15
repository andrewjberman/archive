"""IRPT_DASHBD round 121, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-243, the THREE GRANTS of hop 1 as a Terraform EDIT (CTO analysis @9d4bd6adf3 ruling 1):
the reporting-gold role gains (1) PutObject on the one `filled_report_values` gold prefix, (2) GetObject on the one served model-series object, (3) GetObject and a
prefix-conditioned ListBucket on the one household crosswalk prefix; explicit, no wildcard; written in the Terraform FILES only (nothing planned, applied or
deployed: the plan 0 add / 2 change / 0 destroy belongs to the applier).

  DB-b-243 (~197) iam.tf and locals.tf of infra/aws/terraform/investor-reporting/reporting-gold gain the grants, ADDITIVELY; a facts record names each grant's
                  resolved ARNs, which the checker recomputes from the naming builder and the module's own constants.
                                                                                           DB121-2-AC1 (the HCL: explicit actions, no wildcard, derived not typed),
                                                                                           DB121-2-AC2 (additive; no other Terraform file),
                                                                                           DB121-2-AC3 (the facts: resolved ARNs equal the recount, plan 0/2/0)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the clauses on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~197/RD_GRANTS_FACTS_R121.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-243.hop-1-grants-in-the-reporting-gold-terraform.md"
TF_DIR = "infra/aws/terraform/investor-reporting/reporting-gold/"
IAM_REL = TF_DIR + "iam.tf"
LOC_REL = TF_DIR + "locals.tf"
MODULE_REL = "data/assets/scripts/gold/irpt_reporting/filled_report_values.py"
ADAPTER_REL = "data/assets/scripts/gold/irpt_reporting/adapters/model_series_windows.py"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
ALLOWED_ACTIONS = {"s3:GetObject", "s3:ListBucket", "s3:PutObject"}
PLAN_RESOURCES = ["aws_iam_role_policy.irpt_reporting_gold", "module.irpt_reporting_gold.aws_lambda_function.this"]
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "arn", "arns", "list_prefix_pattern", "resources")
HEX64 = re.compile(r"[0-9a-f]{64}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True).stdout


def base_commit(root):
    out = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL).split()
    need(out, "the order's first commit is not in this history")
    return out[-1]


def numstat(root, base, rel):
    out = git(root, "diff", "--numstat", base, "HEAD", "--", rel).strip().split("\n")[0].split("\t")
    need(len(out) >= 2 and out[0].isdigit() and out[1].isdigit(), "no change recorded for %s" % rel)
    return int(out[0]), int(out[1])


def own_commits(root, author):
    """The commits of this order's worker (author serial), oldest first, since the order was issued: the diff clauses read these commits only, never a whole-repo base..HEAD
    (other seats commit to the same trunk). Round 122 ruling 3."""
    base = base_commit(root)
    out = git(root, "log", "--reverse", "--format=%H", "--author=" + author, base + "..HEAD").split()
    need(out, "no commit by %s since the order was issued" % author)
    return out


def own_numstat(root, commits, rel):
    add = dele = 0
    for c in commits:
        for ln in git(root, "show", "--numstat", "--format=", c, "--", rel).strip().splitlines():
            parts = ln.split("	")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                add += int(parts[0])
                dele += int(parts[1])
    return add, dele


def own_files(root, commits):
    names = set()
    for c in commits:
        names |= set(git(root, "show", "--name-only", "--format=", c).split())
    return names


def strip_comments(text):
    return "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))


def statements(text):
    """{sid: block text} of the statement blocks of an aws_iam_policy_document."""
    out = {}
    for m in re.finditer(r"statement\s*\{", text):
        depth, i = 1, m.end()
        while depth and i < len(text):
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        blk = text[m.start():i]
        s = re.search(r'sid\s*=\s*"([^"]+)"', blk)
        if s:
            out[s.group(1)] = blk
    return out


def block_actions(blk):
    m = re.search(r"actions\s*=\s*\[([^\]]*)\]", blk)
    return re.findall(r'"([^"]+)"', m.group(1)) if m else []


# ------------------------------------------------------------------------------------------------ the HCL clauses (pure)
def check_hcl(iam, loc, base_iam, module_table, adapter_ok=True):
    ic, lc = strip_comments(iam), strip_comments(loc)
    st, base_st = statements(ic), statements(strip_comments(base_iam))
    new = sorted(set(st) - set(base_st))
    need(len(new) >= 1, "iam.tf must gain at least one new statement (the served model series), found %d" % len(new))
    for sid, blk in st.items():
        acts = block_actions(blk)
        need(acts, "statement %s has no explicit actions list" % sid)
        need(all("*" not in a for a in acts), "statement %s has a wildcard action" % sid)
        need(set(acts) <= ALLOWED_ACTIONS | {"sts:AssumeRole", "logs:CreateLogStream", "logs:PutLogEvents", "dynamodb:GetItem"}, "statement %s has an action outside the allowed set: %s" % (sid, acts))
    for sid in new:
        need(set(block_actions(st[sid])) <= {"s3:GetObject", "s3:ListBucket"}, "new statement %s may only read or list" % sid)
    puts = [sid for sid, blk in st.items() if "s3:PutObject" in block_actions(blk)]
    need(len(puts) == 1 and "irpt_rg_gold_write_arns" in st[puts[0]], "exactly one PutObject statement must remain, on irpt_rg_gold_write_arns (found %s)" % puts)
    need(re.search(r'irpt_rg_gold_table_filled\s*=\s*"%s"' % re.escape(module_table), lc), "locals.tf must define irpt_rg_gold_table_filled = %r (the module's TABLE)" % module_table)
    wa = re.search(r"irpt_rg_gold_write_arns\s*=\s*\[(.*?)\n\s*\]", lc, re.S)
    need(wa is not None and "filled" in wa.group(1), "irpt_rg_gold_write_arns must carry the filled prefix")
    need("model_series_windows.py" in (ic + lc), "the served model series must be read from the adapter's constants (model_series_windows.py), not typed")
    both = ic + lc
    need("opal-data-portal-v2" not in both and "model_portfolio_timeseries" not in both, "the served bucket or key is typed in the Terraform; derive it from the adapter file")
    need("household_crosswalk" in both, "the crosswalk grant must name the household_crosswalk table")
    need(not re.search(r'"arn:aws:s3:::\*', both) and 'resources = ["*"]' not in both, "an all-resources grant")
    return new


# ------------------------------------------------------------------------------------------------ the recount (naming builder + module constants)
def recount(root):
    sys.path.insert(0, str(root))
    from lib import opal_naming
    mod = (Path(root) / MODULE_REL).read_text(encoding="utf-8")
    ad = (Path(root) / ADAPTER_REL).read_text(encoding="utf-8")
    table = re.search(r'^TABLE\s*=\s*"([^"]+)"', mod, re.M).group(1)
    sb = re.search(r'^SERVED_BUCKET\s*=\s*"([^"]+)"', ad, re.M).group(1)
    sk = re.search(r'^SERVED_KEY\s*=\s*"([^"]+)"', ad, re.M).group(1)
    wa = opal_naming.address("irpt", FIRM, "gold", table, "date=2000-01-03", "data.parquet")
    wb, wk = wa[len("s3://"):].split("/", 1)
    wpre = wk.split("/date=", 1)[0] + "/"
    ca = opal_naming.address("advi", FIRM, "gold", "household_crosswalk", "date=2000-01-01", "x")
    cb, ck = ca[len("s3://"):].split("/", 1)
    cpre = ck.split("household_crosswalk/", 1)[0] + "household_crosswalk/"
    return {"table": table,
            "write_filled": {"actions": ["s3:PutObject"], "arns": ["arn:aws:s3:::%s/%s*" % (wb, wpre)]},
            "read_model_series": {"actions": ["s3:GetObject"], "arns": ["arn:aws:s3:::%s/%s" % (sb, sk)]},
            "read_crosswalk": {"actions": ["s3:GetObject", "s3:ListBucket"], "arns": ["arn:aws:s3:::%s/%s*" % (cb, cpre), "arn:aws:s3:::%s" % cb],
                               "list_prefix_pattern": cpre + "*"}}


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_facts(rec, truth, sha_of, file_exists):
    exp = {"firm", "files_changed", "grants", "expected_plan", "validated", "derivations", "words", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    fc = rec["files_changed"]
    need(isinstance(fc, list) and [f.get("file") for f in fc] == [IAM_REL, LOC_REL], "files_changed must be iam.tf then locals.tf")
    for f in fc:
        need(set(f) == {"file", "sha256", "kind"} and nes(f["kind"]) and file_exists(f["file"]) and HEX64.match(str(f["sha256"])) and sha_of(f["file"]) == f["sha256"],
             "files_changed entry %s: hash or form" % f.get("file"))
    g = rec["grants"]
    need(isinstance(g, list) and [x.get("id") for x in g] == ["write_filled", "read_model_series", "read_crosswalk"], "grants must be the three, in order")
    for x in g:
        t = truth[x["id"]]
        keys = {"id", "actions", "arns", "statement_ids", "words"} | ({"list_prefix_pattern"} if x["id"] == "read_crosswalk" else set())
        need(set(x) == keys and nes(x["words"]) and isinstance(x["statement_ids"], list) and x["statement_ids"] and all(nes(s) for s in x["statement_ids"]), "grant %s form" % x["id"])
        need(sorted(x["actions"]) == sorted(t["actions"]), "grant %s actions %s, expected %s" % (x["id"], x["actions"], t["actions"]))
        need(sorted(x["arns"]) == sorted(t["arns"]), "grant %s ARNs differ from the recount" % x["id"])
        if x["id"] == "read_crosswalk":
            need(x["list_prefix_pattern"] == t["list_prefix_pattern"], "crosswalk list prefix pattern differs from the recount")
    ep = rec["expected_plan"]
    need(isinstance(ep, dict) and set(ep) == {"to_add", "to_change", "to_destroy", "resources", "words"} and ep["to_add"] == 0 and ep["to_change"] == 2 and ep["to_destroy"] == 0
         and sorted(ep["resources"]) == PLAN_RESOURCES and nes(ep["words"]), "expected_plan must be 0 add / 2 change / 0 destroy on the two named resources")
    v = rec["validated"]
    need(isinstance(v, dict) and set(v) == {"ran", "words"} and isinstance(v["ran"], bool) and nes(v["words"]), "validated form (say whether terraform fmt or validate ran, and why not)")
    dv = rec["derivations"]
    need(isinstance(dv, dict) and set(dv) == {"served_series", "crosswalk", "filled_prefix"} and all(nes(dv[k]) for k in dv), "derivations form")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


def run(root, cid):
    root = Path(root)
    if cid == "DB121-2-AC1":
        base = base_commit(root)
        iam = (root / IAM_REL).read_text(encoding="utf-8")
        loc = (root / LOC_REL).read_text(encoding="utf-8")
        base_iam = git(root, "show", "%s:%s" % (base, IAM_REL))
        need(base_iam.strip(), "base iam.tf unreadable")
        table = re.search(r'^TABLE\s*=\s*"([^"]+)"', (root / MODULE_REL).read_text(encoding="utf-8"), re.M).group(1)
        new = check_hcl(iam, loc, base_iam, table)
        print("OK: iam.tf gains %d statements (%s); every action is explicit, no wildcard, one PutObject statement; the served series and crosswalk are derived" % (len(new), ", ".join(new)))
        return True
    if cid == "DB121-2-AC2":
        cs = own_commits(root, "0.9.0_WK_IRPT_DASHBD~197")
        ga, la = own_numstat(root, cs, IAM_REL)
        gb, lb = own_numstat(root, cs, LOC_REL)
        need(ga >= 12 and la <= 4, "iam.tf gains %d loses %d (needs gain >= 12, lose <= 4)" % (ga, la))
        need(gb >= 6 and lb <= 4, "locals.tf gains %d loses %d (needs gain >= 6, lose <= 4)" % (gb, lb))
        other = sorted(f for f in own_files(root, cs) if f.startswith("infra/aws/terraform/") and f not in (IAM_REL, LOC_REL))
        need(not other, "this worker's commits changed other Terraform files: %s" % other)
        print("OK: additive in the worker's own %d commits: iam.tf +%d/-%d, locals.tf +%d/-%d, no other Terraform file" % (len(cs), ga, la, gb, lb))
        return True
    if cid == "DB121-2-AC3":
        rec = load(root, REC_REL)
        truth = recount(root)
        check_facts(rec, truth, lambda rel: hashlib.sha256((root / rel).read_bytes()).hexdigest(), lambda rel: (root / rel).is_file())
        print("OK: grants facts: three grants, ARNs equal the recount from the builder and the module constants; plan 0/2/0 on the two resources")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    base_iam = 'data "x" "y" {\n statement {\n sid = "A"\n actions = ["s3:GetObject"]\n resources = local.r\n }\n statement {\n sid = "Wr"\n actions = ["s3:PutObject"]\n resources = local.irpt_rg_gold_write_arns\n }\n}\n'
    iam = base_iam + 'statement {\n sid = "Ms"\n actions = ["s3:GetObject"]\n resources = [local.ms]\n}\nstatement {\n sid = "Cw"\n actions = ["s3:GetObject", "s3:ListBucket"]\n resources = [local.cw]\n}\n'
    loc = 'locals {\n irpt_rg_gold_table_filled = "filled_report_values"\n x = file("adapters/model_series_windows.py")\n y = "household_crosswalk"\n irpt_rg_gold_write_arns = [\n  "a",\n  "${local.irpt_rg_gold_filled_prefix}",\n ]\n}\n'
    assert len(check_hcl(iam, loc, base_iam, "filled_report_values")) == 2

    def bad(i=iam, lo=loc, t="filled_report_values"):
        try:
            check_hcl(i, lo, base_iam, t)
            return False
        except Fail:
            return True
    assert bad(i=iam.replace('"s3:GetObject", "s3:ListBucket"', '"s3:*"'))
    assert bad(i=iam + 'statement {\n sid = "P2"\n actions = ["s3:PutObject"]\n resources = [local.q]\n}\n')
    assert bad(lo=loc.replace("filled_report_values", "other"))
    assert bad(lo=loc.replace("model_series_windows.py", "x.py"))
    assert bad(lo=loc + ' z = "opal-data-portal-v2"')
    assert bad(i=base_iam)
    truth = {"table": "t", "write_filled": {"actions": ["s3:PutObject"], "arns": ["a"]}, "read_model_series": {"actions": ["s3:GetObject"], "arns": ["b"]},
             "read_crosswalk": {"actions": ["s3:GetObject", "s3:ListBucket"], "arns": ["c", "d"], "list_prefix_pattern": "p*"}}
    rec = {"firm": FIRM, "files_changed": [{"file": IAM_REL, "sha256": "a" * 64, "kind": "terraform"}, {"file": LOC_REL, "sha256": "a" * 64, "kind": "terraform"}],
           "grants": [{"id": "write_filled", "actions": ["s3:PutObject"], "arns": ["a"], "statement_ids": ["W"], "words": "w"},
                      {"id": "read_model_series", "actions": ["s3:GetObject"], "arns": ["b"], "statement_ids": ["M"], "words": "w"},
                      {"id": "read_crosswalk", "actions": ["s3:ListBucket", "s3:GetObject"], "arns": ["d", "c"], "statement_ids": ["C"], "words": "w", "list_prefix_pattern": "p*"}],
           "expected_plan": {"to_add": 0, "to_change": 2, "to_destroy": 0, "resources": PLAN_RESOURCES, "words": "w"}, "validated": {"ran": False, "words": "no terraform on the box"},
           "derivations": {"served_series": "s", "crosswalk": "c", "filled_prefix": "f"}, "words": "w", "claim": "inferred", "files_in_repo": False, "served_values_changed": False,
           "pushed": False, "deployed": False}
    import copy
    assert check_facts(rec, truth, lambda r: "a" * 64, lambda r: True)
    for mutate in (lambda r: r["grants"][0].update(arns=["z"]), lambda r: r["expected_plan"].update(to_change=1), lambda r: r["grants"][2].update(list_prefix_pattern="q*"),
                   lambda r: r.update(deployed=True), lambda r: r["grants"].pop(), lambda r: r["files_changed"][0].update(sha256="b" * 64)):
        r = copy.deepcopy(rec)
        mutate(r)
        try:
            check_facts(r, truth, lambda x: "a" * 64, lambda x: True)
            raise AssertionError("a red arm passed")
        except Fail:
            pass
    print("selftest: 7 HCL arms and 7 record arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        root, cid = sys.argv[1], sys.argv[2]
        run(root, cid)
        print("%s PASS" % cid)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
