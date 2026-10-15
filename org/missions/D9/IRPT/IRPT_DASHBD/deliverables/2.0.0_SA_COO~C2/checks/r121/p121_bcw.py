"""IRPT_DASHBD round 121, workstream B-CW (issuer 2.0.0_SA_COO~C2) -- how each firm's gold account_dim is written, read before the Cottonwood account_dim producer is designed.

  DBC121-1-AC1 the record: for the three firms (49financial, inflection, cottonwood) the gold account_dim table's state (fresh LIST), the repo code that writes it, the Terraform function/role/schedule labels and cron
               that run it (each named file exists and carries the label), the Cottonwood adapter's state, and the verdict

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p114", str(HERE.parent / "r114" / "p114_bcw.py"))
p114 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p114)
Fail, need = p114.Fail, p114.need

REC = p114.D + "0.9.0_WK_IRPT_DASHBD~408/ACCOUNT_DIM_WRITER_PATTERN_R121.json"
FIRMS = ("49financial", "inflection", "cottonwood")
VERDICTS = ("PATTERN_EXISTS_FOR_49F", "NO_49F_WRITER", "NOT_ESTABLISHED")
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py"


def ac_1(root):
    naming, cal = p114.lib(root)
    r = p114.load(root, REC)
    p114.no_identifiers(r)
    need(r.get("claim") in p114.CLAIMS, "claim missing")
    need(r["verdict"] in VERDICTS and r["words"].strip() != "", "verdict or words missing")
    need(sorted(r["firms"]) == sorted(FIRMS), "firms are not the three")
    s3 = p114.s3client()
    for f in FIRMS:
        row = r["firms"][f]
        b, pfx = split_prefix(naming, f)
        dates = p114.list_dates(s3, b, pfx)
        need(row["partition_count"] == len(dates), "partition_count differs from a fresh LIST for " + f)
        need(row["newest_date"] == (max(dates) if dates else None), "newest_date differs from a fresh LIST for " + f)
        for w in row["writers"]:
            p = Path(root) / w["file"]
            need(p.is_file(), "writer file absent: " + w["file"])
            need("account_dim" in p.read_text(encoding="utf-8", errors="replace"), "writer file does not name account_dim: " + w["file"])
        need(row["writer_count"] == len(row["writers"]), "writer_count differs from the list for " + f)
        for t in row["terraform"]:
            p = Path(root) / t["file"]
            need(p.is_file() and t["label"] in p.read_text(encoding="utf-8"), "terraform label absent in file: %s %s" % (t["file"], t["label"]))
        if row["writer_count"] == 0:
            need(row["none_words"].strip() != "" and row["claim"] in ("absent", "inferred"), "zero writers need none_words and a claim of absent or inferred: " + f)
    ad = r["cottonwood_adapter"]
    need(ad["file"] == ADAPTER and (Path(root) / ADAPTER).is_file(), "the adapter file is not the known one")
    need(ad["upload_refused"] is ("NotImplementedError" in (Path(root) / ADAPTER).read_text(encoding="utf-8")), "upload_refused differs from the adapter's source")
    need(r["cottonwood_inputs"]["words"].strip() != "" and len(r["cottonwood_inputs"]["tables"]) >= 1, "the adapter's inputs are not recorded")
    if r["verdict"] == "PATTERN_EXISTS_FOR_49F":
        need(r["firms"]["49financial"]["writer_count"] >= 1 and len(r["firms"]["49financial"]["terraform"]) >= 1, "PATTERN_EXISTS_FOR_49F needs a 49 Financial writer and its Terraform labels")
    rd = r["reads"]
    need(all(rd.get(k) == 0 for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads", "aws_writes")), "a write is recorded")
    need(r.get("pushed") is False and r.get("deployed") is False, "side-effect flags")


def split_prefix(naming, firm):
    a = naming.address("irpt", firm, "gold", "account_dim", "date=2000-01-03")
    m = re.match(r"s3://([^/]+)/(.*)date=2000-01-03$", a)
    need(m is not None, "address() shape unexpected for " + firm)
    return m.group(1), m.group(2)


ARMS = {"DBC121-1-AC1": ac_1}


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
