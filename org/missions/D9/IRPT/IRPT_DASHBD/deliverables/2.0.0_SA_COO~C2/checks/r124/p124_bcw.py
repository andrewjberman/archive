"""IRPT_DASHBD round 123, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- the Cottonwood account_dim NEVER-WIDEN PACKET (unsigned), cell DB-c-19.

  DBC124-1-AC1 the record and the packet agree with a FRESH read made here (gold prefix empty, pinned date in both silver tables), the names and the key equal builder output,
               the packet carries its eight headings in order and the word UNSIGNED, no signature state, no write counter above zero
  DBC124-2-AC1 the bounds: only the worker's folder, the channel and the order changed; the packet blob hash is printed

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

BASE = (HERE / "BASE_R124.txt").read_text(encoding="ascii").strip()
D = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = D + "deliverables/0.9.0_WK_IRPT_DASHBD~412/"
PACKET = FOLDER + "NEVER_WIDEN_PACKET_DB-c-19_R123_ACCOUNT_DIM.md"
RECORD = FOLDER + "ACCOUNT_DIM_PACKET_READS_R123.json"
ALLOWED = (FOLDER, D + "surprise-channel/investigations/INVESTIGATION_v1.md",
           D + "task-orders/IRPT_DASHBD.TO-DB-c-19.cottonwood-account-dim-never-widen-packet-unsigned.md")
HEADINGS = ("## Change set", "## Function", "## Catch-up first", "## Keys written", "## Both branches", "## Rollback",
            "## Questions for the CTO's half", "## Not in this packet")
TABLES = ("fact_holdings", "fact_allocations")


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root)] + list(args), capture_output=True, text=True, timeout=60)
    need(r.returncode == 0, "git %s failed rc=%s: %s" % (args[0], r.returncode, r.stderr.strip()[:200]))
    return r.stdout


def builder_names(naming):
    f = "account-dim"
    return (naming.name("irpt", "cottonwood", f, "lambda"), naming.name("irpt", "cottonwood", f, "role"),
            naming.name("irpt", "cottonwood", f, "policy"), naming.name("irpt", "cottonwood", f, "role", "scheduler"),
            naming.name("irpt", "cottonwood", f, "policy", "scheduler"), naming.name("irpt", "cottonwood", f, "daily"))


def silver_prefixes(root):
    """(bucket, prefix) of each silver table, from the Lambda's own silver_locations() (run un-isolated: the trading calendar needs user site packages)."""
    code = ("import json,sys; sys.path.insert(0,'infra/aws/lambda/investor-reporting/account-dim-cot'); import lambda_function as L; "
            "print(json.dumps(L.silver_locations('2000-01-03')))")
    r = subprocess.run([sys.executable, "-c", code], cwd=str(root), capture_output=True, text=True, timeout=100)
    need(r.returncode == 0, "silver_locations failed: " + r.stderr.strip()[-200:])
    locs = json.loads(r.stdout.strip().splitlines()[-1])
    out = {}
    need(set(locs) == set(TABLES), "silver_locations tables unexpected: %s" % sorted(locs))
    for tbl in TABLES:
        b, k = locs[tbl]
        need(k.endswith("date=2000-01-03/data.parquet"), "silver key shape unexpected")
        out[tbl] = (b, k[: -len("date=2000-01-03/data.parquet")])
    return out


def ac_1(root):
    root = Path(root)
    naming, _cal = p114.lib(root)
    rec = p114.load(root, RECORD)
    p114.no_identifiers(rec)
    need(rec.get("claim") == "measured" and rec.get("pushed") is False and rec.get("deployed") is False, "record flags")
    need(rec["reads"].get("writes") == 0, "a write counter above 0")
    need((root / PACKET).is_file(), "packet absent")
    text = (root / PACKET).read_text(encoding="utf-8")
    need(text.lstrip().startswith("# "), "no title line")
    need(re.search(r"Status:\s*UNSIGNED", text) is not None and "UNSIGNED" in text, "the UNSIGNED status line is absent")
    need(re.search(r"(?im)^\s*(signed by|signature|approved by)\s*:", text) is None, "a signature state is present")
    pos = []
    for h in HEADINGS:
        i = text.find("\n" + h)
        need(i >= 0, "heading absent: " + h)
        pos.append(i)
    need(pos == sorted(pos), "headings out of order")
    for n in builder_names(naming):
        need(n in text, "builder name absent from the packet: " + n)
    s3 = p114.s3client()
    pre = silver_prefixes(root)
    fresh = {t: set(p114.list_dates(s3, b, p)) for t, (b, p) in pre.items()}
    sec = text[text.index("\n## Keys written"):text.index("\n## Both branches")]
    dates = sorted(set(re.findall(r"date=(\d{4}-\d{2}-\d{2})/data\.parquet", sec)))
    need(len(dates) == 1, "the Keys written section must name exactly one date: %s" % dates)
    day = dates[0]
    need(all(day in fresh[t] for t in TABLES), "the pinned date is not a partition of both silver tables in a fresh LIST")
    need(rec["silver"]["common_newest"] == day, "common_newest in the record differs from the pinned date")
    uri = naming.address("irpt", "cottonwood", "gold", "account_dim", "date=%s" % day) + "/data.parquet"
    need(uri in sec, "the key (address() output) is absent from Keys written: " + uri)
    gb, gk = re.match(r"s3://([^/]+)/(.*)date=%s/data\.parquet$" % day, uri).groups()
    keys = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=gb, Prefix=gk):
        keys += [o["Key"] for o in page.get("Contents", [])]
    need(rec["gold_account_dim"]["object_count"] == 0 and len(keys) == 0, "the account_dim gold prefix is not empty in a fresh LIST (%d objects)" % len(keys))
    for k in ("function", "role", "scheduler_role", "schedule"):
        need(rec["exists"].get(k) in ("ABSENT", "EXISTS", "REFUSED"), "exists result missing: " + k)


def ac_2(root):
    root = Path(root)
    need((root / PACKET).is_file(), "packet absent")
    changed = sorted({p for p in git(root, "log", "--first-parent", "--no-merges", "--name-only", "--format=", BASE + "..HEAD").splitlines() if p.strip()})
    need(changed, "nothing changed since the base")
    extra = [p for p in changed if not any(p == a or (a.endswith("/") and p.startswith(a)) for a in ALLOWED)]
    need(not extra, "files outside the grant changed: " + ", ".join(extra[:5]))
    print("packet blob " + git(root, "hash-object", PACKET).strip())


ARMS = {"DBC124-1-AC1": ac_1, "DBC124-2-AC1": ac_2}


def main(argv):
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
