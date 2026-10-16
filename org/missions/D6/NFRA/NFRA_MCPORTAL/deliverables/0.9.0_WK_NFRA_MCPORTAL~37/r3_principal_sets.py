"""MP-pf-7 (R3) comparator: the People view's principal set against a raw read of the grant store.

Standard library only; Python 3.9 compatible.

compare(page_set, raw_set) returns the set sizes after de-duplication, the two one-sided differences,
`vacuous` (both sets empty) and `equal` (both differences 0 AND not vacuous).

CLI: python r3_principal_sets.py --from-read <file> --out r3_run.json
  <file> is the stdout of pf7.run.sh. Lines read:
    SIM identity=... table_arn_ok=... Scan=... DescribeTable=... OperatorRoleScan=...
    RAW {json}      complete, pages, per_page, count, scanned, policy_items, raw_set, raw_n, audit_only_principals
    ssm command=<id> status=<s>
    R3PAGE {json}   page_set, page_n
    RESULT: READ | RESULT: STOP
  Exit 3 and no run file when the file ends RESULT: STOP (the SIM line is printed).
  Exit 2 and no run file when the file lacks a RAW or an R3PAGE line (or a SIM line, or a RESULT line).
  The raw set is never written; only digests are compared and counted here.
"""
import argparse
import json
import re
import sys


def compare(page_set, raw_set):
    page = set(page_set)
    raw = set(raw_set)
    only_page = page - raw
    only_raw = raw - page
    vacuous = (not page) and (not raw)
    equal = (not only_page) and (not only_raw) and (not vacuous)
    return {
        "page_n": len(page),
        "raw_n": len(raw),
        "only_page_n": len(only_page),
        "only_raw_n": len(only_raw),
        "equal": equal,
        "vacuous": vacuous,
    }


SIM_RE = re.compile(r"^SIM\s+(.*)$")
SSM_RE = re.compile(r"^ssm\s+command=(\S+)\s+status=(\S+)\s*$")


def _kv(text):
    out = {}
    for tok in text.split():
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
    return out


def _json_after(prefix, line):
    return json.loads(line[len(prefix):])


def parse_read(lines):
    """Return a dict with keys sim, raw, ssm, page, result (None where a line is absent)."""
    found = {"sim": None, "raw": None, "ssm": None, "page": None, "result": None}
    for raw_line in lines:
        line = raw_line.rstrip("\r\n")
        m = SIM_RE.match(line)
        if m and found["sim"] is None:
            found["sim"] = _kv(m.group(1))
            continue
        if line.startswith("RAW ") and found["raw"] is None:
            found["raw"] = _json_after("RAW ", line)
            continue
        m = SSM_RE.match(line)
        if m and found["ssm"] is None:
            found["ssm"] = {"command": m.group(1), "status": m.group(2)}
            continue
        if line.startswith("R3PAGE ") and found["page"] is None:
            found["page"] = _json_after("R3PAGE ", line)
            continue
        if line.startswith("RESULT:"):
            found["result"] = line[len("RESULT:"):].strip()
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description="MP-pf-7 comparator: People view set against raw read")
    ap.add_argument("--from-read", required=True, help="stdout of pf7.run.sh")
    ap.add_argument("--out", required=True, help="run file to write (r3_run.json)")
    args = ap.parse_args(argv)

    with open(args.from_read, encoding="utf-8") as fh:
        found = parse_read(fh.readlines())

    if found["result"] == "STOP":
        sim = found["sim"] or {}
        print("SIM " + " ".join("%s=%s" % (k, v) for k, v in sim.items()))
        print("STOP: the read ended RESULT: STOP; no run file written")
        return 3

    if found["sim"] is None or found["raw"] is None or found["page"] is None:
        missing = [name for name, key in (("SIM", "sim"), ("RAW", "raw"), ("R3PAGE", "page")) if found[key] is None]
        print("ERROR: read file lacks %s; no run file written" % ", ".join(missing))
        return 2
    if found["result"] != "READ":
        print("ERROR: read file has no RESULT: READ line (got %r); no run file written" % found["result"])
        return 2

    raw = found["raw"]
    page = found["page"]
    sim = found["sim"]
    ssm = found["ssm"] or {"command": "NONE", "status": "NONE"}
    raw_set = raw.get("raw_set") or []
    page_set = page.get("page_set") or []
    cmp = compare(page_set, raw_set)

    run = {
        "sim_scan": sim.get("Scan"),
        "sim_operator_role_scan": sim.get("OperatorRoleScan"),
        "raw_complete": raw.get("complete"),
        "raw_pages": raw.get("pages"),
        "raw_count": raw.get("count"),
        "raw_scanned": raw.get("scanned"),
        "raw_n": raw.get("raw_n"),
        "policy_items": raw.get("policy_items"),
        "audit_only_principals": raw.get("audit_only_principals"),
        "page_n": page.get("page_n"),
        "only_page_n": cmp["only_page_n"],
        "only_raw_n": cmp["only_raw_n"],
        "equal": cmp["equal"],
        "vacuous": cmp["vacuous"],
        "ssm_status": ssm["status"],
        "ssm_command": ssm["command"],
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(run, fh, indent=2)
        fh.write("\n")
    print("OK: wrote %s equal=%s only_page_n=%s only_raw_n=%s vacuous=%s page_n=%s raw_n=%s"
          % (args.out, run["equal"], run["only_page_n"], run["only_raw_n"], run["vacuous"],
             run["page_n"], run["raw_n"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
