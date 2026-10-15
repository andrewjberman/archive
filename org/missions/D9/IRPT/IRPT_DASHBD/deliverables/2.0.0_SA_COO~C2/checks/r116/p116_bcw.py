"""IRPT_DASHBD round 116, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the Cottonwood holdings-performance function build (repo files only) and the Black Diamond account-return read.

  DB-c-7 (~404) BUILD, LOCAL (repo files; nothing is applied, planned or uploaded):
      DBC116-1-AC1 the handler's catch-up planner fails loud on a refused listing, its other three behaviours are unchanged, and the planted test passes
      DBC116-2-AC1 the Terraform root carries the Cottonwood function, roles, policy and schedule (created DISABLED at cron(15 8 ? * MON-FRI *) America/New_York), additive only
      DBC116-3-AC1 nothing existing moved: the 49 Financial and Inflection blocks are byte-unchanged (no removed line in the four .tf files; handler.py changes only inside _days_to_compute)
  DB-c-8 (~405) the Black Diamond Cottonwood layers: which tables carry an account-level return series, at what grain. A READ.                       DBC116-4-AC1

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import datetime as dt
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

BASE = "7f16db08c3"  # the commit this round was issued at (the worker branches are cut from it); the unchanged-blocks arm diffs against it
H = "infra/aws/lambda/investor-reporting/holdings-performance/"
T = "infra/aws/terraform/investor-reporting/holdings-performance/"
TF = [T + n for n in ("iam.tf", "lambda.tf", "locals.tf", "schedule.tf")]
HANDLER = H + "handler.py"
NEWTEST = H + "tests/test_refused_listing_fails_loud.py"
OLDTEST = H + "tests/test_catch_up.py"
REC4 = p114.D + "0.9.0_WK_IRPT_DASHBD~405/BD_RETURNS_READ_R116.json"
BD_BUCKET = "opal-data-assets"
BD_ROOT = "blackdiamond/cottonwood/"
VERDICTS = ("ACCOUNT_RETURN_SERIES", "ACCOUNT_VALUE_ONLY", "HOLDINGS_ONLY", "NOT_ESTABLISHED")
RETURN_LIKE = re.compile(r"return|twr|perf|pnl|gain|roi|irr", re.I)


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, encoding="utf-8")
    need(r.returncode == 0, "git " + " ".join(args[:2]) + " failed: " + r.stderr[:120])
    return r.stdout


def func_range(src, name):
    m = re.search(r"^def %s\(" % re.escape(name), src, re.M)
    need(m is not None, "function absent: " + name)
    start = src[: m.start()].count("\n") + 1
    nxt = re.search(r"^(def |class )", src[m.end():], re.M)
    end = (src[: m.end() + nxt.start()].count("\n")) if nxt else src.count("\n") + 1
    return start, end


def load_handler(root):
    sys.path.insert(0, str(Path(root)))
    sys.path.insert(0, str(Path(root) / "lib"))
    sys.path.insert(0, str(Path(root) / "data/assets/scripts/gold/irpt_holdings_performance"))
    import types
    stub = types.ModuleType("holdings_performance")
    stub.main = lambda argv: 0
    stub.TABLE_DAILY = "holdings_performance_daily"
    sys.modules["holdings_performance"] = stub
    spec2 = importlib.util.spec_from_file_location("hp_handler_r116", str(Path(root) / HANDLER))
    m = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(m)
    return m


def ac_1(root):
    src = (Path(root) / HANDLER).read_text(encoding="utf-8")
    need("computing the single day" not in src, "the single-day fallback print is still in the handler")
    a, b = func_range(src, "_days_to_compute")
    body = "\n".join(src.splitlines()[a - 1: b])
    need(re.search(r"^\s+raise\b", body, re.M) is not None, "_days_to_compute holds no raise")
    m = load_handler(root)
    now = dt.datetime(2026, 10, 15, 12, 15, tzinfo=dt.timezone.utc)

    def bad(_s):
        raise PermissionError("AccessDenied")

    raised = False
    try:
        m._days_to_compute(now, {"source": "blackdiamond_z09"}, lister=bad)
    except Exception:
        raised = True
    need(raised, "a refused listing did not raise")
    need(m._days_to_compute(now, {"date": "2026-10-09"}, lister=bad) == ["2026-10-09"], "the manual-date path changed")
    need(m._days_to_compute(now, {"source": "x"}, lister=lambda s: []) == ["2026-10-14"], "the no-landed-day path changed")
    need(m._days_to_compute(now, {"source": "x"}, lister=lambda s: ["2026-10-14"]) == [], "the already-landed path changed")
    need(m._days_to_compute(now, {"source": "x"}, lister=lambda s: ["2026-10-08", "2026-10-09"]) == ["2026-10-12", "2026-10-13", "2026-10-14"], "the catch-up window path changed")
    nt = Path(root) / NEWTEST
    need(nt.is_file() and "def test_refused_listing_fails_loud" in nt.read_text(encoding="utf-8"), "the planted test is absent")
    r = subprocess.run([sys.executable, "-m", "pytest", str(nt), str(Path(root) / OLDTEST), "-q", "-p", "no:cacheprovider"], capture_output=True, text=True, cwd=str(root), timeout=110)
    need(r.returncode == 0 and re.search(r"\d+ passed", r.stdout) is not None and "failed" not in r.stdout, "pytest on the planted test and the catch-up tests did not pass: " + r.stdout[-200:])


def block_of(text, header_re):
    m = re.search(header_re, text)
    need(m is not None, "block absent: " + header_re)
    i = text.find("{", m.end() - 1)
    depth = 0
    for j in range(i, len(text)):
        depth += text[j] == "{"
        depth -= text[j] == "}"
        if depth == 0:
            return text[m.start(): j + 1]
    raise Fail("unbalanced block: " + header_re)


def ac_2(root):
    txt = {f: (Path(root) / f).read_text(encoding="utf-8") for f in TF}
    allt = "\n".join(txt.values())
    for label in ('module "irpt_holdings_performance_cot_lambda_name"', 'module "irpt_holdings_performance_cot"', 'resource "aws_iam_role" "irpt_holdings_performance_cot"',
                  'data "aws_iam_policy_document" "irpt_holdings_performance_cot"', 'resource "aws_iam_role_policy" "irpt_holdings_performance_cot"',
                  'resource "aws_iam_role" "irpt_holdings_performance_cot_scheduler"', 'resource "aws_scheduler_schedule" "irpt_holdings_performance_cot"'):
        need(label in allt, "Cottonwood block absent: " + label)
    sched = block_of(allt, r'resource "aws_scheduler_schedule" "irpt_holdings_performance_cot"\s*\{')
    need(re.search(r'state\s*=\s*"DISABLED"', sched), "the Cottonwood schedule is not created DISABLED")
    need("cron(15 8 ? * MON-FRI *)" in sched and "America/New_York" in sched, "the Cottonwood schedule is not cron(15 8 ? * MON-FRI *) America/New_York")
    need("blackdiamond_z09" in sched, "the trigger input does not name source blackdiamond_z09")
    need("irpt_holdings_performance_cot" in sched and "irpt_holdings_performance_cot.function_arn" in sched, "the schedule does not target the Cottonwood function")
    pol = block_of(allt, r'data "aws_iam_policy_document" "irpt_holdings_performance_cot"\s*\{')
    need(not re.search(r"s3:Delete|s3:\*|\"\*\"\s*\]?\s*$", pol, re.M), "the Cottonwood policy grants a delete or a wildcard action")
    need(re.search(r's3:PutObject', pol) is not None, "the Cottonwood policy has no PutObject statement")
    need("irpt_hp_cot_gold_write_arns" in pol or "gold_write_arns" in pol, "the PutObject statement does not use a Cottonwood write-arn local")
    block_of(allt, r'resource "aws_iam_role" "irpt_holdings_performance_cot"\s*\{')
    need("lambda.amazonaws.com" in allt, "no lambda trust policy")
    try:
        r = subprocess.run(["terraform", "fmt", "-check", "-diff", str(Path(root) / T)], capture_output=True, text=True)
    except FileNotFoundError:
        r = None  # no terraform binary on this box: the structural arms above stand alone
    if r is not None and r.returncode == 3:
        raise Fail("terraform fmt -check reports unformatted files: " + r.stdout[:160])
    removed_apply = re.search(r'terraform apply|aws lambda update-function-code', allt)
    need(removed_apply is None, "an apply command text is in the Terraform")


def numstat_removed(root, files):
    out = git(root, "diff", "--numstat", BASE, "--", *files)
    rows = [ln.split("\t") for ln in out.splitlines() if ln.strip()]
    return {r[2]: (int(r[0]) if r[0].isdigit() else 0, int(r[1]) if r[1].isdigit() else 0) for r in rows}


def ac_3(root):
    ns = numstat_removed(root, TF)
    for f, (added, removed) in ns.items():
        need(removed == 0, "removed lines in an existing Terraform file: %s (%d)" % (f, removed))
    need(sum(a for a, _ in ns.values()) > 0, "no Terraform line was added: the build is absent")
    base_src = git(root, "show", BASE + ":" + HANDLER)
    a, b = func_range(base_src, "_days_to_compute")
    d = git(root, "diff", "-U0", BASE, "--", HANDLER)
    for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", d, re.M):
        s, n = int(m.group(1)), int(m.group(2) or 1)
        need(n == 0 and a - 1 <= s <= b or (a <= s and s + n - 1 <= b), "handler.py changes outside _days_to_compute at base lines %d-%d" % (s, s + n - 1))
    other = git(root, "diff", "--name-only", BASE, "--", T, H, "data/assets/scripts/gold/irpt_holdings_performance")
    allowed = set(TF) | {HANDLER, NEWTEST, OLDTEST}
    allowed |= {ln for ln in other.splitlines() if ln.startswith(H + "tests/") and "refused_listing" in ln}
    extra = [ln for ln in other.splitlines() if ln and ln not in allowed]
    need(not extra, "files changed outside the order's surface: " + ", ".join(extra[:4]))


class RangeFile(io.RawIOBase):
    def __init__(self, s3, bucket, key):
        self.s3, self.b, self.k = s3, bucket, key
        self.size = s3.head_object(Bucket=bucket, Key=key)["ContentLength"]
        self.pos = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        return self.pos

    def readinto(self, buf):
        n = len(buf)
        if self.pos >= self.size:
            return 0
        end = min(self.size - 1, self.pos + n - 1)
        body = self.s3.get_object(Bucket=self.b, Key=self.k, Range="bytes=%d-%d" % (self.pos, end))["Body"].read()
        buf[: len(body)] = body
        self.pos += len(body)
        return len(body)


def schema_columns(s3, bucket, key):
    import pyarrow as pa
    import pyarrow.parquet as pq
    return sorted(pq.read_schema(pa.PythonFile(RangeFile(s3, bucket, key), mode="r")).names)


def table_prefixes(s3, bucket, root):
    out = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=root, Delimiter="/"):
        out += [c["Prefix"] for c in pg.get("CommonPrefixes", [])]
    return out


def ac_4(root):
    r = p114.load(root, REC4)
    p114.no_identifiers(r)
    need(r.get("claim") in p114.CLAIMS, "claim missing")
    need(r["verdict"] in VERDICTS and r["words"].strip() != "" and r["grain_words"].strip() != "", "verdict, words or grain_words missing")
    s3 = p114.s3client()
    layers = sorted(table_prefixes(s3, BD_BUCKET, BD_ROOT))
    need(sorted(lay_["prefix"] for lay_ in r["layers"]) == layers, "the recorded layers differ from a fresh LIST of " + BD_ROOT)
    ret_like = []
    for lay in r["layers"]:
        tabs = sorted(table_prefixes(s3, BD_BUCKET, lay["prefix"]))
        need(sorted(t["prefix"] for t in lay["tables"]) == tabs, "the recorded tables differ from a fresh LIST of " + lay["prefix"])
        for t in lay["tables"]:
            ds = p114.list_dates(s3, BD_BUCKET, t["prefix"])
            if not ds:
                need(t["partition_count"] == 0, "partition_count differs from a fresh LIST for " + t["prefix"])
                continue
            need(t["partition_count"] == len(ds) and t["newest_date"] == max(ds), "partition_count or newest_date differs from a fresh LIST for " + t["prefix"])
            newest = None
            pg = s3.get_paginator("list_objects_v2")
            for page in pg.paginate(Bucket=BD_BUCKET, Prefix=t["prefix"] + "date=" + max(ds) + "/"):
                for o in page.get("Contents", []):
                    if o["Key"].endswith(".parquet") and newest is None:
                        newest = o["Key"]
            if newest is None:
                need(t["columns"] == [], "columns recorded for a table with no parquet object: " + t["prefix"])
                continue
            cols = schema_columns(s3, BD_BUCKET, newest)
            need(t["columns"] == cols, "columns differ from a fresh footer read for " + t["prefix"])
            ret_like += [t["prefix"] + ":" + c for c in cols if RETURN_LIKE.search(c)]
    need(sorted(r["return_like_columns"]) == sorted(ret_like), "return_like_columns differ from the recomputed set")
    if r["verdict"] == "ACCOUNT_RETURN_SERIES":
        need(len(ret_like) > 0, "ACCOUNT_RETURN_SERIES needs at least one return-like column")
    rd = r["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes")), "a write is recorded")
    need(r.get("pushed") is False and r.get("deployed") is False, "side-effect flags")


ARMS = {"DBC116-1-AC1": ac_1, "DBC116-2-AC1": ac_2, "DBC116-3-AC1": ac_3, "DBC116-4-AC1": ac_4}


def selftest(root):
    src = "x = 1\n\ndef a(b):\n    return 1\n\ndef _days_to_compute(n):\n    return 2\n\n\ndef z():\n    pass\n"
    need(func_range(src, "_days_to_compute") == (6, 9), "func_range arm: %s" % (func_range(src, "_days_to_compute"),))
    tf = 'resource "x" "y" {\n  a = { b = 1 }\n}\nresource "q" "r" {\n}\n'
    need(block_of(tf, r'resource "x" "y"\s*\{').endswith("}\n}") or block_of(tf, r'resource "x" "y"\s*\{').count("{") == 2, "block_of arm")
    need(RETURN_LIKE.search("daily_twr") and not RETURN_LIKE.search("market_value"), "RETURN_LIKE arm")
    h = load_handler(root)
    need(callable(getattr(h, "_days_to_compute", None)), "handler import arm")
    print("SELFTEST PASS")


def main(argv):
    if argv and argv[0] == "--selftest":
        try:
            selftest(argv[1] if len(argv) > 1 else ".")
        except Fail as e:
            print("SELFTEST FAIL: " + str(e))
            return 1
        return 0
    root, cid = argv[0], argv[1]
    try:
        need(cid in ARMS, "unknown criterion " + cid)
        ARMS[cid](root)
    except Fail as e:
        print(str(e))
        print(cid + " FAIL")
        return 1
    except Exception as e:
        print("checker error: " + type(e).__name__ + ": " + str(e)[:200])
        print(cid + " FAIL")
        return 1
    print(cid + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
