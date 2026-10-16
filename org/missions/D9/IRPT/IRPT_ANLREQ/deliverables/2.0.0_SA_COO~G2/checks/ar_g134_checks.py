"""IRPT_ANLREQ AR-g-134 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g134_checks.py verify <trace json>   the trace is well formed and every citation is real: the file parses; it names the report-generation entry points it
                                                   read; every dependency row carries a site "path:line" whose file exists at that line and whose recorded line_text equals
                                                   the file's line (after strip); every row says whether a Yahoo-priced holding needs it (YES or NO), what removes it, and
                                                   its claim word (MEASURED or INFERRED); the summary counts equal the rows; a row with needs=YES names the id source it uses
    python ar_g134_checks.py scope <base ref> <worker folder> <order path>   the branch changed only the worker's folder, the order and the channel file (vs the merge-base)

Prints one RESULT line: AR-G134-OK / AR-G134-FAIL (or -SCOPE-); rc 0 only on OK. ASCII only.
"""
import json
import os
import subprocess
import sys

CLAIMS = ("MEASURED", "INFERRED")
NEEDS = ("YES", "NO")
CHANNEL = "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md"


def verify(path):
    fails = []
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as exc:
        return ["cannot read the trace: %s" % exc]
    if not isinstance(doc, dict) or not isinstance(doc.get("entry_points_read"), list) or not doc["entry_points_read"]:
        return ["entry_points_read is missing or empty"]
    for entry in doc["entry_points_read"]:
        if not isinstance(entry, str) or not os.path.isfile(entry):
            fails.append("entry point %r is not a file" % (entry,))
    rows = doc.get("dependencies")
    if not isinstance(rows, list) or not rows:
        return fails + ["dependencies is missing or empty"]
    for i, row in enumerate(rows):
        tag = "row %d" % i
        if not isinstance(row, dict):
            fails.append("%s is not an object" % tag)
            continue
        site = row.get("site")
        if not isinstance(site, str) or ":" not in site:
            fails.append("%s site %r is not path:line" % (tag, site))
            continue
        file_path, _, line_no = site.rpartition(":")
        try:
            number = int(line_no)
            with open(file_path, encoding="utf-8") as fh:
                lines = fh.read().split("\n")
            actual = lines[number - 1].strip()
        except (OSError, ValueError, IndexError):
            fails.append("%s site %s does not exist" % (tag, site))
            continue
        if not isinstance(row.get("line_text"), str) or row["line_text"].strip() != actual or not actual:
            fails.append("%s line_text does not equal %s" % (tag, site))
        if row.get("needs_ycharts_id_for_yahoo_priced_holding") not in NEEDS:
            fails.append("%s needs_ycharts_id_for_yahoo_priced_holding is %r (want YES or NO)" % (tag, row.get("needs_ycharts_id_for_yahoo_priced_holding")))
        if row.get("claim") not in CLAIMS:
            fails.append("%s claim is %r (want MEASURED or INFERRED)" % (tag, row.get("claim")))
        for key in ("what", "removal"):
            if not isinstance(row.get(key), str) or len(row[key].strip()) < 10:
                fails.append("%s %s is missing" % (tag, key))
        if row.get("needs_ycharts_id_for_yahoo_priced_holding") == "YES" and not (isinstance(row.get("id_source"), str) and row["id_source"].strip()):
            fails.append("%s needs=YES but names no id_source" % tag)
    summary = doc.get("summary")
    yes = sum(1 for r in rows if isinstance(r, dict) and r.get("needs_ycharts_id_for_yahoo_priced_holding") == "YES")
    if not isinstance(summary, dict) or summary.get("dependencies") != len(rows) or summary.get("needs_yes") != yes:
        fails.append("summary %r does not equal the rows (%d rows, %d YES)" % (summary, len(rows), yes))
    return fails


def scope(base_ref, folder, order):
    rc = subprocess.run(["git", "merge-base", "HEAD", base_ref], capture_output=True)
    base = rc.stdout.decode().strip()
    if rc.returncode != 0 or not base:
        return ["no merge-base with %s" % base_ref]
    diff = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True)
    if diff.returncode != 0:
        return ["git diff rc=%d" % diff.returncode]
    names = [n for n in diff.stdout.decode().splitlines() if n.strip()]
    prefix = folder.rstrip("/") + "/"
    issuer = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/",
              "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/", "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/task_orders/")
    stray = [n for n in names if not n.startswith(prefix) and n not in (order, CHANNEL) and not n.startswith(issuer)]
    return ["outside the cell's write set: %s" % ", ".join(stray)] if stray else []


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "verify":
        fails = verify(sys.argv[2])
        print("AR-G134-%s %s" % ("FAIL" if fails else "OK", "; ".join(fails) if fails else "trace verified"))
        return 1 if fails else 0
    if len(sys.argv) == 5 and sys.argv[1] == "scope":
        fails = scope(sys.argv[2], sys.argv[3], sys.argv[4])
        print("AR-G134-SCOPE-%s %s" % ("FAIL" if fails else "OK", "; ".join(fails)))
        return 1 if fails else 0
    print("AR-G134-FAIL usage: verify <trace json> | scope <base ref> <worker folder> <order path>")
    return 2


if __name__ == "__main__":
    sys.exit(main())
